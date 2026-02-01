---
alias: ["Compile-Time Computation", "TLP", "Type-Level Logic", "Proof-Carrying Code", "Simulated Dependent Types", "Dependent Types"]
aliases: ["Proof-Carrying Code", "Simulated Dependent Types", "Dependent Types"]
confidence: "5/5"
created: 2025-12-29T16:09:40+00:00
epistemic: "authoritative"
last_reviewed: "2026-01-10"
modified: 2026-01-10T14:45:00+00:00
purpose: "The definitive Source of Truth for Type-Level Programming (TLP), defining the paradigm, foundations, and implementation strategies for compile-time logic."
review_interval: "6 months"
see_also: ["[[SoT - The Curry-Howard Correspondence (Propositions as Types)]]", "[[SoT - Quantitative Type Theory]]", "[[SoT - Type-Driven Development (The Torvalds Loop)]]"]
source_of_truth: []
status: "stable"
tags: ["compilers", "programming", "rust", "scala", "haskell", "type_theory", "formal_verification"]
title: SoT - Type-Level Programming
type: "SoT"
---

## 1. Definitive Statement

> [!definition] Type-Level Programming (TLP)
> TLP is a paradigm where computations are executed at compile-time by encoding values as types and logic as type relationships. In this model, the compiler acts as a logic engine or theorem prover, ensuring that only valid "proofs" (programs) are generated. The ultimate goal is Correctness by Construction.

## 2. The Core Problem: The Brittleness of Runtime Uncertainty

Standard type systems prevent type errors (e.g., treating an integer as a string) but cannot prevent logic errors (e.g., accessing index 5 of a size-3 vector). In conventional programming, these are checked via Runtime Assertions or Unit Tests.

| Failure Mode | The Conventional Approach | The TLP Solution |
| :--- | :--- | :--- |
| Logic Errors | `assert!(index < list.len())` (Runtime Panic). | Dependent Types: Types that depend on values (e.g., `Fin n` for index < `n`). |
| Illegal States | Defensive coding for nulls or inconsistent fields. | Unrepresentable States: Types that enforce invariants (e.g., `LoggedInUser` must have a token). |
| Bugs in Tests | Writing more code to test code. | Compiler as Prover: Verification is part of the build process, not a separate suite. |

TLP shifts failure modes from Runtime (Panic) to Compile-Time (Build Error).

## 3. Foundations: Values as Types

The core insight of TLP is the ability to lift runtime values into the type system, creating a hierarchy where Terms < Types < Kinds.

### 3.1 Natural Numbers (Peano Encoding)
Numbers are represented as nested type constructors.
- `Zero`: Represents 0.
- `Succ[N]`: Represents the successor of N ($N+1$). 
- _Example:_ `Succ[Succ[Zero]]` is the type-level representation of $2$.

### 3.2 Booleans as Types
Logical states represented as distinct types enable type-level branching.
- `sealed trait Bool`
- `class True extends Bool`, `class False extends Bool`

### 3.3 Generalized Algebraic Data Types (GADTs)
GADTs allow data constructors to specify their return type, enabling them to "carry" type-level proofs. They are the primary bridge between runtime data and type-level constraints.

## 4. Mechanisms of Computation

### I. Match Types (Scala 3)
Allows direct pattern matching on types to express type reduction.
- Recursive Logic: `Plus[Succ[A], B]` reduces to `Succ[Plus[A, B]]`.

### II. Implicit Proof Search (Scala/Haskell)
Embodying the Curry-Howard Correspondence.
- Types as Propositions: `CanShow[Int]` is a proposition.
- Values as Proofs: `given` or `instance` provides the evidence.
- Summoning: The compiler performs a Proof Search to find evidence.

### III. Trait Solver (Rust)
TLP implemented through the trait system.
- Trait Bounds: Logical premises.
- Associated Types: Outputs of type-level functions.
- Phantom Data: Zero-sized markers that carry type information without runtime cost.

## 5. Architectural Goal: Proof-Carrying Code

TLP makes invalid states unrepresentable.

- Length-Indexed Lists: A `Vect n a` where `head` can only be called if `n > 0`.
- Matrix Safety: Proving matrix dimensions match for multiplication at compile-time.
- Typestate Patterns: Enforcing state transitions (e.g., `Closed` connection cannot `Query`) via type-consuming methods.

## 6. Challenges: The Prophecy Problem

TLP often requires information at compile-time that is only available at runtime (e.g., user input).

- The Solution: Force a strict separation between Untrusted Boundaries (parsing/validation) and the Proven Core. Use parsing code to "witness" data and transform it into a dependently-typed structure. Once inside the core, the compiler guarantees correctness.

## 7. Language Implementation References

- Rust: [[SoT - Proof-Carrying Code via Simulated Dependent Types]] (Deprecated -> Merged here).
- Haskell: [[SoT - Dependent Haskell and Singletons]].
- TypeScript: [[SoT - TypeScript as a Proof Engine (Set Theory and Distributivity)]].

## 8. Minimum Viable Understanding (MVU)

1. Types are Values: We represent data (0, 1, true, false) as types.
2. Logic is Relationship: We use match types or trait bounds to define how types interact.
3. Compiler is the Engine: The "runtime" for TLP is the compilation phase. If it builds, the logic is proven sound.