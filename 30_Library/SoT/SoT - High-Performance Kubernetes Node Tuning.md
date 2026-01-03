---
aliases: ["K8s Node Tuning", "Golden Config", "Topology Manager", "Hugepages"]
confidence: "5/5"
created: 2025-12-31T00:00:00Z
epistemic: "pattern"
last_reviewed: "2025-12-31"
modified: 2026-01-03T10:18:54+00:00
purpose: "To define the 'Golden Config' for high-performance Kubernetes data planes on modern cloud hardware."
review_interval: "6 months"
see_also: ["[[MOC - Cloud Hardware Architecture]]"]
source_of_truth: []
status: "stable"
tags: ["kubernetes", "performance", "configuration", "tuning"]
title: SoT - High-Performance Kubernetes Node Tuning
type: "SoT"
uid: 
updated: 
---

## 1. The "Golden Config"

To align the software data plane with the physical reality of Cloud Silicon, the following Kubelet and OS configurations are mandatory.

### 1.1 Topology Manager

**Policy:** `single-numa-node`
* **Effect:** Restricts a Pod's resource allocation (CPU + Memory) to a single NUMA domain.
* **Why:** Prevents the "Split Brain" scenario where a Pod straddles the UPI link, incurring the ~140ns remote memory penalty.

### 1.2 CPU Manager

**Policy:** `static`
* **Effect:** Grants exclusive physical cores to containers in the `Guaranteed` QoS class.
* **Why:** Removes the container from the CFS Shared Pool, eliminating "Steal Time" and maximizing L1/L2 cache locality.

### 1.3 Huge Pages (Explicit)

**Config:** `hugepages-1Gi` (Boot Parameter: `hugepagesz=1G hugepages=N`)
**Disable:** `transparent_hugepage=never`
* **Why:**
    1. Reduces TLB misses (critical for large heaps).
    2. Eliminates the non-deterministic jitter of the `khugepaged` background defragmenter.

### 1.4 Interrupt Isolation

**Config:** `isolcpus=<data_plane_cores>`
* **Effect:** Instructs the Linux kernel to NEVER schedule general processes or IRQs on these cores.
* **Usage:** The Data Plane application must manually bind itself to these cores using `taskset` or internal affinity APIs.

---

## 2. Pod Specification Example

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: high-perf-data-plane
spec:
  containers:
  - name: dp-app
    resources:
      limits:
        cpu: "8" # Must be integer for static policy
        memory: "16Gi"
        hugepages-1Gi: "16Gi" # Explicit hugepages
    securityContext:
      privileged: true # Often needed for specialized networking (SR-IOV/DPDK)
```
