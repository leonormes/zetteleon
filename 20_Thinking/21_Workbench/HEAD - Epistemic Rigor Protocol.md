---
aliases: []
created: 2026-04-21T00:00:18+00:00
modified: 2026-04-21T17:07:06+00:00
tags: [prodos/head, state/thinking]
title: HEAD - Epistemic Rigor Protocol
---

## Applicability Limits

Name them explicitly in the doc. This workflow is optimised for argumentative non-fiction prose. It needs modification or replacement for:

| Text type                        | What breaks                                                   |
| -------------------------------- | ------------------------------------------------------------- |
| Mathematical / formal proofs     | 1.4 is trivially satisfied; the interesting work is elsewhere |
| Fiction / narrative              | No claim–grounds structure to map                             |
| Poetry                           | 1.1 strips the content                                        |
| Empirical papers with statistics | Need base rates, priors, effect sizes—1.4 is too coarse       |
| Reference material               | No argument; skip Phase 1 entirely, go straight to atoms      |
| Rhetoric as object-of-study      | 1.1 is wrong; rhetoric is the data                            |

---

## Revised Skeleton

```
Phase 0 — Triage
  0.1 Purpose (why am I reading this?)
  0.2 Depth warrant (skim / literature note / full deconstruction)
  0.3 Text-type check (does this workflow apply, or do I need a variant?)

Phase 1 — Deconstruction  (argumentative prose variant)
  1.1 Strip rhetoric; surface unstated assumptions; steelman
  1.2 Toulmin map (claim, grounds, warrant, backing, qualifier, rebuttal)
  1.3 Categorise: descriptive / normative / procedural;
      field-invariant vs field-dependent
  1.4 Test: validity+soundness OR strength+cogency+falsifiability;
      update Bayesian prior

Phase 1.5 — Literature Note  (new)
  Summary in own words, bound to source + locator

Phase 2 — Synthesis
  2.1 Atomic (self-contained, one idea, one level, own words)
  2.2 Structural hub note with typed-link vocabulary
  2.3 Idea Compass (origins, applications, allies, competitors, trajectory)
  2.4 Cluster-to-draft trigger (e.g. 5–7 outbound links on a theme)

Phase 3 — Maintenance & Retrieval  (new)
  3.1 Periodic review (orphans, dead hubs, stale claims)
  3.2 Pruning / merging / retiring notes
  3.3 Query-driven retrieval (new question → walk the graph)
```

---

## Phase 2: Knowledge Architecture (Synthesis)

Once the text is filtered, translate the surviving ideas into your own system, ensuring a strict separation between objective facts and subjective context.

1. Cleave into Atomic Notes: * _Action:_ Write each verified, objective claim as a single, indivisible idea.
    - _Enhancement:_ Enforce a "Binary Category Invariant." Atomic notes must be entirely context-free—acting purely as building blocks (e.g., definitions, verifiable statements). They should be written in your own words to ensure true comprehension, not simply copied.
2. Construct Structural / Hub Notes: * _Action:_ Rebuild the context that was stripped away during the cleaving process.
    - _Enhancement:_ Create Structural Notes (or map notes) to preserve the original narrative, argument, or sequence. Use these notes to link your new atomic facts together using typed links (e.g., _Note A_ `[supports]` _Note B_). The Structural Note provides the architecture; the Atomic Notes provide the bricks.
3. Stress-Test & Connect (The Idea Compass): * _Action:_ Compare new notes against existing ones to detect contradictions or paradoxes.
    - _Enhancement:_ Map the new proposition along four axes: its _origins_ (where did this idea come from?), its _applications_ (where does this lead?), its _allied concepts_ (what is similar?), and its _competitors_ (what opposes this?).
4. Iterate Towards Output: * _Action:_ Allow the system to act as a dialogue partner.
    - _Enhancement:_ Treat this network not as an archive for storage, but as an active workspace. As connections form, cluster these notes to outline original arguments, transitioning seamlessly from note-making to drafting new writing.
This is an exceptional critique. It diagnoses the exact points of friction where knowledge systems typically collapse into mere archives—specifically the activation energy required to process texts, the lossy nature of skipping literature notes, and the lack of a maintenance schedule. The structural gaps identified are spot on.

As instructed, we will not overhaul the entire protocol in one go. We will focus strictly on the highest-leverage addition to reduce task-initiation friction.

Here is the implementation of Phase 0 into the working document:

---

### Phase 0: Triage (The Pre-Filter)

Before running the full deconstruction engine, answer these three questions to manage the required activation energy and determine the appropriate depth of processing:

- Purpose: Why am I engaging with this text? _(e.g., Answering a specific question, general learning, drafting a specific piece of writing, steelmanning an opposing view, or pure curiosity)._
- Depth Warrant: What level of processing does this text actually deserve? _(e.g., A quick skim, a standalone Literature Note, or a full Phase 1 deconstruction)._
- Text-Type Check: Does the standard argumentative workflow apply here? _(e.g., If it is a mathematical proof, narrative fiction, or reference material, bypass the standard rhetoric filters and use the appropriate variant)._

---

By gating the heavy machinery behind this triage step, the system immediately becomes less daunting to initiate.

Whenever you are ready for the next sitting, we can integrate the Literature Note layer (Phase 1.5) and establish the typed-link vocabulary.
