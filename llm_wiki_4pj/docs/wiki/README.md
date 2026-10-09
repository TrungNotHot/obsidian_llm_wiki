# Living Knowledge Wiki (`wiki/`)

This directory houses the active, living technical knowledge base. Unlike static archives, documents here are continuously kept in sync with the codebase by AI agents.

---

## 📂 Subdirectories

- **`concepts/`**: Atomic architectural patterns, algorithms, and data modeling concepts:
  - `universal/`: General, cross-project patterns (e.g. Kimball dimensional modeling, Change Data Capture hashing, watermark windowing, retry mechanisms). Portable to a General Knowledge Base.
  - `local/`: Project-specific mechanisms and domain-tailored implementations.
- **`entities/`**: Systems, platforms, databases, and service registries:
  - `universal/`: Core orchestration engines, container platforms, and database compute engines.
  - `local/`: Specific upstream source systems, enterprise databases, and integration endpoints.
- **`easy_read/`**: Stakeholder- and developer-accessible architecture guides organized by pipeline layers or service domains:
  - `staging/`: Bronze raw extract pipelines and source-to-staging mappings.
  - `intermediate/`: Silver harmonization, watermark windowing, and entity discovery.
  - `dwh/`: Gold dimensional star schema, conformed dimensions, and fact tables.
  - `logging/`: Execution telemetry, control locks, and connection diagnostics.
- **`_archive/`**: Decommissioned, superseded, or obsolete documentation preserved for auditability.

---

## 📐 Governance & Rules

- Governed by `docs/SCHEMA.md`.
- All pages must include YAML frontmatter (`title`, `created`, `updated`, `type`, `tags`, `confidence`, `contested`, `status`).
- Maintain at least **2 outbound wikilinks** (`[[...]]`) per page to ensure high network connectivity in Obsidian's graph view.
