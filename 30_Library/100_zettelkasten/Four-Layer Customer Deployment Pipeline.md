---
conformant: true
created: 2026-09-23T14:48:24+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-25T16:29:23+00:00
permalink: llmeon/00-inbox/four-layer-customer-deployment-pipeline
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [argocd, cue, helm, infrastructure-as-code, terraform]
title: Four-Layer Customer Deployment Pipeline
type: claim
upstream: '[[CUE-ASSESSMENT]]'
---

## Four-Layer Customer Deployment Pipeline

Customer deployment to production runs through four layers, each owning part of one customer's configuration: per-cluster Terraform, an ArgoCD Application, an umbrella Helm chart carrying 901 lines of defaults, and hand-written per-customer override YAML.

### Scope & Conditions

Describes the pre-CUE deployment architecture for a specific multi-tenant customer estate. Not a general claim about all GitOps pipelines.

### Evidence

> "Four layers, each owning part of one customer's configuration: 1. Terraform (per cluster) … 2. ArgoCD Application … 3. ffnode umbrella chart … 4. Per-customer overrides"

### Implications

- Any correctness gap in one layer is invisible to the layers around it.
- A change to shared defaults (layer 3) can silently reclassify customers who omit an override (layer 4).

### Related

- [[SoT - DevOps & Infrastructure Architecture Strategy]]—shared mechanism: a layered, data-oriented deployment model is exactly the strategic pivot that SoT argues for.
- [[SoT - CUE Configuration]]—extends: describes the concrete, pre-CUE baseline that CUE's unification model is proposed as an alternative to.
