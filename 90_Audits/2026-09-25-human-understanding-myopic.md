---
created: 2026-09-25T00:00:00+00:00
modified: 2026-09-25T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-25-human-understanding-myopic
title: 2026-09-25-human-understanding-myopic
type: note
---

## Expansion and enrichment — [[Human Understanding is Inherently Myopic]] — 2026-09-25

> Routed to [[Orphan Note Positioning & Thread Audit]] per [[00 - Prompt Library Router]] (a 72-word note with `type: ''`, two bare links and no claim fields). Lexical search only (1MCP tools were unavailable).

### Where it sits

Step 4 of the argument map [[Myopic Understanding]]: understanding pays out as prediction and causal insight, both scale with the width of the view, but the view is structurally narrow. It already carried typed edges from the map and a `depends_on` from [[Antithetical Knowledge Systems in the 17th Century]]. Before this run it asserted the limit without saying why, what it costs, or what helps.

### Expansion (your original paragraph and two links kept)

| Section | Content |
|---|---|
| **Why It Happens** | Capacity ([[Limited Capacity Brain]], [[SoT - Working Memory & Schema Theory]]); completeness is assumed (WYSIATI); part of the picture lives outside our heads (community of knowledge); plus the reinforcement loop (IoED, biases reinforcing mental models) |
| **What It Costs** | Seven linked notes: paradigm shifts, transitional eras, listening, attribution errors, flawed models, closed systems, information overload |
| **What Helps** | Abstraction (with what it costs), outside error-detectors, feedback-seeking, provisional views, externalising the picture: 11 notes |
| **Tensions** | [[Deep Focus on a Single Concept Sparks Innovation]] (deliberate narrowing is a tool) |
| **Related, Further Reading** | The neighbouring steps of the argument map; three books |

### New Evidence (all quotes verified verbatim)

| Note | Source | Supports |
|---|---|---|
| [[Evidence - Kahneman WYSIATI Says We Treat the Limited Information We Have as if It Were All There Is]] | *Thinking, Fast and Slow* (Calibre 53) | The bias half: the limited view is treated as complete |
| [[Evidence - Levitin Says Attention Is a Limited-Capacity Resource With Definite Limits]] | *The Organized Mind* (Calibre 689) | The capacity mechanism |
| [[Evidence - Sloman and Fernbach Say We Mistake Knowledge in the Community for Knowledge in Our Heads]] | *The Knowledge Illusion* (Calibre 707) | Why the individual view is narrower than it feels |

Each states what it does not show: none measures how small a fraction of reality we perceive, and Kahneman and Sloman and Fernbach support the incompleteness, not the capacity claim.

### Frontmatter and edges

- `type` `''` → `claim`; `proposition`, `epistemic_status: medium`, `evidence_links` (3), `contradicts: []`, `conformant: true`; tags extended.
- **New:** `[depends_on:: [[Limited Capacity Brain]], confidence=high]` (the map's own step 5 names capacity as the mechanism; that note is an axiom).
- **Inbound edges added:** [[Paradigm Shifts Complete Through Generational Turnover, Not Persuasion]] and [[Abstraction as Climbing a Hill]] each `depends_on` this claim (`confidence=medium`). Both already argue from the premise ("neither side can see from inside", "we are forced to climb because we are lost in the valley").

### Graph effect

`--why` now shows the claim supported by the three Evidence notes and resting on the capacity axiom. It has dependents (the two above plus the earlier Antithetical Knowledge Systems chain), so it is a load-bearing claim that was previously unevidenced; that is now closed.

### Judgement calls

- **Tension, not `contradicts`:** the map holds a `contradicts` edge between the myopia thesis and deep focus. I wrote it here as prose because the two claims are about different conditions (unnoticed versus chosen narrowness); the map's edge is untouched.
- **Kept `epistemic_status: medium`:** the claim is broad and the evidence supports its parts (capacity, assumed completeness, external knowledge), not a measured "small fraction".
- **The `Information Overload` note** is a YouTube-link stub; linked as it is.

### Fixed during the run

One link used the wrong case (`The Brain is Biased toward…` versus the file `The brain is biased toward…`); corrected with a display alias.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2897 notes, 1404 edges). Resolver: 0 unresolved links in the note and the three Evidence notes.
