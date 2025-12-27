---
aliases: ["Data Link vs Network Access", "Layer 2 vs TCP/IP Link"]
confidence: "5/5"
created: 2025-12-24T12:00:00Z
epistemic: "technical"
last_reviewed: 2025-12-24
modified: 2025-12-27T20:41:19+00:00
purpose: "To disambiguate the lowest layers of the OSI and TCP/IP models."
review_interval: "1 year"
see_also: ["[[SoT - Protocol Data Units (PDU)]]"]
source_of_truth: ["[[SoT - Protocol Data Units (PDU)]]"]
status: "stable"
tags: ["networking", "osi", "tcp-ip"]
title: IP Link Layer
type: "concept"
uid: 
updated: 
---

While both models address local network segment transfers, they differ in granularity and scope.

## 📐 OSI Data Link Layer (Layer 2)

- **Granularity:** Explicitly separates Layer 2 (Data Link) from Layer 1 (Physical).
- **Sublayers:** Formally divided into **LLC** (Logical Link Control - protocol multiplexing) and **MAC** (Media Access Control - hardware addressing).
- **Reliability:** Can be reliable or unreliable; protocols like Ethernet often omit acknowledgments.
- **PDU:** Exclusively the **Frame**.

## 📐 TCP/IP Link Layer

- **Scope:** Often called the "Network Access" or "Network Interface" layer.
- **Integration:** Encompasses both OSI Layer 2 and Layer 1 functionality.
- **Hardware Independence:** Designed to run on any link-layer technology (Ethernet, PPP, or even VPN tunnels).
- **Focus:** Immediate next-neighbour connectivity required for internetworking.

## 🔄 Comparison Matrix

| Feature | OSI Data Link (L2) | TCP/IP Link Layer |
|:--- |:--- |:--- |
| **Layer Position**| 2nd of 7 | 1st of 4 (Bottom) |
| **PDU Name** | Frame | Frame |
| **Focus** | Procedural means to transfer data | Local link scope and hardware drivers |
| **Addressing** | MAC Addresses | ARP (Translation to MAC) |
