---
aliases: ["Data-Oriented Rust", "DOP in Rust", "Parse don't Validate"]
confidence: "5/5"
created: 2026-01-02T14:50:00Z
epistemic: "knowledge"
last_reviewed: "2026-01-02"
modified: 2026-01-08T10:49:44+00:00
purpose: "To define the application of Data-Oriented Programming (DOP) principles within the Rust type system and software architecture."
review_interval: "6 months"
see_also: ["[[SoT - Data-Centric Software Engineering]]", "[[SoT - Rust Language]]"]
source_of_truth: []
status: "stable"
tags: ["design-patterns", "dop", "rust", "SoftwareEngineering/Architecture"]
title: SoT - Data-Oriented Programming (DOP) in Rust
type: "SoT"
---

## 1. Core Philosophy: Hardware over Abstraction

Design software based on how the machine actually works (**Memory Layout**, **CPU Cache**, **SIMD**) rather than human-centric abstractions (Classes/Encapsulation).

- **Noun-Oriented:** Modelling "Objects" that _have_ state and behavior.
- **Verb-Oriented (DOP):** Modelling "Transformations" of data pipelines.

---

## 2. Fundamental Principles

### 2.1 Separation of Data and Logic

Data and behavior are strictly separated.

- **The Component:** Pure, "dumb" data. Transparent layout (public fields).
- **The System:** Stateless functions that transform data from one state to another.

### 2.2 Parse, Don't Validate

Instead of checking a boolean `isValid`, parse data into a type that **cannot exist** in an invalid state.

- **Mental Model:** The Type System is a gatekeeper. If the data exists as Type B, it _is_ valid by definition.
- **Transformation Pipeline:** `Bytes` -> `UntrustedPayload` -> `ValidatedCommand` -> `Response`.

### 2.3 The "Database" Mindset (State as Tables)

Treat application state as an in-memory relational database rather than a graph of objects.

- **Component:** A row in a table.
- **System:** A query/transformation that processes homogeneous chunks of rows.

---

## 3. Implementation Patterns in Rust

### 3.1 Newtypes for Safety

Use tuple structs to wrap primitive types, preventing accidental mixing of different domains (e.g., `Email(String)` vs `Username(String)`).

### 3.2 Enums for State Transitions

Use Enums to model the specific "shapes" data can take, ensuring all states are handled via pattern matching.

```rust
pub enum RemoteData<T> {
    NotAsked,
    Loading,
    Loaded(T),
    Error(String),
}
```

### 3.3 Public by Default (Transparency)

In DOP, structs often have public fields (`pub`) to allow systems to inspect and transform them directly, prioritizing transparency over encapsulation.

---

## 4. Performance: Machine Sympathy

- **Cache Locality:** Organizing data in contiguous blocks (`Vec<Struct>`) rather than lists of pointers (`Array<Object>`).
- **SIMD Alignment:** Immutable-by-default iterators in Rust reliably trigger auto-vectorization in the compiler.
