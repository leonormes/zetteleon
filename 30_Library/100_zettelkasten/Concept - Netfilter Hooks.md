---
aliases: []
created: 2025-11-22T15:00:09+00:00
last_reviewed: '2025-11-22'
modified: 2026-07-04T10:51:53+00:00
permalink: llmeon/30-library/100-zettelkasten/concept-netfilter-hooks
status: seedling
tags: [SoftwareEngineering/networking/kernel]
title: Concept - Netfilter Hooks
type: concept
updated: null
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
