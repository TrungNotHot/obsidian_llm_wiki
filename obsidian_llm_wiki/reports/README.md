# Reports & Syntheses Layer (`reports/`)

This directory stores permanent, high-value analytical outputs and architectural investigations produced by AI agents via `/kb-report`.

---

## 💎 The Golden Principle
> **"Never Answer in Chat, Always Answer in Files"**
> Complex architectural questions, deep lineage analyses, or multi-component comparisons must never be lost in transient chat sessions. They are authored as structured, persistent markdown assets here.

---

## 📝 Conventions & Standards

1. **File Naming**: Formatted as `YYYY-MM-DD-<topic_slug>.md` (e.g. `2026-09-25-initial-system-survey.md`).
2. **Frontmatter Standard**:
   ```yaml
   ---
   title: "Descriptive Report Title"
   created: YYYY-MM-DD
   type: report
   tags: [report, <domain-tag>]
   confidence: high | medium
   status: published
   ---
   ```
3. **Report Structure**:
   - **Executive Summary**: 2–3 sentence high-level finding.
   - **Detailed Technical Breakdown**: Data contracts, interfaces, lineage, or code walkthroughs.
   - **Visual Diagrams**: Mermaid sequence, flowchart, or ER diagrams.
   - **Backlinks**: Connected via `[[...]]` to relevant living notes in `wiki/`.

---

## 🔄 Compounding Knowledge Loop
When an investigation formalizes a reusable architectural pattern, core model rule, or comparative matrix, the agent automatically extracts an atomic concept into `wiki/concepts/` or `wiki/entities/`, linking the report and concept bidirectionally. Every query compounds the total intelligence of the vault.
