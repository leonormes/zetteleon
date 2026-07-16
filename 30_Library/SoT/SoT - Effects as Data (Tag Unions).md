---
aliases: [Effect Systems, Roc Language Effects, Tag Unions]
created: 2025-12-19T09:29:36+00:00
modified: 2026-07-13T08:52:45+00:00
permalink: llmeon/30-library/so-t/so-t-effects-as-data-tag-unions
tags: [functional-programming, roc, SoftwareEngineering/Architecture, type-theory]
title: SoT - Effects as Data (Tag Unions)
type: sot
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## 0. The Lineage

This pattern is a Functional Implementation of the Data-Centric Philosophy.

- The Axiom: [[SoT - Data-Centric Software Engineering]]—_Code should process data, not perform side effects directly._
- The Theory: [[MOC - Type Theory]]—_Sum Types (Unions) can represent the "Shape" of an Effect._

---

## 1. Definitive Statement

> Effects as Data is the architectural pattern of treating side effects (I/O) not as _actions_ to be executed immediately, but as _values_ (Data Structures) to be returned and interpreted.
>
> By representing an operation (e.g., "Read File") as a Tag Union (Sum Type), we decouple the Description of the work from the Execution of the work.

---

## 2. The Architectural Problem: Precision vs. Ergonomics

In statically typed languages (like Rust), chaining operations with different error types is painful.

- Constraint: `HTTP` returns `HttpError`. `File` returns `FileError`. They cannot be returned from the same function without a wrapper (Box or Enum).
- Friction: This leads to "Error Wrapping Fatigue" or generic `AnyError` types that lose precision.

---

## 3. The Solution: Accumulating Anonymous Unions

Using Structural Tag Unions (as seen in the Roc language):

1. Type Inference: The compiler infers the return type as the _union_ of all possible tags returned (e.g., `[Red, Green, Blue]`).
2. Automatic Composition: A function performing HTTP and File I/O simply returns `[HttpError, FileError]`. No manual wrapper is needed.
3. Exhaustiveness: The caller _must_ handle both cases, but the "wrapping" is done by the compiler.

---

## 4. Runtime Architecture: The State Machine

Under the hood, an Effect is a State Machine.

- Structure: An `Operation` variant contains:
    - Payload: Data needed (e.g., URL).
    - Continuation: A closure (`Result -> NextOperation`) defining the next step.
- Interpreter: A "Runtime" loops over these values. It sees `Read(Path, Next)`, performs the read, and calls `Next(Result)`.

---

## 5. Operational Benefits

1. Simulation Testing: You can test the _logic_ of your effects without doing I/O. Your test runner just inspects the `Operation` tree (`assert(op == Read("file.txt"))`).
2. Observability: The central runtime can log every effect before executing it.
3. Zero-Cost: These unions can be compiled down to efficient C-style tagged unions on the stack.
