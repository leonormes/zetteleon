---
aliases: []
confidence: 
created: 2025-05-15T09:49:03Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T11:06:55Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [osi, topic/technology/networking]
title: OSI model
type:
uid: 
updated: 
version:
---

[[Layer 7 Application Layer]]

[[Layer 6 Presentation Layer]]

[[Layer 5 Session Layer]]

[[Layer 4 Transport Layer]]

[[Layer 3 Network Layer]]

[[Layer 2 Data Link Layer]]

[[Layer 1 Physical Layer]]

## HTTP/HTTPS Requests in Node.js

Here are common examples of Layer 7 protocols and their Node.js implementations:

1. **Using the built-in `http/https` module:**

```javascript
const https = require("https")
// Making a GET request
https
  .get("https://api.example.com/data", (resp) => {
    let data = ""

    // Receiving data chunks
    resp.on("data", (chunk) => {
      data += chunk
    })

    // Response completed
    resp.on("end", () => {
      console.log(JSON.parse(data))
    })
  })
  .on("error", (err) => {
    console.error("Error: " + err.message)
  })
```

2. **Using Fetch API (Node.js 18+):**

```javascript
async function fetchData() {
  try {
    const response = await fetch("https://api.example.com/data")
    const data = await response.json()
    console.log(data)
  } catch (error) {
    console.error("Error:", error)
  }
}
```

3. **Using Axios (Popular HTTP client):**

```javascript
const axios = require("axios")

// Making various types of requests
async function makeAPIcalls() {
  try {
    // GET request
    const getData = await axios.get("https://api.example.com/data")

    // POST request with data
    const postData = await axios.post("https://api.example.com/create", {
      name: "John",
      age: 30
    })

    // PUT request
    const putData = await axios.put("https://api.example.com/update/1", {
      name: "Updated Name"
    })

    // DELETE request
    const deleteData = await axios.delete("https://api.example.com/delete/1")
  } catch (error) {
    console.error("Error:", error.message)
  }
}
```

[[Layer 7 Protocol Elements in Node.js]]

## Key Points About Layer 7 in Node.js

1. **Protocol Handling:**
   - HTTP/HTTPS protocols
   - WebSocket protocol
   - FTP, SMTP (for email), etc.

2. **Data Formatting:**
   - JSON encoding/decoding
   - Form data handling
   - File uploads/downloads

3. **Authentication/Authorization:**
   - JWT tokens
   - OAuth
   - API keys

4. **Session Management:**
   - Cookies
   - Session tokens
   - State management

This layer is where your application directly interacts with the network, and Node.js provides various built-in modules and third-party packages to handle these Layer 7 protocols and functionalities. The code you write at this layer doesn't need to worry about the underlying network infrastructure (handled by layers 1-6) and focuses on application-level protocols and data formats.

Okay, let's break down how a Node.js process, specifically when using Axios to make a GET request, interacts with the lower layers of the OSI model, including Layer 6 (Presentation Layer).

## Interaction Flow

1. **Application Layer (Layer 7):**
   - You write Node.js code using Axios to make an HTTP GET request.
   - Axios abstracts away many of the lower-level details, allowing you to focus on the application logic.
   - You specify the URL, headers, and any data you want to send (though in a GET request, data is usually in the URL).

2. **Presentation Layer (Layer 6):**
   - **Data Formatting:** Axios handles the formatting of the data into a standard format (e.g., JSON).
   - **Encryption (SSL/TLS):** If you're using `https://`, Axios (or the underlying `https` module) initiates a TLS/SSL handshake. This involves:
     - Negotiating encryption algorithms.
     - Exchanging certificates to verify the server's identity.
     - Establishing a secure, encrypted connection.
   - **Compression:** The Presentation Layer might also handle data compression to reduce the amount of data transmitted over the network.

3. **Session Layer (Layer 5):**
   - The Session Layer manages the connection between your Node.js application and the server.
   - It establishes, maintains, and terminates the connection.
   - In the case of HTTP/HTTPS, this layer is often implicitly managed by the underlying TCP connection.

4. **Transport Layer (Layer 4):**
   - The Transport Layer (typically TCP) takes the data from the Session Layer and breaks it into segments.
   - It adds headers for sequencing and error checking.
   - It establishes a connection with the server's Transport Layer using a three-way handshake (SYN, SYN-ACK, ACK).
   - It ensures reliable data delivery through acknowledgments and retransmissions.

5. **Network Layer (Layer 3):**
   - The Network Layer (IP) adds IP headers to the segments, including the source and destination IP addresses.
   - It routes the packets across the network to the destination server.
   - Routers use routing tables to determine the best path for the packets.

6. **Data Link Layer (Layer 2):**
   - The Data Link Layer adds a frame header and trailer to the packets.
   - It includes the MAC addresses of the source and destination network interfaces.
   - It handles error detection and correction within the local network segment.

