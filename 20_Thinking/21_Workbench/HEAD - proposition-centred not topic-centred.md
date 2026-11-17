---
aliases: ["PKM should probably be proposition-centered, not topic-centered", "PKM should probably be proposition-centred, not topic-centred"]
conformant: false
created: 2026-04-23T15:27:21+00:00
epistemic_status: hypothesis
modified: 2026-11-17T07:09:41+00:00
own_words: false
permalink: llmeon/30-library/100-zettelkasten/pkm-should-probably-be-proposition-centred-not-topic-centred
project_category: prodos
project_name: ProdOS
project_status: active
status: conjecture
tags: [prodos/llmeon, topic/knowledge-architecture]
title: PKM should probably be proposition-centred, not topic-centred
type: claim
---


### 1. Steel-Manned Statement

<!-- TODO: Leon—replace with your own 1-2 sentence formulation, then set own_words: true -->

For my engineering and architectural work, organising my vault around testable propositions ("What do I think is true about $X$, and why?") yields better decisions and model revisions than organising around topical buckets ("What information have I collected about $X$?"), provided structural rigour is pulled by live decisions rather than pushed onto every note at capture.

### 2. Evidence & Vault Observations (Why I Hold This)

- Positive Vault Instance (2026-08-29—Axiom Retirement): Converting ProdOS Kernel Axiom 1 (_"If a note doesn't help you act, it is noise"_) into an explicit proposition (`[[Claim - A Note That Does Not Help You Act Is Noise]]`) exposed a direct contradiction with the Zettelkasten layer, leading to its formal retirement and replacement by `[[Claim - Thinking Earns Its Place by Improving Model Fidelity]]`. In a topic-bucket wiki, both contradictory statements would have coexisted silently.
- Negative Vault Instance (2026-11—The Schema-Over-Use Trap): My `30_Library` audit revealed 58 ProdOS structural/governance notes (`sot`, `map`, `protocol`) supporting only 6 `claim` cards, alongside a habit of using LLMs to tidy notes for a dopamine fix while doing real thinking in ephemeral chat windows. This demonstrates that heavy upfront schema ceremony causes avoidance and productive procrastination.
- External Grounding (Cognitive Load Theory): Offloading _extraneous_ load (formatting, filing) helps working memory, but offloading _germane_ load (translating ideas into personal claims and resolving contradictions) causes metacognitive laziness and the fluency illusion (Bastani et al., 2024; Fan et al., 2025).

### 3. Mechanism: Proposition-Centred (Not Proposition-Only) & Pull-Based Rigour

A personal wiki optimises for retrieval, which LLMs already handle over raw text. A thinking PKM optimises for belief revision and decision support.

However, not all knowledge is propositional. Following Gilbert Ryle (_knowing-how_ vs. _knowing-that_) and Michael Polanyi (tacit knowledge), propositions are the centre of gravity, supported by four scaffolding types:

| Note Type | Purpose | Minimum Viable Form (Default) |
|:--- |:--- |:--- |
| Claim (`claim`) | A proposition I hold or am testing. | Declarative sentence title + 2 lines of "why". |
| Concept (`concept`) | A distinction or boundary needed to state claims. | Term + 1–2 sentences carving out what it is and is not. |
| Evidence (`evidence` / `source`) | External data, benchmark, or quote (kept separate from my belief). | Verbatim extract/link + 1 line on which claim it shifts. |
| Question (`question`) | An unresolved tension or active problem (`HEAD - …?`). | Question title + what blocks the answer. |
| Procedure (`procedure` / `protocol`) | Repeatable operational know-how. | One-screen imperative checklist; zero theory. |

#### The Pull-Based Escalation Rule (Avoiding Extraneous Load)

- Tier 1 (Default Claim): Title (declarative sentence) + 2 lines of rationale. Zero required falsifiers or typed edges.
- Tier 2 (Load-Bearing Claim): Escalate to the full schema (Counter-positions, Crux, Falsifier, Dated Position, Typed Edges) only when a claim is consulted for a real decision, promoted on second reuse, or directly contradicts another note.

#### Map vs. Topic Bucket Boundary Test

Index notes (`type: map` / MOCs) may exist sparingly as navigation hubs. The Test: A Map may contain only links and 1-line relational context. The moment a Map contains raw paragraphs, quotes, or unlinked facts, it has decayed into a Topic Bucket and must be split or purged.

