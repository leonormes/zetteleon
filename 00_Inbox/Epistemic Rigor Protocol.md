---
created: 2026-04-21T17:04:15+00:00
modified: 2026-04-21T17:13:07+00:00
title: Epistemic Rigor Protocol
---

## Phase 0—Triage

0.1 Purpose (why am I reading this?)

0.2 Depth warrant (skim / literature note / full deconstruction)

0.3 Text-type check (does this workflow apply, or do I need a variant?)

- Purpose: Why am I engaging this text? (Answering a specific question / general learning / writing X / steelmanning an opponent / pure curiosity)
- Depth warrant: Does this text deserve full deconstruction, a lighter pass, or just a literature note?

Without this, you'll keep running the heavy machinery on inputs that warrant a skim.

## Phase 1: The Epistemic Filters (Deconstruction)

When analysing a text, process it through these filters in sequence to isolate and evaluate the core intellectual material.

[[Linguistic Stripping & Assumption Identification]]

[[The Extended Argument Map]]

[[Epistemic Categorisation]]

[[Structural Integrity (Validity & Soundness)]]

### 2. Missing the Literature Note Layer

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

- Correct framing but mechanically underspecified. "Cluster notes to outline arguments" is exactly the kind of verb-without-object that fails ADHD executive function. What is the _concrete ritual_? My suggestion: when a hub note reaches ~5–7 outbound links on a coherent theme, that's the trigger to draft.

### 3. No Phase 3: Retrieval & Review

The workflow terminates at "drafting new writing." But the system's compounding value is over time: notes you made six months ago informing a question you didn't have yet. You have no cadence for:

- Surfacing—periodic review of orphan notes, unlinked atoms, dead hubs.
- Re-reading—reviewing a structural note and asking "does this still hold?"
- Query-driven retrieval—starting from a new question and walking backwards into the graph.

### 4. No Pruning / Garbage Collection

Notes rot. Claims get contradicted by later evidence. Duplicates accumulate under different phrasings. You have an _entry_ pipeline but no _maintenance_ pipeline. Without one, the Zettelkasten becomes an archive—which is exactly what Phase 2.4 correctly warns against.
