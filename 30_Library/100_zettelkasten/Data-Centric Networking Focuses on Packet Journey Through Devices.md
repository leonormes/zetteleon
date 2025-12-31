---
aliases: []
confidence: "0.9"
created: 2025-10-31T10:30:00Z
epistemic: "fact"
last_reviewed: ""
modified: 2025-12-31T23:08:54+00:00
purpose: "Explain data-centric approach to understanding network devices."
review_interval: "90"
see_also: []
source_of_truth: []
status: "seedling"
tags: ["methodology", "topic/technology/networking"]
title: Data-Centric Networking Focuses on Packet Journey Through Devices
type: "concept"
uid: 
updated: 
---

## Data-Centric Networking Focuses on Packet Journey Through Devices

**Summary:** A data-centric approach to networking examines how packets flow through and are transformed by each network device, providing deeper understanding than device-centric perspectives.

**Key aspects:**

- Follows packet lifecycle from source to destination
- Examines transformations at each hop
- Reveals policy enforcement points
- Shows how devices complement each other

## Example Transformations

### 1. Load Balancer (Layer 7)

- **Incoming:** `Source: Client IP` | `Dest: LB Public IP` | `Port: 443`
- **Transformation:** LB terminates TLS, parses headers, selects target.
- **Outgoing:** `Source: LB Internal IP` | `Dest: Target IP` | `Port: 8080` (with `X-Forwarded-For` header).

### 2. NAT Gateway (Egress)

- **Incoming:** `Source: Private IP` | `Dest: External IP`
- **Transformation:** Gateway maps Private IP:Port to its own Public IP:Ephemeral Port in a state table.
- **Outgoing:** `Source: Gateway Public IP` | `Dest: External IP`

### 3. VPN Gateway (Encapsulation)

- **Incoming:** `Source: Private IP` | `Dest: Remote IP`
- **Transformation:** Gateway encrypts payload (AES) and wraps it in an **ESP (IPsec)** header.
- **Outgoing:** `Source: Gateway Public IP` | `Dest: Remote VPN IP` (Protocol 50).

### 4. API Gateway (Management)

- **Transformation:** Injects `X-Correlation-ID`, validates JWT, and routes based on URI path (e.g., `/api/v1/orders` -> `orders-service`).

**Benefits:**
- Clarifies each device's role
- Shows interdependencies
- Highlights security boundaries
