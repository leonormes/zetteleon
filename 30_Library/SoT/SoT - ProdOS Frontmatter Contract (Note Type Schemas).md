---
aliases: [Frontmatter Contract, FrontmatterContract, Note Type Schemas, TAC Frontmatter Schema]
created: 2026-07-17T00:00:00+00:00
modified: 2026-07-20T16:33:41+00:00
permalink: llmeon/30-library/so-t/so-t-prodos-frontmatter-contract-note-type-schemas
see_also: ["[[Goal - Frontmatter Bulk Migration (Phase 3)]]", "[[Protocol - Typed Answer Contract (TAC) for Vault Agents]]", "[[SoT - PRODOS Core Specification]]", "[[SoT - Typed Answer Contract (TAC) for LLM Output]]"]
supersedes: ["[[Typed-Answer-Contract-RAG]]"]
tags: [domain/pkm, prodos/sot, topic/frontmatter]
title: SoT - ProdOS Frontmatter Contract (Note Type Schemas)
---

> Canonical status: this note is the authoritative frontmatter schema spec for the vault, superseding the same content previously living inside the `20_Thinking/21_Workbench/Typed-Answer-Contract-RAG.md` scratch note (now retired to `.trash/`). `AGENTS.md`, `sys_merger`, and every prompt with a `## TAC FRONTMATTER COMPLIANCE (MANDATORY)` block link here. Section numbers (§1–§9) are preserved unchanged from the workbench version so existing citations by number remain correct.

## Minimum Viable Understanding (MVU)

Every note's frontmatter is a typed data contract, not free-form YAML. An agent editing or creating a note must fill in the required `FrontmatterContract` fields (§2)—and, for the five canonical knowledge-node types, the type-specific schema (§3)—or explicitly set `conformant: false` with a `non_conformance_reason` rather than writing an incomplete or guessed frontmatter block. This is the frontmatter-specific instance of the vault's broader Typed Answer Contract principle (see [[SoT - Typed Answer Contract (TAC) for LLM Output]] for the output/prose-side instance, and [[Protocol - Typed Answer Contract (TAC) for Vault Agents]] for the enforcement callout used across prompts).

## 1. Typed Answer Contracts (TAC) Overview

Your vault has transitioned to a strictly enforced schema model governed by Typed Answer Contracts (TAC). Every LLM operation on a note is a typed data extraction/writing contract.

If an LLM or agent cannot fill the schema cleanly, it MUST flag `conformant: false` and note the `non_conformance_reason`.

- `type` is now a STRICTly required top-level field (superseding previous deprecation).
- `title`, `created`, `modified`, and `tags` remain required.
- `conformant` (boolean) and `non_conformance_reason` (string) are required top-level flags.

---

## 2. The Frontmatter Contract (All Notes)

Any agent touching frontmatter MUST return a `FrontmatterContract` object. This is the shared envelope all note types inherit:

| Field | Required | Type | Rule |
|:------|:---------|:-----|:-----|
| `title` | Yes | string | Matches filename. |
| `type` | Yes | string | `claim`, `concept`, `evidence`, `question`, `procedure`, `protocol`, `map`, `journal`, `project`, `sot`. |
| `project_name` | No | string | Parent project context if applicable. |
| `project_category` | No | string | e.g. `prodos`, `devops`, `personal`. |
| `status` | No | string | `draft`, `stable`, `evergreen`, `stale`. |
| `tags` | Yes | list | Prefer hierarchical tags. |
| `conformant` | Yes | boolean | `false` if the note cannot be cleanly typed. Do NOT write as true unless completely valid. |
| `non_conformance_reason` | Conditional | string | Required if `conformant: false`. |

---

## 3. The 5 Canonical Note Types (Knowledge Nodes)

Each of your five canonical note types has its own TAC schema. Any agent creating or editing a note must adhere to these schemas.

### 3.1 ClaimNote

- `type`: `claim`
- `title`: A single declarative sentence—the claim itself.
- `proposition`: The claim in one clear sentence, beginning with a verb or noun phrase. NOT a topic.
- `epistemic_status`: `high` (confident/evidence), `medium` (plausible), `low` (speculative), `unknown`.
- `evidence_links`: List of Wikilinks to Evidence notes that support this claim.
- `contradicts`: List of Wikilinks to Claim notes this contradicts, if any.

