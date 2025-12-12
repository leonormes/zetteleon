---
aliases: [NDP]
confidence: 1.0
created: 2025-11-22T15:00:08Z
epistemic: fact
last_reviewed: 2025-11-22
modified: 2025-11-22T14:41:58Z
purpose: "Defines the IPv6 equivalent of ARP."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [networking/protocol]
title: Concept - Neighbor Discovery Protocol
type: concept
uid: 2025-11-22T15:00:08Z
updated: 2025-11-22T15:00:08Z
---

## Neighbor Discovery Protocol

**Summary:** The Neighbor Discovery Protocol (NDP) is the IPv6 protocol used to determine the link-layer addresses for neighbors on the same network link, replacing the functionality of ARP in IPv4.

**Details:**
Specifically, it uses ICMPv6 multicast messages for neighbor solicitation and advertisement to resolve IP addresses to MAC addresses. It also handles router discovery and parameter discovery.
