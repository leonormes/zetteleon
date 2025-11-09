---
aliases: []
confidence: 
created: 2025-10-24T15:16:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:27Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [bridge, cni, container, linux, topic/technology/networking, type/mechanism]
title: How to set up a Linux bridge for container networking
type: Mechanism
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - Container Networking Model]]
- Related: [[What is a Linux bridge]], [[What is a veth pair]], [[How Linux bridge learns MAC addresses]], [[How a veth pair connects two network namespaces]]

## Summary

Setting up a Linux bridge for container networking involves creating a virtual switch, attaching veth pair ends to it as ports, assigning IPs to containers and the bridge, and configuring routing to enable multi-container same-node communication and external connectivity.

## Context / Problem

Veth pairs enable point-to-point connectivity between two namespaces, but container environments need a **many-to-many** topology where multiple containers communicate with each other and the host. A Linux bridge solves this by acting as a Layer 2 switch that connects multiple veth pairs into a single broadcast domain, simulating how a physical switch connects multiple devices.

## Mechanism / Details

### Step-by-Step Setup

#### Phase 1: Create the Bridge

```bash
# 1. Create a bridge named v-net-0 (or cni0 in Kubernetes)
ip link add v-net-0 type bridge

# 2. Bring the bridge interface up
ip link set v-net-0 up

# 3. Assign an IP to the bridge (acts as gateway for containers)
ip addr add 10.244.0.1/24 dev v-net-0

# Verify
ip link show v-net-0
ip addr show v-net-0
```

**Bridge IP Purpose**: The bridge IP (10.244.0.1) becomes the default gateway for all containers attached to it.

#### Phase 2: Create and Attach Container Namespaces

```bash
# 1. Create two container namespaces
ip netns add pod-red
ip netns add pod-blue

# 2. Create veth pairs (one pair per container)
ip link add veth-red type veth peer name veth-red-br
ip link add veth-blue type veth peer name veth-blue-br

# 3. Move container ends into namespaces
ip link set veth-red netns pod-red
ip link set veth-blue netns pod-blue

# 4. Attach bridge ends to the bridge
ip link set veth-red-br master v-net-0
ip link set veth-blue-br master v-net-0

# 5. Bring all interfaces up
ip link set veth-red-br up
ip link set veth-blue-br up
ip -n pod-red link set veth-red up
ip -n pod-blue link set veth-blue up
ip -n pod-red link set lo up
ip -n pod-blue link set lo up

# 6. Assign IPs to containers
ip -n pod-red addr add 10.244.0.10/24 dev veth-red
ip -n pod-blue addr add 10.244.0.20/24 dev veth-blue

# 7. Set default gateway in containers
ip -n pod-red route add default via 10.244.0.1
ip -n pod-blue route add default via 10.244.0.1
```

#### Phase 3: Enable External Connectivity

```bash
# 1. Enable IP forwarding (required for routing beyond the bridge)
sysctl -w net.ipv4.ip_forward=1

# 2. Add MASQUERADE rule for container egress
iptables -t nat -A POSTROUTING -s 10.244.0.0/24 ! -d 10.244.0.0/24 -j MASQUERADE

# This allows containers to reach external IPs like 8.8.8.8
```

### Packet Flow: Pod-to-Pod on Same Node

```sh
pod-red (10.244.0.10) pings pod-blue (10.244.0.20)

┌─────────────────────────────────────────────────┐
│ 1. pod-red: Packet created                      │
│    src=10.244.0.10, dst=10.244.0.20             │
│    Routing: 10.244.0.0/24 via veth-red          │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│ 2. Packet enters veth-red                       │
│    Exits veth-red-br on host                    │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│ 3. veth-red-br attached to v-net-0 bridge       │
│    Bridge checks MAC table                      │
│    - If MAC known → Forward to specific port    │
│    - If unknown → Flood to all ports            │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│ 4. Frame forwarded to veth-blue-br              │
│    (MAC learning: bridge now knows pod-blue MAC)│
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│ 5. Packet enters veth-blue-br                   │
│    Exits veth-blue in pod-blue namespace        │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│ 6. pod-blue: Packet received                    │
│    dst=10.244.0.20 matches local IP             │
│    Reply sent back (reverse path)               │
└─────────────────────────────────────────────────┘
```

### Packet Flow: Pod-to-External (e.g., 8.8.8.8)

