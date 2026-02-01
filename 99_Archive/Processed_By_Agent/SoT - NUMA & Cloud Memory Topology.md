---
aliases: ["Cloud Latency", "NUMA", "SNC", "Sub-NUMA Clustering", "UPI"]
confidence: "5/5"
created: 2025-12-31T00:00:00Z
epistemic: "fact"
last_reviewed: "2025-12-31"
modified: 2026-01-08T10:49:42+00:00
purpose: "To map the physical latency terrain of cloud memory interconnects."
review_interval: "1 year"
see_also: ["[[MOC - Cloud Hardware Architecture]]"]
source_of_truth: []
status: "stable"
tags: ["hardware", "latency", "numa", "performance"]
title: SoT - NUMA & Cloud Memory Topology
type: "SoT"
uid: 
updated: 
---

## 1. The Latency Map

In modern cloud servers, "Memory" is not a flat pool. It is a tiered landscape defined by physical distance and interconnects.

| Path | Latency | Description |
|:--- |:--- |:--- |
| L1 Cache | ~1 ns | Instant. |
| L2 Cache | ~3 ns | Private to core. |
| L3 Cache (Local Slice) | ~20 ns | On the same mesh stop. |
| L3 Cache (Remote Slice) | ~35 ns | On a different tile (Sapphire/Emerald). |
| Local DRAM | ~90 ns | Attached to local memory controller. |
| Remote DRAM (1 Hop) | ~140 ns | Across the UPI link to the other socket. |

---

## 2. The Interconnects

### 2.1 UPI (Ultra Path Interconnect)

The bridge between Sockets.

- Cost: Crossing this link adds ~50ns of latency.
- Risk: If a Kubernetes pod is split across sockets, 50% of its memory access might be remote, degrading performance by 30-40%.

### 2.2 Sub-NUMA Clustering (SNC)

Modern CPUs partition a single socket into logical NUMA domains (SNC2 or SNC4) to localize traffic.

- AWS: Often disables SNC, presenting 1 NUMA node per socket. This "averages" latency (raising the floor but lowering the ceiling).
- Azure: Often exposes SNC. This allows higher peak performance _if_ the application is NUMA-aware, but risks severe penalties if the OS scheduler migrates threads across domains.

---

## 3. The Lie of "Flat Memory"

On 4-Tile chips (Sapphire Rapids), even "Local Socket" memory access is non-uniform. Accessing a memory controller on a different tile involves traversing the EMIB (Embedded Multi-die Interconnect Bridge). This creates "Near" and "Far" memory within the same socket.
