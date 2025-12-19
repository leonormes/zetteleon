---
aliases: ["Dependent Haskell", "Proof-Carrying Code in Haskell", "Singleton Pattern", "Type-Level Programming"]
confidence: 5/5
confidence-gaps: []
created: 2025-12-18T12:00:00Z
decay-signals: ["GHC implementation of full Dependent Types (breaking change)"]
epistemic: authoritative
last_reviewed: 2025-12-18
modified: 2025-12-19T10:12:37Z
purpose: Defines the architectural patterns for implementing Dependent Types in Haskell using Singletons and GADTs.
quality-markers: ["Synthesized from Stephanie Weirich's Dependent Haskell Talk"]
related-soTs: ["[[SoT - Computational Type Theory (Meaning as Use)]]", "[[SoT - Proof-Carrying Code via Simulated Dependent Types]]"]
resonance-score: 8
review_interval: 1 year
see_also: []
source_of_truth: true
status: stable
tags: ["architecture", "functional_programming", "haskell", "singletons", "type_theory"]
title: SoT - Dependent Haskell and Singletons
type: SoT
uid:
updated:
---

## 1. Working Knowledge (Stable Foundation)

- **The Goal:** To bridge the "Syntax Gap" between the **Term Level** (Runtime Values) and the **Type Level** (Compile-time Logic) in Haskell.

- **The Problem:** Haskell traditionally separates these worlds. We want to write functions where the *Type* of the output depends on the *Value* of the input.

- **The Solution (The Singleton Pattern):** A structural bridge that mirrors runtime values at the type level.

  - **Promoted Constructors:** Lifting data (like `'True`, `'False`) to be Types.

  - **Singleton Types (`SBool`):** A GADT that links the Term-level value (`True`) to the Type-level index (`'True`).

## 2. Current Understanding (Coherent Narrative)

### The Architecture of Dependent Haskell

Weirich demonstrates a "Compiler-Driven Development" workflow where the compiler acts as a query engine for domain logic.

1. **Promoted Data Constructors:**
    - Standard Haskell: `True` is a value of type `Bool`.
    - Dependent Haskell: `'True` is a Type of kind `Bool`. We "lift" data to the type level so the compiler can reason about it.

2. **The Singleton Bridge ("Fake Pi Types"):**
    - To write a dependent function (where $f(x)$ returns a type depending on $x$), we need to know *which* type to return at runtime.
    - **The Mechanism:** The `Singleton` library generates a "Mirror Type" (e.g., `SOnce`, `SMany`).
    - **Pattern Matching:** When you match on a Singleton (`case s of SOnce -> ...`), you prove to the compiler exactly which Type-level branch is active. This is the "runtime witness" for the static proof.

3. **Proof-Carrying Code (Type Error Engineering):**
    - **Concept:** Encode business logic (like Regex capture groups) into the Type System.
    - **Result:** A function accessing a regex group isn't just checking a string; it's proving the group exists.
    - **Failure Mode:** If you access a non-existent group, the error is not "Type Mismatch" but a specific domain error (e.g., "Field 'f' not found in schema").

### Template Haskell as Parser

The architecture uses Template Haskell (`[r| ... |]`) as the **Ingress Controller**. It parses raw strings (Regex) and generates the rigid, type-indexed AST that the rest of the system relies on.

## 3. Understanding Layers (Progressive Abstraction)

- **Layer 1 (The Pattern):** Mirror every Value with a Type. Connect them with a Singleton GADT.

- **Layer 2 (The Flow):** Parse Data -> Generate Types -> Write Code that matches on Singletons -> Compiler proves Logic.

- **Layer 3 (The Mental Model):** We are tricking a non-dependent language into behaving dependently by manually carrying the "Runtime Witness" (Singleton) that a true Dependent Language would carry automatically.

## 4. Minimum Viable Understanding (MVU)

- **Promoted Types:** `DataKinds` lets us use values as types.

- **Singletons:** `SValue` links the runtime value to the promoted type.

- **Dependent Match:** Matching on `SValue` reveals type information to the compiler.

## 5. Tensions, Gaps, and Cross-SoT Coherence

- **Comparison with Rust:** This is the Haskell equivalent of the "Simulated Dependent Types" technique in [[SoT - Proof-Carrying Code via Simulated Dependent Types]].

  - *Rust:* Uses Traits and PhantomData.

  - *Haskell:* Uses GADTs and DataKinds (Singletons).

- **Boilerplate:** Both approaches suffer from high verbosity ("Type Gymnastics") to achieve what languages like Idris do natively.

## 6. Sources and Links

- **Source:** Stephanie Weirich, *Dependent Types in Haskell* (YouTube).
