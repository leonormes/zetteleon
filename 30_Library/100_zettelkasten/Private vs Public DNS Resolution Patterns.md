---
aliases: [DNS Resolution Patterns]
confidence:
created: 2025-07-16T17:30:03Z
epistemic:
last_reviewed:
modified: 2025-10-30T15:36:27Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: ["security", "topic/technology/networking/dns"]
title: Private vs Public DNS Resolution Patterns
type:
uid:
updated:
version:
---

There is a fundamental architectural difference between resolving private and public DNS names.

## Private Resolution

- **Goal**: Securely resolve internal hostnames without public exposure.
- **Mechanism**: Uses [[Private DNS Zones Provide Internal Network Name Resolution|private DNS zones]] and a [[Hybrid Cloud DNS Resolution Flow]]. Traffic is routed over private connections like VPN or ExpressRoute.
- **Security**: Exposing a private resolver's IP address on the public internet would be a significant security vulnerability. The entire resolution path is kept internal.

## Public Resolution

- **Goal**: Allow global access to a service over the internet.
- **Mechanism**: A public DNS record (e.g., `app.example.com`) points to a public IP address, typically of a cloud load balancer or firewall.
- **Security**: The public endpoint is designed to be internet-facing and is protected by services like a Web Application Firewall (WAF).

Understanding this distinction is key to designing secure and efficient network architectures. The use of a private TLD like `privatelink.fitfile.net` is a clear signal that the private pattern is intended. This relates to the broader topic of how [[DNS is a distributed database]] with different accessibility scopes.
