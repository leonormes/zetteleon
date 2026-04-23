---
title: "Epistemic filters and knowledge architecture workflow"
source: "https://claude.ai/chat/97e9de35-b69d-4508-b4ea-a7c45d2b6cd2"
captured: "2026-04-23T12:18:30+01:00 2026-04-23T12:18:30+01:00"
status: "processing"
tags:
  - "input"
type: "head"
---
## Raw Output / Content
**You**

I am developing a workflow. Help me iterate and improve upon it Phase 1: The Epistemic Filters (Deconstruction) When analysing a text, process it through these filters in sequence to isolate and evaluate the core intellectual material.

1. Linguistic Stripping & Assumption Identification: \* Action: Strip away rhetorical noise, jargon, and attitude indicators to isolate the raw declarative statements.
	- Enhancement: Actively identify the author's unstated assumptions. Often, the logical starting point of a text is entirely implicit. Bring these underlying premises to the surface before moving to the next filter.
2. The Extended Argument Map: \* Action: Identify the Claim (conclusion) and Grounds (evidence).
	- Enhancement: Expand beyond the basic Warrant to include the full Toulmin model framework. Identify the Backing (the deeper authority supporting the warrant), note any Qualifiers (the degree of certainty, such as "presumably" or "usually"), and search for Rebuttals (conditions under which the claim would not hold true).
3. Epistemic Categorisation: \* Action: Separate descriptive facts (what is) from normative judgements (what ought to be).
	- Enhancement: Distinguish between field-invariant elements (the universal logical structure of the argument) and field-dependent elements (the domain-specific criteria required to actually prove the claim).
4. Structural Integrity (Validity & Soundness): \* Action: Test the logical flow and the truth of the premises.
	- Enhancement: Apply the correct standard of proof. For deductive arguments, test for strict validity and soundness. For inductive or explanatory arguments, test for logical strength, cogency, and falsifiability (whether it is possible to specify an observable outcome that could prove the explanation false). Phase 2: Knowledge Architecture (Synthesis) Once the text is filtered, translate the surviving ideas into your own system, ensuring a strict separation between objective facts and subjective context.
5. Cleave into Atomic Notes: \* Action: Write each verified, objective claim as a single, indivisible idea.
	- Enhancement: Enforce a "Binary Category Invariant." Atomic notes must be entirely context-free—acting purely as building blocks (e.g., definitions, verifiable statements). They should be written in your own words to ensure true comprehension, not simply copied.
6. Construct Structural / Hub Notes: \* Action: Rebuild the context that was stripped away during the cleaving process.
	- Enhancement: Create Structural Notes (or map notes) to preserve the original narrative, argument, or sequence. Use these notes to link your new atomic facts together using typed links (e.g., Note A `[supports]` Note B). The Structural Note provides the architecture; the Atomic Notes provide the bricks.
7. Stress-Test & Connect (The Idea Compass): \* Action: Compare new notes against existing ones to detect contradictions or paradoxes.
	- Enhancement: Map the new proposition along four axes: its origins (where did this idea come from?), its applications (where does this lead?), its allied concepts (what is similar?), and its competitors (what opposes this?).
8. Iterate Towards Output: \* Action: Allow the system to act as a dialogue partner.
	- Enhancement: Treat this network not as an archive for storage, but as an active workspace. As connections form, cluster these notes to outline original arguments, transitioning seamlessly from note-making to drafting new writing.

---

## Assessment

You've built a disciplined pipeline that fuses **Toulmin argumentation** with **Luhmann/Ahrens-style note architecture**. The bones are solid. The critique below targets four structural gaps and some phase-level tightening — not cosmetic issues.

The workflow's main weakness is that it is **linear where sense-making is recursive**, and **assumes an argumentative text where many inputs aren't**. It also ends where the most valuable work of a Zettelkasten begins: retrieval over time.

---

### Four structural gaps

#### 1\. Missing Phase 0: Telos / Triage

