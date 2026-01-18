---
aliases: ["AWS vs Azure Compute", "Cloud Silicon Topology", "Compute Architectures"]
confidence: "5/5"
created: 2025-12-31T16:56:11+00:00
epistemic: "Architectural Audit"
last_reviewed: 
modified: 2026-01-08T10:49:44+00:00
purpose: "To define the architectural shift from monolithic to chiplet designs in cloud compute and identify the optimal substrates for high-performance data planes."
review_interval: "1 year"
see_also:
  - "[[SoT - Hypervisor Abstractions]]"
  - "[[SoT - Processor Microarchitectures]]"
source_of_truth: []
status: "Stable"
tags: ["architecture", "aws", "azure", "cloud", "compute"]
title: SoT - Cloud Compute Architectures
type: "SoT"
uid: 
updated: 
---

## SoT - Cloud Compute Architectures

> **The Shift:** Cloud compute is transitioning from **Monolithic** dies (Uniform Memory Access) to **Disaggregated Chiplets** (Non-Uniform Memory Access). This breaks the "Flat Memory" assumption, introducing complex latency maps defined by interconnect topology.

### 1. The Topology Transition

- **Monolithic (Old):** Single die (Ice Lake). Predictable, uniform latency (~85ns).
    - _Instances:_ AWS m6i, Azure D_v5.
- **Chiplet (New):** Multi-tile mesh (Sapphire/Emerald Rapids). High throughput (DDR5), variable latency (95ns-150ns).
    - _Instances:_ AWS m7i, Azure D_v6.

### 2. The Instance Selection Matrix

For Data-Oriented Design, the "Instance Type" is a specific Silicon SKU with a known cache hierarchy.

| Workload Characteristic | Recommended Instance | Reasoning |
|:--- |:--- |:--- |
| **Latency Sensitive (Cache Heavy)** | **Azure D_v6 (Emerald Rapids)** | **5 MB L3/core** (320MB Pool). Massive cache masks DRAM latency. |
| **Throughput Intensive (Vector)** | **AWS m7i (Sapphire Rapids)** | DDR5 bandwidth + AMX/AVX-512. Nitro System provides "Near-Metal" topology transparency. |
| **General Purpose** | **AWS m6i / Azure D_v5** | Monolithic design offers lower core-to-core latency variance. Mature and cost-effective. |
| **Cost-Sensitive** | **AWS m7g (Graviton3)** | Monolithic mesh avoids tile penalties. Excellent perf/watt for non-AVX-512 workloads. |

### 3. The "Golden Config" for Data Planes

To align software with silicon reality:

1. **BIOS:** Disable "Node Interleaving" (Enable NUMA) where possible.
2. **Kernel:** `isolcpus` to remove OS noise; `transparent_hugepage=never` to stop compaction jitter.
3. **Kubernetes:** `--topology-manager-policy=single-numa-node` to enforce socket affinity.
4. **Application:** Align data structures to **64-byte** cache lines and fit hot sets within **2 MB** (L2).
