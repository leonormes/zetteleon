---
aliases: ["Python socket operations"]
confidence: 
created: 2025-10-31T13:39:00Z
epistemic: NA
last_reviewed: 2025-10-31
modified: 2025-11-01T09:43:58Z
purpose: "Document the standard socket lifecycle operations in Python."
review_interval: 180
see_also: []
source_of_truth: []
status: seedling
tags: [networking, programming, python, socket]
title: Socket Lifecycle in Python Programming
type: instructional
uid: 2025-10-31T13:39:00Z
updated: 2025-10-31T13:39:00Z
---

## Socket Lifecycle in Python Programming

**What:** The five-stage lifecycle for using sockets in Python: create, connect, send, receive, and close.

**How:**

**Client-side socket operations:**

1. **Create socket object**

   ```python
   import socket
   s = socket.socket()
   ```

   - Requests OS to create a communication endpoint
   - Returns a file descriptor (handle) for the socket

2. **Connect to server**

   ```python
   s.connect(('example.com', 80))
   ```

   - Initiates TCP handshake to target IP and port
   - OS handles DNS resolution, IP routing

3. **Send data**

   ```python
   s.send(b'GET / HTTP/1.1\r\n\r\n')
   ```

   - Writes bytes into kernel buffer
   - OS pushes data out to network

4. **Receive data**

   ```python
   data = s.recv(1024)
   ```

   - Reads up to 1024 bytes from kernel buffer
   - Returns data received from server

5. **Close socket**

   ```python
   s.close()
   ```

   - Releases system resources
   - Terminates the connection

**Server-side operations:**

1. Create socket
2. **Bind** to address and port: `s.bind(('0.0.0.0', 8080))`
3. **Listen** for connections: `s.listen()`
4. **Accept** client connection: `client_socket, address = s.accept()`
5. Send/receive with client socket
6. Close both client and server sockets

**Failure modes:**
- Connection refused if server not listening
- Timeout if server doesn't respond
- Broken pipe if connection lost during send/receive
- Address already in use if port is occupied

**Example:**

```python
# Simple HTTP client
import socket
s = socket.socket()
s.connect(('example.com', 80))
s.send(b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n')
response = s.recv(4096)
s.close()
print(response)
```
