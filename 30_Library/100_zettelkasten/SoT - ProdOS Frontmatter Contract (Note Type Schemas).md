---
aliases: [Frontmatter Contract, FrontmatterContract, Note Type Schemas, TAC Frontmatter Schema]
conformant: true
created: 2026-07-17T00:00:00+00:00
modified: 2026-10-26T14:36:21+00:00
permalink: llmeon/30-library/so-t/so-t-prodos-frontmatter-contract-note-type-schemas
see_also: ["[[SoT - Atomic Note Standard (The Proposition Card)]]", "[[Goal - Frontmatter Bulk Migration (Phase 3)]]", "[[Protocol - Typed Answer Contract (TAC) for Vault Agents]]", "[[SoT - PRODOS Core Specification]]", "[[SoT - Typed Answer Contract (TAC) for LLM Output]]"]
project_category: prodos
tags: [domain/pkm, prodos/sot, topic/frontmatter, topic/knowledge-architecture]
title: SoT - ProdOS Frontmatter Contract (Note Type Schemas)
type: sot
---

> Canonical status: this note is the authoritative frontmatter spec for the vault. It replaced the retired workbench scratch note `Typed-Answer-Contract-RAG.md` as the home of this content. It does not supersede [[SoT - Typed Answer Contract (TAC) for LLM Output]], which covers the output side of TAC and is a separate, live note. `AGENTS.md`, `sys_merger` and every prompt with a `## TAC FRONTMATTER COMPLIANCE (MANDATORY)` block link here. Section numbers §1–§9 are cited by number elsewhere, so they stay fixed.
>
> Reviewed 2026-10-26 against `validate_note_frontmatter.py`, `validate_note_shape.py`, the `Note` fileClass and [[SoT - Atomic Note Standard (The Proposition Card)]]. Where this note and a script disagree, §9 says which is wrong.

## Minimum Viable Understanding (MVU)

Every note's frontmatter is a typed data contract, not free-form YAML. An agent editing or creating a note fills in the §2 envelope and, for the five knowledge-node types, the §3 schema. If it cannot do so with confidence, it sets `conformant: false` with a `non_conformance_reason` instead of writing a guessed block. This is the frontmatter instance of the vault's Typed Answer Contract principle: [[SoT - Typed Answer Contract (TAC) for LLM Output]] gives the theory and [[Protocol - Typed Answer Contract (TAC) for Vault Agents]] gives the enforcement callout used across prompts.

## 1. Typed Answer Contracts (TAC) Overview

Every agent write to a note's frontmatter is a typed data contract. Enforcement is by the two validators and the fileClasses (§5), not by a gate on every write. Legacy notes are tolerated, and new notes are held to the contract.

- `type` is required on every note. Obsidian's fileClass detection keys off it (`fileClassAlias: type`), so a note without it gets no schema, no validation and no editable Bases row.
- `title`, `tags` and `conformant` are required by both validators. `created` and `modified` are also required on atomic notes by `validate_note_shape.py`, and expected everywhere.
- `non_conformance_reason` is required whenever `conformant: false`.
- If an agent cannot fill the schema cleanly it MUST write `conformant: false` and say why.

---

## 2. The Frontmatter Contract (All Notes)

Any agent touching frontmatter MUST produce a valid `FrontmatterContract`, the shared envelope every note type inherits:

