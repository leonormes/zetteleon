---
conformant: true
contradicts: []
created: 2026-09-19T15:26:16+00:00
created_utc: 2026-09-19 00:00:00+00:00
epistemic_status: medium
evidence_links: []
modified: 2026-09-22T00:00:00+00:00
non_conformance_reason: ''
permalink: llmeon/00-inbox/the-right-data-structure-not-a-smart-one-is-pikes-actual-rule
proposition: Rob Pike Rule 4, use simple algorithms as well as simple data structures, asks for the structure that correctly fits the domain, not a maximally clever or elaborate one; over-engineered types and deep class hierarchies are themselves a form of accidental complexity, so pushing complexity into structure is not unconditionally good advice.
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [accidental-complexity, falsifier, over-engineering, rob-pike]
title: "The Right Data Structure, Not a Smart One, Is Pike's Actual Rule"
type: claim
upstream: '[[tmp_atoms_data-structures-vs-control-flow]]'
---

## The Right Data Structure, Not a Smart One, Is Pike's Actual Rule

Rob Pike's Rule 4 ("use simple algorithms as well as simple data structures") asks for the structure that correctly fits the domain, not a maximally clever or elaborate one; over-engineered types and deep class hierarchies are themselves a form of accidental complexity, so "push complexity into structure" is not unconditionally good advice.

### Scope & Conditions

A falsifier/boundary condition on the whole "smart structures" thesis—names its own failure mode.

### Evidence

> "Pike warns against 'smart'. His Rule 4 says to use simple algorithms as well as simple data structures. He asks for the right structure, not a smart one. Over-engineered types and deep class hierarchies are structural complexity that is itself accidental."

### Implications

- Any "push complexity into data structures" guideline needs a matching falsifier: has the resulting type/schema become elaborate enough to be its own source of accidental complexity?

### Related

- [[SoT - Data-Oriented Design]]—qualifies: presents "smart structures" affirmatively (§0 MVU) without this caveat.
- [[SoT - Type-Driven Development (The Torvalds Loop)]]—qualifies: same affirmative framing throughout; this atom supplies the missing boundary condition.

### Further Reading (Personal Library)

- [Modern Software Engineering — Dave Farley, "Fear of Over-Engineering"](calibre://view-book/GCcalibreBooks/215/EPUB)—_a concrete worked example of the failure mode: a "grand plan for a distributed, service-based component architecture" imposed on a project, illustrating structure becoming its own accidental complexity._
- [Refactoring to Patterns — Joshua Kerievsky, Ch. 1 "Why I Wrote This Book"](calibre://view-book/GCcalibreBooks/176/EPUB)—_corroborates the general definition: "When you make your code more flexible or sophisticated than it needs to be, you over-engineer it… code you produce in anticipation of needs that never materialize… never gets removed."_
