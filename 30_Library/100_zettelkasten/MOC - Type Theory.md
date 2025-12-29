---
aliases: ["PLT MOC", "Programming Language Theory Index", "Type Theory MOC"]
confidence: "5/5"
created: 2025-12-18T11:20:00Z
epistemic: "null"
last_reviewed: "2025-12-18T00:00:00.000Z"
modified: 2025-12-28T18:49:32+00:00
purpose: ""
review_interval: "null"
see_also: []
source_of_truth: []
status: "stable"
tags: ["computer_science", "logic", "software_engineering", "type_theory"]
title: MOC - Type Theory
type: "moc"
uid: 
updated: 
---

## MOC - Type Theory

> [!definition] Definition
> **Type Theory** is a branch of mathematical logic and computer science that provides a formal framework for classifying "terms" (values and expressions) into "types." It serves as the foundation for modern programming languages and formal verification systems.

### 1. Foundational Isomorphisms

The "Meta-Framework" linking logic, math, and code.

- **[[SoT - Algebraic Data Types (ADTs)]]**: The core building blocks (Sums and Products) used to model domain state space and eliminate invalid states.
- **[[SoT - The Trinity of Isomorphism (Logic, Computation, Categories)]]**: The full Curry-Howard-Lambek correspondence, defining Products and Sums via Category Theory arrows and duality.
- **[[SoT - The Curry-Howard Correspondence (Propositions as Types)]]**: The bedrock isomorphism between logical propositions and computer types. "A program is a proof."
- **[[SoT - The Algebra of Types (Cardinality and Isomorphism)]]**: Understanding types through set cardinality and algebraic laws (Sums, Products, Exponentials).

### 2. Computational Semantics (The Harper School)

The perspective that **computation is primary**, and logic is derived from it.

- **[[SoT - Computational Type Theory (Meaning as Use)]]**: Types defined by introduction/elimination rules and program behavior.
- **[[SoT - Equality in Type Theory (Intensional vs Extensional)]]**: The architectural tension between semantic truth (Reflection) and mechanical checkability (Decidability).

### 3. Advanced & Homotopy Type Theory

Bridging the gap between structure and computation.

- **[[SoT - The Structure of Identity (UIP and Groupoids)]]**: The pivotal discovery that equality proofs are not unique (UIP is false), paving the way for types as spaces.
- **[[SoT - Cubical Type Theory (Computational Univalence)]]**: A geometric approach to making the Univalence Axiom computable via dimension variables.

## 4. Practical Implementation & Verification

Applying type theory to eliminate runtime failure.

- **[[SoT - Type-Driven Development (The Torvalds Loop)]]**: The PRODOS core philosophy; bridging the gap between hardware reality and mathematical truth.
- **[[SoT - Rust Type System Modeling (Formality Core)]]**: Making type systems executable and verifiable for busy engineers.
- **[[SoT - Rust Type System Tensions and Critiques]]**: Theoretical analysis of Rust's debt regarding Linearity, Dependent Types, and the ABI.
- **[[SoT - Proof-Carrying Code via Simulated Dependent Types]]**: Techniques for encoding logic proofs into Rust's type system to render bugs unrepresentable.
- **[[SoT - Dependent Haskell and Singletons]]**: The architectural patterns (Promoted Constructors, Singletons) for implementing dependent types in Haskell.
- **[[SoT - Interleaved Compilation (The Hackett Architecture)]]**: Fusing Lisp macros with Haskell types by running expansion and type-checking simultaneously.
- **[[SoT - TypeScript as a Proof Engine (Set Theory and Distributivity)]]**: The mental model of TypeScript types as Sets and the compiler as a constraint solver, addressing the Distributivity Trap.

### 5. Philosophical & Mathematical Context

- **[[Logicism (Mathematics as Extension of Logic)]]**: The quest to reduce math to pure logic.
- **[[Intuitionism Rejects the Law of the Excluded Middle]]**: The constructive logic foundation of type theory.
- **[[Russell's Paradox in Naive Set Theory]]**: The paradox that necessitated type stratification.

### 6. Related Domains

- [[MOC - Software Architecture Principles]]
- [[MOC - Computer Science Foundations]]
- [[SoT - PRODOS (System Architecture)]]
