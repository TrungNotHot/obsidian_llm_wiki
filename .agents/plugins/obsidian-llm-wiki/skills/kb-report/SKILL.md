---
name: kb-report
description: Given a question, searches wiki, writes a full report into reports/.
---

# /kb-report Skill

Given a question or investigation topic, searches the knowledge wiki and codebase, and writes a comprehensive, permanent report into `reports/`.

## Purpose
Enforces the core Karpathy / `@polydao` principle: **"Never Answer in Chat, Always Answer in Files"**. Every serious question becomes a permanent compounding asset in your vault.

> Refer to `references/wiki-guidelines.md` for report formatting standards, wikilink syntax, and core vault principles.

## Workflow Steps:

1. **Step 0 — Session Orientation**:
   - Read `SCHEMA.md` and `index.md` to identify candidate topics, existing entities, and previous investigation reports.
   - Scan the last 20 lines of `log.md` to see recent queries or investigations.

2. **Step 1 — Search & Read Context**:
   - Query across `wiki/` (concepts, entities, and architecture).
   - Cross-check with source code in primary codebase directories (e.g. `src/`, `app/`, `lib/`) when code-level verification is needed.

3. **Step 2 — Synthesize & Author Report**:
   - Create a new report file: `reports/YYYY-MM-DD-<topic_slug>.md`.
   - Use standard frontmatter conforming to `SCHEMA.md`:
     ```yaml
     ---
     title: "Report Title"
     created: YYYY-MM-DD
     type: report
     tags:
       - report
       - <domain-tag>
     confidence: high | medium
     contested: false
     contradictions: []
     status: published
     ---
     ```
   - Structure the report:
     - **Executive Summary**: 2-3 sentence high-level takeaway.
     - **Detailed Technical Analysis**: Technical breakdown, interfaces, data models, or logic flow.
     - **Mermaid Diagrams**: Visual architecture, sequence, or ER diagrams.
     - **Backlinks & References**: Obsidian wikilinks `[[...]]` connecting to relevant concept notes and entities.

4. **Step 3 — Compounding Loop (File Back to Wiki)**:
   - *Karpathy Principle*: Good answers should compound in the knowledge base, not stay trapped in reports.
   - If the investigation uncovered a reusable architectural concept, core domain rule, or comparative matrix:
     - Extract an atomic note into `wiki/concepts/<slug>.md` or `wiki/entities/<slug>.md`.
     - Link the report to this atomic note and vice-versa.

5. **Step 4 — Update Catalog & Log**:
   - Add the report link to `index.md` under the Reports section.
   - Append to `log.md`:
     ```markdown
     ## [YYYY-MM-DD] Report | <Report Title>
     - Question investigated: "<User Query>"
     - Report created: `reports/YYYY-MM-DD-<topic_slug>.md`
     - Compounding concepts extracted: None (or list `[[ConceptSlug]]`)
     ```
