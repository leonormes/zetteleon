---
aliases: [Data-Centric Software Engineering, DOD, Anemic Domain Model, Data-Oriented Manifesto]
tags: [software-architecture, design-principle, data-oriented, rust]
created: 2026-01-30T09:00:00+00:00
modified: 2026-01-30T11:30:00+00:00
---

# Data-Oriented Design

**Data-Oriented Design (DOD)** is the architectural axiom that **Data is Truth; Code is Derivative.** Unlike Object-Oriented Design (OOD), which couples data with behavior (Classes), DOD separates them completely to optimize for both hardware performance (CPU Cache) and cognitive clarity (Simplicity).

## The Core Philosophy: The Conservation of Complexity

Software complexity obeys a conservation law: it must reside either in the **Procedural Logic** (The Code) or the **Structural Representation** (The Data).
*   **Code-Centric:** "Smart Code" + "Dumb Data" = Fragile, Complex, Hard to Test.
*   **Data-Centric:** "Smart Data" + "Dumb Code" = Robust, Simple, Self-Documenting.

> [!quote] The Lineage of Truth
> *   **Fred Brooks (1975):** "Show me your tables, and I won't usually need your flowcharts; they'll be obvious."
> *   **Rob Pike (1989):** "Data dominates. If you've chosen the right data structures... the algorithms will almost always be self-evident."
> *   **Linus Torvalds (2006):** "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."

## The Manifesto

To prevent [[SoT - Context Rot]] and [[SoT - Parochial Code]], we adhere to these strict principles:

### 1. Separate Data from Behavior
*   **The Rule:** Use **Anemic Domain Models**.
*   **Data:** Structs/Records hold *only* state. They are dumb containers.
*   **Behavior:** Logic resides in separate, pure functions that transform data.
*   **Why:** Eliminates the hidden state mutations and side effects of methods.

### 2. Composition Over Inheritance
*   **The Rule:** Rigid class hierarchies are forbidden.
*   **Mechanism:** Build complex types by composing simple structs (Product Types) or choosing between variants (Sum Types).
*   **Why:** Inheritance hides the flow of data; Composition makes it explicit.

### 3. Data Flow Visualization
*   **The Rule:** Treat the program as a pipeline, not a web of objects.
*   **Model:** `Input Data → Transformation Function → Output Data`
*   **Benefit:** The system state is always a snapshot of the pipeline, making debugging trivial.

### 4. Explicit Over Implicit
*   **The Rule:** No "Magic." Data flow must be traceable in the type signature.
*   **Example:** `fn assess(Blueprint) -> Assessment` explicitly states the dependency. Dependency Injection containers are often anti-patterns here.

---

## Relationship to Type-Driven Development

DOD provides the **Philosophy** (Structure is Truth), while **[[SoT - Type-Driven Development (The Torvalds Loop)]]** provides the **Methodology** (How to enforce that structure using the Type System).

*   **DOD:** "Data should be separate from behavior."
*   **Type-Driven:** "Here is how we use `struct` vs `impl` blocks to enforce that separation."

---
**See Also:** [[SoT - Parochial Code]], [[SoT - Context Rot]], [[SoT - Dimensions of Code Understanding]]
