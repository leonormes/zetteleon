---
conformant: true
created: 2026-09-23T14:49:36+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-23T14:56:28+00:00
permalink: llmeon/00-inbox/poc-b-does-not-validate-its-own-generated-output
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [cue, proof-of-concept, validation]
title: POC B Does Not Validate Its Own Generated Output
type: claim
upstream: '[[CUE-ASSESSMENT]]'
---

## POC B Does Not Validate Its Own Generated Output

The second proof-of-concept's `#InfraFacts` type validates its Terraform input, but its `values:` output remains an ordinary open struct, so a typo in the rendering logic itself renders successfully and deploys wrong.

### Scope & Conditions

Applies specifically to the output side of the second proof-of-concept, as distinct from its already-typed input side.

### Evidence

> "A typo in `render_fitfile.cue`—`mongoDb:` for `mongodb:`—renders happily and deploys wrong. The typo class from §2.1 is not closed by POC B as written."

### Implications

- Adopting this proof-of-concept as-is would not close the original Helm typo problem it was partly built to solve.
- Closing this gap requires applying a closed schema to the output side, not just the input side.

### Tensions

- [[SoT - Generative Infrastructure Configuration Framework]]—contradicts: violates that SoT's "Fail Fast" principle, that the Generator contract must be validated, and its "Schema as Truth" pattern.

### Related

- [[POC B Generates ~1,150 Lines From 64 Hand-Written Lines]]—extends: describes the specific validation gap left open in the same proof-of-concept.
