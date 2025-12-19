---
alias: ["Algebraic Data Types", "Isomorphisms", "The Algebra of Types", "Type Cardinality"]
aliases: []
confidence: 5/5
confidence-gaps: []
created: 2025-12-18T11:15:00Z
decay-signals: []
epistemic: authoritative
last_reviewed: 2025-12-18
modified: 2025-12-18T21:31:56Z
purpose: Defines the algebraic structure of data types (Sums, Products, Exponentials) and their isomorphisms.
quality-markers: ["Synthesized from All Angles: Type theory and the algebra of types"]
related-soTs: ["[[SoT - The Curry-Howard Correspondence (Propositions as Types)]]"]
resonance-score: 6
review_interval: 1 year
see_also: []
source_of_truth: true
status: stable
tags: ["algebra", "architecture", "functional_programming", "type_theory"]
title: SoT - The Algebra of Types (Cardinality and Isomorphism)
type: SoT
uid:
updated:
---

## 1. Working Knowledge (Stable Foundation)

- **Core Concept:** Types can be understood algebraically by the size (cardinality) of their set of possible values.
- **The Arithmetic:**
  - **Sum Types ($A + B$):** `Enum` / `Union`. Cardinality = $|A| + |B|$.
  - **Product Types ($A \times B$):** `Struct` / `Tuple`. Cardinality = $|A| \times |B|$.
  - **Function Types ($A \to B$):** `Map` / `Exponent`. Cardinality = $|B|^{|A|}$.
- **Neutral Elements:**
  - **Void ($0$):** Identity for Sums ($A + 0 = A$).
  - **Unit ($1$):** Identity for Products ($A \times 1 = A$).

## 2. Current Understanding (Coherent Narrative)

### The Core Definition

A type is a set of allowed values equipped with operations. By counting these values, we can predict the state space complexity of a system.

- *Architectural Implication:* Minimizing state space (cardinality) reduces bug surface area.

### Algebraic Operations

1. **Addition (OR Logic):** A **Sum Type** (`Result<T, E>`) holds *either* T *or* E. We add the possibilities.
2. **Multiplication (AND Logic):** A **Product Type** (`struct User { name, age }`) holds T *and* E. We multiply the possibilities.
3. **Exponentiation (Mapping):** A function from A to B is written as $B^A$. For each of the $|A|$ inputs, you can choose one of the $|B|$ outputs.

### Isomorphisms (Refactoring via Algebra)

Because types follow standard algebraic laws, we can prove that two different code structures are mathematically identical (Isomorphic).

- **Distributivity:** $a \times (b + c) = (a \times b) + (a \times c)$.
  - *Code:* `(A, Either<B, C>)` is isomorphic to `Either<(A, B), (A, C)>`.
- **Currying (Exponent Laws):** $(a^b)^c = a^{b \times c}$.
  - *Code:* A function returning a function `A -> (B -> C)` is isomorphic to a function taking a tuple `(A, B) -> C`.
- **Function to Unit:** $1^A = 1$.
  - *Code:* A function that returns `Unit` (void) has only one possible implementation (do nothing/return unit), regardless of the input.

## 3. Understanding Layers (Progressive Abstraction)

- **Layer 1 (Counting):** If `Bool` has 2 states and `u8` has 256, then `(Bool, u8)` has 512 states.
- **Layer 2 (Structure):** `Option<T>` is just `T + 1` (The set of T plus one "None" case).
- **Layer 3 (Proofs):** We can use high-school algebra to prove that two data structures contain the same information and can be losslessly converted.

## 4. Minimum Viable Understanding (MVU)

- **Sum (+):** `OR` (Enums).
- **Product (*):** `AND` (Structs).
- **Exponent (^):** `Map` (Functions).
- **Isomorphism:** If the algebra equations match, the code structures are equivalent.

## 5. Tensions, Gaps, and Cross-SoT Coherence

- **Connection to Logic:** This algebra perfectly mirrors the logic in [[SoT - The Curry-Howard Correspondence (Propositions as Types)]].
  - $A \times B$ (Product) is $A \land B$ (Conjunction).
  - $A + B$ (Sum) is $A \lor B$ (Disjunction).
  - $B^A$ (Exponent) is $A \implies B$ (Implication).

## 6. Sources and Links

- **Source:** All Angles, *Type theory and the algebra of types* (YouTube).
