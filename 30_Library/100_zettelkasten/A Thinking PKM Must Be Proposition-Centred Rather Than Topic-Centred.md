---
aliases:
- PKM should probably be proposition-centred, not topic-centred
- PKM should probably be proposition-centered, not topic-centered
conformant: true
contradicts: []
created: 2026-11-16T23:00:00+00:00
epistemic_status: medium
evidence_links: []
modified: 2026-11-17T10:30:00+00:00
permalink: llmeon/30-library/100-zettelkasten/pkm-should-probably-be-proposition-centred-not-topic-centred-1
proposition: Organising a personal knowledge vault around testable propositions yields
  better decisions and model revisions than topical buckets when structural rigour
  is pulled by live decisions rather than pushed at capture.
status: seed
tags:
- domain/pkm
- prodos/llmeon
- topic/knowledge-architecture
title: A Thinking PKM Must Be Proposition-Centred Rather Than Topic-Centred
type: claim
---

## A Thinking PKM Must Be Proposition-Centred Rather Than Topic-Centred

For engineering and architectural work, organising a vault around testable propositions yields better decisions and model revisions than organising around topical buckets. This advantage holds only when structural rigour is pulled by live decisions rather than pushed onto every note at capture.

### Scope & Conditions

- Applies to personal knowledge systems used for belief revision and decision support, under a 90-day empirical test (2026-11-17 to 2027-02-15) tracked via an external Decision Log.
- **90-day falsifiers:** (1) across the next 5 real decisions, claim cards must alter the decision over a raw-note LLM query in at least 2 of 5 cases; (2) fewer than 5 Decision Log citations, or more effort spent editing PKM schema/linter rules than logging claim updates, falsifies this claim.
- **Dated position:** 2026-04-23 (~0.75 hypothesis); 2026-08-29 (~0.80 working belief after retiring Axiom 1); 2026-11-16 (~0.65 conjecture under test after the 58:6 governance-to-claim audit).

### Evidence

This claim rests on my own reasoning, two vault observations, and Cognitive Load Theory (no verbatim source quotation is attached here):

- **Axiom Retirement (2026-08-29):** Converting ProdOS Kernel Axiom 1 into `[[Claim - A Note That Does Not Help You Act Is Noise]]` exposed a contradiction with the Zettelkasten layer, leading to its replacement by `[[Claim - Thinking Earns Its Place by Improving Model Fidelity]]`. In a topic-bucket wiki, both statements would have coexisted silently.
- **Schema-Over-Use Trap (2026-11):** A `30_Library` audit found 58 governance notes (`sot`, `map`, `protocol`) supporting only 6 `claim` cards, showing that heavy upfront schema ceremony induces maintenance avoidance.
- **Cognitive Load Theory (Bastani et al., 2024; Fan et al., 2025):** Offloading extraneous load aids working memory, whereas offloading germane load (translating ideas into personal claims and resolving contradictions) induces metacognitive laziness and the fluency illusion.

### Implications

- Operational details (the five core note types, Tier 1/Tier 2 pull escalation, and the Map vs Topic Bucket test) live in `[[SoT - Proposition-Centred PKM Architecture]]`.
- Notes remain low-friction scratchpads in `00_Inbox/` or `20_Thinking/` until reached a second time or used in a decision, entering `30_Library/` at Tier 1.

### Steelman

- Long-context LLMs with semantic search over raw notes and chat transcripts may deliver most of the decision support at a fraction of the maintenance cost.
- Maintaining formal ontologies (`validate_note_shape.py`, `edge_lint.py`) risks substituting system-building for actual thinking and shipping.

### Related

- [[SoT - Proposition-Centred PKM Architecture]]—compiles the operational rules, five-type taxonomy, and Tier 1/Tier 2 pull escalation from this claim.
[supports:: [[SoT - Proposition-Centred PKM Architecture]], strength=5, confidence=high]
- [[Proposition-Centred Notes Create Cognitive Leverage That Topical Notes Lack]]—supplies the cognitive mechanism for why declarative propositions outperform topical nouns.
[depends_on:: [[Proposition-Centred Notes Create Cognitive Leverage That Topical Notes Lack]], strength=5, confidence=high]
- [[Claim - Thinking Earns Its Place by Improving Model Fidelity]]—explains why testing beliefs in `30_Library/` is valid work even without an immediate action item.
[depends_on:: [[Claim - Thinking Earns Its Place by Improving Model Fidelity]], strength=5, confidence=high]
- [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]]—separates low-friction capture from propositional clarification to prevent premature formalisation.
[depends_on:: [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]], strength=4, confidence=high]
- [[SoT - Knowledge Compiler (Argument Graph Spec)]]—relies on proposition-centred claims and typed edges to expose load-bearing premises and contradictions.
[supports:: [[SoT - Knowledge Compiler (Argument Graph Spec)]], strength=4, confidence=high]