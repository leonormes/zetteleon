---
aliases: [stream sockets, TCP sockets]
conformant: false
created: 2025-10-31T13:37:00+00:00
modified: 2026-08-08T10:29:24+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/stream-sockets-provide-reliable-ordered-tcp-communication
tags: [protocol, socket, SoftwareEngineering/Networking, tcp]
title: Stream Sockets Provide Reliable Ordered TCP Communication
type: claim
---

## Stream Sockets Provide Reliable Ordered TCP Communication

Summary: Stream sockets (TCP sockets) provide reliable, ordered communication similar to a phone call, ensuring data arrives in the correct sequence without loss.

Details:

Stream sockets use the TCP (Transmission Control Protocol) to guarantee:

- Reliability: Data packets are acknowledged and retransmitted if lost
- Ordering: Packets arrive in the same sequence they were sent
- Error checking: Built-in mechanisms to detect and correct transmission errors

The communication model resembles a phone call - once the connection is established, both parties can reliably exchange information in a continuous stream.

Use Cases:

- Video streaming (e.g., Netflix) - requires data to arrive in order without glitches
- Web browsing (HTTP/HTTPS)
- File transfers (FTP, SFTP)
- Email protocols (SMTP, IMAP)
- Any application where data integrity and order are critical

The trade-off for reliability is slightly higher latency and overhead compared to datagram sockets.

## Related

- [[Concept - UDP vs TCP]]
