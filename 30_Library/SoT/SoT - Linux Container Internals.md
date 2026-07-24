---
conformant: false
created: 2025-12-24T12:00:00+00:00
modified: 2026-07-20T16:33:47+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-linux-container-internals
tags: []
title: SoT - Linux Container Internals
type: sot
---

## 1. Definitive Statement

> [!definition] Definition
> "Containers" do not exist in the Linux kernel. They are a user-space abstraction created by the coordinated application of three independent kernel primitives:
>
> 1.  Namespaces (Isolation: "What can I see?")
> 2.  Cgroups (Resource Control: "How much can I use?")
> 3.  Union Filesystems (Distribution: "What creates my reality?")

A container is simply a process with a restricted view of the system.

---

## 2. The Trinity of Containerisation

### A. Namespaces (Isolation)

Namespaces wrap global system resources in an abstraction, making them appear private to the process.

| Namespace | Resource Isolated | Security Impact (If Missing)               |
|:-------- |:---------------- |:----------------------------------------- |
| PID       | Process IDs       | Low. Process visibility only.              |
| Network   | Interfaces, Ports | Medium. Can sniff/spoof host traffic.      |
| Mount     | Filesystem        | CRITICAL. Zero isolation. (See Section 3). |
| UTS       | Hostname          | Low. Confusion in logs.                    |
| IPC       | Message Queues    | Low. Inter-process communication leaks.    |
| User      | UID/GID           | High. Root in container = Root on host.    |

### B. Control Groups / Cgroups (Resource Management)

Cgroups provide metering and limiting. They aggregate sets of processes into hierarchical groups.

- Functions: Resource limiting (CPU/RAM quotas), prioritisation (CPU shares), accounting (billing/monitoring), and control (freezing/pausing processes).

### C. Security Hardening (Capabilities & Seccomp)

The kernel provides mechanisms to restrict the "Superuser" power even for root processes.

- Capabilities: Breaking down "root" privileges into distinct, droppable bits (e.g., `CAP_NET_BIND_SERVICE`).
- Seccomp (Secure Computing Mode): A firewall for system calls. It filters what calls a process can make to the kernel, reducing the attack surface.

---

## 3. The Security Boundary: Mount Namespace as Gatekeeper

> [!warning] The Isolation Fallacy
> Creating Network, PID, and UTS namespaces without a Mount Namespace creates a dangerous state of "Decoupled Identity."

- The Mechanism: The security boundary is defined by the Mount Namespace in conjunction with Pivot Root.
  1. Clone: Create process with `CLONE_NEWNS`.
  2. Pivot Root: Switch the root filesystem (`/`) to the container image.
  3. Unmount: Detach the old root so the host filesystem is mathematically unreachable.
- Without this sequence: The process retains full read/write access to the host filesystem. It is merely a process with a mask.

---

## 4. The Runtime Abstraction Layer

Kernel primitives are too low-level for application development. Container Runtimes bridge this gap.

### The Standard Stack (OCI)

1. Orchestrator (Kubernetes): Manages the fleet. "Schedule this Pod."
2. High-Level Runtime (containerd / CRI-O): Manages the image lifecycle. Pulls images, unpacks layers, creates network interfaces.
3. Low-Level Runtime (runc / crun): The "Engine." It talks to the kernel to spawn the process, sets up the namespaces/cgroups, applies the Seccomp profile, and hands over control.

---

## 5. Related Components

- [[SoT - Container Security & Hardening]] - Tactical guide for securing this architecture.
- [[SoT - Kubernetes Cluster State Architecture]] - How these primitives are orchestrated.
- [[SoT - Namespacing in Computing]] - General theory of namespacing.

---

## 6. Isolation Primitives (Knowledge-Graph Nodes)

> These are addressable graph nodes per [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]. Each `content-block` defines one isolation concept as the authoritative target for edges emitted elsewhere — notably the per-namespace blocks in [[linux-namespaces]], which `implement`/`synthesize` these concepts. Validated by `10_System/scripts/edge_lint.py`.

<!--content-block-start type="concept" id="namespace-isolation"-->

**Namespace isolation** — the general capability by which a namespace wraps a global kernel resource so a process sees a private instance of it ("what can I see?", §2A). The specific isolation types below each specialise it; [[linux-namespaces]]'s `namespace-integration` block `synthesizes` this node.

<!--content-block-end-->

<!--content-block-start type="concept" id="filesystem-isolation"-->

%%concept.extends{namespace-isolation}%%

**Filesystem isolation** — an independent mount tree and root filesystem, realised by the Mount namespace with `pivot_root` and detachment of the old root (§3). Implemented by [[linux-namespaces]]'s `mount-namespace` block.

<!--content-block-end-->

<!--content-block-start type="concept" id="network-isolation"-->

%%concept.extends{namespace-isolation}%%

**Network isolation** — a private network stack: interfaces, IP addresses, port ranges, routing tables, and a dedicated loopback (§2A). Synthesized by [[linux-namespaces]]'s `network-namespace` block.

<!--content-block-end-->

<!--content-block-start type="concept" id="process-tree-isolation"-->

%%concept.extends{namespace-isolation}%%

**Process-tree isolation** — an independent PID space in which the container owns its own PID 1 and cannot see host or sibling processes (§2A). Implemented by [[linux-namespaces]]'s `pid-namespace` block.

<!--content-block-end-->

<!--content-block-start type="concept" id="hostname-isolation"-->

%%concept.extends{namespace-isolation}%%

**Hostname isolation** — a distinct hostname and NIS domain via the UTS namespace, decoupling container identity from the host (§2A). Implemented by [[linux-namespaces]]'s `uts-namespace` block.

<!--content-block-end-->

<!--content-block-start type="concept" id="ipc-isolation"-->

%%concept.extends{namespace-isolation}%%

**IPC isolation** — a private set of System V IPC objects and POSIX message queues (shared memory, semaphores), preventing cross-container IPC leakage (§2A). Implemented by [[linux-namespaces]]'s `ipc-namespace` block.

<!--content-block-end-->

<!--content-block-start type="concept" id="system-isolation"-->

%%concept.synthesizes{namespace-isolation}%%

%%concept.synthesizes{namespace-integration}%%

**System isolation** — the emergent, container-grade isolation produced by coordinating every namespace type together with cgroups and union filesystems (§1, "a process with a restricted view of the system"). This is the abstract goal that [[linux-namespaces]]'s `containerization-implementation` block `implements`.

<!--content-block-end-->

