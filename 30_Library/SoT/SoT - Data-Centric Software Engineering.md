---
aliases: []
confidence: 5/5
created: 2025-12-22T00:00:00Z
epistemic: architecture
last_reviewed: 2025-12-22
modified: 2025-12-27T20:40:58+00:00
purpose: ">-"
review_interval: 6 months
see_also: []
source_of_truth: []
status: stable
tags: [data-centric, dod, systems-programming, go]
title: SoT - Data-Centric Software Engineering
type: SoT
uid:
updated:
---

## 1. Definitive Statement

> [!definition] The Core Philosophy
> "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."—**Linus Torvalds**
>
> **Data-Centric Software Engineering** is the discipline of treating **Data Structures** as the primary source of truth and complexity in a system, rendering the **Code** (Logic) as a trivial derivation of that structure.

### The Conservation Law of Complexity

Software complexity obeys a conservation law: it must reside either in the procedural logic (the Code) or the structural representation (the Data).

* **Code-Centric:** Complexity is handled by imperative logic (nested `if`, flags, loops). Result: Fragile, hard to test.
* **Data-Centric:** Complexity is encoded in the schema (Graph, Map, Table). Result: "Dumb" code that merely traverses the "Smart" structure.

---

## 2. The Structural Logic (10 Pillars)

Software quality is a direct function of its underlying structural logic. If the foundation is flawed, the algorithms built atop it will inevitably fail.

| Pillar | Principle | The Data-Centric View |
|:--- |:--- |:--- |
| **1. Foundational Integrity** | *Structure is Bedrock* | A robust data structure is the foundation. If flawed, the entire system is compromised. |
| **2. Epistemology** | *The Problem Lens* | The choice of structure defines *how* you view the problem. The right choice turns complex tasks into simple operations. |
| **3. Efficiency** | *Emergent Property* | Performance is not an added feature; it is an emergent property of the correct memory layout. |
| **4. Systemic Influence** | *Upstream Design* | Solving problems at the data layer simplifies downstream architecture, preventing technical debt. |
| **5. Algorithmic Symbiosis** | *Data Limits Logic* | Algorithms are functionally dependent on data. A superior algorithm cannot fix a poor structure. |
| **6. Scalability** | *Graceful Failure* | Handling load is not about "more servers"; it is about how data is organized and accessed under pressure. |
| **7. Cognitive Load** | *Legibility* | Clear data organization makes code obvious to other humans, reducing onboarding time. |
| **8. Debugging** | *State Tracing* | Bugs live in state transitions. Organized data makes these transitions trivial to trace. |
| **9. Performance** | *Optimization* | Optimization is fundamentally an exercise in data structure refinement (memory footprint, cache locality). |
| **10. Flexibility** | *Adaptability* | Robust structures allow business pivots with minimal friction; brittle structures require rewrites. |

---

## 3. The Hardware Reality: Data-Oriented Design (DOD)

Data-centricity is not just logical elegance; it is a physical requirement of modern hardware.

### The Lie of Object-Oriented Programming (OOP)

OOP organizes data as an **Array of Structures (AoS)** (e.g., `[Ball(x,y,c), Ball(x,y,c)]`). This causes **Cache Pollution**: loading a `Ball` to update its position `x` also loads irrelevant data like color `c` into the CPU cache line.

### The Solution: Structure of Arrays (SoA)

DOD organizes data as contiguous arrays of single attributes (e.g., `[x,x,x]`, `[y,y,y]`).

* **Cache Locality:** The CPU loads only relevant data.
* **SIMD:** The CPU can process multiple data points in a single clock cycle.
* **Result:** Orders of magnitude performance improvement (e.g., 10x more entities in game engines).

---

## 4. Algorithmic Simplification

### Table-Driven Methods

The "Code-Centric" developer writes a "Giant Switch Statement" to handle state. The "Data-Centric" developer uses a **Lookup Table**.

* **Code:** `if cmd == "SAVE": save()`
* **Data:** `commands = {"SAVE": save_fn}`. Logic becomes `commands[input]()`.
* **Benefit:** Cyclomatic complexity drops to 1. New commands are added to data, not code.

---

