---
type: lib-sot
title: SoT - PRODOS - Problem Architecture
status: stable
confidence: 5/5
tags: [source/lib, system_design, problem_solving]
---


## 1. Definitive Statement
> [!definition] Definition of a Problem
> A problem exists **if and only if** there is a distinct gap between the **Current State** ($S_c$) and the **Desired State** ($S_d$), and the method to bridge that gap is **unknown**.
>
> $$Problem = (S_d - S_c) + Uncertainty$$

## 2. Taxonomy of Challenges

| Type | Definition | PRODOS Strategy |
| :--- | :--- | :--- |
| **Problem** | Gap + Unknown Path. | **HEAD Note**. Structure the gap, hypothesize the path. |
| **Task** | Gap + Known Path. | **Kinetic Action**. Execute immediately. |
| **Constraint** | Unchangeable Variable. | **Boundary Condition**. Optimise *around* it; do not try to solve it. |
| **Situation** | Reality with no Desired State. | **Acceptance**. If there is no goal, there is no problem. |

## 3. The Constraint Protocol
Constraints reduce the **Search Space** of a problem. They are helpful filters, not just blockers.

* **Hard Constraint:** Binary. Must be satisfied (e.g., "Must run on Linux").
* **Soft Constraint:** Gradient. Penalised if violated (e.g., "Should be written in Go").

## 4. Verification Log
* **Source:** Systems Thinking Principles / Kepner-Tregoe Analysis.
* 