# LLM Wiki Knowledge Vault

Welcome to the **LLM Wiki Knowledge Base** — a persistent, compounding technical knowledge repository managed by AI agents and navigated via Obsidian, built on the principles of Andrej Karpathy's LLM Wiki and Hermes Agent architecture.

---

## 🏛️ 3-Layer Architecture

```
llm_wiki/
├── SCHEMA.md            # Layer 3: Constitutional schema, tag taxonomy, and quality rules
├── index.md             # Content catalog & master navigation map
├── log.md               # Chronological append-only operations log
│
├── raw/                 # Layer 1: Immutable Sources (read-only)
│   ├── articles/        # Clipped web articles and technical write-ups
│   ├── assets/          # Downloaded diagrams, images, and attachments
│   └── superpowers/     # Historical design specs and phased execution plans
│       ├── specs/       # Technical specifications
│       └── plans/       # Phased implementation plans
│
├── wiki/                # Layer 2: Living Knowledge Wiki (agent-maintained)
│   ├── concepts/        # Atomic architectural, algorithmic, and domain concepts
│   ├── entities/        # External systems, databases, APIs, and platform registries
│   ├── easy_read/       # Stakeholder guides, workflows, and architectural overviews
│   └── _archive/        # Superseded, deprecated, or decommissioned notes
│
└── reports/             # Permanent Deep Syntheses & Analytical Query Outputs
```

---

## 🧭 Master Navigation Files

- **`SCHEMA.md`**: The internal constitution governing naming conventions, tag taxonomy, page thresholds (split >200 lines), contradiction policy, and quality signals (`confidence`, `contested`).
- **`index.md`**: Master catalog organizing every living note, architecture guide, and deep report by functional domain.
- **`log.md`**: Chronological audit trail tracking all compilations, report generations, and vault health audits.
- **`wiki/TODO.md`**: Actionable integrity backlog for broken links, code-doc drift, and content gaps.

---

## 🛠️ Operating Principles

1. **Obsidian is the IDE; the Agent is the Maintainer**: Developers view graph connections, read guides, and explore knowledge in Obsidian; AI agents maintain cross-references, update summaries, and log changes.
2. **Never Answer in Chat, Always Answer in Files**: High-value investigations and architectural syntheses are permanently filed in `reports/` and compounded back into `wiki/concepts/`.
3. **Immutable Raw Sources**: Content in `raw/` is never modified after creation.