### 3.2 ConceptNote

- `type`: `concept`
- `title`: The term or distinction being defined.
- `definition`: A single-paragraph definition in your own words.
- `distinguishes_from`: List of related terms this concept is NOT, with wikilinks.
- `used_in_claims`: List of Wikilinks to Claim notes that use this concept.

### 3.3 EvidenceNote

- `type`: `evidence`
- `title`: Descriptive title of the evidence.
- `source_quote`: The exact quote, data point, or benchmark. Direct extraction only.
- `source_reference`: Author, book/URL, date.
- `supports_claims`: List of Wikilinks to Claim notes this evidence supports.
- `confidence`: Float 0.0 to 1.0 indicating strength of support.

### 3.4 QuestionNote

- `type`: `question`
- `title`: The question itself—must end with '?'.
- `tension`: What belief or observation generates this question?
- `candidate_answers`: List of possible answers; can be empty.
- `related_claims`: List of related Claim notes.

### 3.5 ProcedureNote

- `type`: `procedure`
- `title`: 'How to [do X]' format.
- `trigger`: When is this procedure invoked?
- `steps`: Ordered, physical, verb-first steps.
- `verification`: How do you know it worked?

---

## 4. The `prodos` Object (Legacy Extension & Routing)

The nested `prodos` YAML object handles systemic routing and lifecycle events not covered directly by the base TAC.

_(Note: As the TAC architecture rolls out, elements of `prodos` may be fully migrated into top-level typed fields.)_

### 4.1 Universal Subkeys

| Key | Required | Type | Allowed values / notes |
|:----|:---------|:-----|:----------------------|
| `prodos.kind` | Yes | string | `head`, `sot`, `protocol`, `moc`, `atomic`, `project`, `ops`, `prompt`, `journal` |
| `prodos.lifecycle` | Yes | string | `seedling`, `active`, `stable`, `evergreen`, `archived` |
| `prodos.trust` | No | string | `low`, `working`, `stable`, `authoritative`—epistemic confidence |
| `prodos.review` | No | mapping | Optional cadence (`interval`, `last_reviewed`) |
| `prodos.id` | No | string | Canonical stable id for the note. |

---

## 5. Machine-readable Schema

1. JSON Schema (many tools / IDEs): `gemini-scribe/schemas/prodos-note-frontmatter.schema.json`.
2. TAC Models are validated in Python via `pydantic`.
3. Vault Action contracts ensure `dry_run` is True unless explicitly bypassed by human execution.

---

## 6. Legacy Frontmatter Mapping (Migration Table)

> Formalised 2026-07-17. [[Goal - Frontmatter Bulk Migration (Phase 3)]] cited this section by number before it existed in this document—the table below is that migration's own mapping rules, promoted here so the spec and the prompt that depends on it actually agree. No new policy invented; this is what the 2026-07-11 migration run already used.

Legacy `type` values map to `prodos.kind` as follows (folder context disambiguates ties—see §7):

| Legacy `type` (context) | Target |
|:---|:---|
| `concept`, `atom`, `permanent`, `note`, `''`, `null`, `'null'` (in `100_zettelkasten/`) | `prodos.kind: atomic`; set `prodos.atomic.form: concept` unless tags indicate `hypothesis`/`claim`/`definition` |
| `SoT` / `sot` | `prodos.kind: sot`; if filename starts `Protocol - `, use `prodos.kind: protocol` instead and top-level `type: protocol` |
| `daily` | `prodos.kind: journal` |
| `map` | `prodos.kind: moc` (top-level `type` stays `map`—`moc` is the routing kind, not the FrontmatterContract type) |
| `command`, `atomic_command`, `playbook` | `prodos.kind: ops`; keep disambiguation (`cmd` vs `playbook`) in `tags` |
| anything else | Do NOT guess—log to an exceptions report for human decision |

Legacy key renames (apply after the type mapping above):

