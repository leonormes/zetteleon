---
conformant: true
created: 2026-09-23T14:48:28+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-23T14:56:28+00:00
permalink: llmeon/00-inbox/unvalidated-helm-values-accept-arbitrary-keys-silently
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [configuration-management, failure-mode, helm, validation]
title: Unvalidated Helm Values Accept Arbitrary Keys Silently
type: claim
upstream: '[[CUE-ASSESSMENT]]'
---

## Unvalidated Helm Values Accept Arbitrary Keys Silently

In the absence of a `values.schema.json`, Helm accepts any key in a customer values file, including typos and entirely invented keys, and renders successfully with exit code 0.

### Scope & Conditions

Applies to any Helm chart with no schema file present. Verified directly against a specific platform's `ffnode` chart.

### Evidence

> "`replicaCnt` (a typo of `replicaCount`) and an entirely invented top-level key both pass silently … exit 0, no stderr."

### Implications

- The chart silently falls back to its default value instead of failing the typo'd field.
- The deployment reports success ("green") while running the wrong configuration.

### Related

- [[SoT - CUE Configuration]]—shared mechanism: §3's Failure Modes table contrasts exactly this behaviour against CUE's compile-time equivalent.
- [[SoT - Type-Driven Infrastructure Strategy]]—extends: this is a concrete instance of the runtime-not-synthesis-time validation the "Shift Left" principle argues against.

[supports:: [[SoT - Infrastructure Complexity]], confidence=high]
