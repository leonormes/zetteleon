---
aliases: []
confidence: 
created: 2025-10-24T15:05:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [container, linux, namespace, topic/technology/networking, type/fact]
title: What is a network namespace
type: Factual
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - Container Networking Model]]
- Related: [[What is a veth pair]], [[How to create and connect network namespaces]]

## Summary

A network namespace is an isolated copy of the Linux network stack, providing each container with its own independent set of network interfaces, IP addresses, routing tables, and iptables rules.

## Context / Problem

Containers need network isolation to prevent conflicts (e.g., multiple containers binding to port 80) and to enable security boundaries. Without network namespaces, all processes would share the same network configuration, making multi-tenant container systems impossible.

## Mechanism / Details

A network namespace contains:

- **Network interfaces** (lo, eth0, etc.) - separate from the host
- **IP addresses** - assigned independently per namespace
- **Routing tables** - each namespace has its own routing decisions
- **iptables rules** - firewall rules are namespace-specific
- **Network statistics** - counters and metrics isolated per namespace

### Creating a Network Namespace

```bash
# Create namespace
ip netns add pod-red

# List namespaces
ip netns list

# Execute command in namespace
ip netns exec pod-red ip addr show
```

When created, a namespace starts with only a loopback interface (`lo`), which is down by default.

### The Root Namespace

The host system operates in the "root" namespace—the default network context comparable to a Kubernetes node's network namespace. All containers/Pods run in child namespaces created from the root.

## Connections / Implications

### What This Enables

- **Container isolation**: Each Pod gets its own IP and can bind to any port without conflicts
- **Multi-tenancy**: Different applications can coexist with identical network configs
- **Security boundaries**: Network policies can enforce isolation between namespaces
- **Kubernetes Pods**: kubelet creates a network namespace for each Pod

### What Breaks If This Fails

- If namespace creation fails, the Pod cannot start (CrashLoopBackOff)
- If namespace is accidentally deleted, the Pod loses all network connectivity
- Pods sharing a namespace (hostNetwork: true) lose isolation and can conflict

### How It Maps to Kubernetes

- Each Kubernetes Pod runs in its own network namespace
- `kubectl exec` uses `nsenter` to enter the Pod's network namespace
- CNI plugins create and configure the namespace during Pod creation
- The pause container holds the namespace open for other containers in the Pod

## Questions / To Explore

- [[How does kubelet create network namespaces for Pods?]]
- [[What is the pause container in Kubernetes?]]
- [[How are network namespaces mounted in /var/run/netns?]]
- [[What happens to network namespaces when a Pod is deleted?]]
- [[How do you debug inside a network namespace?]]
