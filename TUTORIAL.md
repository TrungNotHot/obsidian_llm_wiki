# Tutorial: LLM Wiki — `llm_wiki_4pj` + `obsidian_llm_wiki`

This repository contains two separate projects based on Andrej Karpathy's LLM Wiki ideas and Hermes Agent principles. AI agents write and maintain the wiki; people read and review it in Obsidian.

| | `llm_wiki_4pj` | `obsidian_llm_wiki` |
|---|---|---|
| Role | Template embedded in a software project | Central general knowledge vault, independent of any project |
| Wiki location | `<project>/docs/` after scaffolding | `obsidian_llm_wiki/` inside this repository |
| Note partitions | `universal/` for reusable knowledge, `local/` for project details | Flat `concepts/` and `entities/` directories for general knowledge |
| Git policy | Notes are tracked alongside project code | Personal notes are ignored; schemas, templates, and agent configuration are tracked |
| Additional skill | — | `/kb-colluni` |
| Shared skills | `/kb-compile`, `/kb-report`, `/kb-index`, `/kb-health` | Same |

## 1. Repository Layout and Knowledge Flow

Clone the shared repository:

```bash
git clone https://github.com/TrungNotHot/obsidian_llm_wiki.git
cd obsidian_llm_wiki
```

The checkout directory and the central vault directory share the same name. Inside the checkout, the layout is:

```text
<repository-root>/
├── .git/                  # Git metadata for both projects
├── README.md
├── TUTORIAL.md
├── obsidian_llm_wiki/      # Central vault
│   ├── .gitignore
│   ├── index.example.md
│   ├── log.example.md
│   ├── raw/
│   ├── wiki/
│   │   └── TODO.example.md
│   └── reports/
└── llm_wiki_4pj/           # Project wiki template
    ├── .gitignore
    ├── setup.sh
    └── docs/
```

Both projects are regular directories, not submodules or nested repositories. There is no root `.gitignore`; each project's rules apply within its own directory. Run Git review, commit, and push commands from the repository root. Unless stated otherwise, setup commands below also start there.

```text
 Project A (llm_wiki_4pj)        Project B (llm_wiki_4pj)
 docs/wiki/*/universal/          docs/wiki/*/universal/
              |                         |
              +------ /kb-colluni -------+
                          |
                          v
        obsidian_llm_wiki/raw/articles/    (raw sources without wikilinks)
                          | /kb-compile
                          v
        obsidian_llm_wiki/wiki/concepts|entities/
                          | /kb-report
                          v
        obsidian_llm_wiki/reports/
```

Work in each software project, capture reusable knowledge in `universal/`, and periodically collect it into the central vault.

## 2. The Three Layers

Paths in this table are relative to the vault: `obsidian_llm_wiki/` for central knowledge, or `<project>/docs/` for a project wiki.

| Layer | Directory | Rules |
|---|---|---|
| Raw | `raw/` | Immutable web clips, specifications, and converted documents. Frontmatter includes `source_url` or `source_file`, `ingested`, and `sha256`. |
| Wiki | `wiki/` | Living notes maintained by agents: `concepts/`, `entities/`, `easy_read/`, `_archive/`, and `TODO.md`. |
| Reports | `reports/` | Permanent investigation results: *Never answer in chat, always answer in files.* |

Governance files are `SCHEMA.md` (rules and taxonomy), `index.md` (catalog and glossary), and `log.md` (append-only operations log).

## 3. Prerequisites and MCP Configuration

