---
aliases: []
confidence: "null"
created: 2025-10-26T17:22:00Z
epistemic: "null"
last_reviewed: "null"
modified: 2025-12-31T23:08:48+00:00
purpose: "null"
review_interval: "null"
see_also: []
source_of_truth: []
status: "null"
tags: ["cni", "container-runtime", "kubelet", "topic/technology/containers", "topic/technology/kubernetes", "topic/technology/networking"]
title: Container Runtime Configures Pod Networking Through CNI Plugins
type: "Fact"
uid: 
updated: 
version: "1"
---

## Summary

The container runtime is responsible for managing container lifecycle and coordinates with CNI plugins to configure pod networking, including network namespace creation, IP address assignment, and interface setup.

## Details

### Container Runtime Responsibilities

- **Lifecycle Management**: Manages creation, start, stop, and deletion of containers
- **Network Coordination**: Interacts with CNI plugins when pods are created
- **Configuration**: Sets up network namespace, assigns IP addresses, configures interfaces
- **Notification**: Notifies kubelet when containers are ready for network configuration

### Network Configuration Process

1. **Pod Creation**: kubelet instructs container runtime to create containers
2. **Container Startup**: Runtime starts containers within the pod
3. **Readiness Notification**: Runtime notifies kubelet that containers are ready
4. **CNI Invocation**: kubelet invokes CNI plugin to configure pod network
5. **Network Setup**: CNI plugin assigns IP, sets up interfaces, configures routing

### Key Interactions

- **With kubelet**: Receives pod creation instructions, reports container status
- **With CNI Plugins**: Provides container context for network configuration
- **With Kernel**: Creates and manages network namespaces at kernel level

## Runtime Examples

- **containerd**: Default runtime in modern Kubernetes
- **CRI-O**: Lightweight runtime focused on Kubernetes
- **Docker**: Legacy runtime with CRI shim

## Related

- [[Pods communicate across cluster using CNI-provided networking]] - CNI plugin role
- [[MOC - Container Runtime & Orchestration]] - Runtime in orchestration context
