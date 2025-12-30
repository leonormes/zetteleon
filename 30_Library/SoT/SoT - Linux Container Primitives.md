---
aliases: ["Container Primitives SoT", "Linux Container Internals"]
confidence: "5/5"
created: 2025-12-24T12:00:00Z
epistemic: "technical"
last_reviewed: 2025-12-24
modified: 2025-12-30T14:11:34+00:00
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

## 4. The Runtime Abstraction Layer

While kernel primitives provide the raw capabilities, they are too low-level for practical application development. **Container Runtimes** bridge this gap.

### Why Runtimes are Essential (The Missing Link)

1. **Complexity Abstraction:** Manually configuring namespaces, cgroups, and capabilities for every process is error-prone. Runtimes automate this via declarative configs (OCI Spec).
2. **Lifecycle Management:** Kernel primitives do not know about "starting", "stopping", or "pulling" containers. Runtimes manage this state machine.
3. **Image Management:** The kernel understands filesystems, not "images." Runtimes handle the pulling, unpacking, and layering (OverlayFS) of OCI images from registries.
4. **Standardization:** Runtimes adhere to **OCI (Open Container Initiative)** standards, ensuring that a container built with one tool runs on any compliant platform.

### Runtime Architecture

1. **Low-Level Runtimes (runc, crun, Kata):**
    - **Scope:** The mechanical interface to the kernel.
    - **Responsibility:** Spawns the process, sets up namespaces/cgroups, applies security profiles (Seccomp/AppArmor), and hands over control.
    - **Analogy:** The "Engine" that turns the gears.

2. **High-Level Runtimes (containerd, CRI-O):**
    - **Scope:** The manager of the container ecosystem.
    - **Responsibility:** Image transport (pull/push), storage management (unpacking layers), network interface creation (CNI invocation), and supervision of low-level runtimes.
    - **Analogy:** The "Property Manager" that handles tenants and maintenance.

3. **Orchestrators (Kubernetes):**
    - **Scope:** Multi-node fleet management.
    - **Responsibility:** Scheduling, scaling, self-healing, and networking *across* hosts using the underlying runtimes via the **CRI (Container Runtime Interface)**.
