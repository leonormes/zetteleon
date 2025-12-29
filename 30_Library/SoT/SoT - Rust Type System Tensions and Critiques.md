---
aliases: ["The Price of Ignoring Theory", "Rust vs Linearity", "Rust ABI Critiques"]
confidence: "5/5"
created: 2025-12-29
epistemic: "critical"
last_reviewed: "2025-12-29"
modified: 2025-12-29
purpose: "To document the theoretical and engineering critiques of Rust's type system and architecture from a formal type theory perspective."
review_interval: "1 year"
see_also: ["[[SoT - Rust's Design Philosophy]]", "[[SoT - Rust Type System]]", "[[SoT - Dependent Types in Software]]"]
source_of_truth: []
status: "stable"
tags: ["rust", "critique", "type-theory", "linearity", "systems-programming"]
title: SoT - Rust Type System Tensions and Critiques
type: "SoT"
uid: 
updated: 
---

## 1. The Theoretical Debt

A critical perspective from formal type theory argues that Rust was developed "orthogonally to theory," leading to an "unbound and incomplete" type system that faces structural challenges as it evolves.

## 2. Core Critiques

### A. Borrowing vs. Linearity
- **The "Cop-out"**: Critics argue that Rust's ownership/borrowing model is a "separate pass" that generates constraints rather than a unified type-directed solution.
- **Linearity**: The principled alternative is **Linear Logic** (and graded modal types), which allows for precise quantification of resource usage (e.g., "this resource must be used exactly once").
- **The Adjunction**: Borrowing and Linearity form an adjunction; Rust focuses on the borrowing half but misses the linearity half that would enable more powerful resource management.

### B. Region-Based Aliasing (Oxide)
- **Oxide**: Cited as a more successful formalization of Rust using region-based aliasing. 
- **Decoupling**: Regions decouple data lifetimes from specific function call stacks, potentially allowing for more flexible stack usage without the rigidity of current Rust lifetimes.

### C. Type System Limitations
- **Second-Class GATs**: Generic Associated Types (GATs) are viewed as "second-class" compared to true higher-kinded types.
- **Dependent Types**: The lack of **Dependent Types** (as seen in Idris) prevents "correctness by construction" for things like guaranteed in-bounds array access, forcing Rust to rely on runtime panics.
- **Soundness Issues**: Long-standing issues (e.g., casting local lifetimes to `'static`) highlight where Rust's subtyping and function type tracking fail to be theoretically rigorous.

### D. Engineering & ABI
- **The ABI Mistake**: Rust is criticized for repeating "mistakes of C via LLVM" by failing to improve the Application Binary Interface (ABI). This forces small objects into memory rather than passing them in registers.
- **Static Linking**: The "culture of static linking" is seen as a security risk, delaying security patches and bloating binary sizes ("trashing the cache") by duplicating common functions like `printf` across all executables.

---

## 3. Alternative Models

- **Granule**: Uses **graded modal types** for fine-grained control over resource use counts.
- **Swift's Resilient Layout**: Praised for its stable ABI and witness tables, enabling better dynamic linking than Rust's monomorphization.

## 4. Minimum Viable Understanding (MVU)

1. **Rust as a "Stop-gap"**: From a theoretical view, Rust is a significant improvement over C++ but falls short of the rigor found in Haskell or OCaml.
2. **Equations over Fiddling**: Functional purists argue programming should be about **equations and transformations** rather than "manually fiddling with mutable registers."
3. **Backwards Compatibility**: Theoretical flaws are now difficult to fix due to the pressure to remain stable and compatible.

## 5. Sources and Links

- **Source:** James Faure, "Rust and the price of ignoring theory".
- **Related:** [[SoT - Dependent Types in Software]], [[SoT - Runtime Guards vs Compile-Time Proofs]].
