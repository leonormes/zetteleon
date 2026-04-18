---
aliases: [Conservation of Complexity, Software Complexity Law, Tesler's Law]
created: 2026-01-08T12:05:00Z
last_reviewed: 2026-02-05
modified: 2026-04-17T09:25:44+00:00
status: stable
tags: [architecture, complexity, mental_models, software_engineering, sot]
title: SoT - Conservation of Complexity
type: SoT
---

## Minimum Viable Understanding (MVU)

Software complexity obeys a conservation law (Tesler's Law): it cannot be destroyed, only relocated. In any non-trivial system, complexity must reside in one of two primary containers:

1. Control Flow (Code/Time): Logic, branches, loops, and temporal sequences (The "How").
2. Representation (Data/Space): Schemas, types, graphs, and static structures (The "What").

---

## 1. The Core Trade-off

When a developer "worries about data structures" (Torvalds/Pike), they are moving complexity out of the procedural layer and into the structural layer.

| Logic-Heavy (Bad) | Data-Heavy (Good) |
|:--- |:--- |
| Where: Functions, `if/else`, flags. | Where: Types, Schemas, Tables. |
| Mental Model: "Steps to execute." | Mental Model: "Valid states to exist." |
| Fragility: High (Path explosion). | Fragility: Low (Compiler enforcement). |
| Example: `if (isProd) { … }` | Example: `config: ProductionConfig` |

### The "Linus Torvalds" Bridge

> _"Bad programmers worry about the code. Good programmers worry about data structures and their relationships."_—Linus Torvalds

This is not just about using HashMaps vs Arrays. It is about Data Modeling.

- The "Computer Science" View: Optimizing for memory/cpu (Linked Lists, Binary Trees).
- The "Domain" View: Optimizing for correctness (Schema Normalization, Discriminated Unions).

By designing the _shape_ of your data to prohibit invalid states ("Making Illegal States Unrepresentable"), you eliminate the need for defensive code to handle those states.

---

## 2. Practical Application: "DBA Thinking" in Code

Just as a DBA normalizes a database to ensure data consistency, a developer should normalize in-memory structures.

- DBA: "Don't store `UserAddress` in the `Orders` table; reference `UserID`."
- Dev: "Don't store `isValid` boolean next to `Result`; return a `Result | Error` type."

### Case Study: Helm Charts

- The Anti-Pattern: A `values.yaml` full of boolean flags (`enableFeatureX: true`) requiring complex `{{ if }}` logic in templates.
- The Solution: A `values.yaml` defining a _list_ of objects. The template simply iterates over the list. The complexity moves from the _template logic_ to the _data definition_.
- _Reference:_ [[Pattern - Helm Chart as a Compiler]]

---

## 3. Case Study: Cloud Control Planes (AWS Vs Azure)

The two major cloud platforms manage complexity differently, providing a perfect illustration of Tesler's Law.

| Platform | Complexity Location | Analogy | Pros/Cons |
|:--- |:--- |:--- |:--- |
| AWS | Late-Bound (User) | Dynamic Typing (JavaScript) | Pro: High Velocity. "Just run it."<br>Con: Referential integrity is the user's job (Dangling ENIs, Orphaned Volumes). |
| Azure | Early-Bound (Platform) | Static Typing (C#) | Pro: High Integrity. "Compiler checked."<br>Con: High Upfront Friction (Must define Resource Groups, Location, Hierarchy first). |

- AWS prioritizes _local correctness_ (The API call succeeds if the syntax is right).
- Azure prioritizes _global correctness_ (The API call fails if the structural invariants are violated).

Complexity is conserved: You either pay the tax upfront (Azure/Schema Design) or you pay the tax on cleanup (AWS/Garbage Collection).

---

## 4. Cognitive Implications

- Static vs. Dynamic: Humans and machines find it easier to reason about static topology (what things _are_) than dynamic execution (how things _change_).
- Schema Debt: Because data structures often "ossify" (become hard to change once shared), failing to encode complexity in structure _early_ leads to "interest" paid in the form of increasingly complex procedural glue code.

## 4. Relation to LLMs

This law is the foundation for the [[LLM Reasoning Efficiency is Proportional to Structural Constraint|LLM Corollary]]. LLMs are significantly more effective at traversing structure (Knowledge Graphs, Schemas) than simulating execution (simulating a CPU).

---

## Related Knowledge

- [[SoT - Kubernetes Cluster State Architecture]] (K8s shifts complexity to State/etcd).
- [[Pattern - Helm Chart as a Compiler]] (Implementation of this law in DevOps).

## Minimum Viable Understanding (MVU)

### The "Balloon" Analogy (Tesler's Law)

Complexity acts like a balloon. You cannot deflate it (remove it); if you squeeze it in one place, it bulges in another.

- Squeeze the UI (Simple Interface): The "bulge" moves to the internal engineering (complex code).
- Squeeze the Engineering (Simple Code): The "bulge" moves to the user (complex manual configuration).
- The Goal: Move the "bulge" into the Data Structure, where it is rigid, validated, and managed by the compiler, rather than human cognition.

### Philosophical Foundation

- [[SoT - Simple Made Easy (Rich Hickey)]]—_The Axiom._ Simple (one braid) is not Easy (near at hand). Decomplecting logic from state is the primary tool for managing conservation laws.
