---
aliases: ["Worse is Better"]
confidence: "5/5"
created: 2025-12-19T00:00:00Z
epistemic: "principle"
last_reviewed: "2025-12-19"
modified: 2026-01-03T10:18:49+00:00
purpose: "To explain the market dynamics that allow simple, less-correct systems to dominate complex, theoretically pure ones."
review_interval: "12 months"
see_also: ["[[SoT - Pragmatism vs Rigour in Software]]"]
source_of_truth: []
status: "stable"
tags: ["market-dynamics", "philosophy", "software-design"]
title: SoT - The Worse is Better Philosophy
type: "SoT"
uid: 
updated: 
---

## 2. The Core Problem: The Market's Selection Filter

The software market does not optimize for theoretical purity or correctness; it optimizes for velocity and adoptability. This creates a selection pressure that favors systems that are "good enough" and easy to start with.

| Failure Mode of "Correct" Systems | The Problem | The "Worse is Better" Advantage |
|:--- |:--- |:--- |
| **High Barrier to Entry** | Rigorous, theoretically pure systems (e.g., Lisp Machines, formal methods) demand significant upfront investment in education and tooling. | **Lowers the bar:** Simple systems can be used by a wider pool of developers, dramatically increasing the rate of software production. |
| **Slow Implementation** | Achieving correctness and a perfect interface is slow and expensive. | **Prioritizes speed:** A simple implementation ships faster, capturing mindshare and creating a network effect. |
| **Incomplete Solutions** | A "correct" system might try to solve 100% of the problem, making it large and complex. | **Solves the common case:** A "worse" system solves 80% of the problem well, making it smaller and more focused. |

---

## 3. The Architecture: The Viral Adoptability Model

The success of "Worse is Better" systems is not an accident; it's a predictable outcome based on a few key architectural traits.

### A. The Mechanics of Spread

1. **Simplicity of Implementation:** The developer can understand and replicate the system easily. This is more important than the simplicity of the interface for the end-user.
2. **Sacrifice Correctness:** The system is willing to make trade-offs, omitting features or corner-case correctness for the sake of implementation simplicity.
3. **Consistency over Completeness:** The system is consistent in its (flawed) model, making it predictable, even if not fully correct.
4. **Initial Portability:** The system is designed to run on common, existing hardware (e.g., Unix on PDP-11s) rather than requiring specialized environments.

---

## 4. Protocols & Implementation

### Protocol: Applying "Worse is Better" for Project Success

*Use when launching a new open-source project, internal tool, or library.*

**Phase 1: Maximize for Initial Adoption**

1. [ ] **Identify the 80% Use Case:** What is the single most common problem users will have? Solve that first.
2. [ ] **Choose Simplicity over Features:** Ruthlessly cut any feature that significantly complicates the initial implementation, even if it's "correct".
3. [ ] **Write a "Getting Started" Guide in 5 Minutes:** If a new developer can't be productive in 5 minutes, the barrier to entry is too high.

**Phase 2: Iterate from a Position of Strength**
4. [] **Let Users Find the Edge Cases:** Once you have a user base, let their needs guide the evolution of the system.
5. [] **Preserve the Simple Core:** As the system grows, protect the simplicity of the original implementation. Add complexity at the edges, not in the core.

---

## 5. Minimum Viable Understanding (MVU)

1. **Speed of adoption is the primary predictor of success.**
2. **To maximize adoption, simplify the implementation above all else.**
3. **Start with a "worse" but simple solution, get users, and let their problems guide the evolution toward a "better" one.**

---

## 6. Open Questions & Tensions

- **Tension:** **The Maintenance Trap.** While "Worse is Better" excels at initial adoption, it can lead to systems that are incredibly expensive to maintain and evolve over the long term, as the initial "incorrect" assumptions become deeply embedded.
- **Tension:** **The Security Cliff.** The "Worse is Better" approach often sacrifices security and robustness for speed, leading to fragile systems that require an entire ecosystem of "band-aids" (firewalls, static analysis, extensive testing) to function safely.

## 7. Related Components

- [[SoT - Pragmatism vs Rigour in Software]]