| Field | Required | Type | Rule |
|:------|:---------|:-----|:-----|
| `title` | Yes | string | Matches the filename without `.md`. |
| `type` | Yes | string | One of the 15 values below. Lowercase. |
| `tags` | Yes | list | Non-empty. Prefer hierarchical tags. |
| `conformant` | Yes | boolean | `false` if the note cannot be cleanly typed. Never `true` unless fully valid. |
| `non_conformance_reason` | Conditional | string | Required if `conformant: false`. Omit or leave empty when `true`. |
| `created`, `modified` | Yes on atomic notes | ISO 8601 | Never write `updated` or `creation_date`. |
| `status` | No | string | `draft`, `seed`, `stable`, `evergreen`, `stale`, `superseded`. Meanings and promotion criteria: [[Note Status Lifecycle]]. |
| `supersedes` | No | list of wikilinks | Older note(s) this one replaces. Set on the surviving note. |
| `superseded_by` | Conditional | list of wikilinks | Required if `status: superseded`. |
| `aliases` | No | list | Alternative names. |
| `see_also` | No | list of wikilinks | Related notes. Typed edges go in the body ([[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]). |
| `project_name`, `project_category` | No | string | Parent project context, for example `prodos`, `devops`, `personal`. |
| `own_words` | No | boolean | Marks a protected note. See below. |

`type` values: `claim`, `concept`, `evidence`, `question`, `procedure` (the five knowledge nodes, §3) and `protocol`, `map`, `journal`, `project`, `sot`, `link_report`, `equipment`, `source`, `prompt`, `tombstone` (routing types, envelope only).

Routing types:

- `prompt` lives in `10_System/prompts/` (added 2026-10-16).
- `source` is the per-book or per-article hub named `Source - Title` in `100_zettelkasten/`. It carries `source_reference`, `authors`, `year`, `calibre_id` and `calibre_link`.
- `tombstone` is a retired HEAD note kept at its original title. Its shape is in [[SoT - HEAD Note Contract (The Workbench)]] §3.1.
- `link_report` is an auto-generated link index, and `equipment` is a device reference note.

`own_words: true` marks a protected note. Only Leon sets it, by hand or from his HEAD template. An agent never sets, changes or removes it, and never edits the body of a note that carries it, nor of any existing note in `01_journals/` or `20_Thinking/` ([[AGENTS]] §6.1). Frontmatter migrations may still touch the other fields.

Cross-type rules enforced by `validate_note_shape.py` on atomic notes in `100_zettelkasten`:

- `title` must equal the filename without `.md`.
- `confidence` belongs to `evidence` notes only.
- These legacy keys must not be written: `uid`, `purpose`, `epistemic`, `updated`, `creation_date`, `last_reviewed`.
- No `prodos` key (§4).

---

## 3. The 5 Canonical Note Types (Knowledge Nodes)

Each knowledge-node type has its own schema and fileClass. The body, title, links and checks for an atomic note in `100_zettelkasten` are specified in [[SoT - Atomic Note Standard (The Proposition Card)]]. Where the two notes disagree about such a note, that standard wins.

### 3.1 ClaimNote

- `type`: `claim`
- `title`: A single declarative sentence, the claim itself.
- `proposition`: The claim in one clear sentence. Not a topic.
- `epistemic_status`: `high` (confident, evidenced), `medium` (plausible), `low` (speculative) or `unknown`.
- `evidence_links`: List of wikilinks to Evidence notes that support the claim.
- `contradicts`: List of wikilinks to Claim notes it contradicts, empty if none.

### 3.2 ConceptNote

- `type`: `concept`
- `title`: The term or distinction being defined.
- `definition`: A single-paragraph definition in your own words.
- `distinguishes_from`: List of related terms this concept is not, with wikilinks.
- `used_in_claims`: List of wikilinks to Claim notes that use this concept.

### 3.3 EvidenceNote

- `type`: `evidence`
- `title`: Descriptive title of the evidence.
- `source_quote`: The exact quote, data point or benchmark. Direct extraction only.
- `source_reference`: Author, book or URL, date. Link the `Source - ` note where one exists.
- `supports_claims`: List of wikilinks to Claim notes this evidence supports.
- `confidence`: Float 0.0 to 1.0 for strength of support.

### 3.4 QuestionNote

- `type`: `question`
- `title`: The question itself. Must end with `?`.
- `tension`: The belief or observation that generates the question.
- `candidate_answers`: List of possible answers, may be empty.
- `related_claims`: List of related Claim notes.

### 3.5 ProcedureNote

- `type`: `procedure`
- `title`: `How to [do X]`.
- `trigger`: When the procedure is invoked.
- `steps`: Ordered, physical, verb-first steps.
- `verification`: How you know it worked.

---

## 4. The `prodos` Object (Optional Routing Layer)

The nested `prodos` object is an optional routing and lifecycle layer. It is separate from `type` and `status`, and it does not replace them.

> Amended 2026-09-26: the `prodos` object is not part of an atomic note (`100_zettelkasten`). The Obsidian Linter deletes the key on save, most notes never carried it, and `type` plus `status` carry the same information. It must not be written on new atomic notes. It stays valid, optional metadata on SoTs, MoCs, protocols, HEAD notes, prompts and projects. See [[SoT - Atomic Note Standard (The Proposition Card)]] §3.

### 4.1 Universal Subkeys

| Key | Required | Type | Allowed values and notes |
|:----|:---------|:-----|:-------------------------|
| `prodos.kind` | No | string | `head`, `sot`, `protocol`, `moc`, `atomic`, `project`, `ops`, `prompt`, `journal`. Not for atomic notes. |
| `prodos.lifecycle` | No | string | `seedling`, `active`, `stable`, `evergreen`, `archived`. A separate vocabulary from top-level `status`. Never copy values between them. |
| `prodos.trust` | No | string | `low`, `working`, `stable`, `authoritative`. |
| `prodos.review` | No | mapping | Review cadence (`interval`, `last_reviewed`). |
| `prodos.id` | No | string | Stable id for the note. |

`type` and `prodos.kind` are different fields and are not always the same string. A `map` note has `prodos.kind: moc`. Read both before assuming a note's category.

---

## 5. Enforcement Surfaces

1. `10_System/scripts/validate_note_frontmatter.py` checks the §2 envelope and the §3 field presence for the five types.
2. `10_System/scripts/validate_note_shape.py` checks atomic-note frontmatter, body and links.
3. `10_System/fileClasses/` holds the `Note` fileClass (the §2 envelope and §4 object) and the five type fileClasses that extend it. Obsidian enforces its Select options live.
4. The `## TAC FRONTMATTER COMPLIANCE (MANDATORY)` block in each prompt makes agents self-check before a write ([[00 - Prompt Library Router]], Maintenance Rule 5).

There is no JSON Schema, no `pydantic` model and no `dry_run` gate. Earlier versions of this section said otherwise, and no such code exists in `10_System/`.

---

## 6. Legacy Frontmatter Mapping (Migration Table)

> Formalised 2026-07-17 as the mapping the 2026-07-11 migration used. [[Goal - Frontmatter Bulk Migration (Phase 3)]] is a historical record of that run. Revised 2026-10-26 for the atomic-note exception.

Use this table to normalise a legacy note. For a note in `100_zettelkasten/`, set only the top-level `type` and `status` and write no `prodos` key (§4). For other notes, the routing kind goes in `prodos.kind`. Folder context disambiguates ties (§7).

| Legacy `type` (context) | Target |
|:---|:---|
| `concept`, `atom`, `permanent`, `note`, `''`, `null`, `'null'` in `100_zettelkasten/` | Top-level `type: concept`, or `claim` if the note states a proposition. No `prodos` key. |
| `SoT` / `sot` | `type: sot`. If the filename starts `Protocol - `, use `type: protocol`. Optional `prodos.kind: sot` or `protocol`. |
| `daily` | `type: journal`. Optional `prodos.kind: journal`. |
| `map` | `type: map`. Optional `prodos.kind: moc`. |
| `command`, `atomic_command`, `playbook` | `prodos.kind: ops`. Keep the `cmd` or `playbook` distinction in `tags`. The top-level `type` needs a human decision, so log it. |
| anything else | Do not guess. Log it to an exceptions report for a human. |

Legacy key renames, applied after the type mapping:

| Legacy key | Target |
|:---|:---|
| `status` with `seedling`, `active`, `stable`, `evergreen` or `archived` | Non-atomic notes: `prodos.lifecycle`. Atomic notes: map to the §2 `status` (`seedling` becomes `seed`) and write no `prodos`. Anything else goes to the exceptions report. |
| `trust-level` | `prodos.trust` (non-atomic only) |
| `last_reviewed`, `review_interval` | `prodos.review.*` (non-atomic only). Forbidden on atomic notes. |
| `last_synthesis`, `synthesis-count` | `prodos.chronos.*` (non-atomic only) |
| `id`, `ID`, `uid` | `prodos.id` (non-atomic only). Forbidden on atomic notes. |
| `updated`, `creation_date` | Delete, after copying the value into `created` or `modified` if missing. |
| `superseded-by` | `superseded_by` |

Hard rules: if a note already has a `prodos` object, merge and never overwrite its values with legacy-derived ones. Never delete a legacy value that could not be mapped.

---

## 7. Folder-to-`prodos.kind` Normativity

> Formalised 2026-07-17. A strong default, not a law. A note's content can override its folder when the two genuinely disagree.

For a note that carries a `prodos` object, the folder sets the expected `prodos.kind`:

| Folder | Expected `prodos.kind` |
|:---|:---|
| `30_Library/SoT/` | `sot`, or `protocol` if the filename starts `Protocol - ` |
| `30_Library/MoC/` | `moc` |
| `30_Library/100_zettelkasten/` | none. Atomic notes carry no `prodos` (§4). |
| `30_Library/200_Projects/` | `project` |
| `30_Library/ops/` | `ops` |
| `01_journals/` | `journal` |
| `10_System/prompts/` | `prompt` |
| `20_Thinking/` | `head` |

When folder and content disagree, trust the content and flag the mismatch in `non_conformance_reason`.

---

## 8. Scope & Priority

> Formalised 2026-07-17. Revised 2026-10-26 after the 2026-07-30 Hermes split.

The validators scan `30_Library/`, `20_Thinking/`, `10_System/`, `01_journals/` and `00_Inbox/`. Everything else is outside the contract: `.obsidian/`, `.trash/`, `99_Archive/`, `90_Audits/`, `wiki/`, the root files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) and the whole Hermes vault. `raw/`, `output/`, `index.md` and `log.md` no longer exist in this vault.

