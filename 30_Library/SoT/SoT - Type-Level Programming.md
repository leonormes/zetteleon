---
aliases: []
alias: ["TLP", "Type-Level Logic", "Compile-Time Computation"]
confidence: "5/5"
created: 2025-12-29T16:09:40+00:00
epistemic: "authoritative"
last_reviewed: "2025-12-29"
modified: 2025-12-29T16:24:53+00:00
purpose: "To define Type-Level Programming (TLP) as a paradigm for performing computations at compile-time using the type system."
review_interval: "6 months"
see_also: ["[[SoT - The Curry-Howard Correspondence (Propositions as Types)]]", "[[SoT - Proof-Carrying Code via Simulated Dependent Types]]"]
source_of_truth: []
status: "stable"
tags: ["programming", "type_theory", "scala", "rust", "compilers"]
title: SoT - Type-Level Programming
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Type-Level Programming (TLP)
> TLP is a paradigm where **computations are executed at compile-time** by encoding values as types and logic as type relationships. In this model, the compiler acts as a logic engine or theorem prover, ensuring that only valid "proofs" (programs) are generated.

---

## 2. Foundations: Values as Types

The core insight of TLP is the ability to lift runtime values into the type system.

### A. Natural Numbers (Peano Encoding)

Numbers are represented as nested type constructors.

- `Zero`: Represents 0.
- `Succ[N]`: Represents the successor of N ($N+1$).
- *Example:* `Succ[Succ[Zero]]` is the type-level representation of $2$.

### B. Booleans as Types

Logical states are represented as distinct types to enable type-level branching.

- `sealed trait Bool`
- `class True extends Bool`
- `class False extends Bool`

---

## 3. Mechanisms of Computation

Different languages provide different "calculi" for type-level computation.

### I. Match Types (Scala 3)

Match types allow direct pattern matching on types, providing a readable way to express type reduction without complex implicit chains.

- **Recursive Logic:** Addition can be defined as a recursive match type where `Plus[Succ[A], B]` reduces to `Succ[Plus[A, B]]`.

### II. Given/Using & Summoning (Scala 3)

This mechanism embodies the **Curry-Howard Correspondence**.

- **Types as Propositions:** `CanShow[Int]` is a proposition that "Int can be converted to a string."
- **Values as Proofs:** A `given` instance provides the evidence for that proposition.
- **Summoning as Proof Search:** The compiler searches the environment for evidence using `summon` (Scala 3) or `implicitly` (Scala 2).

### III. Trait Solver (Rust)

In Rust, TLP is implemented through the trait system.

- **Constraints as Logic:** Trait bounds (e.g., `where N: Add<M>`) serve as logical premises.
- **Associated Types:** These act as the "output" of a type-level function.

---

## 4. Architectural Goal: Correctness by Construction

TLP is the primary implementation vehicle for **[[SoT - Proof-Carrying Code via Simulated Dependent Types]]**.

- **Length-Indexed Lists:** A `List[N, T]` type where `N` is a Peano number. The compiler can prove that `head` is safe to call only on lists where $N > 0$.
- **Matrix Safety:** Proving that matrix $A_{m \times n}$ and $B_{n \times p}$ can be multiplied (where $n=n$) at compile-time.
- **Protocol Enforcment:** Ensuring a database connection is `Authenticated` before allowing `Query` operations.

---

## 5. Minimum Viable Understanding (MVU)

1. **Types are Values:** We represent data (0, 1, true, false) as types.
2. **Logic is Relationship:** We use match types or trait bounds to define how these types interact.
3. **Compiler is the Engine:** The "runtime" for TLP is the compilation phase. If it builds, the logic is proven sound.
