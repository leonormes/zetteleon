---
title: 'PKM LLM Integration — Pipeline Audit: Why the IoED Zettels Came Out Malformed'
output_type: report
created: 2026-07-25 12:00:00+00:00
tags:
- output
- pkm-config
- agents-md
- frontmatter-contract
permalink: llmeon/output/2026-07-25-report-pkm-llm-integration-pipeline-audit
---

## Summary

The 10 atomic notes created from `SoT - Illusion of Explanatory Depth (IoED)` today are all structurally broken in the same way: they carry the `raw/proposed-claims/` **Claim Stub** schema (`AGENTS.md` §2.4) verbatim into `30_Library/100_zettelkasten/`, instead of the **ClaimNote** schema (`SoT - ProdOS Frontmatter Contract (Note Type Schemas)` §3.1) that permanent claim notes are supposed to satisfy. Nothing in the current config performs that conversion, so nothing did.

Confirmed defects, present on all 10 notes:

- `permalink` still reads `llmeon/raw/proposed-claims/...` — stale, points at a path the file no longer occupies.
- No `conformant` / `non_conformance_reason` — the one pair the Frontmatter Contract calls non-negotiable ("required top-level flags... do NOT write an incomplete or guessed frontmatter block").
- No `proposition`, `epistemic_status`, `evidence_links`, `contradicts` — the actual §3.1 ClaimNote fields.
- Orphaned stub-only fields survive: `claim_statement`, `steel_man`, `falsifiers`/`crux`/`confidence`/`counter_positions` (all `null`), `status: proposed`, `tags: [claim-stub, agent-proposed]`.
- Body prose in several notes is a near-verbatim table-quote dump with mid-sentence ellipses, violating both the source SoT's own stated Zettelkasten principle ("you MUST write notes in your own words") and the Conjunction Test in `10_System/prompts/Atomic Signal Extractor → Write TMP file.md`.

## Root Cause

Two schemas exist for the same conceptual object (a claim), designed for two different lifecycle stages, and nothing bridges them:

| | Claim Stub (§2.4) | ClaimNote (§3.1) |
|---|---|---|
| Location | `raw/proposed-claims/` | `30_Library/100_zettelkasten/` |
| Purpose | Minimal proposal, awaiting human completion | Permanent, query-able knowledge node |
| Key fields | `claim_statement`, `steel_man`, blank `falsifiers`/`crux`/`confidence`/`counter_positions` | `proposition`, `epistemic_status`, `evidence_links`, `contradicts`, `conformant`, `non_conformance_reason` |

`AGENTS.md` §2.4 says only "Promotion to `30_Library/` is a human action" — it never specifies *what changes* on promotion. The prompt library already has a correctly-built solution to this exact problem — `10_System/prompts/Atomic Linker → Promote & Connect.md` — which has an explicit Kind→type mapping table and mandates `conformant`/`non_conformance_reason` on every promoted note. But it targets `00_Inbox/` as its write destination, which the current `AGENTS.md` hard-constraints forbid agents from writing to. So the one component built to do this correctly is currently unusable under present governance rules.

Separately: no automated frontmatter validator exists. The Frontmatter Contract SoT names one (`gemini-scribe/scripts/validate_note_frontmatter.py`) but documents it as not yet written (§9). `edge_lint.py` only checks typed edges, not frontmatter shape — so malformed notes like these 10 pass the one automated gate that does exist.

## Proposed Fix 1 — Amend AGENTS.md §2.4

Add a promotion-mapping subsection so "promotion" has a defined output shape. Suggested insertion, immediately after the existing §2.4 body (before the `---` separator):

> **Promotion mapping (stub → ClaimNote).** When a human promotes a stub from `raw/proposed-claims/` into `30_Library/100_zettelkasten/`, the resulting note MUST satisfy [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] §2 and §3.1, not retain the stub schema. Concretely:
>
> | Stub field | Becomes |
> |---|---|
> | `claim_statement` | `proposition` (rewritten as one clean sentence if needed) |
> | `steel_man` | Moved to body, under `## Steelman` |
> | `falsifiers` / `crux` / `counter_positions` | Moved to body, under `## Open Questions` (kept blank if still unanswered — do not carry forward as frontmatter `null`) |
> | `confidence` | Mapped to `epistemic_status` (`high`/`medium`/`low`/`unknown`) if set, else `unknown` |
> | `type: claim-stub`, `status: proposed`, `tags: [claim-stub, agent-proposed]` | Dropped |
> | — | `conformant` and `non_conformance_reason` added (set `conformant: false` with a reason if `evidence_links` can't point to a real Evidence note yet) |
> | — | `permalink` regenerated to match the new path |
>
> Agents may draft this mapping for review; applying it to a note already living in `30_Library/` is still promotion — a human action.

## Proposed Fix 2 — Atomic Linker → Promote & Connect target folder

`10_System/prompts/Atomic Linker → Promote & Connect.md` currently writes permanent notes to `00_Inbox/` (§ "File Naming Convention" and the Output Behaviour section). Under current `AGENTS.md` hard constraints this folder is agent-read-only. Two options, your call:

- **(a)** Change the prompt's write target from `00_Inbox/` to `raw/proposed-claims/`, and have it emit stub-shaped output (its rich template minus the fields §2.4 doesn't have) so it becomes the actual implementation of the §2.4 pipeline rather than a parallel, currently-inert one.
- **(b)** Leave the prompt targeting `00_Inbox/` but explicitly carve out a §9.3-style exception for it in `AGENTS.md`, since `00_Inbox/` is meant as a human triage point, not a claim-layer write.

(a) is the smaller change and keeps one pipeline instead of two.

## Not fixed here

Building the missing frontmatter validator (`gemini-scribe/scripts/validate_note_frontmatter.py`) is out of scope for this report — flagging it as the second-order fix worth doing once the schema mapping above is settled, so future promotions get caught automatically rather than by manual review.