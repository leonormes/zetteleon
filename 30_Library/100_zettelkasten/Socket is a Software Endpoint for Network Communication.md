---
aliases: ["network socket", "socket endpoint"]
confidence: 0.9
created: 2025-10-31T13:35:00Z
epistemic: fact
last_reviewed: 2025-10-31
modified: 2025-11-01T09:43:58Z
purpose: "Define what a socket is in network programming."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [networking, programming, socket]
title: Socket is a Software Endpoint for Network Communication
type: concept
uid: 2025-10-31T13:35:00Z
updated: 2025-10-31T13:35:00Z
---

## Socket is a Software Endpoint for Network Communication

**Summary:** A socket is a software endpoint that enables communication between two devices over a network by combining an IP address and port number into a socket address.

**Details:**

A socket functions like a phone line - one end connects to your device, the other to another device. Once both sides are connected, a two-way conversation is established.

The socket address is formed by combining:

- **IP address**: Identifies the device on the network
- **Port number**: Identifies the specific application or service on that device

This combination works like a postal address with an apartment number (e.g., "123 Main Street, Apartment 22").

Sockets are not physical connections but software objects that serve as placeholders or endpoints. When you create a socket in code, your program talks to the operating system, which handles the actual network communication.