### 4. Counter-Positions (Steel-Manned Objections)

1. LLM + Raw Notes Baseline: Modern long-context LLMs and semantic search over raw, uncurated markdown notes or chat transcripts may deliver 90% of the decision support at 5% of the maintenance cost of curating atomic claim cards and typed edges.
2. System-Building as Cognitive Substitution: Maintaining a proposition-centred ontology (`validate_note_shape.py`, `edge_lint.py`, frontmatter contracts) is intellectually seductive to a platform architect and easily substitutes for actual thinking and shipping.
3. Maintenance Decay: Even with a tiered schema, auditing falsifiers and updating dated positions requires ongoing epistemic hygiene that often collapses under high work/family load.

### 5. Crux

Does the Tier 1 → Tier 2 pull model (promoting and formalising claims only when reused or consulted in a live decision) beat raw-note LLM search in real architectural/personal decisions without triggering maintenance burnout?

### 6. Falsifier (90-Day Empirical Test: 2026-11-17 to 2027-02-15)

Tracked via an external `[[Decision Log]]` (1 line per real work/architecture decision):

1. The Baseline A/B Test: For the next 5 real architectural or life decisions, query an LLM over raw notes/transcripts first, then consult/write the relevant Claim cards. If the Claim cards do not alter or sharpen the decision over the raw-note LLM answer in at least 2 of the 5 cases, this claim is falsified.
2. The Revision & Usage Threshold: If, between 2026-11-17 and 2027-02-15, fewer than 5 real decisions in `[[Decision Log]]` cite a vault Claim card, OR if more time/commits are spent editing PKM schema/linter rules than logging claim updates, the proposition-centred architecture is falsified as net-negative ceremony.

### 7. Operating Rules

1. No Topic Buckets: Never create `Networking.md` to store facts. Create a Tier 1 claim _about_ networking, a concept distinction, or a debugging procedure.
2. Capture the Delta: Only record what surprised you, explained a failure, or shifted your prior confidence.
3. Promote on Second Touch: Notes stay as low-friction scratchpads in `00_Inbox/` or `20_Thinking/` until you reach for them a second time or use them in a decision.

### 8. Dated Position

- 2026-04-23: ~0.75 (hypothesis)—Initial distinction between topic wikis and belief-revision PKMs drafted (`PKM ProdOS`).
- 2026-08-29: ~0.80 (working belief)—Upward update after formalising and retiring Kernel Axiom 1 (`[[Claim - A Note That Does Not Help You Act Is Noise]]`) proved that propositional framing catches real system contradictions.
- 2026-11-16: ~0.65 (conjecture under test)—Downward update after `30_Library` audit showed 58 structural/governance notes vs. only 6 claim cards, and after adversarial review exposed that pushing full schema rigour onto every note causes maintenance avoidance. Shifted to a pull-based tiered model pending the 90-day `[[Decision Log]]` test.

---

### Related Knowledge

- [[Proposition-Centred Notes Create Cognitive Leverage That Topical Notes Lack]]—_Supplies the underlying cognitive mechanism for why declarative propositions outperform topical nouns._ [depends_on:: [[Proposition-Centred Notes Create Cognitive Leverage That Topical Notes Lack]]]
- [[Claim - Thinking Earns Its Place by Improving Model Fidelity]]—_Explains why testing beliefs in 30_Library is valid work even when no immediate GTD task is generated._ [depends_on:: [[Claim - Thinking Earns Its Place by Improving Model Fidelity]]]
- [[SoT - Atomic Note Standard (The Proposition Card)]]—_Defines the structural contract that must be updated to support Tier 1 (2-line default) vs Tier 2 (full schema) claims._ [contrasts_with:: [[SoT - Atomic Note Standard (The Proposition Card)]]]

### PKM Should Probably Be Proposition-centred, not Topic-centred

A personal wiki is mostly about "What is X?" and "What facts do I have about X?". A thinking-oriented PKM is more like "What do I think is true about X?" and "How confident am I?".

#### The Key Shift

Instead of organising around subjects, organise around beliefs, questions, models, and evidence. Organize around _propositions_.

##### The Five Core Note Types

To eliminate taxonomy bloat and infrastructure toil, ProdOS enforces exactly five note types:

