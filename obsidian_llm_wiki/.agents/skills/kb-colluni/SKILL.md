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
- **Source `.agentignore`**: if `src_vault` (or its repo root) has a `.agentignore`, read it and NEVER read or extract any path it matches (secrets, credentials, env files), even if the catalog lists it.
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
  find "<src_vault>" -maxdepth 5 -type d -path "*/universal"
  ```

- If the source vault does not use the `universal/` and `local/` convention, pick candidates by judgement (timeless, reusable patterns and platforms) and let the user confirm them in Step 1 of the workflow.

All extracted and sanitized documents are saved to:
- `dest_vault/raw/articles/<kebab-case-slug>.md`

---

## 3. Raw Layer Isolation Protocol (Zero Wikilinks in raw/)

Per the constitutional Karpathy & Hermes Agent LLM Wiki design, **`raw/` is Layer 1 (Immutable Source Evidence)**.
- **Strict Invariant**: Files inside `raw/articles/` must **NEVER contain Obsidian wikilinks (`[[...]]`)**. Wikilinks exist exclusively in Layer 2 (`wiki/`).
- If wikilinks were kept in `raw/`, they would cause **Graph Pollution** and create **ghost/unresolved backlinks** across the vault.

### Sanitization Rules:
1. **Universal Pattern Mentions $\rightarrow$ Plain Text / Bold Terms**:
   - Strip the `[[...]]` brackets and convert to the canonical industry name:
     - `[[some-pattern|Some Pattern]]` $\rightarrow$ **Some Pattern**
     - `[[platform-note]]` $\rightarrow$ **Platform Name** (the well-known product name)
2. **Project-Specific Mentions $\rightarrow$ Generic Case Studies**:
   - Strip project wikilinks and convert to a generic description of what the thing does:
     - `[[project-specific-note]]` $\rightarrow$ `nightly ingestion pipeline` (or inline code with the bare name)
     - Strip internal file paths (e.g. `docs/specs/...`, `src/utils/...`) and replace with descriptive citations: *(derived from the project's design specs)*.
3. **Preserve Complete Substance**:
   - Retain 100% of mathematical equations, ASCII/Mermaid diagrams, decision tables, schema definitions, and algorithm pseudo-code.
   - The output must be an authoritative, self-contained reference article ready for knowledge compilation.
4. **Scrub Sensitive & Identifying Data**:
   - Replace host names, internal URLs, connection strings, credentials/tokens, IP addresses, personal names, employee identifiers and company-specific names with a generic description (e.g. `the ERP database server`, `an employee ID`). Keep the technical meaning, drop the identity.
   - If you are unsure whether something is sensitive, stop and ask the user before writing.

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
   - Apply Section 1: if `src_vault` was not provided, **STOP and ask the user** for it (*"Please provide the path to the source project repository or vault (`src_vault`) to extract universal concepts and entities from."*) and do not proceed with discovery until they answer. `dest_vault` defaults to the current vault; do not ask unless the user overrides it.

2. **Step 1 — Discovery & Inventory (Catalog-First)**:
   - Apply Section 2 (master catalog, directory catalogs, then the fallback if needed).
   - Present the identified universal candidate list to the user (file names, inferred topics, source locations) and **STOP until the user confirms** which items to harvest. If the confirmed set is **10 or more** files, restate the count and destination before writing.

3. **Step 2 — Semantic Read & Reference Sanitization**:
   - For each file, read the full content.
   - Strip ALL `[[...]]` wikilinks, converting universal concepts to standard architectural terminology and local items to generic case studies.
   - Replace project-internal relative paths with descriptive citations.
   - Apply the Section 3 scrub rule (sensitive and identifying data).
   - Ensure ZERO `[[wikilinks]]` remain in the article body.

4. **Step 3 — Distillation & File Generation**:
   - Compute the `sha256` of the sanitized body: the UTF-8 text after the frontmatter's closing `---`, with surrounding whitespace stripped (this is how `kb-health` recomputes it for drift checks).
   - **Check the destination first**: if `dest_vault/raw/articles/<kebab-case-slug>.md` already exists, compare its stored `sha256` with the new one. *Identical*: skip (already harvested). *Different*: do NOT overwrite (raw is immutable); report it as source drift and ask the user whether to save under a new dated slug.
   - Construct standard frontmatter (`source_vault`, `source_file`, `ingested`, `sha256`, `tags`).
   - Write the resulting markdown file to `dest_vault/raw/articles/<kebab-case-slug>.md`.

5. **Step 4 — Audit & Verification**:
   - Verify that no wikilink remains in the written `raw/articles/*.md` files. Ignore fenced and inline code (shell conditionals like `[[ -f x ]]` are not wikilinks); a wikilink is `[[Name]]` or `[[Name|Alias]]` in prose.
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
