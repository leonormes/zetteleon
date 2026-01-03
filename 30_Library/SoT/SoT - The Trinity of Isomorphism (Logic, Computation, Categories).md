---
aliases: []
alias: ["Curry-Howard Correspondence", "Category Theory in Rust", "Isomorphic Architecture", "The Trinity"]
confidence: "5/5"
created: 2025-12-18T21:30:15+00:00
epistemic: "theory"
last_reviewed: "2025-12-30"
modified: 2026-01-03T10:18:49+00:00
purpose: "To explore the deep isomorphism between Logic, Computation (Types), and Category Theory, and applying it to Software Architecture."
review_interval: "12 months"
see_also: ["[[SoT - The Algebra of Types (Cardinality and Isomorphism)]]", "[[SoT - Rust's Design Philosophy]]", "[[SoT - Type-Driven Infrastructure as Code]]"]
source_of_truth: []
status: "stable"
tags: ["type_theory", "category_theory", "architecture", "logic"]
title: SoT - The Trinity of Isomorphism (Logic, Computation, Categories)
type: "SoT"
uid: 
updated: 
---

## 1. The Trinity

Isomorphism is not just about data shapes; it connects three fundamental fields of thought.

1. **Logic:** Propositions and Proofs.
2. **Computation:** Types and Programs.
3. **Categories:** Objects and Morphisms.

This connection allows us to use Logic to prove our Programs are correct.

---

## 2. The Curry-Howard Correspondence (Logic $\cong$ Computation)

The "Propositions as Types" principle states that **Types are Logical Propositions** and **Programs are Proofs**.

| Logical Concept | Notation | Rust Construct | Interpretation |
|:--- |:--- |:--- |:--- |
| **Implication** | $A \implies B$ | `Fn(A) -> B` | If you give me an A, I can produce a B. |
| **Conjunction** | $A \land B$ | `(A, B)` | I have proof of A AND proof of B. |
| **Disjunction** | $A \lor B$ | `enum { A(A), B(B) }` | I have proof of A OR proof of B. |
| **True** | $\top$ | `()` (Unit) | Always provable (trivial). |
| **False** | $\bot$ | `!` (Never) | Impossible to construct (cannot exist). |
| **Universal** | $\forall T. P(T)$ | `fn foo<T>(x: T)` | True for any Type T (Generics). |

### 2.1 Practical Application: The Unconstructible State

If a state is "Logically False" (e.g., an authenticated user without an ID), we represent it with the `!` (Never) type or by making the type unconstructible.

> **Rule:** If the type checks, the logic is sound.

---

## 3. The Category $\mathcal{Rust}$ (Categories $\cong$ Computation)

We can model Rust programming as a Category:

- **Objects:** Rust Types (`String`, `User`).
- **Morphisms:** Pure Functions (`fn(A) -> B`).
- **Composition:** Connecting functions ($g \circ f$).

### 3.1 Hexagonal Architecture as Morphism Substitution

Hexagonal Architecture (Ports & Adapters) is a categorical concept.

- **Port (Trait):** Defines the "Category" of allowed morphisms.
- **Adapter (Struct):** A specific Object that satisfies the morphisms.

For a Mock Repository to be valid, it must be **Behaviorally Isomorphic** to the Postgres Repository with respect to the Trait laws.

---

## 4. Architectural Isomorphism

We extend isomorphism beyond a single process to the entire distributed system.

### 4.1 The Universal Application (Wasm)

In Rust, "Isomorphic" means sharing the exact same **Bytecode** via generic libraries.

- **Core:** Pure Logic (Platform Agnostic).
- **Server:** Imports Core.
- **Client (Wasm):** Imports Core.

$$Logic_{server} \cong Logic_{client}$$

This prevents "Logic Drift" (e.g., frontend validation differing from backend validation).

### 4.2 Type-Safe API Boundaries (Shared Types)

Instead of loose JSON schemas, we share **Type Definitions** across the network.

1. **Shared Crate:** Defines `struct CreateUserCmd`.
2. **Server:** Expects `CreateUserCmd`.
3. **Client:** Constructs `CreateUserCmd`.

The Compiler guarantees the isomorphism. If you change the struct, both Client and Server builds fail. This elevates "Contract Testing" to "Compile-Time Verification."

---

## 5. Conclusion

By understanding these isomorphisms, we stop viewing "Type Safety" as a nuisance and start viewing it as "Logical Proof."

- **Refactoring** is algebraic simplification.
- **Architecture** is defining category boundaries.
- **Coding** is constructing proofs.
