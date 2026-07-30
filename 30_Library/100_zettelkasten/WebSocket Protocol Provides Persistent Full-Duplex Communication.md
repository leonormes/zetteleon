---
aliases: [WebSocket, WebSocket protocol]
conformant: false
created: 2025-10-31T13:44:00+00:00
modified: 2026-07-28T09:12:53+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/web-socket-protocol-provides-persistent-full-duplex-communication
tags: [protocol, real-time, SoftwareEngineering/Networking, websocket]
title: WebSocket Protocol Provides Persistent Full-Duplex Communication
type: claim
---

## WebSocket Protocol Provides Persistent Full-Duplex Communication

Summary: WebSockets overlay TCP sockets, starting as an HTTP request and upgrading to a persistent, full-duplex connection ideal for real-time web applications.

Details:

WebSocket is a protocol that runs on top of TCP sockets, designed specifically for real-time, bidirectional communication between web browsers and servers.

Connection establishment:

1. Client sends HTTP request with upgrade headers:

   ```sh
   GET /chat HTTP/1.1
   Host: example.com
   Upgrade: websocket
   Connection: Upgrade
   ```

2. Server responds with upgrade confirmation:

   ```sh
   HTTP/1.1 101 Switching Protocols
   Upgrade: websocket
   Connection: Upgrade
   ```

3. The HTTP connection transforms into a WebSocket connection
4. Both sides can now send messages at any time

Key characteristics:

- Full-duplex: Both client and server can send messages simultaneously
- Persistent: Connection stays open until explicitly closed
- Low overhead: After initial handshake, minimal protocol overhead compared to HTTP polling
- Message-based: Frames data as discrete messages, not raw byte streams
- Built on TCP: Inherits TCP's reliability and ordering guarantees

Comparison to HTTP:

Traditional HTTP is request-response only - the server cannot initiate communication. WebSockets break this limitation, allowing true push notifications from server to client.

Comparison to raw TCP sockets:

WebSockets provide a higher-level protocol that works through firewalls and proxies (since they start as HTTP) and include message framing, making them easier to use in web contexts than raw TCP sockets.

Protocol overhead:

After the initial HTTP upgrade handshake, WebSocket messages have only 2-14 bytes of overhead per message, making them efficient for real-time data.

## Related

- [[WebSocket Use Cases for Real-Time Applications]] - The practical applications of this protocol.
- [[Stream Sockets Provide Reliable Ordered TCP Communication]] - The underlying TCP communication layer that WebSockets build upon.
