---
aliases: []
created: 2025-11-22T15:00:09Z
last_reviewed: "2025-11-22"
modified: 2026-02-01T15:08:35+00:00
status: "seedling"
tags: ["SoftwareEngineering/networking/kernel"]
title: Concept - Netfilter Hooks
type: "concept"
updated: 
---

## Netfilter Hooks

Summary: Netfilter hooks are specific points in the Linux kernel packet traversal path where software (like iptables or nftables) can register callbacks to inspect, modify, or drop packets.

Details:

The five standard hooks are:

- PREROUTING: Triggered immediately upon packet arrival, before the routing decision.
- INPUT: Triggered for packets destined for the local system.
- FORWARD: Triggered for packets routed to another host.
- OUTPUT: Triggered for locally generated packets before they leave.
- POSTROUTING: Triggered just before packets leave the network device.
These hooks enable firewalls, NAT, and packet logging.
