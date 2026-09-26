---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-time-boxing-research
title: 2026-09-24-time-boxing-research
type: note
---

## Value check and ProdOS linking — [[Time-Boxing Research Prevents Productive Procrastination]] — 2026-09-24

> Method note: 1MCP was still down, so checks were lexical (`rg`) plus file reads.

### Verdict: keep, as the atomic core of a fuller protocol

- **Useful:** it is the cited "canonical reference" and "operational antidote" for the research rabbit hole in [[MOC - Breaking the ADHD Overthinking-Procrastination Cycle]] (three mentions), and it targets a failure you have written about in your own notes ([[I have a lot of shame about my life]] links to it). Its example is an engineering one (a Terraform `for_each` lookup), which fits your day job.
- **Not the whole story:** [[SoT - Research-to-Action Protocol]] is the fuller version. It adds scope-lock, a hard start from memory, a 70% stop rule and a savestate when the timer fires first. The MoC calls this note "full protocol with failure modes", which overstates it. This note is the timer-and-question core.
- **It had no link to that SoT**, or to any protocol, and its `type` was `instructional`, which is not a canonical type.

### Changes

| File | Change |
|---|---|
| The note | `type` → `procedure`; added `trigger`, `steps` (4, verb-first, from the note's own How list), `verification`, `conformant: true`; new `## Related` with 5 annotated links; `[implements:: [[The Core Principles of Time Boxing are Fixed Time Allocation a Goal-Oriented Approach and Commitment to Focus]], confidence=medium]` |
| SoT - Research-to-Action Protocol | Related bullet pointing back at the technique |
| Protocol - Vague-to-Action | new bullet under "When It Fails": preparation that turns into open-ended research |

The `implements` edge is structural, so it does not change exposure. The `trigger` and `verification` fields are paraphrased from the note's own text; check the wording.

### Left alone

- **Duplicate SoTs:** [[SoT - Research-to-Action Protocol]] and `Instruction SoT - Research-to-Action Protocol` are near-identical (they differ in Phase 3 and the Related section). A merge candidate, not changed here.
- **`rel:: antidote [[SoT - Illusion of Explanatory Depth (IoED)]]`** is unparsed by `edge_lint.py` and `antidote` is not in the six-word vocabulary, so I left the line as prose. The plain link still resolves.
- **Title** is not in the "How to [do X]" form the procedure schema asks for. Not renamed, to keep the MoC links.
- **Not linked:** [[Protocol - Autonomous Action System]] and [[Protocol - Action-First GTD (LLM Chief of Staff)]] are about routing captured items, not bounding research.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2840 notes, 1381 edges).
