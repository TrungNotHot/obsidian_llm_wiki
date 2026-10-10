---
name: kb-ask
description: Quick Q&A over the wiki (chat answer, read-only); asks permission before any web search.
---

# /kb-ask Skill

Fast lookup: answers a question in chat from the wiki. Does NOT write files, `docs/log.md` or `docs/index.md`.

## Workflow
1. **Locate seeds**: read `docs/index.md` (catalog, glossary) and the folder `README.md` catalogs (`docs/wiki/concepts/`, `docs/wiki/entities/`, `docs/wiki/easy_read/`). Analyze the question yourself: identify the concepts it involves (including implied, broader or related ones; the wiki is in English, so translate first if needed) and pick the catalog entries that best cover them by judgement. Use grep on `title:`/`tags:` (taxonomy in `docs/SCHEMA.md`) only to confirm or fill gaps, not as the primary selector. Read those notes.
2. **Follow the links (graph traversal)**: notes are cross-referenced, so use the embedded references instead of keyword search alone:
   - *Outbound*: read `[[wikilinks]]` inside seed notes and open the relevant ones. Pick the depth by question type: **1 hop** for a fact lookup, **2 hops** for relationships or summaries (stop as soon as the answer is covered). Multi-hop reasoning questions (chains across 3+ notes) are better served by `/kb-report`.
   - *Backlinks*: Grep `\[\[<note-name>` across `docs/wiki/` to find notes that cite the seed.
   - *Frontmatter links*: check `contradictions:` (read the conflicting note too) and `sources:` (open the `docs/raw/` file only if wiki detail is insufficient).
   - *Rank in two levels*: **Level 1 (outline)**: run `python3 .claude/scripts/outline.py docs --seeds <seed-notes> --hops <1|2> [--limit 40]`. It lists every note reachable by links/backlinks within the hop limit with its title, tags, confidence and ALL headings (no scoring). Read those outlines and **rerank them yourself** by relevance to the question, keeping the best up to the budget below. **Level 2 (full read)**: read the selected notes in full. If `candidates` is within the budget, skip the ranking and read them all; if the list is truncated, narrow the seeds or hops. If the script fails, fall back to grep + your own judgement.
   - *Budget*: read in full at most **6 notes for a 1-hop lookup, 12 for 2 hops**; pick the most relevant. Read independent notes in parallel. No dependency on Obsidian being open.
3. Answer concisely, citing notes as `[[NoteName]]`. Flag `contested: true` notes and low-`confidence` sources.
4. **Wiki gap → web search is allowed, but ASK FIRST**: state what is missing, then ask the user for permission to search the web. Never search silently.
5. If approved: answer with web results clearly labeled **"Web sources (unverified, not in wiki)"** with URLs, kept separate from wiki-sourced facts. Suggest clipping valuable pages into `docs/raw/articles/` then `/kb-compile`.
6. If the question needs multi-source synthesis, suggest `/kb-report` instead.
