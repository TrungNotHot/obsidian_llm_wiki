---
name: kb-compile
description: Scans raw/, summarizes new docs, creates/updates pages in wiki/.
---

# /kb-compile Skill

Ingests new sources (local files in `raw/` or direct URLs), extracts atomic concepts & entities, updates documentation in `wiki/`, and maintains cross-references.

## Purpose
Acts as the automated librarian and compiler for incoming information (web articles, API specs, design documents, research notes). Ensures the knowledge base compounds over time without duplicate pages or unflagged contradictions.

> Governed by `SCHEMA.md` and `references/wiki-guidelines.md`.

## Workflow Steps:

1. **Step 0 — Session Orientation (CRITICAL)**:
   - Read `SCHEMA.md` to review the domain taxonomy and page thresholds.
   - Read `index.md` to check existing pages and summaries.
   - Scan the last 20–30 lines of `log.md` to understand recent activity and prevent duplicating work.

2. **Step 1 — Source Capture (Binary Document, Local File, or URL)**:
   - **If a binary document (`.pdf`, `.docx`, `.pptx`, `.xlsx`, images) is provided or added to `raw/binary/`**:
     - Convert the binary source into clean Markdown via the helper script:
       ```bash
       uv run --with "markitdown[all]" python3 .agents/scripts/parse_document.py <path_to_binary_file>
       # Or scan all binary files:
       uv run --with "markitdown[all]" python3 .agents/scripts/parse_document.py
       ```
     - The script automatically handles SHA-256 caching, prevents duplicate conversion, and outputs to `raw/articles/<slug>.md`.
     - Read the generated `raw/articles/<slug>.md` in full to proceed with distillation.
   - **If a URL is provided**: Use `read_url_content` to extract clean markdown.
     - Compute the `sha256` hash of the content body.
     - If the file already exists in `raw/articles/`, compare the new hash with the stored `sha256`:
       - *Identical*: Skip re-compiling (source unchanged, saving tokens).
       - *Different*: Flag as **Source Drift** and proceed with compilation.
     - Save to `raw/articles/<slug>.md` with frontmatter:
       ```yaml
       ---
       source_url: https://...
       ingested: YYYY-MM-DD
       sha256: <hex-digest-of-body>
       ---
       ```
   - **If local files in `raw/`**: Inspect newly added or modified source files and read them in full.

3. **Step 2 — Distill & Check Thresholds**:
   - Identify core concepts, entities, architectural patterns, and business rules.
   - **Page Thresholds** (per `SCHEMA.md`): Only create a dedicated page if an entity/concept appears in $\ge 2$ sources OR is central to this source. Avoid creating clutter for passing mentions.
   - For pages reaching >300 lines, decompose into sub-topics.
   - **Find related existing pages (before creating or editing)**: grep `wiki/` for each candidate concept/entity name, synonyms, and `tags:`/`title:` in frontmatter (not only `index.md`) and read the matches. For each page you will edit, also read the pages it links to via `[[wikilinks]]` (1 hop) to check for contradictions and to find link targets. Update an existing page instead of creating a near-duplicate. If this finds **10 or more** affected pages, apply the Mass-Update Guardrail below.
   - **Mass-Update Guardrail**: If the planned ingestion will touch **10 or more** existing wiki pages, summarize the affected notes and confirm the update scope with the user before applying edits.

4. **Step 3 — Update or Create Pages with Contradiction Handling**:
   - **Concepts**: Save/update in `wiki/concepts/<slug>.md`.
   - **Entities**: Save/update in `wiki/entities/<slug>.md`.
   - **Contradiction Policy**: If new info conflicts with existing wiki content, **check dates first** (a newer source or current code generally supersedes an older one; update the page and say so). Only when the conflict is genuine and unresolved:
     - Document both claims with dates and source citations.
     - Set frontmatter: `contested: true` and `contradictions: [other-note-slug]`.
     - Set `confidence: medium` or `low` until reconciled.
   - **Confidence**: never set `high` without support from 2+ sources.
   - **Superseded pages**: if a page is fully replaced or decommissioned, follow the Archiving Workflow in `SCHEMA.md` (move to `wiki/_archive/`, drop from `index.md`, mark inbound links `(archived)`, log it).
   - Standard frontmatter:
     ```yaml
     ---
     title: "Page Title"
     created: YYYY-MM-DD
     updated: YYYY-MM-DD
     type: concept | entity | architecture
     tags: [from SCHEMA.md taxonomy]
     sources: [raw/...]
     confidence: high | medium | low
     contested: false
     contradictions: []
     status: published
     ---
     ```
   - Ensure minimum 2 outbound `[[wikilinks]]` per page.

5. **Step 4 — Bulk Ingest (When processing multiple sources)**:
   - Read all raw sources first.
   - Extract all candidate entities across all sources in one pass.
   - Check `index.md` and search vault once to map existing vs new pages.
   - Write/update files in batch, then update index and log once.

6. **Step 5 — Log & Re-Index**:
   - Append to `log.md`:
     ```markdown
     ## [YYYY-MM-DD] Compile | <Source Title>
     - Summarized: `[[SourceNote]]`
     - Created/Updated: `[[ConceptOrEntityPage]]`
     - Contradictions flagged: None (or list conflicting notes)
     ```
   - Update `index.md` under the appropriate section, or invoke `/kb-index`.
