---
aliases: []
confidence: 
created: 2025-10-24T15:13:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:22Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [model, osi, protocol, topic/technology/networking, type/fact]
title: What is the OSI model
type: Factual
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - OSI Model]]
- Related: [[How OSI layers encapsulate data in a packet trace]], [[Show a minimal end-to-end example of data encapsulation]]

## Summary

The OSI (Open Systems Interconnection) model is a 7-layer conceptual framework that standardizes network communication by dividing it into hierarchical stages, from raw physical signals (Layer 1) to human-readable applications (Layer 7).

## Context / Problem

Networking involves complex interactions between hardware, software, and protocols. Without a common reference model, understanding how data flows from an application (e.g., web browser) to physical transmission (e.g., electrical signals) would be chaotic. The OSI model provides a universal language for describing, troubleshooting, and designing networks by breaking the process into discrete, manageable layers.

## Mechanism / Details

### The Seven Layers

| Layer | Name          | Function | Example Protocols/Tech |
|-------|---------------|----------|------------------------|
| **7** | Application   | User-facing data formats (HTTP, DNS) | HTTP, SMTP, DNS, SSH |
| **6** | Presentation  | Data encoding and encryption | TLS, JSON, JPEG |
| **5** | Session       | Connection management and state | NetBIOS, RPC |
| **4** | Transport     | End-to-end delivery, segmentation | TCP, UDP |
| **3** | Network       | Logical addressing and routing | IP, ICMP, routing |
| **2** | Data Link     | Frame delivery on local segment | Ethernet, ARP, bridges |
| **1** | Physical      | Electrical/optical signal transmission | Cables, NICs, WiFi |

### Data Transformation per Layer

As data moves **down** the stack (sending):

1. **Application** → Data formatted (HTTP request)
2. **Transport** → Segmented + TCP header added
3. **Network** → IP header added (source/dest IPs)
4. **Data Link** → Ethernet header + trailer added (MACs)
5. **Physical** → Converted to bits, transmitted as signals

As data moves **up** the stack (receiving):

- Each layer strips its header and processes the payload
- Eventually, the original application data is delivered

### Encapsulation Terminology

| Layer | Unit Name | What's Added |
|-------|-----------|-------------|
| Application | **Data** | User message |
| Transport | **Segment** | TCP/UDP header (ports) |
| Network | **Packet** | IP header (IP addresses) |
| Data Link | **Frame** | Ethernet header (MACs) + trailer |
| Physical | **Bits** | Electrical signals |

### Practical Example: HTTP Request

```sh
Layer 7: GET /index.html HTTP/1.1
Layer 4: [TCP Header: src=49152, dst=80] + HTTP Data
Layer 3: [IP Header: src=10.0.0.5, dst=93.184.216.34] + TCP Segment
Layer 2: [Ethernet: src=aa:bb:cc, dst=dd:ee:ff] + IP Packet + [CRC]
Layer 1: 010101110100... (electrical pulses)
```

## Connections / Implications

### What This Enables

- **Modular design**: Each layer is independent; changes at one layer don't require changes at others
- **Troubleshooting**: Problems can be isolated by layer (e.g., "Layer 3 issue" = routing problem)
- **Interoperability**: Vendors implement layers independently using standard protocols
- **Teaching framework**: Universal language for networking education

### Container Networking and OSI

- **Layer 1**: Physical NICs on the host
- **Layer 2**: Linux bridges (`cni0`), veth pairs, MAC learning via ARP
- **Layer 3**: IP routing between Pods, iptables NAT
- **Layer 4**: TCP/UDP connections between Pods, port-based Services
- **Layer 7**: Application protocols (HTTP, gRPC) used by Pods

### Real-World Vs OSI

The OSI model is a **conceptual** reference:

- Real networks use the **TCP/IP model** (4 layers: Link, Internet, Transport, Application)
- Many protocols span multiple OSI layers (e.g., TLS operates at Layers 5-6)
- The model is still valuable for precise communication and debugging

### Debugging with OSI

| Problem | OSI Layer | Example |
|---------|-----------|------|
| Cable unplugged | Layer 1 | Physical |
| MAC address conflict | Layer 2 | Data Link |
| IP routing failure | Layer 3 | Network |
| TCP handshake fails | Layer 4 | Transport |
| HTTP 404 error | Layer 7 | Application |

## Questions / To Explore

- [[How does data encapsulation work across OSI layers?]]
- [[How does the TCP/IP model differ from OSI?]]
- [[How do CNI plugins operate at different OSI layers?]]
- [[What OSI layer does a Linux bridge operate at?]]
- [[How does TLS encryption fit into the OSI model?]]
- [[DEBUG - How to diagnose which OSI layer is failing?]]
