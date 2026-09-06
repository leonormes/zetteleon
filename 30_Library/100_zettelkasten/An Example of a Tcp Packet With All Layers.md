---
aliases: [Packet Anatomy, TCP Packet Example]
axiom: true
conformant: true
created: 2025-10-21T13:23:09+00:00
epistemic_status: high
modified: 2026-07-10T23:25:00+01:00
permalink: llmeon/30-library/100-zettelkasten/an-example-of-a-tcp-packet-with-all-layers
prodos.kind: atomic
prodos.lifecycle: stable
proposition: "A TCP packet structurally encapsulates data through the OSI layers—Application (L7), Transport (L4), Network (L3), and Data Link (L2)—with each layer adding discrete routing and control headers."
tags: [SoftwareEngineering/Networking]
title: An Example of a Tcp Packet With All Layers
type: claim
---

## TCP Packet Layers & Headers

### Application Layer Data

- Actual data sent by an app (e.g., HTTP request: "GET /index.html").

---

### Transport Layer: TCP Header (Layer 4)

_See: TCP Segment Details_

| Field            | Example Value   | Notes                                       |
|:--------------- |:-------------- |:------------------------------------------ |
| Source Port      | 12345           | Sending app's port                          |
| Destination Port | 80              | Receiving app's port (e.g., HTTP)           |
| Sequence Number  | 3764878698      | Order for data                              |
| Acknowledgment   | 145298484       | Next byte expected by receiver              |
| Data Offset      | 5               | TCP header length (no options)              |
| Reserved         | 0               | Reserved for future use                     |
| Flags            | 0x18 (PSH, ACK) | Connection control bits                     |
| Window Size      | 8192            | Bytes receiver can accept                   |
| Checksum         | 0xf24c          | Error detection                             |
| Urgent Pointer   | 0               | Points to urgent data (if any, else 0)      |
| Options          | None            | Used sometimes (e.g., during handshake/MSS) |

---

### Network Layer: IP Header (Layer 3 - IPv4)

_See: IP Packet Details_

| Field                | Example Value | Notes                         |
|:------------------- |:------------ |:---------------------------- |
| Version              | 4             | IPv4                          |
| Header Length        | 20 bytes      | Typically without options     |
| Total Length         | 140 bytes     | Header + TCP + data           |
| Source Address       | 192.168.1.21  | Sender IP                     |
| Destination Address  | 172.217.22.36 | Receiver IP                   |
| Identification       | 0x1234        | For fragmentation             |
| Flags/Fragment Offs. | 0             | Usually 0 if no fragmentation |
| TTL                  | 64            | Packet lifetime in hops       |
| Protocol             | 6             | 6 = TCP                       |
| Header Checksum      | 0x0000        | IP error detection            |

---

### Data Link Layer: Ethernet Header (Layer 2)

_See: Ethernet Frame Details_

| Field           | Example Value     | Notes                  |
|:-------------- |:---------------- |:--------------------- |
| Destination MAC | 00:1A:2B:3C:4D:5E | Receiver's MAC address |
| Source MAC      | 5E:4D:3C:2B:1A:00 | Sender's MAC address   |
| Ethertype       | 0x0800            | IPv4 protocol          |

---

### Physical Layer (Layer 1)

- Bits/signals on wire (not usually shown in diagrams or captures)

---

## Full Example (Flattened)

| Ethernet Header              | IP Header                                                     | TCP Header                                                                 | Application Data                                   |
|:--------------------------- |:------------------------------------------------------------ |:------------------------------------------------------------------------- |:------------------------------------------------- |
| Dest MAC (00:1A:2B:3C:4D:5E) | Version 4, Src 192.168.1.21, Dest 172.217.22.36, Protocol TCP | Src port 12345, Dest port 80, Seq 3764878698, Ack 145298484, Flags ACK/PSH | "GET /index.html HTTP/1.1\r\nHost: example.com\r\n…" |

---

This condensed presentation lets you reference key fields for packet analysis, teaching, or debugging workflows.

[supports:: [[SoT - The Data-Centric Theory of Networking]]]
