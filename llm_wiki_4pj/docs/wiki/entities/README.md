# Entities Layer (`wiki/entities/`)

This directory stores entity registry notes for external platforms, databases, source APIs, third-party services, and core infrastructure components.

To cleanly separate **Universal Platforms & Infrastructure** (reusable across technical projects / General Knowledge Base) and **Local Systems & Data Sources** (specific to this repository), this directory is organized into two subdirectories:

---

## 📂 Subdirectory Structure

### 1. `universal/` (Universal Platforms & Orchestration)
Underlying technology engines, container platforms, cloud services, and databases that apply across multiple projects:
- Add technology and platform notes here (e.g. `postgresql.md`, `redis.md`, `kubernetes.md`, `apache_kafka.md`).

### 2. `local/` (Project Systems & Data Sources)
Add your project-specific databases, third-party APIs, SaaS endpoints, and external services here:
- Examples: `stripe_payment_gateway.md`, `sendgrid_email_service.md`, `legacy_crm_database.md`.

---

## 📐 Conventions & Rules (per `docs/SCHEMA.md`)

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
3. **Connectivity**: Every entity page must link to at least **2 related concepts, downstream pipeline guides, or parent platforms** using `[[...]]`.
