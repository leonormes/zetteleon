---
aliases: []
created: 2025-11-22T15:00:00+00:00
modified: 2026-07-13T08:52:25+00:00
permalink: llmeon/30-library/100-zettelkasten/concept-tcp-three-way-handshake
tags: [SoftwareEngineering/networking/tcp]
title: Concept - TCP Three-Way Handshake
---

## TCP Three-Way Handshake

Summary: The TCP three-way handshake is the three-step process (SYN, SYN-ACK, ACK) used to establish a reliable connection between a client and server before data transfer begins.

Details:

During this handshake, both parties synchronize their initial sequence numbers and negotiate connection parameters and options.

1. SYN: The client sends a segment with the SYN flag, proposing its initial sequence number and options (e.g., MSS, SACK-permitted, Window Scale).
2. SYN-ACK: The server acknowledges the client's SYN and sends its own SYN with its sequence number and supported options.
3. ACK: The client acknowledges the server's SYN, moving the connection state to `ESTABLISHED`.
For HTTPS connections, the TLS handshake occurs only after this TCP handshake is complete.
