---
name: kb-report
description: Given a question, searches wiki, writes a full report into reports/.
---

# /kb-report Skill

Given a question or investigation topic, searches the knowledge wiki and codebase, and writes a comprehensive, permanent report into `reports/`.

## Purpose
Enforces the core Karpathy / `@polydao` principle: **"Never Answer in Chat, Always Answer in Files"**. Every serious question becomes a permanent compounding asset in your vault.

> Refer to `.agents/references/wiki-guidelines.md` for report formatting standards, wikilink syntax, and core vault principles.

## Workflow Steps:

1. **Step 0 — Session Orientation**:
   - Read `SCHEMA.md` and `index.md` to identify candidate topics, existing entities, and previous investigation reports.
   - Scan the last 20 lines of `log.md` to see recent queries or investigations.

2. **Step 1 — Search & Read Context**:
   - **Find relevant notes**: read `index.md` (if it is large, read the relevant sections or grep it). Analyze the question, identify the concepts it involves (including implied or related ones), and pick the best-matching entries by judgement. Read the folder `README.md` catalogs only if the index does not cover the topic. If no catalog entry matches, or before concluding the wiki lacks something, grep keywords (with synonyms) across `wiki/` and `reports/`.
   - **Read**: read the relevant notes in full (in parallel), most relevant first, until the topic is covered (typically 8-15 notes; stop earlier when covered). Follow `[[wikilinks]]` that point to something the report needs. Read the `contradictions:` partners of notes you read, and open `sources:` files in `raw/` when primary-source detail is needed. Keep a list of visited notes to cite in the report.
   - **Optional, expand with links**: when notes you read link to unseen notes that the question needs, or the catalog did not cover the topic, run `python3 .agents/scripts/outline.py . --seeds a,b --hops <1|2|3>` (`--seeds` = note file names without `.md`, **comma-separated, no spaces**). It lists neighbours (links and backlinks, including prior reports) with title, tags, confidence and all headings; choose the relevant ones yourself. **1 hop** for a fact lookup, **2** for relationships or summaries, **3** only for reasoning chains across 3+ notes. If it reports truncation, narrow `--seeds` or raise `--limit N` (max 100). If it fails, fall back to grep.
   - **Code cross-check (core step)**: when the wiki describes behavior implemented in code (DAGs, SQL, config), verify it against the real code in the primary codebase directories (e.g. `src/`, `app/`, `lib/`, `dags/`, `include/`) and record doc/code discrepancies. Skip only if the vault has no codebase.
   - **Web search (when wiki lacks enough info)**: ASK the user for permission first, stating what is missing. Never search silently. If approved, cite every web-sourced claim with its URL in the report and label it as unverified (not yet in `raw/`); set `confidence: medium` or lower.

3. **Step 2 — Synthesize & Author Report**:
   - Create a new report file: `reports/YYYY-MM-DD-<topic_slug>.md`.
   - Frontmatter follows the **Frontmatter Schema in `SCHEMA.md`** (single source of truth: fill every required field it lists, do not rely on a copy here). Report-specific: `type: report`, `tags` include `report` plus a domain tag from the taxonomy, `sources:` lists the wiki/raw notes the report relied on, `confidence` is not `high` unless backed by 2+ sources.
   - Structure the report:
     - **Executive Summary**: 2-3 sentence high-level takeaway.
     - **Detailed Technical Analysis**: Technical breakdown, interfaces, data models, or logic flow.
     - **Code Cross-check** (when code was checked): each doc/code discrepancy found, with the file and what differs.
     - **Mermaid Diagrams**: Visual architecture, sequence, or ER diagrams.
     - **Backlinks & References**: Obsidian wikilinks `[[...]]` connecting to relevant concept notes and entities.
     - **External Sources (required if any web/external info was used)**: a dedicated section listing each external source: URL/site, search query used, access date, and which report claims depend on it. Mark them unverified (not in `raw/`). Omit the section only if no external info was used.

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
