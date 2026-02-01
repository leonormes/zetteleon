---
aliases: [Law of Conservation of Complexity, Tesler's Law]
created: 2026-01-31T00:00:00+00:00
last_reviewed:
modified: 2026-02-01T15:08:00+00:00
status: evergreen
tags: [architecture, complexity, system-design]
title: SoT - Conservation of Complexity
type: SoT
updated:
---

## The Core Insight

> Software complexity is conserved: it must reside either in control flow (code) or in representation (data structures), and systems become simpler, safer, and more scalable when complexity is pushed into structure.

## 1. Tesler's Law (The Balloon Metaphor)

Every application has an inherent amount of complexity that cannot be removed or hidden. It can only be moved.

- **If the User experiences simplicity**, the System must carry the complexity (UI vs. Backend).
- **If the Code is simple**, the Data Structures must be complex/rich (Torvalds' Principle).

## 2. The Choice of Container: Code vs. Data

Linus Torvalds: _"Bad programmers worry about the code. Good programmers worry about data structures and their relationships."_

| Feature | Complexity in Code (Logic) | Complexity in Data (Structure) |
| --- | --- | --- |
| **Nature** | Dynamic / Temporal | Static / Topological |
| **Cognitive Load** | High (must simulate execution) | Low (can inspect schema) |
| **Constraints** | Implicit (hidden in `if` checks) | Explicit (Enums, Types, Schemas) |
| **Scalability** | Combinatorial Explosion | Linear / Graph expansion |

**Sustainability Heuristic:** Complexity belongs where it can be named, constrained, and inspected. That place is almost always **Data**.

## 3. Dimensions of Complexity

### A. Objective (The System)

- **Kolmogorov Complexity:** The length of the shortest possible description of the system. This defines the "Irreducible Floor."
- **Cyclomatic Complexity:** The number of linearly independent paths through code. High scores indicate logic that has bypassed structural containment.

### B. Subjective (The Observer)

- **Essential Complexity:** Difficulty inherent in the problem itself (e.g., tax law). Cannot be reduced.
- **Accidental Complexity:** Difficulty created by poor tools or architecture. Must be eliminated.
- **Chunking:** The ability of a specialist to group multiple parts into a single mental unit. Complexity hasn't vanished; it is stored in the observer's mental model.

## 4. Diagnostic Heuristic

> "Is this logic compensating for missing structure?"

If yes, you are paying interest on **Schema Debt**.

**Common Smells:**
- Large `if/elif` ladders → missing tables/polymorphism.
- Boolean flags tracking state → missing state machine.
- Defensive null checks everywhere → invalid states allowed by schema.
- "Special cases" → broken representation.