- An agent that reads `CLAUDE.md` or `AGENTS.md` and supports skills. The repository includes Claude Code skills under `.claude/skills/` and agent skills under `.agents/skills/`.
- Python 3 for the `kb-health` and `kb-compile` scripts.
- [Obsidian](https://obsidian.md) for browsing notes, graphs, and backlinks.
- Optional Obsidian MCP integration: install the **Local REST API** plugin, configure its port (normally `27124`), and install `uvx` if required by the MCP configuration.

Each project includes `.mcp.json` and `.agents/mcp_config.json`. These files are versioned and reference environment variables. Set `OBSIDIAN_API_KEY` in the environment of the process launching your agent; keep the actual value out of committed files. Both project `.gitignore` files ignore `.env*`, plugin `data.json` files, and the `remotely-save` credential directory.

A `.env` file is not automatically loaded by every agent or shell. Export the required variables or use your agent's supported environment-loading mechanism before launching it. Without MCP, the agent can still edit Markdown files directly.

## 4. Set Up the Central Vault (`obsidian_llm_wiki`)

1. In Obsidian, choose *Open folder as vault* and select `<repository-root>/obsidian_llm_wiki/`, not the repository root.
2. Initialize missing local files from their versioned examples:

   ```bash
   cd obsidian_llm_wiki
   test -e index.md || cp index.example.md index.md
   test -e log.md || cp log.example.md log.md
   test -e wiki/TODO.md || cp wiki/TODO.example.md wiki/TODO.md
   cd ..
   ```

   These commands preserve existing files. `index.md`, `log.md`, and `wiki/TODO.md` remain local-only; the `.example.md` files are versioned templates.

3. Adjust **Domain** and the tag taxonomy in `SCHEMA.md` if needed. Add new tags to the schema before using them.
4. Launch your agent from `<repository-root>/obsidian_llm_wiki/` so it uses the vault's instructions and skills.

## 5. Add a Wiki to a Software Project (`llm_wiki_4pj`)

Start from the shared repository root. The target project directory must already exist:

```bash
cd llm_wiki_4pj
./setup.sh /path/to/your-project
cp -n CLAUDE.md /path/to/your-project/
cd ..
```

`setup.sh` copies `.agents/`, `.claude/`, `AGENTS.md`, and `docs/`, including `docs/.obsidian/`, without overwriting existing files. It also copies `.mcp.json` when the source exists and the target does not; missing local MCP configuration does not stop setup. `CLAUDE.md` is copied separately in the command above.

The script makes the helper scripts executable. If the target already has a `.gitignore` and it does not contain `docs/raw/binary`, setup appends rules for binary sources, Superpowers drafts, and Obsidian workspace state. It does not create a missing target `.gitignore` or copy the template's entire ignore policy. Ensure the target project also ignores its `.env*` files and credential-bearing plugin state.

Open `<project>/docs/SCHEMA.md`, find **Part 2: Project Domain Configuration**, and set **Domain Scope** and **Project-Specific Domain Tags**, such as `billing` or `api`. Open `<project>/docs/` as an Obsidian vault if desired, and launch your agent from the target project root.

## 6. Available Skills

Run skills from the relevant project root or central vault directory. Output paths below are relative to that vault.

| Skill | Purpose | Output |
|---|---|---|
| `/kb-compile` | Turn sources in `raw/`, or external URLs, into atomic notes | `wiki/`, `index.md`, `log.md` |
| `/kb-report <question>` | Investigate a topic and write a permanent report; reusable conclusions feed back into concepts | `reports/` |
| `/kb-index` | Rebuild the catalog, glossary, and concept map | `index.md` |
| `/kb-health` | Check broken links, orphans, stale notes, metadata, and code–documentation drift | `wiki/TODO.md` |
| `/kb-colluni` (central vault only) | Collect universal knowledge from project wikis | `raw/articles/` only |

Compile, index, health, report, and archive operations must append to `log.md` and update `index.md`.

## 7. Example Workflows

### A. Work Inside a Software Project

1. Add references to `docs/raw/articles/`, or binary documents to `docs/raw/binary/`.
2. Run `/kb-compile`. Reusable patterns go into `docs/wiki/concepts|entities/universal/`; project details go into `local/`.
3. Investigate a deeper question, for example: `/kb-report Why does the employee-load DAG process unchanged rows?`
4. Run `/kb-index` and `/kb-health`, review the diff, and commit manually in the software project's repository.

### B. Collect Reusable Knowledge into the Central Vault

1. From `obsidian_llm_wiki/`, run `/kb-colluni` and identify the source project or vault.
2. The skill reads the source `index.md` sections *Universal Architecture Patterns* and *Universal Platforms & Infrastructure*, falling back to `*/universal/` directories.
3. The agent rewrites the material: project-specific names become general case studies, internal paths are removed, and formulas, diagrams, tables, and pseudocode are preserved.
4. Output goes to `raw/articles/<kebab-case-slug>.md`, without `[[wikilinks]]` that could create ghost backlinks. This collection step does not modify `wiki/` or `index.md`.
5. Run `/kb-compile` to synthesize and cross-link the collected material into the central wiki.

### C. Maintain the Wiki

Run `/kb-index` after major changes and `/kb-health` regularly. Review and resolve items in `wiki/TODO.md`.

## 8. Note Rules (`SCHEMA.md`)

```yaml
---
title: "Watermark Incremental Sync"
created: 2026-01-01
updated: 2026-01-01
type: concept                   # concept|entity|comparison|query|report|architecture|guide
tags: [architecture, pipeline]  # Select from the controlled taxonomy
sources: [raw/articles/some-source.md]
confidence: high                # high|medium|low
contested: false
contradictions: []
status: published               # published|draft|deprecated
---
```

- Use lowercase, hyphen-separated filenames. Each concept or entity needs at least two outbound `[[wikilinks]]`; update `updated` whenever the note changes.
- When synthesizing at least three sources, add provenance markers such as `^[raw/source.md]` to key paragraphs.
- Create a page when its topic appears in at least two sources or is the main focus of an approved specification. Split pages longer than 200 lines.
- Before changing ten or more existing wiki pages, the agent must summarize the changes and obtain confirmation.
- Preserve both sides of unresolved contradictions, with dates and sources. Set `contested: true`, list `contradictions`, and update the log and TODO.
- Archive superseded notes in `wiki/_archive/<subfolder>/`, remove their catalog entries, mark incoming links as `[[slug]] (archived)`, and log the operation.
- Split catalog sections exceeding 50 entries. Add `wiki/topic-map.md` above 200 cataloged pages. Rotate logs exceeding 500 entries into `log-YYYY.md`.

## 9. Guardrails and Git Workflow

- **No automatic commits.** Agents leave changes for you to review.
- **Sensitive access:** follow `AGENTS.md`, `CLAUDE.md`, and `.agentignore`. Versioning an MCP configuration does not remove agent access restrictions. Agents need explicit permission to access protected paths.
- **Versioned configuration:** keep MCP configuration free of literal credentials. Actual secrets belong in the environment or ignored `.env*` files.
- **Git scope:** project wiki notes are tracked; central vault notes remain local-only. Central examples, schemas, and agent configuration are tracked.
- **One Git repository:** both template projects use the root `.git`. Review and push shared repository changes from `<repository-root>/`; do not initialize Git inside either project directory.
- Use a lightweight workflow for small tasks; use planning for major reorganizations.

```bash
# Run from the shared repository root.
git status
git diff
# Stage only the files you reviewed, then commit and push manually.
```

## 10. Troubleshooting

| Symptom | Action |
|---|---|
| Ghost or unresolved nodes in the graph | Avoid unintended `[[wikilinks]]` when ingesting raw clips; run `/kb-health`. Preserve immutable raw sources. |
| `/kb-colluni` finds no reusable content | Check the source catalog's universal sections or its `*/universal/` directories. |
| `/kb-*` skills are missing | Launch the agent from the project or vault directory containing `.claude/skills/kb-*`. |
| `check_health.py` is not executable | Run `chmod +x .claude/skills/kb-health/scripts/check_health.py` from the relevant project or vault directory. |
| MCP does not connect | Start Obsidian and Local REST API, verify the configured port, and provide `OBSIDIAN_API_KEY` to the agent process; direct file editing remains available. |
| `index.md`, `log.md`, or central `wiki/TODO.md` is missing after cloning | Initialize it from the corresponding `.example.md` file using section 4. |
| The agent ignores project rules | Check that `CLAUDE.md` and `AGENTS.md` are in the directory from which you launch the agent. |
