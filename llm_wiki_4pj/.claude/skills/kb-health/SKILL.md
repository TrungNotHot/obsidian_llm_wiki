---
name: kb-health
description: Runs linting checks, creates TODO notes where gaps are found.
---

# /kb-health Skill

Runs linting checks across the knowledge vault and codebase, identifies gaps, inconsistencies, and creates actionable TODO notes.

## Purpose
Maintains high integrity and low chaos across living documentation. Ensures source code across primary codebase directories (e.g. `src/`, `app/`, `lib/`, `dags/`) never drifts out of sync with documentation in `docs/wiki/`.

> Follow vault integrity rules, directory conventions, and auditing standards defined in `references/wiki-guidelines.md`.

## Workflow Steps:

1. **Layer 1 — Script Scan (deterministic)**:
   - Run the bundled standalone health check script via terminal:
     ```bash
     python3 .claude/scripts/check_health.py docs
     ```
     *(Add `--json` for machine-readable output).*
   - **Evaluate Output**:
     - Check reported broken `[[...]]` links.
     - Review "links resolving only to `docs/raw/`": a `[[link]]` whose only match is a raw source usually means the same-named wiki note was deleted or renamed (a raw/ copy would otherwise mask it). Intentional links to raw specs are fine.
     - Check orphan notes in `docs/wiki/` (0 inbound links).
     - Check notes flagged with `contested: true` or `confidence: low`, and `confidence: high` notes with fewer than 2 `sources:` (rule in `docs/SCHEMA.md`: never `high` without 2+ sources).
     - **Index completeness**: "Not in index.md" lists wiki pages missing from `docs/index.md`.
     - **Frontmatter and taxonomy**: "Missing frontmatter fields" (required: `title, created, updated, type, tags`) and "Tags outside SCHEMA.md taxonomy".
     - **Source drift**: "Source drift" lists `docs/raw/` files whose body no longer matches the stored `sha256` (raw/ is immutable).
     - Check "Outdated vs cited source" (page `updated` is >90 days older than a raw source it cites: likely stale) and "Aging candidates" (>90 days since update). Age alone is not staleness: report an aging note as stale only if a newer source or note on the same entities exists. Check oversized pages (>300 lines, `docs/wiki/` notes only; `docs/raw/` and `docs/reports/` are not split).
   - The script is fast but blind to semantic issues — it NEVER replaces Layer 2 below.
   - **Clipper author-link policy**: Obsidian Web Clipper writes `author: "[[name]]"` wikilinks in `docs/raw/` frontmatter. These are never real links — normalize to plain text (`author: "name"`) on sight without asking. The script already excludes frontmatter from link scanning, so this is a silent normalization, not a broken-link fix.

2. **Layer 2 — Agent Sweep (mandatory, covers what the script cannot: semantic checks)**:
   - **Contradiction review** (needs reading, script regex cannot do this): the candidates come from the script, deterministically, so no area is silently skipped: its "Contradiction-review clusters" (specific tags with 2-8 notes) and "Contradiction-review pairs" (linked notes sharing 2+ topic tags, document-type tags excluded). Read every cluster and pair (use `python3 .claude/scripts/outline.py docs --seeds <notes> --hops 1` for a quick look at titles and headings when a cluster is large) and judge only whether their claims genuinely conflict, per the `docs/SCHEMA.md` contradiction policy. Do not replace the script's list with your own picks; if you skip any candidate, state which and why in `docs/log.md`.
   - **Code vs doc drift**: compare active codebase components, modules, services, or data contracts (e.g. `src/`, `app/`, `lib/`, `dags/`) against `docs/wiki/entities/`; flag modules with no matching entity page.
   - **Log rotation**: if `docs/log.md` exceeds 500 entries, rotate to `docs/log-YYYY.md` and start fresh.
   - If any check is skipped, state which one and why in `docs/log.md` — silent skipping is not allowed.

3. **Generate or Update `docs/wiki/TODO.md`**:
   - Synthesize findings from BOTH layers into an actionable checklist grouped by severity:
     ```markdown
     # Knowledge Base Health TODOs
     Last checked: YYYY-MM-DD

     ## 🔴 High Severity: Broken Links & Critical Code Drift
     - [ ] Note `path/to/note.md` links to non-existent `[[MissingNote]]`
     - [ ] Module/Service `module_name` in codebase has no corresponding entity note in `docs/wiki/entities/`

     ## 🟡 Medium Severity: Contested Pages & Stale Notes
     - [ ] Note `[[NoteName]]` is marked `contested: true` with conflicting claims
     - [ ] Note `[[OldNote]]` is older than a newer source on the same entities (update it, or archive it per the `SCHEMA.md` Archiving Workflow if superseded)

     ## 🟢 Low Severity: Orphan Pages & Taxonomy Cleanup
     - [ ] Note `[[OrphanNote]]` has 0 inbound links; link it from `docs/index.md` or a concept note
     ```

4. **Log the Health Check**:
   - Append to `docs/log.md`:
     ```markdown
     ## [YYYY-MM-DD] Health | Vault Health Check
     - Layer 1 (script): <N broken links, M orphans, ...>.
     - Layer 2 (agent): <index/frontmatter/drift/contradiction findings or "skipped: <check> because <reason>">.
     - Actionable items logged to `docs/wiki/TODO.md`.
     ```
