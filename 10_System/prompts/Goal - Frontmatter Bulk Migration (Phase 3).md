---
title: Goal - Frontmatter Bulk Migration (Phase 3)
created: 2026-07-11 00:00:00+00:00
modified: 2026-07-11 00:00:00+00:00
tags:
- prodos/prompt
- topic/pkm
- migration
aliases: []
prodos:
  kind: prompt
  lifecycle: active
  prompt:
    description: Bulk-migrate legacy frontmatter (type/status/updated/last_reviewed)
      to the prodos object across ProdOS territory.
    inject_as: system_context
---


## /goal — Frontmatter Bulk Migration (Phase 3)

You are executing Phase 3 (bulk normalisation) of [[SoT - ProdOS Note Metadata (Frontmatter)]]. That SoT is the canonical spec; its §6 legacy mapping table governs every transformation. This prompt adds scope, ordering, and safety rails only.

### Scope

**In scope:** `30_Library/**`, `20_Thinking/**`, `10_System/**`, `01_journals/**`, `00_Inbox/**`.
**Out of scope — never touch:** `raw/` (sealed per AGENTS.md §2.1), `wiki/` (has its own dossier schema), `output/`, `.trash/`, `.obsidian/`, `AGENTS.md`, `index.md`, `log.md`.

This is an explicitly authorised human-instructed bulk edit of `30_Library/` frontmatter ONLY. Note bodies are read-only: change nothing below the closing `---`. Abort any file where the frontmatter cannot be parsed as YAML; log it instead.

### Mapping rules (measured against current vault state, 2026-07-11)

Folder is normative for `prodos.kind` (spec §3.2). Legacy `type` values and counts, with targets:

| Legacy `type` | Count | Action |
|:---|:---|:---|
| `concept`, `atom`, `permanent`, `note`, `''`, `null`, `'null'` (in `100_zettelkasten/`) | ~1,020 | `prodos.kind: atomic`; set `prodos.atomic.form: concept` unless tags indicate `hypothesis`/`claim`/`definition` |
| `SoT` | 267 | `prodos.kind: sot`; if filename starts `Protocol - `, use `protocol` |
| `daily` | 218 | `prodos.kind: journal` |
| `map` | 103 | `prodos.kind: moc` |
| `command`, `atomic_command`, `playbook` | ~75 | `prodos.kind: ops`; keep disambiguation in `tags` |
| anything else | tail | Do NOT guess — log to the exceptions report for human decision |

Then, per spec §6: `status` → `prodos.lifecycle` (only for exact enum matches: `seedling/active/stable/evergreen/archived`; `draft` → `seedling`; anything else → exceptions report). `trust-level` → `prodos.trust`. `last_reviewed`/`review_interval` → `prodos.review.*`. `last_synthesis`/`synthesis-count` → `prodos.chronos.*`. `id`/`ID`/`uid` → `prodos.id`. Delete `updated` and `creation_date` (preserve into `created`/`modified` first if those are missing). Delete the legacy keys only after their values are captured.

If a note already has a `prodos` object, merge — never overwrite existing `prodos` values with legacy-derived ones.

### Execution order (checkpointed)

1. **Dry run.** Scan all in-scope notes; produce `output/reports/YYYY-MM-DD-frontmatter-migration-dryrun.md` containing: per-folder counts, the full exceptions list, and 10 sample before/after diffs. **Stop and wait for human approval.**
2. **Batch 1 — high-traffic:** `30_Library/MoC/`, `30_Library/SoT/`, `30_Library/ops/` (spec §8 priority). Git commit: `frontmatter migration: batch 1 (MoC/SoT/ops)`.
3. **Batch 2:** `30_Library/100_zettelkasten/`. Commit.
4. **Batch 3:** `30_Library/200_Projects/`, `20_Thinking/`, `10_System/`, `01_journals/`. Commit.
5. **Validate:** run `gemini-scribe/scripts/validate_note_frontmatter.py` (spec §9) over the vault; append results to the final report.
6. **Final report** to `output/reports/YYYY-MM-DD-frontmatter-migration-report.md`: counts migrated, exceptions remaining, validation failures. Append one entry to `log.md`.

### Hard rules

- One git commit per batch; never proceed past a failed commit.
- Never delete a legacy value that could not be mapped — exceptions keep their legacy keys untouched.
- Do not update `modified` timestamps for frontmatter-only migration edits (avoids destroying real modification history semantics) — log this decision in the report.
- If more than 5% of a batch hits exceptions, halt and report rather than continuing.
