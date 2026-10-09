# Concepts Layer (`wiki/concepts/`)

This directory stores atomic, reusable concept notes maintained by AI agents, covering architectural patterns, domain models, algorithms, and technical mechanisms.

---

## 📐 Conventions & Rules (per [[SCHEMA]])

1. **Atomic & Focused**: Each note covers exactly one concept, pattern, or mechanism. Keep notes concise and scannable (< 200 lines).
2. **Standard Frontmatter**:
   ```yaml
   ---
   title: "Concept Name"
   created: YYYY-MM-DD
   updated: YYYY-MM-DD
   type: concept
   tags: [concept, <domain-tag>]
   confidence: high # high | medium | low
   contested: false
   status: published
   ---
   ```
3. **Connectivity**: Every concept note must contain at least **2 outbound wikilinks** (`[[...]]`) connecting to related entities, architectural guides, or parent concepts.
