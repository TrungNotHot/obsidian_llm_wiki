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
   - Query across `docs/wiki/` (concepts, entities, and architecture): grep keywords/synonyms and `title:`/`tags:` in frontmatter, plus the folder `README.md` catalogs, to find seed notes.
   - **Traverse embedded references**: from each seed note follow outbound `[[wikilinks]]`, choosing depth by question type: **1 hop** for a fact lookup, **2 hops** for relationships or summaries, **3 hops** for multi-hop reasoning, find backlinks via Grep `\[\[<note-name>` across `docs/wiki/` and `docs/reports/` (prior reports on the topic), read `contradictions:` partners, and open `sources:` files in `docs/raw/` when primary-source detail is needed. Rank candidates in two tiers: **Tier 1 (script)**: run `python3 .agents/scripts/rerank.py docs --query "<question keywords>" --seeds <seed-notes> --hops <1|2|3> --top <2 x budget>` (it prints `candidates: N` and scores notes on query terms in title, tags, filename and ALL headings, plus link-reach and confidence); **Tier 2 (LLM, only if N is above the budget)**: skim the headings of the shortlist and choose which to read in full. If the script fails, fall back to grep + your own judgement. Read in full at most **6 notes for 1 hop, 12 for 2 hops, 18 for 3 hops**, picking the most relevant to the question; if coverage is still thin, start a new traversal from a newly found seed instead of going deeper. Keep a list of visited notes to cite in the report.
   - Cross-check with source code in primary codebase directories (e.g. `src/`, `app/`, `lib/`) when code-level verification is needed.
   - **Web search (when wiki lacks enough info)**: ASK the user for permission first, stating what is missing. Never search silently. If approved, cite every web-sourced claim with its URL in the report and label it as unverified (not yet in `docs/raw/`); set `confidence: medium` or lower.

3. **Step 2 — Synthesize & Author Report**:
   - Create a new report file: `docs/reports/YYYY-MM-DD-<topic_slug>.md`.
   - Use standard frontmatter conforming to `docs/SCHEMA.md`:
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
     - **External Sources (required if any web/external info was used)**: a dedicated section listing each external source: URL/site, search query used, access date, and which report claims depend on it. Mark them unverified (not in `raw/`). Omit the section only if no external info was used.

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
