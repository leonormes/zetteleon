---
aliases: ["Monomorphization", "Rust ADTs", "Rust Generics", "Rust Traits", "Rust Type System"]
created: 2025-12-27T20:28:33+00:00
last_reviewed: "2025-12-30"
modified: 2026-02-01T15:07:52+00:00
status: "stable"
tags: ["compilers", "rust", "SoftwareEngineering/Architecture", "type-system"]
title: SoT - Rust Type Mechanics
type: "SoT"
updated: 
---

## 1. Definitive Statement

Rust uses a Nominal, Static, Affine Type System with Parametric Polymorphism (Generics) and Ad-hoc Polymorphism (Traits).

- Nominal: A type is defined by its name (`struct A`), not its shape. `struct A { x: i32 }`!= `struct B { x: i32 }`.
- Static: Types are resolved at compile time.
- Affine: Values can be used at most once (Move Semantics).

---

## 2. Polymorphism: Generics & Traits

### 2.1 The Architecture

| Component | Role | Analogy |
|:--- |:--- |:--- |
| Generics (`<T>`) | The Placeholder. A variable for a Type. | A form with blank spaces. |
| Traits | The Contract. Defines required behavior. | The job description (must `impl Display`). |
| Bounds | The Gatekeeper. Restricts `T` to specific Traits. | "Only hire candidates who meet the description." |

### 2.2 Monomorphization (The Performance Secret)

Rust does not use type erasure (like Java/TS) or v-tables (like C++ virtual functions) by default. It uses Monomorphization.

- Process: The compiler analyzes every usage of `fn process<T>(x: T)`.
- Generation: It generates a unique copy for each concrete type (e.g., `process_i32`, `process_String`).
- Result: Static Dispatch. The CPU executes hard-coded memory offsets. Zero runtime overhead.

---

## 3. Algebraic Data Types (Enums)

In Rust, an `enum` is a Sum Type (Tagged Union), representing a closed set of mutually exclusive possibilities.

- Comparison: Unlike C/TS Enums (which are integers/constants), Rust Enums can hold different shapes of data per variant.
- Exhaustiveness: `match` expressions must handle _every_ variant. This makes invalid states unrepresentable.
- Optimization: Rust uses "Niche Optimization" (e.g., using a pointer's null-bit to store the tag) to often make `Option<Box<T>>` the same size as `Box<T>`.

---

## 4. Zero-Sized Types (ZST)

A unique architectural feature is the Zero-Sized Type.

- Definition: A struct with no fields: `struct Token;`.
- Size: 0 bytes. It does not exist at runtime.
- Utility: Used as a Type Witness or State Token in Type-Driven Development. Passing it around costs nothing but proves a logical fact to the compiler.

---

## 5. Memory Layout & Padding

Rust structs are not always tightly packed. They must satisfy alignment requirements (e.g., a `u64` must start at a memory address divisible by 8).

### 5.1 The Padding Problem

The compiler inserts invisible padding bytes to ensure alignment, which wastes cache space.

```rust
struct Bad {
    a: u8,   // 1 byte
    // 7 bytes padding
    b: u64,  // 8 bytes
} // Total: 16 bytes (50% waste)
```

### 5.2 The Solution: Field Reordering

Order fields from Largest to Smallest to minimize padding.

```rust
struct Good {
    b: u64,  // 8 bytes
    a: u8,   // 1 byte
    // 7 bytes padding at end (only if needed for array alignment)
}
```

---

## 6. Related Components

- For design patterns using these mechanics (Parse don't Validate, Typestates), see [[SoT - Type-Driven Development (The Torvalds Loop)]].
- For memory rules, see [[SoT - Rust's Ownership Model]].

---

## 7. Applied Patterns (Will Crichton)

How to use these mechanics to build "Misuse-Resistant" APIs.

### 6.1 Extension Traits (Retroactive Abstraction)

You can add methods to types you do not own (e.g., standard library types) by defining a new trait and implementing it.

- Mechanism: `impl<T: Iterator> MyExtension for T {… }`
- Result: Enables fluent dot-notation (`vec.iter().my_custom_method()`) without modifying upstream code.

### 6.2 Conditional Capabilities (Trait Bounds)

Functionality can be conditionally enabled based on the properties of T.

- Mechanism: `impl<T> Progress<T> where T: ExactSizeIterator {… }`
- Result: The method `show_eta()` is _only_ physically available if the underlying iterator knows its length. Calling it on an unbounded stream is a compile-time error.

### 6.3 Type State Pattern (State Machines)

Encoding the state of an object into its Type to make invalid transitions unrepresentable.

- Mechanism: `fn start(self: Request<Builder>) -> Request<Pending>`
- Result: You cannot call `send()` on a `Builder`; you must transition it to `Pending` first. The compiler enforces the order of operations.
