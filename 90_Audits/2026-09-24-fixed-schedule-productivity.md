---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-fixed-schedule-productivity
title: 2026-09-24-fixed-schedule-productivity
type: note
---

## Value check and ProdOS linking — [[Fixed-Schedule Productivity Creates Artificial Constraints to Drive Efficiency]] — 2026-09-24

> Method note: 1MCP tools were unavailable, so checks were lexical (`rg`) plus file reads and `edge_lint.py`. The note was positioned once before ([[2026-07-31-fixed-schedule-productivity]]), which added its only edge.

### Verdict: keep, but it was stranded

- **Useful:** it names a distinct, well-known scheduling stance: every minute planned in advance with a hard stop. It fits your own stated failure mode of work bleeding into personal time, and it is the mirror of the Unschedule in [[SoT - Indistractable Model (Focus Management)]].
- **Stranded:** nothing linked to it (inbound from vault notes: zero, only the old audit). The canonical hub, [[SoT - Temporal Management (Blocking and Boxing)]], covers time boxing and never mentions it. Its `epistemic_status` was `high` with no evidence, which overclaims.
- **Not a graph node**: its only edge is structural, so `--why` and `--impact` return "no node found".

### Changes

| File | Change |
|---|---|
| The note | `epistemic_status` high → `medium` (no evidence linked); new `## Related` with 4 links and a `### Tension` section with 3; `[extends:: [[The Core Principles of Time Boxing are Fixed Time Allocation a Goal-Oriented Approach and Commitment to Focus]], confidence=medium]` |
| SoT - Temporal Management (Blocking and Boxing) | bullet under Related Knowledge |
| Flexibility Within Structure is Key to Sustainable Timeboxing | bullet pointing at the rigid pole it qualifies |

### Tension, deliberately not an edge

[[Flexibility Within Structure is Key to Sustainable Timeboxing]] says a schedule should be "a guide, not a rigid prison". That collides with a fully planned day, but both can hold if the failure mode differs (work bleeding out versus brittle plans). Under the contradiction-vs-tension test that is a tension, so it is written as prose and there is no `contradicts` edge. The ADHD version is in [[Combining structure with flexibility satisfies neurodivergent dual needs]].

### ProdOS protocols

- **[[Protocol - Weekly Command Centre]]:** linked as the minimal end of the spectrum. **Corrected 2026-09-24 (later run):** I first wrote that it blocks one deep-work session per week; in fact its Tier 0 floor plans no schedule, and a single deep-work block is only a Tier 1 candidate, promoted after four clean runs. The link text in the note was fixed. It is contrast, not application.
- **No protocol operationalises a fixed schedule.** The two protocols the Temporal SoT names ([[Protocol - Weekly Command Centre]], [[Protocol - Action-First GTD (LLM Chief of Staff)]]) cover weekly alignment and task capture. Adopting a fixed schedule would be a design decision for you, and it sits awkwardly with ProdOS's "manage energy and focus, not just time" principle in [[leon-context-project-prodos]].

### Left alone

- **The existing `implements` edge to [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]] is weak.** That SoT's Container phase time-boxes one MVA, not a whole day. It is structural, so harmless to exposure, but it overstates the link. Not changed.
- **No source or evidence:** the note names no author. The Temporal SoT credits the Newport "Slow Productivity" philosophy, but I did not attribute the note to him without a source.
- **Frontmatter `prodos.kind`/`prodos.lifecycle`** were left as they were.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2843 notes, 1383 edges).
