#!/usr/bin/env python3
"""
Obsidian LLM Wiki Health Checker.
Audits vault integrity: broken links, orphan notes, contested claims, and oversized pages.
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def audit_vault(vault_path: Path):
    if not vault_path.exists() or not vault_path.is_dir():
        print(f"Error: Vault path '{vault_path}' does not exist or is not a directory.", file=sys.stderr)
        sys.exit(1)

    wiki_dir = vault_path / "wiki"

    def visible(f: Path) -> bool:
        # Skip hidden files/dirs (.claude, .agents, .obsidian) relative to the vault.
        return not any(part.startswith(".") for part in f.relative_to(vault_path).parts)

    md_files = [
        f for f in vault_path.glob("**/*.md")
        if visible(f) and "_archive" not in f.parts
    ]

    # Wikilinks resolve by note name (any folder, incl. raw/ specs); attachments (![[img.png]])
    # resolve against non-md files by name.
    all_stems = {f.stem: f for f in md_files}
    # Names backed by a note outside raw/ (so a same-named raw/ copy can't mask a missing note).
    non_raw_stems = {f.stem for f in md_files if f.relative_to(vault_path).parts[0] != "raw"}
    attachments = {f.name for f in vault_path.glob("**/*") if f.is_file() and f.suffix != ".md" and visible(f)}
    inbound = {f.stem: 0 for f in wiki_dir.glob("**/*.md") if not f.name.startswith(".")} if wiki_dir.exists() else {}

    broken_links = []
    raw_only_links = []
    contested_pages = []
    oversized_pages = []
    stale_pages = []
    outdated_vs_source = []
    now = datetime.now(timezone.utc)

    link_pat = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")

    for f in md_files:
        try:
            raw = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        rel_path = f.relative_to(vault_path).as_posix()
        line_count = len(raw.splitlines())

        # Check page size threshold (>300 lines): wiki/ notes only (raw/ is immutable, reports are permanent)
        if line_count > 300 and rel_path.startswith("wiki/") and not f.name.startswith("TODO"):
            oversized_pages.append({"file": rel_path, "lines": line_count})

        # Parse YAML frontmatter
        fm_match = re.match(r"^---\n(.*?)\n---", raw, re.DOTALL)
        if fm_match:
            fm_text = fm_match.group(1)
            if re.search(r"^contested:\s*true\b", fm_text, re.MULTILINE):
                contested_pages.append(rel_path)

            # Check staleness (>90 days since updated date)
            upd_match = re.search(r"^updated:\s*(\d{4}-\d{2}-\d{2})", fm_text, re.MULTILINE)
            if upd_match:
                try:
                    upd_date = datetime.strptime(upd_match.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
                    if (now - upd_date).days > 90:
                        stale_pages.append({"file": rel_path, "updated": upd_match.group(1)})
                except ValueError:
                    pass

            # Page older than a source it cites: a cited raw/ file was ingested >90 days after the page's `updated`
            if upd_match:
                src_block = re.search(r"^sources:\s*(\[.*?\]|\n(?:\s+-\s+.*\n?)+)", fm_text, re.MULTILINE)
                for src in re.findall(r"raw/[^\s,\]#\"']+\.md", src_block.group(1)) if src_block else []:
                    sp = vault_path / src
                    if not sp.exists():
                        continue
                    ing = re.search(r"^ingested:\s*(\d{4}-\d{2}-\d{2})", sp.read_text(encoding="utf-8", errors="ignore"), re.MULTILINE)
                    if ing:
                        try:
                            gap = (datetime.strptime(ing.group(1), "%Y-%m-%d") - datetime.strptime(upd_match.group(1), "%Y-%m-%d")).days
                        except ValueError:
                            continue
                        if gap > 90:
                            outdated_vs_source.append({"file": rel_path, "updated": upd_match.group(1), "source": src, "ingested": ing.group(1)})

        # Strip YAML frontmatter: metadata fields (e.g. clipper `author: "[[name]]"`)
        # are plain-text by policy, never real wikilinks — ponytail: frontmatter
        # excluded from link scan so author artifacts can't flag as broken.
        body = re.sub(r"^---\n.*?\n---", "", raw, count=1, flags=re.DOTALL)

        # Strip code blocks and inline code to prevent false positives from documentation examples
        clean = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
        clean = re.sub(r"`.*?`", "", clean)

        for link in link_pat.findall(clean):
            target = Path(link.strip()).name
            if target in attachments:
                continue
            if target in all_stems:
                if target in inbound:
                    inbound[target] += 1
                if target not in non_raw_stems and rel_path.split("/")[0] != "raw":
                    raw_only_links.append({"source": rel_path, "target": link.strip()})
            else:
                broken_links.append({"source": rel_path, "target": link.strip()})

    orphans = [
        stem for stem, count in inbound.items()
        if count == 0 and not stem.startswith("TODO") and not stem.startswith("README")
    ]

    result = {
        "vault": str(vault_path),
        "total_files": len(md_files),
        "broken_links": broken_links,
        "raw_only_links": raw_only_links,
        "orphans": orphans,
        "contested": contested_pages,
        "oversized": oversized_pages,
        "stale": stale_pages,
        "outdated_vs_source": outdated_vs_source,
    }
    result.update(mechanical_checks(vault_path, md_files))
    return result


REQUIRED_FM = ("title", "created", "updated", "type", "tags")
NON_NOTE = ("README", "TODO", "index", "log")
TYPE_TAGS = {"concept", "entity", "comparison", "query", "report", "guide", "easy-read", "documentation", "architecture"}  # document-type tags say nothing about topic


def _fm(text):
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
    return (m.group(1), text[m.end():]) if m else ("", text)


def _list_field(fm, key):
    """Values of a YAML list field written inline `key: [a, b]` or as a `- a` block."""
    inline = re.search(rf"^{key}:\s*\[(.*?)\]", fm, re.MULTILINE)
    if inline:
        return [x.strip().strip("\"'") for x in inline.group(1).split(",") if x.strip()]
    block = re.search(rf"^{key}:\s*\n((?:\s+-\s+.*\n?)+)", fm, re.MULTILINE)
    return [x.strip().strip("\"'") for x in re.findall(r"-\s+(.*)", block.group(1))] if block else []


def _taxonomy(vault_path):
    """Allowed tags: backticked tags on `- **Group**: `a`, `b`` lines of SCHEMA.md (root or docs/)."""
    for cand in (vault_path / "SCHEMA.md", vault_path.parent / "SCHEMA.md"):
        if cand.exists():
            tags = set()
            for line in cand.read_text(encoding="utf-8", errors="ignore").splitlines():
                if re.match(r"^- \*\*[^*]+\*\*:\s*(`[a-z0-9-]+`(,\s*)?)+\s*$", line):
                    tags |= set(re.findall(r"`([a-z0-9-]+)`", line))
            return tags
    return set()


def mechanical_checks(vault_path, md_files):
    """Deterministic checks that used to be done by hand in the agent sweep."""
    rel = lambda f: f.relative_to(vault_path).as_posix()
    wiki = [f for f in md_files if rel(f).startswith("wiki/") and f.stem.split(".")[0] not in NON_NOTE]  # also skips TODO.example.md
    out = {"missing_in_index": None, "frontmatter_missing": [], "unknown_tags": None, "source_drift": [],
           "high_single_source": [], "low_confidence": [], "contradiction_clusters": [], "contradiction_pairs": []}
    index = vault_path / "index.md"
    if index.exists():
        itext = index.read_text(encoding="utf-8", errors="ignore")
        out["missing_in_index"] = [rel(f) for f in wiki
                                  if not re.search(r"\[\[(?:[^\]|]*/)?" + re.escape(f.stem) + r"(?:[|#\]])", itext)]
    allowed = _taxonomy(vault_path)
    if allowed:
        out["unknown_tags"] = []
    groups = {}
    note_tags, note_links = {}, {}
    for f in wiki:
        text = f.read_text(encoding="utf-8", errors="ignore")
        fm, body = _fm(text)
        note_links[f.stem] = {Path(x.strip()).name for x in re.findall(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]", re.sub(r"```.*?```", "", body, flags=re.DOTALL))}
        missing = [k for k in REQUIRED_FM if not re.search(rf"^{k}:", fm, re.MULTILINE)]
        tags = _list_field(fm, "tags")
        if "tags" not in missing and not tags:
            missing.append("tags")
        if missing:
            out["frontmatter_missing"].append({"file": rel(f), "missing": missing})
        if allowed:
            bad = [t for t in tags if t not in allowed]
            if bad:
                out["unknown_tags"].append({"file": rel(f), "tags": bad})
        conf = (re.search(r"^confidence:\s*(\w+)", fm, re.MULTILINE) or [None, ""])[1].lower()
        if conf == "low":
            out["low_confidence"].append(rel(f))
        if conf == "high" and len(_list_field(fm, "sources")) < 2:
            out["high_single_source"].append(rel(f))
        note_tags[f.stem] = set(tags)
        for t in tags:
            groups.setdefault(t, []).append(rel(f))
    # candidate groups for the contradiction review: specific tags (2-8 notes); broad tags group everything
    out["contradiction_clusters"] = [{"tag": t, "notes": sorted(v)} for t, v in
                                     sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])) if 2 <= len(v) <= 8]
    # linked wiki notes that share 2+ tags: close in topic and connected, so claims may overlap or conflict
    by_stem = {f.stem: rel(f) for f in wiki}
    seen = set()
    for a, links in note_links.items():
        for b in links & by_stem.keys() - {a}:
            key = tuple(sorted((a, b)))
            shared = sorted((note_tags.get(a, set()) & note_tags.get(b, set())) - TYPE_TAGS)
            if key not in seen and len(shared) >= 2:
                seen.add(key)
                out["contradiction_pairs"].append({"notes": [by_stem[key[0]], by_stem[key[1]]], "shared_tags": shared})
    for f in md_files:  # raw/ is immutable: a body that no longer matches its stored sha256 is source drift
        if not rel(f).startswith("raw/"):
            continue
        fm, body = _fm(f.read_text(encoding="utf-8", errors="ignore"))
        stored = re.search(r"^sha256:\s*([0-9a-f]{64})", fm, re.MULTILINE)
        if stored:
            variants = {body, body.lstrip("\n"), body.strip()}
            if stored.group(1) not in {hashlib.sha256(v.encode("utf-8")).hexdigest() for v in variants}:
                out["source_drift"].append(rel(f))
    return out


def main():
    parser = argparse.ArgumentParser(description="Audit Obsidian Knowledge Vault Integrity.")
    parser.add_argument("vault", nargs="?", default=".", help="Path to knowledge vault (default: .)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    vault_path = Path(args.vault)
    result = audit_vault(vault_path)

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print(f"=== Knowledge Vault Health Audit ===")
    print(f"Vault: {result['vault']} | Total Scanned Markdown Files: {result['total_files']}\n")

    print(f"🔴 Broken Links ({len(result['broken_links'])}):")
    for b in result["broken_links"][:10]:
        print(f"  - In {b['source']}: [[{b['target']}]]")
    if len(result["broken_links"]) > 10:
        print(f"  ... and {len(result['broken_links']) - 10} more")

    print(f"\n🟡 Links resolving only to raw/ ({len(result['raw_only_links'])}): verify the wiki note was not deleted/renamed")
    for r in result["raw_only_links"][:5]:
        print(f"  - In {r['source']}: [[{r['target']}]]")

    print(f"\n🟡 Contested Pages ({len(result['contested'])}):")
    for c in result["contested"]:
        print(f"  - {c}")

    print(f"\n🟡 Outdated vs cited source ({len(result['outdated_vs_source'])}): page `updated` is >90d older than a source it cites")
    for o in result["outdated_vs_source"][:10]:
        print(f"  - {o['file']} (updated {o['updated']}; {o['source']} ingested {o['ingested']})")

    print(f"\n🟡 Aging candidates, >90d since update ({len(result['stale'])}): age alone is not staleness; confirm a newer source on the same entities exists")
    for s in result["stale"][:10]:
        print(f"  - {s['file']} (last updated: {s['updated']})")

    print(f"\n🟢 Orphan Notes in wiki/ ({len(result['orphans'])}):")
    for o in result["orphans"][:10]:
        print(f"  - [[{o}]]")

    print(f"\nℹ️  Oversized Pages (>300 lines) ({len(result['oversized'])}):")
    for p in result["oversized"][:5]:
        print(f"  - {p['file']} ({p['lines']} lines)")

    def section(title, items, fmt, none_msg=None):
        if items is None:
            print(f"\nℹ️  {title}: skipped ({none_msg})")
            return
        print(f"\n🟡 {title} ({len(items)}):")
        for it in items[:10]:
            print("  - " + fmt(it))
        if len(items) > 10:
            print(f"  ... and {len(items) - 10} more")

    section("Not in index.md", result["missing_in_index"], str, "no index.md")
    section("Missing frontmatter fields", result["frontmatter_missing"], lambda x: f"{x['file']}: {', '.join(x['missing'])}")
    section("Tags outside SCHEMA.md taxonomy", result["unknown_tags"], lambda x: f"{x['file']}: {', '.join(x['tags'])}", "taxonomy not found in SCHEMA.md")
    section("Source drift (raw/ body != stored sha256)", result["source_drift"], str)
    section("confidence: high with fewer than 2 sources", result["high_single_source"], str)
    section("confidence: low", result["low_confidence"], str)
    print(f"\nℹ️  Contradiction-review clusters, specific tags with 2-8 notes ({len(result['contradiction_clusters'])}):")
    for c in result["contradiction_clusters"][:15]:
        print(f"  - {c['tag']} ({len(c['notes'])}): {', '.join(Path(n).stem for n in c['notes'])}")
    print(f"\nℹ️  Contradiction-review pairs, linked notes sharing 2+ tags ({len(result['contradiction_pairs'])}):")
    for c in result["contradiction_pairs"][:15]:
        print(f"  - {Path(c['notes'][0]).stem} <-> {Path(c['notes'][1]).stem} [{', '.join(c['shared_tags'])}]")

    print("\nAudit completed.")


if __name__ == "__main__":
    main()
