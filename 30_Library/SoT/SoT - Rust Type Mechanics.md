---
aliases: ["Rust Type System", "Rust Generics", "Rust Traits", "Monomorphization", "Rust ADTs"]
confidence: "5/5"
created: 2025-12-27T20:28:33+00:00
epistemic: "technical"
last_reviewed: "2025-12-30"
modified: 2025-12-31T11:19:03+00:00
purpose: "To define the mechanical components of Rust's Type System: Generics, Traits, Bounds, and Layout."
review_interval: "6 months"
see_also: ["[[SoT - Rust Language]]", "[[SoT - Type-Driven Development (The Torvalds Loop)]]"]
source_of_truth: []
status: "stable"
tags: ["architecture", "compilers", "rust", "type-system"]
title: SoT - Rust Type Mechanics
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

Rust uses a **Nominal, Static, Affine Type System** with **Parametric Polymorphism** (Generics) and **Ad-hoc Polymorphism** (Traits).

- **Nominal:** A type is defined by its name (`struct A`), not its shape. `struct A { x: i32 }`!= `struct B { x: i32 }`.
- **Static:** Types are resolved at compile time.
- **Affine:** Values can be used at most once (Move Semantics).

---

## 2. Polymorphism: Generics & Traits

### 2.1 The Architecture

| Component | Role | Analogy |
|:--- |:--- |:--- |
| **Generics (`<T>`)** | **The Placeholder.** A variable for a Type. | A form with blank spaces. |
| **Traits** | **The Contract.** Defines required behavior. | The job description (must `impl Display`). |
| **Bounds** | **The Gatekeeper.** Restricts `T` to specific Traits. | "Only hire candidates who meet the description." |

### 2.2 Monomorphization (The Performance Secret)

Rust does not use type erasure (like Java/TS) or v-tables (like C++ virtual functions) by default. It uses **Monomorphization**.

- **Process:** The compiler analyzes every usage of `fn process<T>(x: T)`.
- **Generation:** It generates a unique copy for each concrete type (e.g., `process_i32`, `process_String`).
- **Result:** **Static Dispatch.** The CPU executes hard-coded memory offsets. Zero runtime overhead.

---

## 3. Algebraic Data Types (Enums)

In Rust, an `enum` is a **Sum Type** (Tagged Union), representing a closed set of mutually exclusive possibilities.

- **Comparison:** Unlike C/TS Enums (which are integers/constants), Rust Enums can hold different shapes of data per variant.
- **Exhaustiveness:** `match` expressions must handle *every* variant. This makes invalid states unrepresentable.
- **Optimization:** Rust uses "Niche Optimization" (e.g., using a pointer's null-bit to store the tag) to often make `Option<Box<T>>` the same size as `Box<T>`.

---

## 4. Zero-Sized Types (ZST)

A unique architectural feature is the **Zero-Sized Type**.

- **Definition:** A struct with no fields: `struct Token;`.
- **Size:** 0 bytes. It does not exist at runtime.
- **Utility:** Used as a **Type Witness** or **State Token** in Type-Driven Development. Passing it around costs nothing but proves a logical fact to the compiler.

---

## 5. Related Components

- For design patterns using these mechanics (Parse don't Validate, Typestates), see [[SoT - Type-Driven Development (The Torvalds Loop)]].
- For memory rules, see [[SoT - Rust's Ownership Model]].

---

## 6. Applied Patterns (Will Crichton)

How to use these mechanics to build "Misuse-Resistant" APIs.

### 6.1 Extension Traits (Retroactive Abstraction)

You can add methods to types you do not own (e.g., standard library types) by defining a new trait and implementing it.

* **Mechanism:** `impl<T: Iterator> MyExtension for T {... }`
* **Result:** Enables fluent dot-notation (`vec.iter().my_custom_method()`) without modifying upstream code.

### 6.2 Conditional Capabilities (Trait Bounds)

Functionality can be conditionally enabled based on the properties of T.

* **Mechanism:** `impl<T> Progress<T> where T: ExactSizeIterator {... }`
* **Result:** The method `show_eta()` is *only* physically available if the underlying iterator knows its length. Calling it on an unbounded stream is a compile-time error.

### 6.3 Type State Pattern (State Machines)

Encoding the state of an object into its Type to make invalid transitions unrepresentable.

* **Mechanism:** `fn start(self: Request<Builder>) -> Request<Pending>`
* **Result:** You cannot call `send()` on a `Builder`; you must transition it to `Pending` first. The compiler enforces the order of operations.
