# Constitutional Schema: Technical Knowledge Base

This document defines the governance rules, conventions, quality gates, and taxonomy for the repository knowledge vault.

It is structured into two parts:
1. **Constitutional Framework**: Universal, project-agnostic engineering standards reusable across any technical repository.
2. **Project Domain Configuration**: Project-specific scope, taxonomy overrides, and system definitions.

---

# Part 1: Constitutional Framework (Universal)

## 1. Directory Layout & Conventions

- **Directory Conventions**:
  - `docs/raw/`: Immutable reference sources, clipped articles, specs, and execution plans (read-only).
  - `docs/wiki/concepts/`: Atomic architectural patterns & mechanisms:
    - `universal/`: Cross-project architecture patterns and algorithms (portable to a central General Knowledge Base).
    - `local/`: Project-specific mechanism implementations and domain transformations.
  - `docs/wiki/entities/`: Platform and external system registries:
    - `universal/`: Core compute engines, container platforms, and orchestration engines.
    - `local/`: Specific external data sources, enterprise systems, and integration endpoints.
  - `docs/wiki/easy_read/`: Developer and stakeholder guides organized by architectural layer.
  - `docs/reports/`: Permanent analytical investigation reports ("Never Answer in Chat, Always Answer in Files" for deep analysis; quick lookups via `/kb-ask` are answered in chat, read-only).
  - `docs/wiki/_archive/`: Superseded, deprecated, or decommissioned documentation.
- **File Names**: Lowercase, hyphen- or underscore-separated, no spaces (e.g. `append_on_change_xxhash64.md`, `fact-absence.md`).
- **Frontmatter**: Every wiki page must begin with YAML frontmatter conforming to the schema below.
- **Wikilinks**: Use `[[NoteName]]` or `[[Folder/NoteName|Display Name]]` for all cross-references.
  - Minimum 2 outbound links per concept or entity page.
- **Timestamping**: When modifying an existing page, always update the `updated: YYYY-MM-DD` field in frontmatter.
- **Master Catalog**: Every created or archived page must be reflected in `docs/index.md`.
- **Operations Log**: Every operation (compile, index, health, report, archive) must append an entry to `docs/log.md`.
- **Provenance Markers**: When synthesizing $\ge 3$ sources on a single page, append `^[docs/raw/source-file.md]` to key paragraphs to maintain auditability.

---

## 2. Frontmatter Schema

```yaml
---
title: "Descriptive Page Title"
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: concept | entity | comparison | query | report | architecture
tags:
  - architecture
  - pipeline
sources:
  - docs/raw/articles/source-name.md # optional for purely conceptual/synthesis notes
confidence: high # high | medium | low (degree of certainty/corroboration); do not use high without support from 2+ sources
contested: false # set true if unresolved contradictions exist
contradictions: [] # list of conflicting note slugs, e.g. [legacy-alps-mapping]
status: published
---
```

### Raw Layer Frontmatter (`docs/raw/`)
Raw sources captured from external articles, web clips, or converted from binary documents (`docs/raw/binary/`) must include a frontmatter block with a SHA-256 hash to detect silent source drift on re-ingestion:

```yaml
---
source_url: https://example.com/source # for web clips
source_file: docs/raw/binary/document.pdf # for binary conversions
original_type: pdf | docx | pptx | xlsx # source format
ingested: YYYY-MM-DD
sha256: <hex-digest-of-source-file-or-content>
---
```

---

## 3. Page Thresholds & Safety Gates

- **Create Page**: When an entity, pipeline component, or architectural concept appears in $\ge 2$ sources OR is the primary focus of an approved design spec/source document.
- **Do Not Create**: Passing mentions, transient error logs, or minor internal code helper functions.
- **Split Page**: When any page exceeds **300 lines**, decompose it into focused sub-topic pages and link them back to a parent overview.
- **Mass-Update Guardrail**: If an ingest or refactor would modify **10 or more** existing wiki pages, the agent must summarize the planned modifications and request user confirmation before proceeding.
- **Archive Page**: When an architecture, DAG, or table model is decommissioned or replaced, move it to `docs/wiki/_archive/`.

