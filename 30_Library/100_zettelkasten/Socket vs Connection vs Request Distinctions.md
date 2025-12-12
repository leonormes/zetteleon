---
aliases: []
confidence: 0.9
created: 2025-10-31T13:36:00Z
epistemic: fact
last_reviewed: 2025-10-31
modified: 2025-11-01T09:43:58Z
purpose: "Clarify the distinctions between socket, connection, and request."
review_interval: 90
see_also: ["Socket is a Software Endpoint for Network Communication.md"]
source_of_truth: []
status: seedling
tags: [http, networking, socket, terminology]
title: Socket vs Connection vs Request Distinctions
type: concept
uid: 2025-10-31T13:36:00Z
updated: 2025-10-31T13:36:00Z
---

## Socket Vs Connection Vs Request Distinctions

**Summary:** A socket is a communication endpoint; a connection is an established socket between client and server; a request is a message sent within that connection.

**Details:**

These three terms are often confused but have distinct meanings:

- **Socket**: A communication endpoint (like a pipe). It stays open for the entire duration of communication.
- **Connection**: When a client establishes a TCP connection through a socket to a server, the connection itself is the socket in use. The terms can be used interchangeably in this context.
- **Request**: What travels inside the connection. It could be:
  - An HTTP GET request to load a web page
  - An HTTP POST request to submit form data
  - A WebSocket message for real-time communication

**Relationship:**
- One client connection = one socket
- That socket may handle one or more requests depending on the protocol:
  - HTTP/1.0: one connection = one request
  - HTTP/1.1 with keepalive: multiple requests per connection
  - HTTP/2: multiple concurrent requests per connection
  - WebSockets: persistent bidirectional messaging
