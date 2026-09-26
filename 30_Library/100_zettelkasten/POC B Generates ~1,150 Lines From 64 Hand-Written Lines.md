---
conformant: true
created: 2026-09-23T14:49:36+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-25T16:29:28+00:00
permalink: llmeon/00-inbox/poc-b-generates-1-150-lines-from-64-hand-written-lines
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [configuration-management, cue, proof-of-concept]
title: POC B Generates ~1,150 Lines From 64 Hand-Written Lines
type: claim
upstream: '[[CUE-ASSESSMENT]]'
---

## POC B Generates ~1,150 Lines From 64 Hand-Written Lines

The second CUE proof-of-concept is a full working pipeline in which a 64-line customer configuration file, combined with a platform-defaults module and Terraform-supplied facts, generates approximately 1,150 lines of rendered output.

### Scope & Conditions

Located at `Clusters/eoe/Test/ff-test-1/`; verified to run end-to-end by the assessment's author.

### Evidence

> "64 hand-written lines produce ~1,150 generated lines. Against `hie-prod-34`'s ~1,750 hand-written lines, that is the real prize."

### Implications

- This is concrete evidence that CUE's payoff-per-customer is real and large, not theoretical.
- The comparison customer would go from ~1,750 hand-written lines to a fraction of that.

### Related

- [[SoT - Generative Infrastructure Configuration Framework]]—extends: concrete evidence for that SoT's claim that reducing to a Configuration Kernel cuts error surface area by 80–90%.
- [[SoT - Strategy - Helm to CUE Migration]]—extends: Phase 2 Hybrid Generation, demonstrated working.
