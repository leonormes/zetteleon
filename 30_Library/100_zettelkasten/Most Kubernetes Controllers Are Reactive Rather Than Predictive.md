---
aliases: []
conformant: true
contradicts: []
created: 2026-09-24T12:00:00+00:00
epistemic_status: medium
evidence_links: []
modified: 2026-09-25T16:29:36+00:00
non_conformance_reason: ''
permalink: llmeon/30-library/100-zettelkasten/most-kubernetes-controllers-are-reactive-rather-than-predictive
prodos.atomic.form: claim
prodos.kind: atomic
prodos.lifecycle: seed
proposition: Most Kubernetes controllers are purely reactive and respond to deviations
  after they occur, with the Horizontal Pod Autoscaler having some predictive capability.
source_title: Cybernetic Analysis of Kubernetes State Management (essay captured in
  the vault)
source_url: UNKNOWN
status: seed
tags: [control-theory, kubernetes, limitations]
title: Most Kubernetes Controllers Are Reactive Rather Than Predictive
type: claim
upstream: '[[Cybernetic Analysis of Kubernetes State Management.]]'
---

## Most Kubernetes Controllers Are Reactive Rather Than Predictive

Most Kubernetes controllers respond to deviations only after they occur; predictive control that anticipates future state is rare, with the Horizontal Pod Autoscaler as a partial exception.

### Scope & Conditions

A limitation the source draws from a cybernetic perspective, contrasting reactive with predictive control.

### Evidence

> "Kubernetes controllers are largely reactive. They respond to deviations after they occur."

> "most core controllers are purely reactive."

### Implications

- There is always a window in which the deviation exists before it is corrected.

### Related

- [[Cybernetics]]—shared mechanism: feedback control corrects error after it appears
- [[SoT - Systems Thinking]]—shared mechanism: delays between action and feedback drive system behaviour
