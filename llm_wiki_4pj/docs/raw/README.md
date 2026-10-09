# Raw Sources Layer (`raw/`)

This directory contains raw, immutable source documents that serve as the foundational truth for the knowledge base.

---

## 📂 Subdirectories

- **`articles/`**: Web articles, API specs, and technical references captured via **Obsidian Web Clipper**, `/kb-compile <url>`, or converted from `binary/`.
- **`binary/`**: Immutable binary source documents (`.pdf`, `.docx`, `.pptx`, `.xlsx`, images) parsed into markdown via `parse_document.py` (`markitdown`).
- **`assets/`**: Downloaded diagrams, architecture screenshots, and image attachments referenced by notes.
- **`superpowers/`**: Historical system blueprints:
  - `specs/`: 13 technical design specifications.
  - `plans/`: 31 phased implementation plans.

---

## 🔒 Immutability & Drift Rules

1. **Immutable Source of Truth**: Files here are never edited after ingestion.
2. **Body Hashing (`sha256`)**: When capturing articles, the frontmatter records a `sha256` digest of the body. Re-ingesting the same URL verifies this hash to detect **Source Drift** and prevent duplicate processing.
3. **Living Notes Reference, Never Edit**: Active living notes in `docs/wiki/` cite these raw documents via plain paths (e.g. `^[docs/raw/articles/...]`), never modifying the original.