| Note Type | Purpose | Example |
|:--- |:--- |:--- |
| Claim | A verifiable proposition or belief. The primary unit. | "Packet traces usually outperform dashboards for root-cause analysis." |
| Concept | A definition or distinction needed for thought. | "Congestion control", "epistemic status", "service mesh". |
| Evidence | Why you believe a claim (quotes, data, benchmarks). | A quote from a book, a benchmark result, or an incident log. |
| Question | An unresolved tension or uncertainty. | "When does eBPF actually reduce debugging clarity?" |
| Procedure | Repeatable, binary "know-how" (Protocols). | "How to debug DNS-01 cert-manager failures." |

Note on Maps: Index notes or Maps of Content (MOCs) may exist sparingly to serve as entry points, but they are not "knowledge nodes"—they are just maps.

#### Operating Rules

1. No Topic Buckets: Do not create a note called "Networking" to dump information into. Create claims _about_ networking.
2. Sharpen the Signal: When reading, only capture claims that surprise you, challenge your thinking, or explain real-world failures.
3. Computed Truth: A note should only exist if it sharpens a concept, records a claim, preserves evidence, captures a question, or encodes a useful procedure.

#### Summary

> A PKM is a belief revision system, not an information warehouse.

By sticking to these five types, you ensure that your system remains a "Runtime Environment for Thought" rather than a stagnant database of facts.

[supports:: [[Proposition-Centred Notes Create Cognitive Leverage That Topical Notes Lack]], strength=4, confidence=high]
---

aliases:

  - PKM should probably be proposition-centred, not topic-centred
  - PKM should probably be proposition-centered, not topic-centered
conformant: true
created: 2026-04-23T15:27:21+00:00
epistemic_status: working-belief
modified: 2026-11-16T22:12:00+00:00
own_words: false
permalink: llmeon/30-library/100-zettelkasten/a-thinking-pkm-must-be-proposition-centred-rather-than-topic-centred
project_category: prodos
project_name: ProdOS
project_status: active
status: evergreen
tags:
  - topic/knowledge-architecture
  - prodos/llmeon
title: A thinking PKM must be proposition-centred rather than topic-centred
type: claim

---

### A Thinking PKM Must Be Proposition-Centred Rather Than Topic-Centred

#### 1. Steel-Manned Statement

<!-- TODO: Leon—rewrite this single sentence in your own words and flip own_words: true -->

A personal knowledge system designed for reasoning and decision-making must organise around falsifiable propositions ("What do I currently believe is true about $X$, why, and what would prove me wrong?") rather than topical buckets ("What information have I collected about $X$?").

#### 2. Why I Find This Plausible (Evidence & Provenance)

A personal wiki optimises for retrieval, asking _"What is X?"_ and _"What facts do I have about X?"_ In an era where LLMs make raw fact retrieval trivial, hoarding undigested topic summaries produces warehouse bloat and an illusion of competence (the fluency illusion).

A thinking-oriented PKM functions as an active belief revision system. It optimises for clarification, contradiction detection, synthesis, and model fidelity by asking:

- Stance: What do I think is true about $X$?
- Provenance & Rationale: Why do I think that, and is my confidence grounded in evidence or mere emotional resonance?
- Credence: How confident am I?
- Update Condition: What specific observation or argument would change my mind?

#### 3. Mechanism: Proposition-Centred, Not Proposition-Only

Propositions are the primary bearers of truth and falsity—because they are arguable, refinable, testable, and composable into larger arguments—but not all knowledge is propositional:

- Compositional Scaffolding (Russell): Propositions cannot exist without well-defined constituent Concepts. Even if propositions are the centre of gravity, concepts remain compositionally fundamental.
- Embodied Know-How (Ryle & Polanyi): Gilbert Ryle's distinction between _knowing-that_ (propositional) and _knowing-how_ (procedural), alongside Michael Polanyi's _tacit knowledge_, shows that operational mastery cannot be reduced purely to declarative sentences.

If a vault is _topic-centred_, it decays into a passive junk drawer of unexamined highlights. If a vault is _proposition-only_, it becomes brittle—losing shared vocabulary, procedural execution, and unresolved ambiguity. Therefore, propositions must act as the centre of gravity, supported by four scaffolding note types:

