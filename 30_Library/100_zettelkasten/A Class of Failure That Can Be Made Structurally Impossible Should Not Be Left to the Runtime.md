---
conformant: true
contradicts: []
created: 2026-10-21T14:00:00+00:00
epistemic_status: medium
evidence_links: []
modified: 2026-10-22T15:11:19+00:00
permalink: llmeon/30-library/100-zettelkasten/a-class-of-failure-that-can-be-made-structurally-impossible-should-not-be-left-to-the-runtime
proposition: If a class of failure can be made structurally impossible in types, schemas,
  state files or scaffolds it should be, because leaving it to the runtime pays the
  complexity cost on every execution, though the cost of encoding it and the thin
  empirical base qualify how strongly this applies.
status: seed
tags: [complexity, formal-methods, topic/software-architecture, type-driven-design]
title: A Class of Failure That Can Be Made Structurally Impossible Should Not Be Left
  to the Runtime
type: claim
---

## A Class of Failure That Can Be Made Structurally Impossible Should Not Be Left to the Runtime

If a class of failure can be made structurally impossible, in types, schemas, state files or cognitive scaffolds, it should be. Leaving it as a runtime concern is a design choice to pay the complexity cost on every execution, indefinitely. The SoT states this as a design corollary of the conservation of complexity and writes it as a "MUST"; this note softens it to "should" for the reasons in Scope.

### Scope & Conditions

- The SoT's "MUST" is stronger than the evidence. Encoding a rule in structure has its own costs: structures ossify and become hard to change once shared, and the vault already records this as schema debt ([[Software Complexity is Conserved Between Control Flow and Representation]]).
- Moving complexity into structure relocates it and does not remove it, and [[Elimination and Relocation Are Distinct Complexity-Management Mechanisms, Often Conflated as Conservation]] says to tell the two apart.
- The direct empirical case is thin ([[Empirical Support for Types Prevent Bugs Is Thin and Indirect]]). The mechanism is supported by worked examples, not by controlled studies.

### Evidence

> "If a class of failures can be made structurally impossible—in types, schemas, state files, or cognitive scaffolds—it MUST be. Allowing it to remain a runtime concern is a design choice to pay the complexity tax on every execution, indefinitely."
> ([[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]], §3 Complexity Conservation, emphasis markers omitted)

> "This is an example of the important design guideline, "Make illegal states unrepresentable." We're trying to capture business rules in the type system. If we do this properly, invalid situations can't ever exist in the code and we never need to write unit tests for them."
> (Scott Wlaschin, _Domain Modeling Made Functional_, "Capturing Business Rules in the Type System")

### Implications

- The useful question in a design review is which class of failure the structure removes. A change that makes an illegal state unrepresentable is worth more than a check that catches it.
- The rule should be applied where the rule is stable. Encoding a rule that is still changing moves the cost to every later schema change.

### Related

[depends_on:: [[Software Complexity is Conserved Between Control Flow and Representation]], strength=4, confidence=medium]

[extends:: [[Making Illegal States Unrepresentable via Types (NonEmpty List Example)]], strength=4, confidence=high]

- [[Software Complexity is Conserved Between Control Flow and Representation]]—depends on: the conservation law the corollary is drawn from.
- [[Making Illegal States Unrepresentable via Types (NonEmpty List Example)]]—extends: the worked example that this claim generalises across domains.
- [[Parse, Don't Validate - Validation Is Lossy, Parsing Is Constructive]]—supports: parsing into a stricter type is the usual way to make a state unrepresentable.
- [[SoT - Type-Driven Development (The Torvalds Loop)]]—implements: the working protocol of shape, access, invariants, then logic.

### Tensions

- [[Empirical Support for Types Prevent Bugs Is Thin and Indirect]]—tension, not contradiction: the direct evidence for the benefit is thin, which argues against a "MUST".
- [[Elimination and Relocation Are Distinct Complexity-Management Mechanisms, Often Conflated as Conservation]]—tension, not contradiction: some "structural" fixes move complexity into the schema and do not remove it.
