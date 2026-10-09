# Knowledge Base Health TODOs
Last checked: Not yet audited

> Copy this file to `wiki/TODO.md` and update it after each health audit.

## 🔴 High Severity: Broken Links & Critical Code Drift
- [ ] Check broken wikilinks and restore missing targets.
- [ ] Reconcile documentation with active code, if applicable.
- [ ] Compile pending raw sources into the wiki.

## 🟡 Medium Severity: Contested Pages, Stale Notes & Semantic Drift
- [ ] Review contested claims and low-confidence pages.
- [ ] Review notes not updated in more than 90 days.
- [ ] Check raw source metadata (`source_url`, `ingested`, `sha256`) and hash drift; preserve immutable sources.

## 🟢 Low Severity: Orphans, Size & Taxonomy Cleanup
- [ ] Link orphan pages and sync the catalog in `index.md`.
- [ ] Check frontmatter, controlled tags, and outbound links against `SCHEMA.md`.
- [ ] Split oversized wiki notes according to `SCHEMA.md`.