| Functional Note Type | Epistemic Role | Cognitive Question Answered | Concrete Example |
|:--- |:--- |:--- |:--- |
| Claim (`claim`) | Primary truth-bearing unit; a falsifiable conjecture. | _"What do I believe is true, and what would falsify it?"_ | "Packet traces outperform dashboards for root-cause analysis of opaque network failures." |
| Concept (`concept`) | Compositional definition or boundary distinction needed to state claims. | _"What exact distinction does this term carve out?"_ | "Queueing delay vs. propagation delay", "Epistemic status", "Relative realism". |
| Evidence (`evidence` / `source`) | Empirical grounding or external argument (never auto-promoted to personal belief). | _"What observation, benchmark, or source shifts my credence?"_ | Post-mortem packet capture log, benchmark table, or literature extract. |
| Question (`question`) | Explicit epistemic tension or active workbench problem (`HEAD - …?`). | _"What unresolved crux blocks my model?"_ | "When does eBPF instrumentation reduce rather than increase debugging clarity?" |
| Procedure (`procedure` / `protocol`) | Repeatable binary know-how and operational execution. | _"How do I reliably execute this sequence under load?"_ | "How to debug DNS-01 cert-manager failures." |

_Structural & Compilation Layers:_ Maps (`type: map` / MOCs) and Single Sources of Truth (`type: sot`) sit above these five atomic units as navigational entry points and compiled canonical positions, not as raw topical holding buckets.

#### 4. Counter-Positions

- Premature Formalisation Kills Capture Velocity: Forcing nascent thoughts into rigid propositional schemas at the moment of capture creates high germane cognitive friction, triggering initiation paralysis or turning note-making into bureaucratic form-filling.
- Spatial & Pre-Propositional Intuition: Early-stage sensemaking (e.g., 4D spatial mapping on a canvas, sketching, or exploratory workbench thinking) often operates through visual clusters and loose associations before a thinker can articulate a crisp declarative sentence.

#### 5. Crux

Whether the system enforces stage-separation between low-friction capture (`00_Inbox/` and `20_Thinking/21_Workbench/` in Stage 1 Generate) and strict propositional formalisation (`30_Library/` in Stage 2 Clarify). If propositional rigour is demanded at Stage 1, the system stalls; if it is enforced only upon promotion to the permanent library, cognitive leverage compounds without capture paralysis.

#### 6. Falsifier

This architectural claim is falsified if, over a 90-day audit cycle, maintaining atomic claim cards with explicit falsifiers and typed edges fails to produce measurable belief revisions (logged in `Dated Position` trails) or higher-fidelity engineering/personal decisions compared to querying raw, uncurated notes and LLM transcripts via semantic search.

#### 7. Operating Rules (The Six-Gate Filter)

1. Kill Topic Buckets: Never create a container note titled `Networking.md` to dump facts into. Formulate claims _about_ networking, define the _concepts_ required to state them, or write a _procedure_ to debug them.
2. Capture the Delta, Not the Summary: When reading or conversing with an LLM, do not summarise what the source said. Record only the likelihood delta—the specific mechanism, surprise, or failure mode that updated your prior belief.
3. The Six-Question Admission Gate: Before promoting any note into `30_Library/`, ask:
   1. Is this a claim I am willing to expose to falsification?
   2. If not, is it a concept I need in order to formulate claims?
   3. If not, is it evidence that shifts credence on a claim?
   4. If not, is it an open question worth holding in tension?
   5. If not, is it a reusable procedure?
   6. If none of these, why am I keeping it?

#### 8. Dated Position

- 2026-04-23: Initial working belief (~0.75) established during early ProdOS taxonomy design (`PKM ProdOS`).
- 2026-10-22: Condensed into 5-type operational summary inside `30_Library/200_Projects/`.
- 2026-11-16: Refactored into full v5.0 Claim schema (~0.85 working belief); integrated Ryle/Polanyi/Russell non-propositional scaffolding, Popperian/Bayesian delta-capture rules, and Stage 1/Stage 2 cognitive loop separation.

#### 9. Open Threads

- > Open threads: [[HEAD - How should multi-hop confidence propagation weight procedural vs propositional dependencies in the Knowledge Compiler?]]

---

#### Related Knowledge

