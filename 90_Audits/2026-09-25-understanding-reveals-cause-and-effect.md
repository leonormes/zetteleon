---
created: 2026-09-25T00:00:00+00:00
modified: 2026-09-25T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-25-understanding-reveals-cause-and-effect
title: 2026-09-25-understanding-reveals-cause-and-effect
type: note
---

## Clean-up and enrichment — [[Understanding Reveals Cause-and-Effect]] — 2026-09-25

> Routed to [[Orphan Note Positioning & Thread Audit]] per [[00 - Prompt Library Router]] (two inbound links, no claim fields, and a body that was mostly process residue). Lexical search only (1MCP tools were unavailable).

### What the note actually was

A 1,034-word file in `30_Library/MoC/` typed `map`, but it was not a map. It held one real claim paragraph at the top, then an LLM "alchemical" atomisation transcript (Stages 1 to 4: Prima Materia, Calcinatio, Solutio, Coagulatio) that restated the paragraph as three ideas and drafted three notes and a "MOC" that were never created. It is step 2 of the argument map [[Myopic Understanding]], and it ended with a stray link to [[Human Understanding is Inherently Myopic]].

### Changes

| Area | Change |
|---|---|
| **Location and type** | moved from `MoC/` to `100_zettelkasten/` (it is an atomic claim, and links resolve by name, so none broke); `type` `map` → `claim` |
| **Raw transcript** | preserved in `99_Archive/Understanding Reveals Cause-and-Effect (raw atomisation transcript).md`, retitled so it does not collide with the live note |
| **Body** | your claim paragraph and the two original links kept verbatim; the four transcript stages replaced by the three separable ideas they produced (nature, mechanism, application), kept as **Three Ideas Inside It** |
| Frontmatter | `proposition`, `epistemic_status: medium`, `evidence_links` (2), `contradicts: []`, `conformant: true`, aliases and tags; junk `null` keys removed |
| Sections | **Evidence**; **Limits and Tensions** (4); **Related** (9); **Where It Applies in ProdOS** (2); **Further Reading** (2 books) |
| Typed edge | `[extends:: [[Understanding Enables Accurate Predictions]], confidence=medium]`: step 2 of the map builds on step 1 |

### New Evidence (quotes verified verbatim)

| Note | Source | Supports |
|---|---|---|
| [[Evidence - Deutsch Says Theories Are Explanations Not Merely Predictions]] | *The Fabric of Reality* (Calibre 108) | Prediction versus understanding |
| [[Evidence - Covey Says Doing More Faster Fails to Reach the Chronic Causes Behind a Problem]] | *The 7 Habits* (Calibre 1683) | Application to problem-solving (an illustration, not a study) |

### Tensions recorded

- [[Predictive Power Verifies a Theory via Its Outputs, Not Its Proofs]]: prediction can be enough in practice; the claim is about problem-solving and systems.
- [[Logical Positivism Restricts Science's Aim to Predicting Sensory Patterns]] versus [[Deutsch Rejects Instrumentalism Because Prediction Is a Means, Not the Purpose, of Science]]: the closest vault notes to this claim.
- [[SoT - Cynefin Framework]]: in complex domains cause and effect is visible only in hindsight.

### Decisions to check

1. **Moved the file out of `MoC/`.** If you want it left in place I can move it back; the frontmatter and links do not depend on the folder.
2. **Not split into three notes.** The map treats the idea as one step and the prior atomisation drafted three notes that were never created, so I kept the three ideas as a section.
3. **No typed edge for the tension with the Deutsch or positivism notes**; they are related, not dependent.

### Fixed during the run

The first lint after the move showed 3 "ambiguous title" warnings, because the archived copy still carried the live note's title. I retitled the archive copy, and the lint is clean.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2906 notes, 1409 edges). Foundation gaps unchanged at 38. Resolver: 0 unresolved links in the note and both Evidence notes.
