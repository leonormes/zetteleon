---
conformant: true
created: 2026-09-23T14:50:15+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-25T16:29:30+00:00
permalink: llmeon/00-inbox/recommended-cue-adoption-sequence-is-validate-publish-merge-then-generate
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [cue, infrastructure-as-code, migration-strategy]
title: Recommended CUE Adoption Sequence Is Validate Publish Merge Then Generate
type: procedure
upstream: '[[CUE-ASSESSMENT]]'
---

## Recommended CUE Adoption Sequence Is Validate, Publish, Merge, Then Generate

The recommended adoption sequence is four independently-valuable, independently-abandonable steps: add a closed schema and run `cue vet` in CI with no migration; publish that schema as a versioned CUE module to the container registry; move the deep-merge logic out of Terraform HCL into CUE; and only then generate values, starting with one low-risk non-production node.

### Scope & Conditions

Each step is designed to be a defensible stopping point on its own. Skipping directly to value-generation without completing the merge step reproduces the not-recommended per-repo generator option.

### Evidence

> "Step 0—Validation gate … Step 1—Publish the schema as a CUE module to ACR … Step 2—Move the deep merge out of HCL into CUE … Step 3—Only then, generate values, one non-production node first … Do not skip this step and go straight to generating values—that is Option A, and it is the configuration that has already drifted."

### Implications

- The plan is designed so that stopping after any step still leaves a net improvement.
- The success criterion for Step 2 is that the bespoke merge-semantics documentation tables become unnecessary.

### Related

- [[Three Architectural Options Exist for Where the CUE Boundary Sits]]—extends: this sequence is the path from the cheapest option (validation-only) to the recommended destination (shared module), while explicitly avoiding the not-recommended option.
- [[SoT - Strategy - Helm to CUE Migration]]—extends: near-identical in structure to that SoT's own "Shadow & Strangulate" three-phase strategy, refined into four concrete steps.
- [[Protocol - Helm to CUE Migration]]—extends: the strict protocol-grade version of the same phased migration algorithm.
