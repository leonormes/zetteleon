---
aliases: []
confidence: 
created: 2025-10-24T15:20:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:22Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [model, osi, protocol, topic/technology/networking, type/model]
title: MOC - OSI Model
type: map
uid: 
updated: 
version:
---

## Summary

The OSI Model Map of Content—a comprehensive guide to understanding networking as hierarchical data transformation across seven layers, from raw physical transmission to human-readable applications.

## Context / Problem

Networking involves complex interactions across hardware, protocols, and software. The OSI model provides a universal framework for:

- **Troubleshooting**: Isolating failures by layer ("Is this a Layer 2 or Layer 3 problem?")
- **Design**: Separating concerns (routing decisions independent of physical media)
- **Communication**: Common language for engineers, vendors, and operators

## Model

### The Seven Layer Stack

```sh
┌─────────────────────────────────────────────────┐
│  7  │ Application │ HTTP, DNS, SSH           │
├─────┼─────────────┼──────────────────────────┤
│  6  │ Presentation│ TLS, JSON, JPEG          │
├─────┼─────────────┼──────────────────────────┤
│  5  │ Session     │ NetBIOS, RPC             │
├─────┼─────────────┼──────────────────────────┤
│  4  │ Transport   │ TCP, UDP                 │
├─────┼─────────────┼──────────────────────────┤
│  3  │ Network     │ IP, ICMP, Routing        │
├─────┼─────────────┼──────────────────────────┤
│  2  │ Data Link   │ Ethernet, ARP, Bridges   │
├─────┼─────────────┼──────────────────────────┤
│  1  │ Physical    │ Cables, NICs, WiFi       │
└─────┴─────────────┴──────────────────────────┘
```

### Core Concept: Data as Payload

Each layer treats everything above it as **opaque data** (payload):

- Layer 4 doesn't know if payload is HTTP or DNS—just delivers to port
- Layer 3 doesn't know if payload is TCP or UDP—just routes to IP
- Layer 2 doesn't care about IP—just forwards frames by MAC

This abstraction enables **modularity**: swap HTTP for gRPC without changing TCP, or swap Ethernet for WiFi without changing IP.

### OSI in Container Networking

| Layer | Container Context | Example |
|-------|-------------------|------|
| **7** | Application protocols in Pods | HTTP requests, gRPC calls |
| **6** | TLS encryption for Services | Istio mTLS, cert-manager |
| **5** | Session management (rare in containers) | Persistent connections |
| **4** | TCP/UDP between Pods | Service ports, NodePort |
| **3** | Pod IPs, routing, NAT | kube-proxy DNAT, MASQUERADE |
| **2** | veth pairs, bridges, MAC learning | `cni0` bridge, ARP on bridge |
| **1** | Host NICs | eth0, physical cables |

### Cross-Cutting Concerns

**Encapsulation** ([[How OSI layers encapsulate data in a packet trace]]):  
Each layer adds a header wrapping the payload from above. Decapsulation reverses this process.

**Error Detection**:  

- Layer 2: CRC (Ethernet FCS)  
- Layer 3: IP checksum  
- Layer 4: TCP checksum  

**Addressing**:  

- Layer 2: MAC addresses (local segment)  
- Layer 3: IP addresses (global routing)  
- Layer 4: Ports (application multiplexing)  

## Connections / Implications

### What This Enables

- **Layered troubleshooting**: "Ping works (L3) but HTTP fails (L7)" narrows debugging scope
- **Protocol independence**: Run IPv6 over the same Ethernet (L2) that carried IPv4
- **Tool selection**: tcpdump for L2-L4, curl/nc for L7
- **CNI design**: Plugins operate at L2 (bridges) and L3 (routing)

### What Breaks If Layers Fail

| Failed Layer | Observable Symptom | Debug Tool |
|--------------|--------------------|-----------|
| L1 | No link light, `NO-CARRIER` | `ip link`, physical inspection |
| L2 | ARP fails, MAC conflicts | `bridge fdb show`, `arp -n` |
| L3 | Ping fails, routing loops | `ip route`, `traceroute` |
| L4 | Connection refused, timeouts | `netstat`, `ss -tuln` |
| L7 | HTTP 500, DNS NXDOMAIN | `curl -v`, `dig` |

### How It Maps to Kubernetes

**kube-proxy operates at Layers 3 & 4:**

- Modifies IP headers (DNAT for Services)
- Routes based on TCP/UDP ports

**CNI plugins operate at Layers 2 & 3:**

- Create veth pairs (L2)
- Assign IPs and configure routes (L3)
- Some (Calico) skip L2 and do pure L3 routing

**Service Mesh (Istio/Linkerd) operates at Layer 7:**

- Inspects HTTP headers, gRPC methods
- Implements retries, circuit breaking
- Enforces mTLS (Layer 6)

## Child Notes

### Factual

- What is the OSI model - Definition and layer descriptions

### Mechanisms

- How OSI layers encapsulate data in a packet trace - Step-by-step encapsulation/decapsulation
- Show a minimal end-to-end example of data encapsulation - Real HTTP example

### Related Models

- MOC - Container Networking Model - How Linux primitives map to OSI layers
- MOC - DNS Architecture - DNS operates at Layer 7

## Questions / To Explore

### Factual Gaps

- What is the TCP/IP model and how does it differ from OSI?
- What protocols operate at each OSI layer in Kubernetes?
- What is the difference between Layer 2 and Layer 3 networking?

### Mechanism Gaps

- How does a service mesh intercept Layer 7 traffic?
- How do firewalls inspect packets at different OSI layers?
- How does VXLAN encapsulation add an outer Layer 3 header?

### Debugging Scenarios

- DEBUG - Ping works but HTTP fails (which layer is broken?)
- DEBUG - Packet captured at Layer 2 but not Layer 3
- How to diagnose which OSI layer is causing connectivity issues?

---

## Philosophical Insight

> "Networking is not wires—it's data transformation. The 'network' is a stack of metadata wrappers, each layer adding context (addresses, ports, checksums) around an opaque payload. Only Layer 1 is 'real' (photons and electrons). Everything else is abstraction."
>
> See: INSIGHT - Networking is data labeling not wires
