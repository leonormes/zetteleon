---
conformant: false
non_conformance_reason: "missing schema field proposition for type claim (required when conformant - true); missing schema field epistemic_status for type claim (required when conformant - true); missing schema field contradicts for type claim (required when conformant - true); missing schema field evidence_links for type claim (required when conformant - true)"
created: 2026-09-19T15:25:37+00:00
created_utc: 2026-09-19 00:00:00+00:00
modified: 2026-09-19T15:44:40+00:00
permalink: llmeon/00-inbox/primitive-obsession-forces-validation-into-control-flow-value-objects-absorb-it-into-structure
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [domain-driven-design, primitive-obsession, value-objects]
title: "Primitive Obsession Forces Validation Into Control Flow, Value Objects Absorb It Into Structure"
type: claim
upstream: '[[Data Structures vs Control Flow]]'
---

## Primitive Obsession Forces Validation Into Control Flow, Value Objects Absorb It Into Structure

Representing a heavily-constrained domain concept with a bare primitive type (e.g. a generic string for a Social Security Number, or a plain int for an account balance) discards all structural constraints, forcing every consuming function to re-validate it, whereas a Value Object with a smart constructor enforces the constraint once, at construction, and is thereafter treated as immutable proof of validity.

### Scope & Conditions

A Domain-Driven Design pattern for eliminating "primitive obsession."

### Evidence

> "When primitives are utilized, they carry no structural constraints… developers must sprinkle validation logic and control flow loops throughout the entire application… An AccountBalance type is created with a smart constructor that strictly enforces the rule that the value must be non-negative at the time of creation."

### Implications

- Passing structured Value Objects instead of raw primitives also prevents accidental parameter-order swaps between same-typed primitives.

### Related

- [[SoT - Stringly Typed vs Strongly Typed]]—direct concept match: "Primitive Obsession" and "String Blindness" are listed as this note's own aliases; §1 describes the identical anti-pattern ("A string is just a generic array of bytes… the compiler cannot help you").
- [[SoT - Type-Driven Development (The Torvalds Loop)]]—shared mechanism: §6 "Anti-Patterns to Exorcise" lists Primitive Obsession with the same NewType fix.