| Legacy key | Target |
|:---|:---|
| `status` (exact enum match only: `seedling`/`active`/`stable`/`evergreen`/`archived`; `draft` → `seedling`; anything else → exceptions report) | `prodos.lifecycle` |
| `trust-level` | `prodos.trust` |
| `last_reviewed`, `review_interval` | `prodos.review.*` |
| `last_synthesis`, `synthesis-count` | `prodos.chronos.*` |
| `id`, `ID`, `uid` | `prodos.id` |
| `updated`, `creation_date` | Delete—but only after preserving their value into `created`/`modified` if those are missing. |

Hard rules: if a note already has a `prodos` object, merge—never overwrite existing `prodos` values with legacy-derived ones. Never delete a legacy value that could not be mapped; exceptions keep their legacy keys untouched.

---

## 7. Folder-to-`prodos.kind` Normativity

> Formalised 2026-07-17, referenced as "§3.2" by [[Goal - Frontmatter Bulk Migration (Phase 3)]] before this section existed. The table is inferred from actual vault folder structure and the §6 mapping above—treat it as a strong default, not an unquestionable law; a note's content can override its folder's default `prodos.kind` when the two genuinely disagree.

The folder a note lives in is normative for its expected `prodos.kind`, absent a stronger signal from the note's own `type`/content:

| Folder | Expected `prodos.kind` |
|:---|:---|
| `30_Library/SoT/` | `sot` (or `protocol` if filename starts `Protocol - `) |
| `30_Library/MoC/` | `moc` |
| `30_Library/100_zettelkasten/` | `atomic` |
| `30_Library/200_Projects/` | `project` |
| `30_Library/ops/` | `ops` |
| `01_journals/` | `journal` |
| `10_System/prompts/` | `prompt` |
| `20_Thinking/` | `head` |

When a note's folder and its content-inferred `prodos.kind` disagree, trust the content and flag the mismatch in `non_conformance_reason` rather than silently picking one.

---

## 8. Migration Scope & Priority

> Formalised 2026-07-17, referenced as "§8 priority" by [[Goal - Frontmatter Bulk Migration (Phase 3)]] before this section existed.

TAC governs frontmatter in: `30_Library/`, `20_Thinking/`, `10_System/`, `01_journals/`, `00_Inbox/`. It never governs: `raw/` (sealed), `wiki/` (own dossier schema), `output/`, `.trash/`, `.obsidian/`, `AGENTS.md`, `index.md`, `log.md`.

When multiple notes need bringing into conformance at once, prioritise in this order (highest-traffic, most-linked-against first): `30_Library/MoC/` and `30_Library/SoT/` and `30_Library/ops/` → `30_Library/100_zettelkasten/` → `30_Library/200_Projects/`, `20_Thinking/`, `10_System/`, `01_journals/`. A specific bulk-migration run may checkpoint this into dated batches with git commits—see [[Goal - Frontmatter Bulk Migration (Phase 3)]] for that operational detail; this section states the priority principle only.

---

## 9. Validation

> Formalised 2026-07-17, referenced as "§9" by [[Goal - Frontmatter Bulk Migration (Phase 3)]] before this section existed.

The canonical validator is `gemini-scribe/scripts/validate_note_frontmatter.py`, run over the vault after any bulk migration to confirm every in-scope note satisfies §2 (FrontmatterContract) and, where applicable, §3 (the 5 canonical note-type schemas).

Status: this script does not currently exist in the repository (checked 2026-07-17—no `gemini-scribe/` directory found in the vault). Any prompt or process that assumes it can run this validation will fail until the script is written. Until then, conformance checking is manual: spot-check `conformant`/`non_conformance_reason` presence and `type` enum membership per §2.

## Tensions & Gaps

- Validator doesn't exist yet. §9 documents an aspirational tool path (`gemini-scribe/scripts/validate_note_frontmatter.py`) that has not been written. Conformance is currently self-reported and spot-checked, not machine-enforced.
- Two parallel schemas in flight. Notes may carry either the flatter legacy schema (`type`, `conformant`, `non_conformance_reason` at top level) or the modern `prodos:` nested object—§6 exists precisely because both are live simultaneously during the migration. Don't assume one schema is universal until migration is complete.
- `type` enum collision with routing `prodos.kind`. §6's `map` → `prodos.kind: moc` mapping is a reminder that the top-level `type` field and `prodos.kind` are not always the same string—read both before assuming a note's category.
