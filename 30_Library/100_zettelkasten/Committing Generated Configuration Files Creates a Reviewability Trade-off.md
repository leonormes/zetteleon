---
conformant: true
created: 2026-09-23T14:50:13+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-26T08:45:28+00:00
permalink: llmeon/00-inbox/committing-generated-configuration-files-creates-a-reviewability-trade-off
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [ci-cd, code-review, cue]
title: Committing Generated Configuration Files Creates a Reviewability Trade-off
type: claim
upstream: '[[CUE-ASSESSMENT]]'
---

## Committing Generated Configuration Files Creates a Reviewability Trade-off

Committing a CUE-generated values file to git so ArgoCD can read it forces reviewers to either diff a large generated artefact as noise, or skip reviewing it and leave the generator itself unreviewed.

### Scope & Conditions

Applies whenever generated configuration is committed to version control rather than rendered at deploy time; rendering in CI rather than on a developer's laptop is a partial mitigation.

### Evidence

> "Reviewers now diff a 461-line generated artefact. Either you review generated output (noise) or you don't (and the generator becomes unreviewed). Rendering in CI and committing from the pipeline is better than `make generate-values` on a laptop, which is where POC B leaves it."

### Implications

- The choice of where generation happens (laptop vs CI) directly affects how trustworthy the committed artefact is.

### Related

- [[SoT - Generative Infrastructure Configuration Framework]]—extends: that SoT's "Onboarding Rule" (never manually edit generated output) is a related governance concern about the same generated-file boundary.