- [[Proposition-Centred Notes Create Cognitive Leverage That Topical Notes Lack]]—_Downstream thesis detailing why declarative claim titles outperform topical nouns during graph synthesis._ [supports:: [[Proposition-Centred Notes Create Cognitive Leverage That Topical Notes Lack]], strength=5, confidence=high]
- [[Claim - Thinking Earns Its Place by Improving Model Fidelity]]—_Scopes ProdOS Kernel Axiom 1 so non-immediately-actionable proposition cards in 30_Library are recognised as model-fidelity investments rather than noise._ [depends_on:: [[Claim - Thinking Earns Its Place by Improving Model Fidelity]], strength=5, confidence=high]
- [[SoT - Atomic Note Standard (The Proposition Card)]]—_Operationalises this claim into the vault's concrete structural contract and `validate_note_shape.py` linter rules._ [implements:: [[SoT - Atomic Note Standard (The Proposition Card)]], strength=5, confidence=high]
- [[SoT - Knowledge Compiler (Argument Graph Spec)]]—_Relies on proposition-centred claims and typed edges to expose load-bearing premises and contradictions across the graph._ [supports:: [[SoT - Knowledge Compiler (Argument Graph Spec)]], strength=4, confidence=high]
- [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]]—_Resolves the capture-friction counter-position by separating Stage 1 (Goldberg generation) from Stage 2 (Zinsser propositional clarification)._ [depends_on:: [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]], strength=4, confidence=high]

## Verdict

The architecture is sound, but the note fails its own standard. It argues for evidence-grounded, falsifiable beliefs, yet it contains no evidence, its falsifier can't fail, and its credence rose without an observation. It is not evergreen yet.

### Major Issues

- §2 holds no evidence. It is all rationale: no observation, source or instance from your own vault. By your own Stance/Provenance test, this is closer to "emotional resonance" than grounding.
- Credence went from 0.75 to 0.85 on a refactor. The 2026-11-16 entry logs added philosophers and schema, not anything observed, which breaks Rule 2 (capture the delta). What did you see between April and November that should move the number?
- The falsifier is unfalsifiable as written.
    - "Measurable" has no threshold, and "higher-fidelity decisions" has no measure.
    - The 90-day cycle has no start date.
    - The comparison arm (semantic search over raw notes) isn't being run, so there is no baseline.
    - The Dated Position trails are generated by the system under test, so it marks its own homework.
- The claim and the test don't match. The title says a thinking PKM "must" (universal), while the falsifier is one person over 90 days. The alias "should probably be" is the honest version at 0.85.
- The metadata contradicts itself. `status: evergreen` and `conformant: true` sit alongside `own_words: false` and a live TODO.

### Weaker Spots

- The counter-positions are soft. Both are about capture friction, which §5 then resolves. Stronger ones are missing:
    - Maintenance cost: falsifiers plus typed, scored edges on every note.
    - System-building as a substitute for thinking.
    - "LLM over raw notes is good enough", which is currently hidden in §6.
- Nothing polices Maps against buckets. What test stops a MOC becoming `Networking.md` under another name?
- The edge scores carry no signal. All five are strength 4–5 with confidence high. The first `supports` edge may also be reversed: the description reads as that note supporting this one.
- Terminology:
    - "Germane cognitive friction" should be _extraneous_; germane load is the useful kind.
    - Russell's constituents are objects and universals, not quite "Concepts". I'm less sure this matters for your purposes.
    - "Six-Gate Filter" heads three rules.

### What Would Change My view

One logged case where a claim card's falsifier fired and changed a real decision. That alone would justify 0.85.

### Next Action

In §6, replace "over a 90-day audit cycle" with a start date and a pass number, e.g. "from 2026-11-17, fewer than N logged revisions = falsified". You pick N.

## Verdict

This is ready to run. There are two real errors, both one-phrase fixes. The evidence section, the downward update to 0.65 and the dated falsifier are all honest now.

### The Two Fixes

- Tier 1 collapses into Tier 2. Rule 3 says a note enters the library on second touch, but the Tier 2 trigger also includes "promoted on second reuse". As written, every note arriving in `30_Library` is immediately Tier 2, so the lightweight default never exists. Delete "promoted on second reuse" from the Tier 2 triggers and leave decision use and contradiction.
- Falsifier 1 can barely fail. A second pass at any decision will almost always "sharpen" it, and you are the judge. Cut "or sharpen" so the bar is that the card _altered_ the decision in 2 of 5.

### One Caveat

I haven't checked the two citations in §2 against the papers. Both exist and are about LLM offloading harming learning, which fits, but confirm the wording before you lean on them.

Everything else I'd leave alone until the Decision Log has entries.

### Next Action

In the Tier 2 line, delete the words "promoted on second reuse,".
