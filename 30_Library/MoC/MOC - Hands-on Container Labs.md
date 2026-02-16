---
aliases: []
created: 2025-10-26T17:16:00Z
last_reviewed: "2026-02-06"
modified: 2026-02-16T09:40:27+00:00
status: "stable"
tags: ["debugging", "hands-on", "lab", "SoftwareEngineering/Containers", "tutorial"]
title: MOC - Hands-on Container Labs
type: "map"
updated: 
---

## Summary

Practical tutorials, debugging scenarios, and hands-on exercises for mastering containerisation. This MOC provides step-by-step guides for building container networks from scratch, troubleshooting common issues, and implementing production-ready solutions.

## Context / Problem

Theoretical knowledge of containers is insufficient without practical experience. This MOC bridges the gap between understanding concepts and being able to implement, debug, and optimize container systems in real-world scenarios.

## Structure

### 🛠️ Building from Scratch

- [[Linux Networking]] - Complete hands-on curriculum/Index.
- [[curriculum for learning Kubernetes networking]] - Comprehensive phase-by-phase build guide.
- [[What is a veth pair]] - Configuring the virtual wires.
- [[What is a Linux bridge]] - Building the software switch.

### 🔍 Debugging Scenarios

- [[Protocol - HIE--NNUH Network Debugging]] - Systematic troubleshooting guide.
- [[SoT - Network Debugging Tools & Patterns]] - Using `tcpdump` and `nsenter`.
- [[Protocol - Legacy Helm Refactoring]] - Debugging configuration drift.

### ⚡ Performance & Optimization

- [[SoT - High-Performance Kubernetes Node Tuning]] - Kernel optimization.
- [[SoT - Network Overhead & MTU]] - Tuning packet sizes for overlay networks.

### 🔒 Security Hardening

- [[SoT - Container Security & Hardening]] - Base principles.
- [[SoT - Linux Container Internals]] - Understanding namespaces to secure them.

## Learning Path

### Beginner Track

1. [[Linux Networking]] - Master the fundamentals
2. [[SoT - Linux Networking Primitives]] - Understand Namespaces and Cgroups
3. [[What is a veth pair]] - Connectivity basics
4. [[What is a Linux bridge]] - Switching basics

### Intermediate Track

1. [[curriculum for learning Kubernetes networking]] - Follow Phases 1-3
2. [[SoT - Kubernetes Networking Model]] - The theory applied
3. [[SoT - Calico CNI Architecture]] - Real-world CNI implementation

### Advanced Track

1. [[SoT - High-Performance Data Structures]] - Understanding data locality
2. [[SoT - Zero Knowledge Architecture]] - Advanced security implementation
3. [[SoT - eBPF Observability]] (Planned)

## Lab Environment Setup

### Prerequisites

- Linux host with root privileges
- Basic networking tools (`ip`, `iptables`, `tcpdump`)
- Container runtime (Docker/containerd) optional
- Kubernetes cluster (minikube/kind) for advanced labs

### Tools Required

```bash
# Network debugging
iproute2, iptables, tcpdump, wireshark
# Process debugging  
strace, lsof, /proc filesystem
# Performance monitoring
perf, bpftrace, sysstat
# Security tools
falco, trivy, grype
```

## Common Debugging Commands

### Network Issues

```bash
# List network namespaces
ip netns list

# Inspect interfaces in namespace
ip netns exec <ns> ip addr show

# Trace packet flow
tcpdump -i any -n host <target>

# Check iptables rules
iptables -t nat -L -n -v
```

### Process Issues

```bash
# List processes in namespace
lsns -t pid

# Check resource limits
cat /proc/<pid>/status

# Monitor system calls
strace -p <pid>
```

## Connections to Other Areas

- [[MOC - Container Networking Model]] - Theory behind the labs
- [[MOC - Linux Container Primitives]] - Kernel features in practice
- [[MOC - Container Runtime & Orchestration]] - Production implementation

## Child Notes

### Existing Tutorials

- [[Linux Networking]]
- [[curriculum for learning Kubernetes networking]]
- [[What is a veth pair]]
- [[What is a Linux bridge]]
- [[SoT - Linux Networking Primitives]]

### Planned/Drafts

- Lab - Build Container Network from Scratch (See Curriculum)
- Lab - Implement Simple CNI Plugin (See Curriculum Phase 2)
