---
conformant: true
contradicts: []
created: 2026-09-19T15:25:10+00:00
created_utc: 2026-09-19 00:00:00+00:00
epistemic_status: high
evidence_links: []
modified: 2026-09-25T16:29:28+00:00
non_conformance_reason: ''
permalink: llmeon/00-inbox/parse-dont-validate-validation-is-lossy-parsing-is-constructive
proposition: A validation function discards the proof of correctness it computed, returning only true or false while the data stays in its raw type, whereas a parser is constructive and transforms raw input into a more structured type that carries the proof of validity with it for the rest of its lifetime.
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [alexis-king, parse-dont-validate, type-driven-design, validation]
title: "Parse, Don't Validate - Validation Is Lossy, Parsing Is Constructive"
type: claim
upstream: '[[tmp_atoms_data-structures-vs-control-flow]]'
---

## Parse, Don't Validate - Validation Is Lossy, Parsing Is Constructive

A validation function discards the proof of correctness it computed (returning only true/false while the data stays in its raw type), whereas a parser is constructive—it transforms raw input into a more structured type that carries the proof of validity with it for the rest of its lifetime.

### Scope & Conditions

Alexis King's "Parse, Don't Validate" principle; assumes a type system expressive enough to encode the refined type as distinct from the raw type.

### Evidence

> "Validation is an inherently lossy process… If the function returns True, the calling code knows the data is safe, but the data itself remains in its raw, unconstrained format… Parsing, by contrast, is a constructive transformation… the output type is a distinct refinement of the input type."

### Implications

- Once parsed, downstream functions that require the refined type get their validity guarantee for free from the type system, with zero repeated control flow.
- A validation-only approach forces every downstream function to choose between blind trust and redundant re-checking.

### Related

- [[SoT - Type-Driven Development (The Torvalds Loop)]]—direct concept match: §3 "Pattern: Parse, Don't Validate" gives the near-identical definition, including the same `is_email`/`parse_email` contrast.
- [[Shotgun Parsing Scatters Validation Logic Through Execution Logic]]—_this claim is the constructive fix to the anti-pattern that note names; the two are the same theme's problem and remedy._
- [[Elimination and Relocation Are Distinct Complexity-Management Mechanisms, Often Conflated as Conservation]]—_named by that note as one of its worked relocation instances (validation cost is genuinely moved into the type, not destroyed)._

[depends_on:: [[Shotgun Parsing Scatters Validation Logic Through Execution Logic]], confidence=medium]

[implements:: [[Elimination and Relocation Are Distinct Complexity-Management Mechanisms, Often Conflated as Conservation]], confidence=medium]

### Further Reading (Personal Library)

- [Programming With Types: Examples in TypeScript — Vlad Riscutia, Ch. 1 "Introduction to typing"](calibre://view-book/GCcalibreBooks/421/EPUB)—_corroborates the core mechanism: "type checkers provide powerful ways to eliminate whole classes of errors… types give us more general proofs that the code will behave according to spec regardless of input," matching this atom's validation-vs-parsing distinction._
