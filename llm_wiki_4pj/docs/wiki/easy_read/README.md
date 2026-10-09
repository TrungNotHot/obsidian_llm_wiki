# System & Architecture Guides Layer (`wiki/easy_read/`)

This directory houses stakeholder- and developer-accessible architecture guides, end-to-end data flow specifications, and operational runbooks.

---

## 📂 Suggested Organization

Group guides by pipeline layer, microservice, or domain workflow:
- `ingestion/` or `staging/`: Raw extraction pipelines and input data contracts.
- `transformation/` or `services/`: Business logic, state machines, and data processing.
- `serving/` or `api/`: API endpoints, presentation models, and client contracts.
- `operations/`: Runbooks, alerting, and deployment guides.

---

## 📐 Conventions (per `docs/SCHEMA.md`)

- Every guide should provide clear, accessible explanations ("What it does", "Why it exists", "Data flow", "Configuration").
- Link to relevant concepts in `docs/wiki/concepts/` and entities in `docs/wiki/entities/`.
