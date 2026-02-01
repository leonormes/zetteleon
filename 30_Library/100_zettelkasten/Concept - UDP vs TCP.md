---
aliases: []
created: 2025-11-22T15:00:11Z
last_reviewed: "2025-11-22"
modified: 2026-02-01T15:08:35+00:00
status: "seedling"
tags: ["SoftwareEngineering/networking/protocol"]
title: Concept - UDP vs TCP
type: "concept"
updated: 
---

## UDP Vs TCP

Summary: UDP (User Datagram Protocol) is a connectionless, unreliable protocol, while TCP (Transmission Control Protocol) provides reliable, ordered, and error-checked delivery.

Details:

- TCP: Manages connections, ensures packet ordering, handles retransmissions for lost data, and performs congestion control.
- UDP: operates effectively as a "fire and forget" mechanism. It does not guarantee ordering or delivery. It delivers whole datagrams rather than a stream, leaving reliability and error handling to the application layer.
