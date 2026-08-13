---
aliases: [MTU vs MSS]
conformant: false
created: 2025-11-22T15:00:05+00:00
modified: 2026-08-13T10:56:51+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/concept-maximum-transmission-unit-vs-maximum-segment-size
tags: [SoftwareEngineering/networking/protocol]
title: Concept - Maximum Transmission Unit vs Maximum Segment Size
type: claim
---

## Maximum Transmission Unit Vs Maximum Segment Size

Summary: Maximum Transmission Unit (MTU) determines the largest physical frame size a network interface can transmit, while Maximum Segment Size (MSS) determines the largest TCP payload that fits within that frame.

Details:

- MTU (Layer 2): The hard limit for the total size of an Ethernet frame (typically 1500 bytes). If a packet exceeds this, it must be fragmented or dropped.
- MSS (Layer 4): The limit for the user data inside a single TCP segment. It is calculated as `MTU - (IP Header + TCP Header)`.
During the TCP handshake, peers advertise their MSS to ensure they don't send segments larger than the other side can receive.
