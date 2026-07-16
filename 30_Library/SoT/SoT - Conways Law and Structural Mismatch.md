---
aliases: []
created: 2025-12-17T00:00:00+00:00
modified: 2026-07-13T08:52:45+00:00
permalink: llmeon/30-library/so-t/so-t-conways-law-and-structural-mismatch
tags: [conways-law, organizational-structure, SoftwareEngineering/Architecture, systems-design]
title: SoT - Conways Law and Structural Mismatch
type: sot
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## 1. Definitive Statement

> [!definition] Definition
> Conway's Law is an adage stating that organizations are constrained to produce designs which are copies of their own communication structures. This means a dysfunctional, hierarchical, or siloed social structure will inevitably produce a dysfunctional, monolithic, or fragile technical architecture.

## 2. Core Concepts

The law, articulated by Melvin Conway in 1967, provides a powerful lens for understanding why technical designs often fail for non-technical reasons.

> _"If you have four groups working on a compiler, you'll get a 4-pass compiler."_

### 2.1 Structural Mismatch

A Structural Mismatch occurs when the desired technical topology (e.g., a loosely-coupled microservices architecture) is at odds with the social topology of the organization (e.g., a rigid, top-down hierarchy with siloed teams).

If an organization's social structure is characterized by:

- Rigidity and bureaucracy
- Ego-driven decision-making
- Poor cross-functional communication

Then the resulting technical system will likely exhibit traits such as:

- Monolithic and tightly coupled components
- Fragility and resistance to change
- Inefficient data flows that mirror the political landscape

In essence, the social dysfunction of the organization becomes encoded directly into the software architecture, forcing a suboptimal technical outcome regardless of the team's intentions or the actual requirements of the problem.
