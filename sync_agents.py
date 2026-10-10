#!/usr/bin/env python3
"""Regenerate each repo's .agents/ (Gemini/Antigravity) from its .claude/ (Claude Code) tree.

.claude/ is the source of truth. Differences applied: path prefix `.claude/` -> `.agents/`, and the
URL-fetch tool in kb-compile (`WebFetch` -> `read_url_content`). Edit .claude/, then run:

  python3 sync_agents.py          # write .agents/
  python3 sync_agents.py --check  # only report differences (exit 1 if any)
"""
import sys
from pathlib import Path

REPOS = ["obsidian_llm_wiki", "llm_wiki_4pj"]
SUBDIRS = ["skills", "scripts", "references"]
TOOL_SWAP = {"skills/kb-compile/SKILL.md": ("`WebFetch`", "`read_url_content`")}


def convert(rel, text):
    if not rel.endswith(".md"):  # scripts are copied verbatim
        return text
    text = text.replace(".claude/", ".agents/")
    if rel in TOOL_SWAP:
        text = text.replace(*TOOL_SWAP[rel])
    return text


def main():
    check = "--check" in sys.argv
    root = Path(__file__).parent
    diffs = 0
    for repo in REPOS:
        src, dst = root / repo / ".claude", root / repo / ".agents"
        for sub in SUBDIRS:
            for f in sorted((src / sub).rglob("*")):
                if not f.is_file():
                    continue
                rel = f.relative_to(src).as_posix()
                want = convert(rel, f.read_text(encoding="utf-8"))
                out = dst / rel
                have = out.read_text(encoding="utf-8") if out.exists() else None
                if have != want:
                    diffs += 1
                    print(f"{'DIFF' if check else 'write'}: {repo}/.agents/{rel}")
                    if not check:
                        out.parent.mkdir(parents=True, exist_ok=True)
                        out.write_text(want, encoding="utf-8")
            extra = [p for p in (dst / sub).rglob("*") if p.is_file() and not (src / p.relative_to(dst)).exists()] if (dst / sub).exists() else []
            for p in extra:
                print(f"EXTRA (only in .agents, not removed): {p.relative_to(root)}")
    print(f"{diffs} file(s) {'differ' if check else 'updated'}")
    return 1 if (check and diffs) else 0


if __name__ == "__main__":
    sys.exit(main())
