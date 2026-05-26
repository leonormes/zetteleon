---
aliases: [Anemic Domain Model, Cache Optimization, DOD, Performance Engineering, The Physics of DOD]
created: 2026-01-30T09:00:00+00:00
last_synthesis: 2026-04-02
modified: 2026-05-26T11:44:20+00:00
source_of_truth: true
status: evergreen
synthesis-count: 2
tags: [cache, data-oriented-design, hardware, mechanical-sympathy, performance]
title: SoT - Data-Oriented Design
trust-level: stable
type: "SoT"
---

## Minimum Viable Understanding (MVU)

Data-Oriented Design (DOD) is the architectural realization that Hardware is the Platform. The CPU does not see "Objects"; it sees Bytes and Strides. Performance is a function of Data Layout, not Code Elegance. By aligning data with the hardware's physical reality (CPU Caches), we achieve orders of magnitude improvement in throughput.

---

## 1. The Three Big Lies (Mike Acton)

To write high-performance software, we must reject these abstractions:

1. "Software is the platform." No. Hardware is the platform.
2. "Code models the world." No. Code transforms data.
3. "Code > Data." No. If you don't understand the data layout, you don't understand the performance.

---

## 2. The Physics: The Kitchen Analogy

Memory access is the primary bottleneck of modern computing.

- Chef (CPU): Fast. Can process millions of instructions per second.
- Counter (L1 Cache): Instant access. The "Work Area."
- Supermarket (RAM): 200–500 cycles away.
- The DOD Goal: Keep the Chef at the Counter. Avoid driving to the Supermarket for a single item (Pointer Chasing).

---

## 3. The Cache Line (The Truck)

- Unit: Memory is fetched in 64-byte lines.
- The Rule: Every byte fetched MUST be used. If you fetch a 64-byte line but only use one 4-byte integer, you have wasted 94% of your bandwidth.
- The Fail (OOD): Objects (`AoS`) are "Swiss Cheese" (Padding, VTables, and irrelevant fields). Processing a list of `Player` names requires loading the entire `Player` object (health, position, inventory) into cache, wasting space.

---

## 4. Structural Patterns for Performance

### 4.1 SoA (Structure of Arrays)

- OOD Pattern (Array of Structures): `[{x, y, z}, {x, y, z}, {x, y, z}]`.
- DOD Pattern (SoA): `[x,x,x]`, `[y,y,y]`, `[z,z,z]`.
- Benefit: 100% Cache Density for specific operations. If you only need `x` coordinates, the cache contains only `x` coordinates. It is also SIMD-ready.

### 4.2 Existence Predication

- Instead of using `if (active)` inside a loop (branching), maintain a separate array of "Active" indices.
- Benefit: Zero Branch Misprediction. The CPU can pipeline the transformation without interruption.

### 4.3 Indexes over Pointers

- Use `u32` IDs (indices) instead of raw pointers (`*T`).
- Benefit: Halves the size on 64-bit systems. Data remains relocatable (for memory compaction) and is safer (bounds checking).

---

## Related Knowledge

- Philosophy (The Axiom): [[SoT - The Data-Centric Philosophy]]
- Practice (The Protocol): [[SoT - Type-Driven Development (The Torvalds Loop)]]
- Internals (The Structures): [[MOC - Data-Oriented Structures & Internals]]
- Hardware Context: [[SoT - The Logical Definition of a Computer]]
