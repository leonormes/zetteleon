---
conformant: true
created: 2026-09-19T15:25:53+00:00
created_utc: 2026-09-19 00:00:00+00:00
definition: Reducing procedural complexity by restructuring data can happen through at least two mechanistically different routes, elimination, where a special case is redefined out of existence such as the linked-list pointer-to-pointer trick, and relocation, where the same amount of complexity is genuinely moved into a table, parser, or type constraint such as Pike data tables or parse-dont-validate, and only the second route is actual evidence for a conservation claim.
distinguishes_from: []
modified: 2026-09-25T16:29:21+00:00
non_conformance_reason: ''
permalink: llmeon/00-inbox/elimination-and-relocation-are-distinct-complexity-management-mechanisms-often-conflated-as-conservation
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [conservation-of-complexity, elimination-vs-relocation, epistemics, falsifiability]
title: Elimination and Relocation Are Distinct Complexity-Management Mechanisms, Often Conflated as Conservation
type: concept
upstream: '[[tmp_atoms_data-structures-vs-control-flow]]'
used_in_claims: ["[[Parse, Don't Validate - Validation Is Lossy, Parsing Is Constructive]]", "[[Rob Pike's Rule 5 - Data Dominates]]", "[[The Linked-List Good Taste Example Eliminates Complexity Rather Than Relocating It]]"]
---

## Elimination and Relocation Are Distinct Complexity-Management Mechanisms, Often Conflated as Conservation

Reducing procedural complexity by restructuring data can happen through at least two mechanistically different routes—elimination, where a special case is redefined out of existence (e.g. the linked-list pointer-to-pointer trick), and relocation, where the same amount of complexity is genuinely moved into a table, parser, or type constraint (e.g. Pike's data tables, or parse-don't-validate)—and only the second route is actual evidence for a "conservation" claim.

### Scope & Conditions

A methodological distinction drawn from contrasting Torvalds' linked-list example against Pike's table-driven parsing and King's parse-don't-validate.

### Evidence

> "Only mechanisms 2 and 3 look like conservation. Mechanism 1, the headline Torvalds example, is a counterexample to it."

### Implications

- Citing an elimination example (complexity destroyed) as proof of a conservation law (complexity only relocated) is a category error, even though both examples feel like "the data structure did the work."

### Related

- [[The Linked-List Good Taste Example Eliminates Complexity Rather Than Relocating It]]—the concrete elimination instance of this general distinction.
- [[Rob Pike's Rule 5 - Data Dominates]] and [[Parse, Don't Validate - Validation Is Lossy, Parsing Is Constructive]]—the concrete relocation instances of this general distinction.

### Tensions

- [[Software Complexity is Conserved Between Control Flow and Representation]]—contradicts: asserts unqualified strict conservation ("it cannot be destroyed, only relocated") without distinguishing elimination from relocation.
- [[SoT - Conservation of Complexity]]—contradicts: same unqualified "cannot be destroyed, only relocated" framing (the "balloon" analogy), which this atom shows does not hold for the elimination case.

[contradicts:: [[Software Complexity is Conserved Between Control Flow and Representation]], confidence=high]

[contradicts:: [[SoT - Conservation of Complexity]], confidence=high]
