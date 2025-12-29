---
alias: ["Formality Core", "Executable Type Systems", "Rust Formal Modeling"]
confidence: "5/5"
created: 2025-12-29
epistemic: "technical"
last_reviewed: "2025-12-29"
modified: 2025-12-29
purpose: "To document Formality Core, a lightweight framework for modeling and experimenting with type systems, designed to make Rust's type checker executable and understandable."
review_interval: "1 year"
see_also: ["[[SoT - Rust Type System]]", "[[SoT - The Curry-Howard Correspondence (Propositions as Types)]]"]
source_of_truth: []
status: "stable"
tags: ["rust", "type-theory", "formal-methods", "modeling"]
title: SoT - Rust Type System Modeling (Formality Core)
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Formality Core
> A lightweight, executable framework built in Rust for modeling type systems. It prioritizes **concept density** and logic over performance, serving as a bridge between academic type theory and compiler engineering.

## 2. Core Framework Mechanisms

Formality Core allows engineers to define a language and its type-checking rules in a way that is both human-readable and machine-executable.

- **Grammar Definition**: Uses standard Rust structs and enums with a `#[term]` macro to automatically generate parsers and debug implementations.
- **Judgment Functions**: Type-checking rules are implemented as Rust functions that can represent non-deterministic logic (e.g., searching for a valid proof among multiple possible rules).
- **Mathematical Notation**: Leverages the "Turnstile" notation ($\vdash$) within Rust macros to mirror formal logic papers (e.g., "In environment $\Gamma$, expression $e$ has type $\tau$").

## 3. Strategic Objectives

The framework serves three primary purposes in the Rust ecosystem:

1.  **Context Restoration**: As Rust's type system (Trait Solver, Borrow Checker) grows in complexity, Formality Core provides a way to maintain a high-level "executable mental model" for contributors.
2.  **RFC Verification**: The long-term goal is to model new Rust features in Formality Core during the RFC process, allowing the community to test for soundness and edge cases before stabilization.
3.  **Fuzzing & Soundness**: By generating random programs and executing them against both the Formality Core model and the actual `rustc` compiler, developers can find discrepancies and proof of unsoundness.

## 4. Engineering Workflow

- **Expect Tests**: Integrates with `rust-analyzer` to allow rapid iteration on type rules. Developers write a test, see the failure, and "accept" the new output, updating the specification automatically.
- **Accessible Theory**: By allowing engineers to use the notation of academic papers but execute it in a familiar language (Rust), it lowers the barrier to entry for formal verification.

---

## 5. Minimum Viable Understanding (MVU)

1.  **Formality Core is an Executable Specification**: It defines *how* the type checker should behave in pure logic.
2.  **Bridge to Practice**: It turns abstract logic (judgment rules) into runnable Rust code.
3.  **Future of Rust Design**: It aims to be the sandbox for testing new language features for soundness.

## 6. Sources and Links

- **Source:** Niko Matsakis, "Type Theory for Busy Engineers" (RustNL 2024).
- **Repo:** [github.com/rust-lang/formality](https://github.com/rust-lang/formality)
