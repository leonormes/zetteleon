---
aliases: ["Container Primitives SoT", "Linux Container Internals"]
confidence: "5/5"
created: 2025-12-24T12:00:00Z
epistemic: "technical"
last_reviewed: 2025-12-24
modified: 2025-12-28T18:49:17+00:00
purpose: "To define the stable kernel-level mechanisms that enable modern containerisation."
review_interval: "6 months"
see_also: ["[[SoT - Container Isolation (The Namespace Security Model)]]", "[[SoT - Namespacing in Computing]]"]
source_of_truth: []
status: "stable"
tags: ["containers", "docker", "k8s", "kernel", "linux"]
title: SoT - Linux Container Primitives
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

Containers are not first-class objects in the Linux kernel. They are an abstraction created by the combination of several independent kernel primitives designed to isolate processes and manage resources.

## 2. The Trinity of Containerisation

### A. Namespaces (Isolation)

Namespaces provide **isolation** by wrapping global system resources in an abstraction that makes it appear to the processes within the namespace that they have their own isolated instance of the resource.

- **Types:** PID (Processes), Net (Network), Mount (Filesystems), UTS (Hostname), IPC (Inter-process Comm), User (UID/GID).

### B. Control Groups / Cgroups (Resource Management)

Cgroups provide **metering and limiting**. They aggregate sets of processes into hierarchical groups to manage their resource consumption.

- **Functions:** Resource limiting, prioritisation, accounting, and control (freezing).

### C. Security Hardening (Capabilities & Seccomp)

- **Capabilities:** Breaking down "root" privileges into distinct, drop-able bits.
- **Seccomp:** Filtering system calls to reduce the kernel attack surface.

## 3. Relational Logic: Namespaces vs. Cgroups

- **Namespaces** answer the question: *"What can I see?"* (Isolation).
- **Cgroups** answer the question: *"How much can I use?"* (Resource Control).

## 4. Implementation Layers

1. **Low-Level Runtimes (runc, crun):** Directly interact with kernel syscalls (`clone`, `unshare`, `setns`) and `cgroupfs`.
2. **High-Level Runtimes (Docker, Containerd):** Manage image layers and lifecycle.
3. **Orchestrators (Kubernetes):** Use primitives to enforce **Quality of Service (QoS)** and multi-tenancy.