```sh
1. pod-red: Packet to 8.8.8.8
   ↓ (default route via 10.244.0.1)
2. veth-red → veth-red-br → v-net-0 bridge
   ↓ (bridge forwards to default route)
3. Host routing table: via eth0 (host NIC)
   ↓ (POSTROUTING NAT: MASQUERADE)
4. Packet exits eth0 with src=<node-public-IP>
   ↓
5. Internet router forwards to 8.8.8.8
   ↓ (reply returns to node-public-IP)
6. Conntrack reverses NAT: dst=10.244.0.10
   ↓
7. Packet routed to v-net-0 → veth-red-br → veth-red
   ↓
8. pod-red receives reply
```

### Verification Commands

```bash
# Show bridge configuration
bridge link show
# Output shows which veth interfaces are attached

# View MAC address table (learned via ARP)
bridge fdb show br v-net-0

# Test Pod-to-Pod connectivity
ip netns exec pod-red ping 10.244.0.20

# Test Pod-to-Host connectivity
ip netns exec pod-red ping 10.244.0.1

# Test Pod-to-External connectivity
ip netns exec pod-red ping 8.8.8.8

# Check routing in pod
ip netns exec pod-red ip route
# Should show:
# default via 10.244.0.1 dev veth-red
# 10.244.0.0/24 dev veth-red scope link

# Capture traffic on bridge
tcpdump -i v-net-0 -n icmp
```

## Connections / Implications

### What This Enables

- **Same-node Pod communication**: All Pods on a node form a Layer 2 network
- **Gateway functionality**: Bridge serves as default route for Pods
- **CNI simplicity**: Bridge CNI plugin automates this exact setup
- **Kubernetes `cni0`**: Default bridge created by bridge/flannel CNI plugins

### What Breaks If This Fails

| Issue | Symptom | Debug | Fix |
|-------|---------|-------|-----|
| Bridge interface DOWN | All Pods lose connectivity | `ip link show v-net-0` | `ip link set v-net-0 up` |
| Veth not attached | Pod isolated | `bridge link show` | `ip link set veth-X-br master v-net-0` |
| No bridge IP | Pod cannot route externally | `ip addr show v-net-0` | `ip addr add 10.244.0.1/24 dev v-net-0` |
| IP forwarding disabled | External IPs unreachable | `sysctl net.ipv4.ip_forward` | `sysctl -w net.ipv4.ip_forward=1` |
| No MASQUERADE rule | External IPs unreachable | `iptables -t nat -L POSTROUTING` | Add MASQUERADE rule |

### How It Maps to Kubernetes

**CNI Bridge Plugin Setup:**

```json
{
  "cniVersion": "0.4.0",
  "name": "mynet",
  "type": "bridge",
  "bridge": "cni0",
  "isGateway": true,
  "ipMasq": true,
  "ipam": {
    "type": "host-local",
    "subnet": "10.244.0.0/16"
  }
}
```

**What CNI Does:**

1. Creates `cni0` bridge (if not exists)
2. Creates veth pair per Pod
3. Attaches host-side veth to `cni0`
4. Assigns Pod IP from IPAM
5. Sets default route in Pod to bridge IP
6. Adds MASQUERADE iptables rule

**Result:**

- Every Pod on the node connects to `cni0`
- Pods communicate via Layer 2 switching
- External traffic is MASQUERADE'd

### Architecture Diagram

```sh
┌─────────────────────────────────────────────────┐
│               Host Namespace                    │
│                                                 │
│  ┌─────────────────────────────────────┐        │
│  │        v-net-0 (cni0) Bridge        │        │
│  │        IP: 10.244.0.1/24            │        │
│  └──────┬────────────┬──────────┬──────┘        │
│         │            │          │               │
│    ┌────▼────┐  ┌───▼────┐  ┌──▼────┐          │
│    │veth-red-│  │veth-blue│ │veth-X-│          │
│    │  br     │  │  -br    │ │  br   │          │
│    └────┬────┘  └───┬────┘  └──┬────┘          │
└─────────┼───────────┼──────────┼───────────────┘
          │(veth pair)│          │
┌─────────▼──┐  ┌─────▼───┐  ┌──▼────────┐
│ pod-red NS │  │pod-blue │  │ pod-X NS  │
│ veth-red   │  │veth-blue│  │ veth-X    │
│10.244.0.10 │  │10.244.0.│  │10.244.0.X │
│            │  │   20    │  │           │
└────────────┘  └─────────┘  └───────────┘
```

## Questions / To Explore

- [[How does a Linux bridge learn MAC addresses via ARP?]]
- [[What is the difference between bridge and Calico CNI?]]
- [[How does Flannel use bridges with VXLAN?]]
- [[DEBUG - Bridge exists but Pods cannot communicate]]
- [[What are bridge iptables hooks (br_netfilter)?]]
- [[How to troubleshoot bridge MAC table flooding?]]
