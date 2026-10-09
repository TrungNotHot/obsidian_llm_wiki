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
│   ├── binary/          # Raw binary sources (.pdf, .docx, .pptx, .xlsx, images)
│   └── assets/          # Downloaded diagrams, images, and attachments
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

- **`SCHEMA.md`**: The internal constitution governing naming conventions, tag taxonomy, page thresholds (split >300 lines), contradiction policy, and quality signals (`confidence`, `contested`).
- **`index.md`**: Master catalog organizing every living note, architecture guide, and deep report by functional domain.
- **`log.md`**: Chronological audit trail tracking all compilations, report generations, and vault health audits.
- **`wiki/TODO.md`**: Actionable integrity backlog for broken links, code-doc drift, and content gaps.

---

## 🧰 Skills

- `/kb-compile`: Ingests `raw/` sources into atomic notes in `wiki/`.
- `/kb-colluni`: Collects universal concepts from project vaults into `raw/articles/`.
- `/kb-ask`: Quick read-only Q&A over the wiki, answered in chat (asks before any web search).
- `/kb-report`: Deep multi-source investigation written to `reports/`.
- `/kb-index`: Rebuilds `index.md`, glossary, and concept maps.
- `/kb-health`: Audits broken links, orphans, and metadata gaps.

---

## 🛠️ Operating Principles

1. **Obsidian is the IDE; the Agent is the Maintainer**: Developers view graph connections, read guides, and explore knowledge in Obsidian; AI agents maintain cross-references, update summaries, and log changes.
2. **Never Answer in Chat, Always Answer in Files**: High-value investigations and architectural syntheses are permanently filed in `reports/` and compounded back into `wiki/concepts/`. Quick lookups via `/kb-ask` are the exception: answered in chat, read-only, no files written.
3. **Web Search Only When Needed**: `/kb-ask` and `/kb-report` search the web only when the wiki lacks the answer, and always ask the user first; web-sourced content is labeled unverified.
4. **Immutable Raw Sources**: Content in `raw/` is never modified after creation.
