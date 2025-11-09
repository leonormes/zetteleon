---
aliases: []
confidence: 
created: 2025-05-17T16:34:11Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [networking]
title: Layer 7 Protocol Elements in Node.js
type:
uid: 
updated: 
version:
---

Here's what represents Layer 7 in these examples:

1. **HTTP Methods:**

```javascript
// Different HTTP methods representing different operations
app.get("/api/users") // READ
app.post("/api/users") // CREATE
app.put("/api/users/1") // UPDATE
app.delete("/api/users/1") // DELETE
```

2. **Headers:**

```javascript
const axios = require("axios")

const apiCall = axios.get("https://api.example.com/data", {
  headers: {
    "Content-Type": "application/json",
    Authorization: "Bearer token123",
    Accept: "application/json",
    "User-Agent": "My Node App/1.0"
  }
})
```

3. **Status Codes (Express.js example):**

```javascript
const express = require("express")
const app = express()

app.get("/api/resource", (req, res) => {
  try {
    // Success response
    res.status(200).json({ message: "Success" })
  } catch (error) {
    // Error responses
    res.status(400).json({ error: "Bad Request" })
    res.status(401).json({ error: "Unauthorized" })
    res.status(404).json({ error: "Not Found" })
    res.status(500).json({ error: "Internal Server Error" })
  }
})
```

4. **Content Types and Data Formats:**

```javascript
const express = require("express")
const app = express()

// Handling different content types
app.use(express.json()) // for parsing application/json
app.use(express.urlencoded({ extended: true })) // for parsing application/x-www-form-urlencoded

// Sending different content types
app.get("/api/data", (req, res) => {
  res.json({ data: "JSON response" }) // application/json
  res.send("Plain text response") // text/plain
  res.sendFile("path/to/file.pdf") // application/pdf
})
```

5. **WebSocket (Real-time communication):**

```javascript
const WebSocket = require("ws")
const wss = new WebSocket.Server({ port: 8080 })

wss.on("connection", (ws) => {
  // Send data to client
  ws.send("Connected to WebSocket server")

  // Receive data from client
  ws.on("message", (message) => {
    console.log("received: %s", message)
  })
})
```

[[OSI model]]
