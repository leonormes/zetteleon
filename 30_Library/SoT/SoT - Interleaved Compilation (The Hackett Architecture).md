---
aliases: ["Hackett", "Interleaved Compilation", "Lisp-Haskell Fusion", "Type-Driven Macros"]
confidence: "5/5"
created: 2025-12-18T00:00:00Z
epistemic: "authoritative"
last_reviewed: "2025-12-18"
modified: 2025-12-25T11:40:21+00:00
purpose: "Defines the architectural pattern of interleaved macro expansion and type checking to enable type-aware meta-programming."
review_interval: "1 year"
see_also: ["[[SoT - Dependent Haskell and Singletons]]", "[[SoT - The Algebra of Types (Cardinality and Isomorphism)]]"]
source_of_truth: []
status: "stable"
tags: ["architecture", "macros", "programming_languages", "racket", "type_systems"]
title: SoT - Interleaved Compilation (The Hackett Architecture)
type: "SoT"
uid: 
updated: 
---

## 1. Working Knowledge (Stable Foundation)

- **The Goal:** To fuse the syntactic power of **Lisp Macros** with the semantic guarantees of **Haskell Type Classes**.
- **The Conflict:** Standard compilers are linear (`Parse -> Expand -> Type Check`). This blinds macros to type information.
- **The Solution:** **Interleaved Compilation**. The compiler pipeline is a loop: `Parse -> [Expand <-> Type Check] -> Compile`. Macros can query the type checker, and the type checker can drive macro expansion.

## 2. Current Understanding (Coherent Narrative)

### The Architectural Synthesis

Hackett unifies two distinct meta-programming peaks:

1. **Macros (Racket):** *Syntactic* transformation. Local scope. Blind to types.
2. **Type Classes (Haskell):** *Semantic* transformation. Global scope. Rigid syntax.

### The Mechanism: Type-Directed Macros

By interleaving expansion and checking, Hackett enables "Smart Macros" that know the *expected type* of the expression they are generating.

- **Example (Typed Holes):** A `todo!` macro can ask the compiler "What type is expected here?" and generate a compile-time error message saying "Expected `String -> Int`".
- **Example (DSLs):** A macro can generate a web server (like Servant) or a DB connection where the syntax is arbitrary (Lisp-like), but the generated code is strictly type-checked against a schema.

### Bidirectional Feedback

The live demo proves this is not just "Lisp with Types." The IDE integration (tooltips, red dots) works because the macro expansion phase is inextricably linked to the static analysis phase.

## 3. Understanding Layers (Progressive Abstraction)

- **Layer 1 (The Problem):** Macros are usually text-replacement tools that don't know if the code they generate makes sense.
- **Layer 2 (The Fix):** Give macros a "phone line" to the Type Checker.
- **Layer 3 (The Architecture):** Replace the linear compiler pipeline with a coroutine/loop between the Expander and the Checker.

## 4. Minimum Viable Understanding (MVU)

- **Standard Macros:** `Code -> Code`. (Blind).
- **Hackett Macros:** `(Code, ExpectedType) -> Code`. (Sighted).
- **Result:** You can write DSLs that feel dynamic (no boilerplate) but are statically verified.

## 5. Tensions, Gaps, and Cross-SoT Coherence

- **Complexity:** Implementing an interleaved compiler is significantly harder than a standard one.
- **Relation to Type Classes:** In this model, Type Classes are effectively "Type-Directed Macros" that operate on implicit parameters.

## 6. Sources and Links

- **Source:** Alexis King, *Hackett: Type-Aware Macros* (YouTube).
