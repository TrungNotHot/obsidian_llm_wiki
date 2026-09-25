# Wiki Schema: LLM Wiki Knowledge Base

## Domain
General-purpose technical knowledge base, architecture repository, and AI-assisted documentation vault.
Covers system designs, technical specifications, core concepts, entity registries, workflows, and analytical syntheses.

---

## Conventions
- **File Names**: Lowercase, hyphen-separated, no spaces (e.g., `system-architecture.md`, `rest-api-client.md`).
- **Frontmatter**: Every wiki page must begin with YAML frontmatter conforming to the schema below.
- **Wikilinks**: Use `[[NoteName]]` or `[[Folder/NoteName|Display Name]]` for all cross-references.
  - Minimum 2 outbound links per concept or entity page.
- **Timestamping**: When modifying an existing page, always update the `updated: YYYY-MM-DD` field in frontmatter.
- **Master Catalog**: Every created or archived page must be reflected in `index.md`.
- **Operations Log**: Every operation (compile, index, health, report, archive) must append an entry to `log.md`.
- **Provenance Markers**: When synthesizing $\ge 3$ sources on a single page, append `^[raw/source-file.md]` to key paragraphs to maintain auditability.

---

## Tag Taxonomy
All tags must be selected from the controlled taxonomy below. To add a new domain tag, update this schema first.

- **Architecture, Ops & Reliability**: `architecture`, `logging`, `orchestration`, `security`, `devops`, `operations`, `diagnostics`, `connectivity`, `reliability`, `monitoring`, `audit`, `configuration`
- **Data & Engineering**: `data-engineering`, `data-modeling`, `data-governance`, `schema`, `etl`, `pipeline`, `database`, `storage`, `api`, `utilities`
- **Systems, Infrastructure & Tools**: `infrastructure`, `container`, `cloud`, `service`, `external-service`, `filesystem`
- **Document & Presentation Types**: `concept`, `entity`, `comparison`, `query`, `report`, `guide`, `easy-read`, `documentation`

---

## Frontmatter Schema

```yaml
---
title: "Descriptive Page Title"
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: concept | entity | comparison | query | report | architecture | guide
tags:
  - architecture
  - concept
sources:
  - raw/articles/source-name.md # optional for purely conceptual/synthesis notes
confidence: high # high | medium | low (degree of certainty/corroboration)
contested: false # set true if unresolved contradictions exist
contradictions: [] # list of conflicting note slugs, e.g. [legacy-system-spec]
status: published # published | draft | deprecated
---
```

---

## Raw Layer Frontmatter (`raw/`)
Raw sources captured from external articles, API specs, or web clips must include a frontmatter block with a body hash to detect silent source drift on re-ingestion:

```yaml
---
source_url: https://example.com/source # if applicable
ingested: YYYY-MM-DD
sha256: <hex-digest-of-body-content-below-frontmatter>
---
```

---

## Page Thresholds & Safety Gates
- **Create Page**: When an entity, system component, or architectural concept appears in $\ge 2$ sources OR is the primary focus of an approved design spec/source document.
- **Do Not Create**: Passing mentions, transient error logs, or minor internal code helper functions.
- **Split Page**: When any page exceeds **200 lines**, decompose it into focused sub-topic pages and link them back to a parent overview.
- **Mass-Update Guardrail**: If an ingest or refactor would modify **10 or more** existing wiki pages, the agent must summarize the planned modifications and request user confirmation before proceeding.
- **Archive Page**: When an architecture, specification, or component is decommissioned or replaced, move it to `wiki/_archive/`.

---

## Index Scaling & Log Rotation
- **Index Section Splitting**: When any section in `index.md` exceeds **50 entries**, subdivide it into subsections alphabetically or by sub-domain.
- **Topic Map Navigation**: When total cataloged pages exceed **200 entries**, create `wiki/topic-map.md` grouping notes into overarching architectural themes.
- **Log Rotation**: When `log.md` exceeds **500 entries**, rotate it: rename to `log-YYYY.md` (e.g. `log-2026.md`) and initialize a fresh append-only `log.md`.

---

## Update & Contradiction Policy
When incoming information or codebase changes conflict with an existing wiki page:
1. **Check Timestamps**: Newer source documents or current codebase implementations supersede older specifications.
2. **Document Both Perspectives**: If there is an unresolved discrepancy or dual-state migration, explicitly state both positions with dates and source references.
3. **Set Quality Flags**:
   - Set `contested: true` in frontmatter.
   - List conflicting pages in `contradictions: [other-slug]`.
   - Set `confidence: medium` or `low` until reconciled.
4. **Log the Conflict**: Note the contradiction in `log.md` and flag it for review in `wiki/TODO.md`.

---

## Archiving Workflow (`_archive/`)
When a component, system, or contract is deprecated:
1. Ensure `wiki/_archive/` exists.
2. Move the file into `wiki/_archive/<original-subfolder>/<note-slug>.md`.
3. Remove its entry from `index.md`.
4. Update any existing incoming wikilinks to format: `[[slug]] (archived)`.
5. Append an entry to `log.md`:
   ```markdown
   ## [YYYY-MM-DD] Archive | <Note Title>
   - Moved: `wiki/...` -> `wiki/_archive/...`
   - Superseded by: `[[NewNote]]`
   ```
