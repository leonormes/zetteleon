---
aliases: []
confidence: 
created: 2025-10-24T15:19:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:22Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [encapsulation, osi, protocol, topic/technology/networking, type/mechanism]
title: How OSI layers encapsulate data in a packet trace
type: Mechanism
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - OSI Model]]
- Related: [[What is the OSI model]], [[Show a minimal end-to-end example of data encapsulation]]

## Summary

As data moves down the OSI stack from Application to Physical layer, each layer adds its own header containing metadata (addresses, ports, protocol info), wrapping the payload from the layer above—this process is called encapsulation. On the receiving end, decapsulation reverses this by stripping headers layer by layer.

## Context / Problem

Networking involves multiple independent systems (applications, operating systems, routers, switches) that need to cooperate without knowing each other's internals. Each OSI layer solves a specific problem (addressing, routing, error checking, etc.) by adding its own metadata header. Understanding encapsulation reveals why packet captures show nested headers and how to diagnose which layer is failing.

## Mechanism / Details

### Encapsulation: Sending Data (Top → Down)

```sh
┌──────────────────────────────────────────────────┐
│ Layer 7: Application (HTTP)                      │
│ Data: "GET /index.html HTTP/1.1"                 │
│ Output: [HTTP Data]                              │
└────────────────────┬─────────────────────────────┘
                     │ Pass down to Transport
┌────────────────────▼─────────────────────────────┐
│ Layer 4: Transport (TCP)                         │
│ Adds: TCP Header                                 │
│   - Source Port: 49152                           │
│   - Dest Port: 80                                │
│   - Sequence Number, Flags, Checksum             │
│ Output: [TCP Header][HTTP Data]                  │
│         └─────────Segment─────────┘              │
└────────────────────┬─────────────────────────────┘
                     │ Pass down to Network
┌────────────────────▼─────────────────────────────┐
│ Layer 3: Network (IP)                            │
│ Adds: IP Header                                  │
│   - Source IP: 10.244.0.5                        │
│   - Dest IP: 93.184.216.34                       │
│   - Protocol: TCP, TTL, Checksum                 │
│ Output: [IP Header][TCP Header][HTTP Data]       │
│         └──────────────Packet──────────────┘     │
└────────────────────┬─────────────────────────────┘
                     │ Pass down to Data Link
┌────────────────────▼─────────────────────────────┐
│ Layer 2: Data Link (Ethernet)                    │
│ Adds: Ethernet Header + Trailer                  │
│   Header:                                        │
│     - Source MAC: aa:bb:cc:dd:ee:ff              │
│     - Dest MAC: 11:22:33:44:55:66                │
│     - EtherType: 0x0800 (IPv4)                   │
│   Trailer:                                       │
│     - CRC (error detection)                      │
│ Output: [Eth Hdr][IP Hdr][TCP Hdr][HTTP][CRC]    │
│         └─────────────Frame──────────────────┘   │
└────────────────────┬─────────────────────────────┘
                     │ Pass down to Physical
┌────────────────────▼─────────────────────────────┐
│ Layer 1: Physical                                │
│ Converts frame to bits:                          │
│   0101010111010001... (electrical signals)       │
│ Transmitted over: Copper, Fiber, WiFi            │
└──────────────────────────────────────────────────┘
```

### Decapsulation: Receiving Data (Bottom → Up)

```sh
┌──────────────────────────────────────────────────┐
│ Layer 1: Physical                                │
│ Receives: Electrical/optical signals             │
│ Converts to bits: 0101010111...                  │
│ Passes up as frame                               │
└────────────────────┬─────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────┐
│ Layer 2: Data Link (Ethernet)                    │
│ Reads: [Eth Hdr][IP Hdr][TCP Hdr][HTTP][CRC]     │
│ Checks:                                          │
│   - Dest MAC matches this interface?             │
│   - CRC valid (no corruption)?                   │
│ Strips: Ethernet Header + Trailer                │
│ Passes up: [IP Hdr][TCP Hdr][HTTP Data]          │
└────────────────────┬─────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────┐
│ Layer 3: Network (IP)                            │
│ Reads: [IP Hdr][TCP Hdr][HTTP Data]              │
│ Checks:                                          │
│   - Dest IP matches this host?                   │
│   - TTL > 0? (decrement)                         │
│   - Checksum valid?                              │
│ Strips: IP Header                                │
│ Passes up: [TCP Hdr][HTTP Data]                  │
└────────────────────┬─────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────┐
│ Layer 4: Transport (TCP)                         │
│ Reads: [TCP Hdr][HTTP Data]                      │
│ Checks:                                          │
│   - Dest Port matches listening socket?          │
│   - Sequence number correct?                     │
│   - Checksum valid?                              │
│ Strips: TCP Header                               │
│ Passes up: [HTTP Data]                           │
└────────────────────┬─────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────┐
│ Layer 7: Application (HTTP)                      │
│ Receives: "GET /index.html HTTP/1.1"             │
│ Application processes request                    │
└──────────────────────────────────────────────────┘
```

### Real Packet Example: HTTP GET Request

#### Layer-by-Layer Breakdown

**Layer 7 - Application (HTTP):**

```http
GET /index.html HTTP/1.1
Host: example.com
User-Agent: curl/7.68.0
```

**Layer 4 - Transport (TCP Header):**

