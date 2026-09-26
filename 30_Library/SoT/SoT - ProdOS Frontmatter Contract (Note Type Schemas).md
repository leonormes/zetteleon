---
aliases: [Frontmatter Contract, FrontmatterContract, Note Type Schemas, TAC Frontmatter Schema]
allowlist_decision: "Option C — Documented allowlist. Legacy set frozen. New files must pass 0 errors. allowlist maintained in this file's frontmatter at `non_conformant_allowlist`."
created: 2026-07-17T00:00:00+00:00
modified: 2026-09-26T08:46:20+00:00
permalink: llmeon/30-library/so-t/so-t-prodos-frontmatter-contract-note-type-schemas
see_also: ["[[Goal - Frontmatter Bulk Migration (Phase 3)]]", "[[Protocol - Typed Answer Contract (TAC) for Vault Agents]]", "[[SoT - PRODOS Core Specification]]", "[[SoT - Typed Answer Contract (TAC) for LLM Output]]"]
supersedes: ["[[SoT - Typed Answer Contract (TAC) for LLM Output]]"]
tags: [domain/pkm, prodos/sot, topic/frontmatter, topic/knowledge-architecture]
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
| `type` | Yes | string | `claim`, `concept`, `evidence`, `question`, `procedure`, `protocol`, `map`, `journal`, `project`, `sot`, `link_report`, `equipment`. |
| `project_name` | No | string | Parent project context if applicable. |
| `project_category` | No | string | e.g. `prodos`, `devops`, `personal`. |
| `status` | No | string | `draft`, `seed`, `stable`, `evergreen`, `stale`, `superseded`. |
| `tags` | Yes | list | Prefer hierarchical tags. |
| `conformant` | Yes | boolean | `false` if the note cannot be cleanly typed. Do NOT write as true unless completely valid. |
| `non_conformance_reason` | Conditional | string | Required if `conformant: false`. |
| `supersedes` | No | list of wikilinks | Older note(s) this one replaces. Set on the new/surviving note. |
| `superseded_by` | Conditional | list of wikilinks | The note(s) that replaced this one. Required if `status: superseded`. |

---

## 3. The 5 Canonical Note Types (Knowledge Nodes)

Each of your five canonical note types has its own TAC schema. Any agent creating or editing a note must adhere to these schemas. The body of the note, its title, its links and how all of it is checked are specified in [[SoT - Atomic Note Standard (The Proposition Card)]]; where the two disagree about an atomic note in `100_zettelkasten`, that note wins.

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

> Amended 2026-09-26: the `prodos` object is no longer part of an atomic note (`100_zettelkasten`). The Obsidian Linter deletes the key on save, most notes never carried it, and `type` plus `status` carry the same information. The two keys in the table below are therefore not required for atomic notes and must not be written on new ones. They remain valid, optional routing metadata on SoTs, MoCs, protocols, HEAD notes and projects. See [[SoT - Atomic Note Standard (The Proposition Card)]] §3.

### 4.1 Universal Subkeys

| Key | Required | Type | Allowed values / notes |
|:----|:---------|:-----|:----------------------|
| `prodos.kind` | No (was Yes; not for atomic notes) | string | `head`, `sot`, `protocol`, `moc`, `atomic`, `project`, `ops`, `prompt`, `journal` |
| `prodos.lifecycle` | No (was Yes; not for atomic notes) | string | `seedling`, `active`, `stable`, `evergreen`, `archived` |
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

The canonical validator is `10_System/scripts/validate_note_frontmatter.py`, run over the vault after any bulk migration to confirm every in-scope note satisfies §2 (FrontmatterContract) and, where applicable, §3 (the 5 canonical note-type schemas):

```bash
uv run --with pyyaml python3 10_System/scripts/validate_note_frontmatter.py --audit
```

