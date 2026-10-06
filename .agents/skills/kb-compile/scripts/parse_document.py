#!/usr/bin/env python3
"""
Document Converter for Obsidian LLM Wiki.
Converts PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx), and Images
into clean Markdown in raw/articles/ using Microsoft MarkItDown with SHA-256 caching.
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".pptx", ".xlsx",
    ".doc", ".ppt", ".xls",
    ".png", ".jpg", ".jpeg", ".webp"
}


def compute_sha256(file_path: Path) -> str:
    """Compute hex SHA-256 digest of binary file."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def slugify(text: str) -> str:
    """Normalize filename stem to a clean, lowercase hyphen-separated slug."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    slug = re.sub(r"[-\s]+", "-", text).strip("-")
    return slug or "unnamed-document"


def get_cached_sha256(md_path: Path) -> str | None:
    """Extract sha256 from existing markdown frontmatter if present."""
    if not md_path.exists():
        return None
    try:
        content = md_path.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"^sha256:\s*([a-fA-F0-9]{64})", content, re.MULTILINE)
        if match:
            return match.group(1).lower()
    except Exception:
        pass
    return None


def convert_file(
    file_path: Path,
    output_dir: Path,
    vault_root: Path,
    force: bool = False
) -> dict:
    """Convert a single binary document to Markdown."""
    if not file_path.is_file():
        return {"file": str(file_path), "status": "error", "message": "File not found"}

    ext = file_path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        return {
            "file": str(file_path),
            "status": "skipped",
            "message": f"Unsupported extension '{ext}'. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        }

    sha256 = compute_sha256(file_path)
    slug = slugify(file_path.stem)
    out_file = output_dir / f"{slug}.md"

    # Relative path from vault root for auditability
    try:
        rel_source = file_path.relative_to(vault_root).as_posix()
    except ValueError:
        rel_source = file_path.as_posix()

    try:
        rel_output = out_file.relative_to(vault_root).as_posix()
    except ValueError:
        rel_output = out_file.as_posix()

    # Check cache
    if not force:
        cached_hash = get_cached_sha256(out_file)
        if cached_hash == sha256.lower():
            return {
                "file": rel_source,
                "output": rel_output,
                "status": "cached",
                "sha256": sha256,
                "message": "SHA-256 match, skipped re-conversion"
            }

    # Convert using markitdown
    try:
        from markitdown import MarkItDown
    except ImportError:
        print(
            "Error: markitdown is not installed. Please run with:\n"
            "  uv run --with \"markitdown[all]\" python3 parse_document.py <file>",
            file=sys.stderr
        )
        sys.exit(1)

    try:
        md = MarkItDown()
        result = md.convert(str(file_path))
        body = (result.text_content or "").strip()
    except Exception as e:
        return {
            "file": rel_source,
            "status": "error",
            "message": f"Conversion failed: {str(e)}"
        }

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    title = file_path.stem.replace("_", " ").replace("-", " ").title()

    frontmatter = (
        "---\n"
        f"title: \"{title}\"\n"
        f"source_file: {rel_source}\n"
        f"original_type: {ext.lstrip('.')}\n"
        f"ingested: {today}\n"
        f"sha256: {sha256}\n"
        "---\n\n"
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    out_file.write_text(frontmatter + body + "\n", encoding="utf-8")

    return {
        "file": rel_source,
        "output": rel_output,
        "status": "converted",
        "sha256": sha256,
        "lines": len(body.splitlines())
    }


def find_vault_root() -> Path:
    """Find vault root by walking up from script location first, then cwd."""
    # 1. Walk up from script file location
    curr = Path(__file__).resolve().parent
    for _ in range(6):
        if (
            (curr / "SCHEMA.md").exists()
            or (curr / "raw").exists()
            or (curr / "docs" / "SCHEMA.md").exists()
            or (curr / "docs" / "raw").exists()
        ):
            return curr
        if curr.parent == curr:
            break
        curr = curr.parent

    # 2. Fallback to CWD
    curr = Path.cwd().resolve()
    for _ in range(6):
        if (
            (curr / "SCHEMA.md").exists()
            or (curr / "raw").exists()
            or (curr / "docs" / "SCHEMA.md").exists()
            or (curr / "docs" / "raw").exists()
        ):
            return curr
        if curr.parent == curr:
            break
        curr = curr.parent

    return Path.cwd().resolve()


def main():
    vault_root = find_vault_root()
    is_project_docs = (vault_root / "docs" / "raw").exists()
    auto_scan_dir = "docs/raw/binary" if is_project_docs else "raw/binary"
    auto_output_dir = "docs/raw/articles" if is_project_docs else "raw/articles"

    parser = argparse.ArgumentParser(
        description="Convert binary documents (PDF, DOCX, PPTX, XLSX, Images) to Markdown for Obsidian LLM Wiki."
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to binary file to convert. If omitted, scans --scan-dir."
    )
    parser.add_argument(
        "--scan-dir",
        default=auto_scan_dir,
        help=f"Directory of binary files to scan when no file is specified (default: {auto_scan_dir})"
    )
    parser.add_argument(
        "--output-dir",
        default=auto_output_dir,
        help=f"Output directory for generated markdown (default: {auto_output_dir})"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-conversion even if SHA-256 matches"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result in JSON format"
    )

    args = parser.parse_args()
    vault_root = find_vault_root(Path.cwd())
    output_dir = (vault_root / args.output_dir).resolve()

    results = []

    if args.file:
        target = Path(args.file)
        if not target.is_absolute():
            target = (vault_root / target).resolve()
        res = convert_file(target, output_dir, vault_root, force=args.force)
        results.append(res)
    else:
        scan_path = (vault_root / args.scan_dir).resolve()
        if not scan_path.exists():
            print(f"Error: Scan directory '{scan_path}' does not exist.", file=sys.stderr)
            sys.exit(1)

        files = [
            f for f in scan_path.iterdir()
            if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
        ]

        if not files:
            if args.json:
                print(json.dumps({"results": [], "message": f"No binary documents found in {scan_path}"}))
            else:
                print(f"ℹ️  No binary documents found in {scan_path}.")
            return

        for f in sorted(files):
            res = convert_file(f, output_dir, vault_root, force=args.force)
            results.append(res)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    print("=== Document Ingestion (MarkItDown) ===")
    for r in results:
        status_icon = "✅" if r["status"] == "converted" else ("⚡" if r["status"] == "cached" else "❌")
        if r["status"] == "converted":
            print(f"{status_icon} Converted: {r['file']} -> {r['output']} ({r.get('lines', 0)} lines)")
        elif r["status"] == "cached":
            print(f"{status_icon} Cached:    {r['file']} -> {r['output']} (SHA-256 match)")
        else:
            print(f"{status_icon} Failed:    {r['file']} - {r.get('message', '')}")


if __name__ == "__main__":
    main()
