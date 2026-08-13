---
alias: [PLT MOC, Programming Language Theory Index, Type Theory Index]
aliases: []
created: 2025-12-29T21:52:02+00:00
modified: 2026-08-13T10:53:37+00:00
permalink: llmeon/30-library/mo-c/moc-type-theory
tags: [logic, programming, SoftwareEngineering/Architecture, type_theory, type/moc]
title: MOC - Type Theory
---

## 1. The Thesis (Applied Type Theory)

Software architecture is an exercise in Applied Type Theory. By understanding the mathematical properties of data (Cardinality, Isomorphism), we can engineer systems that are not only performant (Data-Oriented) but logically virtually bug-free (Type-Driven).

> "Make Illegal States Unrepresentable."

---

## 2. Foundational Isomorphisms (The Math)

The rigorous mathematical rules that govern how data behaves and the "Meta-Framework" linking logic, math, and code.

- [[SoT - The Curry-Howard Correspondence (Propositions as Types)]]: The bedrock isomorphism between logical propositions and computer types. "A program is a proof."
- [[SoT - Conservation of Complexity]]: The law stating complexity moves between Control Flow (Code) and Representation (Types).
- [[SoT - Software Complexity is Conserved Between Control Flow and Representation]]: The deep dive into the trade-off.
- [[SoT - Stringly Typed vs Strongly Typed]]: The practical implication of weak vs strong isomorphism.

---

## 3. Computational Semantics (The Harper School)

The perspective that computation is primary, and logic is derived from it.

- [[SoT - Equality in Type Theory (Intensional vs Extensional)]]: The architectural tension between semantic truth (Reflection) and mechanical checkability (Decidability).
- [[SoT - The Monad Design Pattern (Pipeline Abstraction)]]: Computational contexts modeled as types.
- [[SoT - Effects as Data (Tag Unions)]]: Handling side effects through data reification.

---

## 4. Advanced & Homotopy Type Theory (HoTT)

Bridging the gap between structure and computation spaces.

- [[SoT - Cubical Type Theory (Computational Univalence)]]: A geometric approach to making the Univalence Axiom computable via dimension variables.

---

## 5. Practical Engineering (The Bridge)

Applying type theory to eliminate runtime failure in real-world systems.

- [[SoT - Type-Driven Development (The Torvalds Loop)]]: The PRODOS core design protocol: Shape $\to$ Access $\to$ Invariants $\to$ Logic.
- [[SoT - Parse, Don't Validate]]: Pushing checks to the boundaries of the system.
- [[SoT - The Data-Centric Philosophy]]: The physical reality. Why data layout (DOD) matters more than code (OOP).
- [[SoT - The Infrastructure Witness Pattern]]: Using proof-carrying code to enforce infrastructure dependencies (IP $\to$ DNS $\to$ Cert).
- [[SoT - Type-Driven Infrastructure Strategy]]: Applying these concepts to Cloud/IaC.
- [[SoT - Type-Driven Shell Architecture]]: Applying strong typing to CLI design.

---

## 6. Language Implementation

How specific languages reify these concepts.

### Rust (Systems & Affine Types)

- [[SoT - Rust's Ownership Model]]: Implementing Linear Logic (Affine Types) for memory safety.
- [[SoT - Rust Type Mechanics]]: The mechanical components: Generics, Traits, and Layout.
- [[SoT - Rust Type Theory & Critique]]: Formal modeling (Formality Core) and analysis of Rust's theoretical debt.

### TypeScript (Expressivity)

- [[SoT - TypeScript as a Proof Engine (Set Theory and Distributivity)]]: TypeScript types as Sets and the compiler as a constraint solver.

### Lisp/Racket (Metaprogramming)

- [[SoT - Interleaved Compilation (The Hackett Architecture)]]: Fusing Lisp macros with Haskell types.

---

## 7. AI & Complexity Theory

- [[SoT - LLM Reasoning Obeys the Complexity Conservation Law]]: Why typed systems generate better AI code.

---

## 8. Philosophical Context

- [[Logicism (Mathematics as Extension of Logic)]]: The quest to reduce math to pure logic.
- [[Intuitionism Rejects the Law of the Excluded Middle]]: The constructive logic foundation of type theory.
