---
aliases: [ARP]
confidence: 1.0
created: 2025-11-22T15:00:03Z
epistemic: fact
last_reviewed: 2025-11-22
modified: 2025-11-22T14:41:07Z
purpose: "Defines the protocol for mapping IP addresses to MAC addresses."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [networking/protocol]
title: Concept - Address Resolution Protocol
type: concept
uid: 2025-11-22T15:00:03Z
updated: 2025-11-22T15:00:03Z
---

## Address Resolution Protocol (ARP)

**Summary:** The Address Resolution Protocol (ARP) is a communication protocol used for discovering the link layer address (MAC address) associated with a given IPv4 address.

**Details:**
When the kernel needs to send a frame to a local IP but does not know the details, it broadcasts an ARP request asking "Who has IP X?". The device with that IP replies with its MAC address. The kernel then caches this mapping to avoid repeated lookups. IPv6 uses the Neighbor Discovery Protocol (NDP) instead of ARP.
