---
aliases: []
created: 2025-11-22 15:00:02+00:00
last_reviewed: '2025-11-22'
modified: 2026-02-01 15:08:35+00:00
status: seedling
tags:
- SoftwareEngineering/networking/routing
title: Concept - Linux Kernel Routing Decision
type: concept
updated: null
permalink: llmeon/30-library/100-zettelkasten/concept-linux-kernel-routing-decision
---

## Linux Kernel Routing Decision

Summary: The Linux kernel determines the destination interface for a packet by consulting its routing tables to match the destination IP address.

Details:

The decision process generally reduces to checking if the destination IP is on a locally directly-connected network or if it requires a gateway.

- Local: If the IP matches a connected network range, the packet is sent directly out of the corresponding interface.
- Gateway: If no local match is found, the packet is forwarded to the default gateway (usually a router) specified in the routing table.
Advanced configurations can use `ip rule` to consult multiple routing tables based on source address or firewall marks.