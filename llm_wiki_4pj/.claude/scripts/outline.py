#!/usr/bin/env python3
"""
Candidate outline for /kb-ask and /kb-report (stdlib only, no scoring, no model).

Collects notes reachable from seed notes within N hops (outbound links + backlinks) and prints one
compact block per note: path, hop, title, tags, confidence and ALL headings. The LLM reads these
outlines (level 1) and picks which notes to read in full (level 2).

  outline.py <vault> --seeds a,b --hops 2 [--limit 40] [--max-headings 25]
  outline.py --selftest
"""

import argparse
import re
import sys
import tempfile
from pathlib import Path

SKIP_STEMS = {"index", "log", "TODO", "README", "SCHEMA"}  # exact names only; "logging-x" is a real note
LINK = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")


def skip(stem):
    base = stem.split(".")[0]  # index.example -> index
    return base in SKIP_STEMS or re.fullmatch(r"log-\d{4}", base) is not None


def parse(path):
    raw = path.read_text(encoding="utf-8", errors="ignore")
    m = re.match(r"^---\n(.*?)\n---\n?", raw, re.DOTALL)
    fm, body = (m.group(1), raw[m.end():]) if m else ("", raw)
    title = (re.search(r'^title:\s*"?(.*?)"?\s*$', fm, re.M) or [None, path.stem])[1]
    conf = (re.search(r"^confidence:\s*(\w+)", fm, re.M) or [None, ""])[1].lower()
    inline = re.search(r"^tags:\s*\[(.*?)\]", fm, re.M)
    if inline:
        tags = [t.strip().strip("\"'") for t in inline.group(1).split(",") if t.strip()]
    else:
        block = re.search(r"^tags:\s*\n((?:\s+-\s+.*\n?)+)", fm, re.M)
        tags = [t.strip().strip("\"'") for t in re.findall(r"-\s+(.*)", block.group(1))] if block else []
    plain = re.sub(r"```.*?```", "", body, flags=re.DOTALL)  # '#' inside code is not a heading
    heads = [(len(h), t.strip()) for h, t in re.findall(r"^(#{1,6})\s+(.*)$", plain, re.M)]
    links = {Path(x.strip()).name for x in LINK.findall(plain)}
    return {"title": title, "tags": tags, "heads": heads, "conf": conf, "links": links}


def load(vault):
    notes = {}
    for f in vault.glob("**/*.md"):
        rel = f.relative_to(vault).parts
        if any(p.startswith(".") for p in rel) or rel[0] == "raw" or "_archive" in rel or skip(f.stem):
            continue
        n = parse(f)
        n["path"] = "/".join(rel)
        notes[f.stem] = n
    return notes


def reach(notes, seeds, hops):
    """BFS over outbound links and backlinks. Returns {stem: hop}."""
    back = {k: set() for k in notes}
    for k, v in notes.items():
        for t in v["links"]:
            if t in back:
                back[t].add(k)
    dist = {s: 0 for s in seeds if s in notes}
    frontier = list(dist)
    for h in range(1, hops + 1):
        nxt = []
        for k in frontier:
            for t in (notes[k]["links"] & notes.keys()) | back[k]:
                if t not in dist:
                    dist[t] = h
                    nxt.append(t)
        frontier = nxt
    return dist


def render(notes, dist, limit, max_heads):
    order = sorted(dist, key=lambda k: (dist[k], k))
    out = [f"candidates: {len(order)}" + (f" (showing first {limit}; narrow --seeds/--hops)" if len(order) > limit else "")]
    for k in order[:limit]:
        n = notes[k]
        head = f"[hop {dist[k]}] {n['path']} | title: {n['title']}"
        if n["tags"]:
            head += f" | tags: {', '.join(n['tags'])}"
        if n["conf"]:
            head += f" | confidence: {n['conf']}"
        out.append(head)
        hs = n["heads"][:max_heads]
        if hs:
            out.append("   " + " > ".join(f"{'#' * lvl} {t}" for lvl, t in hs) + (" ..." if len(n["heads"]) > max_heads else ""))
    return "\n".join(out)


def selftest():
    with tempfile.TemporaryDirectory() as d:
        v = Path(d)
        for sub in ("wiki", "raw", ".claude"):
            (v / sub).mkdir()
        (v / "wiki/a.md").write_text('---\ntitle: "Alpha"\ntags: [x, y]\nconfidence: high\n---\n# Alpha\n## Init\nsee [[b]]\n```\n# not a heading\n```\n')
        (v / "wiki/b.md").write_text("---\ntitle: Beta\ntags:\n  - z\n---\n## Beta part\nback [[a]] and [[c]]\n")
        (v / "wiki/c.md").write_text("# Gamma\n")
        (v / "wiki/far.md").write_text("# Far\nlinks [[c]]\n")
        (v / "wiki/logging-design.md").write_text("# Logging\n")
        (v / "wiki/index.md").write_text("# index\n")
        (v / "raw/a.md").write_text("# raw twin\n")
        (v / ".claude/s.md").write_text("# hidden\n")
        notes = load(v)
        assert "logging-design" in notes and "index" not in notes and ".claude" not in "".join(n["path"] for n in notes.values())
        assert [t for _, t in notes["a"]["heads"]] == ["Alpha", "Init"], "code-block # is not a heading"
        assert notes["a"]["tags"] == ["x", "y"] and notes["b"]["tags"] == ["z"]
        assert reach(notes, ["a"], 1) == {"a": 0, "b": 1}
        assert reach(notes, ["a"], 2) == {"a": 0, "b": 1, "c": 2}  # c reached via b; far (3 hops) not yet
        assert "far" not in reach(notes, ["a"], 2) and reach(notes, ["a"], 3).get("far") == 3
        txt = render(notes, reach(notes, ["a"], 1), 40, 25)
        assert "[hop 0] wiki/a.md | title: Alpha | tags: x, y | confidence: high" in txt and "# Alpha > ## Init" in txt, txt
        assert "showing first 1" in render(notes, reach(notes, ["a"], 1), 1, 25)
    print("selftest ok")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vault", nargs="?", default=".")
    ap.add_argument("--seeds", default="", help="comma-separated note names (no extension)")
    ap.add_argument("--hops", type=int, default=2)
    ap.add_argument("--limit", type=int, default=40, help="max notes printed")
    ap.add_argument("--max-headings", type=int, default=25, help="max headings printed per note")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    vault = Path(a.vault)
    if not vault.is_dir():
        sys.exit(f"Error: '{vault}' is not a directory")
    notes = load(vault)
    seeds = [s.strip() for s in a.seeds.split(",") if s.strip()]
    if not seeds:
        sys.exit("Error: --seeds is required (whole-vault outline is intentionally unsupported)")
    missing = [s for s in seeds if s not in notes]
    if missing:
        print(f"warning: seed(s) not found (use the file name without .md): {', '.join(missing)}", file=sys.stderr)
    dist = reach(notes, seeds, a.hops)
    print(render(notes, dist, a.limit, a.max_headings))


if __name__ == "__main__":
    main()
