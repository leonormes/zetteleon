---
aliases: []
created: 2025-10-26T17:16:00Z
last_reviewed: "2026-04-08"
modified: 2026-04-08T17:59:03+00:00
status: "growing"
tags: ["docker", "kubernetes", "SoftwareEngineering/Containers"]
title: MOC - Containerisation
type: "map"
updated: 
---

## Summary

A comprehensive Map of Content for understanding containerisation from Linux fundamentals to Kubernetes orchestration. This MOC organises container knowledge into logical subtopics: networking fundamentals, Linux primitives, Kubernetes integration, and hands-on learning.

## Context / Problem

Containerisation knowledge is fragmented across multiple domains—Linux kernel features, networking concepts, Kubernetes abstractions, and practical implementation details. Without a structured approach, it's difficult to build a coherent mental model that connects the low-level Linux primitives to high-level container orchestration. This MOC provides a navigable framework for learning and reference.

## Structure

### 🌐 [[MOC - Container Networking Model|Container Networking]]

Deep dive into Linux networking primitives that form the foundation of container networking:

- Network namespaces, veth pairs, bridges, iptables
- Packet flows and NAT mechanisms
- Linux to Kubernetes networking mapping
- Hands-on network building tutorials

### 🔧 [[MOC - Linux Container Primitives|Linux Fundamentals & Kernel Internals]]

Core Linux kernel features that enable containerisation—namespaces, cgroups, syscalls, and virtual switching:

- Process isolation (PID namespaces)
- File system isolation (mount namespaces)
- Network isolation (network namespaces)
- Hostname isolation (UTS namespaces)
- Virtual File System (VFS) abstraction
- Cgroups (Control Groups): CPU/memory limits—the "Resource Police"
- Syscalls: `clone()` vs `unshare()` for process isolation
- Virtual Switching: veth pairs and bridges acting as virtual switches

### ⚙️ [[MOC - Container Runtime & Orchestration|Container Orchestration]]

How containers are managed and orchestrated:

- Container runtime interfaces (CRI, CNI)
- Kubernetes networking components
- Service discovery and load balancing
- Network policies and security

### 🏗️ [[MOC - Hands-on Container Labs|Practical Implementation]]

Step-by-step tutorials and practical exercises:

- Build container networks from scratch
- Debug common networking issues
- Performance optimisation techniques
- Security hardening practices

## Quick Navigation

### For Beginners

1. Start with [[Linux Networking]] for a hands-on foundation
2. Progress to [[MOC - Linux Container Primitives]] for namespace and cgroup primitives
3. Connect concepts with [[Kubernetes networking components coordinate through a defined workflow]]

### For Kernel Enthusiasts

1. Dive into [[Cgroups Limit and Manage Container Resources]] for resource management
2. Explore [[MOC - Linux Container Primitives]] for `clone` vs `unshare` syscalls and virtual switching
3. Study [[MOC - Container Networking Model]] to see how Linux bridges emulate physical hardware

### For Kubernetes Practitioners

1. Review [[MOC - Container Networking Model]] for the Linux-to-Kubernetes mapping table and debugging insights
2. Follow the end-to-end flow in [[Kubernetes networking components coordinate through a defined workflow]]
3. Study [[MOC - Container Networking Model]] for CNI plugin architecture

### For System Administrators

1. Focus on Linux primitives in [[MOC - Linux Container Primitives]]
2. Master networking with [[MOC - Container Networking Model]]
3. Implement with [[MOC - Hands-on Container Labs]] and consult [[Container Runtime Configures Pod Networking Through CNI Plugins]] for runtime-specific tasks

## Key Insights

- Container networking is just automated Linux networking—CNI plugins automate `ip` commands
- Namespaces provide isolation, veth pairs provide connectivity—the fundamental pattern
- Kubernetes abstracts but doesn't hide—understanding Linux primitives enables better debugging
- Network policies are iptables rules—security builds on kernel features
- Cgroups are the Resource Police—enforcing limits to ensure Quality of Service (QoS)

## Related Areas

- [[MOC - Kubernetes Architecture]]—broader K8s context

---

## Sub-MOCs

- [[MOC - Container Networking Model]]—Linux networking foundations and Kubernetes mapping
- [[MOC - Linux Container Primitives]]—Kernel features enabling containers (namespaces, cgroups, syscalls)
- [[MOC - Container Runtime & Orchestration]]—Runtime interfaces and orchestration
- [[MOC - Hands-on Container Labs]]—Practical tutorials and debugging guides

## Source of Truth Notes

> These SoT notes are the canonical source for individual concepts—the atomic notes below are entry points to specific sub-topics.

- [[SoT - Linux Networking Primitives]]—Veth, Bridge, IPTables, IP Forwarding, network namespaces
- [[SoT - Kubernetes Networking & DNS]]—Services, Ingress, CNI, CoreDNS, kube-proxy

## Core Reference Notes

### Foundational Concepts

- [[Linux Networking]]—Hands-on learning curriculum
- [[MOC - Container Networking Model]]—Linux-to-Kubernetes mapping table
- [[Cgroups Limit and Manage Container Resources]]—Resource management and isolation deep dive

### Orchestration Components

- [[Container Runtime Configures Pod Networking Through CNI Plugins]]—Runtime networking responsibilities
- [[Kube-Proxy Implements Services Using Iptables or IPVS]]—Service implementation
- [[etcd stores cluster network state and service configuration]]—Cluster state management
- [[Kubernetes networking components coordinate through a defined workflow]]—Component coordination
- [[Kubernetes Provides NodePort and LoadBalancer for External Service Access]]—External access patterns

### Linux Primitives (Atomic Notes)

- [[What is a veth pair]]
- [[What is a Linux bridge]]
- [[What is a mount namespace]]
- [[What is the Linux VFS (Virtual File System)]]

> Note: `What is a network namespace`, `What is a PID namespace`, `What is a UTS namespace`, `What is iptables NAT MASQUERADE`, and `What is IP forwarding` have been absorbed into [[SoT - Linux Networking Primitives]] and [[MOC - Linux Container Primitives]].

### Mechanisms & How-To

> Hands-on procedures (creating network namespaces, connecting veth pairs, configuring bridges, tracing NAT flows) are covered in [[Linux Networking]] and [[SoT - Linux Networking Primitives]].
