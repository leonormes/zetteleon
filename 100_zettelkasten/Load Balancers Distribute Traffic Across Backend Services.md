---
aliases: ["ALB", "NLB"]
confidence: 0.9
created: 2025-10-31T10:32:00Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T10:42:03Z
purpose: "Explain load balancer functionality in cloud networks."
review_interval: 90
see_also: ["Data-Centric Networking Focuses on Packet Journey Through Devices.md"]
source_of_truth: []
status: seedling
tags: [cloud, networking, scalability]
title: Load Balancers Distribute Traffic Across Backend Services
type: concept
uid: 
updated: 
---

## Load Balancers Distribute Traffic Across Backend Services

**Summary:** Cloud load balancers distribute incoming traffic across multiple backend servers to ensure availability and performance.

**Key functions:**
- Health checks (monitor backend health)
- Traffic distribution algorithms (round robin, least conn)
- SSL/TLS termination
- Single entry point for services

**Example packet flow:**
1. TCP SYN to LB public IP:443
2. LB selects healthy backend (Web-Server-B)
3. May:
   - Forward directly (NLB)
   - Terminate TLS, add X-Forwarded-For (ALB)

**Limitations:**
- Not a firewall/WAF
- No API management
- No caching
