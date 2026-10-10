---
name: kb-compile
description: Scans raw/, summarizes new docs, creates/updates pages in wiki/.
---

# /kb-compile Skill

Ingests new sources (local files in `docs/raw/` or direct URLs), extracts atomic concepts & entities, updates documentation in `docs/wiki/`, and maintains cross-references.

## Purpose
Acts as the automated librarian and compiler for incoming information (web articles, API specs, design documents, research notes). Ensures the knowledge base compounds over time without duplicate pages or unflagged contradictions.

> Governed by `docs/SCHEMA.md` and `.agents/references/wiki-guidelines.md`.

## Workflow Steps:

1. **Step 1 — Session Orientation (CRITICAL)**:
   - Read `docs/SCHEMA.md` to review the domain taxonomy and page thresholds.
   - Read `docs/index.md` to check existing pages and summaries.
   - Read the last 5 entries of `docs/log.md` to understand recent activity and prevent duplicating work.

2. **Step 2 — Source Capture (Binary Document, Local File, or URL)**:
   - **If a binary document (`.pdf`, `.docx`, `.pptx`, `.xlsx`, images) is provided or added to `docs/raw/binary/`**:
     - Convert the binary source into clean Markdown via the helper script:
       ```bash
       uv run --with "markitdown[all]" python3 .agents/scripts/parse_document.py <path_to_binary_file>
       # Or scan all unparsed documents:
       uv run --with "markitdown[all]" python3 .agents/scripts/parse_document.py
       ```
     - The script automatically handles SHA-256 caching, prevents duplicate conversion, and outputs to `docs/raw/articles/<slug>.md`.
     - Read the generated `docs/raw/articles/<slug>.md` in full to proceed with distillation.
   - **If a URL is provided**: Fetch the page as clean markdown with `read_url_content`.
     - Compute the `sha256` of the content body (UTF-8 text after the frontmatter, whitespace stripped; see `docs/SCHEMA.md`).
     - If the file already exists in `docs/raw/articles/`, compare the new hash with the stored `sha256`:
       - *Identical*: Skip re-compiling (source unchanged, saving tokens).
       - *Different*: Flag as **Source Drift** and proceed with compilation.
     - Save to `docs/raw/articles/<slug>.md` with frontmatter:
       ```yaml
       ---
       source_url: https://...
       ingested: YYYY-MM-DD
       sha256: <hex-digest-of-body>
       ---
       ```
   - **If local files in `docs/raw/`**: Inspect newly added or modified source files and read them in full.

3. **Step 3 — Distill & Check Thresholds**:
   - Identify core concepts, entities, architectural patterns, and business rules.
   - **Page Thresholds** (per `docs/SCHEMA.md`): Only create a dedicated page if an entity/concept appears in $\ge 2$ sources OR is central to this source. Avoid creating clutter for passing mentions.
   - For pages above the split threshold in `docs/SCHEMA.md`, decompose into sub-topics.
   - **Find related existing pages (before creating or editing)**:
     - Read `docs/index.md` (if it is large, read the relevant sections or grep it) and pick the entries matching the concepts/entities in the source (including broader or related ones) by judgement.
     - Before creating a new page, grep `docs/wiki/` for its name and synonyms: a miss here silently causes duplicate pages or missed contradictions. Read the matches.
     - For a page you will edit, you may run `python3 .agents/scripts/outline.py docs --seeds <those-pages> --hops 1` (note names without `.md`, comma-separated, no spaces) to see the pages it links to and from.
     - Update an existing page instead of creating a near-duplicate.
     - If this finds **10 or more** affected pages, apply the Mass-Update Guardrail below.
   - **Mass-Update Guardrail**: If the planned ingestion will touch **10 or more** existing wiki pages, summarize the affected notes and confirm the update scope with the user before applying edits.

4. **Step 4 — Update or Create Pages with Contradiction Handling**:
   - **Preview**: in an interactive run, before writing, show the user 3-5 key takeaways from the source and the list of pages you will create or update, then continue (the Mass-Update Guardrail still applies). Skip this in non-interactive or bulk runs.
   - **Concepts**: Save/update in `docs/wiki/concepts/universal/<slug>.md` (if general/reusable pattern) or `docs/wiki/concepts/local/<slug>.md` (if project-specific).
   - **Entities**: Save/update in `docs/wiki/entities/universal/<slug>.md` (if core platform/engine) or `docs/wiki/entities/local/<slug>.md` (if project-specific source/service).
   - **Contradiction Policy**: If new info conflicts with existing wiki content, **check dates first** (a newer source or current code generally supersedes an older one; update the page and say so). Only when the conflict is genuine and unresolved:
     - Document both claims with dates and source citations.
     - Set frontmatter: `contested: true` and `contradictions: [other-note-slug]`.
     - Set `confidence: medium` or `low` until reconciled.
   - **Confidence**: never set `high` without support from 2+ sources.
   - **Superseded pages**: if a page is fully replaced or decommissioned, follow the Archiving Workflow in `docs/SCHEMA.md` (move to `docs/wiki/_archive/`, drop from `docs/index.md`, mark inbound links `(archived)`, log it).
   - **Frontmatter**: follow the Frontmatter Schema in `docs/SCHEMA.md` (single source of truth: fill every required field, and set `updated:` when you edit an existing page). Use only tags from its taxonomy; to add a new tag, update `docs/SCHEMA.md` first, then use it.
   - Ensure minimum 2 outbound `[[wikilinks]]` per page.
   - **Provenance**: when a page synthesizes 3 or more sources, add `^[raw/source-file.md]` markers to its key paragraphs (see `docs/SCHEMA.md`).

5. **Step 5 — Bulk Ingest (When processing multiple sources)**:
   - Read all raw sources first.
   - Extract all candidate entities across all sources in one pass.
   - Check `docs/index.md` and search vault once to map existing vs new pages.
   - Write/update files in batch, then update index and log once.

6. **Step 6 — Log & Re-Index**:
   - Append to `docs/log.md`:
     ```markdown
     ## [YYYY-MM-DD] Compile | <Source Title>
     - Source: `raw/articles/<file>.md`
     - Created/Updated: `[[ConceptOrEntityPage]]`
     - Contradictions flagged: None (or list conflicting notes)
     ```
   - Update `docs/index.md` under the appropriate section, or invoke `/kb-index`.
   - **Report to the user** a short summary: pages created, pages updated, and contradictions flagged.
