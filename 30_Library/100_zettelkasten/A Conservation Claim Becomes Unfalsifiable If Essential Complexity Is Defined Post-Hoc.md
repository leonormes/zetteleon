---
conformant: true
contradicts: ["[[Software Complexity is Conserved Between Control Flow and Representation]]"]
created: 2026-09-19T15:26:00+00:00
created_utc: 2026-09-19 00:00:00+00:00
epistemic_status: high
evidence_links: []
modified: 2026-09-26T08:45:25+00:00
non_conformance_reason: ''
permalink: llmeon/00-inbox/a-conservation-claim-becomes-unfalsifiable-if-essential-complexity-is-defined-post-hoc
proposition: If essential complexity is defined merely as whatever complexity survived a simplification attempt, then any observed reduction can always be redescribed as accidental complexity being removed while essential complexity was conserved, making the conservation claim true by definition and untestable; it only becomes falsifiable if essential complexity is estimated independently, before the representation is chosen.
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [conservation-of-complexity, epistemics, falsifiability, unfalsifiable-claims]
title: A Conservation Claim Becomes Unfalsifiable If Essential Complexity Is Defined Post-Hoc
type: claim
upstream: '[[tmp_atoms_data-structures-vs-control-flow]]'
---

## A Conservation Claim Becomes Unfalsifiable If Essential Complexity Is Defined Post-Hoc

If "essential complexity" is defined merely as "whatever complexity survived a simplification attempt," then any observed reduction can always be redescribed as accidental complexity being removed while essential complexity was conserved—making the conservation claim true by definition and untestable; it only becomes falsifiable if essential complexity is estimated independently, before the representation is chosen (e.g. by counting domain states or business rules).

### Scope & Conditions

A general falsifiability critique applicable to any "conservation of X" claim defined circularly around what remains after optimisation.

### Evidence

> "If 'essential' just means 'whatever survived simplification', conservation is true by definition and can't be falsified. It only becomes testable if you estimate essential complexity independently before choosing a representation, for example by counting domain states or business rules."

### Implications

- Any future defence of "complexity is conserved" needs an independent, ex-ante measure of essential complexity, not a post-hoc one.

### Related

- [[Falsifiability Distinguishes Science from Dogma]]—shared mechanism: applies that note's general falsifiability standard to this specific conservation-of-complexity claim.

[implements:: [[Falsifiability Distinguishes Science from Dogma]], confidence=high]

### Tensions

- [[Software Complexity is Conserved Between Control Flow and Representation]]—contradicts: states the conservation law as settled fact with no falsifiability caveat.
- [[SoT - Conservation of Complexity]]—contradicts: same unqualified statement; that note's own "Open threads" pointer to an as-yet-unwritten HEAD note on whether Tesler's Law generalises beyond software suggests this gap was already suspected but never articulated this precisely (the pointer itself is currently dangling—no such HEAD note exists in the vault yet).

[contradicts:: [[SoT - Conservation of Complexity]], confidence=medium]
