# Knowledge Base Archive (`_archive/`)

This directory holds deprecated, superseded, or decommissioned documentation, schemas, and architecture notes.

---

## 🏛️ Archiving Policy (per [[SCHEMA]])

1. **Superseded Content**: When a specification, model, or architectural concept is replaced or retired, move the corresponding markdown file here, preserving its subpath.
2. **Catalog Removal**: Archived files are removed from the active sections of [[index]].
3. **Wikilink Updating**: Active notes referencing an archived page should update their link to `[[NoteSlug]] (archived)`.
4. **Audit Trail**: Every archive action is recorded in [[log]].
5. **Read-Only**: Files in `_archive/` are kept for historical context and are excluded from active health checks (broken link & orphan calculations).
