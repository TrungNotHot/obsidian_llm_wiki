#!/usr/bin/env python3
"""
Deterministic candidate ranker for /kb-ask and /kb-report (no model involved).

Gathers notes reachable from seed notes within N hops (outbound links + backlinks) and
scores them against the question: query terms found in title, tags, filename and ALL headings.

  rerank.py <vault> --query "kafka retry" [--seeds a,b] [--hops 2] [--top 12] [--json]
  rerank.py --selftest
"""

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

W_TITLE, W_TAGS, W_FILE, W_HEAD = 3.0, 2.0, 2.0, 1.0  # ponytail: hand-tuned weights, calibrate on real queries
CONF = {"high": 1.0, "medium": 0.0, "low": -1.0}
SKIP_STEMS = ("index", "log", "TODO", "README", "SCHEMA")
LINK = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")


def terms(text):
    return {t for t in re.findall(r"\w+", text.lower()) if len(t) > 1}


def parse(path):
    raw = path.read_text(encoding="utf-8", errors="ignore")
    m = re.match(r"^---\n(.*?)\n---\n?", raw, re.DOTALL)
    fm, body = (m.group(1), raw[m.end():]) if m else ("", raw)
    title = (re.search(r'^title:\s*"?(.*?)"?\s*$', fm, re.M) or [None, path.stem])[1]
    conf = (re.search(r"^confidence:\s*(\w+)", fm, re.M) or [None, ""])[1].lower()
    tags = ""
    inline = re.search(r"^tags:\s*\[(.*?)\]", fm, re.M)
    if inline:
        tags = inline.group(1)
    else:
        block = re.search(r"^tags:\s*\n((?:\s+-\s+.*\n?)+)", fm, re.M)
        tags = block.group(1) if block else ""
    plain = re.sub(r"```.*?```", "", body, flags=re.DOTALL)  # '#' inside code is not a heading
    heads = " ".join(re.findall(r"^#{1,6}\s+(.*)$", plain, re.M))
    links = {Path(l.strip()).name for l in LINK.findall(plain)}
    return {"title": title, "tags": tags, "heads": heads, "conf": conf, "links": links}


def load(vault):
    notes = {}
    for f in vault.glob("**/*.md"):
        rel = f.relative_to(vault).parts
        if any(p.startswith(".") for p in rel) or rel[0] in ("raw",) or "_archive" in rel:
            continue
        if f.stem.startswith(SKIP_STEMS):
            continue
        n = parse(f)
        n["path"] = "/".join(rel)
        notes[f.stem] = n
    return notes


def score(n, stem, q):
    fields = {"title": (W_TITLE, n["title"]), "tags": (W_TAGS, n["tags"]),
              "file": (W_FILE, stem.replace("-", " ").replace("_", " ")), "headings": (W_HEAD, n["heads"])}
    s, hit = 0.0, []
    for name, (w, text) in fields.items():
        t = terms(text)
        # substring match so "pod" finds "pods"; each query term counts once per field
        m = [x for x in q if x in t or any(x in y for y in t)]
        if m:
            s += w * len(m)
            hit.append(name)
    return s + CONF.get(n["conf"], 0.0), hit


def rank(notes, query, seeds=None, hops=2, top=12):
    q = terms(query)
    base = {k: score(v, k, q) for k, v in notes.items()}
    if not seeds:  # no seeds given: top scorers across the vault
        seeds = [k for k, _ in sorted(base.items(), key=lambda kv: -kv[1][0])[:3] if base[k][1]]
    back = {k: set() for k in notes}
    for k, v in notes.items():
        for t in v["links"]:
            if t in back:
                back[t].add(k)
    dist, frontier = {s: 0 for s in seeds if s in notes}, list(s for s in seeds if s in notes)
    reach = {k: 1 for k in dist}  # number of distinct neighbours that reached it
    for h in range(1, hops + 1):
        nxt = []
        for k in frontier:
            for t in (notes[k]["links"] & notes.keys()) | back[k]:
                reach[t] = reach.get(t, 0) + 1
                if t not in dist:
                    dist[t] = h
                    nxt.append(t)
        frontier = nxt
    rows = []
    for k, d in dist.items():
        s, hit = base[k]
        s += 0.5 * min(reach[k] - 1, 4) - 0.5 * d  # reached by several notes: bonus; far from seeds: small penalty
        rows.append({"note": k, "path": notes[k]["path"], "score": round(s, 2), "hop": d, "matched": hit})
    rows.sort(key=lambda r: (-r["score"], r["hop"], r["note"]))
    return {"candidates": len(rows), "seeds": [s for s in seeds if s in notes], "top": rows[:top]}


def selftest():
    with tempfile.TemporaryDirectory() as d:
        v = Path(d)
        (v / "wiki").mkdir()
        (v / "raw").mkdir()
        (v / "wiki/k8s-pods.md").write_text('---\ntitle: "Kubernetes Pods"\ntags: [container]\nconfidence: high\n---\n# Pods\n## Init containers\nsee [[k8s-volumes]]\n```\n# kafka comment in code\n```\n')
        (v / "wiki/k8s-volumes.md").write_text("---\ntitle: Volumes\ntags:\n  - storage\n---\n## emptyDir\nback [[k8s-pods]]\n")
        (v / "wiki/other.md").write_text("---\ntitle: Kafka\n---\n# Retry\n")
        (v / "raw/k8s-pods.md").write_text("# raw twin\n")
        r = rank(load(v), "pod init containers", hops=1)
        names = [x["note"] for x in r["top"]]
        assert names[0] == "k8s-pods", names  # title+tags+headings+file all match
        assert "k8s-volumes" in names and "other" not in names, names  # reached by link; unrelated note not a candidate
        assert "kafka" not in notes_heads(v), "code-block # must not count as heading"
        r0 = rank(load(v), "kafka", seeds=["k8s-pods"], hops=1)
        assert all(x["note"] != "other" for x in r0["top"])
    print("selftest ok")


def notes_heads(v):
    return parse(v / "wiki/k8s-pods.md")["heads"].lower()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vault", nargs="?", default=".")
    ap.add_argument("--query", default="")
    ap.add_argument("--seeds", default="", help="comma-separated note names; default: top scorers")
    ap.add_argument("--hops", type=int, default=2)
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    vault = Path(a.vault)
    if not vault.is_dir():
        sys.exit(f"Error: '{vault}' is not a directory")
    res = rank(load(vault), a.query, [s.strip() for s in a.seeds.split(",") if s.strip()], a.hops, a.top)
    if a.json:
        print(json.dumps(res, indent=2))
        return
    print(f"seeds: {', '.join(res['seeds']) or '(none)'} | candidates: {res['candidates']} | showing top {len(res['top'])}")
    for r in res["top"]:
        print(f"{r['score']:>6}  hop{r['hop']}  {r['path']}  [{', '.join(r['matched'])}]")


if __name__ == "__main__":
    main()
