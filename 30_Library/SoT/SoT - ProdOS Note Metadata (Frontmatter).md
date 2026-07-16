---
aliases: [Note metadata schema, ProdOS frontmatter specification, TAC Schema]
created: 2026-04-08T18:00:00+00:00
modified: 2026-07-16T15:10:00+00:00
permalink: llmeon/30-library/so-t/so-t-prod-os-note-metadata-frontmatter
see_also: ["[[CLAUDE.md]]", "[[ProdOS-TAC-Plan]]"]
tags: [prodos/schema, topic/pkm]
title: SoT - ProdOS Note Metadata (Frontmatter) & TAC Schemas
type: sot
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## 1. Typed Answer Contracts (TAC) Overview

Your vault has transitioned to a strictly enforced schema model governed by Typed Answer Contracts (TAC). Every LLM operation on a note is a typed data extraction/writing contract. 
If an LLM or agent cannot fill the schema cleanly, it MUST flag `conformant: false` and note the `non_conformance_reason`.

- **`type` is now a STRICTly required top-level field** (superseding previous deprecation).
- `title`, `created`, `modified`, and `tags` remain required.
- `conformant` (boolean) and `non_conformance_reason` (string) are required top-level flags.

---

## 2. The Frontmatter Contract (All Notes)

Any agent touching frontmatter MUST return a `FrontmatterContract` object. This is the shared envelope all note types inherit:

| Field | Required | Type | Rule |
|:------|:---------|:-----|:-----|
| `title` | Yes | string | Matches filename. |
| `type` | Yes | string | `claim`, `concept`, `evidence`, `question`, `procedure`, `map`, `journal`, `project`, `sot`. |
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
- `title`: A single declarative sentence — the claim itself.
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
- `title`: The question itself — must end with '?'.
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
*(Note: As the TAC architecture rolls out, elements of `prodos` may be fully migrated into top-level typed fields.)*

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
