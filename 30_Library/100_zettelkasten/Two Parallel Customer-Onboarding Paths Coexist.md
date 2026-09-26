---
conformant: true
created: 2026-09-23T14:48:25+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-25T16:29:35+00:00
permalink: llmeon/00-inbox/two-parallel-customer-onboarding-paths-coexist
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [cue, infrastructure-as-code, onboarding, process-debt]
title: Two Parallel Customer-Onboarding Paths Coexist
type: claim
upstream: '[[CUE-ASSESSMENT]]'
---

## Two Parallel Customer-Onboarding Paths Coexist

Two unreconciled onboarding paths exist side by side: an established rsync-and-rename script that copies a previous customer's directory, and a newer CUE proof-of-concept where a 64-line customer file generates the full configuration.

### Scope & Conditions

Applies while both paths remain live and no migration has consolidated them onto one canonical route.

### Evidence

> "The established path—`Clusters/nwsde/scripts/create_customer.sh` does `rsync -av` of a previous customer's directory … The newer path—the CUE POC … where a 64-line `config/customer.yaml` generates everything."

### Implications

- New customers can be onboarded via either path, producing structurally different configuration for equivalent customers.
- Institutional knowledge of "which path is canonical" is undocumented and tacit.

### Related

- [[SoT - Strategy - Helm to CUE Migration]]—extends: the CUE POC named here as the newer path is the same migration strategy that SoT describes in phases.
- [[MOC - Generative Infrastructure Configuration]]—shared mechanism: the framework this MOC organises presumes one canonical generator per customer, not two parallel, divergent onboarding routes.
