---
aliases: [Data-First Challenges, DOD Curriculum, DOP Learning Path, Protocol - Data-Oriented Design]
created: 2025-12-31T00:00:00+00:00
last_reviewed: '2026-01-01'
modified: 2026-07-04T10:51:02+00:00
permalink: llmeon/30-library/so-t/so-t-curriculum-data-oriented-design
status: active
tags: [curriculum, dop, exercises, learning-engine, practice]
title: SoT - Curriculum - Data-Oriented Design
type: SoT
updated: null
---

## SoT - Curriculum - Data-Oriented Design

> [!abstract] The Core Philosophy
> "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."—Linus Torvalds
>
> The Objective: Break the habit of "writing code to manage state" and replace it with "designing state that manages itself."

---

### 🗺️ The Map (Syllabus)

You are not here to read. You are here to build. Each stage requires you to defeat a specific "Boss" (Project) to prove your mastery.

Global Constraints:

1. No Tutorials: You may read documentation for syntax, but the logic must be yours.
2. Strict Types: All code must be statically typed (TypeScript/Rust/Go).
3. Data First: Define your data structures _before_ writing a single function.

---

### ⚔️ Stage 1: The State Enforcer

The Concept: Invariants & Impossible States.

The Trap: "Flag Soup" (e.g., `isLoading`, `isSuccess`, `isError` all true at once).

#### Mini-Boss: The "Smart" Traffic Light

- Context: A simple Red-Amber-Green system.
- The Trap: `class TrafficLight { isGreen: boolean; isRed: boolean; }`

#### 💀 Main Boss: The User Registration Flow

The Arena: Refactor a user account system that manages registration steps.

The Problem: Users currently exist in a quantum state of "Suspended" but "Unverified."

Victory Conditions:

- [ ] Create a `User` type where it is compilation-time impossible for a user to be `Suspended` if they have not yet `VerifiedEmail`.
- [ ] Define distinct types for `PendingUser`, `ActiveUser`, and `SuspendedUser`.
- [ ] Eliminate all `if (user.isValid)` runtime checks. The compiler must guarantee validity.

Loot (Resources):

