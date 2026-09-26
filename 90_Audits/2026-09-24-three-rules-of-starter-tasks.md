---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-three-rules-of-starter-tasks
title: 2026-09-24-three-rules-of-starter-tasks
type: note
---

## Refresh — [[The Three Rules of Starter Tasks]] — 2026-09-24

### Prompt routing

Per [[00 - Prompt Library Router]]: not an orphan (six files link in, and a procedure depends on it), so the row for "one note's links checked and expanded" applies: [[Note Refresh & Link Auditor]]. Lexical search only (1MCP tools were unavailable).

### Link audit

No broken links (resolver: 0 unresolved before and after). Its single Related link resolved.

### Finding: an ungrounded foundation

[[Weekly Review Verifies Project Actionability and Context]] carries `[depends_on:: [[The Three Rules of Starter Tasks]]]`, and the note had no grounds, so the compiler listed it as a foundation gap ("depended-on by 1"). The note also cited no source for its numbers (5 to 15 minutes, ideally 1 to 5).

### Changes

| File | Change |
|---|---|
| The note | `proposition`, `epistemic_status: low`, `evidence_links`, empty `contradicts`, `conformant: true`; `[extends:: [[Micro-Stepping Reduces Cognitive Load for Task Initiation]], confidence=medium]`; `## Tensions` (2), `## Related` (8), `### Where It Applies in ProdOS` (4), `### Further Reading` (2 books) |
| **New:** [[Evidence - Tracy Momentum Principle Says Starting Costs More Energy Than Continuing]] | Verbatim quote from *Eat That Frog!* (Calibre 1591) that starting takes far more energy than continuing. Confidence 0.4 |

**Result:** the gap is closed. `--why` now shows the note supported by the Evidence note, and the audit's gap count fell from 39 to 38.

**The evidence is deliberately scoped:** it supports rule 1 (a starter task exists to build momentum). It is a self-help assertion, not a study, and gives no duration, so **the 5 to 15 minute limit and the "simple, physical" rule remain unevidenced.** That is why `epistemic_status` is `low`, not `medium`.

### Tension recorded (unresolved)

The vault gives at least three different sizes for the smallest unit of action:

| Where | Limit |
|---|---|
| This note | 5 to 15 minutes (ideally 1 to 5) |
| [[SoT - PRODOS Core Specification]] §3.2 (also calls it a "Starter Task (MVA)") | under 120 seconds |
| [[Micro-Stepping Reduces Cognitive Load for Task Initiation]] and *Atomic Habits* | under two minutes |

One reading lets them coexist (the MVA is the first physical action inside a starter task), but nothing in the vault says so. The 2026-08-29 fitness audit flagged the same divergence. I recorded it as a tension and did not pick a number.

### Left alone

- [[Chaining Starter Tasks Creates a Momentum Ramp]] (an unrun hypothesis) stays as the note's original Related link.
- [[The Framework Solves Task Initiation Difficulties]] mentions starter tasks but I did not read it closely enough to link.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2862 notes, 1386 edges). Confidence: **medium**.
