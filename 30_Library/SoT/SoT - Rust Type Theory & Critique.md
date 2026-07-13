---
alias: [Formality Core, Rust Formal Modeling, Rust Type Theory, The Price of Ignoring Theory]
aliases: []
created: 2025-12-29T11:13:41+00:00
modified: 2026-07-13T08:52:53+00:00
permalink: llmeon/30-library/so-t/so-t-rust-type-theory-critique
tags: [critique, formal-methods, rust, type-theory]
title: SoT - Rust Type Theory & Critique
---

## 1. The Theoretical Debt

A critical perspective from formal type theory argues that Rust was developed "orthogonally to theory," leading to an "unbound and incomplete" type system.

### Core Critique: Borrowing vs. Linearity

- The Flaw: Rust's Borrow Checker is an engineered solution, distinct from the mathematical concept of Linear Logic.
- Linearity: In Type Theory, Linear Logic ensures a resource is used _exactly once_.
- The Gap: Borrowing and Linearity form an adjunction. Rust focuses on borrowing but misses the full power of Linearity (and Graded Modal Types), which would allow for more precise resource tracking without "fighting the borrower."

## 2. Missing Features: Dependent Types

Rust lacks Dependent Types (types that depend on values), preventing "Correctness by Construction" for arrays and bounds.

- Example: You cannot easily define a type `Vector<T, 3>` where the length is enforced by the type system at a level that allows math on the length (e.g., `append(Vec<T, n>, Vec<T, m>) -> Vec<T, n+m>`).
- Result: Rust relies on runtime panics for out-of-bounds errors, whereas languages like Idris or Agda solve this at compile time.

## 3. Formal Modeling: Formality Core

Because Rust's type system is complex and evolved organically, it lacks a formal specification. Formality Core is an effort to fix this.

> [!definition] Formality Core
> A lightweight, executable framework built in Rust for modeling type systems. It acts as a "Sandbox" to test new language rules (RFCs) for soundness before implementing them in the compiler.

- Mechanism: It uses Rust macros to represent formal judgment rules (e.g., $\Gamma \vdash e: \tau$).
- Goal: To verify that new features (like Polonius or GATs) do not introduce unsoundness.

## 4. The ABI Critique

- The Mistake: Rust creates a new ABI rather than stabilizing a standard one (or fixing the C ABI).
- Consequence: This forces a culture of Static Linking, leading to massive binary sizes ("trashing the instruction cache") because common libraries (like `std`) are duplicated in every executable.

## 5. Minimum Viable Understanding (MVU)

1. Rust is Pragmatic, Not Pure: It prioritizes "running on silicon" over "mathematical beauty."
2. Theoretical Gaps Exist: The difficulty of "fighting the borrow checker" often stems from the lack of more advanced theoretical concepts (Linearity) that would make the rules more expressive.
3. Modeling is Ongoing: Tools like Formality Core are attempting to retrofit a formal mathematical model onto Rust's existing behavior.
