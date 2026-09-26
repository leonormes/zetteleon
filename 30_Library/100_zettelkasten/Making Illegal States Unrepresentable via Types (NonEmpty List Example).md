---
conformant: true
contradicts: []
created: 2026-09-19T15:25:16+00:00
created_utc: 2026-09-19 00:00:00+00:00
epistemic_status: high
evidence_links: []
modified: 2026-09-25T16:29:27+00:00
non_conformance_reason: ''
permalink: llmeon/00-inbox/making-illegal-states-unrepresentable-via-types-non-empty-list-example
proposition: Instead of validating that a list is non-empty before taking its head, a NonEmpty list type, structurally a tuple of one guaranteed element plus a possibly-empty remainder, makes emptiness impossible to represent, so no control flow is needed to guard against it.
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [alexis-king, illegal-states-unrepresentable, type-driven-design]
title: Making Illegal States Unrepresentable via Types (NonEmpty List Example)
type: claim
upstream: '[[tmp_atoms_data-structures-vs-control-flow]]'
---

## Making Illegal States Unrepresentable via Types (NonEmpty List Example)

Instead of validating that a list is non-empty before taking its head, a NonEmpty list type—structurally a tuple of one guaranteed element plus a possibly-empty remainder—makes emptiness impossible to represent, so no control flow is needed to guard against it.

### Scope & Conditions

Requires parsing/converting a generic list into the NonEmpty type at the boundary where the non-emptiness guarantee is first required.

### Evidence

> "The structural solution is to abandon the generic list and define a NonEmpty list data type… A function designed to retrieve the head of a NonEmpty list requires zero control flow, zero Option wrappers, and zero validation checks, because it is structurally impossible for the type to be empty."

### Implications

- If the underlying business rule changes (e.g. empty becomes valid), the type signature itself must change, forcing the compiler to flag every affected call site.

### Related

- [[SoT - Type-Driven Development (The Torvalds Loop)]]—direct concept match: §3 "Example: The Non-Empty List" gives the identical example with working Rust code (`struct NonEmptyList<T>(T, Vec<T>)`).
- [[SoT - Conservation of Complexity]]—extends: "By designing the shape of your data to prohibit invalid states… you eliminate the need for defensive code to handle those states" states the same principle generally.
