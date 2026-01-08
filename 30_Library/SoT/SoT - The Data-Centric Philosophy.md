---
aliases: ["Data Dominates Code", "Linus's Law", "The Data-Centric Philosophy"]
confidence: "5/5"
created: 2025-12-22T00:00:00Z
epistemic: "Fundamental Axiom"
last_reviewed: 
modified: 2026-01-08T10:49:40+00:00
purpose: "To define the core philosophy that Software Complexity is a function of Data Structure, not Code Logic."
review_interval: "1 year"
see_also:
  - "[[MOC - Data-Oriented Design]]"
  - "[[SoT - Type Theory & Data Structures]]"
source_of_truth: []
status: "Stable"
tags: ["complexity", "data-centric", "philosophy", "software-engineering"]
title: SoT - The Data-Centric Philosophy
type: "SoT"
uid: 
updated: 
---

## SoT - The Data-Centric Philosophy

> **The Core Axiom:** "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."—**Linus Torvalds**

### 1. The Conservation of Complexity

Software complexity obeys a conservation law: it must reside either in the procedural **Logic** (Code) or the structural **Schema** (Data).

- **Code-Centric:** Complexity is handled by imperative logic (nested `if`, flags, loops).
    - _Result:_ Fragile, hard to test, state explosion.
- **Data-Centric:** Complexity is encoded in the schema (Graph, Map, Table).
    - _Result:_ "Dumb" code that merely traverses the "Smart" structure.

### 2. The Consensus of the Masters

| Architect | Mental Model | The Core Tenet |
|:--- |:--- |:--- |
| **Linus Torvalds** | **Data-Centric** | "Show me your tables, and I won't usually need your flowcharts; they'll be obvious." (Fred Brooks) |
| **Rob Pike** | **Structural** | "Data dominates. If you've chosen the right data structures... the algorithms will almost always be self-evident." |
| **Mike Acton** | **Data-Oriented** | "The purpose of all programs is to transform data from one form to another." |

### 3. The Litmus Test: Good Taste

Torvalds distinguishes "Good Taste" by how a developer handles edge cases.

- **Bad Taste:** `if (node == head) {... } else {... }`. Logic patches the structure.
- **Good Taste:** `**indirect = &head`. The Data Structure (Pointer-to-Pointer) absorbs the edge case, making the Logic uniform.

**Conclusion:** Complexity in code is a symptom of an insufficient understanding of the data topology.