---

## 4. Index Scaling & Log Rotation

- **Index Section Splitting**: When any section in `docs/index.md` exceeds **50 entries**, subdivide it into subsections alphabetically or by sub-domain.
- **Topic Map Navigation**: When total cataloged pages exceed **200 entries**, create `docs/wiki/topic-map.md` grouping notes into overarching architectural themes.
- **Log Rotation**: When `docs/log.md` exceeds **500 entries**, rotate it: rename to `docs/log-YYYY.md` (e.g. `log-2026.md`) and initialize a fresh append-only `docs/log.md`.

---

## 5. Update & Contradiction Policy

When incoming information or codebase changes conflict with an existing wiki page:
1. **Check Timestamps**: Newer source documents or current codebase implementations supersede older specifications.
2. **Document Both Perspectives**: If there is an unresolved discrepancy or dual-state migration, explicitly state both positions with dates and source references.
3. **Set Quality Flags**:
   - Set `contested: true` in frontmatter.
   - List conflicting pages in `contradictions: [other-slug]`.
   - Set `confidence: medium` or `low` until reconciled.
4. **Log the Conflict**: Note the contradiction in `docs/log.md` and flag it for review in `docs/wiki/TODO.md`.

---

## 6. Archiving Workflow (`_archive/`)

When a component, pipeline, or contract is deprecated:
1. Create `docs/wiki/_archive/` if it does not already exist.
2. Move the file into `docs/wiki/_archive/<original-subfolder>/<note-slug>.md`.
3. Remove its entry from `docs/index.md`.
4. Update any existing incoming wikilinks to format: `[[slug]] (archived)`.
5. Append an entry to `docs/log.md`:
   ```markdown
   ## [YYYY-MM-DD] Archive | <Note Title>
   - Moved: `docs/wiki/...` -> `docs/wiki/_archive/...`
   - Superseded by: `[[NewNote]]`
   ```

---

# Part 2: Project Domain Configuration (<Your Project Name>)

> Configure this section when scaffolding into a new repository.

## 1. Domain Scope
<Describe your project purpose, architecture, and functional boundaries here.>
Example: "Backend API and Microservices for E-Commerce Checkout and Payment Processing."

---

## 2. Tag Taxonomy
All tags must be selected from the following controlled taxonomy. To add a new tag, update this schema first.

### Universal Technical Tags (Standard across all projects)
- **Architecture & Ops**: `architecture`, `logging`, `orchestration`, `security`, `devops`, `operations`, `diagnostics`, `connectivity`, `reliability`, `retry`, `monitoring`, `audit`, `assets`, `event-driven`, `configuration`
- **Data Engineering & Backend**: `dimension`, `dimensions`, `fact`, `facts`, `kimball`, `data-contract`, `schema`, `deduplication`, `watermark`, `cdc`, `etl`, `utilities`, `star-schema`, `dimensional-modeling`, `data-governance`, `data-dictionary`, `entity-resolution`, `surrogate-keys`, `data-engineering`, `mapping`, `quick-reference`, `api`, `service`, `database`
- **Document & Presentation Types**: `concept`, `entity`, `comparison`, `query`, `report`, `easy-read`, `bi-guide`, `documentation`

### Project-Specific Domain Tags (Customize for your repository)
- **Layers & Modules**: `staging`, `intermediate`, `dwh`, `presentation`, `pipeline`, `api`, `worker`
- **Platforms, Sources & Tech**: `airflow`, `mssql`, `postgres`, `redis`, `docker`, `kubernetes`, `external-api`
- **Domain & Business**: `core-domain`, `master-data`, `billing`, `customer`, `transaction`
