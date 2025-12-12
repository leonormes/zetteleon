---
aliases: ["datagram sockets", "UDP sockets"]
confidence: 0.9
created: 2025-10-31T13:38:00Z
epistemic: fact
last_reviewed: 2025-10-31
modified: 2025-11-01T09:43:56Z
purpose: "Explain datagram sockets and UDP characteristics."
review_interval: 90
see_also: ["Stream Sockets Provide Reliable Ordered TCP Communication.md"]
source_of_truth: []
status: seedling
tags: [networking, protocol, socket, udp]
title: Datagram Sockets Provide Fast Unreliable UDP Communication
type: concept
uid: 2025-10-31T13:38:00Z
updated: 2025-10-31T13:38:00Z
---

## Datagram Sockets Provide Fast Unreliable UDP Communication

**Summary:** Datagram sockets (UDP sockets) provide fast transmission where some packets may be lost, prioritizing speed over guaranteed delivery.

**Details:**

Datagram sockets use UDP (User Datagram Protocol) which offers:

- **Speed**: Minimal overhead and low latency
- **No connection establishment**: Fire-and-forget messaging
- **No delivery guarantee**: Packets may arrive out of order, duplicated, or not at all
- **No error correction**: The application layer must handle any errors

Unlike stream sockets, UDP doesn't establish a persistent connection - it simply sends individual packets (datagrams) to their destination.

**Use Cases:**
- Multiplayer gaming - speed matters more than perfect accuracy (a missed shot is acceptable, lag is not)
- Live video/audio streaming - dropping a frame is better than delaying the stream
- DNS queries - small, simple request-response where retry is easy
- IoT sensor data - recent data is more valuable than old data
- Voice over IP (VoIP) - real-time communication where slight quality loss is acceptable

The trade-off for speed is the lack of reliability guarantees, making it suitable only for applications that can tolerate some data loss.
