#!/usr/bin/env python3
"""
Obsidian LLM Wiki Health Checker.
Audits vault integrity: broken links, orphan notes, contested claims, and oversized pages.
"""

import argparse
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
    md_files = [
        f for f in vault_path.glob("**/*.md")
        if not f.name.startswith(".") and "_archive" not in f.parts
    ]

    all_stems = {f.stem: f for f in md_files}
    inbound = {f.stem: 0 for f in wiki_dir.glob("**/*.md") if not f.name.startswith(".")} if wiki_dir.exists() else {}

    broken_links = []
    contested_pages = []
    oversized_pages = []
    stale_pages = []
    now = datetime.now(timezone.utc)

    link_pat = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")

    for f in md_files:
        try:
            raw = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        rel_path = f.relative_to(vault_path).as_posix()
        line_count = len(raw.splitlines())

        # Check page size threshold (>200 lines)
        if line_count > 200 and not f.name.startswith("index") and not f.name.startswith("TODO"):
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

        # Strip code blocks and inline code to prevent false positives from documentation examples
        clean = re.sub(r"```.*?```", "", raw, flags=re.DOTALL)
        clean = re.sub(r"`.*?`", "", clean)

        for link in link_pat.findall(clean):
            target = Path(link.strip()).name
            if target in all_stems:
                if target in inbound:
                    inbound[target] += 1
            else:
                broken_links.append({"source": rel_path, "target": link.strip()})

    orphans = [
        stem for stem, count in inbound.items()
        if count == 0 and not stem.startswith("TODO") and not stem.startswith("README")
    ]

    return {
        "vault": str(vault_path),
        "total_files": len(md_files),
        "broken_links": broken_links,
        "orphans": orphans,
        "contested": contested_pages,
        "oversized": oversized_pages,
        "stale": stale_pages,
    }


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

    print(f"\n🟡 Contested Pages ({len(result['contested'])}):")
    for c in result["contested"]:
        print(f"  - {c}")

    print(f"\n🟡 Stale Pages (>90d) ({len(result['stale'])}):")
    for s in result["stale"][:10]:
        print(f"  - {s['file']} (last updated: {s['updated']})")

    print(f"\n🟢 Orphan Notes in wiki/ ({len(result['orphans'])}):")
    for o in result["orphans"][:10]:
        print(f"  - [[{o}]]")

    print(f"\nℹ️  Oversized Pages (>200 lines) ({len(result['oversized'])}):")
    for p in result["oversized"][:5]:
        print(f"  - {p['file']} ({p['lines']} lines)")

    print("\nAudit completed.")


if __name__ == "__main__":
    main()