You have no pre-filter. Every text gets the full four-stage deconstruction regardless of stakes. This is where your ADHD task-initiation problem bites hardest: the activation energy to run Phase 1.1–1.4 on an article you vaguely want to read is enormous. You'll either over-process or skip entirely.

**Add a Phase 0 with two questions:**

- **Purpose:** Why am I engaging this text? (Answering a specific question / general learning / writing X / steelmanning an opponent / pure curiosity)
- **Depth warrant:** Does this text deserve full deconstruction, a lighter pass, or just a literature note?

Without this, you'll keep running the heavy machinery on inputs that warrant a skim.

#### 2\. Missing the Literature Note layer

Your pipeline jumps from **filtered text → atomic notes**. Ahrens is explicit that there should be an intermediate layer: the **literature note** — a short summary, in your own words, bound to the source. It preserves the *reading experience* before you shatter it into context-free atoms.

You'll want this because:

- Atoms lose the shape of the original. A literature note keeps it, once, in one place.
- It's the natural artefact to cite from later (source + page + your paraphrase).
- It's a cheaper output for low-stakes texts that don't warrant atomisation.

#### 3\. No Phase 3: Retrieval & Review

The workflow terminates at "drafting new writing." But the system's compounding value is **over time**: notes you made six months ago informing a question you didn't have yet. You have no cadence for:

- **Surfacing** — periodic review of orphan notes, unlinked atoms, dead hubs.
- **Re-reading** — reviewing a structural note and asking "does this still hold?"
- **Query-driven retrieval** — starting from a new question and walking backwards into the graph.

#### 4\. No pruning / garbage collection

Notes rot. Claims get contradicted by later evidence. Duplicates accumulate under different phrasings. You have an *entry* pipeline but no *maintenance* pipeline. Without one, the Zettelkasten becomes an archive — which is exactly what Phase 2.4 correctly warns against.

---

### Phase-by-phase tightening

#### Phase 1.1 — Linguistic Stripping

- **Risk:** in some genres, the rhetoric *is* the content (political speeches, literary criticism, advertising). Stripping is lossy, not neutral. Add a qualifier: this step is valid for *argumentative prose*, invalid for rhetoric-as-object-of-study.
- **Good move:** surfacing unstated assumptions. Consider adding an explicit **steelman** step before judgement — construct the strongest version of the author's case before you test it. Protects you from dismissing ideas you didn't fully engage.

#### Phase 1.2 — Toulmin

- Toulmin fits argumentative prose well. It fits poorly for: mathematical proofs, narrative texts, empirical reports with statistical claims, reference material. State the scope explicitly.
- **Consider adding:** a note on **argument mood** — is this a deductive argument, an inference to the best explanation, an empirical generalisation, or a normative claim? Different moods need different tests in 1.4.

#### Phase 1.3 — Epistemic Categorisation

- **Field-invariant vs field-dependent** is good but abstract. Make it operational: "What would a qualified practitioner in this field accept as evidence?" This is where you catch arguments that are logically valid but empirically vacuous in their domain.
- Add a third category beyond descriptive/normative: **procedural** claims (how-to / method claims), which have their own validity criteria (reproducibility, effectiveness).

#### Phase 1.4 — Structural Integrity

- Binary validity/soundness is too blunt for most real-world claims. Add **Bayesian framing**: what was my prior belief? How much does this evidence update it, and in which direction? What would disconfirm it?
- Falsifiability is listed only for inductive/explanatory arguments. Apply it to your own notes too — "what observation would force me to retract this atomic note?"

#### Phase 2.1 — Atomic Notes

- " **Binary Category Invariant** " — I'd challenge this term. Atomic notes are not *context-free*; they are *context-minimal*. A definition has a domain. A claim has scope conditions. Forcing "entirely context-free" will either produce notes that are too vague to be useful, or notes that lie by omission. Reframe as: " **self-contained** — readable in isolation without reference to source."
- **Enforce one idea per note, but also one *level* per note.** A note mixing a definition and an implication violates atomicity just as badly as one mixing two claims.

#### Phase 2.2 — Structural Notes with Typed Links

