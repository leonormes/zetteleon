---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-knowing-vs-understanding
title: 2026-09-24-knowing-vs-understanding
type: note
---

## Refresh — [[Comparison - Knowing vs Understanding]] — 2026-09-24

### Prompt routing

Per [[00 - Prompt Library Router]]: the note has zero outbound links but five inbound files and a typed `synthesizes` edge from [[MOC - From Information to Knowledge]], so it is a connected note that needs its links expanded. Routed to [[Note Refresh & Link Auditor]]. Lexical search only (1MCP tools were unavailable).

### Link audit

No broken links (resolver: 0 unresolved before and after).

### Findings

1. **`type: comparison` is a singleton.** It is not in the contract's type enum and no other note uses it. The note is really one assertion ("understanding integrates knowledge into actionable frameworks while knowing merely accumulates facts") with a table behind it, so it is now a `claim`.
2. **Five sibling notes already make versions of this distinction** and none linked to each other: [[The Gap Between Knowing a Fact and Understanding a Concept]], [[Learning is the Acquisition of Information While Understanding is the Construction of Meaning]], [[2026-07-25-familiarity-vs-comprehension-distinct-states]], [[SOLO Taxonomy Describes Understanding Levels]] and [[Myopic Understanding]]. They differ enough (an example, the learning view, a debugging view, a five-level scale, an argument map) that I linked them and did not merge.
3. **The table's claim was unevidenced**, and its "merely accumulates" wording is too strong.

### Changes

| File | Change |
|---|---|
| The note | `type` → `claim`; `proposition`, `epistemic_status: medium`, `evidence_links`, empty `contradicts`, `conformant: true`; `[extends:: [[Information vs Knowledge]], confidence=medium]`; `## Tensions` (1), `## Related` (11), `### Where It Applies in ProdOS` (4), `### Further Reading` (3 books). The table and Key Difference are untouched |
| **New:** [[Evidence - Ultralearning Chess Experts Rely on Stored Patterns Where Beginners Remember Piece by Piece]] | Verbatim quote from *Ultralearning* (Calibre 710) on expert pattern memory. Confidence 0.5 |

`--why` now shows the note supported by that Evidence note. Nothing rests on it, so no gap was open.

### Evidence scope

The chess passage supports the "compressed patterns" row (structure versus raw data). It begins mid-argument, is a popular account of one domain, and does not support the wider claim that understanding "integrates knowledge into actionable frameworks". The claim stays `medium`. Two other library passages were kept as reading only: *Grammatical Man* (people keep abstract relationships, not wording) and *Learn Like a Pro*.

### Tension recorded

*Learn Like a Pro* says memorising and understanding help each other ("easier to memorize information when you understand it well, but also easier to understand information that you have memorized"). That qualifies the table's word "merely" in "knowing merely accumulates facts". It is written as a boundary condition, not a contradiction.

### ProdOS linking

[[Stage 3 Understand (The Writing to Learn Layer)]], [[SoT - Research-to-Action Protocol]] (its minimal artifact is a demonstration test), [[2026-07-25-question-master-protocol-blooms-taxonomy]] and [[SoT - Active Learning Techniques]].

### Left alone

- **Title** is a "Comparison - ..." label, not a declarative sentence as the claim schema asks. Not renamed, because the MoC and four notes link to it.
- **Frontmatter** keeps the old `criteria` and `subject` fields; they are harmless.
- **Discarded library hits:** de Bono, Levitin (sleep and memory), the Sports Gene and others matched on memory or learning only.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2864 notes, 1388 edges). Confidence: **medium**.
