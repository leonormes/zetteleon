---
aliases: []
confidence: 
created: 2025-10-24T15:06:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [container, linux, topic/technology/networking, type/fact, veth]
title: What is a veth pair
type: Factual
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - Container Networking Model]]
- Related: [[What is a network namespace]], [[What is a Linux bridge]], [[How a veth pair connects two network namespaces]]

## Summary

A veth (virtual Ethernet) pair is a virtual network cable with two ends that can exist in different network namespaces, acting as a point-to-point link for container networking.

## Context / Problem

Network namespaces are isolated—by default, they cannot communicate with each other or the host. Veth pairs solve this by creating a bidirectional pipe: packets sent into one end immediately appear at the other end, even across namespace boundaries.

## Mechanism / Details

### Anatomy of a Veth Pair

A veth pair consists of two virtual network interfaces that are **paired**:

- Packets entering one interface exit the other
- Works like a virtual Ethernet cable
- Each end can be placed in a different network namespace
- Operates at Layer 2 (Data Link layer)

### Creating a Veth Pair

```bash
# Create a veth pair
ip link add veth-red type veth peer name veth-blue

# Move one end to a namespace
ip link set veth-red netns pod-red

# Assign IP and bring up
ip -n pod-red addr add 10.0.1.1/24 dev veth-red
ip -n pod-red link set veth-red up
```

### Properties

- **Bidirectional**: Full duplex communication
- **Stateless**: No connection tracking or protocol awareness
- **MAC addresses**: Each end has its own MAC address
- **MTU**: Can be configured independently per end
- **Always paired**: Deleting one end automatically deletes the other

## Connections / Implications

### What This Enables

- **Pod-to-Node connectivity**: One end in Pod namespace, one end on host/bridge
- **Pod-to-Pod communication**: When both ends connect via a bridge
- **Container isolation traversal**: Controlled communication between isolated namespaces
- **CNI plugin implementation**: Core primitive used by all CNI plugins

### What Breaks If This Fails

- If veth creation fails, Pod networking cannot initialize
- If one end is down, the pair is non-functional (packets dropped)
- If the veth pair is deleted, the Pod immediately loses connectivity
- Misconfigured MTU causes packet fragmentation and performance issues

### How It Maps to Kubernetes

- **Pod `eth0`**: One end of the veth pair (inside Pod namespace)
- **Host-side veth**: Other end attached to `cni0` bridge or routing table
- Named like `veth<random>` on the host
- CNI plugins create the veth pair during Pod ADD operation

### Real-World Example

Inspecting a running Pod's veth pair:

```bash
# On the host, find the Pod's veth
ip link show | grep veth

# Inside the Pod
kubectl exec -it pod-name -- ip link show
# Shows eth0, which is the other end of the veth pair
```

## Questions / To Explore

- [[How does a CNI plugin create and wire veth pairs?]]
- [[How do you identify which veth belongs to which Pod?]]
- [[What happens if both ends of a veth pair are in the same namespace?]]
- [[How does veth differ from macvlan or ipvlan?]]
- [[DEBUG - Veth pair exists but Pod has no connectivity]]
