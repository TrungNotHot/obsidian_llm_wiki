---
name: kb-ask
description: Quick Q&A over the wiki (chat answer, read-only); asks permission before any web search.
---

# /kb-ask Skill

Fast lookup: answers a question in chat from the wiki. Does NOT write files, `docs/log.md` or `docs/index.md`.

## Workflow
1. **Find relevant notes**: read `docs/index.md` (catalog, glossary; if it is large, read the relevant sections or grep it). Analyze the question: identify the concepts it involves (including implied or related ones; the wiki is in English, so translate first if needed) and pick the best-matching entries by judgement. If no catalog entry matches, or before concluding the wiki lacks something, grep keywords (with synonyms) across `docs/wiki/` and `docs/reports/`.
2. **Read**: read the relevant notes in full (in parallel), most relevant first, and stop as soon as the answer is covered (usually 3-8 notes; if it needs more than ~12, suggest `/kb-report`). Follow a note's `[[wikilinks]]` only when they point to something the answer needs. Check `contradictions:` partners, and open `sources:` files in `docs/raw/` only if wiki detail is insufficient. No dependency on Obsidian being open.
3. **Optional, expand with links**: when the question is about relationships and the notes you read link to notes you have not seen, or the catalog did not cover the topic, run `python3 .agents/scripts/outline.py docs --seeds a,b --hops 1` (`--seeds` = note file names without `.md`, **comma-separated, no spaces**). It lists neighbours (links and backlinks) with title, tags, confidence and all headings; choose the relevant ones yourself. Default **1 hop**, **2** only if needed. If it reports truncation, narrow `--seeds` or raise `--limit N` (max 100). If it fails, fall back to grep.
4. Answer concisely, citing notes as `[[NoteName]]`. Flag `contested: true` notes and low-`confidence` sources.
5. **Wiki gap → web search is allowed, but ASK FIRST**: state what is missing, then ask the user for permission to search the web. Never search silently.
6. If approved: answer with web results clearly labeled **"Web sources (unverified, not in wiki)"** with URLs, kept separate from wiki-sourced facts. Suggest clipping valuable pages into `docs/raw/articles/` then `/kb-compile`.
7. If the question needs multi-source synthesis, suggest `/kb-report` instead.
