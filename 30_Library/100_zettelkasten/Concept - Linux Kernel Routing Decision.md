---
aliases: []
created: 2025-11-22 15:00:02+00:00
modified: 2026-07-04 10:51:53+00:00
permalink: llmeon/30-library/100-zettelkasten/concept-linux-kernel-routing-decision
tags:
- SoftwareEngineering/networking/routing
title: Concept - Linux Kernel Routing Decision
prodos:
  kind: atomic
  atomic:
    form: concept
  lifecycle: seedling
  review:
    last_reviewed: '2025-11-22'
---


## Linux Kernel Routing Decision

Summary: The Linux kernel determines the destination interface for a packet by consulting its routing tables to match the destination IP address.

Details:

The decision process generally reduces to checking if the destination IP is on a locally directly-connected network or if it requires a gateway.

- Local: If the IP matches a connected network range, the packet is sent directly out of the corresponding interface.
- Gateway: If no local match is found, the packet is forwarded to the default gateway (usually a router) specified in the routing table.
Advanced configurations can use `ip rule` to consult multiple routing tables based on source address or firewall marks.
