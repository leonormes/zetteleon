---
aliases: []
confidence: 5/5
created: 2025-12-22T00:00:00Z
epistemic: architecture
last_reviewed: 2025-12-22
modified: 2025-12-25T18:34:56Z
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

## 2. The Core Curriculum

To cultivate this mindset, one must move beyond syntax and focus on structural mechanics.

### A. Deepen Understanding of Structure

*Goal: Understand the mechanical cost of abstraction.*
- **Trade-off Analysis:** Don't just learn Hash Tables; learn *when* a B-Tree beats a Hash Table (e.g., range queries, disk locality).
- **First-Principles Implementation:** Implement core structures (Linked List, Ring Buffer) from scratch to understand memory layout and pointer indirection.
- **Complexity:** Internalize Big O notation not as math, but as a predictor of scaling behavior.

### B. Practice Data Modelling

*Goal: accurately map reality to bits.*
- **Entity-First Design:** Sketch entities and relationships (ERD) before writing a single function.
- **Access Patterns:** Design structures based on how data is *read* (Read-Heavy vs. Write-Heavy), not just how it looks.
- **Refactoring:** Converting procedural spaghetti code into clean state machines or lookup tables.

### C. Language-Agnostic Thinking

*Goal: Decouple logic from syntax.*
- **Pseudocode:** Solve the problem in abstract logic before committing to a language constraint.
- **Universal Concepts:** Recognize that `List` in Python, `Slice` in Go, and `Vector` in C++ are all just dynamic arrays with different syntax sugar.
- **API Design:** Focus on the *shape* of the data payload (JSON/Protobuf), not the method of transport.

### D. Continuous Analysis

*Goal: Sharpen the mental model.*
- **Open Source Anatomy:** Dissect high-quality codebases (e.g., Redis, SQLite) to see how they organize memory and state.
- **Mental Compilation:** Practice tracing data flow through a system without running the code.

---

## 3. The Implementation Pattern

1. **Define State:** What is the minimum viable data required?
2. **Map Structure:** What is the optimal container (Array, Graph, Map)?
3. **Define Invariants:** What rules must never be broken?
4. **Derive Logic:** Write the code that maintains the invariants and transforms the state.
