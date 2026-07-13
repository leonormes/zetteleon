---
aliases: [B-Trees vs LSM, Database Internals, MVCC, Query Planning, Storage Engines]
created: 2025-12-31T00:00:00+00:00
modified: 2026-07-13T08:52:45+00:00
permalink: llmeon/30-library/so-t/so-t-database-internals-for-systems-programmers
tags: [database, internals, learning, performance, SoftwareEngineering/Architecture]
title: SoT - Database Internals for Systems Programmers
---

## 1. The Core Thesis

> "Don't learn SQL. Learn Storage Engines."

For a Data-Oriented Programmer, a Database is not a black box; it is the ultimate example of Data-Centric Engineering. The techniques used to build Postgres or Cassandra (managing disk I/O, packing memory, concurrency) are the exact same techniques used to build high-performance game engines and system tools.

---

## 2. Storage Layouts (The "Page" Model)

Databases don't read bytes; they read Pages (usually 4KB or 8KB blocks). This maps 1:1 to CPU Cache Lines (64 bytes).

### 2.1 Slotted Pages

How do you pack variable-length data (strings) into a fixed-size block without fragmentation?

- Technique: Grow headers from the front, data from the back.
- DOP Application: Writing custom memory allocators or serializing network packets efficiently.

---

## 3. Indexing Data Structures

You know Arrays and HashMaps. These are the structures for when data is Sorted or Too Big for RAM.

### 3.1 The B-Tree / B+ Tree (Read-Optimized)

The standard for disk-based indexing.

- Structure: "Fat and Short." High fan-out (hundreds of children) to minimize pointer chasing (disk seeks).
- DOP Application: Spatial partitioning (QuadTrees/Octrees) are specialized B-Trees.

### 3.2 The LSM Tree (Write-Optimized)

_Log-Structured Merge-Tree._ Used in high-write systems (Cassandra, RocksDB).

- Mechanism: Treats storage as an Append-Only Log. Writes go to memory (MemTable), then flush to disk (SSTable). Background threads merge these files.
- DOP Application: Handling massive event streams or telemetry logs without locking the UI thread.

---

## 4. Query Planning (The "Cost Model")

When you run a SQL query, the DB calculates the "Cost" of options based on Cardinality (Selectivity).

- Option A: Scan whole table (Slow read, linear access).
- Option B: Use Index (Fast lookup, random access).
- The Switch: If reading >10% of data, a Scan is faster than an Index.
- DOP Application: Level of Detail (LOD). If you have 10 particles, run high-fidelity physics. If you have 10,000, switch to cheap approximation.

---

## 5. Concurrency: MVCC

How do you read data while someone else is writing it, without locks?

- MVCC (Multi-Version Concurrency Control): Never overwrite data. Create a new "Version".
    - Readers see `Version 1`.
    - Writers create `Version 2`.
- DOP Application: Solving Race Conditions in multi-threaded simulation engines without using Mutexes (which kill performance).

---

## 6. The Reading List (The Sacred Texts)

1. Designing Data-Intensive Applications (Martin Kleppmann): The bridge between systems and architecture. (Chapters 1, 3, 5).
2. Database Internals (Alex Petrov): A deep dive into storage engine code.