7. **Physical Layer (Layer 1):**
   - The Physical Layer converts the frames into electrical signals, radio waves, or light pulses.
   - It transmits the signals over the physical medium (e.g., Ethernet cable, Wi-Fi).

## Code Example and Layer Interaction

```javascript
const axios = require("axios")

async function fetchData() {
  try {
    const response = await axios.get("https://api.example.com/data", {
      headers: {
        Authorization: "Bearer token123"
      }
    })
    console.log(response.data)
  } catch (error) {
    console.error("Error:", error)
  }
}

fetchData()
```

In this example:

- **Layer 7 (Application):** You're using Axios to make an HTTP GET request to `https://api.example.com/data`. You're also setting an `Authorization` header.
- **Layer 6 (Presentation):**
  - Axios and the underlying `https` module handle the TLS/SSL encryption if the URL starts with `https://`.
  - The `Authorization` header is formatted and potentially encoded.
- **Layers 5-1:** These layers are handled by the operating system's network stack and the underlying network hardware. You don't directly interact with them in your Node.js code, but they are essential for transmitting the data across the network.

## Key Takeaways

- Node.js and libraries like Axios provide abstractions that simplify network communication.
- You primarily interact with Layer 7 (Application Layer) in your code.
- The lower layers (6-1) are handled by the operating system's network stack and network hardware.
- Encryption (SSL/TLS) is a key function of the Presentation Layer (Layer 6) and is automatically handled when using `https://`.
- Understanding the OSI model helps you understand the complete process of network communication, even though you don't directly interact with all the layers in your code.

You've hit on a very insightful point about the transition from application-specific code to the more uniform, kernel-level network operations. Let's clarify when the kernel takes over and how the layers become uniform.

## Kernel Handover

1. **Application Layer (Layer 7):**
   - This is where your JavaScript (Node.js), Python, Go, or any other application code resides.
   - You use libraries like Axios (in Node.js) or Requests (in Python) to construct HTTP requests.
   - The code is highly specific to the programming language and the libraries you use.

2. **System Call Boundary:**
   - The transition from user space (where your application runs) to kernel space occurs when your application makes a *system call*.
   - In the context of network communication, this happens when the application needs to send or receive data over the network.
   - For example, when Axios calls the underlying `http` or `https` module, which eventually uses the operating system's socket API (e.g., `socket()`, `connect()`, `send()`, `recv()`).

3. **Kernel Space (Layers 6-1):**
   - Once the system call is made, the kernel takes over.
   - The kernel's network stack handles the lower layers of the OSI model (Presentation, Session, Transport, Network, Data Link, and Physical).
   - The kernel's code is written in C (or a similar low-level language) and is responsible for managing the hardware and network interfaces.

## Uniformity in Lower Layers

1. **System Call Interface:**
   - The system call interface provides a uniform way for applications to interact with the kernel, regardless of the programming language they are written in.
   - For example, the `send()` system call takes a socket descriptor, a buffer of data, and a length as arguments. These arguments are passed to the kernel in a standardized way.

2. **Socket Abstraction:**
   - Sockets provide a uniform abstraction for network communication.
   - Whether you're using sockets in Node.js, Python, or Go, the underlying socket operations are the same.
   - The kernel manages the socket resources and handles the details of sending and receiving data.

3. **Protocol Implementation:**
   - The kernel implements the standard network protocols (TCP, IP, Ethernet, etc.) in a uniform way.
   - Regardless of the application that is using the network, the kernel's implementation of these protocols is the same.

## Example: Node.js vs. Python

Let's illustrate this with a Node.js and a Python example:

**Node.js (using Axios):**

```javascript
const axios = require("axios")

async function fetchData() {
  try {
    const response = await axios.get("https://api.example.com/data")
    console.log(response.data)
  } catch (error) {
    console.error("Error:", error)
  }
}

fetchData()
```

**Python (using Requests):**

```python
import requests

def fetch_data():
  try:
    response = requests.get('https://api.example.com/data')
    print(response.json())
  except Exception as e:
    print(f"Error: {e}")

fetch_data()
```

In both cases:

- The code at Layer 7 (Application Layer) is syntactically different.
- However, both programs make a system call to the kernel to initiate the HTTP request.
- The kernel then handles the lower layers of the OSI model in a uniform way, regardless of whether the request came from Node.js or Python.

## Summary

- The kernel takes over when your application makes a system call to perform network operations.
- The system call interface provides a uniform way for applications to interact with the kernel.
- The kernel implements the standard network protocols in a uniform way, regardless of the application that is using the network.
- The socket abstraction provides a uniform way for applications to manage network connections.
- This uniformity allows applications written in different programming languages to communicate with each other over the network.
