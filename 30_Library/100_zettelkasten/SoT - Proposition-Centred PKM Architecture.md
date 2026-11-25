---
conformant: true
created: 2026-11-16T22:59:14+00:00
modified: 2026-11-17T14:05:00+00:00
prodos:
  kind: sot
  lifecycle: active
  trust: working
project_category: prodos
project_name: ProdOS
status: seed
tags:
  - domain/pkm
  - prodos/sot
  - topic/knowledge-architecture
title: SoT - Proposition-Centred PKM Architecture
type: sot
permalink: llmeon/30-library/100-zettelkasten/so-t-proposition-centred-pkm-architecture
---

## Minimum Viable Understanding (MVU)

A thinking-oriented PKM optimises for **belief revision** and **decision support** rather than raw information retrieval. Propositions (`claim` notes) serve as the centre of gravity, supported by four scaffolding note types (`concept`, `evidence`, `question`, `procedure`), with structural rigour **pulled** by live decisions or contradictions rather than pushed onto every note at capture.

---

## 1. The Five Core Note Types

Not all knowledge is propositional (Ryle's *knowing-how* vs. *knowing-that*; Polanyi's tacit knowledge). To avoid both topic-bucket bloat and proposition-only brittleness, ProdOS centres on propositions supported by four scaffolding types:

| Note Type | Purpose | Minimum Viable Form (Default) |
|:--- |:--- |:--- |
| **Claim** (`claim`) | A proposition held or under test. | Declarative sentence title + 2 lines of "why". |
| **Concept** (`concept`) | A distinction or boundary needed to state claims. | Term + 1–2 sentences carving out what it is and is not. |
| **Evidence** (`evidence` / `source`) | External data, benchmark, or quote (kept separate from personal belief). | Verbatim extract/link + 1 line on which claim it shifts. |
| **Question** (`question`) | An unresolved tension or active problem (`HEAD - …?`). | Question title + what blocks the answer. |
| **Procedure** (`procedure` / `protocol`) | Repeatable operational know-how. | One-screen imperative checklist; zero theory. |

Index notes (`type: map` / MOCs) and Single Sources of Truth (`type: sot`) sit above these five atomic units as navigational entry points and compiled canonical positions, not as raw topical holding buckets.

---

## 2. Pull-Based Escalation (Tier 1 vs. Tier 2)

Pushing full schema ceremony onto every note at capture creates extraneous cognitive load and triggers maintenance avoidance. Rigour is therefore **pulled** only when load-bearing:

- **Tier 1 (Default Claim):** `status: seed` or `draft` — declarative sentence title + 1–3 sentence opening rationale + `epistemic_status`. Zero required falsifiers, `Scope & Conditions`/`Evidence`/`Implications` sections, or typed edges. Every claim promoted into `30_Library/` enters at Tier 1.
- **Tier 2 (Load-Bearing Claim):** Escalate to `status: stable` / `evergreen` and the full schema (`proposition`, `evidence_links`, `contradicts`, `Scope & Conditions`, `Evidence`, `Implications`, `Falsifier` expected, Typed Edges) **only** when a claim:
  1. is consulted for a real decision, or
  2. directly contradicts another note.

  "Falsifier expected" is a convention, not a validator rule: `validate_note_shape.py` still treats the section as optional.

