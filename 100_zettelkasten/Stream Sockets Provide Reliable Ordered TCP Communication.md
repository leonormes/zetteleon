---
aliases: ["stream sockets", "TCP sockets"]
confidence: 0.9
created: 2025-10-31T13:37:00Z
epistemic: fact
last_reviewed: 2025-10-31
modified: 2025-11-01T09:43:58Z
purpose: "Explain stream sockets and TCP characteristics."
review_interval: 90
see_also: ["Datagram Sockets Provide Fast Unreliable UDP Communication.md"]
source_of_truth: []
status: seedling
tags: [networking, protocol, socket, tcp]
title: Stream Sockets Provide Reliable Ordered TCP Communication
type: concept
uid: 2025-10-31T13:37:00Z
updated: 2025-10-31T13:37:00Z
---

## Stream Sockets Provide Reliable Ordered TCP Communication

**Summary:** Stream sockets (TCP sockets) provide reliable, ordered communication similar to a phone call, ensuring data arrives in the correct sequence without loss.

**Details:**

Stream sockets use the TCP (Transmission Control Protocol) to guarantee:

- **Reliability**: Data packets are acknowledged and retransmitted if lost
- **Ordering**: Packets arrive in the same sequence they were sent
- **Error checking**: Built-in mechanisms to detect and correct transmission errors

The communication model resembles a phone call - once the connection is established, both parties can reliably exchange information in a continuous stream.

**Use Cases:**
- Video streaming (e.g., Netflix) - requires data to arrive in order without glitches
- Web browsing (HTTP/HTTPS)
- File transfers (FTP, SFTP)
- Email protocols (SMTP, IMAP)
- Any application where data integrity and order are critical

The trade-off for reliability is slightly higher latency and overhead compared to datagram sockets.
