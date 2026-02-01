---
aliases: ["AWS Nitro", "Nitro Cards", "Nitro System"]
created: 2025-12-31T00:00:00Z
last_reviewed: "2025-12-31"
modified: 2026-02-01T15:08:02+00:00
status: "stable"
tags: ["aws", "cloud", "hypervisor", "performance"]
title: SoT - AWS Nitro System
type: "SoT"
updated: 
---

## 1. Definitive Statement

> The AWS Nitro System is a decoupled virtualization architecture that offloads I/O, networking, storage, and security to dedicated ASICs (Nitro Cards), leaving the main system processor to run a lightweight, KVM-based hypervisor.

For high-performance workloads, Nitro is the gold standard because it effectively eliminates Steal Time and provides High-Fidelity Topology Pass-through.

---

## 2. Architectural Advantages for Data Planes

### 2.1 Static Pinning (Anti-Jitter)

Nitro instances (specifically `m6i`, `m7i`, `c7g`) typically map vCPUs to physical threads in a static manner.

- The Benefit: Once an instance launches, vCPU 0 is pinned to Physical Core X. It does not migrate.
- DOP Impact: L1 and L2 caches remain hot. There is no "Scheduler Thrashing" where the hypervisor moves your thread to a different core, invalidating your cache lines.

### 2.2 Topology Pass-through

Nitro exposes the underlying physical hardware topology (NUMA nodes, L3 Cache slices) directly to the guest OS.

- The Benefit: `numactl --hardware` inside an `m7i.48xlarge` reports the _actual_ physical sockets or SNC (Sub-NUMA Cluster) domains.
- DOP Impact: Kubernetes `TopologyManager` can make correct decisions because the "Virtual Topology" matches the "Physical Topology."

### 2.3 Resource Isolation

Nitro ensures no sharing of core-specific resources (L1/L2, execution ports) between tenants.

- Noisy Neighbor Mitigation: Hard hardware partitioning via Intel RDT (Resource Director Technology) prevents other tenants from thrashing your L3 cache.
