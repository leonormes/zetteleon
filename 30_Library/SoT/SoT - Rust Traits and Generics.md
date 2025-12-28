---
aliases: ["Rust Generics", "Rust Traits", "Trait Bounds", "Monomorphization"]
confidence: "5/5"
created: 2025-12-27T20:31:13+00:00
epistemic: "knowledge"
last_reviewed: "2025-12-27"
modified: 2025-12-28T18:49:16+00:00
purpose: "To explain the mechanics of Rust's polymorphism, focusing on how Generics and Traits enable type abstraction with zero runtime cost."
review_interval: "6 months"
see_also: ["[[SoT - Rust Language]]", "[[SoT - Rust Type System]]", "[[SoT - Rust's Design Philosophy]]"]
source_of_truth: []
status: "stable"
tags: ["rust", "generics", "traits", "polymorphism", "compiler"]
title: SoT - Rust Traits and Generics
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Parametric Polymorphism
> **Generics** allow code to operate on abstract types (`T`), while **Traits** define the capabilities (interface) that `T` must possess.
> **The Cost:** Zero. Rust uses **Monomorphization** to generate concrete implementations for every specific type used, trading binary size for runtime speed.

## 2. Core Architecture: The Contract System

This system prevents "Combinatorial Explosion" by decoupling data from behavior.

| Component | Role | Analogy |
|:--- |:--- |:--- |
| **Generics (`<T>`)** | **The Placeholder.** A variable for a Type. | A template form with blank spaces. |
| **Traits** | **The Contract.** Defines required behavior. | The job description (must be able to `walk()`). |
| **Trait Bounds** | **The Gatekeeper.** Restricts `T` to specific Traits. | "Only hire people who meet the job description." |

### 2.1 The Syntax of Constraints

Rust offers two ways to define bounds. The `where` clause is preferred for complex types to separate the "What" from the "How".

```rust
// Inline (Simple)
fn print_id<T: Display>(item: T) { ... }

// Where Clause (Clean Architecture)
fn complex_logic<T, U>(a: T, b: U) 
where 
    T: Display + Clone, 
    U: Debug + Hash 
{ ... }
```

## 3. Mechanisms of Action

### 3.1 Monomorphization (The "Zero-Cost" Secret)

When you compile generic code, Rust performs a "Copy-Paste" operation. It looks at every place you call the function and generates a unique, optimized version for that specific type.

- **Input:** `fn process<T>(item: T)` called with `i32` and `String`.
- **Output:** Two distinct functions in the binary: `process_i32` and `process_String`.
- **Trade-off:** Fast execution (static dispatch) vs. Larger binary size.

### 3.2 Marker Traits (Compiler Signals)

Some traits have no methods but instruct the compiler to change its behavior.

- **`Sized`:** The type has a known size at compile time.
- **`Copy`:** The type is bitwise copyable (stack-only).
- **`Send` / `Sync`:** The type is safe to move/share across threads.

### 3.3 Extension Traits (Retroactive Abstraction)

This pattern allows you to add methods to types you do not own (e.g., standard library types), enabling a "fluent" API style.

1. **Define a Trait:** Create a trait with the desired new method.
2. **Implement Generic:** Implement it for *all* types that satisfy a condition (`impl<T: Iterator> MyExt for T`).
3. **Result:** You can now call `.my_method()` on `Vec::iter()` directly.

### 3.4 Conditional Capabilities (Conditional API)

You can restrict functionality based on the capabilities of the generic type. A method will **only exist** if the underlying type meets specific bounds.

- **Example:** A `Progress<T>` struct might only have a `.with_bound()` method if `T` implements `ExactSizeIterator`.
- **Safety:** Attempting to call this on an infinite stream is a compile-time error, not a runtime crash.

## 4. Minimum Viable Understanding (MVU)

1. **Generics let you write code once for many types.**
2. **Traits tell the compiler what those types must be able to do.**
3. **Rust generates specific code for each type used (Monomorphization), so there is no runtime slowdown.**
