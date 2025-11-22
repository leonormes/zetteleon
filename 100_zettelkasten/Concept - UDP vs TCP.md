---
aliases: []
confidence: 1.0
created: 2025-11-22T15:00:11Z
epistemic: fact
last_reviewed: 2025-11-22
modified: 2025-11-22T14:42:51Z
purpose: "Contrasts the two primary transport layer protocols."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [networking/protocol]
title: Concept - UDP vs TCP
type: concept
uid: 2025-11-22T15:00:11Z
updated: 2025-11-22T15:00:11Z
---

## UDP Vs TCP

**Summary:** UDP (User Datagram Protocol) is a connectionless, unreliable protocol, while TCP (Transmission Control Protocol) provides reliable, ordered, and error-checked delivery.

**Details:**
-   **TCP:** Manages connections, ensures packet ordering, handles retransmissions for lost data, and performs congestion control.
-   **UDP:** operates effectively as a "fire and forget" mechanism. It does not guarantee ordering or delivery. It delivers whole datagrams rather than a stream, leaving reliability and error handling to the application layer.