- [[SoT - Data-Oriented Programming (DOP)#Algebraic Data Types]]
- _Search Term:_ "Parse, Don't Validate" (Alexis King).

---

### ⚔️ Stage 2: The Recursion Killer

The Concept: Flat Hierarchies & Indices.

The Trap: Recursive Classes (e.g., `class Comment { replies: Comment[] }`). Pointers are expensive; Indices are cheap.

#### Mini-Boss: The Reddit Thread

- Context: A comment section with infinite nesting depth.
- The Trap: Recursive rendering functions that crash the stack on deep threads.

#### 💀 Main Boss: The Flat File System

The Arena: Design a Virtual File System (Folders and Files) without recursion.

The Problem: You need to delete a folder and all 10,000 sub-items efficiently.

Victory Conditions:

- [ ] Constraint: You strictly cannot use a `Folder` class that contains a list/array of `Files`.
- [ ] Implement a `deleteFolder(id)` function that runs in $O(N)$ (or better) without a recursive helper function.
- [ ] Render the full file tree using a single flat loop.

Loot (Resources):

- _Search Term:_ "Adjacency List vs Closure Table"
- _Search Term:_ "Database Path Enumeration"

---

### ⚔️ Stage 3: The Sparse Entity

The Concept: Composition over Inheritance.

The Trap: "Inheritance Hell" (e.g., `class Book extends PhysicalProduct`). Paying for memory/fields you don't use.

#### Mini-Boss: The E-Commerce Catalog

- Context: Selling Books (ISBN), T-Shirts (Size), and Gift Cards (Virtual).
- The Trap: A base `Product` class that gets bloated with optional fields.

#### 💀 Main Boss: The ECS Character System

The Arena: An RPG engine with Warriors, Mages, and Ghosts.

- _Warrior:_ Health, Strength, Position.
- _Mage:_ Health, Mana, Position.
- _Ghost:_ Mana, Position (No Health, No Physical Body).

Victory Conditions:

- [ ] Create a data structure where "Taking Damage" can be applied to Warriors and Mages.
- [ ] Constraint: It must be impossible to call `takeDamage()` on a Ghost (compile-time error or structural impossibility).
- [ ] Constraint: Do not use `if (entity.hasHealth)` checks.
- [ ] Implement a "System" that updates the position of _all_ entities (Warrior, Mage, Ghost) in a single tight loop.

Loot (Resources):

- [[SoT - Entity Component System (ECS)]]
- _Search Term:_ "Data-Oriented Design Composition"

---

### ⚔️ Stage 4: The Time Traveller

The Concept: Event Sourcing & Immutability.

The Trap: The Mutable Snapshot (e.g., `account.balance += 50`). Information is destroyed on every write.

#### Mini-Boss: The Bank Ledger

- Context: A bank account that needs a transaction history.
- The Trap: Storing only `currentBalance`.

#### 💀 Main Boss: The Chess Replay Engine

The Arena: A chess game logic engine.

The Problem: Validating moves requires knowing the history (e.g., En Passant, Castling rights).

Victory Conditions:

- [ ] Constraint: You cannot store the "Board" (8x8 grid) as the primary source of truth.
- [ ] The game state must be derived entirely from an append-only list of moves (`e2 -> e4`).
- [ ] Implement an `undo()` function that simply drops the last event and re-projects the state.
- [ ] Implement a "Time Travel" slider to view the board state at Move 5.

Loot (Resources):

- _Search Term:_ "Event Sourcing vs Command Sourcing"
- _Search Term:_ "Redux Pattern"

---

### 👹 The Final Boss: The "Do It Yourself" Jira

The Project: Build a high-performance Task Management System.

The Architecture:

1. Users: (Stage 1 Strict States) - `Invited` vs `Active`.
2. Tasks: (Stage 2 Flat Hierarchy) - Infinite sub-task nesting.
3. Custom Fields: (Stage 3 Sparse Data) - Some tasks have "Due Dates," some have "Story Points."
4. Audit Trail: (Stage 4 History) - "Who moved this card?" is answered by default.

The Ultimate Constraint:

- You are BANNED from using Classes (`class`).
- You must use only: `Interfaces`, `Arrays`, `Maps`, and `Functions`.
- _Why?_ Stripping away the Object-Oriented shell forces you to see the naked data topology.

Victory Conditions:

- [ ] The entire application state must be serializable to a single JSON object.
- [ ] You can save/load the entire project state instantly.
- [ ] 100% Type Safety.

---

## 🧪 Project Track: Rust Implementation

> [!mission] Objective
> Shift from "Object-Oriented" thinking (encapsulation/identity) to "Data-Oriented" thinking (transformations/memory).
> Capstone: Build a high-performance Particle System Simulation using ECS (Entity Component System) principles that runs at 60fps.

### The Syllabus (The Map)

| Module | Concepts (Mental Models) | Facts (Syntax/Hardware) | Procedures (Unit Tests) |
|:--- |:--- |:--- |:--- |
| 1. The State Enforcer | Parse, Don't Validate. Making illegal states unrepresentable. | Rust `enum`, `match`, `Option`, `Result`. | Refactor a "Flag Soup" class into a strict State Machine (Traffic Light). |
| 2. The Memory Layout | Data Locality. The CPU hates jumping. Struct of Arrays (SoA) vs. Array of Structs (AoS). | Stack vs. Heap, CPU Cache Lines (L1/L2), `Vec` internals. | Benchmark iterating a `Vec<Box<T>>` vs `Vec<T>`. Measure the cache miss penalty. |
| 3. Composition over Inheritance | Decoupling Data. Entities are just IDs. Components are data buckets. | Traits, Generics, `usize` indexing. | Build a simple `World` struct that holds `Position` and `Velocity` vectors for 1000 entities. |
| 4. The Transform Pipeline | Systems as Functions. Logic processes homogeneous data streams. | Iterators (`.map`, `.filter`), Rayon (Parallelism). | Write a `PhysicsSystem` that updates positions based on velocity for all entities in parallel. |

### Unit Test: The Traffic Light (State Enforcer)

Goal: Prevent logical bugs at compile time.

Context: A Traffic Light system.

Constraint: It must be impossible to have `Red` and `Green` active simultaneously.

#### Requirements

1. Define a `TrafficLight` Enum.
2. Each variant (`Red`, `Amber`, `Green`) must hold its own distinct data (e.g., `timer: u32`).
3. Implement a function `next_state(current: TrafficLight) -> TrafficLight`.
4. The Hostile Compiler Test: Attempting to access `pedestrians_waiting` when the light is `Red` must be a compile error.
