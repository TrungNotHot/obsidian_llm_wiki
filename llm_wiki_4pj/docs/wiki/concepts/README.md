# Concepts Layer (`wiki/concepts/`)

This directory stores atomic, reusable concept notes maintained by AI agents, covering architectural patterns, domain data models, transformation algorithms, and technical mechanisms.

To support both **Universal Architecture Patterns** (reusable across any technical project / General Knowledge Base) and **Local Project Implementations** (specific to this repository), this directory is organized into two subdirectories:

---

## 📂 Subdirectory Structure

### 1. `universal/` (Universal Architecture Patterns)
Core engineering principles, algorithms, and data modeling patterns independent of this specific project:
- Add concepts that can be shared across multiple projects or exported to a central General Knowledge Base (e.g. distributed locking, idempotent APIs, change data capture, retry strategies).

### 2. `local/` (Project-Specific Concepts)
Add your project-specific mechanisms, business transformation rules, and custom algorithms here:
- Examples: `user_authentication_flow.md`, `pricing_engine_discount_rules.md`, `order_state_machine.md`.

---

## 📐 Conventions & Rules (per `docs/SCHEMA.md`)

1. **Atomic & Focused**: Each note covers exactly one concept, pattern, or mechanism. Keep notes concise and scannable (split threshold: see [[SCHEMA]]).
2. **Standard Frontmatter**: follow the Frontmatter Schema in [[SCHEMA]] (single source of truth).
3. **Connectivity**: Every concept note must contain at least **2 outbound wikilinks** (`[[...]]`) connecting to related entities, architectural guides, or parent concepts.
