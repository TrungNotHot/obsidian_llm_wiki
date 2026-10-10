---
name: kb-ask
description: Quick Q&A over the wiki (chat answer, read-only); asks permission before any web search.
---

# /kb-ask Skill

Fast lookup: answers a question in chat from the wiki. Does NOT write files, `docs/log.md` or `docs/index.md`.

## Workflow
1. **Locate seeds**: read `docs/index.md` (catalog, glossary) and the folder `README.md` catalogs (`docs/wiki/concepts/`, `docs/wiki/entities/`, `docs/wiki/easy_read/`). Analyze the question yourself: identify the concepts it involves (including implied, broader or related ones) and pick the catalog entries that best cover them by judgement. Use grep on `title:`/`tags:` (taxonomy in `docs/SCHEMA.md`) only to confirm or fill gaps, not as the primary selector. **If the wiki has about 100+ notes, or the catalogs have no matching entry, keyword grep across all of `docs/wiki/` and `docs/reports/` is mandatory** (the index alone may miss relevant content). Read those notes.
2. **Follow the links in two levels**:
   - **Level 1 (outline)**: run `python3 .claude/scripts/outline.py docs --seeds <seed-notes> --hops <1|2>`. Pick the depth by question type: **1 hop** for a fact lookup, **2 hops** for relationships or summaries (stop as soon as the answer is covered; multi-hop reasoning chains across 3+ notes are better served by `/kb-report`). It lists every note reachable by links and backlinks within the hop limit with its title, tags, confidence and ALL headings (no scoring). Read those outlines and **rerank them yourself** by relevance to the question. The output is capped (20 / 40 / 60 notes for 1 / 2 / 3 hops). If it says the list was truncated, do NOT raise `--limit`; rerun with a narrower scope, adjusting in this order: **1) `--seeds`** (drop weakly related seeds, add missing good ones), **2) `--hops`** (only as far as the question type allows). If the script fails, fall back to grep + your own judgement.
   - **Level 2 (full read)**: read in full at most **6 notes for a 1-hop lookup, 12 for 2 hops** (the seed notes already read in step 1 are not counted), the most relevant first (if `candidates` is within the budget, skip ranking and read them all). Read independent notes in parallel. Also check the seeds' `contradictions:` (read the conflicting note too) and `sources:` (open the `docs/raw/` file only if wiki detail is insufficient). No dependency on Obsidian being open.
3. Answer concisely, citing notes as `[[NoteName]]`. Flag `contested: true` notes and low-`confidence` sources.
4. **Wiki gap → web search is allowed, but ASK FIRST**: state what is missing, then ask the user for permission to search the web. Never search silently.
5. If approved: answer with web results clearly labeled **"Web sources (unverified, not in wiki)"** with URLs, kept separate from wiki-sourced facts. Suggest clipping valuable pages into `docs/raw/articles/` then `/kb-compile`.
6. If the question needs multi-source synthesis, suggest `/kb-report` instead.
