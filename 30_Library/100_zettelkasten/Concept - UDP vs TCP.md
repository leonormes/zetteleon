---
aliases: []
conformant: false
created: 2025-11-22T15:00:11+00:00
modified: 2026-08-08T10:29:17+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/concept-udp-vs-tcp
tags: [SoftwareEngineering/networking/protocol]
title: Concept - UDP vs TCP
type: claim
---

## UDP Vs TCP

Summary: UDP (User Datagram Protocol) is a connectionless, unreliable protocol, while TCP (Transmission Control Protocol) provides reliable, ordered, and error-checked delivery.

Details:

- TCP: Manages connections, ensures packet ordering, handles retransmissions for lost data, and performs congestion control.
- UDP: operates effectively as a "fire and forget" mechanism. It does not guarantee ordering or delivery. It delivers whole datagrams rather than a stream, leaving reliability and error handling to the application layer.
