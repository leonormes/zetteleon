---
aliases: [Database and Structures Syllabus, DOP Learning Path, Systems Programming Curriculum]
created: 2025-12-31T00:00:00+00:00
lastreviewed: 2025-12-31
modified: 2026-07-13T08:52:37+00:00
permalink: llmeon/30-library/mo-c/moc-data-oriented-structures-internals
reviewinterval: 3 months
seealso: ["[[SoT - Curriculum - Data-Oriented Design]]", "[[SoT - Data-Centric Software Engineering]]"]
sourceoftruth: []
tags: [curriculum, database, dop, learning, type/moc]
title: MOC - Data-Oriented Structures & Internals
---

## 1. The Core Curriculum

This syllabus is based on the principle that "Software is just a Database that hasn't realized it yet." To write high-performance code, you must learn how Databases store and retrieve data.

### Module A: The Structures (The Vocabulary)

Goal: Stop using Objects/Nodes. Start using Arrays/Indices.

1. The Foundation: [[SoT - Data-Oriented Programming (DOP)]]
    - Concept: Structure of Arrays (SoA) vs. Array of Structures (AoS).
2. The Safe Pointer: [[SoT - Slot Map (Generational Arena)]]
    - Critical: How to safely reference data in an array without garbage collection.
3. The Toolkit: [[SoT - High-Performance Data Structures]]
    - Ring Buffers: For queues/events.
    - Flattened Trees: For hierarchies.
    - CSR Graphs: For networks.

### Module B: The Internals (The Theory)

Goal: Understand storage, indexing, and concurrency.

1. The Database Model: [[SoT - Database Internals for Systems Programmers]]
    - Storage: Why Pages matter (Cache Lines).
    - Indexing: B-Trees (Read) vs. LSM Trees (Write).
    - Concurrency: MVCC (Lock-free reading).
    - Planning: Cost Models and Cardinality.

### Module C: The Practice (The Gym)

Goal: Write code that proves you understand the above.

1. Exercises: [[SoT - Curriculum - Data-Oriented Design]]
    - Level 1: State Enforcers (Enums).
    - Level 2: Recursion Killing (Flattened Arrays).
    - Level 3: Composition (ECS-lite).
    - Level 4: Event Sourcing (The Log).

---

## 2. Recommended Reading Order

1. Start with [[SoT - Data-Oriented Programming (DOP)]] to understand Why.
2. Implement a [[SoT - Slot Map (Generational Arena)]] in TypeScript/Rust.
3. Read [[SoT - Database Internals for Systems Programmers]] to understand the "Page" model.
4. Attempt the "File System" challenge in [[SoT - Curriculum - Data-Oriented Design]] using a Flattened Tree.
