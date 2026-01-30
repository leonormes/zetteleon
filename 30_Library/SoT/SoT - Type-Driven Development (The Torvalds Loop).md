---
aliases: ["Data-Centric Programming", "Parse Don't Validate", "The Torvalds Loop", "Type-Driven Design", "Type-First Development", "Typestate Pattern"]
confidence: "5/5"
created: 2025-12-29T10:28:01+00:00
epistemic: "authoritative"
last_reviewed: "2025-12-30"
modified: 2026-01-23T18:09:16+00:00
purpose: "To define the core programming philosophy of ProdOS: a synthesis of hardware-conscious data design and mathematical type theory."
review_interval: "6 months"
see_also: ["[[SoT - Rust Language]]", "[[SoT - Rust Type Mechanics]]", "[[SoT - Rust's Ownership Model]]"]
source_of_truth: []
status: "stable"
tags: ["design-patterns", "programming", "rust", "SoftwareEngineering/Architecture", "TheHuman/Philosophy", "type_theory"]
title: SoT - Type-Driven Development (The Torvalds Loop)
type: "SoT"
uid: 
updated: 
---

## 0. The Lineage

This protocol is the **Methodological Implementation** of the broader Data-Centric philosophy. It translates abstract principles into a concrete workflow.

- **The Axiom (Physics):** **[[SoT - Data-Oriented Design]]**—_Structure is truth; Code is a derivative._
- **The Theory (Math):** **[[MOC - Type Theory]]**—_Using Category Theory (Sum/Product types) to model that structure rigorosuly._
- **The Practice (Method):** **[[SoT - Type-Driven Development (The Torvalds Loop)]]**—_The strict 4-phase protocol to execute the design._

---

## 1. The Core Mandate

> [!quote] Linus Torvalds
> "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."

The fundamental principle of this system is to move from **"Stringly Typed"** logic (Bash/Go/JS) to **"Type-Driven"** architecture (Rust). We reject the entropy of defensive coding and instead **Make Invalid States Physically Unrepresentable**.

---

## 2. The Torvalds Loop: A Four-Phase Design Protocol

In this protocol, Logic is the _last_ consideration. We prioritize the physical reality of data over the behavior of code.

| Phase | Focus | Architectural Goal |
|:--- |:--- |:--- |
| **1. Shape** | **Physical Reality** | Design memory layout (`struct`/`enum`) for cache efficiency and logical exclusion. |
| **2. Access** | **Mechanics** | Define how data moves (Value vs. Pointer semantics). Control ownership and allocation. |
| **3. Invariants** | **Integrity** | Define constraints that must _always_ be true. Use the type system to enforce them. |
| **4. Logic** | **Transformation** | Write simple, linear algorithms that transform valid state A into valid state B. |

---

## 3. Pattern: Parse, Don't Validate

Do not write code to "validate" messy input repeatedly. Instead, **parse** it _once_ at the edge into a Type where the invalid state cannot exist.

- **Anti-Pattern:** Passing `email: String` and running a regex check in every function.
- **Pattern:**
    1. Define `struct Email(String)`. Keep the field private.
    2. Constructor `Email::parse(s: String) -> Result<Email, Error>` performs the check.
    3. Functions accept `e: Email`. The existence of the instance _proves_ validity to the compiler.

---

## 4. Pattern: Typestate (State Machines)

We use **Affine Types** (Move Semantics) to enforce State Machines where invalid transitions are impossible.

### The Mechanics

1. **State Types:** Define structs for each state (`struct Draft`, `struct Published`).
2. **Transition:** The function consumes the old state (`self`) and returns the new state.

```rust
impl Post<Draft> {
    pub fn publish(self) -> Post<Published> { ... }
}
```

1. **Enforcement:** Because `self` is consumed, the old `Draft` value is invalidated. You physically cannot double-publish.

---

## 5. The Trinity: Mathematical Truth

Logic, Code, and Category Theory are isomorphic. This provides a rigorous foundation for data design.

### A. Sum Types (The "OR" Relationship)

- **Rust Construct:** `enum`.
- **Logic:** $A \lor B$.
- **Rule:** Used for **Choice** and **State**. If states are mutually exclusive, they must be variants of an Enum.

### B. Product Types (The "AND" Relationship)

- **Rust Construct:** `struct`.
- **Logic:** $A \land B$.
- **Rule:** Used for **Grouping** data that must coexist.

---

## 6. Anti-Patterns to Exorcise

- **Boolean Blindness:** Using `bool` flags (e.g., `isBitnami`) to switch behavior.
    - _Fix:_ Use a Sum Type (`enum Vendor { Bitnami, Community }`).
- **Primitive Obsession:** Passing raw `String` or `Int` values for semantic concepts.
    - _Fix:_ Use **NewTypes** (`struct Version(String)`).
- **Zombie States:** Memory layouts where flags and data are decoupled (e.g., `isBuilt` flag + `artifact` field).
    - _Fix:_ Move the artifact into the `Built` variant of a `State` enum.

---

## 6.5 Paradigm Shift: OOD vs. Data-Centric

| Phase | OOD Perspective (Typical) | Data-Centric Perspective (Torvalds Loop) |
|:--- |:--- |:--- |
| **Shape** | Classes modelling "real world" concepts. | Structs modelling memory layout and hardware access. |
| **Access** | Getters/Setters, Encapsulation. | Semantic consistency (Value vs Pointer), API boundaries. |
| **Invariants** | Often checked inside every method or ignored. | Checked at the boundary (Construction); assumed true internally. |
| **Logic** | The primary focus; complex state management. | The final step; simple transformations of trusted data. |

---

## 7. Minimum Viable Understanding (MVU)

1. **Data First:** If the `struct` allows an invalid state, the architecture is broken.
2. **Exhaustiveness:** Use Enums for state; use the compiler to ensure every state is handled.
3. **Mechanical Sympathy:** Respect how the CPU sees your data (contiguity vs. indirection).
