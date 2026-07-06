---
aliases: []
created: 2025-11-22T15:00:10+00:00
last_reviewed: '2025-11-22'
modified: 2026-07-04T10:51:53+00:00
permalink: llmeon/30-library/100-zettelkasten/concept-network-bridge-vs-router
status: seedling
tags: [SoftwareEngineering/networking/infrastructure]
title: Concept - Network Bridge vs Router
type: concept
updated: null
---

## Network Bridge Vs Router

Summary: A network bridge forwards traffic at Layer 2 based on MAC addresses, while a router forwards traffic at Layer 3 based on IP addresses.

Details:

- Bridge: Connects network segments transparently. It does not modify the IP header or decrement the TTL (Time To Live). It acts like a switch.
- Router: Connects different networks. It inspects the IP header, makes routing decisions, decrements the TTL, and (for IPv4) recalculates checksums.
In Linux, a single machine can perform both roles simultaneously using mechanisms like `br0` (bridge) and IP forwarding (router).