## 5. Applied Domains (The Pattern in Practice)

The Data-Centric philosophy is not limited to code; it applies to the entire stack.

### A. Version Control (Git)

* **Problem:** Merging divergent histories.
* **Code Solution (SVN):** Complex heuristics tracking line numbers.
* **Data Solution (Git):** A **Directed Acyclic Graph (DAG)** of immutable snapshots. Merging is simply a graph traversal to find a common ancestor. The complexity is in the Graph, not the Merge script.
* **Deep Dive:** [[SoT - The Data Architecture of Source Control (Git)]]

### B. Infrastructure (Terraform)

* **Concept:** Infrastructure is not a script; it is a **Data Schema**.
* **Application:** Treating `config.tf` as a database of "Desirable State" (Maps/Lists) and `main.tf` as the "Renderer" that transforms that state into API calls.
* **Deep Dive:** [[SoT - Data-Centric Infrastructure (Terraform)]]

---

## 6. The Methodology: The Torvalds Loop

To practice this discipline, resist the urge to write logic immediately. Follow this strict four-phase protocol: **Shape -> Access -> Invariants -> Logic**.

### Phase 1: Shape (The Physical Reality)

*Goal: Maximise information density; minimise cache misses.*

Focus on the **layout of memory**. Before thinking about "objects" or "methods", define the raw data structures.

- **Action:** Optimise `struct` layouts for mechanical sympathy (CPU cache efficiency, alignment, and padding). Define types based on how hardware will consume them.

### Phase 2: Access (The Interface)

*Goal: Predictable memory pressure and clear ownership.*

Determine the **mechanics of interaction**. How does data move?

- **Decision:** **Value Semantics** (Copying) vs. **Pointer Semantics** (Sharing).
- **Action:** Choose receiver types (Go: `(t T)` vs `(t *T)`) to control stack vs. heap allocation.

### Phase 3: Invariants (The Integrity)

*Goal: Zero trust in the caller; absolute trust in the data.*

Define **validity constraints**. An invariant is a condition that must *always* be true.

- **Action:** Use factory functions and unexported fields to enforce constraints at the boundary. Ensure it is impossible to construct a "broken" Shape.

### Phase 4: Logic (The Transformation)

*Goal: Efficient transformation of valid inputs to valid outputs.*

Only now do you write the algorithms. Because the Shape is optimised and Invariants are enforced, the Logic is simple, linear, and performant.

---

## 7. Implementation Example (Go)

### Mechanical Sympathy & Escape Analysis

In the **Access** phase, hardware realities dictate choices:

1. **Value Semantics (Stack):** Preferred. Data is contiguous (Cache Friendly). Allocation/Deallocation is instant (Stack Pointer movement). Zero GC cost.
2. **Pointer Semantics (Heap):** Use only when necessary. Data is scattered (Cache Misses). Allocation requires finding free space; Deallocation requires Garbage Collection (GC Pause).

**Rule of Thumb:**
- **Sharing Down (Stack Safe):** Passing a pointer *into* a function keeps it on the stack.
- **Sharing Up (Heap Escape):** Returning a pointer *out* of a function forces a heap allocation.

### Code Example: High-Throughput Event System

```go
// PHASE 1: SHAPE
// Ordered by size to minimize padding.
type Event struct {
    ID        uint64
    Timestamp int64
    Payload   []byte // Contiguous memory
    Type      uint8  // Aligned
}

// PHASE 2: ACCESS
// Value Semantics for reading (Cheap copy, Thread-safe).
func (e Event) Bytes() []byte {
    return e.Payload
}

// Pointer Semantics for mutation.
func (e *Event) MarkProcessed() {
    e.Type = 0
}

// PHASE 3: INVARIANTS
// Factory enforces that ID and Payload must exist.
func NewEvent(id uint64, payload []byte) (Event, error) {
    if id == 0 {
        return Event{}, errors.New("invalid ID")
    }
    return Event{ID: id, Payload: payload}, nil
}

// PHASE 4: LOGIC
// The logic is pure transformation because data integrity is guaranteed.
func Process(events []Event) {
    for _, e := range events {
        // No null checks needed; Invariants guarantee validity.
        handle(e)
    }
}
```
