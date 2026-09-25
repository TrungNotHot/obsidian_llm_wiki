# Raw Sources Layer (`raw/`)

This directory contains raw, immutable source documents that serve as the foundational truth for the knowledge base.

---

## 📂 Subdirectories

- **`articles/`**: Web articles, API specs, and technical references captured via **Obsidian Web Clipper** or `/kb-compile <url>`.
- **`assets/`**: Downloaded diagrams, architecture screenshots, and image attachments referenced by notes.
- **`superpowers/`**: System blueprints:
  - `specs/`: Technical design specifications.
  - `plans/`: Phased implementation plans.

---

## 🔒 Immutability & Drift Rules

1. **Immutable Source of Truth**: Files here are never edited after ingestion.
2. **Body Hashing (`sha256`)**: When capturing articles, the frontmatter records a `sha256` digest of the body. Re-ingesting the same URL verifies this hash to detect **Source Drift** and prevent duplicate processing.
3. **Living Notes Reference, Never Edit**: Active living notes in `wiki/` cite these raw documents via plain paths (e.g. `^[raw/articles/...]`), never modifying the original.
