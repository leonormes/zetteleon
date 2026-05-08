---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:37+00:00
title: Applicability Limits
---

## Applicability Limits

Name them explicitly in the doc. This workflow is optimised for argumentative non-fiction prose. It needs modification or replacement for:

| Text type | What breaks |

|---|---|

| Mathematical / formal proofs | 1\.4 is trivially satisfied; the interesting work is elsewhere |

| Fiction / narrative | No claim–grounds structure to map |

| Poetry | 1\.1 strips the content |

| Empirical papers with statistics | Need base rates, priors, effect sizes—1.4 is too coarse |

| Reference material | No argument; skip Phase 1 entirely, go straight to atoms |

| Rhetoric as object-of-study | 1\.1 is wrong; rhetoric is the data |

---

## Revised Skeleton

[Phase 0—Triage! 0.1 Purpose (why am I reading this!)! 0.2 Depth warrant (skim! literature no.md](Phase%200%20—%20Triage!%20%200.1%20Purpose%20(why%20am%20I%20reading%20this!)!%20%200.2%20Depth%20warrant%20(skim%20!%20literature%20no.md)

---

## Phase 2: Knowledge Architecture (Synthesis)

Once the text is filtered, translate the surviving ideas into your own system, ensuring a strict separation between objective facts and subjective context.

1. Cleave into Atomic Notes: \* _Action:_ Write each verified, objective claim as a single, indivisible idea.

   - _Enhancement:_ Enforce a "Binary Category Invariant." Atomic notes must be entirely context-free—acting purely as building blocks (e.g., definitions, verifiable statements). They should be written in your own words to ensure true comprehension, not simply copied.

2. Construct Structural / Hub Notes: \* _Action:_ Rebuild the context that was stripped away during the cleaving process.

   - _Enhancement:_ Create Structural Notes (or map notes) to preserve the original narrative, argument, or sequence. Use these notes to link your new atomic facts together using typed links (e.g., _Note A_ `[supports]` \_Note B\_). The Structural Note provides the architecture; the Atomic Notes provide the bricks.

3. Stress-Test & Connect (The Idea Compass): \* _Action:_ Compare new notes against existing ones to detect contradictions or paradoxes.

   - _Enhancement:_ Map the new proposition along four axes: its _origins_ (where did this idea come from?), its _applications_ (where does this lead?), its _allied concepts_ (what is similar?), and its _competitors_ (what opposes this?).

4. Iterate Towards Output: \* _Action:_ Allow the system to act as a dialogue partner.

   - _Enhancement:_ Treat this network not as an archive for storage, but as an active workspace. As connections form, cluster these notes to outline original arguments, transitioning seamlessly from note-making to drafting new writing.
      This is an exceptional critique. It diagnoses the exact points of friction where knowledge systems typically collapse into mere archives—specifically the activation energy required to process texts, the lossy nature of skipping literature notes, and the lack of a maintenance schedule. The structural gaps identified are spot on.

As instructed, we will not overhaul the entire protocol in one go. We will focus strictly on the highest-leverage addition to reduce task-initiation friction.

Here is the implementation of Phase 0 into the working document:

### 2\. Missing the Literature Note Layer

Your pipeline jumps from filtered text → atomic notes. Ahrens is explicit that there should be an intermediate layer: the literature note—a short summary, in your own words, bound to the source. It preserves the _reading experience_ before you shatter it into context-free atoms.

You'll want this because:

- Atoms lose the shape of the original. A literature note keeps it, once, in one place.
- It's the natural artefact to cite from later (source + page + your paraphrase).
- It's a cheaper output for low-stakes texts that don't warrant atomisation.

### Phase 2.1—Atomic Notes

- "Binary Category Invariant"—I'd challenge this term. Atomic notes are not _context-free_; they are _context-minimal_. A definition has a domain. A claim has scope conditions. Forcing "entirely context-free" will either produce notes that are too vague to be useful, or notes that lie by omission. Reframe as: "self-contained—readable in isolation without reference to source."
- Enforce one idea per note, but also one _level_ per note. A note mixing a definition and an implication violates atomicity just as badly as one mixing two claims.

### Phase 2.2—Structural Notes with Typed Links

- You mention typed links but without an ontology. Link types proliferate chaotically unless constrained. Define a small fixed vocabulary, e.g.:
   - `[supports]`, `[contradicts]`, `[refutes]`
   - `[extends]`, `[generalises]`, `[instantiates]`
   - `[depends-on]`, `[precedes]`
   - `[analogous-to]`, `[competes-with]`
- Anything outside this vocabulary is a smell—either the link type should be added deliberately, or the relationship belongs in prose inside a structural note.

### Phase 2.3—Idea Compass

- Four axes (origins, applications, allies, competitors) miss a temporal dimension: trajectory. Where has this idea come from _and where is it going_? What are the currently open problems in its research programme? This matters most for ideas in active flux (software architecture, ML, policy) rather than settled ones.

### Phase 2.4—Iterate Towards Output

- Correct framing but mechanically underspecified. "Cluster notes to outline arguments" is exactly the kind of verb-without-object that fails ADHD executive function. What is the _concrete ritual_? My suggestion: when a hub note reaches \~5–7 outbound links on a coherent theme, that's the trigger to draft.
