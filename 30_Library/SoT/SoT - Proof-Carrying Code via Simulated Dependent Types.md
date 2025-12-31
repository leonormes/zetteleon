---
aliases: ["Proof-Carrying Code", "Simulated Dependent Types", "Type Theory in Rust"]
confidence: "4/5"
created: 2025-12-18T00:00:00Z
epistemic: "derived"
last_reviewed: "2025-12-18"
modified: 2025-12-30T17:49:05+00:00
purpose: "Canonical reference for leveraging type systems to eliminate runtime failure modes."
review_interval: "6 months"
see_also: []
source_of_truth: []
status: "stable"
tags: ["architecture", "formal_verification", "rust", "software_design", "type_theory"]
title: SoT - Proof-Carrying Code via Simulated Dependent Types
type: "SoT"
uid: 
updated: 
---

## 1. Working Knowledge (Stable Foundation)

- **Definition:** Proof-Carrying Code is a software design pattern where the validity of data and logic is encoded directly into the type system. This forces the compiler to verify correctness, transforming runtime checks (which can panic) into compile-time theorems (which fail to build).
- **Core Mechanism:** **Dependent Typing**—where types depend on values. Since most mainstream languages lack native dependent types, this is simulated using **[[SoT - Type-Level Programming]]** (e.g., Peano arithmetic) and **Trait Bounds**.
- **Theoretical Basis:** The approach is grounded in resolving **Russell's Paradox** (avoiding self-reference) by establishing a strict hierarchy: Terms < Types < Kinds < Sorts.

## 2. Current Understanding (Coherent Narrative)

### The Problem: Runtime Uncertainty

Standard type systems prevent type errors (e.g., treating an integer as a string) but cannot prevent logic errors (e.g., accessing index 5 of a size-3 vector). These checks are typically relegated to runtime assertions (`assert!`), which result in panics (crashes) when violated.

### The Solution: Lifting Logic to Types

By moving constraints from values (runtime) to types (compile-time), we make invalid states **unrepresentable**.

1. **The Hierarchy of Types:** To avoid paradoxes, systems like Rust enforce stratification. Terms (values) cannot easily influence Types. Dependent types bridge this gap, allowing a Type to be "A vector of length N" where N is a value.
2. **Implementation Vectors:**
    - **Peano Arithmetic:** Numbers are defined as recursive types (`Zero`, `Successor<N>`) rather than `u32` values.
    - **Match Types (Scala 3):** An evolution of implicit resolution that provides direct, readable pattern matching on types.
    - **Proof-Carrying Structs:** Data structures (like `SizeProofVec<Length>`) include the logic in their signature. `Vec<Nat3>` is a distinct type from `Vec<Nat4>`.
    - **Trait Solver as Logic Engine:** Logic operations (equality, comparison) are implemented as traits. The compiler "solves" these traits to prove validity.

### The Benefit: Compile-Time Theorems

In this paradigm, a function like `copy_from` doesn't check sizes at runtime. It demands a *proof* (via the type system) that `SourceSize <= DestSize`. If the developer attempts to pass incompatible vectors, the code refuses to compile. The failure mode is shifted from "Crash in Production" to "Build Error."

## 3. Understanding Layers (Progressive Abstraction)

- **Layer 1 (Mental Model):** "Make invalid states impossible." If the logic is wrong, the code shouldn't just crash; it shouldn't exist.
- **Layer 2 (Mechanism):** Encode constraints (like size or state) into the Type Signature. The compiler checks the signature before running the code.
- **Layer 3 (Implementation):** Use recursive types (Peano numbers) and trait bounds to simulate value-dependent types in languages that don't support them natively.

## 4. Minimum Viable Understanding (MVU)

- **Goal:** Shift failure modes from Runtime (Panic) to Compile-Time (Error).
- **Technique:** Encode domain logic (e.g., vector length) into the type signature.
- **Mechanism:** In Rust, use **Phantom Data**, **Peano Arithmetic** (Type-level numbers), and **Trait Bounds** to force the compiler to verify constraints.
- **Outcome:** Bugs regarding these constraints become unrepresentable; the binary cannot be built if the logic is flawed.

## 5. Tensions, Gaps, and Cross-SoT Coherence

- **Tension (Safety vs. Ergonomics):** This approach introduces significant boilerplate and complexity ("Type Gymnastics"). It makes simple tasks verbose.
- **Gap:** Rust does not natively support Dependent Types (unlike Idris or Agda), making this a simulation rather than a first-class feature. The `const generics` feature in Rust alleviates some of this but has limitations.
- **Trade-off:** Best used for high-stakes core logic (cryptography, safety-critical systems) rather than general application code.

## 6. Sources and Links

- **Source:** Summary of *"Type Theory for the Working Rustacean"* (YouTube).
