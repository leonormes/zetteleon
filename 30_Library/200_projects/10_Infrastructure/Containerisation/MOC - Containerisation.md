---
aliases: []
confidence: "null"
created: 2025-10-26T17:16:00Z
epistemic: "null"
last_reviewed: "null"
modified: 2025-12-30T14:11:46+00:00
purpose: "null"
review_interval: "null"
see_also: []
source_of_truth: []
status: "null"
tags: ["container", "docker", "kubernetes", "topic/technology/containers"]
title: MOC - Containerisation
type: "map"
uid: 
updated: 
version: "1"
---

## Summary

A comprehensive Map of Content for understanding containerisation from Linux fundamentals to Kubernetes orchestration. This MOC organizes container knowledge into logical subtopics: networking fundamentals, Linux primitives, Kubernetes integration, and hands-on learning.

## Context / Problem

Containerisation knowledge is fragmented across multiple domains - Linux kernel features, networking concepts, Kubernetes abstractions, and practical implementation details. Without a structured approach, it's difficult to build a coherent mental model that connects the low-level Linux primitives to high-level container orchestration. This MOC provides a navigable framework for learning and reference.

## Structure

### 🌐 [[MOC - Container Networking Model|Container Networking]]

Deep dive into Linux networking primitives that form the foundation of container networking:

- Network namespaces, veth pairs, bridges, iptables
- Packet flows and NAT mechanisms
- Linux to Kubernetes networking mapping
- Hands-on network building tutorials

### 🔧 [[MOC - Linux Container Primitives|Linux Fundamentals]]

Core Linux kernel features that enable containerisation:

- Process isolation (PID namespaces)
- File system isolation (mount namespaces)
- Network isolation (network namespaces)
- Hostname isolation (UTS namespaces)
- Virtual File System (VFS) abstraction

### ⚙️ [[MOC - Container Runtime & Orchestration|Container Orchestration]]

How containers are managed and orchestrated:

- Container runtime interfaces (CRI, CNI)
- Kubernetes networking components
- Service discovery and load balancing
- Network policies and security

### 🧠 [[MOC - Kernel Internals|Deep Kernel Internals]]

The mechanisms that enforce isolation and resource limits:

- **Cgroups (Control Groups):** Resource limiting (CPU, Memory), prioritization, and accounting. The key to preventing "noisy neighbors."
- **Syscalls:** `clone()` (creates new isolated processes) vs `unshare()` (isolates existing processes).
- **Virtual Switching:** How `veth` pairs and bridges (like `docker0`) act as virtual switches, comparing them to physical switch logic (MAC learning, forwarding).

### 🏗️ [[MOC - Hands-on Container Labs|Practical Implementation]]

Step-by-step tutorials and practical exercises:

- Build container networks from scratch
- Debug common networking issues
- Performance optimization techniques
- Security hardening practices

## Quick Navigation

### For Beginners

1. Start with [[Linux Networking]] for hands-on foundation
2. Progress through [[What is a network namespace]] and related primitives
3. Connect concepts with [[Pods communicate across cluster using CNI-provided networking]] and [[30_Library/200_projects/Containerisation/Containers Within a Pod Share Network Namespace and IP Address]]

### For Kernel Enthusiasts

1. Dive into [[Cgroups and Containerization A Deep Dive]] for resource management.
2. Understand the syscalls: `clone` vs `unshare` in [[netns and advanced containers]].
3. Study **Virtual Switching** logic to see how Linux bridges emulate physical hardware.

### For Kubernetes Practitioners

1. Review [[Model - Linux to Kubernetes Networking Mapping]] for debugging insights
2. Study [[MOC - Container Networking Model]] for deep understanding
3. Follow the end-to-end flow in [[Kubernetes networking components coordinate through a defined workflow]]

### For System Administrators

1. Focus on Linux primitives in [[MOC - Linux Container Primitives]]
2. Master networking with [[MOC - Container Networking Model]]
3. Implement with [[MOC - Hands-on Container Labs]] and consult [[Container Runtime Configures Pod Networking Through CNI Plugins]] for runtime-specific tasks

## Key Insights

- **Container networking is just automated Linux networking** - CNI plugins automate `ip` commands
- **Namespaces provide isolation, veth pairs provide connectivity** - the fundamental pattern
- **Kubernetes abstracts but doesn't hide** - understanding Linux primitives enables better debugging
- **Network policies are iptables rules** - security builds on kernel features
- **Cgroups are the Resource Police** - enforcing limits to ensure Quality of Service (QoS).

## Related Areas

- [[MOC - Kubernetes Architecture]] - broader K8s context

---

## Sub-MOCs

- **[[MOC - Container Networking Model]]** - Linux networking foundations and Kubernetes mapping
- **[[MOC - Linux Container Primitives]]** - Kernel features enabling containers (planned)
- **[[MOC - Container Runtime & Orchestration]]** - Runtime interfaces and orchestration (planned)
- **[[MOC - Hands-on Container Labs]]** - Practical tutorials and debugging guides (planned)

## Core Reference Notes

### Foundational Concepts

- [[30_Library/200_projects/Containerisation/Containers Within a Pod Share Network Namespace and IP Address]] - Pod-level container communication
- [[Pods communicate across cluster using CNI-provided networking]] - Cluster-wide networking
- [[Kubernetes Provides NodePort and LoadBalancer for External Service Access]] - External access patterns
- [[Linux Networking]] - Hands-on learning curriculum
- [[Model - Linux to Kubernetes Networking Mapping]] - Translation table
- [[Cgroups and Containerization A Deep Dive]] - Deep dive into resource management and isolation
- [[netns and advanced containers]] - Practical Q&A on `ip netns`, `veth`, and `clone`/`unshare` syscalls

### Orchestration Components

- [[Container Runtime Configures Pod Networking Through CNI Plugins]] - Runtime networking responsibilities
- [[Kube-Proxy Implements Services Using Iptables or IPVS]] - Service implementation
- [[etcd stores cluster network state and service configuration]] - Cluster state management
- [[Service mesh provides advanced traffic management and security for service communication]] - Advanced service communication
- [[Kubernetes networking components coordinate through a defined workflow]] - Component coordination

### Linux Primitives

- [[What is a network namespace]]
- [[What is a veth pair]]
- [[What is a Linux bridge]]
- [[What is iptables NAT MASQUERADE]]
- [[What is IP forwarding]]
- [[What is a mount namespace]]
- [[What is a PID namespace]]
- [[What is a UTS namespace]]
- [[What is the Linux VFS (Virtual File System)]]

### Mechanisms & How-To

- [[How to create and connect network namespaces]]
- [[How a veth pair connects two network namespaces]]
- [[How to set up a Linux bridge for container networking]]
- [[How a packet exits a container via NAT]]
- [[How namespaces interact without mount namespace]]

### Insights & Analysis

- [[Namespace Isolation Is Incomplete Without Mount Namespace]]
