---
aliases:
- Namespace-Aware FS
- Virtualized /proc
created: 2025-12-23 22:28:46+00:00
last_reviewed: '2025-12-23'
modified: 2026-02-01 15:07:54+00:00
status: stable
tags:
- kernel
- namespace
- procfs
- SoftwareEngineering/Linux
- sysfs
title: SoT - Namespace-Aware Pseudo-Filesystems
type: SoT
updated: null
permalink: llmeon/30-library/so-t/so-t-namespace-aware-pseudo-filesystems
---

## 1. Definitive Statement

> [!definition] Definition
> Namespace-Aware Filesystems are kernel-managed pseudo-filesystems (primarily `procfs` and `sysfs`) that dynamically alter their content based on the Namespace Context of the accessing process. They allow isolated views of resources (PIDs, Network interfaces) even when processes share a common mount namespace.

---

## 2. Core Mechanisms

The kernel achieves namespace awareness through its VFS (Virtual File System) layer and specific driver implementations:

- nsproxy Check: When a process makes a request to `/proc` or `/sys`, the VFS layer checks the process's `struct nsproxy` to determine its namespace memberships.
- Dynamic Translation: The kernel translates the request into a namespace-specific view. For example, a lookup for `/proc/self` will resolve to a different numeric PID directory depending on the process's PID namespace.

---

## 3. Namespace-Specific File Views

Even without a private Mount namespace, the following locations are "Virtualized":

### A. Network Namespace (`/proc/net`)

Files like `/proc/net/tcp` or `/proc/net/dev` reflect the network interfaces and socket states _only_ for the associated network namespace.

### B. PID Namespace (`/proc/[pid]`)

Process-specific directories are visible only if the target process is within the same PID namespace (or a descendant). A process in a child namespace cannot "see" parent processes via `/proc`.

### C. UTS Namespace (`/proc/sys/kernel/hostname`)

The hostname and domainname files reflect the UTS namespace of the accessing process. Changing the hostname in one namespace does not affect the view from another.

---

## 4. The "Leakage" Limitation

While the _content_ of these files is virtualized, their locations are not.

- Problem: If a new PID namespace is created but `/proc` is not remounted, tools like `ps` will still read from the host's `procfs` instance, revealing all host processes.
- The Mandate: For true isolation, a private Mount Namespace is required to mount _new_ instances of these pseudo-filesystems that are anchored to the process's specific namespaces.

---

## 5. Summary

Pseudo-filesystems are the "interfaces" to kernel state. Namespace-awareness ensures that these interfaces respect the boundaries of isolation, provided the filesystem hierarchy itself is correctly partitioned via mount namespaces.