---
aliases: [Database and Structures Syllabus, DOP Learning Path, Systems Programming Curriculum]
confidence: 5/5
created: 2025-12-31T00:00:00Z
epistemic: index
last_reviewed: 2025-12-31
modified: 2026-01-08T15:03:28+00:00
purpose: A structured learning path for mastering the Data Structures and Database Internals required for Data-Oriented Design.
review_interval: 3 months
see_also:
  - "[[SoT - Curriculum - Data-Oriented Design]]"
  - "[[SoT - Data-Centric Software Engineering]]"
source_of_truth: []
status: active
tags: [curriculum, database, dop, learning, type/moc]
title: MOC - Data-Oriented Structures & Internals
type: map
uid:
updated:
---

## 1. The Core Curriculum

This syllabus is based on the principle that **"Software is just a Database that hasn't realized it yet."** To write high-performance code, you must learn how Databases store and retrieve data.

### Module A: The Structures (The Vocabulary)

_Goal: Stop using Objects/Nodes. Start using Arrays/Indices._

1. **The Foundation:** **[[SoT - Data-Oriented Programming (DOP)]]**
    - _Concept:_ Structure of Arrays (SoA) vs. Array of Structures (AoS).
2. **The Safe Pointer:** **[[SoT - Slot Map (Generational Arena)]]**
    - _Critical:_ How to safely reference data in an array without garbage collection.
3. **The Toolkit:** **[[SoT - High-Performance Data Structures]]**
    - _Ring Buffers:_ For queues/events.
    - _Flattened Trees:_ For hierarchies.
    - _CSR Graphs:_ For networks.

### Module B: The Internals (The Theory)

_Goal: Understand storage, indexing, and concurrency._

1. **The Database Model:** **[[SoT - Database Internals for Systems Programmers]]**
    - _Storage:_ Why Pages matter (Cache Lines).
    - _Indexing:_ B-Trees (Read) vs. LSM Trees (Write).
    - _Concurrency:_ MVCC (Lock-free reading).
    - _Planning:_ Cost Models and Cardinality.

### Module C: The Practice (The Gym)

_Goal: Write code that proves you understand the above._

1. **Exercises:** **[[SoT - Curriculum - Data-Oriented Design]]**
    - _Level 1:_ State Enforcers (Enums).
    - _Level 2:_ Recursion Killing (Flattened Arrays).
    - _Level 3:_ Composition (ECS-lite).
    - _Level 4:_ Event Sourcing (The Log).

---

## 2. Recommended Reading Order

1. Start with **[[SoT - Data-Oriented Programming (DOP)]]** to understand _Why_.
2. Implement a **[[SoT - Slot Map (Generational Arena)]]** in TypeScript/Rust.
3. Read **[[SoT - Database Internals for Systems Programmers]]** to understand the "Page" model.
4. Attempt the "File System" challenge in **[[SoT - Curriculum - Data-Oriented Design]]** using a **Flattened Tree**.
