---
aliases: []
alias: ["ADTs", "Sum and Product Types", "Algebraic Types"]
confidence: "5/5"
created: 2025-12-29T11:10:13+00:00
epistemic: "authoritative"
last_reviewed: "2025-12-29"
modified: 2025-12-29T16:25:02+00:00
purpose: "To define the framework, logic, and cross-language implementation of Algebraic Data Types (ADTs)."
review_interval: "6 months"
see_also: ["[[SoT - The Algebra of Types (Cardinality and Isomorphism)]]", "[[SoT - The Trinity of Isomorphism (Logic, Computation, Categories)]]", "[[SoT - Type-Driven Development (The Torvalds Loop)]]"]
source_of_truth: []
status: "stable"
tags: ["type_theory", "programming", "architecture", "fp"]
title: SoT - Algebraic Data Types (ADTs)
type: "SoT"
uid: 
updated: 
---

## 1. Core Definition

> [!definition] Algebraic Data Type (ADT)
> An ADT is a composite type formed by combining other types using two primary operations: **Sum** (OR) and **Product** (AND). They are "algebraic" because they follow the formal rules of set theory and arithmetic cardinality.

---

## 2. Fundamental Building Blocks

### A. Product Types (Logical AND)

- **Concept:** Requires Value A **AND** Value B to coexist.
- **Cardinality:** Multiplication ($|A \times B| = |A| \cdot |B|$).
- **Implementations:** `struct` (Rust/C), `case class` (Scala), `record` (Java/C#), Tuples.
- **Example:** A `Point` requires both `x` and `y`.

### B. Sum Types (Logical OR)

- **Concept:** Represents a choice between mutually exclusive variants (Choice).
- **Cardinality:** Addition ($|A + B| = |A| + |B|$).
- **Implementations:** `enum` (Rust/Swift), `sealed trait` (Scala), Discriminated Union (TS), `sealed interface` (Java).
- **Example:** `Weather` is either `Sunny` OR `Rainy` OR `Cloudy`.

---

## 3. Underlying Design Logic

The power of ADTs lies in their ability to enforce domain invariants at the type level.

- **Making Illegal States Unrepresentable:** Restricting the state space ensures that invalid data combinations cannot be instantiated.
- **Compositionality:** ADTs can be nested (Sum of Products) to build complex models like Trees or JSON ASTs.
- **Decoupling:** ADTs act as pure data containers, separating state from behavior (Logic).
- **Exhaustiveness:** Compilers use ADT definitions to ensure every possible case is handled in pattern matching, eliminating runtime edge-case bugs.

---

## 4. Cross-Language Implementation Patterns

| Language | Sum Type Mechanism | Product Type Mechanism |
|:--- |:--- |:--- |
| **Rust** | `enum` (with data payloads) | `struct` / `tuple` |
| **Scala** | `sealed trait` / `sealed abstract class` | `case class` |
| **TypeScript** | Discriminated Unions (`kind` property) | `interface` / `type` |
| **C#** | `sealed partial abstract class` + Nested Classes | `record` / `struct` |
| **Java** | `sealed interface` + `permits` | `record` |

### C# / Java Simulation (Legacy)

In languages lacking native Sum types, they are simulated using **Closed Hierarchies**:

1. **Sealed Base Class:** Prevents external inheritance.
2. **Private Constructor:** Ensures only nested variants can exist.
3. **Functional Dispatch:** A `Match` method using lambdas replaces standard polymorphism to enforce exhaustiveness.

---

## 5. Mathematical Equivalences (The "Rig" Framework)

The type system functions as a **Semi-ring (Rig)**—a ring without negative elements.

- **Zero (Void/!):** Additive Identity ($A + 0 = A$). A type with no values.
- **One (Unit/()):** Multiplicative Identity ($A \times 1 = A$). A type with exactly one value.
- **Annihilation:** $A \times 0 = 0$. A product containing a `Void` type is itself unconstructible.
- **Distributivity:** $A \times (B + C) \cong (A \times B) + (A \times C)$. This allows refactoring between "Factored" and "Expanded" models.

---

## 6. Advanced Structures: Recursive ADTs

ADTs can be recursive, allowing for unbounded but logically sound data structures.

- **Example: Tree**
    - `Tree = Leaf | Node(Value, LeftTree, RightTree)`
    - This is a Sum of (Unit OR Product).
- **Example: List**
    - `List = Nil | Cons(Head, Tail)`

---

## 7. Operational Logic

- **Map:** Transform the value inside a container (Product or successful Sum) without unwrapping.
- **Fold (Catamorphism):** Deconstruct an ADT by providing handlers for every variant, reducing it to a single value.
