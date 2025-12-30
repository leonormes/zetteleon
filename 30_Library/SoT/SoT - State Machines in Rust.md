---
aliases: ["Typestate Pattern", "State Machines in Type Theory", "Affine Types for State"]
confidence: "5/5"
created: 2025-12-30
epistemic: "architecture"
last_reviewed: "2025-12-30"
modified: 2025-12-30
purpose: "To define how Rust's type system (Enums and Ownership) is used to implement rigorous, zero-cost State Machines where invalid transitions are unrepresentable."
review_interval: "12 months"
see_also: ["[[SoT - Algebraic Data Types (ADTs)]]", "[[SoT - Rust's Ownership Model]]", "[[SoT - Parse, Don't Validate]]"]
source_of_truth: []
status: "stable"
tags: ["rust", "state-machines", "type-theory", "architecture", "safety"]
title: SoT - State Machines in Rust
type: "SoT"
uid: 
updated: 
---

## 1. Definition

> [!definition] State Machine (Type-Driven)
> A mechanism that uses the Type System to enforce the lifecycle of an object. It ensures that an entity can only exist in a valid state and can only transition to allowed subsequent states.

In Rust, this is achieved through two primary patterns: **Enum-based (Sum Types)** and **The Typestate Pattern (Affine Types)**.

---

## 2. Pattern A: Enum-based State Machines (Logical OR)

This is the standard approach for representing a state that can be one of several variants. It utilizes **Sum Types** to ensure only one state exists at a time.

- **Mechanism:** A single `enum` defines all possible states.
- **Safety:** Use `match` to ensure exhaustiveness (every state is handled).
- **Physicality:** The memory occupied is only as large as the largest variant plus the tag (Zero-cost).

```rust
enum Connection {
    Disconnected,
    Connecting(Attempt),
    Connected(Session),
    Error(String),
}
```

---

## 3. Pattern B: The Typestate Pattern (The "Moving" Proof)

This is the advanced pattern where each state is a **distinct Type**. It uses Rust's **Ownership (Affine Logic)** to "consume" the previous state, making it physically impossible to use an old state after a transition.

### The Mechanics
1. **Linear Progression:** A transition function consumes `self` (Ownership) and returns a new type.
2. **Compile-time Enforcement:** If you try to call a `read()` method on a `Closed` file, the compiler will fail because that method only exists for the `Open` type.

```rust
struct Draft;
struct Published;

struct Post<State> {
    content: String,
    _state: std::marker::PhantomData<State>,
}

impl Post<Draft> {
    // Transition: Consumes Draft, returns Published
    pub fn publish(self) -> Post<Published> {
        Post { content: self.content, _state: std::marker::PhantomData }
    }
}

impl Post<Published> {
    pub fn display(&self) { println!("{}", self.content); }
}
```

---

## 4. Comparison: Why Typestate?

| Feature | Enum-based | Typestate Pattern |
| :--- | :--- | :--- |
| **Logic Location** | Centralized in `match` blocks. | Distributed in specific `impl` blocks. |
| **Safety** | Runtime branch (safe). | **Compile-time** (impossible to call wrong methods). |
| **Memory** | Fixed size (Max variant). | 0 bytes (Phantom types/ZSTs). |
| **Use Case** | Data that changes at runtime (e.g., UI state). | Strict protocols (e.g., TLS Handshake, Driver init). |

---

## 5. Architectural Insight: State as a Witness

In the [[SoT - The Infrastructure Witness Pattern|Witness Pattern]], a state transition is essentially the generation of a new proof.

- **Input:** `Connection<Disconnected>`
- **Function:** `connect()`
- **Output:** `Connection<Connected>`

By requiring a `Connection<Connected>` as an argument for a `send_data` function, you make "sending on a closed socket" a **Type Error**, not a Runtime Error.

---

## 6. Minimum Viable Understanding (MVU)

1. **Move Semantics is the Key:** Consuming `self` during a transition ensures the "Old State" is deleted from existence.
2. **Phantom Types enable ZST States:** You can track complex state machines at compile-time with **zero** runtime memory overhead.
3. **Exhaustiveness:** Enums force you to handle every possible state, preventing "forgotten" edge cases.
