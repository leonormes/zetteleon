---
aliases: []
confidence: 
created: 2025-11-22T15:00:13Z
epistemic: NA
last_reviewed: 2025-11-22
modified: 2025-11-22T14:42:57Z
purpose: "Maps the journey of a network packet through the Linux kernel subsystems."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [networking]
title: MOC - The Life of a Packet in the Linux Kernel
type: map
uid: 2025-11-22T15:00:13Z
updated: 2025-11-22T15:00:13Z
---

## MOC - The Life of a Packet in the Linux Kernel

**Summary:** This map simplifies the complex path a data packet takes through the Linux kernel, covering the transition from user-space application data to electrical signals on the wire and back again.

### High-Level Flow

The journey of a packet is a pipeline of well-defined steps managed by the kernel's networking stack.

1.  **Transmit:** App $\to$ TCP/IP Stack $\to$ Routing $\to$ Neighbor Lookup $\to$ Queuing $\to$ NIC.
2.  **Receive:** NIC $\to$ Ring Buffer $\to$ NAPI $\to$ Routing/Filter $\to$ Socket $\to$ App.

### Part 1 - Transmit: from `write()` to the Wire

#### 1. Application to Kernel

The process begins when an application writes data to a [[Concept - Network Socket|socket]]. The kernel accepts this buffer and prepares it for transmission.

-   **Segmentation:** TCP breaks the buffer into segments. The size is determined by the [[Concept - Maximum Transmission Unit vs Maximum Segment Size|Maximum Segment Size (MSS)]], which is negotiated during the [[Concept - TCP Three-Way Handshake|TCP three-way handshake]].
-   **State:** THe kernel tracks sequence numbers and congestion windows for the connection.

#### 2. Routing Decision

The kernel must decide where to send the packet. This is determined by the [[Concept - Linux Kernel Routing Decision]].

-   If the destination is local, it goes out the corresponding interface.
-   If remote, it is handed to the default gateway.

#### 3. Neighbor Lookup

Once the interface is known, the kernel needs the physical address of the next hop.

-   For IPv4, it uses the [[Concept - Address Resolution Protocol|Address Resolution Protocol (ARP)]] to map the IP to a MAC address.
-   For IPv6, it uses the [[Concept - Neighbor Discovery Protocol|Neighbor Discovery Protocol (NDP)]].

#### 4. Queuing and Traffic Control

Before hitting the hardware, the packet passes through the [[Concept - Linux Queuing Discipline|Queuing Discipline (qdisc)]], which acts as a traffic cop. It handles buffering, pacing, and fair scheduling to prevent bufferbloat.

#### 5. The Driver and NIC

The kernel driver hands the packet to the Network Interface Card (NIC). The NIC uses [[Concept - NIC Direct Memory Access|DMA]] to pull packet data directly from system RAM and converts it into signals on the wire.

### Part 2 - Receive: from the Wire back to Your App

#### 1. Polling with NAPI

When frames arrive, the NIC writes them to memory. To avoid overwhelming the CPU with interrupts for every packet, the kernel uses [[Concept - Linux NAPI|NAPI]] to switch between interrupt mode and polling mode, processing batches of packets efficiently.

#### 2. IP Checks and Filtering

The kernel validates the IP header. This is where [[Concept - Netfilter Hooks]] (used by iptables/nftables) come into play.

-   **PREROUTING/INPUT:** Packets are filtered or improperly routed packets are modified (DNAT) here.
-   The kernel checks if the packet is for the local machine or needs to be forwarded (acting as a router).

#### 3. TCP Reassembly

The TCP stack reorders segments, handles ACKs, and eventually wakes the application waiting on the socket.

### Concepts and Edge Cases

-   **Local Traffic:** Traffic sent to `127.0.0.1` uses the [[Concept - Loopback Interface]], bypassing the physical NIC entirely for high speed.
-   **Device Roles:** It is important to distinguish between switching and routing. A [[Concept - Network Bridge vs Router|bridge operates at Layer 2, while a router operates at Layer 3]].
-   **Protocols:** While TCP is complex and stateful, [[Concept - UDP vs TCP|UDP]] offers a simpler, connectionless alternative for different use cases.
