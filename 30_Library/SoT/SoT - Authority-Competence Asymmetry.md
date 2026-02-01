---
aliases: ["Epistemic Trespassing", "Expert Authority", "HiPPO Effect", "Positional Authority"]
created: 2025-12-17T00:00:00Z
last_reviewed: "2026-01-10"
modified: 2026-02-01T15:08:02+00:00
status: "stable"
tags: ["authority", "bias", "decision-making", "leadership", "social-dynamics", "team-dynamics"]
title: SoT - Authority-Competence Asymmetry
type: "SoT"
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> Authority-Competence Asymmetry is a state of organizational dysfunction where there is a mismatch between who holds the power to make decisions (Positional Authority) and who has the knowledge required to make those decisions correctly (Expert Authority).

This asymmetry manifests as Signal Degradation, where the correct technical solution (the signal) is diluted or overridden by the noise of authority bias.

## 2. Core Concepts

In an efficient system, authority and competence are tightly coupled. The person responsible for a decision is also the most knowledgeable in that specific domain. However, in many organizations, this is decoupled.

### 2.1 Types of Authority

- Positional Authority: Power derived from a title or position within an organizational hierarchy (e.g., Tech Lead, CEO, Manager). This authority is granted by the organization.
- Expert Authority: Power derived from demonstrated knowledge, skill, and experience in a specific domain. This authority is earned and recognized by peers.

### 2.2 The Conflict Mechanism

The asymmetry occurs when Positional Authority overrides Expert Authority. This leads to a decoupled feedback loop: the person making the decision (the manager or lead) does not directly bear the immediate cost or friction of a flawed implementation. The developer or engineer (the Agent) is aware that the plan is suboptimal but is forced by the incentive structure (the hierarchy) to comply.

## 3. Manifestations

### 3.1 The HiPPO Effect

- Acronym: Highest Paid Person's Opinion.
- Mechanism: The anti-pattern where the opinion of the most senior person in the room is automatically given more weight, regardless of their actual knowledge of the subject.
- Result: A failure of data governance, replacing empirical evidence and expert analysis with rank-based authority.

### 3.2 Epistemic Trespassing

- Definition: The error of assuming that competence in one domain (e.g., business management, finance) automatically confers competence in another, unrelated domain (e.g., software architecture, database design).
- Example: When a C-level executive without a technical background dictates a specific database schema or architectural pattern.
- Result: Decisions driven by individuals who are not qualified to make them, leading to Accidental Social Complexity.

## 4. Consequences

- Principal-Agent Problem: A decoupling of decision-making from decision-consequences.
- Signal Degradation: Technical reality is ignored in favor of political or hierarchical convenience.
- Inefficiency & Morale: Experts are disempowered, leading to "malicious compliance" or disengagement.
