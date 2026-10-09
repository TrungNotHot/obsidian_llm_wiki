---
name: kb-ask
description: Quick Q&A over the wiki (chat answer, read-only); asks permission before any web search.
---

# /kb-ask Skill

Fast lookup: answers a question in chat from the wiki. Does NOT write files, `docs/log.md` or `docs/index.md`.

## Workflow
1. **Locate seeds**: read `docs/index.md` (catalog, glossary) and the folder `README.md` catalogs (`docs/wiki/concepts/`, `docs/wiki/entities/`, `docs/wiki/easy_read/`). Grep `docs/wiki/` for keywords/synonyms, matching `title:` and `tags:` in frontmatter (tags from `docs/SCHEMA.md` taxonomy). Read the best 1-3 notes.
2. **Follow the links (graph traversal)**: notes are cross-referenced, so use the embedded references instead of keyword search alone:
   - *Outbound*: read `[[wikilinks]]` inside seed notes and open the relevant ones (max 2 hops, stop when the answer is covered).
   - *Backlinks*: Grep `\[\[<note-name>` across `docs/wiki/` to find notes that cite the seed.
   - *Frontmatter links*: check `contradictions:` (read the conflicting note too) and `sources:` (open the `docs/raw/` file only if wiki detail is insufficient).
   - *Budget*: read at most ~6 notes in full. Read independent notes in parallel. No dependency on Obsidian being open.
3. Answer concisely, citing notes as `[[NoteName]]`. Flag `contested: true` notes and low-`confidence` sources.
4. **Wiki gap → web search is allowed, but ASK FIRST**: state what is missing, then ask the user for permission to search the web. Never search silently.
5. If approved: answer with web results clearly labeled **"Web sources (unverified, not in wiki)"** with URLs, kept separate from wiki-sourced facts. Suggest clipping valuable pages into `docs/raw/articles/` then `/kb-compile`.
6. If the question needs multi-source synthesis, suggest `/kb-report` instead.
