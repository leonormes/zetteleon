---
aliases: ["Hostname-based Routing", "Layer 7 Routing"]
confidence: 0.9
created: 2025-10-31T09:25:24Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T09:31:41Z
purpose: "Define Layer 7 routing in the context of load balancing."
review_interval: 90
see_also: ["A Load Balancer Distributes Traffic for Reliability and Scale.md"]
source_of_truth: []
status: seedling
tags: [load-balancing, networking]
title: Content Switching Allows Layer 7 Routing Based on Hostname or URL Path
type: concept
uid: 
updated: 
---

## Content Switching Allows Layer 7 Routing Based on Hostname or URL Path

**Summary:** Content switching is an Application Load Balancer (Layer 7) feature that routes incoming traffic to different backend servers based on application-level data, such as the HTTP Host header or URL path.

**Details:** Unlike a Layer 4 load balancer that can only route based on IP address and port, a Layer 7 load balancer inspects the content of the request. This enables more intelligent routing decisions. For example, it can route requests for `images.example.com` to a pool of servers optimized for image hosting, while requests for `api.example.com` go to the application servers. This is the mechanism that allows a single load balancer to serve multiple different websites or services from one IP address and port.
