---
aliases: [Law of Conservation of Complexity, Tesler's Law, Complexity Budget]
created: 2026-01-31T00:00:00+00:00
last_reviewed: 
modified: 2026-02-01T17:05:00+00:00
status: evergreen
tags: [architecture, complexity, system-design, mental-model]
title: SoT - Conservation of Complexity
type: SoT
updated: 
---

## The Core Insight

> Software complexity is conserved: it must reside either in control flow (code), in representation (data structures), or in the user's cognitive load. Systems become simpler, safer, and more scalable when complexity is pushed into **Structure** (Data) rather than **Process** (Code).

## 1. Tesler's Law (The Balloon Metaphor)

Every application has an inherent amount of complexity that cannot be removed or hidden. It can only be moved.

-   **The User Trade-off:** If the *User* experiences simplicity (e.g., a one-button interface), the *System* must carry the burden of interpreting intent.
-   **The Engineer Trade-off:** If the *Code* is simpler (generic lists), the *Logic* must be complex to handle it. If the *Data Structure* is complex (rich types), the *Code* becomes trivial.

## 2. The Choice of Container: Code vs. Data

Linus Torvalds: _"Bad programmers worry about the code. Good programmers worry about data structures and their relationships."_

| Feature | Complexity in Code (Logic) | Complexity in Data (Structure) |
| :--- | :--- | :--- |
| **Nature** | Dynamic / Temporal | Static / Topological |
| **Cognitive Load** | High (must simulate execution) | Low (can inspect schema) |
| **Constraints** | Implicit (hidden in `if` checks) | Explicit (Enums, Types, Schemas) |
| **Scalability** | Combinatorial Explosion | Linear / Graph expansion |

**Sustainability Heuristic:** Complexity belongs where it can be named, constrained, and inspected. That place is almost always **Data**.

## 3. Dimensions of Complexity

### A. Objective (The System)

-   **Kolmogorov Complexity:** The length of the shortest possible description of the system. This defines the "Irreducible Floor."
-   **Cyclomatic Complexity:** The number of linearly independent paths through code. High scores indicate logic that has bypassed structural containment.

### B. Subjective (The Observer)

-   **Essential Complexity:** Difficulty inherent in the problem itself (e.g., UK Tax Law). Cannot be reduced, only managed.
-   **Accidental Complexity:** Difficulty created by poor tools, "spaghetti code," or tech debt. Must be eliminated.
-   **Cognitive Chunking:** A specialist perceives a car engine as 4 subsystems; a novice sees 200 parts. Complexity is "reduced" via **Abstraction** (internal mental models), but the objective complexity remains.

### C. Business Complexity (Semantic Density)

How do we measure the complexity of a domain?

1.  **Cynefin Framework:** Is the problem Simple (Categorize), Complicated (Analyze), or Complex (Probe)? >50% Complex = Core Domain.
2.  **Semantic Density:** High vocabulary size + High ambiguity (e.g., "Customer" means different things to Sales vs. Support) = High Complexity.
3.  **Invariant Count:** The number of rules that *must always be true* for an entity. High invariant count requires State Machines (Structure), not boolean flags (Logic).

## 4. Physics vs. Systems Context

Unlike Physics, where "Conservation" is a fundamental law of the universe, Tesler's Law is an empirical heuristic.

| Concept | Physics (Thermodynamics) | Systems (Tesler's Law) |
| :--- | :--- | :--- |
| **Principle** | **Unitarity / 2nd Law:** Information is conserved; Entropy (disorder) increases. | **Conservation:** Complexity is fixed; it only shifts location. |
| **Mechanism** | Energy flow. | Trade-off between Developer effort vs. User effort. |
| **Goal** | Describe the universe. | Minimize cognitive load / Maximize maintainability. |

## 5. Diagnostic Heuristic

> "Is this logic compensating for missing structure?"

If yes, you are paying interest on **Schema Debt**.

**Common Smells:**

-   Large `if/elif` ladders → missing tables/polymorphism.
-   Boolean flags tracking state → missing state machine.
-   Defensive null checks everywhere → invalid states allowed by schema.
-   "Special cases" → broken representation.

See Also: [[SoT - Data-Oriented Design]], [[SoT - Infrastructure Complexity Management]]
