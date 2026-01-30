---
aliases: [Data-Centric Software Engineering, DOD, Anemic Domain Model, Data-Oriented Manifesto]
tags: [software-architecture, design-principle, data-oriented, rust]
created: 2026-01-30T09:00:00+00:00
modified: 2026-01-30T09:00:00+00:00
---

# Data-Oriented Design

**Data-Oriented Design (DOD)** is the architectural axiom that **Data is Truth; Code is Derivative.** Unlike Object-Oriented Design (OOD), which couples data with behavior (Classes), DOD separates them completely to optimize for both hardware performance (CPU Cache) and cognitive clarity (Simplicity).

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
