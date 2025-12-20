---
aliases: []
confidence: 
created: 2025-10-22T09:55:38Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:22Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/technology/networking]
title: Show a minimal end-to-end example of data encapsul
type:
uid: 
updated: 
version:
---

Show a minimal end-to-end example of data encapsulation and transmission

Here’s a **minimal end-to-end example** showing how data encapsulation and transmission work—from user data all the way down to bits crossing the wire—based on canonical OSI/TCP-IP model explanations.

---

## 1. Scenario

You type the message:

```sh
"hello"
```

in a web browser (client) and it sends it as part of an HTTP request to a web server.

---

## 2. Application Layer (HTTP)

The browser constructs an HTTP request:

```sh
GET / HTTP/1.1
Host: example.com
User-Agent: Chrome
```

This is **application data** — the part the user or program understands.

At this point, there is **no routing or transmission metadata** — just the content to send.

---

## 3. Transport Layer (TCP)

The transport layer creates a **TCP segment** by adding its header:

```sh
[TCP Header]
Source Port: 49152
Destination Port: 80
Sequence Number: 1
Acknowledgement Number: 0
Flags: SYN
Payload: [HTTP Request]
```

This header ensures **reliable delivery** and identifies which process (port) on the server should handle the data.

Encapsulated form now:

`Segment = [TCP Header] + [HTTP Data]`.

---

## 4. Network Layer (IP)

Next, the operating system adds an **IP header** to form a packet:

```sh
[IP Header]
Source IP: 192.168.1.10
Destination IP: 93.184.216.34
Protocol: TCP
Payload: [TCP Segment]
```

Now the data can be routed across multiple networks using IP addressing.

Encapsulated form:

`Packet = [IP Header] + [TCP Segment]`.

---

## 5. Data Link Layer (Ethernet)

The Network Interface Card (NIC) wraps the IP packet in an **Ethernet frame**:

```sh
[Ethernet Header]
Source MAC: 00:1A:2B:3C:4D:5E
Destination MAC: 00:9A:BC:12:34:56
Type: IPv4
[IP Packet]
[Ethernet Trailer: CRC]
```

The Ethernet frame allows direct delivery between two machines on the same physical network segment.

Encapsulated form:

`Frame = [Ethernet Header] + [IP Packet] + [Trailer]`.

---

## 6. Physical Layer

Finally, the frame is converted into **electrical, optical, or radio signals (bits)** and transmitted through the physical medium (e.g., fiber, copper, or Wi-Fi).

At this level, data becomes **energy patterns encoding binary information** — voltages, light pulses, or EM waves.

---

## 7. Decapsulation at the Receiver

At the receiving end, the process reverses:

1. The NIC reads the **Ethernet frame**, checks the destination MAC, strips Ethernet headers/trailers.
2. The IP stack reads the **IP packet**, validates the destination IP, strips the IP header.
3. The transport layer reads the **TCP segment**, verifies sequence and ports, reassembles data.
4. The application receives the **HTTP request**, processes it, and replies.

Each layer **removes its own header** in reverse order (decapsulation).

---

## 8. Summary Table

| Layer       | Unit Name | Header Example Fields | Role                    |
| :---------- | :-------- | :-------------------- | :---------------------- |
| Application | Data      | Method, Host          | User message            |
| Transport   | Segment   | Src/Dst Port          | Reliable delivery       |
| Network     | Packet    | Src/Dst IP            | Routing across networks |
| Data Link   | Frame     | Src/Dst MAC           | Local delivery on LAN   |
| Physical    | Bits      | N/A                   | Transmission medium     |

---

This demonstrates the **data packaging lifecycle**:

each layer **adds context until transmission**, and then **peels it away** when received, ensuring end-to-end communication functions transparently across devices and media layers.
