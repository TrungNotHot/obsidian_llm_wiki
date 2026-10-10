#!/usr/bin/env python3
"""
Candidate outline for /kb-ask and /kb-report (stdlib only, no scoring, no model).

Collects notes reachable from seed notes within N hops (outbound links + backlinks) and prints one
compact block per note: path, hop, title, tags, confidence and ALL headings.
Order: nearest hop first, then most connected to the other candidates (then name). When --limit
truncates, the farthest and least connected notes are dropped; connectivity is not relevance. The LLM reads these
outlines (level 1) and picks which notes to read in full (level 2).

  outline.py <vault> --seeds a,b --hops 2 [--limit N] [--max-headings 25]   # --limit default: 20 / 40 / 60 for 1 / 2 / 3 hops
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


def default_limit(hops):
    return {1: 20, 2: 40}.get(hops, 60)  # 20 / 40 / 60 for 1 / 2 / 3+ hops


def render(notes, dist, limit, max_heads):
    # Order: nearest hop first; within a hop, the most connected to the other candidates first (then name),
    # so truncation by --limit drops the least connected notes, not the alphabetically last ones.
    back = {k: set() for k in dist}
    for k in dist:
        for t in notes[k]["links"]:
            if t in back:
                back[t].add(k)
    deg = {k: len((notes[k]["links"] | back[k]) & dist.keys()) for k in dist}
    order = sorted(dist, key=lambda k: (dist[k], -deg[k], k))
    note = f" (showing first {limit}, nearest hop then most connected; narrow --seeds first, then --hops)" if len(order) > limit else ""
    out = [f"candidates: {len(order)}{note}"]
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
        assert [default_limit(h) for h in (1, 2, 3, 4)] == [20, 40, 60, 60]
        big = {f"n{i}": {"links": set(), "title": "t", "tags": [], "conf": "", "heads": [], "path": f"wiki/n{i}.md"} for i in range(10)}
        first = render(big, {k: 0 for k in big}, 4, 25).splitlines()[0]
        assert "narrow --seeds first, then --hops" in first and "--limit" not in first, first  # truncated: narrow, never raise the limit
        assert "narrow" not in render(big, {k: 0 for k in big}, 10, 25).splitlines()[0]  # not truncated: no hint
        # truncation keeps the best connected note of a hop, not the alphabetically first
        (v / "wiki/b0.md").write_text("# B0\nlinks [[a]]\n")
        (v / "wiki/zhub.md").write_text("# Z\nlinks [[a]] [[b0]] [[b]]\n")
        n2 = load(v)
        top = render(n2, reach(n2, ["a"], 1), 2, 25).splitlines()
        assert any("zhub.md" in l for l in top) and not any("b0.md" in l for l in top), top  # seed first, then the most connected hop-1 note
    print("selftest ok")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vault", nargs="?", default=".")
    ap.add_argument("--seeds", default="", help="comma-separated note names (no extension)")
    ap.add_argument("--hops", type=int, default=2)
    ap.add_argument("--limit", type=int, default=None, help="max notes printed (default 20/40/60 for 1/2/3 hops)")
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
    print(render(notes, dist, a.limit or default_limit(a.hops), a.max_headings))


if __name__ == "__main__":
    main()
