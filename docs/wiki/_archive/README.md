# Archive Layer (`wiki/_archive/`)

This directory preserves decommissioned, deprecated, or superseded documentation, architecture specs, and component guides.

---

## 🏛️ Archiving Rules (per `docs/SCHEMA.md`)

When a component, pipeline, or architecture is decommissioned:
1. Move the corresponding note to `docs/wiki/_archive/<subfolder>/<note-slug>.md`.
2. Remove its entry from `docs/index.md`.
3. Update any active incoming wikilinks to format: `[[slug]] (archived)`.
4. Append an entry to `docs/log.md`:
   ```markdown
   ## [YYYY-MM-DD] Archive | <Note Title>
   - Moved: `docs/wiki/...` -> `docs/wiki/_archive/...`
   - Superseded by: `[[NewNote]]`
   ```
