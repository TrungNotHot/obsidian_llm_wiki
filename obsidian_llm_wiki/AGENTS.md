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

### 1. RTK - Rust Token Killer

**Usage**: Token-optimized CLI proxy for shell commands.
- **Agents without native bash interception hooks** (e.g. Antigravity, OpenCode): MUST explicitly prefix shell commands with `rtk`.

#### Rule
Always prefix shell commands with `rtk` to minimize token consumption.

Examples:
```bash
rtk git status
rtk git diff
rtk ls wiki/concepts/
rtk grep -rn "pattern" wiki/
rtk python3 .agents/skills/kb-health/scripts/check_health.py
```

#### Meta Commands
```bash
rtk gain              # Show token savings
rtk gain --history    # Command history with savings
rtk discover          # Find missed RTK opportunities
rtk proxy <cmd>       # Run raw (no filtering, for debugging)
```

#### Why
RTK filters and compresses command output before it reaches the LLM context, cutting up to 90% of the bash output on common operations. Always use `rtk <cmd>` instead of raw commands.

---

### 2. Git Commit Rules

#### Constraints
- **NO Automatic Git Commits**: Do NOT run `git commit` or automatically commit changes unless the user explicitly instructs you to commit.
- Always leave modified files staged/unstaged for the user to review and commit manually.
- **Vault Privacy Awareness**: Note `.gitignore` boundaries — note contents in `raw/articles/*`, `wiki/*/*`, `reports/*`, as well as `index.md`, `log.md`, and `wiki/TODO.md` are local-only / gitignored by default. Only constitutional, design, and agent configuration files are tracked in git.

---

### 3. Sensitive File Access Rules

#### Constraints
- Sensitive configuration and credential paths (secrets, API keys, tokens) are listed in `.agentignore`. Read `.agentignore` to know which paths are off-limits and respect them.
- Before reading, inspecting, parsing, or accessing any file or directory containing secrets, ask the user for explicit permission.
- Do not inspect, print, parse, or output secret credentials in context or responses.

---

### 4. Respect `.agentignore`

#### Constraints
- `.agentignore` (gitignore syntax) lists files and directories agents must not access.
- Do NOT read, search, inspect, parse, print, or edit any path matching `.agentignore`, unless the user gives explicit permission for that specific path.
- Skip matching paths in globs, greps, and directory scans.

---

### 5. Knowledge Base Operations & Schema Governance

Every agent action that reads, writes, or restructures vault content must strictly adhere to `SCHEMA.md`:

1. **Frontmatter Schema**: Every wiki page in `wiki/` must have valid YAML frontmatter conforming to `SCHEMA.md` (`title`, `created`, `updated`, `type`, `tags` from the controlled taxonomy, `sources`, `confidence`, `contested`, `contradictions`, `status`).
2. **Wikilinks**: Use `[[NoteName]]` or `[[Folder/NoteName|Display Name]]`. Ensure a minimum of 2 outbound links per concept or entity note.
3. **Immutable Raw Layer (`raw/`)**: Never modify raw sources after creation. Raw clips must include `source_url`, `ingested`, and `sha256` hash. Author links in raw clips are normalized to plain text to avoid orphan stub creation.
4. **Page Thresholds & Decompositions**:
   - Create a page only when a concept/entity appears in $\ge 2$ sources or is the central topic of an approved spec.
   - When a note exceeds **200 lines**, decompose into focused sub-topic notes linked back to a parent overview.
   - **Mass-Update Guardrail**: If an operation modifies **10 or more** wiki pages, summarize the planned changes and ask for user confirmation before editing.
5. **Contradiction Policy**: When incoming information conflicts with existing knowledge, document both sides with source citations, set `contested: true`, list contradictions, and log in `log.md` and `wiki/TODO.md`.
6. **Logging & Catalog Integrity**: Every compilation (`/kb-compile`), indexing (`/kb-index`), health audit (`/kb-health`), report (`/kb-report`), or archiving action MUST append to `log.md` and update `index.md`.

---

### 6. Skill Ecosystem & Contextual Selection

#### Core Philosophy
- **Lightest Sufficient Ceremony**: Apply the simplest and lightest workflow sufficient to solve the problem safely and correctly. Simple lookups or single-note edits do not require heavy multi-step planning.
- **Autonomous & On-Demand**: Evaluate vault tasks and activate skills contextually.

#### Sweet Spots & Activation Triggers

1. **Obsidian LLM Wiki (`/kb-*`) — Core Operations Engine**:
   - Ingesting external sources or web clips $\rightarrow$ `/kb-compile`.
   - Extracting and collecting universal concepts/entities from project repositories into `raw/articles/` $\rightarrow$ `/kb-colluni`.
   - Rebuilding master catalog `index.md`, concept maps, and glossary $\rightarrow$ `/kb-index`.
   - Auditing broken links, orphan notes, and metadata gaps $\rightarrow$ `/kb-health`.
   - Quick lookups answered in chat (read-only, no files written) $\rightarrow$ `/kb-ask`.
   - Deep multi-source investigations and architectural syntheses $\rightarrow$ `/kb-report` ("Never Answer in Chat, Always Answer in Files" — applies to deep analysis; quick lookups via `/kb-ask` may answer in chat).
   - **Web Search Policy**: `/kb-ask` and `/kb-report` may search the web only when the wiki lacks the answer, and MUST ask/notify the user before searching; web-sourced content is labeled unverified.

2. **Baseline Guardrail (`karpathy-guidelines`)**:
   - *Active on every turn*: Think before editing, make surgical changes (do not touch unrelated notes or reformat arbitrary files), and verify integrity (`check_health.py`, link validity) before declaring completion (`verification-before-completion`).
   - *Content Quality & Simplicity*: Keep notes atomic, dense, and high-signal. Avoid conversational fluff, redundant preamble, or speculative categorization. Prefer 1 crisp note over multiple empty stubs.

3. **Superpowers (High-Ceremony / Macro Knowledge Work)**:
   - *Sweet Spots*: Major vault reorganizations, multi-step structural taxonomy redesigns, or drafting large multi-part synthesis reports $\rightarrow$ `brainstorming`, `writing-plans`.
   - *Skip For*: Software development lifecycle skills (TDD, worktrees, code debugging) are not applicable to standard knowledge vault curation.

4. **Herdr (Terminal & Multi-Agent Multiplexing)**:
   - *Sweet Spots*: Only activate when `HERDR_ENV=1` to coordinate terminal panes or subagents.

---

### 7. Conflict Resolution & User Alignment Protocol

When documentation choices or organizational rules present tradeoffs:

1. **Scope-Based Heuristics**:
   - *Small / Trivial Edits*: Favor Karpathy simplicity (concise notes, surgical updates, minimal ceremony).
   - *Large Refactoring / Structural Migrations*: Favor Superpowers (phased plans, clear milestones, health verification).

2. **Interactive Conflict Resolution (Ask Before Acting)**:
   - When facing architectural forks (e.g. splitting a cohesive note vs keeping it unified; creating a new entity vs merging into an existing concept note; in-place revision vs archiving to `wiki/_archive/`):
     1. **State the Dilemma**: Briefly outline the conflicting options.
     2. **Recommend**: State the recommended option with a 1-sentence rationale based on `SCHEMA.md`.
     3. **Ask the User**: Let the user choose the preferred direction before proceeding.