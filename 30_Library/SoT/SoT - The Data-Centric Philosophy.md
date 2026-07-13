---
aliases: ["Linus's Law", Data Dominates Code, Data-Centric Software Engineering, Data-Oriented Programming, DOD, DOP, The Axiom of Data, The Data-Centric Philosophy]
created: 2025-12-22T00:00:00+00:00
modified: 2026-07-13T08:52:54+00:00
permalink: llmeon/30-library/so-t/so-t-the-data-centric-philosophy
source_of_truth: true
tags: [complexity, data-centric, dod, dop, philosophy, prodos/sot, software-engineering]
title: SoT - The Data-Centric Philosophy
---

## Minimum Viable Understanding (MVU)

Structure is Truth; Code is Derivative. [[SoT - Conservation of Complexity|Software complexity obeys a conservation law (Tesler's Law)]]: it cannot be destroyed, only relocated. It must reside either in the procedural Logic (Code) or the structural Schema (Data). When you "worry about data structures," you move complexity into the static representation, making the dynamic code trivial, robust, and performant.

---

## 1. The Consensus of the Masters

| Architect | Mental Model | The Core Tenet |
|:--- |:--- |:--- |
| Linus Torvalds | Good Taste | "Bad programmers worry about the code. Good programmers worry about data structures and their relationships." |
| Rob Pike | Structural | "Data dominates. If you've chosen the right data structures… the algorithms will almost always be self-evident." |
| Fred Brooks | Relational | "Show me your tables, and I won't usually need your flowcharts; they'll be obvious." |
| Eric Raymond | Unix Philosophy | "Smart data structures and dumb code works a lot better than the other way around." |
| Mike Acton | DOD | "Code models the world? No. Code transforms data." |
| Rich Hickey | Simple/Easy | "Complecting (braiding) state and behavior is the root of all evil." (See: [[SoT - Simple Made Easy (Rich Hickey)]]) |

---

## 2. The Core Architecture: Separate Data from Behavior

To prevent [[SoT - Context Rot|Context Rot]] and [[SoT - Parochial Code|Parochial Code]], the Data-Centric architect adheres to the principles defined in the [[SoT - Type-Driven Development (The Torvalds Loop)|Torvalds Loop]]:

### 2.1 Separate Data from Behavior

- The Rule: Use Anemic Domain Models (where data and logic are decoupled).
- Data: Structs/Records hold _only_ state. They are "dumb" containers.
- Behavior: Logic resides in separate, pure functions that transform data.
- Why: Eliminates the hidden state mutations and side effects of methods. It makes the "Data Flow" visible in the type signature.

### 2.2 Composition Over Inheritance

- The Rule: Rigid class hierarchies are forbidden.
- Mechanism: Build complex types by composing simple structs ([[SoT - Type-Driven Development (The Torvalds Loop)#5. The Trinity: Mathematical Truth|Product Types]]) or choosing between variants ([[SoT - Type-Driven Development (The Torvalds Loop)#5. The Trinity: Mathematical Truth|Sum Types]]).
- Why: Inheritance hides the flow of data; Composition makes it explicit.

---

## 3. The Economics of Schema: Why Data Matters More

Changing code is cheap; changing data is expensive.

- Code Refactoring: A function can be rewritten in an afternoon. Code has low "gravity."
- Schema Debt: Data has mass. Changing a database schema or a public API format involves migrations, downtime, and breaking changes across the entire distributed system.
- The Lesson: "Worrying about data structures" is a risk management strategy. You must get the _hard-to-change_ things right first.

---

## 4. The Litmus Test: "Good Taste"

Linus Torvalds distinguishes "Good Taste" by how a developer handles edge cases.

- Bad Taste: Using conditional logic (`if`) to patch structural gaps. The logic fights the data.
- Good Taste: Using a data structure that absorbs the edge case (e.g., Indirect Pointers or dummy nodes). The logic remains uniform because the structure is complete.

---

## 5. Applied Philosophy: [[SoT - Git|Git's Content-Addressable DAG]]

The architecture of Git is the ultimate proof of this philosophy.

- The Problem: Merging divergent histories is a heuristic nightmare if you only track "file changes" (Code-Centric).
- The Solution: Git tracks the _entire history_ as a Directed Acyclic Graph (DAG) of immutable snapshots.
- The Result: Merging becomes a simple graph traversal problem. The "smart" data structure (Content-Addressable DAG) allows the code to be "dumb" (simple set operations).

---

## Related Knowledge

- Methodology (The Practice): [[SoT - Type-Driven Development (The Torvalds Loop)]]
- Physics (The Hardware): [[SoT - Data-Oriented Design]]
- Mathematics (The Theory): [[MOC - Type Theory]]
- Internals (The Structures): [[MOC - Data-Oriented Structures & Internals]]
- Complexity (The Law): [[SoT - Conservation of Complexity]]
- Information (The Metric): [[SoT - Information Hiding (Parnas)]]
- Execution (The LLM Corollary): [[SoT - LLM Reasoning Obeys the Complexity Conservation Law]]
