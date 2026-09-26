---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-task-bracketing
title: 2026-09-24-task-bracketing
type: note
---

## Positioning and enrichment — [[Task Bracketing Strengthens Habit-Related Neural Circuits]] — 2026-09-24

> Routed to [[Orphan Note Positioning & Thread Audit]] per [[00 - Prompt Library Router]] (one inbound link, no outbound links, no claim fields). Lexical search only (1MCP tools were unavailable).

### Baseline

A three-sentence claim that reinforcing the start and end of a habit strengthens the loop, because basal ganglia circuits are most active at those points. One inbound link (its hub, [[MOC - The Science of Making and Breaking Habits]]), no outbound links, `conformant: false`, and no broken links.

### Key finding: two claims in one

| Claim | Status |
|---|---|
| **Neuroscience:** basal ganglia circuits are most active at the start and finish of a habit | Attributable to Ann Graybiel's striatal work. *The Power of Habit* (Calibre 413) cites her papers in its endnotes, but the chapter text stating the finding could not be retrieved from the index, so it is **unverified here** |
| **Technique:** clear start-cues and end rituals strengthen the whole loop | An inference from the first claim, untested in the vault |

I recorded that split in the note and set `epistemic_status: low`. I did not create an Evidence note, because the only retrievable passages were reference lists, which cannot be quoted as evidence of the finding.

### Changes

| Area | Change |
|---|---|
| Frontmatter | `proposition`, `epistemic_status: low`, empty `evidence_links` and `contradicts`, `conformant: true` |
| Typed edge | `[depends_on:: [[Neuroplasticity is the Foundation for Habit Change]], confidence=medium]`: the strengthening rests on repetition rewiring circuits. That claim is grounded, so no gap is created |
| Sections | **What Is Claimed, and What Is Evidenced**; **Tensions** (1); **Related** (16); **Where It Applies in ProdOS** (3); **Further Reading** (1 book, as a lead only) |
| Reciprocal | bullets on [[Continuation Rituals Bridge Work Sessions for ADHD]] (end-cue) and [[A Startup Ritual Eases the Transition into a Project Mindset]] (start-cue) |

**Not typed:** [[Habits are Automatic Behaviors Triggered by Environmental Cues]] is the natural premise for the start-cue half, but it has no grounds, so an edge would create an ungrounded foundation. It is linked plainly.

### ProdOS

- [[Protocol - Weekly Command Centre]]: a named trigger and a Definition of Done, so a bracketed routine.
- [[SoT - Research-to-Action Protocol]]: a starter task to open, a commit to close, and a ban on "just five more minutes".
- [[SoT - ProdOS Thinking Stream]]: a loop with an explicit EXIT step.

### Tension recorded

[[The Hemingway Technique - End Work With Unfinished Problems]] says end a session on an open problem; bracketing asks for a clear ending. Both can hold, because they apply to different ends (the session's restart versus the habit loop), so it is prose, not `contradicts`.

### Left alone

- **`Exit Ritual For ADHD Time Boxes`** is referenced elsewhere in the vault but does not exist as a note; I did not link it.
- **The library hit that would settle the neuroscience claim** is not retrievable. If you have the Graybiel review (Annual Review of Neuroscience 31, 2008) or the chapter itself, that would make a good Evidence note.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2892 notes, 1398 edges). Resolver: 0 unresolved links in the note.
