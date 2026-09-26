---
conformant: true
created: 2026-09-23T14:49:37+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-26T08:45:25+00:00
permalink: llmeon/00-inbox/a-json-round-trip-forces-a-hand-rolled-string-dispatch-interpreter-inside-cue
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [anti-pattern, architecture, cue, terraform]
title: A JSON Round-Trip Forces a Hand-Rolled String-Dispatch Interpreter Inside CUE
type: claim
upstream: '[[CUE-ASSESSMENT]]'
---

## A JSON Round-Trip Forces a Hand-Rolled String-Dispatch Interpreter Inside CUE

Because Terraform output data crosses a JSON boundary and JSON cannot carry a reference, the second proof-of-concept reimplements a late-binding indirection layer inside CUE as a 111-line string-keyed dispatch table, with no compile-time check that a string in the YAML matches a key in the table.

### Scope & Conditions

This mechanism exists only because of the `terraform output -json` boundary; it is architectural, not a coding mistake.

### Evidence

> "This exists because the data crosses a JSON boundary … a late-binding indirection layer is reimplemented inside CUE, in a language with no first-class support for it … Remove that boundary (let CUE read `common.yaml` and `customer.yaml` directly) and this entire file disappears."

### Implications

- Adding a new template helper requires touching three separate files with no compiler check linking them.
- Removing the JSON boundary, by reading source YAML directly in CUE, eliminates this entire mechanism.

### Related

- [[SoT - Generative Infrastructure Configuration Framework]]—extends: names exactly the `infra_facts` contract boundary, in its own architecture diagram, as the root cause of this mechanism.
