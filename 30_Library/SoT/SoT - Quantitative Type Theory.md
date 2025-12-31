---
aliases: ["Graded Modalities", "Linear Types", "QTT"]
confidence: "4/5"
created: 2025-12-19T00:00:00Z
epistemic: "concept"
last_reviewed: "2025-12-19"
modified: 2025-12-30T17:49:05+00:00
purpose: "To define Quantitative Type Theory as a formal system for tracking resource usage and its superiority to simpler ownership models."
review_interval: "24 months"
see_also: ["[[SoT - Dependent Types in Software]]", "[[SoT - Rust's Ownership Model]]"]
source_of_truth: []
status: "stable"
tags: ["formal-methods", "programming-languages", "resource-management", "type-theory"]
title: SoT - Quantitative Type Theory
type: "SoT"
uid: 
updated: 
---

## 2. The Core Problem: Ownership is Too Coarse

Simple ownership systems (like Rust's) operate on a binary model: you either own a value (and can use it once before it's moved) or you borrow it. This is a subset of a more general problem: managing resources that have specific usage constraints.

| Failure Mode of Simple Ownership | The Problem | The QTT Solution |
|:--- |:--- |:--- |
| **Single-Use Limitation** | In a strict linear system, a value must be used exactly once. This is too restrictive for general programming. | **Graded Modalities:** QTT introduces types that explicitly quantify usage: 0, 1, or many times. A variable's type can specify its exact usage pattern. |
| **No Distinction Between Resources** | A network socket, a file handle, and a configuration struct are all treated the same way by the ownership system, even though their usage patterns are fundamentally different. | **Resource-Specific Types:** QTT allows you to create types that encode the precise usage rules of a resource. For example, a type for a file handle could enforce that it is opened, written to, and then closed, all at compile time. |
| **Inability to Express Fractional Ownership** | Complex data structures, like graphs or arenas, often require a concept of shared or fractional ownership that is difficult to express in a simple ownership model without runtime overhead (e.g., `Rc<T>`). | **Coeffects/Graded Semirings:** QTT can model complex sharing patterns by reasoning about resources algebraically, allowing for formal proofs about how data is shared and accessed. |

---

## 3. The Architecture: Graded Modalities

The core innovation of QTT is the **Graded Modality** (or "graded type"). Instead of just having a type `T`, you have a type `T [r]`, where `r` is a "grade" from a mathematical structure (like a semiring) that specifies the usage.

### Example: A Simple Usage Semiring

- **Grade `0`**: The value must not be used (e.g., it has been consumed).
- **Grade `1`**: The value must be used exactly once (a **linear type**). This is perfect for modeling resources that cannot be duplicated, like a unique pointer or a transaction handle.
- **Grade `ω` (Omega/Many)**: The value can be used any number of times (a traditional, unrestricted type).

A function's type signature can then make assertions about how it uses its arguments:

`fn process(file: File [1]) -> String [1]`

This signature states that the `process` function consumes exactly one `File` and produces exactly one `String`. The compiler can statically verify that this contract is met throughout the entire program.

### Relationship to Rust

Rust's ownership system can be seen as a pragmatic, hard-coded implementation of a very simple QTT:

- **Move semantics** approximate a linear type (`[1]`).
- **Types with the `Copy` trait** approximate an unrestricted type (`[ω]`).
- **Borrows** are a special, engineered mechanism to temporarily relax these rules.

QTT provides a unified, theoretical foundation for all these concepts, making it more expressive and consistent.

---

## 5. Minimum Viable Understanding (MVU)

1. **QTT is a type system that counts how many times you use a variable.**
2. **Instead of just "owning" or "borrowing", you can specify usages like "exactly once", "zero times", or "many times".**
3. **This allows for extremely precise, compile-time control over resources (like files, sockets, or memory), making leaks or misuse a compile error.**
4. **It's the formal, academic theory that Rust's ownership model is a practical-but-incomplete approximation of.**

---

## 6. Open Questions & Tensions

- **Tension:** **Annotation Overload & Complexity.** While powerful, QTT often requires significant annotations and a deep understanding of type theory, making it difficult to use for everyday programming. The complexity can be a major barrier to adoption.
- **Confidence Gap:** How much "quantity" information is actually useful? The full power of QTT may be overkill for many applications, and simpler systems like Rust's might represent a more practical trade-off for 99% of use cases.
- **Tension:** **Compiler Performance.** The type-checking and inference algorithms for full QTT can be significantly more complex and slower than for simpler type systems.

## 7. Related Components

- [[SoT - Dependent Types in Software]]
- [[SoT - Rust's Ownership Model]]
- [[SoT - Pragmatism vs Rigour in Software]]
