---
aliases: [Hostname-based Routing, Layer 7 Routing]
conformant: false
created: 2025-10-31T09:25:24+00:00
modified: 2026-07-28T09:12:45+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/content-switching-allows-layer-7-routing-based-on-hostname-or-url-path
tags: [load-balancing, SoftwareEngineering/Networking]
title: Content Switching Allows Layer 7 Routing Based on Hostname or URL Path
type: claim
---

## Content Switching Allows Layer 7 Routing Based on Hostname or URL Path

Summary: Content switching is an Application Load Balancer (Layer 7) feature that routes incoming traffic to different backend servers based on application-level data, such as the HTTP Host header or URL path.

Details: Unlike a Layer 4 load balancer that can only route based on IP address and port, a Layer 7 load balancer inspects the content of the request. This enables more intelligent routing decisions. For example, it can route requests for `images.example.com` to a pool of servers optimized for image hosting, while requests for `api.example.com` go to the application servers. This is the mechanism that allows a single load balancer to serve multiple different websites or services from one IP address and port.
