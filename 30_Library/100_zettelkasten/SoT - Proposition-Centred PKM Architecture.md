---
conformant: true
created: 2026-11-16 22:59:14+00:00
modified: 2026-11-16 22:59:14+00:00
prodos:
  kind: sot
  lifecycle: active
  trust: working
project_category: prodos
project_name: ProdOS
sources:
  - "[[HEAD - proposition-centred not topic-centred]]"
status: draft
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

- **Tier 1 (Default Claim):** Declarative sentence title + 2 lines of rationale. Zero required falsifiers or typed edges. Every claim promoted into `30_Library/` enters at Tier 1.
- **Tier 2 (Load-Bearing Claim):** Escalate to the full schema (Counter-positions, Crux, Falsifier, Dated Position, Typed Edges) **only** when a claim:
  1. is consulted for a real decision, or
  2. directly contradicts another note.

*(Note: "Promoted on second reuse" is intentionally excluded from Tier 2 triggers so that Rule 3's second-touch promotion into `30_Library/` does not collapse Tier 1 into Tier 2.)*

---

## 3. Map vs. Topic Bucket Boundary Test

Index notes (`type: map` / MOCs) may exist sparingly as navigation hubs, but must not decay into passive topical warehouses.

- **The Test:** A Map may contain **only** links and 1-line relational context. The moment a Map contains raw paragraphs, quotes, or unlinked facts, it has decayed into a Topic Bucket and must be split or purged.

---

## 4. Operating Rules

1. **No Topic Buckets:** Never create a topical container (e.g., `Networking.md`) to store facts. Create a Tier 1 claim *about* the topic, a concept distinction, or a debugging procedure.
2. **Capture the Delta:** Do not summarise sources. Record only what surprised you, explained a failure, or shifted your prior confidence.
3. **Promote on Second Touch:** Notes stay as low-friction scratchpads in `00_Inbox/` or `20_Thinking/` until reached for a second time or used in a decision, entering `30_Library/` at Tier 1.

---

## 5. Falsifier (90-Day Empirical Test: 2026-11-17 to 2027-02-15)

Tracked via an external Decision Log (1 line per real work/architecture decision):

1. **The Baseline A/B Test:** For the next 5 real architectural or life decisions, query an LLM over raw notes/transcripts first, then consult/write the relevant Claim cards. If the Claim cards do not **alter** the decision over the raw-note LLM answer in at least **2 of the 5 cases**, this architecture is falsified.
2. **The Revision & Usage Threshold:** If, between **2026-11-17 and 2027-02-15**, fewer than **5 real decisions** in the Decision Log cite a vault Claim card, OR if **more time/commits are spent editing PKM schema/linter rules than logging claim updates**, the proposition-centred architecture is falsified as net-negative ceremony.

---

## Working Knowledge & Upstream Grounding

- [[Proposition-Centred Notes Create Cognitive Leverage That Topical Notes Lack]]—_Supplies the underlying cognitive mechanism for why declarative propositions outperform topical nouns._ [synthesizes:: [[Proposition-Centred Notes Create Cognitive Leverage That Topical Notes Lack]], confidence=high]
- [[Proposition-Centred Notes Make Superior RAG Chunks for LLM Context Engines]]—_Shows how atomic propositional units improve retrieval precision and context assembly._ [synthesizes:: [[Proposition-Centred Notes Make Superior RAG Chunks for LLM Context Engines]], confidence=high]
- [[Propositions Are the Only Thing That Can Be Wrong]]—_Grounds the epistemic primacy of propositions as the sole units capable of truth, falsity, and revision._ [synthesizes:: [[Propositions Are the Only Thing That Can Be Wrong]], confidence=high]
- [[Claim - Thinking Earns Its Place by Improving Model Fidelity]]—_Scopes ProdOS Kernel Axiom 1 so model-fidelity investments in 30_Library are recognised as valid work._ [depends_on:: [[Claim - Thinking Earns Its Place by Improving Model Fidelity]], confidence=high]
- [[The Atomicity Principle - One Idea Per Note]]—_Provides the atomicity constraint underpinning Tier 1 and Tier 2 claim cards._ [depends_on:: [[The Atomicity Principle - One Idea Per Note]], confidence=high]
- [[SoT - PRODOS Core Specification]]—_Defines the overarching ProdOS Thinking Stream within which this proposition-centred architecture operates._ [extends:: [[SoT - PRODOS Core Specification]], confidence=high]
- [[SoT - Atomic Note Standard (The Proposition Card)]]—_Specifies the concrete structural contract and linter rules for atomic proposition cards._ [depends_on:: [[SoT - Atomic Note Standard (The Proposition Card)]], confidence=high]
- [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]—_Defines the frontmatter envelope and the five knowledge-node schemas._ [depends_on:: [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]], confidence=high]
- [[SoT - Knowledge Compiler (Argument Graph Spec)]]—_Relies on proposition-centred claims and typed edges to audit support, contradictions, and load-bearing premises._ [depends_on:: [[SoT - Knowledge Compiler (Argument Graph Spec)]], confidence=high]
- [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]]—_Separates low-friction capture from propositional clarification to prevent premature formalisation._ [depends_on:: [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]], confidence=high]