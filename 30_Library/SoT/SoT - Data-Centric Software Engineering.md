---
aliases: []
confidence: 5/5
created: 2025-12-22T00:00:00Z
epistemic: architecture
last_reviewed: 2025-12-22
modified: 2025-12-26T18:21:30+00:00
purpose: ">-"
review_interval: 6 months
see_also: []
source_of_truth: []
status: stable
tags: [data-centric]
title: SoT - Data-Centric Software Engineering
type: SoT
uid:
updated:
---

## 1. Definitive Statement

> [!definition] The Core Philosophy
> "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."—**Linus Torvalds**
>
> **Data-Centric Software Engineering** is the discipline of treating **Data Structures** as the primary source of truth and complexity in a system, rendering the **Code** (Logic) as a trivial derivation of that structure.

### The Conservation Law of Complexity
Software complexity obeys a conservation law: it must reside either in the procedural logic (the Code) or the structural representation (the Data).
*   **Code-Centric:** Complexity is handled by imperative logic (nested `if`, flags, loops). Result: Fragile, hard to test.
*   **Data-Centric:** Complexity is encoded in the schema (Graph, Map, Table). Result: "Dumb" code that merely traverses the "Smart" structure.

---

## 2. The Intellectual Lineage

This principle is not an isolated opinion but a fundamental law of computing recognized by generations of architects.

| Luminary | Principle | Quote |
| :--- | :--- | :--- |
| **Fred Brooks** | *Representation is Essence* | "Show me your tables, and I won't usually need your flowcharts; they'll be obvious." |
| **Rob Pike** | *Cognitive Load* | "Data dominates. If you've chosen the right data structures... the algorithms will almost always be self-evident." |
| **Eric Raymond** | *Smart Data / Dumb Code* | "Smart data structures and dumb code works a lot better than the other way around." |

---

## 3. The Hardware Reality: Data-Oriented Design (DOD)

Data-centricity is not just logical elegance; it is a physical requirement of modern hardware.

### The Lie of Object-Oriented Programming (OOP)
OOP organizes data as an **Array of Structures (AoS)** (e.g., `[Ball(x,y,c), Ball(x,y,c)]`). This causes **Cache Pollution**: loading a `Ball` to update its position `x` also loads irrelevant data like color `c` into the CPU cache line.

### The Solution: Structure of Arrays (SoA)
DOD organizes data as contiguous arrays of single attributes (e.g., `[x,x,x]`, `[y,y,y]`).
*   **Cache Locality:** The CPU loads only relevant data.
*   **SIMD:** The CPU can process multiple data points in a single clock cycle.
*   **Result:** Orders of magnitude performance improvement (e.g., 10x more entities in game engines).

---

## 4. Algorithmic Simplification

### Table-Driven Methods
The "Code-Centric" developer writes a "Giant Switch Statement" to handle state. The "Data-Centric" developer uses a **Lookup Table**.
*   **Code:** `if cmd == "SAVE": save()`
*   **Data:** `commands = {"SAVE": save_fn}`. Logic becomes `commands[input]()`.
*   **Benefit:** Cyclomatic complexity drops to 1. New commands are added to data, not code.

---

## 5. Applied Domains (The Pattern in Practice)

The Data-Centric philosophy is not limited to code; it applies to the entire stack.

### A. Version Control (Git)
*   **Problem:** Merging divergent histories.
*   **Code Solution (SVN):** Complex heuristics tracking line numbers.
*   **Data Solution (Git):** A **Directed Acyclic Graph (DAG)** of immutable snapshots. Merging is simply a graph traversal to find a common ancestor. The complexity is in the Graph, not the Merge script.
*   **Deep Dive:** [[SoT - The Data Architecture of Source Control (Git)]]

### B. Infrastructure (Terraform)
*   **Concept:** Infrastructure is not a script; it is a **Data Schema**.
*   **Application:** Treating `config.tf` as a database of "Desirable State" (Maps/Lists) and `main.tf` as the "Renderer" that transforms that state into API calls.
*   **Deep Dive:** [[SoT - Data-Centric Infrastructure (Terraform)]]

### C. Identity (IAM)
*   **Concept:** Authorization is a set intersection between **Identity Data** (Tokens) and **Policy Data** (Bindings).
*   **Application:** Zero Trust architectures rely on rich context datasets rather than static network perimeters.
*   **Deep Dive:** [[SoT - Data-Centric IAM in Zero Trust]]

### D. Networking
*   **Concept:** The network is a distributed system of **State Transport**.
*   **Application:** Routing is simply `Hash(Header) -> Backend`. DNS is a distributed Key-Value store.
*   **Deep Dive:** [[SoT - The Data-Centric Theory of Networking]]

---

## 6. The Core Curriculum

To cultivate this mindset, one must move beyond syntax and focus on structural mechanics.

### A. Deepen Understanding of Structure

*Goal: Understand the mechanical cost of abstraction.*
- **Trade-off Analysis:** Don't just learn Hash Tables; learn *when* a B-Tree beats a Hash Table (e.g., range queries, disk locality).
- **First-Principles Implementation:** Implement core structures (Linked List, Ring Buffer) from scratch to understand memory layout and pointer indirection.
- **Complexity Analysis:** Internalize Big O notation not as math, but as a predictor of scaling behavior.
- **Broaden Models:** Look beyond Relational (SQL). Understand where NoSQL (Document, Key-Value, Graph) models offer superior structural alignment for specific problems.

### B. Practice Data Modelling

*Goal: Accurately map reality to bits.*
- **Entity-First Design:** Sketch entities and relationships (ERD, UML) before writing a single function.
- **Access Patterns:** Design structures based on how data is *read* (Read-Heavy vs. Write-Heavy), not just how it looks.
- **Refactoring:** Converting procedural spaghetti code into clean state machines or lookup tables.
- **Diagramming:** Visualize the data flow. If you can't draw the shape of the data, you don't understand the problem.

### C. Language-Agnostic Thinking

*Goal: Decouple logic from syntax.*
- **Pseudocode:** Solve the problem in abstract logic before committing to a language constraint.
- **Universal Concepts:** Recognize that `List` in Python, `Slice` in Go, and `Vector` in C++ are all just dynamic arrays with different syntax sugar.
- **API Design:** Focus on the *shape* of the data payload (JSON/Protobuf) and how it is consumed, not just the transport method.
- **Pattern Recognition:** Read code in unfamiliar languages to identify the underlying structural patterns common to all computing.

### D. Continuous Analysis

*Goal: Sharpen the mental model.*
- **Open Source Anatomy:** Dissect high-quality codebases (e.g., Redis, SQLite) to see how they organize memory and state.
- **Mental Compilation:** Practice tracing data flow through a system without running the code.
- **Classic Texts:** Engage with foundational texts (e.g., *Introduction to Algorithms*) to ground your understanding in theory.

---

## 7. The Implementation Pattern

1. **Define State:** What is the minimum viable data required?
2. **Map Structure:** What is the optimal container (Array, Graph, Map)?
3. **Define Invariants:** What rules must never be broken?
4. **Derive Logic:** Write the code that maintains the invariants and transforms the state.
