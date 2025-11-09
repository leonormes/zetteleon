---
aliases: []
confidence: 
created: 2025-10-24T15:12:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:22Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [arp, layer2, protocol, topic/technology/networking, type/fact]
title: What is ARP
type: Factual
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - Container Networking Model]]
- Related: [[What is a Linux bridge]], [[How Linux bridge learns MAC addresses]]

## Summary

ARP (Address Resolution Protocol) is a Layer 2 protocol that maps IP addresses to MAC addresses on a local network, enabling devices to discover the hardware address needed for Ethernet frame delivery.

## Context / Problem

IP packets contain logical IP addresses, but Ethernet frames require physical MAC addresses. When a Pod wants to send a packet to another Pod on the same subnet (same bridge), it needs to resolve the destination IP to a MAC address. ARP provides this translation by broadcasting a "who has this IP?" request and receiving a "I have it, my MAC is X" reply.

## Mechanism / Details

### What Is It

ARP operates at the boundary between Layer 2 (Data Link) and Layer 3 (Network):

- **Purpose**: Resolve IPv4 address → MAC address
- **Scope**: Only works on local network segment (same broadcast domain)
- **Protocol**: RFC 826
- **Replacement**: IPv6 uses NDP (Neighbor Discovery Protocol)

### ARP Message Types

1. **ARP Request** (broadcast)
   - "Who has IP 10.244.0.5? Tell 10.244.0.2"
   - Sent to broadcast MAC: `ff:ff:ff:ff:ff:ff`
   - All devices receive it

2. **ARP Reply** (unicast)
   - "10.244.0.5 is at MAC 52:54:00:12:34:56"
   - Sent directly to requester's MAC
   - Only requester receives it

### ARP Packet Structure

```sh
┌─────────────────────────────────┐
│ Hardware Type (Ethernet = 1)    │
│ Protocol Type (IPv4 = 0x0800)   │
│ Hardware Addr Length (6)        │
│ Protocol Addr Length (4)        │
│ Operation (Request=1, Reply=2)  │
│ Sender MAC Address              │
│ Sender IP Address               │
│ Target MAC Address (0 if req)   │
│ Target IP Address               │
└─────────────────────────────────┘
```

### ARP Cache

Resolved mappings are cached to avoid repeated broadcasts:

```bash
# View ARP cache
ip neigh show
# or
arp -n

# Sample output:
# 10.244.0.5 dev cni0 lladdr 52:54:00:12:34:56 REACHABLE
```

Cache states:

- **REACHABLE**: Recently confirmed
- **STALE**: Not recently used, may be invalid
- **DELAY**: Validity being verified
- **FAILED**: Resolution failed

### Container Networking Example

```bash
# Pod A (10.244.0.2) wants to ping Pod B (10.244.0.5)
# 1. Pod A checks ARP cache for 10.244.0.5
# 2. Cache miss → Send ARP request via veth to cni0 bridge
# 3. Bridge floods ARP request to all attached veth pairs
# 4. Pod B receives request and replies with its MAC
# 5. Bridge learns Pod B's MAC on that port
# 6. Pod A caches the IP→MAC mapping
# 7. Subsequent packets go directly via learned MAC
```

## Connections / Implications

### What This Enables

- **Layer 2 communication**: Enables Ethernet frame delivery between Pods
- **Bridge efficiency**: Bridge learns MACs via ARP replies
- **Same-node Pod connectivity**: Pods discover each other's MACs on `cni0`
- **Gateway resolution**: Pods use ARP to find the bridge's MAC for external routing

### What Breaks If This Fails

- **Pods cannot communicate on same node**: ARP failures prevent frame delivery
- **Bridge flooding**: Without MAC learning (via ARP), bridge floods all traffic
- **Network storms**: ARP broadcast storms can saturate network
- **Cache poisoning**: Malicious ARP replies can hijack traffic

### How It Maps to Kubernetes

- **Pod-to-Pod same-node**: ARP resolves Pod IPs on the `cni0` bridge
- **Pod-to-gateway**: Pod uses ARP to find the bridge's MAC for routing
- **Network policies**: Some CNI plugins inspect ARP to enforce L2 security
- **Cross-node traffic**: No ARP involved (uses overlay tunnels or routing)

### Debugging ARP Issues

```bash
# Capture ARP traffic on bridge
tcpdump -i cni0 -n arp

# Clear ARP cache (force re-resolution)
ip neigh flush dev cni0

# Manually add ARP entry
ip neigh add 10.244.0.5 lladdr 52:54:00:12:34:56 dev cni0
```

## Questions / To Explore

- [[How does the Linux bridge use ARP to learn MAC addresses?]]
- [[What is gratuitous ARP and how is it used in Kubernetes?]]
- [[How does IPv6 NDP differ from ARP?]]
- [[DEBUG - Pods on same node cannot communicate despite bridge setup]]
- [[What is ARP spoofing and how do CNIs prevent it?]]
- [[How does proxy ARP work in container networking?]]
