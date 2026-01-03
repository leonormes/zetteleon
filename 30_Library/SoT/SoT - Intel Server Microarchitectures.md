---
aliases: ["Ice Lake", "Sapphire Rapids", "Emerald Rapids", "Intel Xeon Scalable"]
confidence: "5/5"
created: 2025-12-31T00:00:00Z
epistemic: "fact"
last_reviewed: "2025-12-31"
modified: 2026-01-03T10:18:54+00:00
purpose: "To detail the specific silicon microarchitectures powering AWS m6i/m7i and Azure D_v5/D_v6 instances."
review_interval: "1 year"
see_also: ["[[MOC - Cloud Hardware Architecture]]"]
source_of_truth: []
status: "stable"
tags: ["hardware", "intel", "cpu", "cache", "performance"]
title: SoT - Intel Server Microarchitectures
type: "SoT"
uid: 
updated: 
---

## 1. The Generational Shift

The cloud is transitioning from **Monolithic** dies (Uniform) to **Chiplet/Tile** designs (Non-Uniform).

| Feature | Ice Lake (3rd Gen) | Sapphire Rapids (4th Gen) | Emerald Rapids (5th Gen) |
|:--- |:--- |:--- |:--- |
| **Instance** | AWS `m6i` / Azure `D_v5` | AWS `m7i` | Azure `D_v6` |
| **Core** | Sunny Cove | Golden Cove | Raptor Cove |
| **Topology** | **Monolithic** (MCC) | **4-Tile Chiplet** (XCC) | **2-Tile Chiplet** (XCC) |
| **L2 Cache** | 1.25 MB | 2 MB | 2 MB |
| **L3 Cache** | 1.5 MB/core | 1.875 MB/core | **5 MB/core** |
| **Memory** | DDR4-3200 | DDR5-4800 | **DDR5-5600** |

---

## 2. Ice Lake (The Old Guard)

* **Architecture:** Monolithic die.
* **Pro:** Uniform memory latency. Ideally suited for "General Purpose" workloads where NUMA awareness is low.
* **Con:** **AVX-512 Downclocking.** Heavy vector usage throttles the CPU frequency significantly.

## 3. Sapphire Rapids (The Tile Era)

* **Architecture:** 4 Compute Tiles connected by EMIB.
* **Pro:** **AMX (Advanced Matrix Extensions)** allows massive matrix math throughput without the severe frequency penalties of AVX-512.
* **Con:** **Mesh Latency.** Accessing L3 cache on a different tile (even within the same socket) incurs a latency penalty. This breaks the "Uniform Socket" assumption.

## 4. Emerald Rapids (The Cache King)

* **Architecture:** Refined 2-Tile design.
* **The Killer Feature:** **5 MB L3 Cache per Core**.
    * On a 64-core instance, this creates a **320 MB Shared L3 Pool**.
    * **DOP Impact:** Entire instruction sets and massive packet lookup tables can sit resident in L3, masking the higher latency of DRAM. This makes D_v6 the superior choice for latency-sensitive data planes.
