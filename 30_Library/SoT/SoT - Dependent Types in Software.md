---
aliases: [Dependent Types, Type-Level Programming]
confidence: 4/5
confidence-gaps: [The practical application in mainstream languages is still an area of active research.]
created: 2025-12-19T13:17:01Z
decay-signals: []
epistemic: concept
last_reviewed: 2025-12-19
modified: 2025-12-19T13:23:46Z
purpose: "To define Dependent Types as a feature of advanced type systems that allows types to depend on values, enabling compile-time proofs of program correctness."
quality-markers: [Contrasts with traditional unit testing, Explains the 'making illegal states unrepresentable' philosophy., Provides a clear vector-indexing example]
related-soTs: ["[[SoT - Pragmatism vs Rigour in Software]]", "[[SoT - Quantitative Type Theory]]", "[[SoT - Runtime Guards vs Compile-Time Proofs]]"]
resonance-score: 9
review_interval: 18 months
see_also: []
source_of_truth: true
status: stable
supersedes: []
tags: ["compilers", "correctness", "formal-methods", "type-theory"]
title: SoT - Dependent Types in Software
type: SoT
uid: 
updated:
---

## 1. Definitive Statement

> [!definition] Definition
> **Dependent Types** are a feature of advanced type systems where types are allowed to depend on *values*. This blurs the line between types and program logic, allowing a developer to encode complex program invariants (properties that must always be true) directly into the type system. If the program compiles, the invariants are mathematically proven to hold, eliminating entire classes of runtime errors.

---

## 2. The Core Problem: The Brittleness of Runtime Assertions

In conventional programming, we ensure correctness by writing code and then writing *more code* (unit tests, assertions, runtime checks) to verify that the first batch of code was correct. This is fundamentally inefficient and error-prone.

| Failure Mode of Conventional Types | The Problem | The Dependent Type Solution |
| :--- | :--- | :--- |
| **Out-of-Bounds Errors** | A function that takes a list and an index has no compile-time guarantee that the index is valid. `get(list, 99)` is syntactically valid even if the list only has 2 elements. This must be checked at runtime. | **Types that Depend on Values:** A dependently-typed list would have the type `Vect n a` (a vector of `n` items of type `a`). A function to access it would take an index of type `Fin n` (a number *proven* to be less than `n`). An invalid index becomes a **compile-time type error**. |
| **Bugs in Tests** | Unit tests are just more code, and they can have bugs themselves. A test suite can pass while the underlying logic is still flawed. | **The Compiler as Prover:** The type checker acts as a mechanical theorem prover. If the types check out, the property is proven correct. It is not merely "tested"; it is verified. |
| **Illegal State Representation** | Conventional type systems allow you to represent impossible states (e.g., a `User` object where `isLoggedIn` is true but `sessionToken` is null). This must be prevented with defensive coding and assertions. | **Making Illegal States Unrepresentable:** The type system can enforce that a `LoggedInUser` type *must* contain a valid `sessionToken`. You cannot construct an object that violates the invariant. The invalid state cannot be modeled. |

---

## 3. The Architecture: Types as Propositions (Curry-Howard Correspondence)

Dependent types are the practical application of a deep idea in computer science: the **Curry-Howard Correspondence**, which states that a program is a proof, and its type is the proposition it proves.

### Example: A Type-Safe `head` Function

- **The Problem:** In most languages, getting the `head` (first element) of an empty list is a runtime error.
- **The Dependent Type Solution:**
    1. Define two types of lists: `Vect 0 a` (an empty vector) and `Vect (n+1) a` (a non-empty vector).
    2. The `head` function's type signature is: `head : Vect (n+1) a -> a`.
    3. This signature states that `head` can *only* be called on a vector that is proven, at compile time, to have at least one element.
    4. Calling `head` on an empty list is not a runtime error; it is a **type mismatch error** that the compiler catches immediately. You have failed to prove the proposition "this list is not empty."

This shifts the burden of proof from the programmer (writing a test) to the compiler (checking the types).

---

## 4. The "Prophecy Problem"

A major practical challenge for dependent types is that they often require information to be known at compile time that is only available at runtime (e.g., the length of a list received from a network request).

- **The Challenge:** You can't have a type `Vect n a` if `n` is the result of user input.
- **The Solution:** Dependently-typed programming forces a strict separation between the "un-trusted" boundaries of your application and the "proven" core. You write parsing code at the boundary that takes raw runtime data and transforms it into a dependently-typed structure. If the parsing and validation succeed, the core of your application can operate with full compile-time guarantees of correctness.

---

## 5. Minimum Viable Understanding (MVU)

1. **Dependent Types allow types to be based on values** (e.g., `ListOfN(5)` is a different type from `ListOfN(6)`).
2. **This lets you bake logic and rules directly into your types.** For example, the type for a list index can be "a number that is provably smaller than the list's length."
3. **This turns potential runtime bugs (like out-of-bounds errors) into compile-time type errors.**
4. **The philosophy is: "Make illegal states unrepresentable."** If your code compiles, it is correct in ways that tested code can never be.

---

## 6. Open Questions & Tensions

- **Tension:** **Cognitive Load vs. Benefit.** Writing dependently-typed code is significantly more difficult than conventional programming. It requires a different way of thinking that is closer to writing mathematical proofs. The key question is whether the benefit of provable correctness outweighs this massive increase in cognitive load.
- **Tension:** **The "Type-Level Programming" Rabbit Hole.** Dependent types can be so powerful that developers can get lost writing incredibly complex logic entirely within the type system, creating code that is impenetrable to anyone not an expert in type theory.
- **Confidence Gap:** Are dependent types the future of mainstream programming, or will they forever remain a powerful but niche tool for safety-critical domains like aerospace, finance, and cryptography?

## 7. Related Components

- [[SoT - Quantitative Type Theory]]
- [[SoT - Pragmatism vs Rigour in Software]]
- [[SoT - Runtime Guards vs Compile-Time Proofs]]
