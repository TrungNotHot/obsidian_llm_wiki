# Obsidian LLM Wiki Guidelines

You are the maintainer and librarian of this project's local knowledge base.
Obsidian is the viewer/IDE; you are the compiler and programmer; markdown files in `./` are the living codebase.

## 1. Core Principles
- **Orientation Before Action**: Before ingesting, querying, or modifying notes, always read `index.md` and scan the last 20-30 lines of `log.md` (along with `SCHEMA.md`) to establish context and avoid duplicating existing pages.
- **Never Answer in Chat, Always Answer in Files**: Whenever producing complex architectural syntheses, component analyses, or investigation reports, save them as permanent structured markdown assets in `reports/`.
- **Immutable Raw Layer**: Never modify files inside `raw/`. They are immutable reference documents.
- **Maintain Compounding Knowledge**: Every new finding or report should backlink to relevant concepts, components, or entities using Obsidian wikilinks `[[filename_without_extension]]`.
- **Living Documentation**: Maintain active system architecture and design notes inside `wiki/`, keeping them synchronized with codebase changes.
- **Explicit Conflict Management**: Never silently overwrite conflicting claims. Note contradictions with dates/sources, and flag `contested: true` per `SCHEMA.md`.
- **Mass-Update Guardrail**: Always confirm with the user before applying edits if an ingestion or refactor touches 10 or more existing pages.
- **Log Rotation**: When `log.md` exceeds 500 entries, rotate to `log-YYYY.md` and start fresh.

## 2. Directory Conventions
- `SCHEMA.md`: Internal constitutional schema, tag taxonomy, and page thresholds.
- `raw/`: Sources, web clips, external specs, and raw reference documents (read-only).
- `wiki/concepts/`: Atomic architectural & domain concepts.
- `wiki/entities/`: Systems, platforms, tools, and external services.
- `wiki/_archive/`: Superseded, deprecated, or decommissioned notes.
- `reports/`: Compiled reports, presentations, and query syntheses.
- `index.md`: Central catalog — must be updated whenever new pages are created or archived.
- `log.md`: Chronological log — append an entry: `## [YYYY-MM-DD] <Action> | <Summary>`.

## 3. Wikilink Syntax & Frontmatter Standard
- Always use `[[NoteName]]` or `[[Folder/NoteName|Display Name]]`.
- Add YAML frontmatter to newly generated knowledge pages:
  ```yaml
  ---
  title: "Page Title"
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  type: concept | entity | comparison | query | report | architecture
  tags:
    - architecture
    - <domain-tag>
  sources:
    - raw/... # optional
  confidence: high # high | medium | low
  contested: false # true if conflicting with another note
  contradictions: [] # [slug-of-conflicting-note]
  status: published
  ---
  ```

## 4. Canonical Skills
- `/kb-compile`: Ingests sources (local or URL), summarizes, and creates/updates pages in `wiki/`.
- `/kb-index`: Rebuilds `index.md`, organizes glossary, and refreshes concept maps.
- `/kb-health`: Runs script-assisted vault checks (broken links, orphans, stale notes), audits code-doc drift, and logs to `wiki/TODO.md`.
- `/kb-report`: Queries wiki and codebase, writes reports in `reports/`, and files back reusable atomic concepts into `wiki/`.
