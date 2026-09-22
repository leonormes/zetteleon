---
conformant: false
non_conformance_reason: "missing schema field definition for type concept (required when conformant - true); missing schema field distinguishes_from for type concept (required when conformant - true); missing schema field used_in_claims for type concept (required when conformant - true)"
created: 2026-09-13T09:35:15+00:00
created_utc: '2026-09-13T00:00:00Z'
modified: 2026-09-19T15:44:29+00:00
permalink: llmeon/00-inbox/a-proposed-eight-predicate-edge-vocabulary-for-typed-pkm-links
source_title: A Portable Interest and PKM Knowledge Graph
source_url: UNKNOWN
status: seed
tags: [knowledge-graph, pkm, predicate-vocabulary, typed-edges]
title: A Proposed Eight-Predicate Edge Vocabulary for Typed PKM Links
type: concept
upstream: '[[PKM Meta-Graph System Research]]'
---

## A Proposed Eight-Predicate Edge Vocabulary for Typed PKM Links

A proposed minimal predicate vocabulary for typed Markdown links in a PKM graph consists of eight predicates: "is a" (subtype, inverse "has subtype"), "part of" (structural component, inverse "has part"), "supports" (evidence for a claim, inverse "supported by"), "challenges" (disputes or creates tension with a claim), "applies to" (transfers a mechanism into a domain, inverse "application of"), "enables" (makes a capability possible, inverse "enabled by"), "derived from" (records provenance, inverse "source for"), and "contrasts with" (clarifies difference without necessarily refuting, symmetric).

### Scope & Conditions

A ninth predicate, "related to," is permitted only as a temporary inbox marker to be reviewed later into a more precise type or deleted—not a permanent category.

### Evidence

> "Use these eight predicates for the first version… Permit 'related to' only as a temporary inbox predicate."

### Implications

- This vocabulary overlaps but does not match the LLMeon vault's own controlled typed-edge vocabulary, which is a direct tension rather than a drop-in addition.
- Reconciling the two vocabularies (or explicitly deciding they serve different purposes) is a prerequisite before this research's edge model can be adopted wholesale.

### Tensions

[contradicts:: [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]], strength=4, confidence=high]

- [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]—contradicts: the vault's canonical vocabulary is a closed set of six relations (`extends`, `synthesizes`, `implements`, `contradicts`, `supports`, `depends_on`, plus `revises`). Only `supports` overlaps. This note's `challenges`, `applies to`, `enables`, `derived from`, `contrasts with`, `is a`, and `part of` are all outside that closed set—per that SoT's own §2 rule, "the list is closed—an unknown relationship is a compiler error, not a silent pass." Adopting any of this note's predicates would require deliberately extending the canonical vocabulary table, not just using them.
