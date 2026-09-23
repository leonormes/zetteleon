---
conformant: true
contradicts: []
created: 2026-02-01T20:57:04+00:00
epistemic_status: medium
evidence_links: []
modified: 2026-09-22T00:00:00+00:00
non_conformance_reason: ''
permalink: llmeon/30-library/100-zettelkasten/software-complexity-is-conserved-between-control-flow-and-representation
proposition: Software complexity obeys a conservation law, it cannot be destroyed, only relocated, and in any non-trivial system it must reside either in control flow or in representation.
tags: [concept/complexity, domain/software-engineering, law]
title: Software Complexity is Conserved Between Control Flow and Representation
type: claim
---

## Software Complexity is Conserved Between Control Flow and Representation

Software complexity obeys a conservation law: it cannot be destroyed, only relocated. In any non-trivial system, complexity must reside in one of two primary containers:

1. Control Flow (Code/Time): Logic, branches, loops, and temporal sequences.
2. Representation (Data/Space): Schemas, types, graphs, and static structures.

### The Trade-off

When a developer "worries about data structures" (Torvalds/Pike), they are moving complexity out of the procedural layer and into the structural layer.

- Smart Structures ⇒ Dumb Code: If the data model perfectly mirrors the problem domain's constraints, the algorithms required to manipulate that data become trivial, often reducing to simple traversals or lookups.
- Dumb Structures ⇒ Brittle Code: If the data model is a "flat bucket" or lacks internal constraints, the code must compensate with defensive null-checks, complex `if/else` ladders, and state-tracking flags.

### Cognitive and Computational Implications

- Static vs. Dynamic: Humans and machines find it easier to reason about static topology (what things are) than dynamic execution (how things change over time).
- Schema Debt: Because data structures often "ossify" (become hard to change once shared or at scale), failing to encode complexity in structure early leads to "interest" paid in the form of increasingly complex and fragile code.

### Relation to LLMs

This law is the foundation for the [[SoT - LLM Reasoning Obeys the Complexity Conservation Law|LLM Corollary]], as LLMs are significantly more effective at traversing structure than simulating execution.

### Known Challenges to Strict Conservation

The "cannot be destroyed, only relocated" wording above is the strong, unqualified version of this claim, and a cluster of sibling atoms drawn from the same source material each show a real gap in it — this is why `epistemic_status` is `medium`, not `high`, despite the mechanism itself being well-evidenced:

- Elimination, not just relocation: [[The Linked-List Good Taste Example Eliminates Complexity Rather Than Relocating It]] is Torvalds' own headline "good taste" example, and on inspection it is complexity being *destroyed*, not moved — the special-case `if` doesn't relocate, it stops existing. [[Elimination and Relocation Are Distinct Complexity-Management Mechanisms, Often Conflated as Conservation]] generalises why conflating the two is a category error.
- Unfalsifiable if stated circularly: [[A Conservation Claim Becomes Unfalsifiable If Essential Complexity Is Defined Post-Hoc]] — if "essential complexity" just means "whatever survives simplification," this law is true by definition and untestable; it only becomes falsifiable against an independent, ex-ante estimate of essential complexity.
- Cost amortisation may be the better-supported frame: [[Moving a Constraint Into a Type Is Cost Amortisation, Not a Zero-Sum Transfer]] argues that what actually changes when a constraint moves from control flow into a type is *enforcement cost* (written once, checked by the compiler everywhere) rather than a like-for-like transfer of a fixed quantity of complexity.
- Thin direct empirical support: [[Empirical Support for Types Prevent Bugs Is Thin and Indirect]] — the closest available measurements (Gao, Bird & Barr 2017; Berger et al. 2019) are adjacent to this claim, not direct tests of it.

---

[supports:: [[SoT - Conservation of Complexity]], strength=4, confidence=high]

Source: footnote to Linus Torvalds, "Re: Licensing and the library version of git", git mailing list, 27 Jul 2006 — not a standalone essay; see [[Smart Data Structures Yield Trivial Code (Torvalds' Maxim, Corrected Sourcing)]] for the corrected sourcing this claim's own framing borrowed without attribution.