When many notes need bringing into conformance at once, go highest-traffic first: `30_Library/MoC/`, `SoT/` and `ops/`, then `100_zettelkasten/`, then `200_Projects/`, `20_Thinking/`, `10_System/` and `01_journals/`. Protected notes (§2) are excluded from body edits whatever the priority.

---

## 9. Validation

> Formalised 2026-07-17. Revised 2026-10-26.

```bash
uv run --with pyyaml python3 10_System/scripts/validate_note_frontmatter.py --audit
uv run --with pyyaml python3 10_System/scripts/validate_note_shape.py
```

`validate_note_frontmatter.py` checks the §2 required fields, `tags` and `conformant` typing, the conditional `non_conformance_reason`, the `type`, `status`, `prodos.kind` and `prodos.lifecycle` enums, `supersedes` and `superseded_by` as lists, and `superseded_by` when `status: superseded`. It checks the §3 schema fields (and the `epistemic_status` enum and claim list typing) only when `conformant: true`, so a note can declare that it is not yet complete. `validate_note_shape.py` checks atomic notes created on or after 2026-09-26. Older notes are frozen, which is the vault's only grandfathering rule. There is no allowlist: an earlier `allowlist_decision` key described one that was never built, and it was removed on 2026-10-26.

Known defects:

- The 2026-10-26 `--audit` run reported 1,192 files with errors (2,578 errors in total), mostly legacy notes with no `type` or `conformant`.
- No regression-case mode exists, unlike `edge_lint.py --regress`.
- Nothing runs the validators on commit or on a schedule.
- Eight prompts still carry the old ten-value `type` list in their TAC block. They are listed in the 2026-10-26 review.

