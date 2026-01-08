---
aliases: ["Container Primitives MOC", "Linux Primitives Map"]
confidence: "5/5"
created: 2025-10-26T17:16:00Z
epistemic: "technical"
last_reviewed: 2025-12-24
modified: 2026-01-08T15:03:29+00:00
purpose: "Map of Content for Linux kernel primitives enabling containers."
review_interval: "1 year"
see_also: ["[[SoT - Linux Container Primitives]]"]
source_of_truth: ["[[SoT - Linux Container Primitives]]"]
status: "stable"
tags: ["kernel", "SoftwareEngineering/Containers", "SoftwareEngineering/Linux", "type/moc"]
title: MOC - Linux Container Primitives
type: "map"
uid: 
updated: 
---

## 🏛️ Foundational Principles

- [[SoT - Linux Container Primitives]] (Source of Truth)
- [[SoT - Process Execution (Kernel Logic)]]
- [[SoT - Namespacing in Computing]]
- [[SoT - Container Isolation (The Namespace Security Model)]]

## 🔒 Isolation (Namespaces)

- [[What is a network namespace]]
- [[What is a mount namespace]]
- [[What is a PID namespace]]
- [[What is a UTS namespace]]
- [[What is the Linux VFS (Virtual File System)]]

## ⚡ Resource Management (Cgroups)

- [[Cgroups Limit and Manage Container Resources]]
- [[Cgroups v2 Unified Hierarchy]]
- [[Namespace Isolation Is Incomplete Without Mount Namespace]]

## 🔐 Security Hardening

- [[SoT - Container Security & Hardening]] (Best Practices)
- [[SoT - Container Isolation (The Namespace Security Model)]]
- Linux Capabilities (Planned)
- Seccomp Profiles (Planned)

---

**Related:** [[Networking MOC]], [[Cloud Networking MOC]]
