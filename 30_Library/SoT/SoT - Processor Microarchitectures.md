---
aliases: ["Intel Ice Lake vs Sapphire Rapids vs Emerald Rapids", "Processor Specs"]
confidence: "5/5"
created: 2026-01-07T00:00:00Z
epistemic: "Hardware Specs"
last_reviewed: 
modified: 2026-01-08T10:49:41+00:00
purpose: "To compare the microarchitectural features of Intel Ice Lake, Sapphire Rapids, Emerald Rapids, and AWS Graviton3 for data plane optimization."
review_interval: "1 year"
see_also:
  - "[[SoT - Cloud Compute Architectures]]"
source_of_truth: []
status: "Stable"
tags: ["arm", "cache", "intel", "microarchitecture", "processor"]
title: SoT - Processor Microarchitectures
type: "SoT"
uid: 
updated: 
---

## SoT - Processor Microarchitectures

> **Optimization Reality:** Data-Oriented Design requires tuning for the specific cache hierarchy of the underlying silicon.

### 1. Comparative Specification

| Feature | Ice Lake (m6i/D_v5) | Sapphire Rapids (m7i) | Emerald Rapids (D_v6) | Graviton3 (m7g) |
|:--- |:--- |:--- |:--- |:--- |
| **Core** | Sunny Cove | Golden Cove | Raptor Cove | Neoverse V1 |
| **Topology** | Monolithic (MCC) | 4-Tile Chiplet (XCC) | 2-Tile Chiplet (XCC) | Monolithic |
| **L2 Cache** | 1.25 MB | 2 MB | 2 MB | 1 MB |
| **L3 Cache** | 1.5 MB/core | 1.875 MB/core | **5 MB/core** | ~32MB (Shared) |
| **Memory** | DDR4-3200 | DDR5-4800 | **DDR5-5600** | DDR5-4800 |
| **Vector** | AVX-512 (Throttles) | AMX / AVX-512 | AMX / AVX-512 | SVE (256-bit) |

### 2. Microarchitectural Notes

#### Intel Ice Lake (The Baseline)

- **Non-Inclusive L2:** Maximizes total cache capacity.
- **Limitation:** Heavy AVX-512 usage triggers frequency downclocking ("licensing" penalties).

#### Intel Sapphire Rapids (The Workhorse)

- **Chiplet Design:** High throughput but introduces "Mesh" latency. Remote memory access incurs ~140ns latency.
- **AMX:** Accelerates matrix math without the severe throttling of AVX-512.

#### Intel Emerald Rapids (The Cache King)

- **5 MB L3:** Allows massive instruction and data pools (320MB on large sizes) to stay on-die.
- **Consolidation:** 2-Tile design reduces mesh hops compared to Sapphire Rapids.

#### AWS Graviton3 (The Efficient Alternative)

- **Monolithic:** Avoids tile-to-tile penalties.
- **Consistency:** Superior performance-per-watt, though lower peak vector throughput than x86.
