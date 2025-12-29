---
aliases: ["The Torvalds Loop", "Type-Driven Design", "Data-Centric Programming", "Type-First Development"]
confidence: "5/5"
created: 2025-12-29
epistemic: "authoritative"
last_reviewed: "2025-12-29"
modified: 2025-12-29
purpose: "To define the core programming philosophy of PRODOS: a synthesis of hardware-conscious data design and mathematical type theory."
review_interval: "6 months"
see_also: ["[[SoT - The Trinity of Isomorphism (Logic, Computation, Categories)]]", "[[SoT - Rust's Design Philosophy]]", "[[SoT - The Algebra of Types (Cardinality and Isomorphism)]]"]
source_of_truth: []
status: "stable"
tags: ["philosophy", "programming", "rust", "type_theory", "architecture"]
title: SoT - Type-Driven Development (The Torvalds Loop)
type: "SoT"
uid: 
updated: 
---

## 1. The Core Mandate

> [!quote] Linus Torvalds
> "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."

The fundamental principle of this system is to move from **"Stringly Typed"** logic (Bash/Go/JS) to **"Type-Driven"** architecture (Rust). We reject the entropy of defensive coding and instead **Make Invalid States Physically Unrepresentable**.

---

## 2. The Torvalds Loop: A Four-Phase Design Protocol

In this protocol, Logic is the *last* consideration. We prioritize the physical reality of data over the behavior of code.

| Phase | Focus | Architectural Goal |
| :--- | :--- | :--- |
| **1. Shape** | **Physical Reality** | Design memory layout (`struct`/`enum`) for cache efficiency and logical exclusion. |
| **2. Access** | **Mechanics** | Define how data moves (Value vs. Pointer semantics). Control ownership and allocation. |
| **3. Invariants** | **Integrity** | Define constraints that must *always* be true. Use the type system to enforce them. |
| **4. Logic** | **Transformation** | Write simple, linear algorithms that transform valid state A into valid state B. |

### The "Parse, Don't Validate" Principle
Do not write code to "validate" messy input. Instead, **parse** it into a Type where the invalid state cannot exist. If parsing succeeds, the logic that follows is guaranteed to be safe.

---

## 3. The Trinity: Mathematical Truth

Logic, Code, and Category Theory are isomorphic. This provides a rigorous foundation for data design.

### A. Sum Types (The "OR" Relationship)
- **Rust Construct:** `enum`.
- **Logic:** $A \lor B$.
- **Definition:** Defined by "Arrows In" (Constructors).
- **Rule:** Used for **Choice** and **State**.
- **The Equation:** Handling a Sum type ($A+B$) requires a **Product of functions** ($C^A \times C^B$). This is why `match` statements must be exhaustive.

### B. Product Types (The "AND" Relationship)
- **Rust Construct:** `struct`.
- **Logic:** $A \land B$.
- **Definition:** Defined by "Arrows Out" (Projections).
- **Rule:** Used for **Grouping** data that must coexist.

---

## 4. Anti-Patterns to Exorcise

- **Boolean Blindness:** Using `bool` flags (e.g., `isBitnami`) to switch behavior.
    - *Fix:* Use a Sum Type (`enum Vendor { Bitnami, Community }`).
- **Primitive Obsession:** Passing raw `String` or `Int` values for semantic concepts (e.g., `Version`).
    - *Fix:* Use **NewTypes** (`struct Version(String)`) with specific parsing rules.
- **Zombie States:** Memory layouts where flags and data are decoupled, allowing states like "IsBuilt = false, but BuildArtifact is present."
    - *Fix:* Move the artifact into the `Built` variant of a `State` enum.

---

## 5. Active Implementation Contexts

| Project | Architectural Lens | Key Type Transition |
| :--- | :--- | :--- |
| **[[Project - Toy Vault]]** | State Machine | `Barrier` as a Sum Type: `Sealed | Unsealed`. |
| **[[Project - Chart Manager]]** | Type Refinement | `ImageRef` as an atomic unit; `ImageVersion` as a Sum Type. |
| **[[Project - Release Script]]** | Process Reification | Linear Bash script $\to$ Rust Finite State Machine (FSM). |

---

## 6. Minimum Viable Understanding (MVU)

1. **Data First:** If the `struct` allows an invalid state, the architecture is broken.
2. **Exhaustiveness:** Use Enums for state; use the compiler to ensure every state is handled.
3. **Mechanical Sympathy:** Respect how the CPU sees your data (contiguity vs. indirection).
