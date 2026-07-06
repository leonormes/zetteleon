---
aliases: [Cognitive Load, Expertise, Schema Theory, Working Memory]
created: 2025-12-07T00:00:00+00:00
last_reviewed: '2025-12-24'
modified: 2026-07-04T10:50:46+00:00
permalink: llmeon/30-library/so-t/so-t-working-memory-schema-theory
status: stable
tags: [learning, psychology, TheHuman/Cognition, TheHuman/Neuroscience]
title: SoT - Working Memory & Schema Theory
type: SoT
updated: null
---

## 2. Core Memory Systems

### A. Working Memory (The Bottleneck)

The active processing unit.

- Phonological Loop: Stores verbal/auditory info (e.g., variable names, verbal instructions). _Limit: ~2 seconds._
- Visuospatial Sketchpad: Stores visual/spatial info (e.g., architecture diagrams, code nesting).
- Central Executive: The "Manager" that focuses attention and switches tasks. _Crucial for debugging._

### B. Long-Term Memory (The Library)

The effectively limitless storage of knowledge.

- Schemas: Interconnected structures of knowledge.
- The Learning Process: Learning is simply the successful transfer of data from WM to LTM schemas.

---

## 3. Schema Theory: The Mechanism of Expertise

Why can an expert read complex code instantly while a novice struggles?

- Novice: Sees `for (int i = 0; i < n; i++)` as 20+ separate characters filling their WM.
- Expert: Sees 1 single chunk ("Standard Loop Schema"), occupying almost zero WM.

Key Insight: Expertise is not "smarter" processing; it is better indexing.

---

## 4. The Programmer's Cognitive Load

Programming is uniquely demanding because it saturates all WM subsystems simultaneously:

1. Variable States: (What does `x` equal now?)
2. Control Flow: (Where did this function come from?)
3. Syntax: (Where does the semicolon go?)
4. Business Logic: (What is this actually supposed to do?)

The Multiple Demand (MD) System:

Neuroscience confirms that programming heavily engages the MD system (frontal/parietal regions), which is the seat of executive function and fluid intelligence. This explains why interruptions are so costly: rebuilding the "House of Cards" in WM takes minutes, but collapsing it takes seconds.

---

## 5. Mitigation Strategies (Managing the Load)

Since we cannot upgrade our biological RAM (especially with ADHD), we must optimize the software.

| Strategy | Mechanism | Action |
|:--- |:--- |:--- |
| Chunking | Compresses data into schemas. | Use descriptive naming (`getUser` vs `func1`) and design patterns. |
| Externalization | Offloads storage to the environment. | Draw diagrams (UML), write comments _before_ code, use a whiteboard. |
| Incrementalism | Reduces active variables. | TDD (Test-Driven Development): Solve one tiny problem at a time. |
| Tooling | Offloads syntax/state tracking. | Use Linters (syntax check) and Debuggers (state tracking) to free up WM. |

---

## 6. Related Components

- [[SoT - Learning Mechanisms]]
- [[SoT - The Extended Mind]]
- [[SoT - ADHD Neurology & Core Concepts]]
- [[SoT - PRODOS (System Architecture)]]
