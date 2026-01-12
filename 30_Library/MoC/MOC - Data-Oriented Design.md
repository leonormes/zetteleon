---
aliases:
  - Cache Optimization
  - DoD
  - Performance Engineering
confidence: 5/5
created: 2026-01-07T00:00:00Z
epistemic: Physical Reality
last_reviewed:
modified: 2026-01-08T15:03:28+00:00
purpose: To define the physical constraints of computing hardware (Cache, Memory, Layout) and how they dictate software performance.
review_interval: 1 year
see_also:
  - "[[SoT - Rust Type Mechanics]]"
  - "[[SoT - The Data-Centric Philosophy]]"
source_of_truth: []
status: Stable
tags:
  - cache
  - data-oriented-design
  - hardware
  - performance
title: MOC - Data-Oriented Design
type: map
uid:
updated:
---

## MOC - Data-Oriented Design

> **The Core Reality:** Hardware is the platform. The CPU does not see "Objects"; it sees **Bytes** and **Strides**. Performance is a function of **Data Layout**, not Code Elegance.

### 1. The Three Big Lies (Mike Acton)

1. **"Software is the platform."** No. Hardware is the platform.
2. **"Code models the world."** No. Code transforms data.
3. **"Code > Data."** No. If you don't understand the data layout, you don't understand the performance.

### 2. The Physics of Computing

#### The Kitchen Analogy

- **Chef (CPU):** fast.
- **Counter (L1 Cache):** Instant access.
- **Supermarket (RAM):** 200 cycles away.
- **The DoD Goal:** Keep the Chef at the Counter. Do not drive to the Supermarket for one onion (Pointer Chasing).

#### The Cache Line (The Truck)

- **Unit:** Memory is fetched in **64-byte lines**.
- **The Rule:** Every byte fetched MUST be used.
- **The Fail:** Objects (`AoS`) are "Swiss Cheese" (Padding + VTables). 90% bandwidth waste.

### 3. Structural Patterns

| Pattern | Definition | Benefit |
|:--- |:--- |:--- |
| **SoA (Structure of Arrays)** | `[x,x,x]`, `[y,y,y]` | 100% Cache Density. SIMD-ready. |
| **Existence Predication** | Separate "Active" Array | Zero Branching (`if is_active`). |
| **Indexes over Pointers** | `u32` ID vs `*T` | Halves size. Relocatable. Safe. |

### 4. Related Concepts

- [[SoT - Rust Type Mechanics]] (Enforcing Layout)
- [[SoT - The Logical Definition of a Computer]] (The Hardware Context)
