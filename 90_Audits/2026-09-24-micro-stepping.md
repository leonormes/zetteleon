---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-micro-stepping
title: 2026-09-24-micro-stepping
type: note
---

## Refresh — [[Micro-Stepping Reduces Cognitive Load for Task Initiation]] — 2026-09-24

### Prompt routing

Per [[00 - Prompt Library Router]]: unlike the previous note, this one is **not** an orphan. It has 13 inbound files and three typed edges pointing at it ([[MOC - Why Task Initiation is Difficult in ADHD]] `synthesizes`, [[SoT - ADHD Management Protocols]] `implements` with strength 5, [[Master Micro-Actions & Starter Tasks]] `supports`). The router row for "ONE note's links checked and expanded" is [[Note Refresh & Link Auditor]], so I used that instead of the orphan-positioning prompt. Lexical search only (1MCP tools were unavailable).

### Link audit

- **Broken links: none.** A resolver run finds 0 unresolved links before and after.
- **One syntax problem:** the note's `rel:: [[SoT - ADHD Management Protocols]] (Section 3.4...)` line is not parsed by `edge_lint.py`. Replaced by an annotated bullet that says the SoT carries the real `implements` edge.

### Refresh applied

| Area | Change |
|---|---|
| Frontmatter | `proposition`, `epistemic_status: medium`, empty `evidence_links` and `contradicts`, `conformant: true` (was missing all four claim fields) |
| Related | 9 annotated links added (Master Micro-Actions, Three Rules of Starter Tasks, 5-Minute Action, Limbic Friction, MVE, Infinite Canvas, Low Activation Cost Effect, Next Action claim, the hub) |
| New section | `### Overlap With Sibling Notes` |
| New section | `### Where It Applies in ProdOS` (Vague-to-Action, Weekly Command Centre, Weekly Review note, Execution Protocol SoT) |
| New section | `### Further Reading (Personal Library)`: *Atomic Habits* (Two-Minute Rule) and *Eat That Frog!* (momentum principle), both read in full in the previous run |

**No new typed edges.** The three existing inbound edges are correct. A reverse edge to [[Master Micro-Actions & Starter Tasks]] would create a cycle, and an edge to [[Limbic Friction is the Activation Energy for Habits]] fails the denial test (the claim works without the anxiety-and-tiredness definition), so those stay plain links.

### Thread audit

- **Grounding:** `--why` shows the claim supported by [[Master Micro-Actions & Starter Tasks]], which is an **axiom** with `epistemic_status: high` and no evidence. The whole family therefore rests on one unevidenced premise.
- **Exposure:** nothing counts as depending on it (the two inbound `implements` and `synthesizes` edges are structural).
- **Not linked as evidence:** the Bandura and Schunk Evidence note from the previous run supports chunking for progress and interest, not cognitive load, so it was not attached here.

### Finding: three notes describe one family of moves

| Note | Scope |
|---|---|
| [[Master Micro-Actions & Starter Tasks]] (axiom) | The specific rule: first step under two minutes, purely physical, below the "Wall of Awful" |
| **This note** | The general intervention: smallest possible actionable steps, lowers activation cost |
| [[Breaking Projects Into Micro-Tasks Reduces ADHD Overwhelm]] | The project-level version: visible path, milestones, re-entry |

Master Micro-Actions and this note are close to restatements of each other; the `supports` edge between them mostly records that. Merging is a design choice, so nothing was merged.

**Correction to my previous audit:** I said this note and the Breaking Projects note share the alias "Task Chunking". They do not: this note's alias is `Task Chunking` and the other's is `Task Chunking Strategy`. They are near-duplicates, not identical.

### Next action

Decide whether to fold the three notes into one parent claim with two sections, keeping Master Micro-Actions as the evidenced or axiom core.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2861 notes, 1385 edges). Confidence: **medium**.
