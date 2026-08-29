---
aliases: [Architecture MOC, MOC - Systems Architecture, System Design Index]
created: 2025-10-31T12:38:00+00:00
exclusions: Data-Level Implementation Details (See [[MOC - Data-Centric Software Engineering]])
modified: 2026-08-29T09:36:31+00:00
permalink: llmeon/30-library/mo-c/moc-software-architecture-principles
scope: Macro-Architecture (System-to-System)
tags: [boundaries, SoftwareEngineering/Architecture, systems_design, type/moc]
title: MOC - Software Architecture Principles
---

## 1. The Core Philosophy (System Integrity)

While [[MOC - Data-Centric Software Engineering]] governs _how_ we build components (Micro), this MOC governs _how_ we connect them (Macro).

> "Architecture is about the important stuff. Whatever that is."—_Ralph Johnson_
> "Architecture represents the significant design decisions that shape a system, where significant is measured by cost of change."—_Grady Booch_

---

## 2. Boundaries & Coupling (The Primary Constraint)

Managing the friction and dependencies between disparate systems.

- [[SoT - Namespacing in Computing]] - The primary mechanism for isolation and collision avoidance at the system level.
- [[Strategic Duplication Reduces System Coupling]] - The conscious decision to copy data (violating DRY) to preserve system independence.
- [[Dependency Problems Create Cascading Failures]] - Understanding the blast radius of shared code.
- [[SoT - Atomicity and Loose Coupling]] - Designing boundaries such that failures are contained (The Bulkhead Pattern).

---

## 3. Information Flow & Interfaces

How systems talk to each other without exposing their internal "Shape".

- [[SoT - Information Hiding (Parnas)]] - The interface must reveal the _intent_, not the _implementation_.
- [[SoT - Parse, Don't Validate]] - The Gateway Principle: Systems should sanitize inputs at the border, not deep within the core.
- [[SoT - The Worse is Better Philosophy]] - The trade-off between Interface Correctness (MIT) and Implementation Simplicity (New Jersey).

---

## 4. Operational Integrity

- [[SoT - Code Duplication and Refactoring]] - Distinguishing "Accidental Duplication" (bad) from "Essential Duplication" (decoupling).
- [[SoT - Pragmatism vs Rigour in Software]] - The decision framework for when to incur Technical Debt for speed.

---

## 5. Architectural Mindset

- [[Decoupling Ego from Outcomes to Improve Decisions]] - The ability to kill your darlings (features/systems) for the greater good.
- [[SoT - Simple Made Easy (Rich Hickey)]] - Architecture is about _decomplecting_ (untangling) concerns, not just making things easy to type.
- [[SoT - Accelerate & DORA]]
