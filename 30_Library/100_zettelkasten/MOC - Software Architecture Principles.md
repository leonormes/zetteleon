---
aliases: ["MOC - Systems Architecture", "System Design Index", "Architecture MOC"]
confidence: "5/5"
created: 2025-10-31T12:38:00Z
epistemic: "The principles of designing High-Cohesion, Low-Coupling Systems."
exclusions: "Data-Level Implementation Details (See [[MOC - Data-Centric Software Engineering]])"
last_reviewed: "2025-12-31"
modified: 2025-12-31T12:05:00+00:00
purpose: "To organize principles regarding System Boundaries, Coupling, and Integration."
review_interval: "180"
scope: "Macro-Architecture (System-to-System)"
see_also: ["[[MOC - Data-Centric Software Engineering]]"]
source_of_truth: []
status: "active"
tags: ["architecture", "systems_design", "boundaries", "moc"]
title: MOC - Software Architecture Principles
type: "map"
uid: 
updated: 
---

## 1. The Core Philosophy (System Integrity)

While **[[MOC - Data-Centric Software Engineering]]** governs *how* we build components (Micro), this MOC governs *how* we connect them (Macro).

> "Architecture is about the important stuff. Whatever that is." — *Ralph Johnson*
> "Architecture represents the significant design decisions that shape a system, where significant is measured by cost of change." — *Grady Booch*

---

## 2. Boundaries & Coupling (The Primary Constraint)

Managing the friction and dependencies between disparate systems.

- **[[SoT - Namespacing in Computing]]** - The primary mechanism for isolation and collision avoidance at the system level.
- **[[Strategic Duplication Reduces System Coupling]]** - The conscious decision to copy data (violating DRY) to preserve system independence.
- **[[Dependency Problems Create Cascading Failures]]** - Understanding the blast radius of shared code.
- **[[SoT - Atomicity and Loose Coupling]]** - Designing boundaries such that failures are contained (The Bulkhead Pattern).

---

## 3. Information Flow & Interfaces

How systems talk to each other without exposing their internal "Shape".

- **[[SoT - Information Hiding (Parnas)]]** - The interface must reveal the *intent*, not the *implementation*.
- **[[SoT - Parse, Don't Validate]]** - The Gateway Principle: Systems should sanitize inputs at the border, not deep within the core.
- **[[SoT - The Worse is Better Philosophy]]** - The trade-off between Interface Correctness (MIT) and Implementation Simplicity (New Jersey).

---

## 4. Operational Integrity

- **[[SoT - Code Duplication and Refactoring]]** - Distinguishing "Accidental Duplication" (bad) from "Essential Duplication" (decoupling).
- **[[SoT - Pragmatism vs Rigour in Software]]** - The decision framework for when to incur Technical Debt for speed.

---

## 5. Architectural Mindset

- **[[Decoupling Ego from Outcomes to Improve Decisions]]** - The ability to kill your darlings (features/systems) for the greater good.
- **[[SoT - Simple Made Easy (Rich Hickey)]]** - Architecture is about *decomplecting* (untangling) concerns, not just making things easy to type.