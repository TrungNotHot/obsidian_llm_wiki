# LLM Wiki for Projects (`llm_wiki_4pj`)

A production-ready, standardized starter kit for embedding an **Andrej Karpathy LLM Wiki** inside any software repository or data platform.

Designed for AI pair-programming assistants (Antigravity, Claude Code, Cursor, Copilot) to author, maintain, and compound project knowledge directly inside code repositories, visualized seamlessly with **Obsidian**.

---

## 🌟 Key Architecture & Highlights

1. **3-Layer Compounding Architecture**:
   - `docs/raw/`: Immutable reference documents, web clippings, and architecture specs with SHA-256 drift detection.
   - `docs/wiki/`: Living system architecture, maintained and kept in sync with code by AI agents.
   - `docs/reports/`: Permanent deep reports following the principle: *"Never Answer in Chat, Always Answer in Files"*.
2. **Symmetrical `universal/` vs `local/` Partitioning**:
   - `docs/wiki/concepts/universal/` & `docs/wiki/entities/universal/`: Core architectural patterns and platform engines. These can be exported, symlinked, or synced to a central **General Knowledge Base**.
   - `docs/wiki/concepts/local/` & `docs/wiki/entities/local/`: Project-specific domain rules, endpoints, and mechanisms.
3. **Turnkey AI Agent Skills**:
   - `/kb-compile`: Ingests documentation or URLs into atomic notes.
   - `/kb-report`: Investigates complex topics and outputs structured markdown reports.
   - `/kb-index`: Maintains `docs/index.md` master catalog and glossary.
   - `/kb-health`: Audits broken wikilinks, orphan notes, stale content, and code-doc drift.
4. **Pre-populated Universal Starter Pack**:
   - Includes proven patterns: Kimball 4-Step Star Schema, Append-on-Change CDC (xxHash64), Monotonic Watermark Sync, Surrogate Key handling, and 3-layer Retry strategies.
   - Includes platform baselines: Apache Airflow, Microsoft SQL Server, and Red Hat OpenShift / Kubernetes.

---

## 📁 Repository Structure

```text
llm_wiki_4pj/
├── README.md                  # This guide
├── setup.sh                   # Scaffolding helper script
├── .gitignore
│
├── .agents/                   # AI Agent Configuration & Skills
│   ├── mcp_config.json        # MCP definition for Obsidian Local REST API
│   └── skills/                # Standalone skills (kb-compile, kb-health, kb-index, kb-report)
│
└── docs/                      # Standard documentation scaffold
    ├── README.md              # Documentation orientation guide
    ├── SCHEMA.md              # 2-part constitutional schema (Universal + Project Config)
    ├── index.md               # Master navigation catalog & glossary
    ├── log.md                 # Chronological operations log
    ├── .obsidian/             # Obsidian workspace settings (auto-update links enabled)
    ├── raw/                   # Immutable sources
    │   ├── articles/          # Web clips & converted markdown
    │   ├── binary/            # Raw binary sources (.pdf, .docx, .pptx, .xlsx)
    │   ├── assets/            # Architecture diagrams & screenshots
    │   └── superpowers/       # Design specs and execution plans
    ├── wiki/                  # Living wiki notes
    │   ├── concepts/          # universal/ and local/
    │   ├── entities/          # universal/ and local/
    │   ├── easy_read/         # Pipeline / module walkthroughs
    │   └── _archive/          # Decommissioned notes
    └── reports/               # Permanent investigation reports
```

---

## 🚀 Quick Start: Scaffolding a New Project

### Method 1: Using `setup.sh` (Fastest)

Navigate to `llm_wiki_4pj` and run:

```bash
./setup.sh /path/to/your-target-project
```

The script will copy `.agents/` and `docs/` into your target repository and ensure clean initial states.

---

### Method 2: Manual Copy

Copy `.agents/` and `docs/` directly to your project root:

```bash
cp -r .agents /path/to/your-project/
cp -r docs /path/to/your-project/
```

---

### Method 3: Clone the Shared Repository

The scaffold now lives under `llm_wiki_4pj/` in the shared repository:

```bash
git clone https://github.com/TrungNotHot/obsidian_llm_wiki.git
cd obsidian_llm_wiki/llm_wiki_4pj
./setup.sh /path/to/your-target-project
```

---

## ⚙️ Project Customization (Only 2 Minutes)

Once scaffolded into a new project, you only need to customize **Part 2** of `docs/SCHEMA.md`:

1. Open `docs/SCHEMA.md`.
2. Scroll to `# Part 2: Project Domain Configuration`:
   - Update **Domain Scope**: Describe what this project does.
   - Update **Project-Specific Domain Tags**: Add domain tags relevant to your repository (e.g. `billing`, `checkout`, `customer`, `api`).
3. (Optional) In Obsidian, open the `docs/` folder as a Vault.

Everything else — all rules, safety thresholds, frontmatter formats, and `/kb-*` skills — works immediately out of the box!
