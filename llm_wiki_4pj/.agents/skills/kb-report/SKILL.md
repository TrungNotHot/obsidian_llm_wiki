---
name: kb-report
description: Given a question, searches wiki, writes a full report into reports/.
---

# /kb-report Skill

Given a question or investigation topic, searches the knowledge wiki and codebase, and writes a comprehensive, permanent report into `docs/reports/`.

## Purpose
Enforces the core Karpathy / `@polydao` principle: **"Never Answer in Chat, Always Answer in Files"**. Every serious question becomes a permanent compounding asset in your vault.

> Refer to `references/wiki-guidelines.md` for report formatting standards, wikilink syntax, and core vault principles.

## Workflow Steps:

1. **Step 0 — Session Orientation**:
   - Read `docs/SCHEMA.md` and `docs/index.md` to identify candidate topics, existing entities, and previous investigation reports.
   - Scan the last 20 lines of `docs/log.md` to see recent queries or investigations.

2. **Step 1 — Search & Read Context**:
   - Find seed notes: analyze the question yourself, identify the concepts it involves (including implied, broader or related ones), and pick the best-covering entries from `docs/index.md` and the folder `README.md` catalogs (`docs/wiki/concepts/`, `docs/wiki/entities/`, `docs/wiki/easy_read/`) by judgement. Use grep on `title:`/`tags:` only to confirm or fill gaps, not as the primary selector. Before concluding the wiki lacks something, or when the catalog entries are too coarse to judge, run one keyword grep (with synonyms) across `docs/wiki/` and `docs/reports/` as a safety net.
   - **Traverse embedded references** (outline first, then full reads):
     - **Depth by question type**: **1 hop** for a fact lookup, **2 hops** for relationships or summaries, **3 hops** for multi-hop reasoning.
     - **Level 1 (outline)**: run `python3 .agents/scripts/outline.py docs --seeds <seed-notes> --hops <1|2|3>` (`<seed-notes>` = note file names without `.md`, **comma-separated, no spaces**, e.g. `--seeds note-a,note-b`). It lists every note reachable by links and backlinks within the hop limit (including prior reports in `docs/reports/`) with its title, tags, confidence and ALL headings (no scoring), nearest hop first. Read the outlines and **rerank them yourself** by relevance to the question. The output is capped (default 20 / 40 / 60 notes for 1 / 2 / 3 hops). If it says the list was truncated, rerun adjusting in this order: **1) `--seeds`** (drop weakly related seeds), **2) `--hops`** (only as far as the question type allows), **3) `--limit N`** (hard cap 100) when every seed is needed; outline entries are cheap, the read budget below is what controls cost. If the script fails, fall back to grep + your own judgement.
     - **Level 2 (full read)**: read in full at most **hops × min(5 + seeds, 12)** notes, where `seeds` = number of notes passed to `--seeds` (e.g. 6 / 12 / 18 with one seed, up to 12 / 24 / 36 with 7+ seeds; the seed notes already read in Step 1 are not counted), the most relevant first; if `candidates` is within the budget, skip the ranking and read them all. Also read the `contradictions:` partners of the notes you read, and open `sources:` files in `docs/raw/` when primary-source detail is needed.
     - If coverage is still thin, start a new traversal from a newly found seed instead of going deeper. Keep a list of visited notes to cite in the report.
   - Cross-check with source code in primary codebase directories (e.g. `src/`, `app/`, `lib/`) when code-level verification is needed.
   - **Web search (when wiki lacks enough info)**: ASK the user for permission first, stating what is missing. Never search silently. If approved, cite every web-sourced claim with its URL in the report and label it as unverified (not yet in `docs/raw/`); set `confidence: medium` or lower.

3. **Step 2 — Synthesize & Author Report**:
   - Create a new report file: `docs/reports/YYYY-MM-DD-<topic_slug>.md`.
   - Frontmatter follows the **Frontmatter Schema in `docs/SCHEMA.md`** (single source of truth: fill every required field it lists, do not rely on a copy here). Report-specific: `type: report`, `tags` include `report` plus a domain tag from the taxonomy, `sources:` lists the wiki/raw notes the report relied on, `confidence` is not `high` unless backed by 2+ sources.
   - Structure the report:
     - **Executive Summary**: 2-3 sentence high-level takeaway.
     - **Detailed Technical Analysis**: Technical breakdown, interfaces, data models, or logic flow.
     - **Mermaid Diagrams**: Visual architecture, sequence, or ER diagrams.
     - **Backlinks & References**: Obsidian wikilinks `[[...]]` connecting to relevant concept notes and entities.
     - **External Sources (required if any web/external info was used)**: a dedicated section listing each external source: URL/site, search query used, access date, and which report claims depend on it. Mark them unverified (not in `docs/raw/`). Omit the section only if no external info was used.

4. **Step 3 — Compounding Loop (File Back to Wiki)**:
   - *Karpathy Principle*: Good answers should compound in the knowledge base, not stay trapped in reports.
   - If the investigation uncovered a reusable architectural concept, core domain rule, or comparative matrix:
     - Extract an atomic note into `docs/wiki/concepts/universal/<slug>.md` (if general pattern) or `docs/wiki/concepts/local/<slug>.md` (if project-specific), or `docs/wiki/entities/{universal,local}/<slug>.md`.
     - Link the report to this atomic note and vice-versa.

5. **Step 4 — Update Catalog & Log**:
   - Add the report link to `docs/index.md` under the Reports section.
   - Append to `docs/log.md`:
     ```markdown
     ## [YYYY-MM-DD] Report | <Report Title>
     - Question investigated: "<User Query>"
     - Report created: `docs/reports/YYYY-MM-DD-<topic_slug>.md`
     - Compounding concepts extracted: None (or list `[[ConceptSlug]]`)
     ```
