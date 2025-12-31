---
aliases: ["Container Internals", "Linux Container Primitives", "Namespace Architecture", "The Trinity of Containerisation"]
confidence: "5/5"
created: 2025-12-24T12:00:00Z
epistemic: "technical"
last_reviewed: "2025-12-30"
modified: 2025-12-31T23:08:35+00:00
purpose: "To define the definitive kernel-level mechanisms (Namespaces, Cgroups, Layered Filesystems) that enable modern containerisation."
review_interval: "6 months"
see_also: ["[[SoT - Container Security & Hardening]]", "[[SoT - Namespacing in Computing]]", "[[SoT - Kubernetes Cluster State Architecture]]"]
source_of_truth: []
status: "stable"
tags: ["containers", "docker", "k8s", "kernel", "linux", "systems_engineering"]
title: SoT - Linux Container Internals
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> "Containers" do not exist in the Linux kernel. They are a user-space abstraction created by the coordinated application of three independent kernel primitives:
> 1.  **Namespaces** (Isolation: "What can I see?")
> 2.  **Cgroups** (Resource Control: "How much can I use?")
> 3.  **Union Filesystems** (Distribution: "What creates my reality?")

A container is simply a process with a restricted view of the system.

---

## 2. The Trinity of Containerisation

### A. Namespaces (Isolation)

Namespaces wrap global system resources in an abstraction, making them appear private to the process.

| Namespace | Resource Isolated | Security Impact (If Missing) |
|:--- |:--- |:--- |
| **PID** | Process IDs | Low. Process visibility only. |
| **Network** | Interfaces, Ports | Medium. Can sniff/spoof host traffic. |
| **Mount** | **Filesystem** | **CRITICAL. Zero isolation.** (See Section 3). |
| **UTS** | Hostname | Low. Confusion in logs. |
| **IPC** | Message Queues | Low. Inter-process communication leaks. |
| **User** | UID/GID | High. Root in container = Root on host. |

### B. Control Groups / Cgroups (Resource Management)

Cgroups provide **metering and limiting**. They aggregate sets of processes into hierarchical groups.

- **Functions:** Resource limiting (CPU/RAM quotas), prioritisation (CPU shares), accounting (billing/monitoring), and control (freezing/pausing processes).

### C. Security Hardening (Capabilities & Seccomp)

The kernel provides mechanisms to restrict the "Superuser" power even for root processes.

- **Capabilities:** Breaking down "root" privileges into distinct, droppable bits (e.g., `CAP_NET_BIND_SERVICE`).
- **Seccomp (Secure Computing Mode):** A firewall for system calls. It filters what calls a process can make to the kernel, reducing the attack surface.

---

## 3. The Security Boundary: Mount Namespace as Gatekeeper

> [!warning] The Isolation Fallacy
> Creating Network, PID, and UTS namespaces without a **Mount Namespace** creates a dangerous state of **"Decoupled Identity."**

- **The Mechanism:** The security boundary is defined by the **Mount Namespace** in conjunction with **Pivot Root**.
    1. **Clone:** Create process with `CLONE_NEWNS`.
    2. **Pivot Root:** Switch the root filesystem (`/`) to the container image.
    3. **Unmount:** Detach the old root so the host filesystem is mathematically unreachable.
- **Without this sequence:** The process retains full read/write access to the host filesystem. It is merely a process with a mask.

---

## 4. The Runtime Abstraction Layer

Kernel primitives are too low-level for application development. **Container Runtimes** bridge this gap.

### The Standard Stack (OCI)

1. **Orchestrator (Kubernetes):** Manages the fleet. "Schedule this Pod."
2. **High-Level Runtime (containerd / CRI-O):** Manages the image lifecycle. Pulls images, unpacks layers, creates network interfaces.
3. **Low-Level Runtime (runc / crun):** The "Engine." It talks to the kernel to spawn the process, sets up the namespaces/cgroups, applies the Seccomp profile, and hands over control.

---

## 5. Related Components

- [[SoT - Container Security & Hardening]] - Tactical guide for securing this architecture.
- [[SoT - Kubernetes Cluster State Architecture]] - How these primitives are orchestrated.
- [[SoT - Namespacing in Computing]] - General theory of namespacing.
