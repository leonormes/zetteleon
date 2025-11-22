---
aliases: [MTU vs MSS]
confidence: 1.0
created: 2025-11-22T15:00:05Z
epistemic: fact
last_reviewed: 2025-11-22
modified: 2025-11-22T14:41:50Z
purpose: "Clarifies the distinction between Layer 2 and Layer 4 payload limits."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [networking/protocol]
title: Concept - Maximum Transmission Unit vs Maximum Segment Size
type: concept
uid: 2025-11-22T15:00:05Z
updated: 2025-11-22T15:00:05Z
---

## Maximum Transmission Unit Vs Maximum Segment Size

**Summary:** Maximum Transmission Unit (MTU) determines the largest physical frame size a network interface can transmit, while Maximum Segment Size (MSS) determines the largest TCP payload that fits within that frame.

**Details:**
-   **MTU (Layer 2):** The hard limit for the total size of an Ethernet frame (typically 1500 bytes). If a packet exceeds this, it must be fragmented or dropped.
-   **MSS (Layer 4):** The limit for the user data inside a single TCP segment. It is calculated as `MTU - (IP Header + TCP Header)`.
During the TCP handshake, peers advertise their MSS to ensure they don't send segments larger than the other side can receive.
