---
aliases: ["The Rust Language", "RustLang"]
confidence: "5/5"
created: 2025-12-27T14:11:28+00:00
epistemic: "knowledge"
last_reviewed: "2025-12-27"
modified: 2025-12-27T20:31:38+00:00
purpose: "The canonical entry point for the Rust programming language in the SoT."
review_interval: "6 months"
see_also: ["[[MOC - Rust Programming Language]]", "[[SoT - Rust's Design Philosophy]]", "[[SoT - Rust's Ownership Model]]", "[[SoT - Rust Type System]]"]
source_of_truth: []
status: "stable"
tags: ["rust", "programming-language", "systems"]
title: SoT - Rust Language
type: "SoT"
---

> **Rust** is a multi-paradigm, general-purpose programming language that emphasizes performance, type safety, and concurrency. It enforces memory safety—that is, that all references point to valid memory—without requiring the use of a garbage collector or reference counting present in other memory-safe languages.

## 1. Key Characteristics

### Memory Safety without GC

Rust's defining feature. It uses an **Ownership** system with a **Borrow Checker** to prove at compile time that:

1. All memory access is valid.
2. No data races occur.
3. Resources are freed exactly when they are no longer needed.

See [[SoT - Rust's Ownership Model]].

### Zero-Cost Abstractions

Rust follows the C++ philosophy: "What you don't use, you don't pay for. And further: what you do use, you couldn't hand code any better."

- Higher-level concepts like Iterators, Closures, and Generics compile down to the same machine code as hand-written loops.

### Algebraic Type System

Rust's type system (Enums and Structs) allows for the expression of **Product Types** (Structs) and **Sum Types** (Enums).

- **Pattern Matching:** `match` allows for exhaustive handling of all possible states.
- **Traits:** Defines shared behavior (interfaces) rather than inheritance hierarchies.

See [[SoT - Rust Type System]].

## 2. The Module System: Namespacing vs. Location

Rust uses an absolute/relative path system similar to a filesystem.

| Syntax | Mental Model | Translation |
|:--- |:--- |:--- |
| `crate::` | `@/` (Root Alias) | Points to the root of the project (`src/lib.rs`). |
| `super::` | `../` | Points to the parent module. |
| `::` | Path Separator | Navigates locations (e.g., `std::io::stdin`). |
| `:` | Constraint | Defines a requirement (e.g., `T: Clone`). |

## 3. Traits & The `#[derive]` Macro

Rust uses **Traits** as interfaces. The `#[derive]` attribute is a **compile-time code generator** (macro) that automatically "polyfills" standard logic for your types.

### Common Derivable Traits

| Trait | TS Mental Model | Purpose |
|:--- |:--- |:--- |
| **`Debug`** | `util.inspect()` | Allows formatting for dev logs via `{:?}`. |
| **`Clone`** | `structuredClone()` | Deep copies data (required for move semantics). |
| **`PartialEq`** | `isEqual(a, b)` | Implements `==` logic. |
| **`Eq`** | "Total Equality" | A marker that `a == a` is **always** true (Floats are not `Eq`). |
| **`Default`** | Initial State | Provides a baseline via `Type::default()`. Use `#[default]` on an enum variant. |

### The Recursive Requirement Chain

`derive` is strictly declarative. It can only generate logic if **every internal field** of the struct/enum also implements that trait. If one variant contains a type that cannot be cloned (e.g., a File Stream), the entire enum cannot `derive(Clone)`.

## 4. The Ecosystem

- **Cargo:** The integrated build system and package manager. It handles dependencies, building, testing, and documentation generation.
- **Crates.io:** The central registry for Rust packages.
- **Clippy:** A collection of lints to catch common mistakes and improve code quality.

## 5. Use Cases

- **Systems Programming:** Operating systems, game engines, file systems.
- **CLI Tools:** High-performance, cross-platform command-line utilities.
- **WebAssembly:** Running near-native code in the browser.
- **Network Services:** High-throughput, low-latency servers.

## 6. Common Anti-Patterns

- **Lazy Error Handling:** Using `.unwrap()` or `.expect()` in production code instead of propagating errors with `?` or handling them via `match`.
- **Cloning Everywhere:** Using `.clone()` to satisfy the borrow checker instead of fixing ownership or using references/`Arc`.
- **Glob Imports:** `use crate::*;` leads to namespace pollution and future breakage.
- **Stringly Typed:** Passing `String` everywhere instead of using specific Types (see [[SoT - Rust Type System]]).

## 7. Minimum Viable Understanding (MVU)

1. **Rust = Safety + Speed.** It replaces C/C++.
2. **The Compiler is strict.** It forces you to handle memory correctly *before* the program runs.
3. **Modern Tooling.** It comes with a modern package manager and build system out of the box.

### Polymorphism (Generics)

Rust avoids "Type Rigidity" via Parametric Polymorphism. It allows you to write code that is abstract over types but compiled into optimized machine code for each specific use.

- **Generics (`<T>`):** Placeholders for types.
- **Traits:** Contracts that define what those types must be able to do.

See [[SoT - Rust Traits and Generics]].

^See [[SoT - Rust Type System]].
