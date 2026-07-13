---
aliases: [cgroups, Control Groups]
created: 2025-12-24T12:00:00+00:00
modified: 2026-07-13T08:44:53+00:00
permalink: llmeon/30-library/100-zettelkasten/cgroups-limit-and-manage-container-resources
tags: [kernel, resource-management, SoftwareEngineering/Containers, SoftwareEngineering/Linux]
title: Cgroups Limit and Manage Container Resources
---

## Control Groups (Cgroups)

Cgroups are a Linux kernel feature that provides a mechanism for aggregating sets of processes into hierarchical groups with specialised behaviour. They act as the "resource containers" for modern virtualisation.

### 🧩 Core Functionalities

- Resource Limiting: Sets hard/soft limits on memory, CPU, and I/O.
- Prioritisation: Assigns relative weights (shares) so critical processes get priority during contention.
- Accounting: Tracks usage metrics for billing or capacity planning.
- Control: Allows suspending (freezing) or resuming groups of processes.

### 📁 Implementation: Cgroupfs

Cgroups are managed via a pseudo-filesystem (usually at `/sys/fs/cgroup`).

- Directories: Represent individual cgroups.
- Files: Act as the interface for controllers (e.g., `cpu.max`, `memory.limit_in_bytes`).
- PIDs: Processes are added by writing their PID to `cgroup.procs`.

### 🚀 Usage in Containerisation

- Docker: Maps the `--cpus` and `--memory` flags directly to cgroup settings.
- Kubernetes: Uses cgroups to enforce Resource Quotas and manage Burstable vs. Guaranteed pods (Noisy Neighbour prevention).
- Links: [[What is a PID namespace]], [[Cgroups v2 Unified Hierarchy]]
