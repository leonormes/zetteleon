---
aliases: ["Data Dominates Code", "Data-Centric Software Engineering", "Data-Oriented Programming", "DOD", "DOP", "Linus's Law", "The Data-Centric Philosophy"]
created: 2025-12-22T00:00:00Z
last_reviewed: "2026-01-10"
modified: 2026-02-01T15:07:50+00:00
status: "stable"
tags: ["complexity", "data-centric", "dod", "dop", "philosophy", "software-engineering"]
title: SoT - The Data-Centric Philosophy
type: "SoT"
---

## 1. Definitive Statement

> [!definition] The Core Axiom
> "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."—Linus Torvalds

The Data-Centric Philosophy posits that software complexity is a function of data structure, not code logic. If the data schema is correctly mapped to the problem domain and hardware reality, the resulting algorithms become trivial, self-evident, and robust.

---

## 2. The Conservation of Complexity

Software complexity obeys a conservation law: it must reside either in the procedural Logic (Code) or the structural Schema (Data).

- Code-Centric Approach: Complexity is handled by imperative logic (nested `if` statements, state flags, loops). This leads to fragile systems, "state explosion," and high maintenance load.
- Data-Centric Approach: Complexity is encoded into the schema (Graphs, Maps, Tables, Types). This results in "dumb" code that merely traverses or transforms "smart" structures.

---

## 3. The Consensus of the Masters

| Architect | Mental Model | The Core Tenet |
|:--- |:--- |:--- |
| Linus Torvalds | Data-Centric | "Data structures, not algorithms, are central to computer science." |
| Rob Pike | Structural | "Data dominates. If you've chosen the right data structures… the algorithms will almost always be self-evident." |
| Mike Acton | Data-Oriented | "The purpose of all programs is to transform data from one form to another. Understand the data first." |
| Fred Brooks | Relational | "Show me your tables, and I won't usually need your flowcharts; they'll be obvious." |

---

## 4. Fundamental Principles

### 4.1 Separation of Data and Logic

Data and behavior should be strictly decoupled. Data structures should be "transparent" (public fields, simple types), while logic should consist of stateless functions that transform these structures.

### 4.2 Parse, Don't Validate

Instead of checking data validity at every step using booleans or assertions, parse raw input into a specific Type that _proves_ validity by its very existence. Make invalid states unrepresentable.

### 4.3 Machine Sympathy (DOD)

Data-Oriented Design (DOD) focuses on the hardware's reality:

- Cache Locality: Use Structure of Arrays (SoA) instead of Array of Structures (AoS) to ensure contiguous memory access and 100% cache line utility.
- SIMD Ready: Contiguous data allows for Single Instruction, Multiple Data (SIMD) optimizations, providing 10x performance gains over "Clean Code" OOP patterns.

### 4.4 The Database Mindset

Treat application state as an in-memory relational database. Entities are IDs (Primary Keys), properties are Columns (Arrays), and logic consists of "Queries" and "Joins" over these collections.

---

## 5. The Litmus Test: "Good Taste"

Torvalds distinguishes "Good Taste" by how a developer handles edge cases.

- Bad Taste: Using conditional logic to patch structural gaps (e.g., `if (node == head) { … }`). The logic is fighting the data.
- Good Taste: Using a data structure that absorbs the edge case (e.g., Indirect Pointers or dummy nodes). The logic remains uniform because the structure is complete.

---

## 6. Minimum Viable Understanding (MVU)

1. Understand the Data: You do not understand a problem until you can visualize the data's layout in memory.
2. Logic is a Derivative: Complexity in code is a symptom of an insufficient understanding of the data topology.
3. Efficiency is Structural: Performance is not a hack; it is a consequence of choosing the right structural representation for the hardware.
