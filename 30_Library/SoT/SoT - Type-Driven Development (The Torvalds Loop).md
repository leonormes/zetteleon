---
aliases: ["Data-Centric Programming", "Parse Don't Validate", "The Torvalds Loop", "Type-Driven Design", "Type-First Development", "Typestate Pattern"]
created: 2025-12-29T10:28:01+00:00
last_reviewed: "2026-04-04"
modified: 2026-04-19T18:30:30+00:00
source_of_truth: true
status: "stable"
synthesis-count: 3
tags: ["design-patterns", "programming", "rust", "SoftwareEngineering/Architecture", "TheHuman/Philosophy", "type_theory"]
title: SoT - Type-Driven Development (The Torvalds Loop)
type: "SoT"
updated: 
---

## 0. The Lineage

This protocol is the Methodological Implementation of the broader Data-Centric philosophy. It translates abstract principles into a concrete workflow.

- The Axiom (Physics): [[SoT - Data-Oriented Design]]—_Structure is truth; Code is a derivative._
- The Logic (Proofs): [[SoT - The Curry-Howard Correspondence (Propositions as Types)]]—_A program is a proof; a type is a proposition._
- The Theory (Math): [[MOC - Type Theory]]—_Using Category Theory (Sum/Product types) to model that structure rigorously._
- The Practice (Method): [[SoT - Type-Driven Development (The Torvalds Loop)]]—_The strict 4-phase protocol to execute the design._

---

## 1. The Core Mandate

> [!quote] Linus Torvalds
> "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."

The fundamental principle of this system is to move from [[SoT - Stringly Typed vs Strongly Typed|Stringly Typed]] logic (Bash/Go/JS) to "Type-Driven" architecture (Rust). We reject the entropy of defensive coding and instead Make Invalid States Physically Unrepresentable.

---

## 2. The Torvalds Loop: A Four-Phase Design Protocol

In this protocol, Logic is the _last_ consideration. We prioritize the physical reality of data over the behavior of code.

| Phase | Focus | Architectural Goal |
|:--- |:--- |:--- |
| 1. Shape | Physical Reality | Design memory layout (`struct`/`enum`) for cache efficiency and logical exclusion. (See: [[SoT - Rust Type Mechanics|Rust ADTs]]) |
| 2. Access | Mechanics | Define how data moves (Value vs. Pointer semantics). Control ownership and allocation. |
| 3. Invariants | Integrity | Define constraints that must _always_ be true. Use the type system to enforce them. |
| 4. Logic | Transformation | Write simple, linear algorithms that transform valid state A into valid state B. |

---

## 3. Pattern: Parse, Don't Validate

> [!definition] Parse, Don't Validate
> A design philosophy (coined by Alexis King) stating that we should Parse incoming data (transforming it into a structural Type that preserves the check) rather than just Validating it (checking a property and discarding the proof).

- Validation: checks `is_email(string) -> bool`. The output is still just a `string`. You have to check it again later.
- Parsing: checks `parse_email(string) -> Result<Email, Error>`. The output is an `Email` type. The existence of the instance _proves_ validity to the compiler.

### The Problem: "Shotgun Parsing"

When we rely on validation, we fall into the trap of Shotgun Parsing: checking data integrity ad-hoc, everywhere in the codebase.

- Redundancy: Every function checks `if valid(x)`.
- Fragility: If one function forgets to check, the system breaks.
- Boolean Blindness: The boolean result (`true`) doesn't carry _why_ it's valid or _what_ invariants are guaranteed.

### Example: The Non-Empty List

Validation Approach (Bad):

```rust
fn head(list: List<T>) -> Option<T> {
    if list.is_empty() { None } else { Some(list[0]) }
}
// You have to handle the Option case everywhere.
```

Parsing Approach (Good):

```rust
struct NonEmptyList<T>(T, Vec<T>); // Proof: Head is always present.

fn head(list: NonEmptyList<T>) -> T {
    list.0 // No check needed. Guaranteed by the type.
}
```

---

## 4. Pattern: [[SoT - Rust Type Mechanics#6.3 Type State Pattern (State Machines)|Typestate (State Machines)]]

We use Affine Types (Move Semantics) to enforce State Machines where invalid transitions are impossible.

### The Mechanics

1. State Types: Define structs for each state (`struct Draft`, `struct Published`).
2. Transition: The function consumes the old state (`self`) and returns the new state.

```rust
impl Post<Draft> {
    pub fn publish(self) -> Post<Published> { ... }
}
```

1. Enforcement: Because `self` is consumed, the old `Draft` value is invalidated. You physically cannot double-publish.

---

## 5. The Trinity: Mathematical Truth

Logic, Code, and Category Theory are isomorphic. This provides a rigorous foundation for data design.

### A. Sum Types (The "OR" Relationship)

- Rust Construct: `enum`.
- Logic: $A \lor B$.
- Rule: Used for Choice and State. If states are mutually exclusive, they must be variants of an Enum. (See: [[SoT - Rust Type Mechanics#3. Algebraic Data Types (Enums)|Rust Sum Types]])

### B. Product Types (The "AND" Relationship)

- Rust Construct: `struct`.
- Logic: $A \land B$.
- Rule: Used for Grouping data that must coexist.

---

## 6. Anti-Patterns to Exorcise

- Boolean Blindness: Using `bool` flags (e.g., `isBitnami`) to switch behavior.
    - _Fix:_ Use a Sum Type (`enum Vendor { Bitnami, Community }`).
- Primitive Obsession: Passing raw `String` or `Int` values for semantic concepts.
    - _Fix:_ Use NewTypes (`struct Version(String)`).
- Zombie States: Memory layouts where flags and data are decoupled (e.g., `isBuilt` flag + `artifact` field).
    - _Fix:_ Move the artifact into the `Built` variant of a `State` enum.

---

## 6.5 Paradigm Shift: OOD vs. Data-Centric

| Phase | OOD Perspective (Typical) | Data-Centric Perspective (Torvalds Loop) |
|:--- |:--- |:--- |
| Shape | Classes modelling "real world" concepts. | Structs modelling memory layout and hardware access. |
| Access | Getters/Setters, Encapsulation. | Semantic consistency (Value vs Pointer), API boundaries. |
| Invariants | Often checked inside every method or ignored. | Checked at the boundary (Construction); assumed true internally. |
| Logic | The primary focus; complex state management. | The final step; simple transformations of trusted data. |

---

## 7. Minimum Viable Understanding (MVU)

1. Data First: If the `struct` allows an invalid state, the architecture is broken.
2. Exhaustiveness: Use Enums for state; use the compiler to ensure every state is handled.
3. Mechanical Sympathy: Respect how the CPU sees your data (contiguity vs. indirection).

---

## See Also

- [[SoT - The Data-Centric Philosophy]]—_The worldview that prioritizes structure over logic._
- [[SoT - Rust Type Mechanics]]—_The deep dive into the specific mechanics of the Rust type system._
- [[SoT - The Curry-Howard Correspondence (Propositions as Types)]]—_The mathematical foundation for the program-as-proof paradigm._
- [[SoT - Stringly Typed vs Strongly Typed]]—_A detailed look at the pitfalls of primitive obsession._
- [[SoT - Conservation of Complexity]]—_The law that necessitates moving complexity into types._
