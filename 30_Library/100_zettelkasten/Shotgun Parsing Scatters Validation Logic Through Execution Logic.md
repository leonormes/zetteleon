---
conformant: true
created: 2026-09-19T15:25:02+00:00
created_utc: 2026-09-19 00:00:00+00:00
modified: 2026-09-19T15:44:42+00:00
permalink: llmeon/00-inbox/shotgun-parsing-scatters-validation-logic-through-execution-logic
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [alexis-king, anti-pattern, shotgun-parsing, validation]
title: Shotgun Parsing Scatters Validation Logic Through Execution Logic
type: concept
upstream: '[[Data Structures vs Control Flow]]'
---

## Shotgun Parsing Scatters Validation Logic Through Execution Logic

"Shotgun parsing" (Alexis King's term) is the anti-pattern where input-validation checks are interleaved with execution logic and repeated at scattered points across a codebase instead of being performed once at a system boundary.

### Scope & Conditions

Applies to systems that accept loosely-typed input (e.g. generic dictionaries) and validate it ad hoc wherever it is consumed.

### Evidence

> "Alexis King refers to this anti-pattern as 'shotgun parsing,' a state where input-validating logic is mixed directly with the execution logic and scattered randomly across the codebase… late-stage validation failures can occur after partial processing has already mutated the system state, leading to data corruption."

### Implications

- Because validation isn't bound to the data's type, downstream code must either blindly trust it or redundantly re-check it.

### Related

- [[SoT - Type-Driven Development (The Torvalds Loop)]]—direct concept match: §3 "The Problem: Shotgun Parsing" defines the identical anti-pattern with the identical name and rationale.
