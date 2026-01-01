---
aliases: ["DOP", "DOD", "Data-Oriented Design", "Structure of Arrays"]
confidence: "5/5"
created: 2025-12-31T00:00:00Z
epistemic: "pattern"
last_reviewed: 2026-01-01
modified: 2026-01-01T12:32:06+00:00
purpose: "To define the tactical patterns of Data-Oriented Programming, specifically optimizing for CPU Cache, SIMD, and Memory Layout."
review_interval: "6 months"
see_also: ["[[SoT - Data-Centric Software Engineering]]", "[[SoT - Slot Map (Generational Arena)]]", "[[SoT - Rust Language]]", "[[SoT - Database Internals for Systems Programmers]]"]
source_of_truth: []
status: "stable"
tags: ["dop", "dod", "performance", "architecture", "rust"]
title: SoT - Data-Oriented Programming (DOP)
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] The Core Philosophy
> **Data-Oriented Programming (DOP)** is the practice of designing software based on the **hardware's reality** (Memory Layout, CPU Cache, SIMD) rather than the **programmer's abstraction** (Objects, Classes, Encapsulation).
>
> **The Shift:** From "Modelling Concepts" (Noun-Oriented) to "Modelling Transformations" (Verb-Oriented).

---

## 2. The Core Logic: Machine Sympathy

While OOP optimises for the developer's mental model (grouping properties by entity), DOP optimises for the machine's execution model (streaming data through pipelines).

### 2.1 Memory Layout: AoS vs. SoA

The fundamental difference lies in how data is arranged in RAM.

> **The Hardware Reality:** Cache line sizes and memory latencies are not theoretical; they are defined by the silicon.
> *   *See:* **[[MOC - Cloud Hardware Architecture]]** for the specific latency maps of AWS/Azure.
> *   *See:* **[[SoT - Intel Server Microarchitectures]]** for L1/L2/L3 sizes (Ice Lake vs Sapphire Rapids).

| Layout | Description | Diagram | Pros | Cons |
|:--- |:--- |:--- |:--- |:--- |
| **AoS** | **Array of Structures** (OOP) | `[XYZ, XYZ, XYZ]` | Easy to access one entity. | Cache pollution. No SIMD. |
| **SoA** | **Structure of Arrays** (DOP) | `[XXX, YYY, ZZZ]` | **SIMD ready.** 100% Cache hits. | Harder to add/remove entities. |

#### The "Cache Line" Reality (The Kitchen Analogy)

The CPU fetches memory in **64-byte chunks** (Cache Lines).

* **OOP:** Fetching a `Player` to update their `x` position brings in `name`, `inventory`, and `status` (Junk data).
* **DOP:** Fetching the `Position` array brings in 16 `x` coordinates at once. Every byte loaded is used.

### 2.2 SIMD (Single Instruction, Multiple Data)

Because SoA layout places homogeneous data contiguously (e.g., `[x1, x2, x3, x4]`), the compiler (LLVM) or hardware can execute a single instruction to update multiple entities simultaneously.

* **Scalar (OOP):** `x1 += v1` (1 cycle) -> `x2 += v2` (1 cycle)...
* **Vector (DOP):** `[x1,x2,x3,x4] += [v1,v2,v3,v4]` (**1 cycle total**).

---

## 3. Structural Comparison: OOP vs DOP

| Feature | Object-Oriented (OOP) | Data-Oriented (DOP) |
|:--- |:--- |:--- |
| **Primary Unit** | The **Object** (State + Behaviour) | The **System** (Logic) + **Component** (Data) |
| **Logic Location** | Methods inside classes | Pure functions in stateless modules |
| **Data Visibility** | Encapsulated (Private) | Transparent (Public/Structs) |
| **Polymorphism** | V-Tables (Inheritance) | Enums / Switch / Pattern Matching |
| **State** | Mutable internal state | Immutable / Partitioned data streams |
| **Thinking Style** | "What is this thing?" | "How is this data transformed?" |

---

## 4. The "Hybrid" Architecture (Virtual Objects)

Pure DOP can be cognitively difficult. The standard industry solution (used in Game Engines like Unity DOTS) is the **Hybrid Approach**.

### The "Iceberg" Model

* **Above Water (API):** Standard OOP classes/interfaces for ease of use.
* **Below Water (Core):** DOP/SoA arrays for performance.

### The "Handle" Pattern

The Object the user holds is a lie. It is a "Handle" containing only an ID and a reference to the central data store.

```typescript
// THE CORE (DOP) - Hidden
class ParticleRepository {
    x: Float32Array; // Structure of Arrays
    y: Float32Array;
}

// THE SHELL (OOP) - Exposed
class ParticleHandle {
    constructor(private repo: ParticleRepository, private id: number) {}

    // Looks like OOP, acts like DOP
    get x() { return this.repo.x[this.id]; }
    set x(val) { this.repo.x[this.id] = val; }
}
```

---

## 5. Architectural Patterns

### 5.1 Existence-Based Predication (The Dirty Flag)

Instead of checking every object `if (obj.isActive)` or `if (obj.isDirty)`:

* **The Anti-Pattern:** Branch misprediction hell. The CPU cannot guess the state of the flag.
* **The Pattern:** Move objects to separate collections based on state (e.g., `ActiveParticles` vs `InactiveParticles`).
* **Result:** Iterate linearly over the `Active` array. **Zero branching.**

### 5.2 The "Database" Mindset

Treat application state as an **In-Memory Relational Database**.

* **Objects** -> Primary Keys (IDs).
* **Properties** -> Columns (Arrays).
* **References** -> Foreign Keys (IDs).
* **Loops** -> Query Plans (Full Table Scans).
* **Find** -> Index Lookups (Maps).

### 5.3 Slot Maps (Safe References)

To solve the "Dangling Pointer" problem in DOP (where indices are reused), use **Generational Indices**.

* *See:* [[SoT - Slot Map (Generational Arena)]]

### 5.4 Table-Based Output (Decoupling)

Rather than calling methods on external systems (e.g., `Render()`), output a **Table of Changes**.

* **Process:** Logic -> `DrawCommands[]`.
* **Consumption:** Renderer consumes `DrawCommands`.
* **Benefit:** The Logic is now a pure transformation pipeline. The Renderer is just a consumer. No tight coupling.

---

## 6. When to use DOP? (The Benchmark)

**Casey Muratori's Benchmark:** Pure "Clean Code" (OOP) vs. DOP can result in a **1.5x to 10x** performance difference. A 10x loss is equivalent to erasing **12 years of hardware progress**.

| Use OOP (Standard) | Use DOP (Performance) |
|:--- |:--- |
| **Heterogeneous Data:** UI Widgets, configuration, complex singletons. | **Homogeneous Data:** Particles, enemies, database rows, pixels. |
| **Complex Logic:** State depends on private history. | **Simple Logic:** Position = Position + Velocity. |
| **Developer Speed:** Ease of use is priority. | **Execution Speed:** Latency/Throughput is priority. |
