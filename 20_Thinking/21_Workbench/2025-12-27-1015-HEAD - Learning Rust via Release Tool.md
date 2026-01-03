---
title: HEAD - Learning Rust via Release Tool
type: head
confidence: ""
epistemic: ""
purpose: ""
modified: 2025-12-27T18:19:23+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
aliases:
  - Rust Learning Project
  - Release Tool Curriculum
tags:
  - project
  - learning
  - rust
  - head
created: 2025-12-27T14:11:28+00:00
status: active
---

# HEAD - Learning Rust via Release Tool

## 1. The Spark

> "I want to learn Rust. I have a simple tool for making releases via git tags... I need a curriculum."

**Context:** The user understands Type Theory (Sum/Product types, Morphisms). We will use this existing mental model as the "Hook" for the **Compress** phase of the [[SoT - Accelerated Learning (3C Protocol)|3C Protocol]].

**The Goal:** Build the `release-tool` from scratch, using it to master Rust's specific "borrow checker" constraints and "systems" focus.

## 2. The Model: "Type-Driven Systems Programming"

We will avoid standard "Hello World" tutorials. Instead, we map the **Release Tool Wiki** directly to Rust concepts.

| Module | Release Tool Feature | Rust Concept | Theory Hook |
|:--- |:--- |:--- |:--- |
| **1. Domain** | `Ticket`, `SemanticVersion`, `IncrementStrategy` | Structs, Enums, `derive`, Newtypes | Algebraic Data Types (Product/Sum) |
| **2. Logic** | `determine_strategy`, `bump_version` | Pattern Matching, `Option`, `Result`, Unit Testing | Total Functions, Exhaustiveness |
| **3. Boundary** | Parsing Git Logs, Shell Commands | `std::process`, `std::fs`, `TryFrom`, `thiserror` | "Dirty World" vs "Pure Domain" |
| **4. App** | CLI Args, TUI Dashboard | `clap`, `ratatui`, Lifetimes in Structs | The Elm Architecture (Model/View/Update) |

---

## 3. The Curriculum (The "Compile" Phase)

### Module 1: The Domain Layer (Defining the Universe)

**Objective:** Define the "Nouns" so invalid states are unrepresentable.

1. **Setup:** `cargo new release-tool --lib`
2. **Task A (Product Types):** Implement `SemanticVersion` as a `struct`. Implement `Display` and `Ord` traits.
3. **Task B (Sum Types):** Implement `IncrementStrategy` as an `enum`. Use the variant `Custom(SemanticVersion)` to practice holding data in enums.
4. **Task C (Newtypes):** Implement `Ticket(String)` and ensure it validates the format `FFAPP-\d+` upon creation (Private constructor, public `parse` method).

**The Next Test:**
- [ ] `cargo test` confirms `SemanticVersion(1,0,0) < SemanticVersion(2,0,0)`.
- [ ] `cargo test` confirms `Ticket::parse("invalid")` returns `Err`.

### Module 2: The Logic Layer (The Morphisms)

**Objective:** Write pure functions that transform data.

1. **Task A (Pattern Matching):** Implement `fn bump(current: &SemanticVersion, strategy: &IncrementStrategy) -> SemanticVersion`.
    * *Constraint:* Must use `match`. Handle the `Custom(v)` variant to extract data.
2. **Task B (Option/Result):** Implement `fn parse_commit(msg: &str) -> Option<ConventionalCommit>`.
    * *Constraint:* Use `Option` to handle non-compliant commits without panicking.
3. **Task C (Unit Tests):** Write tests in the same file (`mod tests`) to verify logic.

**The Next Test:**
- [ ] Function correctly bumps `1.0.0` + `Minor` -> `1.1.0`.
- [ ] Function correctly extracts version from `Custom` strategy.

### Module 3: The Boundary Layer (Talking to the World)

**Objective:** Interface with the "Dirty" OS (Git) and convert to "Clean" Domain types.

1. **Task A (Command Execution):** Use `std::process::Command` to run `git log -n 10`.
2. **Task B (Error Handling):** Create a custom `ReleaseError` enum (using `thiserror`). Map `io::Error` to `ReleaseError::GitFailure`.
3. **Task C (Parsing Traits):** Implement `impl TryFrom<&str> for Commit` to parse raw git output.

**The Next Test:**
- [ ] Run `git log` from Rust and print a struct field to stdout.

### Module 4: The Application Layer (The Interface)

**Objective:** Assemble the parts into a binary.

1. **Task A (CLI):** Use `clap` to parse arguments: `release-tool --dry-run --force`.
2. **Task B (Ownership Integration):** Pass the `RuntimeMode` (Enum) down to the logic layer.
3. **Task C (TUI - Optional):** Use `ratatui` to show a list of commits and the calculated "Next Version".

---

## 4. Tensions & Risks

* **Borrow Checker Wall:** In Module 3, parsing strings from Git output will trigger lifetime issues (`&str` vs `String`).
    * *Mitigation:* Start by owning everything (`String`). Refactor to `&str` (references) only in Week 2.
* **Over-Engineering:** The temptation to make the "perfect" Type System (e.g., specific types for `MajorVersion`, `MinorVersion`) will slow progress.
    * *Mitigation:* Stick to the Wiki's types.

## 5. Resources

- [[SoT - Rust's Design Philosophy]]
- [[SoT - Rust's Ownership Model]]
- [[MOC - Rust Programming Language]]
- External: [The Rust Book](https://doc.rust-lang.org/book/)
- External: [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
