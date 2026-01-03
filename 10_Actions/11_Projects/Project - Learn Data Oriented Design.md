---
aliases: []
title: "Project: Master Data-Oriented Design (Rust)"
type: project
confidence: ""
epistemic: ""
purpose: ""
modified: 2026-01-03T10:19:45+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
created: 2026-01-02T09:33:27+00:00
tags:
  - project
  - learning
  - rust
  - architecture
  - active
status: Active
priority: High
bridge_note: "Ready to start. First Mission: The Traffic Light State Enforcer."
---

# Project: Master Data-Oriented Design (Rust)

> [!mission] Objective
> Shift from "Object-Oriented" thinking (encapsulation/identity) to "Data-Oriented" thinking (transformations/memory).
> **Capstone:** Build a high-performance **Particle System Simulation** using ECS (Entity Component System) principles that runs at 60fps.

---

## 1. The Syllabus (The Map)

| Module | Concepts (Mental Models) | Facts (Syntax/Hardware) | Procedures (Unit Tests) |
|:--- |:--- |:--- |:--- |
| **1. The State Enforcer** | **Parse, Don't Validate.** Making illegal states unrepresentable. | Rust `enum`, `match`, `Option`, `Result`. | Refactor a "Flag Soup" class into a strict State Machine (Traffic Light). |
| **2. The Memory Layout** | **Data Locality.** The CPU hates jumping. Struct of Arrays (SoA) vs. Array of Structs (AoS). | Stack vs. Heap, CPU Cache Lines (L1/L2), `Vec` internals. | Benchmark iterating a `Vec<Box<T>>` vs `Vec<T>`. Measure the cache miss penalty. |
| **3. Composition over Inheritance** | **Decoupling Data.** Entities are just IDs. Components are data buckets. | Traits, Generics, `usize` indexing. | Build a simple `World` struct that holds `Position` and `Velocity` vectors for 1000 entities. |
| **4. The Transform Pipeline** | **Systems as Functions.** Logic processes homogeneous data streams. | Iterators (`.map`, `.filter`), Rayon (Parallelism). | Write a `PhysicsSystem` that updates positions based on velocity for all entities in parallel. |

---

## 2. First Unit Test: The Traffic Light (State Enforcer)

**Goal:** Prevent logical bugs at compile time.
**Context:** A Traffic Light system.
**Constraint:** It must be impossible to have `Red` and `Green` active simultaneously.

### Requirements:

1. Define a `TrafficLight` Enum.
2. Each variant (`Red`, `Amber`, `Green`) must hold its own distinct data (e.g., `timer: u32`).
3. Implement a function `next_state(current: TrafficLight) -> TrafficLight`.
4. **The Hostile Compiler Test:** Attempting to access `pedestrians_waiting` when the light is `Red` must be a compile error.

---

## 3. Resources (Reference Only)

* *Read only when the Unit Test fails.*
* [Article] "Parse, Don't Validate" by Alexis King.
* [Book] "Data-Oriented Design" by Richard Fabian.
* [Docs] Rust `enum` and Pattern Matching documentation.

---

## 4. Bridge Note (Cryosleep)

* **Current State:** Project Initialized. Syllabus defined.
* **Next Physical Action:** Open IDE. Create `traffic_light.rs`. Define the `TrafficLight` enum.
* **Hook:** If I get this right, I never have to write `if (is_valid)` ever again.
