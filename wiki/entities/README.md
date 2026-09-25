# Entities Layer (`wiki/entities/`)

This directory stores entity registry notes for external platforms, databases, source APIs, third-party services, and core infrastructure components.

---

## 📐 Conventions & Rules (per [[SCHEMA]])

1. **Entity Granularity**: One page per notable external system, database, or API service.
2. **Standard Frontmatter**:
   ```yaml
   ---
   title: "Entity Name"
   created: YYYY-MM-DD
   updated: YYYY-MM-DD
   type: entity
   tags: [entity, <domain-tag>]
   confidence: high # high | medium | low
   contested: false
   status: published
   ---
   ```
3. **Connectivity**: Every entity page must link to at least **2 related concepts, downstream guides, or parent platforms** using `[[...]]`.
