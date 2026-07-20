---
aliases: []
conformant: false
created: 2025-11-22T15:00:02+00:00
modified: 2026-07-20T16:34:32+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/concept-linux-kernel-routing-decision
tags: [SoftwareEngineering/networking/routing]
title: Concept - Linux Kernel Routing Decision
type: claim
---

## Linux Kernel Routing Decision

Summary: The Linux kernel determines the destination interface for a packet by consulting its routing tables to match the destination IP address.

Details:

The decision process generally reduces to checking if the destination IP is on a locally directly-connected network or if it requires a gateway.

- Local: If the IP matches a connected network range, the packet is sent directly out of the corresponding interface.
- Gateway: If no local match is found, the packet is forwarded to the default gateway (usually a router) specified in the routing table.
Advanced configurations can use `ip rule` to consult multiple routing tables based on source address or firewall marks.
