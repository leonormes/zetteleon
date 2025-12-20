---
aliases: []
confidence: 5/5
created: 2025-12-17T00:00:00Z
epistemic: 
last_reviewed: 2025-12-17
modified: 2025-12-20T09:54:09Z
purpose: To explain how an organization's communication structure inevitably shapes the technical systems it produces.
related-soTs: ["[[MOC - Socio-Technical Dissonance]]"]
review_interval: 
see_also: []
source: https://gemini.google.com/share/7368b72e8f22
source_of_truth: true
status: stable
tags: [architecture, conways-law, organizational-structure, systems-design]
title: SoT - Conways Law and Structural Mismatch
type: SoT
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> **Conway's Law** is an adage stating that organizations are constrained to produce designs which are copies of their own communication structures. This means a dysfunctional, hierarchical, or siloed social structure will inevitably produce a dysfunctional, monolithic, or fragile technical architecture.

## 2. Core Concepts

The law, articulated by Melvin Conway in 1967, provides a powerful lens for understanding why technical designs often fail for non-technical reasons.

> *"If you have four groups working on a compiler, you'll get a 4-pass compiler."*

### 2.1 Structural Mismatch

A **Structural Mismatch** occurs when the desired technical topology (e.g., a loosely-coupled microservices architecture) is at odds with the social topology of the organization (e.g., a rigid, top-down hierarchy with siloed teams).

If an organization's social structure is characterized by:

- Rigidity and bureaucracy
- Ego-driven decision-making
- Poor cross-functional communication

Then the resulting technical system will likely exhibit traits such as:

- Monolithic and tightly coupled components
- Fragility and resistance to change
- Inefficient data flows that mirror the political landscape

In essence, the social dysfunction of the organization becomes encoded directly into the software architecture, forcing a suboptimal technical outcome regardless of the team's intentions or the actual requirements of the problem.
