---
aliases: ["MSS Clamping", "PMTUD", "Protocol Overhead"]
created: 2025-12-23T22:39:13Z
last_reviewed: "2025-12-23"
modified: 2026-02-01T15:07:54+00:00
status: "stable"
tags: ["mtu", "overhead", "performance", "SoftwareEngineering/Networking", "vpn"]
title: SoT - Network Overhead & MTU
type: "SoT"
updated: 
---

## 1. The Mathematics of Overhead

Encapsulation introduces Overhead—the portion of the total transmitted data that consists of protocol headers rather than user data.

- Example: A small 100-byte HTTP request can experience up to 66% total overhead after adding TCP (20B), IP (20B), and Ethernet (18B) headers/trailers.
- Capacity Planning: A "1 Gbps connection" typically refers to the wire-speed (bits). Actual application throughput is always lower due to the 4-7% overhead inherent in standard TCP/IP over Ethernet.

---

## 2. MTU (Maximum Transmission Unit)

MTU is the size of the largest PDU that a layer can pass onwards.

- Standard Ethernet MTU: 1500 bytes.
- The VPN Problem: Protocols like IPsec or GRE add their own headers (encapsulation). This reduces the "inner" space available for data. If a client sends a full 1500-byte packet into a VPN tunnel, it will exceed the path MTU and be Fragmented or dropped.

---

## 3. Mitigation Strategies

### A. MSS Clamping

Maximum Segment Size (MSS) determines the largest chunk of data TCP will send.

- The Fix: Routers can "clamp" the MSS (e.g., to 1360 bytes) during the TCP handshake. This forces the client to send smaller segments that will fit through the VPN tunnel without fragmentation.

### B. PMTUD (Path MTU Discovery)

The process where a host uses ICMP "Destination Unreachable" messages to dynamically discover the lowest MTU along a network path.

- Failure Mode: If firewalls block ICMP, PMTUD fails, leading to "Black Hole" connections where small requests (like a login) work, but large requests (like a file download) hang indefinitely.

---

## 4. Summary

Network efficiency is a balance between Payload Size and Overhead. Large packets minimize overhead but risk fragmentation on complex paths (Cloud/VPN). Small packets are robust but waste bandwidth on redundant headers.
