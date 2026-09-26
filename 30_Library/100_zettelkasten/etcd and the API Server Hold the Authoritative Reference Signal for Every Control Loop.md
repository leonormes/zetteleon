---
aliases: []
conformant: true
contradicts: []
created: 2026-09-24T12:00:00+00:00
epistemic_status: medium
evidence_links: []
modified: 2026-09-26T08:45:41+00:00
non_conformance_reason: ''
permalink: llmeon/30-library/100-zettelkasten/etcd-and-the-api-server-hold-the-authoritative-reference-signal-for-every-control-loop
prodos.atomic.form: claim
prodos.kind: atomic
prodos.lifecycle: seed
proposition: In the cybernetic model of Kubernetes, etcd accessed through the API
  server holds the authoritative reference signal for the control loops.
source_title: Cybernetic Analysis of Kubernetes State Management (essay captured in
  the vault)
source_url: UNKNOWN
status: seed
tags: [api-server, etcd, kubernetes]
title: etcd and the API Server Hold the Authoritative Reference Signal for Every Control Loop
type: claim
upstream: '[[Cybernetic Analysis of Kubernetes State Management.]]'
---

## Etcd and the API Server Hold the Authoritative Reference Signal for Every Control Loop

In the cybernetic model, etcd, accessed through the API server, is the central repository of the reference signal that the control loops steer towards.

### Scope & Conditions

Controllers read desired and last-known actual state through the API server rather than from etcd directly.

### Evidence

> "Within our cybernetic model, etcd acts as the central repository of the normative information or reference signal."

> "It's the single point of entry for all state modifications."

### Implications

- Every change passes through one validation, admission and auditing pipeline.
- The declared state in the API is the truth the loops act on.

### Related

- [[etcd stores cluster network state and service configuration]]—extends: that note says what etcd stores; this atom gives its role in the control model
- [[SoT - Kubernetes Cluster State Architecture]]—shared mechanism: the SoT's state-store view of the cluster
