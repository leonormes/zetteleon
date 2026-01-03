---
source_of_truth: []
aliases: ["Rust HPC", "Azure AKS Rust Optimization", "ZK Proof Optimization", "Hardware Targeting"]
confidence: "5/5"
created: 2026-01-02T14:40:00Z
epistemic: "knowledge"
last_reviewed: "2026-01-02"
modified: 2026-01-03T10:18:48+00:00
purpose: "To define the full-stack optimization path for Rust applications running compute-intensive workloads on cloud infrastructure (AKS)."
review_interval: "6 months"
see_also: ["[[SoT - Rust Concurrency & Async Paradigms]]", "[[SoT - Data-Oriented Programming (DOP) in Rust]]"]
status: "stable"
tags: ["rust", "hpc", "optimization", "azure", "aks", "zkp"]
title: SoT - Rust High-Performance Computing (HPC) Optimization
type: "SoT"
---

## 1. Infrastructure Layer (Azure AKS Tuning)

Standard Kubernetes scheduling is suboptimal for compute-heavy ZK workloads due to cache invalidation.

### 1.1 CPU Pinning & Topology

* **Static CPU Manager:** Switch kubelet policy to `static`. This grants the pod **exclusive** use of CPU cores.
* **Single NUMA Node:** Use `topologyManagerPolicy: single-numa-node` to ensure all cores and memory are on the same physical socket, preventing high-latency cross-NUMA access.
* **Guaranteed QoS:** Kubernetes only pins CPUs if `resources.limits` exactly match `resources.requests` and use **integer** cores.

### 1.2 Huge Pages

Heavy field arithmetic (FFT, MSM) causes massive TLB (Translation Lookaside Buffer) thrashing. Use **2MB** or **1GB** Huge Pages to reduce address translation overhead.

---

## 2. Build Layer (Targeting the Silicon)

Generic `x86_64` binaries miss 2x-4x performance gains from specialized vector instructions.

* **Targeting:** Compile specifically for the Azure node's architecture (e.g., Intel Ice Lake/Cascade Lake).
* **AVX-512:** Crucial for the 256-bit field arithmetic in ZK proofs.
* **Flag:** Use `RUSTFLAGS="-C target-cpu=skylake-avx512"` or a specific architecture rather than generic `native` (which might target the CI/CD runner).

---

## 3. Application Layer (The Optimization Stack)

### 3.1 Memory Allocation

The default `libc` malloc suffers from lock contention under high thread counts.

* **Solution:** Use `jemallocator` or `mimalloc`.
* **Impact:** Reduces memory fragmentation and allocation bottlenecks.

### 3.2 Thread Pinning

Even with K8s pinning, the application must map its software threads 1:1 to logical hardware cores.

* **Tool:** `core_affinity` crate.

### 3.3 Data-Oriented Hot Loops

* **Binary over JSON:** Avoid JSON/Hex strings in compute loops. Use raw `[u8; 64]` or flat binary structs.
* **Flat Arrays:** Avoid `Vec<Box<T>>` (pointer chasing). Use `Vec<u64>` or `Vec<Fr>` (contiguous memory) for pre-fetching efficiency.

---

## 4. Summary Checklist for the Architect

| Layer | Optimization | Why? |
|:--- |:--- |:--- |
| **K8s** | `cpuManagerPolicy: static` | Prevents context switching and noisy neighbor issues. |
| **K8s** | `single-numa-node` | Eliminates cross-socket memory latency. |
| **Build** | `target-cpu=...` | Enables vector instructions (AVX-512) for ZK math. |
| **Rust** | `jemallocator` | Removes allocation locks. |
| **Rust** | `core_affinity` | Maps software threads to hardware silicon. |
