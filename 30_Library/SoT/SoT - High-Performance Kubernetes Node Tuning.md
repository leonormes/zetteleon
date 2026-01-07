---
aliases: ["K8s Node Tuning", "The Golden Config", "Topology Manager Policy", "CPU Pinning K8s"]
confidence: "High"
created: 2026-01-06
epistemic: "Guide"
last_reviewed: 
modified: 
purpose: "To define the specific OS and Kubernetes configurations required to align the software data plane with the underlying hardware topology for maximum performance."
review_interval: "1 year"
see_also: 
  - "[[SoT - Cloud Compute Substrates (Audit)]]"
  - "[[MOC - Cloud Hardware Architecture]]"
source_of_truth: []
status: "Active"
tags: ["kubernetes", "performance", "tuning", "linux", "numa"]
title: SoT - High-Performance Kubernetes Node Tuning
type: "SoT"
uid: 
updated: 
---

# SoT - High-Performance Kubernetes Node Tuning

> **The Golden Config:** Bridging the gap between virtual abstraction and silicon reality. The default "Best Effort" policies of Kubernetes are insufficient for high-throughput data planes on tiled CPUs (Sapphire/Emerald Rapids).

## 1. The Core Strategy: Alignment

We must align three layers:
1.  **Physical:** The NUMA/Socket topology.
2.  **Kernel:** The Linux scheduler and memory manager.
3.  **Kubernetes:** The Kubelet's resource allocation.

## 2. Kubernetes Configuration (Kubelet)

### A. Topology Manager
*   **Policy:** `single-numa-node`
*   **Mechanism:** Restricts a pod's CPU and Memory allocation to a single NUMA domain.
*   **Why:** Prevents cross-socket traffic (UPI traversal), which incurs a ~1.5x latency penalty. On tiled CPUs (Sapphire Rapids), this aligns the pod to a specific "quadrant" of the mesh.

### B. CPU Manager
*   **Policy:** `static`
*   **Mechanism:** Grants **exclusive**, pinned physical cores to containers requesting integer CPU limits (Guaranteed QoS).
*   **Why:** Eliminates "Steal Time" and cache thrashing caused by the Linux CFS scheduler migrating threads between cores.

### C. Pod Specification (Guaranteed QoS)
To trigger the strict policies above, the Pod spec must meet specific criteria:
```yaml
resources:
  limits:
    cpu: "8"            # Must be an integer (not 8.5)
    memory: "16Gi"
    hugepages-1Gi: "16Gi"
  requests:
    cpu: "8"            # Must match limits exactly
    memory: "16Gi"
```

## 3. Kernel & OS Tuning (Boot Parameters)

### A. Explicit Huge Pages
*   **Parameter:** `default_hugepagesz=1G hugepagesz=1G hugepages=N`
*   **Why:** Reduces TLB (Translation Lookaside Buffer) misses. 1GB pages are superior to 2MB pages for large heaps because they require 512x fewer TLB entries.
*   **Critical:** Must be allocated at boot time to ensure physical contiguity.

### B. Transparent Huge Pages (THP)
*   **Parameter:** `transparent_hugepage=never`
*   **Why:** The `khugepaged` background daemon introduces non-deterministic latency spikes ("jitter") as it defragments memory. For predictable latency, disable it and use explicit pages.

### C. CPU Isolation (Advanced)
*   **Parameter:** `isolcpus=<list>`
*   **Why:** Removes specific cores from the general kernel scheduler balancing algorithms. Useful for extreme low-latency requirements, but requires manual thread placement (`taskset`) inside the application.

## 4. Application-Layer Alignment (DOD)

The software must be aware of its boundaries.

1.  **Thread Affinity:** Bind worker threads to specific logical cores (Hyper-threads).
    *   *Pattern:* Place cooperative threads (Worker + Helper) on sibling hyper-threads (L1/L2 sharing).
    *   *Pattern:* Place contentious threads (Worker + Worker) on separate physical cores.
2.  **Memory Awareness:** Use `libnuma` to ensure memory is allocated on the local node. (Usually handled automatically by the `single-numa-node` policy if the application doesn't explicitly override it).