- You mention typed links but without an ontology. Link types proliferate chaotically unless constrained. **Define a small fixed vocabulary**, e.g.:
	- `[supports]`, `[contradicts]`, `[refutes]`
		- `[extends]`, `[generalises]`, `[instantiates]`
		- `[depends-on]`, `[precedes]`
		- `[analogous-to]`, `[competes-with]`
- Anything outside this vocabulary is a smell — either the link type should be added deliberately, or the relationship belongs in prose inside a structural note.

#### Phase 2.3 — Idea Compass

- Four axes (origins, applications, allies, competitors) miss a temporal dimension: **trajectory**. Where has this idea come from *and where is it going*? What are the currently open problems in its research programme? This matters most for ideas in active flux (software architecture, ML, policy) rather than settled ones.

#### Phase 2.4 — Iterate Towards Output

- Correct framing but mechanically underspecified. "Cluster notes to outline arguments" is exactly the kind of verb-without-object that fails ADHD executive function. What is the *concrete ritual*? My suggestion: when a hub note reaches ~5–7 outbound links on a coherent theme, that's the trigger to draft.

---

### Applicability limits

Name them explicitly in the doc. This workflow is **optimised for argumentative non-fiction prose**. It needs modification or replacement for:

| Text type | What breaks |
| --- | --- |
| Mathematical / formal proofs | 1.4 is trivially satisfied; the interesting work is elsewhere |
| Fiction / narrative | No claim–grounds structure to map |
| Poetry | 1.1 strips the content |
| Empirical papers with statistics | Need base rates, priors, effect sizes — 1.4 is too coarse |
| Reference material | No argument; skip Phase 1 entirely, go straight to atoms |
| Rhetoric as object-of-study | 1.1 is wrong; rhetoric is the data |

---

### Revised skeleton

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

### Immediate next action

**Open your workflow document and add Phase 0 as three bullet points**: Purpose, Depth warrant, Text-type check.

That's it for this sitting. Don't try to revise the whole thing — the triage step is the highest-leverage addition because it gates everything else and directly attacks your activation-energy problem. Everything else can iterate in later sessions.

---

**You**

I have an llm that has access to my books about writing and knowledge. Give me a prompt to direct it to surface the ideas and rules about propositions. I want the llm to act as a teacher and guide helping becomes expert in writing/reading propositions and uncovering assumptions.

---

**Claude**

## Prompt Design

Before the prompt itself, two framing notes so you can tune it later:

- **Why this shape:** your LLM has RAG over your library, so the prompt's job is to *constrain retrieval and pedagogy*, not to supply content. I've pushed hard on: citing sources, refusing to extrapolate beyond them, and Socratic rather than lecture mode — because the failure mode of teacher-LLMs is confident generic pedagogy that drifts from your actual corpus.
- **Why Socratic over exposition:** you already absorb theory well (per your own self-description). The bottleneck is *doing* — writing and reading propositions in the wild. A teacher that quizzes and critiques your attempts will close the knowing–doing gap faster than one that explains.

---

### The Prompt

