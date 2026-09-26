---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-question-master-protocol
title: 2026-09-24-question-master-protocol
type: note
---

## Value check and ProdOS linking — [[2026-07-25-question-master-protocol-blooms-taxonomy]] — 2026-09-24

> Method note: 1MCP tools were unavailable, so checks were lexical (`rg`) plus file reads and `edge_lint.py`. This note was already positioned once in [[2026-07-30-question-master-protocol]]; this run re-checks it.

### Verdict: keep, as a small atom in the IoED forcing-function set

- **Useful, modestly.** It is one of the named antidotes in [[SoT - Illusion of Explanatory Depth (IoED)]] (section 4E), alongside the build-it standard, five whys and time-boxing. It is a real technique, and its own steelman correctly scopes it to consolidation, not first-pass learning.
- **Thin on its own:** one paragraph, no ProdOS protocol operationalises it, and the SoT gives it two lines.
- **Placement gap:** [[SoT - Active Learning Techniques]] is the vault's canonical collection of learning antidotes and did not mention it.

### Finding: a mis-typed edge closed a loop

The note carried `[supports:: [[SoT - Illusion of Explanatory Depth (IoED)]]]` (added in the 2026-07-30 run). That fails the denial test: if active questioning did not work, the SoT's diagnosis that the illusion exists would still stand; it would only lose one remedy. It also created a cycle: IoED SoT → [[2026-07-25-familiarity-vs-comprehension-distinct-states]] → this note → IoED SoT.

**Fix:** retyped it to `[implements:: [[SoT - Illusion of Explanatory Depth (IoED)]], confidence=medium]` with a sentence explaining why. The audit's cycle count dropped from 35 to 34, and no new gap appeared. This reverses a decision from the earlier run.

### Changes

| File | Change |
|---|---|
| The note | edge retyped (above); new `## Related` with 5 annotated links (Active Learning Techniques, Build-It sibling, Five Whys sibling, Time-Boxing sibling, Information Retrieval Is Not Learning) |
| SoT - Active Learning Techniques | new `## Related` with one bullet for this technique |

### ProdOS linking: honest result

No existing ProdOS protocol applies this technique, so I did not force a link. The closest candidate is ingestion of source material ([[Atomic Signal Extractor → Write TMP file]]), which already has a "Card Forcing Function" for size. A question-generation pass before extraction would match this note's own steelman (best for consolidation). That would be a new step in a prompt, so it is a design decision for you, not a link.

### Left alone

- **The same cycle pattern** exists through [[2026-07-25-build-it-standard-tests-understanding-via-creation]], [[2026-07-25-five-whys-chain-drills-to-first-principles]] and [[Information Retrieval Is Not Learning]] (all `supports` the IoED SoT, which supports [[2026-07-25-familiarity-vs-comprehension-distinct-states]]). Not changed here.
- **Title** is a date-prefixed slug, not a declarative sentence; the sentence lives in an alias, and [[2026-07-25-familiarity-vs-comprehension-distinct-states]] links through that alias. Not renamed.
- **Empty fields:** `## Open Questions` (falsifiers, crux, counter-positions) is blank and `evidence_links` is empty; the only evidence is the SoT's own line.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2842 notes, 1382 edges).
