---
aliases: []
confidence: 1.0
created: 2025-11-22T15:00:09Z
epistemic: fact
last_reviewed: 2025-11-22
modified: 2025-11-22T14:42:03Z
purpose: "Lists the interception points in the Linux networking stack."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [networking/kernel]
title: Concept - Netfilter Hooks
type: concept
uid: 2025-11-22T15:00:09Z
updated: 2025-11-22T15:00:09Z
---

## Netfilter Hooks

**Summary:** Netfilter hooks are specific points in the Linux kernel packet traversal path where software (like iptables or nftables) can register callbacks to inspect, modify, or drop packets.

**Details:**
The five standard hooks are:
-   **PREROUTING:** Triggered immediately upon packet arrival, before the routing decision.
-   **INPUT:** Triggered for packets destined for the local system.
-   **FORWARD:** Triggered for packets routed to another host.
-   **OUTPUT:** Triggered for locally generated packets before they leave.
-   **POSTROUTING:** Triggered just before packets leave the network device.
These hooks enable firewalls, NAT, and packet logging.
