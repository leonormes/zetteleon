---
aliases: ["Type-Driven Design", "Rust Type State Pattern", "Parse Don't Validate", "Invariant Enforcement"]
confidence: "5/5"
created: 2025-12-27T20:28:33+00:00
epistemic: "pattern"
last_reviewed: "2025-12-27"
modified: 2025-12-28T18:49:16+00:00
purpose: "To document the patterns and mechanisms for using Rust's type system to enforce invariants and correctness at compile time."
review_interval: "6 months"
see_also: ["[[SoT - Rust Language]]", "[[SoT - Rust's Ownership Model]]", "[[SoT - Rust's Design Philosophy]]", "[[SoT - Dependent Types in Software]]"]
source_of_truth: []
status: "stable"
tags: ["rust", "type-system", "design-patterns", "architecture"]
title: SoT - Rust Type System
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Type-Driven Design
> A methodology where **business logic and invariants are encoded directly into the type system**, transforming runtime errors into compile-time compilation failures.
> **The Mantra:** "Parse, don't validate."
> **The Goal:** To make invalid states unrepresentable.

## 2. Core Concept: Invariant Enforcement

An **invariant** is a logical rule or condition that must remain true throughout a program's execution. Rust allows moving enforcement from **Runtime** (brittle, expensive) to **Compile-Time** (robust, zero-cost).

| Tier | Mechanism | Reliability | Cost |
|:--- |:--- |:--- |:--- |
| **Manual** | Documentation, Code Review, Tribal Knowledge. | Low (Human Error) | High (Debugging/Incidents) |
| **Runtime** | `assert!`, Unit Tests, Conditionals. | Medium (Crashes) | Medium (CPU/Latency) |
| **Type System** | **New Types**, **Type States**, **Enums**. | **High (Guaranteed)** | **Zero (Compile-time)** |

### 2.1 The "Parse, Don't Validate" Pattern

Instead of passing a primitive (e.g., `String`) and repeatedly validating it, you "parse" it once into a trusted Type.

- **Anti-Pattern (Validate):** A function accepts `email: String` and checks regex every time.
- **Pattern (Parse):**
    1. Define a `struct EmailAddress(String)`.
    2. Keep the inner field private.
    3. Provide a constructor (e.g., `parse()`) that returns `Result<EmailAddress, Error>`.
    4. Downstream functions accept `EmailAddress`, guaranteed to be valid by its very existence.

### 3. The Type State Pattern

This pattern uses the type system to model the **valid state transitions** of an object (finite state machine), making illegal operations impossible.

### Mechanics

1. **State Modeling:** Define distinct structs for each state (e.g., `OrderDraft`, `OrderPaid`, `OrderShipped`).
2. **Ownership Transitions:** Transition functions take `self` by value (consuming the old state) and return the new state.
    - `fn pay(self: OrderDraft) -> OrderPaid`
3. **Invalidation:** Because `OrderDraft` is consumed, the compiler prevents any further modification to the draft once it is paid. The "old" state no longer exists.

### Example: The Builder Pattern (Progress Bar)

Instead of a single struct with `Option` fields (runtime checks), use generics to track initialization state.

- **Start:** `ProgressBar<Unbounded>`
- **Transition:** calling `.with_limit(100)` returns `ProgressBar<Bounded>`.
- **Enforcement:** Methods like `.eta()` are *only* implemented for `ProgressBar<Bounded>`. Calling `.eta()` on an unbounded bar is a compiler error.

## 4. The Sum Type (Enum) Architecture

In Rust, an `enum` is a **Sum Type** (or Tagged Union), representing a closed set of mutually exclusive possibilities. This is the primary tool for "Making Invalid States Unrepresentable."

### Comparison: TypeScript vs. Rust

| Feature | TypeScript Enum | Rust Enum (Sum Type) |
|:--- |:--- |:--- |
| **Nature** | Named constants (Labels for numbers/strings). | Data containers (Algebraic Data Types). |
| **Data Payload** | None (only maps name to value). | Each **Variant** can hold distinct types/structs. |
| **Runtime** | Object/Lookup table. | Minimal overhead (Tag + Largest Variant size). |
| **Safety** | Open/Loose (can be bypassed with `any`). | **Exhaustive Matching**: Compiler forces handling of every variant. |

### The "Variant" Concept

A **Variant** is a formal "branch" of the type. It consists of:

1. **The Discriminant (Tag):** A hidden integer identifying which variant is active.
2. **The Payload:** The data stored within that branch.

> [!tip] Mental Model for TS Devs
> Think of a Rust Enum as a **Discriminated Union** (`type Shape = Circle | Square`) flattened into a single atomic structure where the "kind" field is managed automatically by the compiler.

## 5. Formal Modeling & Executable Specifications

As the type system grows, maintaining a manual mental model becomes unsustainable. The community uses formal frameworks to validate language features.

- **[[SoT - Rust Type System Modeling (Formality Core)]]**: Niko Matsakis's lightweight framework for defining grammar and judgment rules as executable Rust code. It allows testing new RFCs for soundness before stabilization.
- **Oxide**: A formalization of Rust using region-based aliasing to decouple lifetimes from the call stack.

## 6. Advanced: Pattern Types (Future)

*Note: As of late 2025, this is an emerging feature.*

Pattern types allow restricting the valid range of a base type directly in the signature (e.g., `u32` constrained to `1..=100`). This removes the need for "unsafe" compiler hacks for optimizations (like `NonZeroU32`) and allows the compiler to perform layout optimizations based on known valid bit patterns.

## 6. Minimum Viable Understanding (MVU)

1. **Make Invalid States Unrepresentable:** If a state shouldn't exist, the type system shouldn't allow you to write it.
2. **Trust the Types:** Once a value is created, it should be trusted. Do the hard work at the edges (parsing).
3. **Consume State:** Use ownership to destroy old states so they can't be reused incorrectly.
