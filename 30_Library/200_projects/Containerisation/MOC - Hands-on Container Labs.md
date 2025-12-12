---
aliases: []
confidence:
created: 2025-10-26T17:16:00Z
epistemic:
last_reviewed:
modified: 2025-12-08T11:11:52Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [debugging, hands-on, lab, topic/technology/containers, tutorial]
title: MOC - Hands-on Container Labs
type: map
uid:
updated:
version: 1
---

## Summary

Practical tutorials, debugging scenarios, and hands-on exercises for mastering containerisation. This MOC provides step-by-step guides for building container networks from scratch, troubleshooting common issues, and implementing production-ready solutions.

## Context / Problem

Theoretical knowledge of containers is insufficient without practical experience. This MOC bridges the gap between understanding concepts and being able to implement, debug, and optimize container systems in real-world scenarios.

## Structure

### 🛠️ Building from Scratch

- **[[Linux Networking]]** - Complete hands-on curriculum
- **Build container network manually** - Step-by-step namespace creation (planned)
- **Implement simple CNI plugin** - Write basic networking code (planned)
- **Create container runtime** - Minimal container implementation (planned)

### 🔍 Debugging Scenarios

- **Pod cannot ping same-node Pods** - veth/bridge issues (planned)
- **Cross-node connectivity failures** - routing/overlay problems (planned)
- **DNS resolution issues** - CoreDNS and local DNS debugging (planned)
- **Service access problems** - kube-proxy and iptables troubleshooting (planned)

### ⚡ Performance & Optimization

- **Network throughput optimization** - Tuning kernel parameters (planned)
- **Memory usage analysis** - Container memory profiling (planned)
- **CPU scheduling optimization** - cgroup tuning techniques (planned)
- **Storage performance tuning** - Volume and filesystem optimization (planned)

### 🔒 Security Hardening

- **Container escape prevention** - Namespace and capability hardening (planned)
- **Network policy implementation** - iptables and eBPF security (planned)
- **Image security scanning** - Vulnerability detection and remediation (planned)
- **Runtime security monitoring** - Falco and security tools (planned)

## Learning Path

### Beginner Track

1. **[[Linux Networking]]** - Master the fundamentals
2. **Network namespace labs** - Isolation exercises
3. **Basic connectivity labs** - veth and bridge setup
4. **Simple troubleshooting** - Common issue resolution

### Intermediate Track

1. **Multi-container networking** - Bridge and routing labs
2. **NAT and egress debugging** - iptables and internet access
3. **Service implementation** - Load balancing exercises
4. **Performance analysis** - Monitoring and optimization

### Advanced Track

1. **CNI plugin development** - Custom networking solutions
2. **Security hardening** - Production security practices
3. **Performance tuning** - Large-scale optimization
4. **Complex debugging** - Multi-layer problem solving

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

- **[[MOC - Container Networking Model]]** - Theory behind the labs
- **[[MOC - Linux Container Primitives]]** - Kernel features in practice
- **[[MOC - Container Runtime & Orchestration]]** - Production implementation

## Child Notes

### Existing Tutorials

- [[Linux Networking]] - Comprehensive hands-on curriculum
- [[How to create and connect network namespaces]]
- [[How a veth pair connects two network namespaces]]
- [[How to set up a Linux bridge for container networking]]
- [[How a packet exits a container via NAT]]

### Planned Debugging Guides

- DEBUG - Pod cannot ping other Pods on same node
- DEBUG - Pod can reach same-node Pods but not cross-node
- DEBUG - Pod cannot resolve DNS names
- DEBUG - Service ClusterIP unreachable from Pods

### Planned Advanced Labs

- Lab - Build Container Network from Scratch
- Lab - Implement Simple CNI Plugin
- Lab - Container Security Hardening
- Lab - Performance Optimization Techniques
- Lab - Multi-node Network Troubleshooting