```sh
+------------------+
| Source Port: 49152 (client ephemeral)    |
| Dest Port: 80 (HTTP)                     |
| Sequence: 1001                           |
| ACK: 5001                                |
| Flags: PSH, ACK                          |
| Window: 229                              |
| Checksum: 0xa3f2                         |
+------------------+
+ [HTTP Data]
```

**Layer 3 - Network (IP Header):**

```sh
+------------------+
| Version: 4 (IPv4)                        |
| Header Length: 20 bytes                  |
| Total Length: 150 bytes                  |
| TTL: 64                                  |
| Protocol: 6 (TCP)                        |
| Source IP: 10.244.0.5                    |
| Dest IP: 93.184.216.34                   |
| Checksum: 0x1c46                         |
+------------------+
+ [TCP Segment]
```

**Layer 2 - Data Link (Ethernet Frame):**

```sh
+------------------+
| Dest MAC: 52:54:00:12:34:56              |
| Source MAC: aa:bb:cc:dd:ee:ff            |
| EtherType: 0x0800 (IPv4)                 |
+------------------+
+ [IP Packet]
+------------------+
| Frame Check Sequence (CRC): 0x9a3b2c1d   |
+------------------+
```

**Layer 1 - Physical:**

```sh
Bits: 01010100110101... (transmitted as voltage/light)
```

### Complete Encapsulated Packet (Wire Format)

```sh
┌──────────────────────────────────────────────────┐
│ Preamble (Layer 1 sync)                          │
├──────────────────────────────────────────────────┤
│ Ethernet Header (14 bytes)                       │
│   Dest MAC (6) | Src MAC (6) | Type (2)          │
├──────────────────────────────────────────────────┤
│ IP Header (20 bytes)                             │
│   Ver | IHL | ToS | Length | ID | Flags | TTL    │
│   Protocol | Checksum | Src IP | Dst IP          │
├──────────────────────────────────────────────────┤
│ TCP Header (20 bytes)                            │
│   Src Port | Dst Port | Seq | ACK | Flags        │
│   Window | Checksum | Urgent                     │
├──────────────────────────────────────────────────┤
│ HTTP Data (variable)                             │
│   GET /index.html HTTP/1.1\r\n                   │
│   Host: example.com\r\n...                       │
├──────────────────────────────────────────────────┤
│ Ethernet FCS (4 bytes, CRC)                      │
└──────────────────────────────────────────────────┘
```

### Container Networking Context

When a **Pod sends an HTTP request**, the encapsulation happens as follows:

```bash
# Pod → External API
1. Application (curl): Creates HTTP request
2. TCP: Adds source/dest ports
3. IP: Adds Pod IP (10.244.0.5) → External IP (93.184.216.34)
4. Ethernet: Adds Pod MAC → Bridge MAC
5. Packet travels: veth → bridge → host routing
6. MASQUERADE rewrites IP header (Layer 3)
   - Source IP: 10.244.0.5 → 203.0.113.5 (node IP)
7. New Ethernet frame: Host MAC → Gateway MAC
8. Physical: Transmitted via node NIC
```

**Key Insight:** MASQUERADE operates at Layer 3, modifying the IP header AFTER encapsulation but BEFORE final transmission.

### Tcpdump Analysis Example

```bash
# Capture on Pod interface
ip netns exec pod-red tcpdump -i veth-red -vv -n

# Sample output:
10.244.0.5.49152 > 93.184.216.34.80: Flags [P.], seq 1:100, ack 1, win 229, length 99: HTTP: GET /

# Breakdown:
# - 10.244.0.5.49152: Source IP.Port (Layer 3 + 4)
# - 93.184.216.34.80: Dest IP.Port
# - Flags [P.]: TCP PSH + ACK (Layer 4)
# - seq 1:100: TCP sequence range
# - length 99: Payload size (Layer 7 data)
```

## Connections / Implications

### What This Enables

- **Modular networking**: Each layer operates independently
- **Troubleshooting by layer**: Isolate failures ("Layer 3 issue" = IP routing)
- **Protocol interoperability**: Mix and match protocols at each layer
- **Debugging with tcpdump/Wireshark**: Visualize headers layer-by-layer

### What Breaks If Encapsulation Fails

| Layer | Failure | Symptom |
|-------|---------|----------|
| L7 | Malformed HTTP | 400 Bad Request |
| L4 | TCP checksum error | Connection reset |
| L3 | IP header corrupted | Packet dropped silently |
| L2 | CRC mismatch | Frame discarded |
| L1 | Signal noise | No packets received |

### How It Maps to Kubernetes

- **Pod-to-Pod**: Encapsulation starts in Pod, packets flow through veth → bridge
- **Service routing (kube-proxy)**: Modifies Layer 3 (IP) and Layer 4 (port) via DNAT
- **Network Policies**: Operate at Layer 3/4 (IP addresses, ports)
- **Service Mesh (Istio)**: Proxies operate at Layer 7 (HTTP headers)

## Questions / To Explore

- How does VXLAN encapsulation add an outer IP header?
- What is the maximum packet size (MTU) and how does it affect encapsulation?
- How do firewalls inspect packets at different OSI layers?
- DEBUG - Packet captured on one interface but not another
- How does TLS/SSL encryption fit into OSI encapsulation?
- What tools can decode and visualize packet encapsulation?
