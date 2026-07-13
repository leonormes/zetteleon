---
created: 2026-02-01T20:56:02+00:00
last-synthesis: 2026-02-01
modified: 2026-07-13T08:45:10+00:00
permalink: llmeon/30-library/so-t/so-t-complexity-conservation
related:
- - Code vs Data Structures (Torvalds Essay)
source_of_truth: true
tags: [concept/complexity, domain/software-engineering, type/SoT]
title: SoT - Complexity Conservation
---

## Minimum Viable Understanding (MVU)

Software complexity obeys a conservation law: it must reside either in control flow (code/time) or in representation (data structures/space). By shifting complexity into structure, we minimize accidental complexity and maximize the reasoning capacity of both humans and LLMs.

## Working Knowledge

### Core Principles

- [[Software Complexity is Conserved Between Control Flow and Representation]]
- [[LLM Reasoning Efficiency is Proportional to Structural Constraint]]
- [[Minimum Viable Context for LLMs Prevents Hallucination via Structural Boundaries]]
- [[Targeting LLM Attention Requires Encoding Relevance as Structure]]
- [[SoT - LLM Codebase Understanding & Hierarchy]]

## Current Understanding

### Case Study: Federated Medical Research

A practical example of separating structural vs. algorithmic complexity.

The Problem: Analyze post-COVID cardiovascular risk across isolated NHS Trusts without moving patient data.

Complexity Allocation:

- Structural Complexity (Privacy & Governance): Handled by the _Data Architecture_.
    - Nodes hold identifiable data (Invariant: Raw data never leaves).
    - Hub receives only aggregates (Invariant: No PII in wire format).
- Algorithmic Complexity (Statistics): Handled by the _Hub_.
    - Meta-analysis and bias correction are the "irreducible remainder" requiring algorithmic sophistication.

---

### History

- 2026-02-01: Initial synthesis from `HEAD Challenging Data Structures Claim` and `HEAD Ubiquitous Language Consolidation`.
