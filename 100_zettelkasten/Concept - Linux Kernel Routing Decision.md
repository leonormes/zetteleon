---
aliases: []
confidence: 1.0
created: 2025-11-22T15:00:02Z
epistemic: fact
last_reviewed: 2025-11-22
modified: 2025-11-22T14:41:17Z
purpose: "Explains how the Linux kernel selects the path for outgoing packets."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [networking/routing]
title: Concept - Linux Kernel Routing Decision
type: concept
uid: 2025-11-22T15:00:02Z
updated: 2025-11-22T15:00:02Z
---

## Linux Kernel Routing Decision

**Summary:** The Linux kernel determines the destination interface for a packet by consulting its routing tables to match the destination IP address.

**Details:**
The decision process generally reduces to checking if the destination IP is on a locally directly-connected network or if it requires a gateway.
-   **Local:** If the IP matches a connected network range, the packet is sent directly out of the corresponding interface.
-   **Gateway:** If no local match is found, the packet is forwarded to the default gateway (usually a router) specified in the routing table.
Advanced configurations can use `ip rule` to consult multiple routing tables based on source address or firewall marks.
