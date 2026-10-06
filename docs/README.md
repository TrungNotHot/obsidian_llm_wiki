# Project Knowledge Vault

Welcome to the **Knowledge Vault** — a persistent, compounding technical knowledge repository managed by AI agents and navigated via Obsidian, built on the principles of Andrej Karpathy's LLM Wiki and Hermes Agent architecture.

---

## 🏛️ 3-Layer Architecture

```
docs/
├── SCHEMA.md            # Constitutional schema, tag taxonomy, and quality rules
├── index.md             # Content catalog & master navigation map
├── log.md               # Chronological append-only operations log
│
├── raw/                 # Layer 1: Immutable Sources (read-only)
│   ├── articles/        # Clipped web articles and technical write-ups
│   ├── assets/          # Downloaded diagrams, images, and attachments
│   └── superpowers/     # Historical design specs and phased execution plans
│
├── wiki/                # Layer 2: Living Knowledge Wiki (agent-maintained)
│   ├── concepts/        # Atomic architectural, algorithmic, and data modeling concepts
│   │   ├── universal/   # Universal engineering patterns (portable to General Vault)
│   │   └── local/       # Project-specific mechanisms and domain logic
│   ├── entities/        # External systems, databases, APIs, and platform registries
│   │   ├── universal/   # Compute engines & infrastructure platforms (portable)
│   │   └── local/       # Project-specific data sources & corporate integrations
│   ├── easy_read/       # Stakeholder & developer end-to-end pipeline guides
│   └── _archive/        # Superseded, deprecated, or decommissioned notes
│
└── reports/             # Layer 3: Permanent Deep Syntheses & Query Reports
```

---

## 🧭 Master Navigation Files

- **`SCHEMA.md`**: The internal constitution governing naming conventions, tag taxonomy, page thresholds (split >200 lines), contradiction policy, quality signals (`confidence`, `contested`), and the `universal/` vs `local/` layout convention.
- **`index.md`**: Master catalog organizing every living note, architecture guide, and deep report by functional domain.
- **`log.md`**: Chronological audit trail tracking all compilations, report generations, and vault health audits.
- **`wiki/TODO.md`**: Actionable integrity backlog for broken links, code-doc drift, and content gaps.

---

## 🛠️ Operating Principles

1. **Obsidian is the IDE; the Agent is the Maintainer**: Developers view graph connections, read guides, and explore architecture in Obsidian; AI agents maintain cross-references, update summaries, and log changes.
2. **Never Answer in Chat, Always Answer in Files**: High-value investigations and architectural syntheses are permanently filed in `reports/` and compounded back into `wiki/concepts/`.
3. **Immutable Raw Sources**: Content in `raw/` is never modified after ingestion.
4. **Universal vs Local Separation**: Concepts and entities are partitioned into `universal/` (reusable cross-project engineering assets) and `local/` (project-specific implementations). The `universal/` trees can be exported or symlinked directly to a central General Knowledge Vault.
