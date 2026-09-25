---
name: kb-health
description: Runs linting checks, creates TODO notes where gaps are found.
---

# /kb-health Skill

Runs linting checks across the knowledge vault and codebase, identifies gaps, inconsistencies, and creates actionable TODO notes.

## Purpose
Maintains high integrity and low chaos across living documentation. Ensures source code across primary codebase directories (e.g. `src/`, `app/`, `lib/`, `dags/`) never drifts out of sync with documentation in `wiki/`.

> Follow vault integrity rules, directory conventions, and auditing standards defined in `references/wiki-guidelines.md`.

## Workflow Steps:

1. **Automated Graph & Vault Integrity Verification**:
   - Run the bundled standalone health check script via terminal:
     ```bash
     python3 .agents/plugins/obsidian-llm-wiki/skills/kb-health/scripts/check_health.py .
     ```
     *(Add `--json` if structured machine-readable output is preferred).*
   - **Evaluate Output**:
     - Check reported broken `[[...]]` links.
     - Check orphan notes in `wiki/` (0 inbound links).
     - Check notes flagged with `contested: true` or `confidence: low`.
     - Check stale notes (>90 days without updates) and oversized pages (>200 lines).

2. **Schema & Tag Taxonomy Validation**:
   - Verify note frontmatter conforms to `SCHEMA.md`.
   - Check if any notes introduce rogue tags outside the approved taxonomy.
   - Flag notes over **200 lines** as candidates for splitting.

3. **Code vs Doc Drift Auditing**:
   - Compare active components, modules, services, or data contracts in the codebase against documentation in `wiki/`.
   - Verify if newly added/modified modules or interfaces have matching entity pages in `wiki/entities/`.

4. **Generate or Update `wiki/TODO.md`**:
   - Synthesize findings into an actionable checklist grouped by severity:
     ```markdown
     # Knowledge Base Health TODOs
     Last checked: YYYY-MM-DD

     ## 🔴 High Severity: Broken Links & Critical Code Drift
     - [ ] Note `path/to/note.md` links to non-existent `[[MissingNote]]`
     - [ ] Module/Service `module_name` in codebase has no corresponding entity note in `wiki/entities/`

     ## 🟡 Medium Severity: Contested Pages & Stale Notes
     - [ ] Note `[[NoteName]]` is marked `contested: true` with conflicting claims
     - [ ] Note `[[OldNote]]` has not been updated in >90 days

     ## 🟢 Low Severity: Orphan Pages & Taxonomy Cleanup
     - [ ] Note `[[OrphanNote]]` has 0 inbound links; link it from `index.md` or a concept note
     ```

5. **Log the Health Check**:
   - Append to `log.md`:
     ```markdown
     ## [YYYY-MM-DD] Health | Vault Health Check
     - Checked broken links, orphans, contested notes, and code drift.
     - Actionable items logged to `wiki/TODO.md`.
     ```
