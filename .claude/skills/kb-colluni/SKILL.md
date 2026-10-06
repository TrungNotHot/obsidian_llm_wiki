---
name: kb-colluni
description: Extracts and collects universal concepts & entities from a project vault into the general vault's raw/articles, using LLM semantic reasoning to filter and rewrite references.
---

# /kb-colluni Skill

Extracts architectural patterns, algorithms, and technology entities from a project-specific repository or vault into the Central Knowledge Base (`dest_vault/raw/articles/`).

Rather than performing a mechanical file copy, the AI agent uses **semantic reasoning** to separate timeless principles from project-specific implementation details, rewriting references so the extracted notes become self-contained, clean, and immediately ready for knowledge synthesis.

> [!IMPORTANT]
> **Strict Scope Boundary (Raw Ingestion Only)**:
> This skill focuses **exclusively on harvesting and saving sanitized source articles into `dest_vault/raw/articles/`**. It NEVER touches `wiki/` (concepts, entities) and NEVER modifies `index.md`. The synthesis and cross-linking of these raw articles into the living wiki is strictly delegated to `/kb-compile`.

---

## 1. Input Parameters & Interaction Rule

- **`src_vault` (REQUIRED — Must Prompt User if Missing)**:
  - Absolute or relative path to the source project repository or vault root (e.g. `/home/tdtr/workspace/code/hr-scorecard` or `./docs`).
  - **MANDATORY**: If the user invokes `/kb-colluni` without explicitly providing `src_vault`, the agent **MUST STOP and ASK THE USER** for the source vault path before proceeding. Do NOT assume or guess the source vault path.
- **`dest_vault` (AUTOMATIC DEFAULT)**:
  - Path to the destination General Knowledge Vault.
  - **DEFAULT**: Automatically defaults to the current active vault directory (the root of `obsidian_llm_wiki`). The user does NOT need to provide this unless explicitly overriding it.

---

## 2. Source Discovery & Target Layout

To locate universal notes reliably without brute-force filesystem scans, the agent follows a **Catalog-First Discovery Hierarchy**:

### A. Primary Method: Master Catalog & Directory Index (`index.md` & `README.md`)
1. **Master Catalog Inspection**:
   - Read `<src_vault>/docs/index.md` (or `<src_vault>/index.md`).
   - Locate the constitutional universal sections:
     - `#### 🌐 Universal Architecture Patterns` (under `wiki/concepts/universal/`)
     - `#### 🌐 Universal Platforms & Infrastructure` (under `wiki/entities/universal/`)
   - Extract the curated list of note wikilinks (`[[...]]`) and summaries.
2. **Directory Catalog Inspection**:
   - Read `<src_vault>/docs/wiki/concepts/README.md` and `<src_vault>/docs/wiki/entities/README.md` (or `<src_vault>/wiki/*/README.md`).
   - Confirm the boundary separating `universal/` (cross-project patterns) from `local/` (project-specific implementations).

### B. Fallback Method: Convention Directories & Search
If `index.md` is absent or does not explicitly categorize universal sections:
- Inspect standard convention directories directly:
  - `<src_vault>/docs/wiki/concepts/universal/*.md`
  - `<src_vault>/docs/wiki/entities/universal/*.md`
  (or `<src_vault>/wiki/...` without `docs/`).
- If needed, run a bounded discovery command:
  ```bash
  rtk find "<src_vault>" -maxdepth 5 -type d -path "*/universal"
  ```

All extracted and sanitized documents are saved to:
- `dest_vault/raw/articles/<kebab-case-slug>.md`

---

## 3. Raw Layer Isolation Protocol (Zero Wikilinks in raw/)

Per the constitutional Karpathy & Hermes Agent LLM Wiki design, **`raw/` is Layer 1 (Immutable Source Evidence)**.
- **Strict Invariant**: Files inside `raw/articles/` must **NEVER contain Obsidian wikilinks (`[[...]]`)**. Wikilinks exist exclusively in Layer 2 (`wiki/`).
- If wikilinks were kept in `raw/`, they would cause **Graph Pollution** and create **ghost/unresolved backlinks** across the vault.

### Semantic Link Sanitization Rules:
1. **Universal Pattern Mentions $\rightarrow$ Plain Text / Bold Terms**:
   - Strip the `[[...]]` brackets and convert to canonical architectural names:
     - `[[watermark_incremental_sync|Watermark Incremental Sync]]` $\rightarrow$ **Watermark Incremental Synchronization**
     - `[[append_on_change_xxhash64]]` $\rightarrow$ **Append-on-Change CDC (xxHash64)**
     - `[[kimball_dimensional_modeling]]` $\rightarrow$ **Ralph Kimball Dimensional Modeling (Star Schema)**
     - `[[apache_airflow]]` $\rightarrow$ **Apache Airflow**
     - `[[microsoft_sql_server]]` $\rightarrow$ **Microsoft SQL Server**
