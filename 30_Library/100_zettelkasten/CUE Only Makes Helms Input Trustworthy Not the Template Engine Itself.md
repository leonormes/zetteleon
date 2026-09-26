---
conformant: true
created: 2026-09-23T14:50:13+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-25T16:29:19+00:00
permalink: llmeon/00-inbox/cue-only-makes-helms-input-trustworthy-not-the-template-engine-itself
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [architecture, cue, helm, scope]
title: CUE Only Makes Helms Input Trustworthy Not the Template Engine Itself
type: concept
upstream: '[[CUE-ASSESSMENT]]'
---

## CUE Only Makes Helm's Input Trustworthy, Not the Template Engine Itself

CUE generates the values.yaml file consumed by Helm, but everything downstream—the chart's template helpers, the double-`tpl` rendering, ArgoCD's sync behaviour, and Terraform's provisioning—is unchanged and remains as error-prone as before.

### Scope & Conditions

Distinguishes "CUE as an input-validation layer" from "CUE as a replacement for Helm". A full Helm replacement (Timoni) exists but is a separate, much larger rewrite.

### Evidence

> "CUE makes its input trustworthy; it does not make the template engine safer. Anyone selling this as 'replacing Helm' is overselling it."

### Implications

- Adopting CUE does not reduce risk in the Go-template layer, identified as arguably the most error-prone part of the estate.
- Claims that CUE "replaces Helm" should be treated as incorrect unless a full Timoni-style rewrite is also being proposed.

### Related

- [[SoT - CUE Configuration]]—extends: §6's Ecosystem Isolation risk is the same theme—vendors ship Helm Charts, not CUE modules.
- [[SoT - Strategy - Helm to CUE Migration]]—extends: Phase 2's explicit choice to "keep Helm for K8s resource generation" is this same scope boundary.
- [[Triple-Escaped Vault Secret Templates Are Hand-Written Per Customer]]—extends: names the specific downstream Go-template layer this distinction says CUE does not fix.
