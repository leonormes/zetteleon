---
aliases: [L7 Routing, Virtual Hosting]
conformant: false
created: 2025-12-24T12:00:00+00:00
modified: 2026-08-29T09:36:01+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/host-based-routing-enables-virtual-hosting-in-cloud-infrastructure
tags: [cloud, http, SoftwareEngineering/Networking]
title: Host-Based Routing Enables Virtual Hosting in Cloud Infrastructure
type: claim
---

## Host-Based Routing

Host-Based Routing is a technique where an Application Load Balancer (ALB) or API Gateway uses the HTTP `Host` header to determine which backend service should receive a request. This allows multiple distinct services (e.g., `api.example.com` and `web.example.com`) to share a single public IP address.

### 🧩 How it Works

1. Public DNS: Multiple FQDNs point to the same ALB IP.
2. Request Arrival: The ALB terminates the TLS connection and inspects the `Host` header.
3. Rule Matching:
   - `Host: api.example.com` -> Forward to `api-target-group`.
   - `Host: web.example.com` -> Forward to `web-target-group`.

### 🚀 Cloud Implementations

- AWS ALB: Configured via "Listener Rules" with conditions matching the "Host header."
- Azure Application Gateway: Implemented using "Multi-site Listeners."

### 🔐 Benefits

- IP Conservation: Minimises the need for scarce IPv4 addresses.
- Logical Abstraction: The FQDN becomes a stable identifier for a service fleet, decoupling it from the underlying ephemeral infrastructure.
