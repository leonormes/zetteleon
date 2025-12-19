---
aliases: [Effects as Data, Simple Functional Effects, Tag Unions for Effects]
confidence: 5/5
created: 2025-12-19T10:30:00Z
epistemic: authoritative
last_reviewed: 2025-12-19
modified: 2025-12-19T10:12:36Z
purpose: To define the architectural pattern of functional effects as data, specifically using Tag Unions (anonymous sum types) to decouple description from execution.
quality-markers: [Synthesized from Richard Feldman's 'Simple Functional Effects with Tag Unions']
related-soTs: ["[[SoT - The Algebra of Types (Cardinality and Isomorphism)]]", "[[SoT - TypeScript as a Proof Engine (Set Theory and Distributivity)]]"]
resonance-score: 8
review_interval: 1 year
see_also: []
source_of_truth: true
status: stable
tags: [architecture, functional_programming, roc, type_theory]
title: SoT - Functional Effects (Effects as Data)
type: SoT
uid:
updated:
---

## 1. Definitive Statement

> [!definition] Definition
> **Effects as Data** is an architectural pattern that decouples the *description* of a side effect from its *execution*. By representing operations as **Tag Unions** (anonymous sum types), the system transforms opaque execution steps into transparent, accumulating data sets that the compiler can reason about.

## 2. Core Concepts: The Tag Union Model

The standard "Execution-First" model fails when errors diverge (e.g., mixing `HttpError` and `FileError` in Rust without manual wrappers).

### A. Anonymous Tag Unions

In the Roc language model, **Tag Unions** are structural and anonymous.

- **Structural Identity:** Defined by content, not declaration.
- **Accumulation:** Chaining multiple effects results in a union of all possible tags (e.g., `[HttpError, FileReadError, FileWriteError]`).
- **Composition:** Chaining is "zero-toil"—the compiler automatically infers the set of all possible failures, maintaining exhaustive handling without requiring manual error hierarchies.

### B. The Task as a State Machine

Under the hood, a `Task` abstraction compiles into an `Operation` tag union.

- **The Variant:** Contains the command payload (e.g., `GetBytes { url: String }`).
- **The Continuation:** A closure (`Result -> NextOperation`) that determines the transition to the next state.
- **The Loop:** A runtime interpreter unwraps the `Operation`, performs the I/O, and passes the result to the continuation.

## 3. Operational Benefits

### A. Simulation Testing (The "Memory Runner")

Because the effect chain is a data structure, tests can traverse the `Operation` tree without executing real I/O.

- **Mechanism:** A test runner inspects the intent (e.g., "Client requested URL X") and injects a mock response in-memory.
- **Result:** Removes the dependency on local servers or complex mocking frameworks.

### B. Centralised Observability

The interpreter traversing the state machine provides a single point of enforcement for logging and telemetry. Every effect variant is observed and recorded by the runtime before execution.

## 4. Performance: Zero-Cost Abstractions
- **Monomorphisation:** Tag Unions are compiled into efficient C-style structs/unions.
- **Stack Allocation:** Closures and unions are stack-allocated, avoiding heap overhead and garbage collection pressure.
- **Efficiency:** Comparable to Rust's async state machines but with higher ergonomic safety for error composition.

## 5. Minimum Viable Understanding (MVU)
- **Effect = Description (Data).**
- **Error = Structural Union (Automatic Composition).**
- **Runtime = Interpreter (State Machine).**
- **Test = Data Traversal (Zero I/O).**

## 6. Sources and Links
- **Source:** Richard Feldman, *Simple Functional Effects with Tag Unions* (YouTube/Roc-lang).
- **Related:** [[SoT - The Algebra of Types (Cardinality and Isomorphism)]] (Sums and Products).