## Change Log

- 2026-10-26: review against the live scripts. Removed the false `supersedes` link to the TAC SoT, the unbuilt allowlist and the `pydantic` and `dry_run` claims. Documented `own_words` and the 15-value `type` enum. Rewrote §6 and §7 so atomic notes carry no `prodos`. Updated §8 for the Hermes split. Added `source`, `prompt` and `tombstone` to `validate_note_shape.py` so it matches the enum.
- 2026-10-16: `prompt` added to the `type` enum.
- 2026-09-26: `source` added to the enum. `prodos` dropped for atomic notes.
- 2026-09-22: `seed` added to `status`. `superseded` formalised with `supersedes` and `superseded_by`. `link_report` and `equipment` added to `type`. The `status` values `tmp` (24 notes, migrated to `seed`) and `owned` (7, migrated to `stable`) were retired as invalid. Five hyphenated `superseded-by` keys were renamed. `conformant` flags were synced to the validator (163 flipped to `false`, 305 to `true`). The `--audit` schema check runs only when `conformant: true`, and an early sync that ignored this wrongly promoted 405 incomplete claims before being reverted.
- 2026-09-14: `validate_note_frontmatter.py` created.
- 2026-07-17: §6–§9 formalised.

## Open Tensions

- A number of notes carry `supersedes` or `superseded_by` without a matching `status: superseded`, or the reverse. No pass has reconciled them. `--audit` surfaces them.
- Notes that were already `conformant: false` keep the `non_conformance_reason` text they had, which may not match current validator wording.
- Two schemas are still live: flat legacy frontmatter and the optional `prodos` object. §6 handles the migration, but do not assume one schema is universal.
