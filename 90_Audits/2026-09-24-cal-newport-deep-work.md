---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-cal-newport-deep-work
title: 2026-09-24-cal-newport-deep-work
type: note
---

## Value check and ProdOS linking — [[Cal Newport's Deep Work Method Involves Rigorous Time Blocking to Maximize Concentration]] — 2026-09-24

> Method note: 1MCP tools were unavailable, so checks were lexical (`rg`) plus file reads and `edge_lint.py`.

### Verdict: keep, as the hub of the Deep Work cluster

- **Useful:** it is the anchor for a small 2026 deep-work set. [[Hybrid Attention Model Assigns Remote Days to Deep Work and Office Days to Shallow Work]], [[Structured Collaboration Systems Replace Hyperactive Hive-Mind Messaging Cultures]], [[Pseudo-productivity Heuristic]] and [[Quality Over Quantity in Creative and Cognitive Work]] all point at it, and it fits your own work pattern (long stretches of complex infrastructure work that fragment easily).
- **Underlinked in the graph:** those four inbound notes state the relationship in prose ("extends:", "supports:") but only Quality Over Quantity has a real typed edge (`synthesizes`). It is not a graph node. It also had no outbound links, and the Temporal SoT did not list it.
- **Frontmatter** was non-conformant (four missing claim fields).

### Changes

| File | Change |
|---|---|
| The note | `proposition`, `epistemic_status: medium`, empty `evidence_links` and `contradicts`, `conformant: true`; `[extends:: [[The Core Principles of Time Blocking are Proactive Planning Single-Tasking and Visual Schedule Integration]], confidence=medium]`; new `## Related` (7 links) and `### Where It Applies in ProdOS` (3 links) |
| SoT - Temporal Management (Blocking and Boxing) | bullet under Related Knowledge |
| Fixed-Schedule Productivity note | new Related bullet for this note, plus a **correction** (below) |

### Correction to my previous run

In the Fixed-Schedule audit I said [[Protocol - Weekly Command Centre]] "blocks one deep-work session for the week". That was wrong. The line is under **Tier 1 candidates**, promoted only after four clean runs; the Tier 0 floor plans no schedule at all. I corrected both the note's link text and that audit.

### ProdOS linking

- [[SoT - Indistractable Model (Focus Management)]]: protects a scheduled block from prompts.
- [[Phase 3 - Compartmentalized Focus to Beat Distraction]]: its "deep work environment" step.
- [[Protocol - Weekly Command Centre]]: linked, with the accurate Tier 1 wording.
- No ProdOS protocol currently schedules deep-work blocks as part of the running loop.

### Left alone

- **Overlap with [[Fixed-Schedule Productivity Creates Artificial Constraints to Drive Efficiency]]:** both describe a fully planned day with a hard focus on protecting output. Different emphasis (concentration versus hard stop), so I linked them and did not merge.
- **Prose-only relationships in the four inbound notes** (Hybrid Attention "extends", Structured Collaboration "extends", Pseudo-productivity "supports") were not converted to typed edges. Each would need its own test, and "structured collaboration is infrastructure required for deep work" reads more like a `depends_on` on that side than an `extends`.
- **Attribution:** the Temporal SoT cites Newport's *Slow Productivity*; this note is about *Deep Work*. The note's Related bullet says so, so the two are not confused.
- **No evidence** is linked; the note rests on Newport's book, which I did not quote.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2845 notes, 1384 edges).