2. **Project-Specific Mentions $\rightarrow$ Generic Case Studies**:
   - Strip project wikilinks and convert to generic implementation descriptions:
     - `[[dag_crawl_employee]]` $\rightarrow$ `Employee Ingestion Pipeline` (or inline code `` `dag_crawl_employee` ``)
     - `[[traffic_cop_logging]]` $\rightarrow$ `centralized database execution logging`
     - Strip internal file paths (`docs/raw/superpowers/specs/...` or `include/utils/...`) and replace with descriptive citations: *(derived from production ETL design specs)*.
3. **Preserve Complete Substance**:
   - Retain 100% of mathematical equations, ASCII/Mermaid diagrams, decision tables, schema definitions, and algorithm pseudo-code.
   - The output must be an authoritative, self-contained reference article ready for knowledge compilation.

---

## 4. Frontmatter Standardization for `raw/articles/`

Every extracted file placed in `dest_vault/raw/articles/` conforms to the `SCHEMA.md` specification for raw sources:

```yaml
---
title: "<Clean Page Title>"
source_vault: "<Source Project Name>"
source_file: "<Relative path in source repo>"
source_type: "universal_concept" | "universal_entity"
ingested: YYYY-MM-DD
sha256: <hex-digest-of-body-content>
tags:
  - "clippings"
  - "imported-source"
  - "universal-<concept|entity>"
  - "<domain-tag-from-SCHEMA.md>"
---
```

---

## 5. Step-by-Step Agent Execution Workflow

When `/kb-colluni` is triggered:

1. **Step 0 — Parameter Validation & User Prompt (MANDATORY)**:
   - Check if the user specified the `src_vault` path in their request.
   - **If `src_vault` is NOT provided**: The agent MUST immediately pause and ask the user:
     > *"Please provide the path to the source project repository or vault (`src_vault`) to extract universal concepts and entities from."*
     Do not proceed with discovery until the user supplies this path.
   - **Set `dest_vault`**: Automatically default to the current active General Knowledge Vault (`obsidian_llm_wiki`). Do NOT ask the user for `dest_vault` unless they explicitly request an override.

2. **Step 1 — Discovery & Inventory (Catalog-First)**:
   - **Inspect Master Catalog**: Read `<src_vault>/docs/index.md` (or `<src_vault>/index.md`) to extract the list of Universal Concepts and Universal Entities directly from the master index.
   - **Cross-check Directory Catalogs**: Read `<src_vault>/docs/wiki/concepts/README.md` and `<src_vault>/docs/wiki/entities/README.md` to confirm the scope and summary of each item.
   - **Fallback**: If `index.md` is absent, scan convention folders (`wiki/concepts/universal/`, `wiki/entities/universal/`) directly.
   - Present the identified universal candidate list to the user (file names, inferred topics, source locations).

3. **Step 2 — Semantic Read & Reference Sanitization**:
   - For each file, read the full content.
   - Strip ALL `[[...]]` wikilinks, converting universal concepts to standard architectural terminology and local items to generic case studies.
   - Replace project-internal relative paths with descriptive citations.
   - Ensure ZERO `[[wikilinks]]` remain in the article body.

4. **Step 3 — Distillation & File Generation**:
   - Compute `sha256` hash of the sanitized body.
   - Construct standard frontmatter (`source_vault`, `source_file`, `ingested`, `sha256`, `tags`).
   - Write the resulting markdown file to `dest_vault/raw/articles/<kebab-case-slug>.md`.

5. **Step 4 — Audit & Verification**:
   - Verify that no `[[` or `]]` exist anywhere in the written `raw/articles/*.md` files.
   - Verify valid YAML frontmatter with `sha256` and `source_vault`.

6. **Step 5 — Log & Next Steps**:
   - Append an entry to `dest_vault/log.md`:
     ```markdown
     ## [YYYY-MM-DD] Ingest | Harvester: kb-colluni (<Source Vault Name>)
     - Source: `<src_vault>`
     - Harvested to raw/articles/: `<list of kebab-slugs>`
     - Verification: Zero wikilinks in raw layer (pure Layer 1 isolation)
     ```
   - Inform the user of the completed extraction and recommend running `/kb-compile` to compile the new raw articles into permanent `wiki/` pages and establish living `[[wikilinks]]`.
