---
aliases: ["DOD Curriculum", "DOP Learning Path", "Data-First Challenges", "Protocol - Data-Oriented Design"]
confidence: "5/5"
created: 2025-12-31T00:00:00Z
epistemic: "curriculum"
last_reviewed: "2026-01-01"
modified: 2026-01-01T20:06:54+00:00
purpose: "A 'Boss Fight' structured curriculum to transition from Code-First to Data-First thinking."
review_interval: "3 months"
see_also: ["[[SoT - Data-Oriented Programming (DOP)]]", "[[SoT - Data-Centric Software Engineering]]", "[[SoT - Slot Map (Generational Arena)]]", "[[SoT - Protocol - Learning Engine]]"]
source_of_truth: []
status: "active"
tags: ["curriculum", "dop", "practice", "exercises", "learning-engine"]
title: SoT - Curriculum - Data-Oriented Design
type: "SoT"
uid: 
updated: 
---

# SoT - Curriculum - Data-Oriented Design

> [!abstract] The Core Philosophy
> "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."—**Linus Torvalds**
>
> **The Objective:** Break the habit of "writing code to manage state" and replace it with "designing state that manages itself."

---

## 🗺️ The Map (Syllabus)

You are not here to read. You are here to build. Each stage requires you to defeat a specific "Boss" (Project) to prove your mastery.

**Global Constraints:**
1. **No Tutorials:** You may read documentation for syntax, but the logic must be yours.
2. **Strict Types:** All code must be statically typed (TypeScript/Rust/Go).
3. **Data First:** Define your data structures *before* writing a single function.

---

## ⚔️ Stage 1: The State Enforcer

**The Concept:** Invariants & Impossible States.
**The Trap:** "Flag Soup" (e.g., `isLoading`, `isSuccess`, `isError` all true at once).

### Mini-Boss: The "Smart" Traffic Light

* **Context:** A simple Red-Amber-Green system.
* **The Trap:** `class TrafficLight { isGreen: boolean; isRed: boolean; }`

### 💀 Main Boss: The User Registration Flow

**The Arena:** Refactor a user account system that manages registration steps.
**The Problem:** Users currently exist in a quantum state of "Suspended" but "Unverified."

**Victory Conditions:**
- [ ] Create a `User` type where it is **compilation-time impossible** for a user to be `Suspended` if they have not yet `VerifiedEmail`.
- [ ] Define distinct types for `PendingUser`, `ActiveUser`, and `SuspendedUser`.
- [ ] Eliminate all `if (user.isValid)` runtime checks. The compiler must guarantee validity.

**Loot (Resources):**
* [[SoT - Data-Oriented Programming (DOP)#Algebraic Data Types]]
* *Search Term:* "Parse, Don't Validate" (Alexis King).

---

## ⚔️ Stage 2: The Recursion Killer

**The Concept:** Flat Hierarchies & Indices.
**The Trap:** Recursive Classes (e.g., `class Comment { replies: Comment[] }`). Pointers are expensive; Indices are cheap.

### Mini-Boss: The Reddit Thread

* **Context:** A comment section with infinite nesting depth.
* **The Trap:** Recursive rendering functions that crash the stack on deep threads.

### 💀 Main Boss: The Flat File System

**The Arena:** Design a Virtual File System (Folders and Files) without recursion.
**The Problem:** You need to delete a folder and all 10,000 sub-items efficiently.

**Victory Conditions:**
- [ ] **Constraint:** You strictly cannot use a `Folder` class that contains a list/array of `Files`.
- [ ] Implement a `deleteFolder(id)` function that runs in $O(N)$ (or better) without a recursive helper function.
- [ ] Render the full file tree using a single flat loop.

**Loot (Resources):**
* *Search Term:* "Adjacency List vs Closure Table"
* *Search Term:* "Database Path Enumeration"

---

## ⚔️ Stage 3: The Sparse Entity

**The Concept:** Composition over Inheritance.
**The Trap:** "Inheritance Hell" (e.g., `class Book extends PhysicalProduct`). Paying for memory/fields you don't use.

### Mini-Boss: The E-Commerce Catalog

* **Context:** Selling Books (ISBN), T-Shirts (Size), and Gift Cards (Virtual).
* **The Trap:** A base `Product` class that gets bloated with optional fields.

### 💀 Main Boss: The ECS Character System

**The Arena:** An RPG engine with Warriors, Mages, and Ghosts.
* *Warrior:* Health, Strength, Position.
* *Mage:* Health, Mana, Position.
* *Ghost:* Mana, Position (No Health, No Physical Body).

**Victory Conditions:**
- [ ] Create a data structure where "Taking Damage" can be applied to Warriors and Mages.
- [ ] **Constraint:** It must be impossible to call `takeDamage()` on a Ghost (compile-time error or structural impossibility).
- [ ] **Constraint:** Do not use `if (entity.hasHealth)` checks.
- [ ] Implement a "System" that updates the position of *all* entities (Warrior, Mage, Ghost) in a single tight loop.

**Loot (Resources):**
* [[SoT - Entity Component System (ECS)]]
* *Search Term:* "Data-Oriented Design Composition"

---

## ⚔️ Stage 4: The Time Traveller

**The Concept:** Event Sourcing & Immutability.
**The Trap:** The Mutable Snapshot (e.g., `account.balance += 50`). Information is destroyed on every write.

### Mini-Boss: The Bank Ledger

* **Context:** A bank account that needs a transaction history.
* **The Trap:** Storing only `currentBalance`.

### 💀 Main Boss: The Chess Replay Engine

**The Arena:** A chess game logic engine.
**The Problem:** Validating moves requires knowing the history (e.g., En Passant, Castling rights).

**Victory Conditions:**
- [ ] **Constraint:** You cannot store the "Board" (8x8 grid) as the primary source of truth.
- [ ] The game state must be derived entirely from an append-only list of moves (`e2 -> e4`).
- [ ] Implement an `undo()` function that simply drops the last event and re-projects the state.
- [ ] Implement a "Time Travel" slider to view the board state at Move 5.

**Loot (Resources):**
* *Search Term:* "Event Sourcing vs Command Sourcing"
* *Search Term:* "Redux Pattern"

---

## 👹 The Final Boss: The "Do It Yourself" Jira

**The Project:** Build a high-performance Task Management System.

**The Architecture:**
1. **Users:** (Stage 1 Strict States) - `Invited` vs `Active`.
2. **Tasks:** (Stage 2 Flat Hierarchy) - Infinite sub-task nesting.
3. **Custom Fields:** (Stage 3 Sparse Data) - Some tasks have "Due Dates," some have "Story Points."
4. **Audit Trail:** (Stage 4 History) - "Who moved this card?" is answered by default.

**The Ultimate Constraint:**
* You are **BANNED** from using Classes (`class`).
* You must use only: `Interfaces`, `Arrays`, `Maps`, and `Functions`.
* *Why?* Stripping away the Object-Oriented shell forces you to see the naked data topology.

**Victory Conditions:**
- [ ] The entire application state must be serializable to a single JSON object.
- [ ] You can save/load the entire project state instantly.
- [ ] 100% Type Safety.
