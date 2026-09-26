---
conformant: true
created: 2026-09-23T14:49:00+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-26T08:45:27+00:00
permalink: llmeon/00-inbox/cue-unification-is-a-commutative-deep-merge
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [cue, lattice, unification]
title: CUE Unification Is a Commutative Deep Merge
type: concept
upstream: '[[CUE-ASSESSMENT]]'
---

## CUE Unification Is a Commutative Deep Merge

In CUE, types and values are the same construct, and combining two configurations is a lattice-meet operation that is commutative, associative, and idempotent, so merge order cannot change the result.

### Scope & Conditions

This is CUE's core mechanism, distinct from Helm's text templating and Kustomize's strategic merge patching.

### Evidence

> "Merging is order-independent. There is no 'last file wins' … Merging is deep by default. You never write a deep-merge function."

### Implications

- "-f a.yaml -f b.yaml" ordering bugs, possible in Helm, cannot exist in CUE by construction.
- Deep merging never needs a hand-written merge function.

### Related

- [[Configuration Unification]]—shared mechanism: an existing atomic note covering the same core mechanism from a different source (a CUE conference talk); the two are near-duplicates and worth a consolidation look.
- [[SoT - CUE Configuration]]—extends: §1–2 of that SoT is the fuller theoretical treatment this atom summarises with concrete numbers from a real assessment.
