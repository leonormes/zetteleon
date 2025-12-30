---
aliases: []
alias: ["Type Algebra", "Cardinality of Types", "Isomorphic Refactoring", "Type Arithmetic"]
confidence: "5/5"
created: 2025-12-18T21:23:11+00:00
epistemic: "theory"
last_reviewed: "2025-12-30"
modified: 2025-12-30T14:11:33+00:00
purpose: "To define the rigorous mathematical rules for counting type states (Cardinality) and transforming structures without losing information (Isomorphism)."
review_interval: "6 months"
see_also: ["[[SoT - Algebraic Data Types (ADTs)]]", "[[SoT - The Trinity of Isomorphism (Logic, Computation, Categories)]]", "[[SoT - Rust's Design Philosophy]]"]
source_of_truth: []
status: "stable"
tags: ["type_theory", "math", "architecture", "rust"]
title: SoT - The Algebra of Types (Cardinality and Isomorphism)
type: "SoT"
uid: 
updated: 
---

## 1. The Arithmetic of Types

Just as we perform arithmetic on numbers, we can perform arithmetic on Types based on the number of possible values they inhabit. This count is called the **Cardinality**, denoted as $|T|$.

### 1.1 Fundamental Constants

- **Void ($0$):** The Empty Set. A type with **zero** values (e.g., Rust `enum Void {}`, `!`).
    - $|0| = 0$
- **Unit ($1$):** The Singleton Set. A type with **one** value (e.g., Rust `()`, `struct Unit;`).
    - $|1| = 1$
- **Bool ($2$):** A type with two values.
    - $|2| = 2$

### 1.2 Algebraic Operations

| Operation | Logical Equivalent | Type Construct | Formula |
|:--- |:--- |:--- |:--- |
| **Sum (+)** | OR (Disjunction) | Enum / Union | $|A + B| = |A| + |B|$ |
| **Product ($	imes$)** | AND (Conjunction) | Struct / Tuple | $|A 	imes B| = |A| 	imes |B|$ |
| **Exponential ($^$)** | Implication ($	o$) | Function | $|A 	o B| = |B|^{|A|}$ |

> **Why Exponentiation?**
> For a function `A -> B`, for *each* of the $|A|$ possible inputs, we must choose one of the $|B|$ possible outputs. Thus, we multiply $|B|$ by itself $|A|$ times.

---

## 2. Isomorphism ($\cong$)

Formally, two types $A$ and $B$ are **Isomorphic** ($A \cong B$) if there exist two total functions that allow lossless conversion back and forth:

$$f: A \to B$$

$$g: B \to A$$

$$g(f(a)) = a \quad \text{and} \quad f(g(b)) = b$$

In Rust, this is codified by the `From` and `Into` traits. If you can implement `From<A> for B` and `From<B> for A` without losing data, they are isomorphic.

### 2.1 Nominal vs. Structural Isomorphism

- **Structural Isomorphism:** Types are equal if their shape is equal (TypeScript).
- **Nominal Isomorphism:** Types are distinct by name but can be mapped (Rust).
    - `struct A { x: i32 }` and `struct B { x: i32 }` are distinct but isomorphic.
    - **Architecture Hint:** We use this to separate "Domain Models" from "DTOs" (Data Transfer Objects) even if they look identical.

---

## 3. Standard Isomorphisms (Refactoring Patterns)

These algebraic identities prove that certain refactorings are mathematically safe.

### 3.1 The Boolean Isomorphism ($2 \cong 1 + 1$)

The primitive `bool` is isomorphic to any Enum with two Unit variants.

```rust
// |Bool| = 2
let b: bool = true;

// |Bit| = 1 + 1 = 2
enum Bit { Zero, One }
```

### 3.2 The Distributive Law ($A \times (B + C) \cong A \times B + A \times C$)

This validates the equivalence between "Normalized" and "Denormalized" data structures.

- **LHS (Normalized):** `(A, Choice<B, C>)` - We store `A` once, alongside the choice.
- **RHS (Denormalized):** `Choice<(A, B), (A, C)>` - We store `A` inside every variant.

**Insight:** You can push shared state *into* variants or pull it *out* without changing the information content.

### 3.3 Currying (Exponential Laws) ($C^{A \times B} \cong (C^B)^A$)

A function taking a tuple is isomorphic to a function returning a function.

- `Fn(A, B) -> C` $\cong$ `Fn(A) -> Fn(B) -> C`

**Architecture Hint:** Dependency Injection is **Partial Application** (Currying). You apply the configuration (`A`) at startup, returning a handler that awaits the request (`B`) to produce the response (`C`).

### 3.4 Struct/Tuple Isomorphism

Named structs are isomorphic to anonymous tuples.

- `struct User { name: String, age: u8 }` $\cong$ `(String, u8)`

Use Tuples for local, ephemeral data transfer; use Structs for long-lived domain modeling.

---

## 4. The Zero-Cost Abstraction

Because isomorphic types have the same Cardinality (and often the same memory layout), the Rust compiler can often optimize the mapping functions ($f$ and $g$) into **No-Ops**.

Transforming a `DbUser` to a `ClientUser` (where fields are identical) compiles down to... nothing. The bits just move. This is the essence of **Zero-Cost Abstractions**.

```
