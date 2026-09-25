# Obsidian LLM Wiki Guidelines

You are the maintainer and librarian of this project's local knowledge base.
Obsidian is the viewer/IDE; you are the compiler and programmer; markdown files in `docs/` are the living codebase.

## 1. Core Principles
- **Orientation Before Action**: Before ingesting, querying, or modifying notes, always read `docs/index.md` and scan the last 20-30 lines of `docs/log.md` (along with `docs/SCHEMA.md`) to establish context and avoid duplicating existing pages.
- **Never Answer in Chat, Always Answer in Files**: Whenever producing complex architectural syntheses, component analyses, or investigation reports, save them as permanent structured markdown assets in `docs/reports/`.
- **Immutable Raw Layer**: Never modify files inside `docs/raw/`. They are immutable reference documents.
- **Maintain Compounding Knowledge**: Every new finding or report should backlink to relevant concepts, components, or entities using Obsidian wikilinks `[[filename_without_extension]]`.
- **Living Documentation**: Maintain active system architecture and design notes inside `docs/wiki/`, keeping them synchronized with codebase changes.
- **Explicit Conflict Management**: Never silently overwrite conflicting claims. Note contradictions with dates/sources, and flag `contested: true` per `docs/SCHEMA.md`.
- **Mass-Update Guardrail**: Always confirm with the user before applying edits if an ingestion or refactor touches 10 or more existing pages.
- **Log Rotation**: When `docs/log.md` exceeds 500 entries, rotate to `docs/log-YYYY.md` and start fresh.

## 2. Directory Conventions
- `docs/SCHEMA.md`: Internal constitutional schema, tag taxonomy, and page thresholds.
- `docs/raw/`: Sources, web clips, external specs, and raw reference documents (read-only).
- `docs/wiki/concepts/`: Atomic architectural & domain concepts.
- `docs/wiki/entities/`: Systems, platforms, tools, and external services.
- `docs/wiki/_archive/`: Superseded, deprecated, or decommissioned notes.
- `docs/reports/`: Compiled reports, presentations, and query syntheses.
- `docs/index.md`: Central catalog — must be updated whenever new pages are created or archived.
- `docs/log.md`: Chronological log — append an entry: `## [YYYY-MM-DD] <Action> | <Summary>`.

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
    - docs/raw/... # optional
  confidence: high # high | medium | low
  contested: false # true if conflicting with another note
  contradictions: [] # [slug-of-conflicting-note]
  status: published
  ---
  ```

## 4. Canonical Skills
- `/kb-compile`: Ingests sources (local or URL), summarizes, and creates/updates pages in `docs/wiki/`.
- `/kb-index`: Rebuilds `docs/index.md`, organizes glossary, and refreshes concept maps.
- `/kb-health`: Runs script-assisted vault checks (broken links, orphans, stale notes), audits code-doc drift, and logs to `docs/wiki/TODO.md`.
- `/kb-report`: Queries wiki and codebase, writes reports in `docs/reports/`, and files back reusable atomic concepts into `docs/wiki/`.
