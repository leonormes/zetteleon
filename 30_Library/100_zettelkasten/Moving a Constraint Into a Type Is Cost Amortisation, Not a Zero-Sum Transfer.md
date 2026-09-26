---
conformant: true
contradicts: ["[[Software Complexity is Conserved Between Control Flow and Representation]]"]
created: 2026-09-19T15:26:07+00:00
created_utc: 2026-09-19 00:00:00+00:00
epistemic_status: high
evidence_links: []
modified: 2026-09-25T16:29:27+00:00
non_conformance_reason: ''
permalink: llmeon/00-inbox/moving-a-constraint-into-a-type-is-cost-amortisation-not-a-zero-sum-transfer
proposition: Even where the same information is preserved whether a constraint lives in a type or in a runtime check, the enforcement cost is not conserved, since a constraint expressed as a type is written once and checked by the compiler at every call site for free, whereas the same constraint expressed as a null check must be repeated at every call site and is enforced by nobody if a site forgets it, so moving a constraint into structure is a cost reduction, not a like-for-like relocation.
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [conservation-of-complexity, cost-amortisation, epistemics, type-systems]
title: Moving a Constraint Into a Type Is Cost Amortisation, Not a Zero-Sum Transfer
type: claim
upstream: '[[tmp_atoms_data-structures-vs-control-flow]]'
---

## Moving a Constraint Into a Type Is Cost Amortisation, Not a Zero-Sum Transfer

Even where the same information is preserved whether a constraint lives in a type or in a runtime check, the enforcement cost is not conserved: a constraint expressed as a type is written once and checked by the compiler at every call site for free, whereas the same constraint expressed as a null check must be repeated at every call site and is enforced by nobody if a site forgets it—so moving a constraint into structure is a cost reduction, not a like-for-like relocation.

### Scope & Conditions

The best-supported alternative to strict "conservation": enforcement cost, not information, is what actually changes when constraints move from control flow into types.

### Evidence

> "A constraint in a type is written once, checked by the compiler, and inherited by every call site. The same constraint as a null check is repeated N times and checked by nobody. Moving it into structure is amortisation, not a zero-sum transfer."

### Implications

- Reframes the defensible thesis as "structure is a cheaper home for essential complexity than control flow", not "total complexity is constant."
- Testable with before/after refactor metrics (conditional count, cyclomatic complexity, defect rate), unlike strict conservation.

### Related

- [[SoT - Type-Driven Development (The Torvalds Loop)]]—extends: supplies the mechanistic justification for why the Torvalds Loop's type-first workflow is cheaper, not merely structurally different, than the validation-first alternative.

[extends:: [[SoT - Type-Driven Development (The Torvalds Loop)]], confidence=high]

### Tensions

- [[Software Complexity is Conserved Between Control Flow and Representation]]—contradicts: frames the type/control-flow trade-off as a like-for-like relocation, not a cost reduction.
- [[SoT - Conservation of Complexity]]—contradicts: same relocation-only framing throughout (§1 "Practical Application").

[contradicts:: [[SoT - Conservation of Complexity]], confidence=medium]