*(Note: "Promoted on second reuse" is intentionally excluded from Tier 2 triggers so that Rule 3's second-touch promotion into `30_Library/` does not collapse Tier 1 into Tier 2.)*

---

## 3. Map vs. Topic Bucket Boundary Test

Index notes (`type: map` / MOCs) may exist sparingly as navigation hubs, but must not decay into passive topical warehouses.

- **The Test:** A Map may contain **only** links and 1-line relational context. The moment a Map contains raw paragraphs, quotes, or unlinked facts, it has decayed into a Topic Bucket and must be split or purged.

---

## 4. SoT Boundary Rule & Transcluded Compilation Pattern

A Single Source of Truth (`type: sot`) is a **compiled argument and synthesis page** built from the five core atomic note types (`claim`, `concept`, `evidence`, `question`, `procedure`), **not** a container for un-extracted prose assertions. Writing standalone claims, definitions, or procedures solely inside an SoT recreates a Topic Bucket under a different name: those assertions cannot be reused, tested, or tracked independently in the justification graph.

To ensure an SoT still reads as a single coherent page without forcing the reader to link-hop across dozens of tabs, SoTs use **Obsidian transclusion**:

1. **Extract First, Compile Second:** Every core proposition, concept distinction, empirical evidence item, or operational procedure belongs in its own atomic note in `30_Library/100_zettelkasten/`.
2. **Transclude in Narrative Order:** Inline those atomic notes into the SoT's sections using `![[Note Title]]` (or `![[Note Title#Heading]]` when only a specific section such as the opening statement or checklist is needed) so the rendered page reads continuously from start to finish.
3. **Connective Framing Only:** Prose authored directly inside the SoT is limited to the MVU summary, section headings, and brief connective transitions that order the argument between transclusions—never un-extracted standalone claims.
4. **Typed Argument & Synthesis Edges:** Record `[depends_on:: [[Claim]]]` for load-bearing premises the SoT's conclusion presupposes, and `[synthesizes:: [[Note Title]]]` for transcluded component notes so `edge_lint.py` and the argument graph can trace which claims the SoT rests on and synthesises.

---

## 5. Operating Rules

1. **No Topic Buckets:** Never create a topical container (e.g., `Networking.md`) to store facts. Create a Tier 1 claim *about* the topic, a concept distinction, or a debugging procedure.
2. **Capture the Delta:** Do not summarise sources. Record only what surprised you, explained a failure, or shifted your prior confidence.
3. **Promote on Second Touch:** Notes stay as low-friction scratchpads in `00_Inbox/` or `20_Thinking/` until reached for a second time or used in a decision, entering `30_Library/` at Tier 1.
4. **Generated, Not Retrieved:** Mechanism content ("X works by Y") enters as a claim I write myself, not as passive topical or reference hoarding. Supporting concepts, questions and sources stay scoped as scaffolding, and exploratory thinking is not procrastination.
5. **Explain Before Checking (load-bearing claims only):** Write the mechanism unaided first, then check sources or LLMs. Record the gap as a dated position entry in `### Scope & Conditions`.
6. **Stuck Points Become Assumptions:** Where the unaided explanation leaned on something it could not justify, add a `[depends_on:: [[Target]]]` edge. If no note exists for the target, stub a Tier 1 claim or question first; never leave a dangling edge (`edge_lint.py` fails on it).
7. **External Adversary:** Each load-bearing claim gets at least one objection I did not write (a person, an LLM prompted to argue against it, or a real-world outcome). Log it under `### Steelman` with its source. Self-critique alone does not surface blind spots. Several LLMs agreeing counts as one data point, because they share priors.
8. **Dated Revisions, Never Overwrite:** When a claim changes or dies, append a dated position entry (what changed, why) under `### Scope & Conditions` and keep prior positions visible. If a new note replaces the claim, use `[revises:: [[Old Note]]]` plus `supersedes` in frontmatter.
9. **Stop Rule:** Stop decomposing once I can state the conclusion and name its weakest link. Legitimate clarification and exploration are not penalised.

---

## 6. Falsifier (90-Day Empirical Test: 2026-11-17 to 2027-02-15)

Tracked via an external Decision Log (1 line per real work/architecture decision):

1. **The Baseline A/B Test:** For the next 5 real architectural or life decisions, query an LLM over raw notes/transcripts first, then consult/write the relevant Claim cards. If the Claim cards do not **alter** the decision over the raw-note LLM answer in at least **2 of the 5 cases**, this architecture is falsified.
2. **The Revision & Usage Threshold:** If, between **2026-11-17 and 2027-02-15**, fewer than **5 real decisions** in the Decision Log cite a vault Claim card, OR if **more time/commits are spent editing PKM schema/linter rules than logging claim updates**, the proposition-centred architecture is falsified as net-negative ceremony.
3. **Method Tripwire:** This practice is working if, by [Leon to fill: date], I can name [Leon to fill: N] claims I've revised or dropped. Count with `rg -c "Dated position" 30_Library/100_zettelkasten` plus `rg "revises::"`.

---

## Working Knowledge & Upstream Grounding

- [[A Thinking PKM Must Be Proposition-Centred Rather Than Topic-Centred]]—_Core thesis claim compiling the rationale, empirical evidence, and 90-day falsifier for this architecture._ [synthesizes:: [[A Thinking PKM Must Be Proposition-Centred Rather Than Topic-Centred]], confidence=high]
- [[Proposition-Centred Notes Create Cognitive Leverage That Topical Notes Lack]]—_Supplies the underlying cognitive mechanism for why declarative propositions outperform topical nouns._ [synthesizes:: [[Proposition-Centred Notes Create Cognitive Leverage That Topical Notes Lack]], confidence=high]
- [[Proposition-Centred Notes Make Superior RAG Chunks for LLM Context Engines]]—_Shows how atomic propositional units improve retrieval precision and context assembly._ [synthesizes:: [[Proposition-Centred Notes Make Superior RAG Chunks for LLM Context Engines]], confidence=high]
- [[Propositions Are the Only Thing That Can Be Wrong]]—_Grounds the epistemic primacy of propositions as the sole units capable of truth, falsity, and revision._ [synthesizes:: [[Propositions Are the Only Thing That Can Be Wrong]], confidence=high]
- [[Claim - Thinking Earns Its Place by Improving Model Fidelity]]—_Scopes ProdOS Kernel Axiom 1 so model-fidelity investments in 30_Library are recognised as valid work._ [depends_on:: [[Claim - Thinking Earns Its Place by Improving Model Fidelity]], confidence=high]
- [[The Atomicity Principle - One Idea Per Note]]—_Provides the atomicity constraint underpinning Tier 1 and Tier 2 claim cards._ [depends_on:: [[The Atomicity Principle - One Idea Per Note]], confidence=high]
- [[SoT - PRODOS Core Specification]]—_Defines the overarching ProdOS Thinking Stream within which this proposition-centred architecture operates._ [extends:: [[SoT - PRODOS Core Specification]], confidence=high]
- [[SoT - Atomic Note Standard (The Proposition Card)]]—_Specifies the concrete structural contract and linter rules for atomic proposition cards (open design tension: §2's lightweight Tier 1 default conflicts with `validate_note_shape.py` requiring `Scope & Conditions`, `Evidence`, and `Implications` on all new `100_zettelkasten/` notes)._ [depends_on:: [[SoT - Atomic Note Standard (The Proposition Card)]], confidence=high]
- [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]—_Defines the frontmatter envelope and the five knowledge-node schemas._ [depends_on:: [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]], confidence=high]
- [[SoT - Knowledge Compiler (Argument Graph Spec)]]—_Relies on proposition-centred claims and typed edges to audit support, contradictions, and load-bearing premises._ [depends_on:: [[SoT - Knowledge Compiler (Argument Graph Spec)]], confidence=high]
- [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]]—_Separates low-friction capture from propositional clarification to prevent premature formalisation._ [depends_on:: [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]], confidence=high]