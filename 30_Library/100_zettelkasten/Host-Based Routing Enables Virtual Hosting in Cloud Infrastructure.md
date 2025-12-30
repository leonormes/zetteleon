---
aliases: ["L7 Routing", "Virtual Hosting"]
confidence: "5/5"
created: 2025-12-24T12:00:00Z
epistemic: "technical"
last_reviewed: 2025-12-24
modified: 2025-12-30T14:11:53+00:00
purpose: "To explain how cloud infrastructure uses HTTP Host headers to route traffic to multiple services from a single IP."
review_interval: "1 year"
see_also: ["[[SoT - Cloud Networking Core Components]]"]
source_of_truth: ["[[SoT - The Data Architecture of DNS]]"]
status: "stable"
tags: ["cloud", "http", "networking"]
title: Host-Based Routing Enables Virtual Hosting in Cloud Infrastructure
type: "concept"
uid: 
updated: 
---

## Host-Based Routing

**Host-Based Routing** is a technique where an **Application Load Balancer (ALB)** or API Gateway uses the HTTP `Host` header to determine which backend service should receive a request. This allows multiple distinct services (e.g., `api.example.com` and `web.example.com`) to share a single public IP address.

### 🧩 How it Works

1. **Public DNS:** Multiple FQDNs point to the same ALB IP.
2. **Request Arrival:** The ALB terminates the TLS connection and inspects the `Host` header.
3. **Rule Matching:**
   - `Host: api.example.com` -> Forward to `api-target-group`.
   - `Host: web.example.com` -> Forward to `web-target-group`.

### 🚀 Cloud Implementations

- **AWS ALB:** Configured via "Listener Rules" with conditions matching the "Host header."
- **Azure Application Gateway:** Implemented using "Multi-site Listeners."

### 🔐 Benefits

- **IP Conservation:** Minimises the need for scarce IPv4 addresses.
- **Logical Abstraction:** The FQDN becomes a stable identifier for a service fleet, decoupling it from the underlying ephemeral infrastructure.
