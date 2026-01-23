---
alias: ["Applied Type Theory", "Type Theory Study Plan"]
aliases: []
confidence: "5/5"
created: 2025-12-29T23:32:47+00:00
epistemic: "curriculum"
last_reviewed: "2025-12-29"
modified: 2026-01-23T18:09:23+00:00
purpose: "A purely practical, code-first curriculum to master Type Theory by refactoring code and proving correctness in Rust."
review_interval: "3 months"
see_also: ["[[MOC - Type Theory]]", "[[SoT - Type-Driven Development (The Torvalds Loop)]]"]
source_of_truth: []
status: "active"
tags: ["curriculum", "exercises", "practice", "rust"]
title: Type Theory Curriculum
type: "Project"
uid: 
updated: 
---

## 1. The Strategy: "Proof by Implementation"

You stated you struggle to **implement** and **explain**. This curriculum solves that by inverting the standard learning model:

1. **Do (Code First):** You will write code that fails to compile until the logic is correct.
2. **Explain (Feynman Test):** You will write a 3-sentence "commit message" explaining _why_ the refactor was necessary.

> **The Capstone Project:** You will iteratively build a **Secure Payment State Machine**.

---

## 2. Level 1: The Shape of Data (Algebraic Data Types)

**Theory:** Types are not just labels; they are Sets. We count them to measure complexity.
- **Reading:** [[SoT - The Algebra of Types (Cardinality and Isomorphism)]]

### 🛠️ Practical Challenge 1: The Boolean Blindness Exorcism

**Scenario:** You have a `struct` with multiple boolean flags. This is a "Product Type" explosion ($2 \times 2 \times 2 = 8$ states).
**Task:** Refactor the following "Zombie Struct" into a proper "Sum Type" (`enum`).

_Bad Code (Start Here):_

```rust
struct Request {
    is_loading: bool,
    is_success: bool,
    is_error: bool,
    data: Option<String>,
    error_msg: Option<String>,
}
// Problem: What does `is_loading: true, is_error: true` mean?
```

_Required Output:_

- Create an `enum RequestState` where invalid combinations (like Loading + Error) are physically impossible to represent.

### 🗣️ The Feynman Test

> "Explain to a Java/Python developer why `Option<T>` is mathematically safer than `null`. Do not use the word 'Monad'. Use the concept of a 'Box' that might be empty."

---

## 3. Level 2: Logic as Code (Propositions as Types)

**Theory:** Writing a function is writing a proof. If `fn(A) -> B` compiles, you have proved that "If I have A, I can produce B."
- **Reading:** [[SoT - The Curry-Howard Correspondence (Propositions as Types)]]

### 🛠️ Practical Challenge 2: The "Parse, Don't Validate" Pattern

**Scenario:** You have a function that accepts a `String` and returns a `String`. This is "Stringly Typed."
**Task:** Create a **NewType** `EmailAddress` that _cannot_ be constructed with invalid data.

_Bad Code:_

```rust
fn send_email(to: String, body: String) {
    if !to.contains("@") { panic!("Invalid email!"); }
    // ...
}
```

_Required Output:_

1. Define `struct EmailAddress(String);`.
2. Implement a `parse` constructor: `impl TryFrom<String> for EmailAddress`.
3. Refactor `send_email` to accept `EmailAddress`.
4. **Goal:** Remove the `if` check from `send_email`. The validation happens _once_ at the edge; the function logic is now "correct by construction."

### 🗣️ The Feynman Test

> "Explain why 'NewTypes' (wrapper structs) are free in Rust (Zero-Cost Abstractions) but expensive in languages like Java (Object Overhead)."

---

## 4. Level 3: Time & Transition (Affine Types & State Machines)

**Theory:** Data has a lifecycle. It flows from one state to another. We use **Move Semantics** (Affine Types) to consume the old state so it can never be used again.
- **Reading:** [[SoT - Type-Driven Development (The Torvalds Loop)]]

### 🛠️ Practical Challenge 3: The Payment State Machine

**Scenario:** A Payment can be `Pending`, `Authorized`, or `Settled`. You cannot Settle a Pending payment without Authorizing it first.
**Task:** Implement the **Type State Pattern**.

_Code Goal:_

```rust
let pending = Payment::new(100);
let authorized = pending.authorize(creds); // `pending` is consumed here!
// pending.authorize(creds); // COMPILER ERROR: Use after move.
let settled = authorized.settle();
```

_Steps:_

1. Define structs: `Pending`, `Authorized`, `Settled`.
2. Define `Payment<State>`.
3. Implement methods _only_ on specific states (e.g., `impl Payment<Authorized> { fn settle(…) }`).

### 🗣️ The Feynman Test

> "Explain 'Ownership' to a C++ developer using the metaphor of a 'Physical Ticket' that must be handed over to enter a room."

---

## 5. Level 4: Systems Thinking (Equality & Identity)

**Theory:** Identity is tricky. Are two files equal if they have the same content? (Intensional vs. Extensional).
- **Reading:** [[SoT - The Structure of Identity (UIP and Groupoids)]]

### 🛠️ Practical Challenge 4: Content-Addressable Storage (Git-Lite)

**Scenario:** We need to store data efficiently. If two users save the same file, we should only store it once.
**Task:** Implement a simple **Merkle Tree** node.

_Required Output:_

1. Create a `Blob` struct.
2. Implement `fn hash(&self) -> String`.
3. Store blobs in a `HashMap<Hash, Blob>`.
4. **Goal:** Prove that if `Hash(A) == Hash(B)`, then `A` and `B` are effectively the same object, regardless of where they came from.

### 🗣️ The Feynman Test

> "Explain why Distributed Systems (like Git or Blockchain) use Hashes for ID instead of Auto-Incrementing Integers."

---

## 6. Resources for "Getting Unstuck"

If you cannot solve a challenge:

1. **Read:** _Parse, Don't Validate_ (Alexis King).
2. **Watch:** _Type-Driven API Design in Rust_ (Will Crichton).
3. **Reference:** [[SoT - Rust Language|Rust Design]]
