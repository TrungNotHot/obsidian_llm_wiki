---
name: kb-ask
description: Quick Q&A over the wiki (chat answer, read-only); asks permission before any web search.
---

# /kb-ask Skill

Fast lookup: answers a question in chat from the wiki. Does NOT write files, `log.md` or `index.md`.

## Workflow
1. **Locate seeds**: read `index.md` (catalog, glossary) and the folder `README.md` catalogs (`wiki/concepts/`, `wiki/entities/`, `wiki/easy_read/`). Grep `wiki/` for keywords/synonyms, matching `title:` and `tags:` in frontmatter (tags from `SCHEMA.md` taxonomy). Read the best 1-3 notes.
2. **Follow the links (graph traversal)**: notes are cross-referenced, so use the embedded references instead of keyword search alone:
   - *Outbound*: read `[[wikilinks]]` inside seed notes and open the relevant ones. Pick the depth by question type: **1 hop** for a fact lookup, **2 hops** for relationships or summaries (stop as soon as the answer is covered). Multi-hop reasoning questions (chains across 3+ notes) are better served by `/kb-report`.
   - *Backlinks*: Grep `\[\[<note-name>` across `wiki/` to find notes that cite the seed.
   - *Frontmatter links*: check `contradictions:` (read the conflicting note too) and `sources:` (open the `raw/` file only if wiki detail is insufficient).
   - *Rank in two tiers*: **Tier 1 (script)**: run `python3 .agents/scripts/rerank.py . --query "<question keywords>" --seeds <seed-notes> --hops <1|2> --top <2 x budget>`. It reaches notes by links/backlinks within the hop limit and scores each on query terms found in title, tags, filename and ALL headings (plus link-reach and confidence), then prints `candidates: N`. **Tier 2 (LLM, only if N is above the budget)**: skim the headings of the shortlist and choose which notes to read in full; if N is within the budget, skip tier 2. If the script fails (e.g. no python), fall back to grep + your own judgement.
   - *Budget*: read in full at most **6 notes for a 1-hop lookup, 12 for 2 hops**; pick the most relevant. Read independent notes in parallel. No dependency on Obsidian being open.
3. Answer concisely, citing notes as `[[NoteName]]`. Flag `contested: true` notes and low-`confidence` sources.
4. **Wiki gap → web search is allowed, but ASK FIRST**: state what is missing, then ask the user for permission to search the web. Never search silently.
5. If approved: answer with web results clearly labeled **"Web sources (unverified, not in wiki)"** with URLs, kept separate from wiki-sourced facts. Suggest clipping valuable pages into `raw/articles/` then `/kb-compile`.
6. If the question needs multi-source synthesis, suggest `/kb-report` instead.