Status (updated 2026-09-14): the script exists and is runnable—checks §2's required fields, `tags`/`conformant` typing, the conditional `non_conformance_reason`, the `type` enum, `prodos.kind`/`prodos.lifecycle` enum membership, and §3's type-specific schema fields when `conformant: true`. It landed at `10_System/scripts/validate_note_frontmatter.py`, not the `gemini-scribe/scripts/` path this section originally named—that path was aspirational and never existed; update any other note or prompt still citing `gemini-scribe/scripts/validate_note_frontmatter.py`. Not yet extended with a regression-case mode the way `edge_lint.py --regress` was (see `10_System/evals/README.md`)—a reasonable next step, not done here.

## Tensions & Gaps

- ~~Validator doesn't exist yet.~~ Resolved 2026-09-14—`10_System/scripts/validate_note_frontmatter.py` exists and is runnable; see §9. Conformance can now be machine-checked (`--audit`), though nothing currently runs it automatically on a commit or schedule.
- Two parallel schemas in flight. Notes may carry either the flatter legacy schema (`type`, `conformant`, `non_conformance_reason` at top level) or the modern `prodos:` nested object—§6 exists precisely because both are live simultaneously during the migration. Don't assume one schema is universal until migration is complete.
- `type` enum collision with routing `prodos.kind`. §6's `map` → `prodos.kind: moc` mapping is a reminder that the top-level `type` field and `prodos.kind` are not always the same string—read both before assuming a note's category.
- ~~`status` enum missing `seed`.~~ Resolved 2026-09-22—§2 listed only `draft`/`stable`/`evergreen`/`stale`, but the `Note` fileClass (`10_System/fileClasses/Note.md`) and `validate_note_frontmatter.py` both always included `seed`, and it's by far the most-used value in the vault (399 notes, vs. 43 `draft`). §2 now lists all five; the doc was stale, not the implementation.
- ~~`tmp`/`owned`/`superseded` statuses undocumented.~~ Resolved 2026-09-22. `tmp` (24 notes) and `owned` (7) weren't real lifecycle states—`tmp` was auto-generated `type: link_report` index reports (migrated to `seed`) and `owned` was device/equipment reference notes conflating physical possession with content maturity (migrated to `stable`, since the notes are complete). `superseded`, by contrast, was a real and already-used deprecation signal (`10_System/prompts/Knowledge Consolidation Agent.md` already taught agents to write `status: superseded`)—it's now a formal enum value here and in both implementations, backed by new `supersedes`/`superseded_by` fields on the `Note` fileClass (§2). Also fixed in passing: ~50 notes carry blank `supersedes`/`superseded_by` scaffold fields from the note template, but five populated instances used a hyphenated `superseded-by` instead—renamed to match the underscore convention every other multi-word field in this contract uses, and fixed the prompt that was teaching the hyphenated form.
- Not yet done: a number of notes with a populated `supersedes`/`superseded_by` don't have `status: superseded` set to match (or vice versa)—the two fields were formalised together here, but no pass has reconciled existing data against the new conditional rule (`validate_note_frontmatter.py --audit` will now surface these).
- ~~`type: link_report` / `type: equipment` outside the enum.~~ Resolved 2026-09-22—both were real, structurally consistent note species (24 auto-generated link-index reports, 7 owned-equipment reference notes) that simply predated this table. Added to §2's `type` enum in the `Note` fileClass and `validate_note_frontmatter.py`, same tier as `protocol`/`map`/`journal`/`project`—a valid routing `type` with no dedicated §3 schema, not a sixth canonical knowledge-node type.
- `conformant`/`non_conformance_reason` synced against `validate_note_frontmatter.py --audit` 2026-09-22 across the full scoped vault: 163 notes flipped `true`→`false` (were claiming conformance the validator couldn't confirm), 305 flipped `false`→`true` (were fully valid but marked otherwise). Scope note: this pass only touched notes where the _boolean_ was wrong—the ~1,177 notes that were already (correctly) `conformant: false` keep whatever `non_conformance_reason` text they had; their reasons were not rewritten to match current validator phrasing. A caught-and-fixed subtlety: the validator's §3 schema-completeness check only runs when `conformant: true` (by design, so a note can self-declare "not trying to be complete" without being penalised for it)—an initial naive sync mistakenly promoted 405 incomplete `claim` notes to `true` on the strength of that gate suppressing their real errors; caught by re-validating post-write and reverted before this could ship.
