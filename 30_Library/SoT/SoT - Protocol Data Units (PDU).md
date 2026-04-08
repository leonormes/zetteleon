---
aliases: ["Encapsulation", "Network Units", "PDU", "SDU", "The Russian Doll Mechanism"]
created: 2025-12-23T22:38:57Z
last_reviewed: "2026-04-04"
modified: 2026-04-08T17:58:57+00:00
status: "stable"
tags: ["osi", "pdu", "protocol", "SoftwareEngineering/Networking", "topic/technology"]
title: SoT - Protocol Data Units (PDU)
type: "SoT"
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> A Protocol Data Unit (PDU) is a single unit of information transmitted between peer entities in a computer network. It consists of layer-specific control information (headers and trailers) plus the user data (payload).

---

## 2. The "Russian Doll" Mechanism (Encapsulation)

The networking stack utilizes Encapsulation to allow independent systems (apps, OS, routers) to cooperate without knowing each other's internals.

- Process: As data moves down the stack, each layer treats the unit from the layer above as an opaque payload and wraps it with its own header (and sometimes a trailer).
- Result: A nested structure where the "outer" layers provide the context needed for the "inner" data to reach its destination.

### SDU vs. PDU

To understand the nesting, we distinguish between two types of data units:

1. SDU (Service Data Unit): The data received from the layer above.
2. PDU (Protocol Data Unit): The total package (Header + SDU + Trailer) passed to the layer below.

Formula: `Header + SDU = PDU`.

---

## 3. The Path of a Request (HTTP Example)

## 2. Layer-by-Layer Encapsulation Logic

### Layer 4: The TCP Segment (Reliability)

Function: Takes the continuous stream of application data and divides it into manageable chunks. It adds a header to ensure reliable, ordered delivery.

| Header Field | Size (bits) | Purpose |
|:--- |:--- |:--- |
| Source/Dest Port | 16 | Multiplexing. Identifies the specific sending and receiving applications (e.g., Web Server on 80). |
| Sequence Number | 32 | Ordering. Assigns a unique ID to every byte to allow reassembly of out-of-order packets. |
| Ack Number | 32 | Reliability. Confirms receipt of data, implicitly requesting the next chunk. |
| Window Size | 16 | Flow Control. Tells the sender how much buffer space the receiver has left to prevent overflow. |
| Checksum | 16 | Integrity. Detecting errors in the header and payload. |
| Flags | 9 | Control. SYN (Start), ACK (Confirm), FIN (End), RST (Reset/Error). |

### Layer 3: The IP Packet (Routing)

Function: Encapsulates the TCP Segment to handle global addressing and routing across different networks.

| Header Field | Size (bits) | Purpose |
|:--- |:--- |:--- |
| Source/Dest IP | 32 | Global Addressing. The logical address used by routers to forward the packet to the final destination. |
| TTL | 8 | Loop Prevention. Time To Live. Decremented by each router; packet dropped if 0. |
| Protocol | 8 | Demultiplexing. Tells the receiver which L4 protocol is inside (6=TCP, 17=UDP). |
| Fragment Offset | 13 | Reassembly. Used if the packet was split (fragmented) to fit a smaller network link. |

### Layer 2: The Ethernet Frame (Local Delivery)

Function: Encapsulates the IP Packet for transmission over a physical medium (wire/air) within a local network (LAN). It adds a header and a trailer.

| Field | Size (bytes) | Purpose |
|:--- |:--- |:--- |
| Preamble/SFD | 8 | Synchronization. Alternating 1s and 0s to wake up the receiver and sync clocks. |
| Source/Dest MAC | 6 | Physical Addressing. The hardware address of the NIC. Used by switches to forward frames locally. |
| EtherType | 2 | Demultiplexing. Identifies the L3 protocol inside (0x0800 = IPv4). |
| FCS / CRC | 4 | Error Detection. A cyclical redundancy check at the _end_ (trailer) to verify the frame arrived intact. |

### Layer 1: The Physical Bit Stream

Function: Encodes the Frame into physical signals (Voltage, Light, Radio Waves) for transmission. No headers are added here; the PDU is the raw Bit.
---

## 3. Historical Context: OSI vs. TCP/IP

The concept of the PDU emerged with early networks like ARPANET and was formalised in the late 1970s.

- OSI Model: A comprehensive design reference defining seven distinct PDUs (Segment, Packet, Frame, Bit).
- TCP/IP Model: A practical implementation illustrating the logic of the Internet Protocol suite. While less rigorous in its layering, it uses the same PDU concepts (e.g., TCP Segments, IP Datagrams).

While "packet" is often used colloquially for all data, PDUs have precise technical names based on their position in the OSI Model:

| OSI Layer | PDU Name | Typical Data |
|:--- |:--- |:--- |
| 7. Application | Data | User-facing info (HTTP request, DNS query). |
| 6. Presentation| Data | Encryption, compression, formatting. |
| 5. Session | Data | Session management. |
| 4. Transport | Segment (TCP) / Datagram (UDP) | End-to-end delivery and reliability metadata. |
| 3. Network | Packet | Logical addressing (IP) and routing info. |
| 2. Data Link | Frame | Physical addressing (MAC) and error detection. |
| 1. Physical | Bits | Raw electrical or optical signals (1s and 0s). |

---

## 3. Common Misconceptions

- "Packet" ≠ Everything: Technically, a packet exists only at Layer 3. Using the term for Layer 2 traffic (Frames) or Layer 4 traffic (Segments) can cause confusion during high-level troubleshooting.
- TCP vs. UDP: TCP always uses Segments (reflecting its segmentation of a data stream), while UDP uses Datagrams (self-contained units with minimal overhead).

---

## 4. Summary

PDUs define the Scope of Responsibility for each layer. Identifying the specific PDU experiencing issues (e.g., "CRC errors in the Frame") allows engineers to isolate failures to specific hardware or protocols.
