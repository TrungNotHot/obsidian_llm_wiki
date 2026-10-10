---
name: kb-index
description: Rebuilds index pages, glossary, and concept maps.
---

# /kb-index Skill

Rebuilds `index.md`, organizes glossary terms, and regenerates knowledge navigation maps.

## Purpose
Ensures that as the wiki grows, developers and AI agents can always navigate the entire vault through a unified, self-updating master catalog without requiring complex vector infrastructure.

> Refer to `references/wiki-guidelines.md` for standard directory conventions and catalog organization.

## Workflow Steps:

1. **Scan the Entire Vault**:
   - Traverse all subdirectories under `wiki/` (e.g. system architecture, domain models, concepts, entities).
   - Traverse `reports/` and `raw/`.

2. **Extract Metadata**:
   - Read titles, summaries, tags, and cross-references from frontmatter and headings.

3. **Rebuild `index.md`**:
   - **System Overview & Quick Links**: Fast links to core reports, synthesis documents, and the active operations log.
   - **Architecture & System Modules**: Grouped dynamically by the discovered architectural layers or component subdirectories.
   - **Concepts Map**: Categorized by architectural themes, design patterns, or technical mechanisms based on note tags.
   - **Entities Registry**: External systems, platforms, databases, and third-party APIs.
   - **Glossary of Terms**: Alphabetical quick-reference table of core domain terms and acronyms.
   - **Compounding Reports**: Chronological catalog of generated reports with concise one-line summaries.

3b. **Guardrail before overwriting `index.md`** (it is the entry point of every other skill and is gitignored, so git cannot restore it):
   - Compare the rebuilt catalog with the current `index.md`: count entries **added**, **removed** and **changed**, and reuse existing hand-written summaries instead of rewriting them.
   - If any entry is **removed**, or **10 or more** entries are added/changed, show the user this summary (with the removed entries) and **ask for confirmation before writing**.
   - If only a few notes changed, edit the affected entries in place instead of regenerating the whole file.

4. **Log the Operation**:
   - Append to `log.md`:
     ```markdown
     ## [YYYY-MM-DD] Index | Rebuilt Knowledge Catalog & Glossary
     - Cataloged X concepts, Y entities, Z architecture notes, W reports.
     ```
