---
alias: ["PLT MOC", "Programming Language Theory Index", "Type Theory Index"]
aliases: []
confidence: "5/5"
created: 2025-12-29T21:52:02+00:00
epistemic: "The central entry point for Type Theory, linking mathematical foundations with software engineering practices."
last_reviewed: "2025-12-31"
modified: 2026-01-08T10:49:46+00:00
purpose: "To bridge the gap between rigorous Mathematical Logic (Isomorphism, Homotopy) and Pragmatic Software Engineering (Rust, Data-Centric)."
review_interval: "6 months"
see_also: ["[[MOC - Data-Centric Infrastructure]]", "[[MOC - Data-Centric Software Engineering]]", "[[MOC - Rust Programming Language]]"]
source_of_truth: []
status: "stable"
tags: ["logic", "programming", "SoftwareEngineering/Architecture", "type_theory", "type/moc"]
title: MOC - Type Theory
type: "map"
uid: 
updated: 
---

## 1. The Thesis (Applied Type Theory)

Software architecture is an exercise in **Applied Type Theory**. By understanding the mathematical properties of data (Cardinality, Isomorphism), we can engineer systems that are not only performant (Data-Oriented) but logically virtually bug-free (Type-Driven).

> "Make Illegal States Unrepresentable."

---

## 2. Foundational Isomorphisms (The Math)

The rigorous mathematical rules that govern how data behaves and the "Meta-Framework" linking logic, math, and code.

- **[[SoT - Type Theory & Data Structures]]** - The Master Note. Connects Logic, Math, and Memory.
- **[[SoT - The Algebra of Types (Cardinality and Isomorphism)]]** - The core building blocks: Sum Types (OR), Product Types (AND), and Exponentials.
- **[[SoT - The Trinity of Isomorphism (Logic, Computation, Categories)]]** - The full Curry-Howard-Lambek correspondence, defining Products and Sums via Category Theory arrows and duality.
- **[[SoT - The Curry-Howard Correspondence (Propositions as Types)]]**: The bedrock isomorphism between logical propositions and computer types. "A program is a proof."

---

## 3. Computational Semantics (The Harper School)

The perspective that **computation is primary**, and logic is derived from it.

- **[[SoT - Computational Type Theory (Meaning as Use)]]**: Types defined by introduction/elimination rules and program behavior.
- **[[SoT - Equality in Type Theory (Intensional vs Extensional)]]**: The architectural tension between semantic truth (Reflection) and mechanical checkability (Decidability).

---

## 4. Advanced & Homotopy Type Theory (HoTT)

Bridging the gap between structure and computation spaces.

- **[[SoT - The Structure of Identity (UIP and Groupoids)]]**: The pivotal discovery that equality proofs are not unique (UIP is false), paving the way for types as spaces.
- **[[SoT - Cubical Type Theory (Computational Univalence)]]**: A geometric approach to making the Univalence Axiom computable via dimension variables.
- **[[SoT - Quantitative Type Theory]]**: Tracking resource usage (Linearity) within the type system.

---

## 5. Practical Engineering (The Bridge)

Applying type theory to eliminate runtime failure in real-world systems.

- **[[SoT - Type-Driven Development (The Torvalds Loop)]]**: The PRODOS core design protocol: Shape $\to$ Access $\to$ Invariants $\to$ Logic.
- **[[SoT - Parse, Don't Validate]]**: Pushing checks to the boundaries of the system.
- **[[SoT - Data-Centric Software Engineering]]**: The physical reality. Why data layout (DOD) matters more than code (OOP).
- **[[SoT - Type Theory of PKI and Cryptography]]**: Cryptographic proofs modeled as type constraints and transformations.
- **[[SoT - The Infrastructure Witness Pattern]]**: Using proof-carrying code to enforce infrastructure dependencies (IP $\to$ DNS $\to$ Cert).

---

## 6. Language Implementation

How specific languages reify these concepts.

### Rust (Systems & Affine Types)

- **[[SoT - Rust Language]]**: Why Rust forces you to think about types.
- **[[SoT - Rust's Ownership Model]]**: Implementing Linear Logic (Affine Types) for memory safety.
- **[[SoT - Rust Type Mechanics]]**: The mechanical components: Generics, Traits, and Layout.
- **[[SoT - Rust Type Theory & Critique]]**: Formal modeling (Formality Core) and analysis of Rust's theoretical debt.
- **[[SoT - Proof-Carrying Code via Simulated Dependent Types]]**: Encoding logic proofs into Rust's type system.

### Haskell & TypeScript (Expressivity)

- **[[SoT - Dependent Haskell and Singletons]]**: Architectural patterns (Promoted Constructors, Singletons) for dependent types.
- **[[SoT - TypeScript as a Proof Engine (Set Theory and Distributivity)]]**: TypeScript types as Sets and the compiler as a constraint solver.
- **[[SoT - Interleaved Compilation (The Hackett Architecture)]]**: Fusing Lisp macros with Haskell types.

---

## 7. Philosophical Context

- **[[Logicism (Mathematics as Extension of Logic)]]**: The quest to reduce math to pure logic.
- **[[Intuitionism Rejects the Law of the Excluded Middle]]**: The constructive logic foundation of type theory.
- **[[Russell's Paradox in Naive Set Theory]]**: The paradox that necessitated type stratification.
