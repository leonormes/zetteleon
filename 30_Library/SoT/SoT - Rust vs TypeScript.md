---
aliases: ["Rust for TypeScript Developers", "Rust vs TS", "Nominal vs Structural Typing"]
confidence: "5/5"
created: 2025-12-28T00:00:00Z
epistemic: "knowledge"
last_reviewed: "2025-12-28"
modified: 2025-12-28T18:49:16+00:00
purpose: "To provide a high-contrast comparative analysis between Rust and TypeScript to aid developers in shifting mental models."
review_interval: "12 months"
see_also: ["[[SoT - Rust Language]]", "[[SoT - Rust Type System]]"]
source_of_truth: []
status: "stable"
tags: ["rust", "typescript", "comparison", "language-design"]
title: SoT - Rust vs TypeScript
type: "SoT"
---

> **The Core Divergence:** While both languages use static analysis to improve reliability, TypeScript optimizes for **Flexibility** (matching the dynamic nature of JavaScript), while Rust optimizes for **Correctness and Performance** (matching the strict nature of hardware).

## 1. Type Philosophy: Nominal vs. Structural

The most fundamental shift for a TypeScript developer learning Rust is the nature of "Type Identity."

| Feature | TypeScript (Structural / Duck Typing) | Rust (Nominal Typing) |
|:--- |:--- |:--- |
| **Identity** | **Shape-based.** If it *looks* like a duck (has `walk()`), it *is* a duck. | **Name-based.** A type is defined by its explicit declaration name. |
| **Logic** | `interface A { x: number }` is compatible with `interface B { x: number }`. | `struct A { x: i32 }` is **distinct** from `struct B { x: i32 }`. |
| **Why?** | To interoperate with the "wild west" of existing JavaScript libraries. | To enforce semantic strictness and ensure invariants in systems code (e.g., `FileHandle` ≠ `SocketHandle`). |
| **Exception** | N/A | Rust uses structural typing for **Tuples** and **References**. |

## 2. Runtime Reality: Erasure vs. Monomorphization

This distinction dictates the performance characteristics and binary size of the final application.

### TypeScript: Type Erasure

- **Mechanism:** Types are ephemeral annotations. The compiler strips them out, leaving pure JavaScript.
- **Runtime:** The V8 engine (JIT) has to "guess" types at runtime using "Hidden Classes" and "Inline Caches."
- **Implication:** Zero binary bloat, but potential for "de-optimization" and unpredictable performance cliffs.

### Rust: Monomorphization

- **Mechanism:** The compiler generates a unique copy of the function for *every concrete type* used with a generic.
- **Runtime:** **Static Dispatch.** The CPU executes hard-coded memory offsets. No guessing.
- **Implication:** Fast, consistent execution at the cost of larger binary sizes (multiple copies of the same logic).

## 3. Memory Layout & Data Structures

### Objects vs. Structs

- **TS Objects:** A "bag of properties" scattered on the heap. Accessing a property involves pointer chasing.
- **Rust Structs:** Contiguous blocks of memory. Fields are packed side-by-side. Accessing a field is a simple offset calculation, maximizing **Cache Locality**.

### Sum Types: Discriminated Unions vs. Enums

| Feature | TypeScript (Discriminated Union) | Rust (Enum / ADT) |
|:--- |:--- |:--- |
| **Syntax** | `type Shape = { kind: "circle" } \| { kind: "square" }` | `enum Shape { Circle, Square }` |
| **Memory** | Discontiguous heap objects. | Contiguous memory block. Size = `MaxVariantSize + Tag`. |
| **Optimization** | Rely on string comparison of `"kind"`. | **Niche Optimization:** Can use invalid bit patterns (like Null) to store the tag for free (e.g., `Option<Box<T>>` has 0 overhead). |

## 4. Error Handling: Exceptions vs. Values

**TypeScript** (inheriting from JS) uses **Exceptions** (`throw` / `try-catch`).
- **Invisible Control Flow:** You cannot tell by looking at a function signature if it will throw.
- **Performance:** unwinding the stack is expensive.

**Rust** uses **Values** (`Result<T, E>`).
- **Explicit Control Flow:** Errors are just data returned on the stack.
- **Mandatory Handling:** You *must* deal with the `Result` (using `match` or `?`) or the code won't compile.

## 5. Minimum Viable Understanding (MVU)

1. **Rust Types exist at Runtime (compiled in):** Unlike TS types which vanish, Rust types dictate the physical layout of memory.
2. **Nominal Typing is stricter:** You cannot accidentally mix two types just because they have the same fields.
3. **Errors are Data:** Stop trying to `catch` errors. Start `matching` on them.
