---
aliases: [Complexity Budget, Law of Conservation of Complexity, Tesler's Law]
created: 2026-01-31T00:00:00+00:00
last_reviewed: 
modified: 2026-02-02T09:58:00+00:00
status: evergreen
tags: [architecture, complexity, mental-model, system-design]
title: SoT - Conservation of Complexity
type: SoT
updated: 
synthesis-count: 3
last-synthesis: 2026-02-02
---

## Minimum Viable Understanding (MVU)

> Software complexity is conserved: it must reside either in Bucket A (Code/Time) or Bucket B (Data/Space).

Tesler's Law dictates the *amount* of complexity is fixed by the domain. The architect's job is not to destroy it, but to shift it from Procedural Logic (fragile, hard to reason about) into Structural Representation (robust, inspectable).

## 1. The Core Dialectic: Bucket A vs Bucket B

Linus Torvalds: _"Bad programmers worry about the code. Good programmers worry about data structures and their relationships."_

We conceptualize the system as two containers for the "Mass" of complexity:

| Feature | Bucket A (Code) | Bucket B (Data) |
|:---|:---|:---|
| Form | Verbs (Algorithms, Control Flow) | Nouns (Schema, Tables, Graphs) |
| Nature | Dynamic / Temporal | Static / Spatial |
| Cognitive Load | High (Must simulate CPU state) | Low (Visual/Topological) |
| Constraint | Implicit (hidden in `if` logic) | Explicit (Types, FKs, Enums) |
| Torvalds' Axiom | "Bad" (Fragile, difficult to test) | "Good" (Robust, self-evident) |

The Strategy: Deliberately migrate complexity from A to B. "Fold knowledge into data so program logic can be stupid and robust" (Rob Pike).

## 2. Mechanisms of Shift

How do we actually move complexity?

### A. Table-Driven Methods
Instead of `if (age < 20) return 5.0; else if...`, use a lookup table.
*   Result: Logic becomes generic (`table.get(age)`). New rules require data entry, not code deployment.

### B. Finite State Machines (FSM)
Instead of "Boolean Salad" (`isLoading && !hasError`), use a Graph.
*   Result: Invalid states become unrepresentable fundamental constraints of the data structure.

### C. Data-Oriented Design (DoD)
Instead of Objects (AoS), use Arrays (SoA).
*   Result: Performance becomes a property of the data layout (cache locality), not the cleverness of the loop.

## 3. Case Studies in Allocation

### A. The Linux Kernel (VFS)
*   Problem: Support 50+ filesystems (EXT4, NTFS, BTRFS) without a massive `switch` statement.
*   Solution (Bucket B): The `file_operations` struct. The VFS defines the *shape* of a filesystem.
*   Outcome: The kernel code is generic (`file->op->read()`). Complexity is encapsulated in the data structure instances of the drivers.

### B. Enterprise Tax Engines
*   Problem: Tax laws change daily and vary by street address.
*   Approach A (Code): `if (zip == 10001) ...`. Result: Maintenance nightmare.
*   Approach B (Data): A Rules Engine (Database). Code is just `SELECT rate FROM Rules`. Result: Auditable, updateable by non-programmers.

## 4. Pathologies (When It Goes Wrong)

Shifting too much complexity to Data can backfire.

### A. The Inner-Platform Effect
Creating a data structure so complex it becomes a programming language (e.g., XML rules with logical operators).
*   *Verdict*: Moving code into a container (Database/Config) that lacks a compiler is worse than just writing code.

### B. The Anemic Domain Model
Stripping all logic from objects until they are just bags of data, leaving the logic in "Services" that have no state.
*   *Verdict*: Valid in functional/DoD contexts, but in OOP, it decouples the data from its invariants, allowing invalid states.

## 5. Dimensions of Complexity (Theory)

*   Kolmogorov Complexity: The irreducible "floor" of the problem (e.g., US Tax Code).
*   Cyclomatic Complexity: The measure of "messiness" in Bucket A.
*   Semantic Density: The ambiguity of the vocabulary.

See Also: [[SoT - Data-Oriented Design]], [[SoT - Infrastructure Complexity Management]]