```markdown
# Role

You are my tutor in the craft of **propositions** — both reading them (extracting, isolating, and stress-testing the propositions embedded in texts) and writing them (composing clear, atomic, defensible propositions of my own). Your sole source of authority is the library of books on writing, reasoning, and knowledge work that you have access to. You are not a generic writing coach; you are a librarian-tutor for *this specific corpus*.

# Mission

Make me expert in:

1. **Identifying** propositions inside prose — including those that are implicit, compound, or disguised as rhetoric.
2. **Surfacing unstated assumptions** that a proposition depends on.
3. **Writing** propositions that are atomic, self-contained, and testable.
4. **Distinguishing** propositions from adjacent constructs (claims, assertions, premises, hypotheses, theses, statements of fact, normative judgements) as the corpus defines them — not as general usage defines them.

# Source Discipline (hard rules)

- **Cite or abstain.** Every rule, definition, or principle you teach must be attributed to a specific book, chapter, and — where possible — page or section. Format: *Author, Title, §Section / p.N*.
- **Corpus-first, not memory-first.** If a concept is in the corpus, teach it from the corpus even if you "know" it from training. If a concept is *not* in the corpus, say so explicitly: "This is not covered in your library; I can flag it as a gap but won't teach it as if it were."
- **Reconcile, don't homogenise.** When two books disagree (e.g. Adler vs. Ahrens vs. Weston vs. a logic text on what counts as a proposition), present the disagreement. Do not average their positions into mush.
- **Quote sparingly, paraphrase by default.** Short quoted phrases are fine for precise definitions; longer passages should be paraphrased with citation.

# Pedagogy (how you teach)

Default to **Socratic and diagnostic**, not expository. Specifically:

- **Start by asking, not telling.** When I bring a text or a proposition, your first move is usually a question that reveals what I already see and what I'm missing.
- **One concept per exchange.** Do not dump frameworks. Surface one idea, let me work with it, then introduce the next.
- **Make me produce.** Every session should end with me having *written or rewritten* at least one proposition, or *extracted* at least one from a text.
- **Critique, don't praise.** When I produce work, your default stance is rigorous critique against the corpus's own standards. Reserve approval for genuinely clean work.
- **Name the move.** When you teach a technique, name it and cite its origin, so I build a working vocabulary tied to sources.

# Session Modes

Offer me these modes at the start of any session, and switch on request:

1. **Extract** — I paste a passage; you walk me through isolating its propositions and unstated assumptions, Socratically.
2. **Compose** — I state an idea I want to express; you coach me through writing it as a clean proposition, iterating on my drafts.
3. **Diagnose** — I paste a proposition (mine or someone else's); you probe it for atomicity, scope, testability, hidden compounds, and buried assumptions.
4. **Contrast** — I name two adjacent constructs (e.g. proposition vs. claim); you map how each book in my library distinguishes them, and where they conflict.
5. **Drill** — You generate short exercises from the corpus (propositions to rewrite, passages to dissect, assumption-hunts) at graded difficulty.
6. **Survey** — You give me a map of what the corpus collectively says about propositions, organised by book, with the disagreements marked.

Default to **Extract** or **Compose** unless I specify.

# Working Method

For any proposition under examination, work through these lenses *as the corpus frames them* — citing which book contributes which lens:

- **Atomicity** — is this one idea or several smuggled together?
- **Self-containment** — is it intelligible without its source context?
- **Scope** — universal, existential, conditional, local?
- **Mood** — descriptive / normative / procedural / definitional?
- **Warrant** — what would have to be true for this to hold?
- **Assumption set** — what is presupposed but unstated?
- **Falsifiability / testability** — what would count as evidence against it?
- **Rhetorical residue** — what attitude, hedging, or emphasis is doing work that isn't part of the proposition itself?

Do not march through all eight every time. Pick the lens that matters for the current text, and tell me why you picked it.

# Output Style

- British English.
- Markdown with clear hierarchy — no walls of prose.
- Keep responses compact. Depth over length.
- End every substantive response with **one** of: a question for me, a small exercise, or a concrete next action. Never both lecture and leave me without a move.
- When you cite, use footnote-style inline: *(Adler, How to Read a Book, Ch.9)*.

# Opening Move

On my first message in a session, do the following — and only this:

1. Ask me which **mode** I want (Extract / Compose / Diagnose / Contrast / Drill / Survey).
2. Ask me what I'm bringing (a text, a draft proposition, a topic, or "teach me from scratch").
3. Do **not** produce content yet.

After I answer, begin.
```

---

### Immediate next action

**Paste the prompt into your LLM as a system prompt or the first message of a fresh thread**, then reply to its opening question with: *"Survey — teach me what the corpus says about what a proposition actually is, and where the books disagree."*

That survey pass will tell you two things at once: (a) what your library actually contains on this topic, and (b) whether the prompt's source-discipline rules are holding. If the LLM drifts into generic content or skips citations on that first run, tighten the Source Discipline section before doing any real work with it.
