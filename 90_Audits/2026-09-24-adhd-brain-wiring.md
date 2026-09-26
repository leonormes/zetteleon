---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-adhd-brain-wiring
title: 2026-09-24-adhd-brain-wiring
type: note
---

## Broken links, value check and ProdOS linking — [[ADHD Brain Wiring vs. Classic Productivity Systems]] — 2026-09-24

> Method note: 1MCP tools were unavailable, so checks were lexical (`rg`) plus file reads and a filename-and-alias resolver script.

### Broken links: 3 found, all fixed (none removed)

| Original link | Problem | Fix |
|---|---|---|
| `[[The OSI model]]` (also had a "the The" typo) | No OSI model note or alias exists | Prose now reads "the [[Layer 1 Physical Layer\|physical layer]] of the OSI model", and the Application Layer mention links to [[Layer 7 Application Layer]] |
| `[[Discomfort with Ambiguity Prevents Deeper Thinking]]` | No such note or alias | Retargeted to [[SoT - Cognitive Ambiguity and Deep Thinking]] (alias "The Ambiguity Barrier"), keeping the original wording as the display text |
| `[[Emergence and the Absence of Teleology]]` | No such note or alias | Split into [[Emergence]] and [[SoT - Metaphysics of Purpose]] (its alias is "Teleological Framework"), with "teleology" as display text |

The fourth link, [[Antithetical Knowledge Systems in the 17th Century]], already resolved. After the edits a resolver run finds **0 unresolved links** in the note.

### Verdict: keep as one note; not atomised

At 308 words it is one thesis (classic linear systems clash with ADHD interest-driven processing) with five illustrative lenses (historical, OSI metaphor, cognitive science, ambiguity, teleology). The lenses are analogies for the thesis, not separate claims, so splitting them would strip the argument. Two of them (decontextualised lists block schema formation; ambiguity may be fuel) could become claims later if you want them tested on their own.

### Changes

| File | Change |
|---|---|
| The note | `type` `permanent` → `claim`; `proposition`, `epistemic_status: low`, empty `evidence_links` and `contradicts`, `conformant: true`; the three link fixes; `## Related` (4 links) and `### Where It Applies in ProdOS` (4 links) |

`epistemic_status` is `low` (speculative) on purpose: the note reasons by analogy, hedges itself ("perhaps", "can be seen as"), and cites no evidence.

### ProdOS linking

- [[SoT - Execution Protocol (GTD & PARA)]]: the classic linear system it critiques.
- [[Deep Dive Sessions for ADHD (Adapted GTD Next Actions)]]: the experiment that tests this thesis directly. Still unrun.
- [[The Clarification Ritual (Stuff to Action)]]: the opposite bet, which this note predicts may cost motivation.
- [[Protocol - Weekly Command Centre]]: a design answer (a floor small enough for a bad week).

### Left alone

- **A structural edge rests on a low-confidence claim:** [[SoT - ADHD Management Protocols]] carries `[extends:: [[ADHD Brain Wiring vs. Classic Productivity Systems]], confidence=high]`. That is structural, so it does not change exposure, but the SoT's stated confidence is higher than the note it extends.
- **[[Emergence]] is a template stub** ("Suggested Links" and "see note 2" placeholders). The link resolves but the note is thin.
- **`last_reviewed: 'null'`** left as it was.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2857 notes, 1382 edges).
