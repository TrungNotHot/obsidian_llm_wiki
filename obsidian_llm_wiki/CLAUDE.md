# AI Agent Instructions & Workspace Guidelines

## 🏛️ Vault Summary & Architecture
- **Vault Purpose**: General-Purpose Technical Knowledge Base & Living AI Wiki, navigated via Obsidian and maintained by AI agents (based on Andrej Karpathy's LLM Wiki & Hermes Agent principles).
- **Domain Scope**: General knowledge across technology, systems architecture, cloud computing, DevOps, AI/ML, data engineering, software design, study guides, and multi-source analytical syntheses. Not specialized to any single project or codebase.
- **3-Layer Knowledge Architecture**:
  - `raw/`: Layer 1 — Immutable Sources (read-only web clips, articles, specs, blueprints, assets).
  - `wiki/`: Layer 2 — Living Knowledge Base (`concepts/`, `entities/`, `easy_read/`, `_archive/`).
  - `reports/`: Layer 3 — Permanent Deep Syntheses & analytical query reports ("Never Answer in Chat, Always Answer in Files").
- **Master Navigation & Governance**:
  - `SCHEMA.md`: Constitutional schema, tag taxonomy, note thresholds, and contradiction rules.
  - `index.md`: Master content catalog, navigation map, and technical glossary.
  - `log.md`: Append-only chronological operations log.
  - `wiki/TODO.md`: Integrity backlog for broken links, missing metadata, and content drift.

---

## ⚡ Core Rules & Behavioral Constraints

### 1. Git Commit Rules

#### Constraints
- **NO Automatic Git Commits**: Do NOT run `git commit` or automatically commit changes unless the user explicitly instructs you to commit.
- Always leave modified files staged/unstaged for the user to review and commit manually.
- **Vault Privacy Awareness**: Note `.gitignore` boundaries — note contents in `raw/articles/*`, `wiki/*/*`, `reports/*`, as well as `index.md`, `log.md`, and `wiki/TODO.md` are local-only / gitignored by default. Only constitutional, design, and agent configuration files are tracked in git. On the `private/*` branch these files are tracked for history; that branch must never be pushed to a remote.

---

### 2. Sensitive File Access Rules

#### Constraints
- Sensitive configuration and credential paths (secrets, API keys, tokens) are listed in `.agentignore`. Read `.agentignore` to know which paths are off-limits and respect them.
- Before reading, inspecting, parsing, or accessing any file or directory containing secrets, ask the user for explicit permission.
- Do not inspect, print, parse, or output secret credentials in context or responses.

---

### 3. Respect `.agentignore`

#### Constraints
- `.agentignore` (gitignore syntax) lists files and directories agents must not access.
- Do NOT read, search, inspect, parse, print, or edit any path matching `.agentignore`, unless the user gives explicit permission for that specific path.
- Skip matching paths in globs, greps, and directory scans.

---

### 4. Knowledge Base Operations & Schema Governance

Every agent action that reads, writes, or restructures vault content must strictly adhere to `SCHEMA.md`:

1. **Frontmatter Schema**: Every wiki page in `wiki/` must have valid YAML frontmatter conforming to `SCHEMA.md` (`title`, `created`, `updated`, `type`, `tags` from the controlled taxonomy, `sources`, `confidence`, `contested`, `contradictions`, `status`).
2. **Wikilinks**: Use `[[NoteName]]` or `[[Folder/NoteName|Display Name]]`. Ensure a minimum of 2 outbound links per concept or entity note.
3. **Immutable Raw Layer (`raw/`)**: Never modify raw sources after creation. Raw clips must include `source_url`, `ingested`, and `sha256` hash. Author links in raw clips are normalized to plain text to avoid orphan stub creation.
4. **Page Thresholds & Decompositions**:
   - Create a page only when a concept/entity appears in $\ge 2$ sources or is the central topic of an approved spec.
   - When a note exceeds the split threshold in `SCHEMA.md`, decompose into focused sub-topic notes linked back to a parent overview.
   - **Mass-Update Guardrail**: If an operation modifies **10 or more** wiki pages, summarize the planned changes and ask for user confirmation before editing.
5. **Contradiction Policy**: When incoming information conflicts with existing knowledge, document both sides with source citations, set `contested: true`, list contradictions, and log in `log.md` and `wiki/TODO.md`.
6. **Logging & Catalog Integrity**: Every compilation (`/kb-compile`), indexing (`/kb-index`), health audit (`/kb-health`), report (`/kb-report`), or archiving action MUST append to `log.md` and update `index.md`.

---

### 5. Skills & Working Style

- **Vault operations** use the `/kb-*` skills: `/kb-compile` (ingest `raw/` into `wiki/`), `/kb-colluni` (harvest universal notes from a project repo into `raw/articles/`), `/kb-index`, `/kb-health`, `/kb-ask` (quick read-only lookup answered in chat) and `/kb-report` (deep analysis written to `reports/`: "Never Answer in Chat, Always Answer in Files").
- **Web search**: `/kb-ask` and `/kb-report` may search the web only when the wiki lacks the answer, MUST ask the user first, and label web-sourced content unverified.
- **Lightest sufficient ceremony**: simple lookups and single-note edits need no planning; for a large reorganization or a multi-part report, plan in phases and run a health check at the end.
- **Surgical and verified**: touch only the notes the task needs, keep notes atomic and dense, and verify integrity (`check_health.py`, link validity) before declaring completion.
- **Architectural forks** (split vs keep a note, new entity vs merge, revise vs archive): state the dilemma, recommend one option with a one-sentence rationale based on `SCHEMA.md`, and ask the user before proceeding.
