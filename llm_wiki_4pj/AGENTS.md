# AI Agent Instructions & Workspace Guidelines

## 🏛️ Vault Summary & Architecture
- **Vault Purpose**: Project-Embedded Technical Knowledge Base & Living AI Wiki, navigated via Obsidian and maintained by AI pair-programming agents (based on Andrej Karpathy's LLM Wiki principles).
- **Domain Scope**: Software project architecture, system design, data pipelines, domain entities, architectural concepts, operational runbooks, and deep investigation reports for the host repository.
- **3-Layer Knowledge Architecture (Under `docs/`)**:
  - `docs/raw/`: Layer 1 — Immutable Sources (read-only web clips, converted binary docs, architectural specs, blueprints, assets).
  - `docs/wiki/`: Layer 2 — Living Knowledge Base:
    - `concepts/universal/` & `entities/universal/`: Cross-project architecture patterns, algorithms, and core platform engines (portable to a central Knowledge Base).
    - `concepts/local/` & `entities/local/`: Project-specific mechanism implementations, domain rules, and integration endpoints.
    - `easy_read/`: Walkthroughs and architectural layer overviews.
    - `_archive/`: Superseded or decommissioned documentation.
  - `docs/reports/`: Layer 3 — Permanent Deep Syntheses & analytical query reports ("Never Answer in Chat, Always Answer in Files").
- **Master Navigation & Governance**:
  - `docs/SCHEMA.md`: Constitutional schema, tag taxonomy, note thresholds, and contradiction rules.
  - `docs/index.md`: Master content catalog, navigation map, and technical glossary.
  - `docs/log.md`: Append-only chronological operations log.
  - `docs/wiki/TODO.md`: Integrity backlog for broken links, missing metadata, and content drift.

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
rtk ls docs/wiki/concepts/
rtk grep -rn "pattern" docs/wiki/
rtk python3 .agents/skills/kb-health/scripts/check_health.py docs
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
- **Repository Version Control Policy**: Unlike standalone personal vaults, project-embedded wiki notes (`docs/wiki/*`, `docs/reports/*`, `docs/index.md`, `docs/log.md`, `docs/raw/articles/*`) are tracked in Git alongside project code. Only raw binary sources (`docs/raw/binary/*`), superpower drafts, and Obsidian local workspace state (`docs/.obsidian/workspace*.json`) are gitignored.

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

Every agent action that reads, writes, or restructures vault content must strictly adhere to `docs/SCHEMA.md`:

1. **Frontmatter Schema**: Every wiki page in `docs/wiki/` must have valid YAML frontmatter conforming to `docs/SCHEMA.md` (`title`, `created`, `updated`, `type`, `tags` from the controlled taxonomy, `sources`, `confidence`, `contested`, `contradictions`, `status`).
2. **Wikilinks**: Use `[[NoteName]]` or `[[Folder/NoteName|Display Name]]`. Ensure a minimum of 2 outbound links per concept or entity note.
3. **Partitioning Rules**:
   - Save cross-cutting, reusable architectural patterns to `docs/wiki/concepts/universal/` and platform definitions to `docs/wiki/entities/universal/`.
   - Save project-specific logic, endpoints, and mechanisms to `docs/wiki/concepts/local/` and `docs/wiki/entities/local/`.
4. **Immutable Raw Layer (`docs/raw/`)**: Never modify raw sources after creation. Raw clips must include `source_url`, `ingested`, and `sha256` hash. Author links in raw clips are normalized to plain text to avoid orphan stub creation.
5. **Page Thresholds & Decompositions**:
   - Create a page only when a concept/entity appears in $\ge 2$ sources or is the central topic of an approved spec.
   - When a note exceeds **200 lines**, decompose into focused sub-topic notes linked back to a parent overview.
   - **Mass-Update Guardrail**: If an operation modifies **10 or more** wiki pages, summarize the planned changes and ask for user confirmation before editing.
6. **Contradiction Policy**: When incoming information conflicts with existing knowledge, document both sides with source citations, set `contested: true`, list contradictions, and log in `docs/log.md` and `docs/wiki/TODO.md`.
7. **Logging & Catalog Integrity**: Every compilation (`/kb-compile`), indexing (`/kb-index`), health audit (`/kb-health`), report (`/kb-report`), or archiving action MUST append to `docs/log.md` and update `docs/index.md`.

---

### 6. Skill Ecosystem & Contextual Selection

#### Core Philosophy
- **Lightest Sufficient Ceremony**: Apply the simplest and lightest workflow sufficient to solve the problem safely and correctly. Simple lookups or single-note edits do not require heavy multi-step planning.
- **Autonomous & On-Demand**: Evaluate vault tasks and activate skills contextually.

#### Sweet Spots & Activation Triggers

1. **Obsidian LLM Wiki (`/kb-*`) — Core Operations Engine**:
   - Ingesting external sources or web clips $\rightarrow$ `/kb-compile`.
   - Rebuilding master catalog `docs/index.md`, concept maps, and glossary $\rightarrow$ `/kb-index`.
   - Auditing broken links, orphan notes, and metadata gaps $\rightarrow$ `/kb-health`.
   - Deep multi-source investigations and architectural syntheses $\rightarrow$ `/kb-report` ("Never Answer in Chat, Always Answer in Files").

2. **Baseline Guardrail (`karpathy-guidelines`)**:
   - *Active on every turn*: Think before editing, make surgical changes (do not touch unrelated notes or reformat arbitrary files), and verify integrity (`check_health.py docs`, link validity) before declaring completion (`verification-before-completion`).
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
   - When facing architectural forks (e.g. splitting a cohesive note vs keeping it unified; creating a new entity vs merging into an existing concept note; in-place revision vs archiving to `docs/wiki/_archive/`):
     1. **State the Dilemma**: Briefly outline the conflicting options.
     2. **Recommend**: State the recommended option with a 1-sentence rationale based on `docs/SCHEMA.md`.
     3. **Ask the User**: Let the user choose the preferred direction before proceeding.