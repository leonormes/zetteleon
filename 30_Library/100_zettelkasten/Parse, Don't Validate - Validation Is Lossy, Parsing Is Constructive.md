---
conformant: false
non_conformance_reason: "missing schema field proposition for type claim (required when conformant - true); missing schema field epistemic_status for type claim (required when conformant - true); missing schema field contradicts for type claim (required when conformant - true); missing schema field evidence_links for type claim (required when conformant - true)"
created: 2026-09-19T15:25:10+00:00
created_utc: 2026-09-19 00:00:00+00:00
modified: 2026-09-19T15:44:40+00:00
permalink: llmeon/00-inbox/parse-dont-validate-validation-is-lossy-parsing-is-constructive
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [alexis-king, parse-dont-validate, type-driven-design, validation]
title: "Parse, Don't Validate - Validation Is Lossy, Parsing Is Constructive"
type: claim
upstream: '[[Data Structures vs Control Flow]]'
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

### Further Reading (Personal Library)

- [Programming With Types: Examples in TypeScript — Vlad Riscutia, Ch. 1 "Introduction to typing"](calibre://view-book/GCcalibreBooks/421/EPUB)—_corroborates the core mechanism: "type checkers provide powerful ways to eliminate whole classes of errors… types give us more general proofs that the code will behave according to spec regardless of input," matching this atom's validation-vs-parsing distinction._
