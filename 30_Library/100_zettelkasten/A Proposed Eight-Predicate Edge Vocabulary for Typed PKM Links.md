---
conformant: true
created: 2026-09-13T09:35:15+00:00
created_utc: '2026-09-13T00:00:00Z'
definition: Eight-predicate relational vocabulary (is a, part of, supports, challenges, applies to, enables, derived from, contrasts with) plus a temporary inbox marker (related to) proposed for human-readable typed PKM links.
distinguishes_from:
  - '[[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]'
modified: 2026-11-08T11:38:00+00:00
permalink: llmeon/30-library/100-zettelkasten/a-proposed-eight-predicate-edge-vocabulary-for-typed-pkm-links
source_title: A Portable Interest and PKM Knowledge Graph
source_url: UNKNOWN
status: seed
tags: [domain/pkm, knowledge-graph, pkm, predicate-vocabulary, topic/knowledge-architecture, typed-edges]
title: A Proposed Eight-Predicate Edge Vocabulary for Typed PKM Links
type: concept
upstream: '[[A Portable Interest and PKM Knowledge Graph]]'
used_in_claims:
  - '[[Claim - Domains relate through named relations, not undifferentiated association]]'
  - '[[Typed Links for Knowledge Context]]'
---

## A Proposed Eight-Predicate Edge Vocabulary for Typed PKM Links

A proposed minimal predicate vocabulary for typed Markdown links in a PKM graph consists of eight predicates: "is a" (subtype, inverse "has subtype"), "part of" (structural component, inverse "has part"), "supports" (evidence for a claim, inverse "supported by"), "challenges" (disputes or creates tension with a claim), "applies to" (transfers a mechanism into a domain, inverse "application of"), "enables" (makes a capability possible, inverse "enabled by"), "derived from" (records provenance, inverse "source for"), and "contrasts with" (clarifies difference without necessarily refuting, symmetric).

### Scope & Conditions

A ninth predicate, "related to," is permitted only as a temporary inbox marker to be reviewed later into a more precise type or deleted. In ProdOS, these predicates serve only as human-level link reasons rather than machine-compiled syntax, and the upstream project later moved to a 14-predicate self-inquiry vocabulary.

### Evidence

> "Use these eight predicates for the first version… Permit 'related to' only as a temporary inbox predicate."

### Implications

- ProdOS uses a two-layer split: richer predicates survive as prose reasons on bullets (`is a` / `part of` → `implements`, `applies to` → `extends`, `enables` → inverse `depends_on`, `derived from` → `revises` or provenance), while `[relation:: [[Target]]]` lines stay restricted to the closed seven-word compiler set.
- Separating `challenges` (`[contradicts:: ...]`) from `contrasts with` (`### Tensions` prose) matches the compiler split between strict negation and scoped tension.
- Treating `related to` as an expiring stub matches the rule that bare links belong only under `### See Also`.

### Related

[implements:: [[Claim - Domains relate through named relations, not undifferentiated association]], strength=3, confidence=high]
[extends:: [[Typed Links for Knowledge Context]], strength=3, confidence=medium]
[supports:: [[Key questions when linking notes in the Zettelkasten method]], confidence=medium]
[depends_on:: [[SoT - Atomic Note Standard (The Proposition Card)]], confidence=high]
[depends_on:: [[SoT - Knowledge Compiler (Argument Graph Spec)]], confidence=high]

- [[Claim - Domains relate through named relations, not undifferentiated association]]—implements: concrete eight-predicate starter set for replacing bare links with named relations.
- [[Typed Links for Knowledge Context]]—extends: operationalises link context into eight forward-and-inverse predicate pairs.
- [[Key questions when linking notes in the Zettelkasten method]]—supports: maps the four linking questions onto named predicates.
- [[SoT - Atomic Note Standard (The Proposition Card)]]—depends on: requires prose link reasons on bullets while restricting standalone edges to the compiler vocabulary.
- [[SoT - Knowledge Compiler (Argument Graph Spec)]]—depends on: formalises the closed seven-predicate compiler and the contradiction-versus-tension split.
- [[A Portable Interest and PKM Knowledge Graph]]—provenance: upstream project that later replaced this set with a 14-predicate self-inquiry vocabulary.

### Tensions

[contradicts:: [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]], strength=4, confidence=high]

- [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]—contradicts as a compiler schema: the canonical vocabulary is a closed seven-relation set (`extends`, `synthesizes`, `implements`, `contradicts`, `supports`, `depends_on`, `revises`), so seven predicates here must be translated or kept as prose annotations.
