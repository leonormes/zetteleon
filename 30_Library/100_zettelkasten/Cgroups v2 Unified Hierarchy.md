---
aliases:
- cgroups v2
- Unified Hierarchy
created: 2025-12-24 12:00:00+00:00
modified: 2026-07-04 10:51:53+00:00
permalink: llmeon/30-library/100-zettelkasten/cgroups-v2-unified-hierarchy
tags:
- kernel
- modern-cgroups
- SoftwareEngineering/Linux
title: Cgroups v2 Unified Hierarchy
prodos:
  kind: atomic
  atomic:
    form: concept
  lifecycle: stable
  review:
    last_reviewed: 2025-12-24
---


## Cgroups V2

Cgroups v2 is the second version of the Linux control groups API, designed to address the inconsistencies and complexity of the original v1 implementation. It is the modern standard for Linux distributions and Kubernetes (v1.25+).

### ✨ Key Improvements

- Unified Hierarchy: Unlike v1, which had separate trees for each controller (CPU, Memory, etc.), v2 uses a single tree where a process belongs to exactly one cgroup.
- Safer Subtree Delegation: Allows non-root users to safely manage resources for sub-groups, enabling Rootless Containers.
- Pressure Stall Information (PSI): Provides granular metrics on resource contention (waiting for CPU/IO), allowing for smarter orchestration.
- Improved Memory Control: More consistent hard/soft limits and better OOM (Out of Memory) handling.

### 🧩 Relational Context

The move to v2 simplifies the interface for container runtimes like Containerd and CRI-O, leading to more predictable performance and better security through rootless operation.

- Links: [[Cgroups Limit and Manage Container Resources]], [[SoT - Linux Container Primitives]]
