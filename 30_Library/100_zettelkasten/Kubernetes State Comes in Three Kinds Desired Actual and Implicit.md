---
aliases: []
conformant: true
created: 2026-09-24T12:00:00+00:00
definition: Kubernetes state is of three kinds, namely desired state declared by users
  in an object spec, actual state (the reported status, granular conditions and the
  real-world condition of running components), and implicit state derived from relationships
  and metadata such as owner references, label selectors and finalizers.
distinguishes_from: ["[[etcd stores cluster network state and service configuration]]"]
modified: 2026-09-26T08:45:41+00:00
non_conformance_reason: ''
permalink: llmeon/30-library/100-zettelkasten/kubernetes-state-comes-in-three-kinds-desired-actual-and-implicit
prodos.atomic.form: distinction
prodos.kind: atomic
prodos.lifecycle: seed
source_title: Cybernetic Analysis of Kubernetes State Management (essay captured in
  the vault)
source_url: UNKNOWN
status: seed
tags: [classification, kubernetes, state]
title: Kubernetes State Comes in Three Kinds Desired Actual and Implicit
type: concept
upstream: '[[Cybernetic Analysis of Kubernetes State Management.]]'
used_in_claims: []
---

## Kubernetes State Comes in Three Kinds Desired Actual and Implicit

Kubernetes state is of three kinds: desired state declared in an object's spec, actual state (reported status, conditions and the real-world condition of nodes, pods and networking), and implicit state derived from relationships and metadata.

### Scope & Conditions

From the source's account of the nature and locus of state. It goes beyond treating etcd as only a database.

### Evidence

> "Desired State: This is explicitly defined by users in the spec section of Kubernetes objects"

> "Implicit State: This is derived from the relationships and metadata within the system."

### Implications

- Owner references form the dependency graph between controllers and objects.
- Label selectors define dynamic groupings that feed services and replica sets.

### Related

- [[SoT - Kubernetes Cluster State Architecture]]—extends: the SoT covers spec and status; this atom adds the implicit kind
- [[etcd stores cluster network state and service configuration]]—shared mechanism: etcd holds the durable desired and reported state
