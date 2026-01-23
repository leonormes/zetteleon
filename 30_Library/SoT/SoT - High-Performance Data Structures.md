---
aliases: ["CSR Graph", "DOP Data Structures", "High-Performance Data Structures", "Implicit Heap", "Ring Buffer"]
confidence: "5/5"
created: 2025-12-31T00:00:00Z
epistemic: "knowledge"
last_reviewed: "2025-12-31"
modified: 2026-01-23T18:09:19+00:00
purpose: "To define the specific data structures required for Data-Oriented Programming, replacing standard 'Node-Based' CS structures."
review_interval: "6 months"
see_also: ["[[SoT - Data-Oriented Programming (DOP)]]", "[[SoT - Slot Map (Generational Arena)]]"]
source_of_truth: []
status: "stable"
tags: ["data_structures", "performance", "rust", "typescript"]
title: SoT - High-Performance Data Structures
type: "SoT"
uid: 
updated: 
---

## 1. The Fundamental Shift: Indices vs. Pointers

Standard CS teaches "Node-Based" structures (Objects pointing to other Objects).

**DOP teaches "Index-Based" structures (Integers pointing to Array Slots).**

- **Why?** CPU Cache. Following a pointer is a random jump in RAM (Cache Miss). Incrementing an integer index is linear (Cache Hit).

---

## 2. The Four Workhorses

### 2.1 Open Addressing Hash Map

Standard Maps (Chaining) use linked lists for collisions.

- **The DOP Way:** **Linear Probing.** If a slot is taken, check the next one. Keep everything in one flat array.
- **Use Case:** High-performance lookups where `malloc` is forbidden.

### 2.2 The Ring Buffer (Circular Queue)

The backbone of all async I/O.

- **Problem:** `Array.shift()` is $O(N)$ because it shifts all elements.
- **Solution:** A fixed-size array with `Head` and `Tail` indices that wrap around.
- **Use Case:** Event queues, Audio buffers, Network packets. Zero allocation after startup.

### 2.3 The Flattened Tree (Implicit Heap)

Used for File Systems, DOMs, and Scene Graphs.

- **Textbook:** `Node { children: Node[] }`. Recursive traversal.
- **DOP:** **Breadth-First Layout** in a flat array.
    - `Root` at 0.
    - `Left Child` = `2 * Index + 1`.
    - `Right Child` = `2 * Index + 2`.
- **Use Case:** traversing a tree mathematically without following a single pointer.

### 2.4 The Graph: CSR (Compressed Sparse Row)

Most real-world data is a graph. Pointer-based graphs explode memory.

- **Technique:** Three integer arrays (`Values`, `Column Indices`, `Row Pointers`) represent millions of connections tightly.
- **Use Case:** Social networks, Logistics routing, GPU meshes.

---

## 3. Implementation Rule

In Rust, implementing a Linked List using pointers (`Option<Box<Node>>`) is a nightmare for the Borrow Checker.

Implementing it using **Indices** (`Vec<Node>` where `next: u32`) is trivial, safe, and faster.

> **Rule:** If you need a complicated data structure, build it inside a `Vec` using integers as handles.
