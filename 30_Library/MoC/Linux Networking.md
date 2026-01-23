---
aliases: ["Container Networking Map", "Linux Networking MOC"]
confidence: "High"
created: 2025-10-22T09:39:10Z
epistemic: "Map"
last_reviewed: 
modified: 2026-01-23T18:09:23+00:00
purpose: "To map the foundational Linux networking concepts that underpin Kubernetes and Container networking."
review_interval: "1 year"
see_also: ["[[SoT - Kubernetes Networking & DNS]]", "[[SoT - Linux Networking Primitives]]"]
source_of_truth: []
status: "Active"
tags: ["containers", "linux", "moc", "networking"]
title: Linux Networking
type: "MoC"
uid: 
updated: 
---

## MoC - Linux Networking

> **Core Concept:** Networking in the cloud is not about physical wires; it is about the **logical transformation of data** via namespaces, virtual interfaces, and routing tables.

### 1. The Primitives (The Building Blocks)

Before understanding Kubernetes CNI, you must understand the Linux Kernel tools it automates.

- **[[SoT - Linux Networking Primitives]]:** The definitive guide to Veth Pairs, Bridges, and Namespaces.
    - _Key Concept:_ **Namespaces** isolate the stack; **Veth Pairs** tunnel through the isolation; **Bridges** switch traffic between them.

### 2. Container Networking (The Application)

How these primitives are assembled to create "Pod Networking."

- **[[SoT - Kubernetes Networking & DNS]]:** How K8s uses these primitives (CNI, CoreDNS, Kube-Proxy) to create a flat network.
- **[[SoT - The Data-Centric Theory of Networking]]:** Viewing the network stack as a series of data transformation layers (encapsulation) rather than a physical pipe.

### 3. Protocols & Traffic

- **[[SoT - Protocol Data Units (PDU)]]:** Understanding Frames, Packets, and Segments.
- **[[SoT - TCP Packet Encapsulation Detailed]]:** (Archived/Merged) See [[SoT - Protocol Data Units (PDU)]] for the layer-by-layer breakdown.

### 4. Diagnostics & Debugging

- **IP Forwarding:** `sysctl -w net.ipv4.ip_forward=1` is the "on switch" for routing.
- **IPTables:** The mechanism for NAT (Masquerade) and Service routing (DNAT).
