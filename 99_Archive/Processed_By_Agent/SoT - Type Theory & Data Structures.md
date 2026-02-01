---
alias: ["ADTs", "Mathematical Foundation of Types", "Sum and Product Types", "The Algebra of Types"]
aliases: []
confidence: "5/5"
created: 2025-12-29T21:52:00+00:00
epistemic: "foundational"
last_reviewed: "2025-12-30"
modified: 2026-01-08T10:49:40+00:00
purpose: "To provide the mathematical justification for Type-Driven Development and Data-Oriented Design, linking Abstract Algebra to Physical Memory."
review_interval: "1 year"
see_also: ["[[SoT - The Curry-Howard Correspondence (Propositions as Types)]]", "[[SoT - Type-Driven Infrastructure Strategy]]"]
source_of_truth: []
status: "stable"
tags: ["computer_science", "math", "programming", "rust", "type_theory"]
title: SoT - Type Theory & Data Structures
type: "SoT"
uid: 
updated: 
---

## SoT - Type Theory & Data Structures

### 1. Definitive Statement

> [!definition] Type Theory
> The formal logic of Computational Sets. It provides the algebraic framework to quantify system complexity (Cardinality) and prove the correctness of transformations (Isomorphism). It bridges the gap between Abstract Logic (correctness) and Physical Reality (memory layout).

---

### 2. Fundamental Building Blocks: Algebraic Data Types (ADTs)

ADTs are "algebraic" because they follow the formal rules of set theory and arithmetic.

#### I. Product Types (Logical AND)

- Concept: Requires Value A AND Value B to coexist.
- Cardinality: Multiplication ($|A \times B| = |A| \cdot |B|$).
- Impl: `struct` (Rust), `interface` (TS), `case class` (Scala).
- Impact: Complexity explodes multiplicatively.

#### II. Sum Types (Logical OR)

- Concept: Mutually exclusive choice between variants.
- Cardinality: Addition ($|A + B| = |A| + |B|$).
- Impl: `enum` (Rust), Discriminated Union (TS), `sealed trait` (Scala).
- Impact: Complexity grows additively. Preferred for reducing state space.

---

### 3. The Algebra of Composition (Counting State)

To "Make Illegal States Unrepresentable," we calculate the Cardinality of the type.

| Operation | Logic | Cardinality Formula | Example |
|:--- |:--- |:--- |:--- |
| Zero | False | 0 | `Void` / `!` (Uninhabitable) |
| One | True | 1 | `Unit` / `()` (Exactly one value) |
| Sum | OR | $A + B$ | `Option<bool>` ($1 + 2 = 3$) |
| Product | AND | $A \times B$ | `(bool, bool)` ($2 \times 2 = 4$) |
| Exponential | Function | $B^A$ | `fn(bool) -> bool` ($2^2 = 4$) |

---

### 4. The Grand Unification: Curry-Howard Isomorphism

The structural identity between Mathematical Logic and Computational Types.

| Logic (Propositions) | Computation (Types) |
|:--- |:--- |
| Proposition ($P$) | Type ($T$) |
| Proof ($P \implies Q$) | Program (`fn(T) -> U`) |
| And ($A \land B$) | Product (`struct`) |
| Or ($A \lor B$) | Sum (`enum`) |

Core Rule: Writing a function is writing a proof. If the code compiles, the proof is valid.

---

### 5. Isomorphism & Refactoring

Two types are Isomorphic ($A \cong B$) if data-lossless conversion exists in both directions.

#### Distributivity Principle

$A \times (B + C) \cong (A \times B) + (A \times C)$

- Refactoring Use Case: You can move from a "God Struct" with an internal enum to a "Top-level Enum" containing specific structs to optimize memory and logic clarity.

---

### 6. Implementation Patterns (Math to Metal)

| Language | Sum Type Mechanism | Product Type Mechanism |
|:--- |:--- |:--- |
| Rust | `enum` (with data) | `struct` |
| TypeScript | Discriminated Unions | `interface` / `type` |
| Scala | `sealed trait` | `case class` |

#### The "Linear" Constraint (Linear Logic)

In logic, facts are eternal. In systems, resources are finite.

- Rust Ownership: Exposes Linear Logic as a type system feature. Passing a value `T` consumes the "proof," preventing its reuse.

---

### 7. Minimum Viable Understanding (MVU)

1. Reduce Entropy: Prefer Sums (`enum`) over Products (`struct`) to keep the state space small.
2. Types are Logic: Business rules are type definitions; business logic is the proof (implementation).
3. Physical Layout: These rules dictate how bytes sit in RAM (e.g., Sum types use a "Tag" byte followed by the largest variant's memory footprint).
