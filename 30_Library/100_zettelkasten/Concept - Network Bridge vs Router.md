---
aliases: []
created: 2025-11-22T15:00:10Z
last_reviewed: "2025-11-22"
modified: 2026-02-01T15:08:35+00:00
status: "seedling"
tags: ["SoftwareEngineering/networking/infrastructure"]
title: Concept - Network Bridge vs Router
type: "concept"
updated: 
---

## Network Bridge Vs Router

Summary: A network bridge forwards traffic at Layer 2 based on MAC addresses, while a router forwards traffic at Layer 3 based on IP addresses.

Details:

- Bridge: Connects network segments transparently. It does not modify the IP header or decrement the TTL (Time To Live). It acts like a switch.
- Router: Connects different networks. It inspects the IP header, makes routing decisions, decrements the TTL, and (for IPv4) recalculates checksums.
In Linux, a single machine can perform both roles simultaneously using mechanisms like `br0` (bridge) and IP forwarding (router).
