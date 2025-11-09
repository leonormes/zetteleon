---
aliases: []
confidence: 
created: 2025-10-24T15:07:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [bridge, container, layer2, linux, topic/technology/networking, type/fact]
title: What is a Linux bridge
type: Factual
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - Container Networking Model]]
- Related: [[What is a veth pair]], [[What is ARP]], [[How Linux bridge learns MAC addresses]], [[How to set up a Linux bridge for container networking]]

## Summary

A Linux bridge is a virtual Layer 2 network switch implemented in software that forwards Ethernet frames between connected interfaces based on MAC addresses, enabling multi-container communication on a single host.

## Context / Problem

Veth pairs provide point-to-point connectivity, but containers need to communicate with multiple peers (other containers, the host, external networks). A Linux bridge acts as a virtual switch, allowing multiple veth pairs to connect to a common network segment, just like a physical switch connects multiple devices.

## Mechanism / Details

### What Is It

A Linux bridge is a kernel network device that:

- Operates at **OSI Layer 2** (Data Link)
- Forwards frames based on **MAC addresses**
- Learns MAC-to-port mappings dynamically (like a physical switch)
- Can have an IP address assigned to it (acting as a gateway)
- Connects multiple network interfaces together

### Creating a Bridge

```bash
# Create a bridge
ip link add cni0 type bridge

# Bring it up
ip link set cni0 up

# Assign an IP (optional, for gateway functionality)
ip addr add 10.244.0.1/24 dev cni0

# Attach a veth to the bridge
ip link set veth-abc master cni0
```

### Key Properties

- **MAC learning**: Automatically builds a forwarding table
- **Flooding**: Sends unknown unicast frames to all ports
- **Broadcast domain**: All attached interfaces share the same broadcast domain
- **Transparent**: Invisible to higher-layer protocols
- **STP-capable**: Can run Spanning Tree Protocol (usually disabled in containers)

### Default Bridge in Kubernetes

Most CNI plugins create a bridge named **`cni0`** on each node:

- All Pod veth pairs attach to this bridge
- The bridge itself gets an IP from the node's Pod CIDR
- Acts as the default gateway for Pods on that node

## Connections / Implications

### What This Enables

- **Same-node Pod communication**: All Pods on a node can communicate via the bridge
- **Gateway functionality**: Bridge IP serves as default route for Pods
- **MAC-based forwarding**: Efficient Layer 2 switching without routing overhead
- **CNI simplicity**: Bridge plugin is one of the simplest CNI implementations

### What Breaks If This Fails

- If bridge interface is down, all Pods lose connectivity
- If MAC table overflows, bridge floods all traffic (performance degradation)
- If bridge has no IP, Pods cannot route beyond the local node
- Misconfigured bridge (wrong CIDR) causes IP conflicts

### How It Maps to Kubernetes

- **`cni0` bridge**: Default bridge created by bridge CNI plugin
- **Pod veth interfaces**: Attached as ports on the bridge
- **Node IP**: Assigned to the bridge for gateway functionality
- **iptables integration**: Rules reference bridge interfaces for SNAT/DNAT

### Real-World Inspection

```bash
# List bridges
ip link show type bridge

# Show interfaces attached to bridge
bridge link show

# View MAC address table
bridge fdb show br cni0
```

## Questions / To Explore

- How does a Linux bridge learn MAC addresses?
- How does a bridge handle broadcast and multicast traffic?
- What is the difference between a bridge and a switch?
- How does the bridge CNI plugin differ from Calico or Flannel?
- DEBUG - Bridge exists but Pods cannot communicate
- What are bridge iptables hooks (br_netfilter)?
