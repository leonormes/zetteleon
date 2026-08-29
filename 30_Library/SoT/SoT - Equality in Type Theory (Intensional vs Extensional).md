---
aliases: [Equality Reflection, Extensional Type Theory, Identity Types, Intensional Type Theory]
conformant: false
created: 2025-12-18T00:00:00+00:00
modified: 2026-08-29T09:36:36+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-equality-in-type-theory-intensional-vs-extensional
tags: [equality, formal_methods, SoftwareEngineering/Architecture, type_theory]
title: SoT - Equality in Type Theory (Intensional vs Extensional)
type: sot
---

## 1. Working Knowledge (Stable Foundation)

- The Conflict: We want a system that is both Expressive (captures all mathematical truths) and Decidable (can be checked by a compiler). With Equality, you generally have to choose one.
- Extensional Equality (The Ideal): If $a$ and $b$ behave the same way, they are equal.
  - _Feature:_ Equality Reflection. If you prove $a=b$, the compiler treats them as interchangeable everywhere silently.
  - _Bug:_ Undecidable. Checking types might require solving open math problems.
- Intensional Equality (The Reality): Equality is a piece of data you must carry around.
  - _Feature:_ Decidable. The compiler only checks the "proof object."
  - _Bug:_ Clunky. You cannot just swap $a$ for $b$; you must explicitly "transport" terms along the path of equality.

## 2. Current Understanding (Coherent Narrative)

### The "Equality Reflection" Trap

In an ideal world (Extensional Type Theory), if you prove $1+1=2$, the compiler instantly knows that `Vec<2>` is the same type as `Vec<1+1>`.

- The Rule: If $\Gamma \vdash p: Id(a, b)$, then $\Gamma \vdash a \equiv b$.
- The Consequence: Type checking becomes proof search. To check if `x` fits in `Type A`, the compiler might have to discover a proof that `A` is equal to `B`. Since mathematical proof search is undecidable (Godel, Turing), the compiler might hang forever.

### The Intensional Solution (Identity Types)

To ensure the compiler always finishes (Decidability), modern systems (like Coq, Agda, Rust's type system) use Intensional Equality.

- Reification: Equality is not a silence system rule; it is a visible Type: `Identity<A, B>`.
- The J Operator: The mechanism to use this equality. It says "If you want to prove something for all equal pairs, just prove it for the reflexive case ($refl$)."
- The Friction: This makes "obvious" things hard. Even if $f$ and $g$ return the same results for all inputs (Function Extensionality), they are not _definitionally_ the same function, so you can't just swap them.

### The "Groupoid" Interpretation

Because Intensional Equality is "weak" (it doesn't force everything to be trivial), it accidentally created room for a richer structure.

- Types as Spaces:
  - Terms are Points.
  - Equalities are Paths between points.
  - Proofs of Equality between Equalities are Surfaces (Homotopies).
- This structure (Groupoid) gave birth to Homotopy Type Theory (HoTT).

## 3. Understanding Layers (Progressive Abstraction)

- Layer 1 (Compiler Engineer): We cannot allow Equality Reflection because we need the build to finish.
- Layer 2 (Mathematician): Intensional equality distinguishes between "definitionally equal" (computed to same bits) and "propositionally equal" (provable logic).
- Layer 3 (Topologist): Equality is not a binary switch (Yes/No); it is a Path in a space.

## 4. Minimum Viable Understanding (MVU)

- Definitional Equality: The compiler checks this automatically. (e.g., `2` == `1+1`).
- Propositional Equality: You must write a proof for this. (e.g., `x + y == y + x`).
- Transport: In Intensional systems, you cannot just "use" a propositional equality; you must explicitly run a function (Transport/J) to convert your data.

## 5. Tensions, Gaps, and Cross-SoT Coherence

- Gap: The lack of Function Extensionality (FunExt) in Intensional systems is painful. We know two functions are "equal", but the compiler won't let us treat them as such.
- Resolution: This tension leads directly to Cubical Type Theory, which tries to fix this without breaking decidability.

## 6. Sources and Links

- Source: Robert Harper, _Computational Type Theory_ (Lectures 3-4).
