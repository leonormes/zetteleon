---
aliases: ["Data Dominates Code", "Data-Centric Software Engineering", "Data-Oriented Programming", "DOD", "DOP", "Linus's Law", "The Data-Centric Philosophy"]
created: 2025-12-22T00:00:00Z
last_synthesis: 2026-02-03
modified: 2026-02-04T07:26:59+00:00
source_of_truth: true
status: evergreen
synthesis-count: 2
tags: ["complexity", "data-centric", "dod", "dop", "philosophy", "prodos/sot", "software-engineering"]
title: SoT - The Data-Centric Philosophy
trust-level: stable
type: "SoT"
---

## Minimum Viable Understanding (MVU)

Structure is Truth; Code is Derivative. Software complexity obeys a conservation law: it must reside either in the procedural Logic (Code) or the structural Schema (Data). When you "worry about data structures," you move complexity into the static representation, making the dynamic code trivial, robust, and performant.

---

## 1. The Consensus of the Masters

| Architect | Mental Model | The Core Tenet |
|:--- |:--- |:--- |
| Linus Torvalds | Data-Centric | "Bad programmers worry about the code. Good programmers worry about data structures and their relationships." |
| Rob Pike | Structural | "Data dominates. If you've chosen the right data structures… the algorithms will almost always be self-evident." |
| Fred Brooks | Relational | "Show me your tables, and I won't usually need your flowcharts; they'll be obvious." |
| Eric Raymond | Unix Philosophy | "Smart data structures and dumb code works a lot better than the other way around." |

---

## 2. The Economics of Schema: Why Data Matters More

Changing code is cheap; changing data is expensive.

- Code Refactoring: A function can be rewritten in an afternoon. Code has low "gravity."
- Schema Debt: Data has mass. Changing a database schema or a public API format involves migrations, downtime, and breaking changes across the entire distributed system.
- The Lesson: "Worrying about data structures" is a risk management strategy. You must get the _hard-to-change_ things right first.

---

## 3. Case Study: Git's DAG

The architecture of Git is the ultimate proof of this philosophy.

- The Problem: Merging divergent histories is a heuristic nightmare if you only track "file changes" (Code-Centric).
- The Solution: Git tracks the _entire history_ as a Directed Acyclic Graph (DAG) of immutable snapshots.
- The Result: Merging becomes a simple graph traversal problem. The "smart" data structure (Content-Addressable DAG) allows the code to be "dumb" (simple set operations), enabling Git to be orders of magnitude faster and safer than its predecessors.

---

## 4. Fundamental Principles & Applications

### 4.1 Table-Driven Methods

Replace complex control flow (Cyclomatic Complexity) with Data Lookups.

- Bad: A "Giant Switch Statement" (Logic) to handle commands.
- Good: A "Dictionary/Map" (Data) mapping command strings to function pointers.
- Result: Adding a new command requires _zero_ code changes to the dispatcher, only a new data entry.

### 4.2 Parse, Don't Validate

Instead of checking data validity at every step using booleans, parse raw input into a specific Type that _proves_ validity by its very existence. Make invalid states unrepresentable.

### 4.3 Machine Sympathy (DOD)

Align the data layout with the hardware reality (CPU Caches).

- Structure of Arrays (SoA): Store homogenous data contiguously (e.g., all `Positions` together). This maximizes cache line utilization and enables SIMD.
- Array of Structures (AoS): The typical OOP pattern (`class Ball { pos, color }`). This pollutes the cache with irrelevant data when processing only one attribute.

---

## 5. The Litmus Test: "Good Taste"

Torvalds distinguishes "Good Taste" by how a developer handles edge cases.

- Bad Taste: Using conditional logic (`if`) to patch structural gaps. The logic fights the data.
- Good Taste: Using a data structure that absorbs the edge case (e.g., Indirect Pointers or dummy nodes). The logic remains uniform because the structure is complete.

---

## Related Knowledge

- Methodology: [[SoT - Type-Driven Development (The Torvalds Loop)]] (How to execute this).
- Hardware: [[SoT - Data-Oriented Design]] (The physical implementation).
- Physics: [[SoT - Complexity Conservation]] (Tesler's Law).
# ## Minimum Viable Understanding (MVU)

### Design Principles
- [[SoT - Simple Made Easy (Rich Hickey)]]: Advocates for "Decomplecting"—untangling data, logic, and state to ensure components can be composed without braid-induced fragility.
