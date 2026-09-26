---
conformant: false
created: 2026-09-18T00:00:00+00:00
created_utc: 2026-09-18T00:00:00Z
modified: 2026-09-25T16:29:16+00:00
non_conformance_reason: "missing schema field definition for type concept (required when conformant - true); missing schema field distinguishes_from for type concept (required when conformant - true); missing schema field used_in_claims for type concept (required when conformant - true)"
permalink: llmeon/30-library/100-zettelkasten/a-single-system-image-presents-a-distributed-resource-pool-as-one-unified-system
prodos.atomic.form: definition
prodos.kind: atomic
source_title: Defining One Computer Concept
status: seed
tags: [cloud, computer-science, distributed-systems]
title: A Single System Image Presents a Distributed Resource Pool as One Unified System
type: concept
---

## A Single System Image Presents a Distributed Resource Pool as One Unified System

A Single System Image (SSI) is a middleware/management layer that presents a collection of distributed, potentially heterogeneous physical resources as one unified, more powerful computing resource to the user or application—hiding the underlying distribution so a large cluster appears as "one system" for purposes like job scheduling or resource management, even though distinct kernels are still running underneath.

### Scope & Conditions

Describes the user-facing unification SSI middleware provides, not any single specific implementation. The distinct kernels and network communication it hides are still real—SSI is a presentation layer, not a change to the underlying logical-computer boundaries.

### Evidence

> "In some cloud and cluster environments, middleware and management layers create a Single System Image (SSI). SSI presents a collection of distributed, potentially heterogeneous resources as a single, unified, and more powerful computing resource to the user or application… making a large cluster appear as 'one system' for specific purposes like job scheduling or resource management."

### Implications

- SSI is the general pattern behind [[SoT - The Logical Definition of a Computer]]'s "Kubernetes Cluster | N Boxes | 'One System'" row: that row is one concrete instance (API server + control plane) of the broader SSI idea, not a special case invented for Kubernetes.
- Because SSI only hides distribution at the presentation layer, the fallacies of distributed computing (partial failure, network unreliability) that apply to the underlying nodes don't go away just because the system looks unified from outside.

### Related

- [[SoT - The Logical Definition of a Computer]]—extends: generalises that SoT's Kubernetes Cluster row (a distributed system with an API/Control Plane presented as "One System") into the broader SSI concept it's an instance of. [extends:: [[SoT - The Logical Definition of a Computer]], strength=3, confidence=high]
