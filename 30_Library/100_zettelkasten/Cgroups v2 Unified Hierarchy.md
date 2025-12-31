---
aliases: ["cgroups v2", "Unified Hierarchy"]
confidence: "5/5"
created: 2025-12-24T12:00:00Z
epistemic: "technical"
last_reviewed: 2025-12-24
modified: 2025-12-31T23:08:54+00:00
purpose: "To explain the differences and improvements in cgroups v2."
review_interval: "1 year"
see_also: ["[[Cgroups Limit and Manage Container Resources]]"]
source_of_truth: ["[[SoT - Linux Container Primitives]]"]
status: "stable"
tags: ["kernel", "linux", "modern-cgroups"]
title: Cgroups v2 Unified Hierarchy
type: "concept"
uid: 
updated: 
---

## Cgroups V2

**Cgroups v2** is the second version of the Linux control groups API, designed to address the inconsistencies and complexity of the original v1 implementation. It is the modern standard for Linux distributions and Kubernetes (v1.25+).

### ✨ Key Improvements

- **Unified Hierarchy:** Unlike v1, which had separate trees for each controller (CPU, Memory, etc.), v2 uses a single tree where a process belongs to exactly one cgroup.
- **Safer Subtree Delegation:** Allows non-root users to safely manage resources for sub-groups, enabling **Rootless Containers**.
- **Pressure Stall Information (PSI):** Provides granular metrics on resource contention (waiting for CPU/IO), allowing for smarter orchestration.
- **Improved Memory Control:** More consistent hard/soft limits and better OOM (Out of Memory) handling.

### 🧩 Relational Context

The move to v2 simplifies the interface for container runtimes like **Containerd** and **CRI-O**, leading to more predictable performance and better security through rootless operation.

- **Links**: [[Cgroups Limit and Manage Container Resources]], [[SoT - Linux Container Primitives]]
