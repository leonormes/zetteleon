---
conformant: true
created: 2026-09-23T14:48:26+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-25T16:29:35+00:00
permalink: llmeon/00-inbox/triple-escaped-vault-secret-templates-are-hand-written-per-customer
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [helm, infrastructure-as-code, templating, vault]
title: Triple-Escaped Vault Secret Templates Are Hand-Written Per Customer
type: claim
upstream: '[[CUE-ASSESSMENT]]'
---

## Triple-Escaped Vault Secret Templates Are Hand-Written Per Customer

Vault Secrets Operator templates require Go-template strings escaped through two sequential `tpl` passes, hand-written per key per customer, occurring 405 times across 18 files.

### Scope & Conditions

Applies wherever a chart renders a value with `tpl` and the destination chart applies a second `tpl` pass over the result.

### Evidence

> "405 occurrences of `get.Secrets` across `ffnodes/` … Git history contains `35123f15 Fix opencost-azure secret escaping causing testing app-of-apps sync failure`."

### Implications

- Getting the escaping wrong is a proven, recurring cause of production incidents, not a theoretical risk.
- The escaping rule exists only as tacit knowledge, re-derived by whoever last debugged it.

### Related

- [[SoT - Pattern - CUE Data Architecture]]—shared mechanism: Pattern 1 (The FFNode Refactor) names this exact "Double-Templating" problem—`vaultSecrets: "text: {{.Values.path}}"`—as its motivating case.
- [[SoT - CUE Configuration]]—extends: §6's Export/Import Friction risk is the general version of this specific escaping failure.

[supports:: [[SoT - Infrastructure Complexity]], confidence=high]
