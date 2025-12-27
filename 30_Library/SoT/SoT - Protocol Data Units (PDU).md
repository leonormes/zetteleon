---
aliases: ["Network Units", "PDU"]
confidence: "5/5"
created: 2025-12-23T22:38:57Z
epistemic: "technical"
last_reviewed: "2025-12-23"
modified: 2025-12-27T20:40:56+00:00
purpose: "To define the Protocol Data Unit (PDU) as the fundamental unit of information at each layer of the network stack."
review_interval: "6 months"
see_also: ["[[SoT - Encapsulation & De-encapsulation]]", "[[SoT - The Data Architecture of DNS]]"]
source_of_truth: []
status: "stable"
tags: ["networking", "osi", "pdu", "protocol", "topic/technology"]
title: SoT - Protocol Data Units (PDU)
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> A **Protocol Data Unit (PDU)** is a single unit of information transmitted between peer entities in a computer network. It consists of layer-specific control information (headers and trailers) plus the user data (payload).

### 🧩 Problems Solved by PDUs

- **Structured Data Transfer:** Ensures peer entities understand the components (addresses, error codes) of the transmitted data.
- **Abstraction through Layering:** Allows each layer to focus on its specific tasks (e.g., L3 on routing, L4 on app identification) without knowing the internals of other layers.
- **Bit Stream Organisation:** Transforms raw electrical signals into meaningful, manageable chunks (Frames).
- **Multiplexing:** PDUs like Segments use port numbers to identify which specific application process should receive the data.

---

## 2. Layer-Specific Terminology

...
---

## 3. Historical Context: OSI vs. TCP/IP

The concept of the PDU emerged with early networks like ARPANET and was formalised in the late 1970s.

- **OSI Model:** A comprehensive design reference defining seven distinct PDUs (Segment, Packet, Frame, Bit).
- **TCP/IP Model:** A practical implementation illustrating the logic of the Internet Protocol suite. While less rigorous in its layering, it uses the same PDU concepts (e.g., TCP Segments, IP Datagrams).

While "packet" is often used colloquially for all data, PDUs have precise technical names based on their position in the **OSI Model**:

| OSI Layer | PDU Name | Typical Data |
|:--- |:--- |:--- |
| **7. Application** | **Data** | User-facing info (HTTP request, DNS query). |
| **6. Presentation**| **Data** | Encryption, compression, formatting. |
| **5. Session** | **Data** | Session management. |
| **4. Transport** | **Segment** (TCP) / **Datagram** (UDP) | End-to-end delivery and reliability metadata. |
| **3. Network** | **Packet** | Logical addressing (IP) and routing info. |
| **2. Data Link** | **Frame** | Physical addressing (MAC) and error detection. |
| **1. Physical** | **Bits** | Raw electrical or optical signals (1s and 0s). |

---

## 3. Common Misconceptions

- **"Packet" ≠ Everything:** Technically, a packet exists only at **Layer 3**. Using the term for Layer 2 traffic (Frames) or Layer 4 traffic (Segments) can cause confusion during high-level troubleshooting.
- **TCP vs. UDP:** TCP always uses **Segments** (reflecting its segmentation of a data stream), while UDP uses **Datagrams** (self-contained units with minimal overhead).

---

## 4. Summary

PDUs define the **Scope of Responsibility** for each layer. Identifying the specific PDU experiencing issues (e.g., "CRC errors in the Frame") allows engineers to isolate failures to specific hardware or protocols.
