---
conformant: true
created: 2026-09-23T14:49:36+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-23T14:56:28+00:00
permalink: llmeon/00-inbox/moving-deep-merge-logic-into-terraform-hcl-relocates-complexity-to-a-worse-place
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [anti-pattern, architecture, cue, terraform]
title: Moving Deep-Merge Logic Into Terraform HCL Relocates Complexity to a Worse Place
  Place
type: claim
upstream: '[[CUE-ASSESSMENT]]'
---

## Moving Deep-Merge Logic Into Terraform HCL Relocates Complexity to a Worse Place

The second proof-of-concept hand-rolls a deep merge of platform defaults against customer YAML inside 512 lines of Terraform HCL using 59 `merge()` calls and 149 `try()` calls, which the source assessment names as its single most important finding because it moves CUE's core benefit upstream into a language with no types and no tests.

### Scope & Conditions

Applies wherever CUE is fed a pre-merged blob from Terraform rather than being allowed to perform the merge itself.

### Evidence

> "Deep merging is the one thing CUE does natively, for free, in zero lines, order-independently. POC B does it in HCL—the worst available language for it … If you adopt CUE and keep this, you have paid for CUE and not bought the main thing it sells."

### Implications

- The bespoke per-key merge semantics this produces need a documentation table to explain, which is itself evidence the logic does not belong there.
- This is the specific defect a shared CUE module reading source YAML directly is designed to eliminate.

### Tensions

- [[SoT - Generative Infrastructure Configuration Framework]]—contradicts: directly violates that SoT's Layer Ownership Rule, under which `locals.tf` owns "Derived values only—no new literals," not hand-rolled merge logic.

### Related

- [[CUE Unification Is a Commutative Deep Merge]]—extends: the specific mechanism this finding says was bypassed by moving the merge upstream into HCL.
