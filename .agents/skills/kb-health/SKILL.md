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

1. **Layer 1 — Script Scan (deterministic)**:
   - Run the bundled standalone health check script via terminal:
     ```bash
     python3 <path-to-this-skill>/scripts/check_health.py .
     ```
     *(Replace `<path-to-this-skill>` with this skill's own directory and add `--json` for machine-readable output).*
   - **Evaluate Output**:
     - Check reported broken `[[...]]` links.
     - Check orphan notes in `wiki/` (0 inbound links).
     - Check notes flagged with `contested: true` or `confidence: low`.
     - Check stale notes (>90 days without updates) and oversized pages (>200 lines).
   - The script is fast but blind to semantic issues — it NEVER replaces Layer 2 below.

2. **Layer 2 — Agent Sweep (mandatory, covers what the script cannot)**:
   - **Index completeness**: list all pages under `wiki/` and confirm each appears in `index.md`.
   - **Frontmatter & taxonomy**: every wiki page must have `title, created, updated, type, tags, sources`; every tag must exist in the `SCHEMA.md` taxonomy.
   - **Quality signals**: surface `confidence: low` pages and single-source pages with no confidence field.
   - **Source drift**: for each `raw/` file with `sha256:` frontmatter, recompute the body hash and flag mismatches (raw/ is immutable).
   - **Contradiction review**: find pages sharing tags/entities with conflicting claims; read the candidates and flag genuine conflicts per the `SCHEMA.md` contradiction policy (script regex cannot do this).
   - **Code vs doc drift**: compare active codebase components, modules, or data contracts against `wiki/entities/`; flag modules with no matching entity page.
   - **Log rotation**: if `log.md` exceeds 500 entries, rotate to `log-YYYY.md` and start fresh.
   - If any check is skipped, state which one and why in `log.md` — silent skipping is not allowed.

3. **Generate or Update `wiki/TODO.md`**:
   - Synthesize findings from BOTH layers into an actionable checklist grouped by severity:
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

4. **Log the Health Check**:
   - Append to `log.md`:
     ```markdown
     ## [YYYY-MM-DD] Health | Vault Health Check
     - Layer 1 (script): <N broken links, M orphans, ...>.
     - Layer 2 (agent): <index/frontmatter/drift/contradiction findings or "skipped: <check> because <reason>">.
     - Actionable items logged to `wiki/TODO.md`.
     ```
