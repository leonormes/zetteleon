---
aliases: []
conformant: true
contradicts: []
created: 2026-09-24T12:00:00+00:00
epistemic_status: medium
evidence_links: []
modified: 2026-09-26T08:45:41+00:00
non_conformance_reason: ''
permalink: llmeon/30-library/100-zettelkasten/many-kubernetes-controllers-reacting-to-one-event-can-overload-the-api-server-as-a-thundering-herd
prodos.atomic.form: failure_mode
prodos.kind: atomic
prodos.lifecycle: seed
proposition: Many Kubernetes controllers reacting to one event at once can overload
  the API server as a thundering herd, mitigated by rate limiting and backoff.
source_title: Cybernetic Analysis of Kubernetes State Management (essay captured in
  the vault)
source_url: UNKNOWN
status: seed
tags: [api-server, kubernetes, thundering-herd]
title: Many Kubernetes Controllers Reacting to One Event Can Overload the API Server as a Thundering Herd
  as a Thundering Herd
type: claim
upstream: '[[Cybernetic Analysis of Kubernetes State Management.]]'
---

## Many Kubernetes Controllers Reacting to One Event Can Overload the API Server as a Thundering Herd

When many controllers react to a single event at once, they can overload the API server; rate limiting and backoff in client-go mitigate this but it remains a concern in large or very active clusters.

### Scope & Conditions

Most relevant to very large or very active clusters, per the source.

### Evidence

> "If many controllers react to a single event simultaneously (a "thundering herd"), it can overload the API Server."

> "Rate limiting and backoff mechanisms in client-go (used by controllers) help mitigate this"

### Implications

- Latency and load are properties of the feedback loop, not just of the components.

### Related

- [[SoT - Kubernetes Cluster State Architecture]]—see also: the event-driven watch model the herd arises from
