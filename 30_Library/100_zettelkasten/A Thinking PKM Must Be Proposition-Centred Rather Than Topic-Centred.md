---
aliases:
- PKM should probably be proposition-centered, not topic-centered
conformant: true
contradicts: []
created: 2026-11-16T23:00:00+00:00
epistemic_status: medium
evidence_links: []
modified: 2026-11-16T23:04:18+00:00
proposition: Organising a personal knowledge vault around testable propositions yields
  better decisions and model revisions than topical buckets when structural rigour
  is pulled by live decisions rather than pushed at capture.
status: seed
tags:
- domain/pkm
- prodos/llmeon
- topic/knowledge-architecture
title: PKM should probably be proposition-centred, not topic-centred
type: claim
permalink: llmeon/30-library/100-zettelkasten/pkm-should-probably-be-proposition-centred-not-topic-centred-1
---

## A Thinking PKM Must Be Proposition-Centred Rather Than Topic-Centred

For engineering and architectural work, organising a vault around testable propositions yields better decisions and model revisions than organising around topical buckets. This advantage holds only when structural rigour is pulled by live decisions rather than pushed onto every note at capture.

### Scope & Conditions

- Applies to personal knowledge systems used for belief revision and decision support, under a 90-day empirical test (2026-11-17 to 2027-02-15) tracked via an external Decision Log.
- **Pull-based escalation (Tier 1 vs Tier 2):** Tier 1 default claims carry only a declarative sentence title and two lines of rationale. Escalation to Tier 2 (counter-positions, crux, falsifier, dated position, typed edges) triggers only when a claim is consulted for a real decision or directly contradicts another note.
- **90-day empirical falsifiers (2026-11-17 to 2027-02-15):**
  1. **Baseline A/B test:** For the next 5 real architectural or life decisions, query an LLM over raw notes and transcripts first, then consult or write the relevant claim cards; if the claim cards do not alter the decision over the raw-note LLM answer in at least 2 of 5 cases, this claim is falsified.
  2. **Revision and usage threshold:** If fewer than 5 real decisions in the Decision Log cite a vault claim card, or if more time or commits are spent editing PKM schema and linter rules than logging claim updates, the proposition-centred architecture is falsified as net-negative ceremony.
- **Dated position:** 2026-04-23 (~0.75 hypothesis); 2026-08-29 (~0.80 working belief after retiring Kernel Axiom 1); 2026-11-16 (~0.65 conjecture under test—downward update after the `30_Library` audit showed 58 governance notes supporting only 6 claim cards).

### Evidence

- **Positive vault observation (2026-08-29 — Axiom Retirement):** Converting ProdOS Kernel Axiom 1 into an explicit proposition (`[[Claim - A Note That Does Not Help You Act Is Noise]]`) exposed a direct contradiction with the Zettelkasten layer, leading to its formal retirement and replacement by `[[Claim - Thinking Earns Its Place by Improving Model Fidelity]]`. In a topic-bucket wiki, both statements would have coexisted silently.
- **Negative vault observation (2026-11 — Schema-Over-Use Trap):** A `30_Library` audit found 58 ProdOS structural and governance notes (`sot`, `map`, `protocol`) supporting only 6 `claim` cards, demonstrating that heavy upfront schema ceremony induces maintenance avoidance and productive procrastination.
- **External grounding (Cognitive Load Theory — Bastani et al., 2024; Fan et al., 2025):** Offloading extraneous load (formatting, filing) aids working memory, whereas offloading germane load (translating ideas into personal claims and resolving contradictions) induces metacognitive laziness and the fluency illusion.

### Implications

- Propositions serve as the centre of gravity supported by four scaffolding types (Concept, Evidence, Question, Procedure), while Maps remain navigation-only hubs without raw paragraphs or unlinked facts.
- Notes remain low-friction scratchpads in `00_Inbox/` or `20_Thinking/` until reached for a second time or used in a decision, entering `30_Library/` as lightweight Tier 1 claims by default.
- Credence updates and falsifiers must track observed decision outcomes rather than structural refactors.

### Steelman

- Long-context LLMs with semantic search over raw notes and chat transcripts may deliver most of the decision support at a fraction of the maintenance cost.
- Maintaining formal ontologies (`validate_note_shape.py`, `edge_lint.py`) risks substituting intellectually seductive system-building for actual thinking and shipping.

### Related

- [[SoT - Proposition-Centred PKM Architecture]]—compiles the five-type architecture, Tier 1/Tier 2 pull escalation, and 90-day falsifiers from this claim into a canonical SoT.
[supports:: [[SoT - Proposition-Centred PKM Architecture]]]
- [[Proposition-Centred Notes Create Cognitive Leverage That Topical Notes Lack]]—supplies the underlying cognitive mechanism for why declarative propositions outperform topical nouns.
[depends_on:: [[Proposition-Centred Notes Create Cognitive Leverage That Topical Notes Lack]]]
- [[Claim - Thinking Earns Its Place by Improving Model Fidelity]]—explains why testing beliefs in `30_Library/` is valid work even without an immediate action item.
[depends_on:: [[Claim - Thinking Earns Its Place by Improving Model Fidelity]]]
- [[SoT - Atomic Note Standard (The Proposition Card)]]—operationalises proposition cards into the vault structural contract and `validate_note_shape.py` rules.
[depends_on:: [[SoT - Atomic Note Standard (The Proposition Card)]]]
- [[SoT - Knowledge Compiler (Argument Graph Spec)]]—relies on proposition-centred claims and typed edges to expose load-bearing premises and contradictions.
[supports:: [[SoT - Knowledge Compiler (Argument Graph Spec)]]]