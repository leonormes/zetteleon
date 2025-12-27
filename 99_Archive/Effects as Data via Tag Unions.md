---
aliases: []
confidence: 
created: 2025-12-19T09:29:36Z
epistemic: 
last_reviewed: 
modified: 2025-12-27T20:40:55+00:00
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Effects as Data via Tag Unions
type: 
uid: 
updated: 
---

I have processed the video "Simple Functional Effects with Tag Unions" by Richard Feldman. Based on your cognitive style, here is a high-level architectural analysis of the proposed effect system, focusing on the underlying mental models and structural logic.

## **Core Mental Model: Effects as Data via Tag Unions**

The system decouples the *description* of a side effect from its *execution* by representing operations as **Tag Unions** (anonymous sum types). This allows the compiler to treat effects and errors as accumulating data sets rather than opaque execution steps.

## **1. The Architectural Problem: Precision vs. Ergonomics**

In statically typed languages (like Rust), short-circuiting error handling (e.g., the `?` operator) requires a consistent return type.

- **The Constraint:** Chaining an HTTP operation (returning `HttpError`) with a File operation (returning `FileError`) fails type checking because the error types diverge `[00:09:52]`.
- **Traditional Workarounds:** Developers often resort to "over-broad" error types (e.g., a generic `IOError`) or manual wrapper types, sacrificing type precision for ergonomic control flow.

## **2. The Solution: Accumulating Anonymous Unions**

Rock's **Tag Unions** are structural and anonymous, meaning they are defined by their content rather than a declaration.

- **Type Inference:** When conditional branches return different tags, the compiler infers the return type as the *union* of those tags (e.g., `[Red, Green, Blue]`) `[00:17:15]`.
- **Automatic Error Composition:** A function performing multiple distinct effects simply returns the union of all possible errors (e.g., `[HttpError, FileWriteError, FileReadError]`). The compiler tracks the exact set of possible failures automatically, eliminating the need for manual wrappers while maintaining exhaustive handling requirements `[00:24:21]`.

## **3. Runtime Architecture: The State Machine**

Under the hood, the `Task` abstraction compiles down to an `Operation` tag union, functioning as a state machine.

- **Structure:** An `Operation` variant contains the command payload (e.g., `GetBytes` with a URL) and a **continuation closure** (`Result -> NextOperation`) that dictates the transition to the next state `[00:28:42]`.
- **Execution Loop:** The runtime unwraps the `Operation`, performs the side effect (e.g., network request), and passes the result to the continuation to generate the next step.

## **4. Operational Benefits**

- **Simulation Testing:** Since the effect chain is merely a data structure, tests can traverse the `Operation` tree without executing real I/O. A test runner can inspect the intent (e.g., "Client requested URL X") and inject a mock response purely in memory, removing the need for local servers or mocks `[00:31:53]`.
- **Centralised Observability:** The interpreter traversing the state machine can enforce centralised logging for every effect variant, ensuring no I/O operation occurs unobserved `[00:33:10]`.

## **5. Performance Characteristics**

- **Zero-Cost Abstraction:** Tag Unions are monomorphised into C-style structs/unions.
- **Stack Allocation:** The system stack-allocates closures and unions, avoiding heap overhead. The resulting runtime performance is comparable to Rust's async state machines `[00:38:40]`.
