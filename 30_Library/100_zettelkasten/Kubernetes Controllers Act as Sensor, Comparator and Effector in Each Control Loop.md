---
aliases: []
conformant: true
contradicts: []
created: 2026-09-24T12:00:00+00:00
epistemic_status: medium
evidence_links: []
modified: 2026-09-26T08:45:41+00:00
non_conformance_reason: ''
permalink: llmeon/30-library/100-zettelkasten/kubernetes-controllers-act-as-sensor-comparator-and-effector-in-each-control-loop
prodos.atomic.form: mechanism
prodos.kind: atomic
prodos.lifecycle: seed
proposition: Each Kubernetes controller acts as sensor, comparator and effector, sensing
  actual state, diffing it against desired state and acting on the difference.
source_title: Cybernetic Analysis of Kubernetes State Management (essay captured in
  the vault)
source_url: UNKNOWN
status: seed
tags: [control-loop, controllers, kubernetes]
title: Kubernetes Controllers Act as Sensor, Comparator and Effector in Each Control Loop
type: claim
upstream: '[[Cybernetic Analysis of Kubernetes State Management.]]'
---

## Kubernetes Controllers Act as Sensor, Comparator and Effector in Each Control Loop

Each Kubernetes controller senses the state of its resources, compares it with the desired state to produce an error signal, and acts to correct the difference.

### Scope & Conditions

Applies to the built-in controllers described in the source; the Kubelet also acts as a sensor for node and pod status.

### Evidence

> "Sensor: Kubernetes controllers, along with components like the Kubelet, act as sensors."

> "Comparator: The reconciliation loop within each controller functions as a comparator."

> "Effector: Controllers also serve as effectors."

### Implications

- The diff between spec and status is the error signal.
- Corrective actions are API calls to create, update or delete objects.

### Related

- [[SoT - Kubernetes Cluster State Architecture]]—extends: that SoT describes the reconciliation loop; this atom splits it into the three cybernetic roles
- [[Cybernetics]]—shared mechanism: a loop needs a sensor, a comparator and an effector
