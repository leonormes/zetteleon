---
aliases: ["WAF"]
confidence: 0.9
created: 2025-10-31T10:35:00Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T10:35:00Z
purpose: "Explain WAF functionality."
review_interval: 90
see_also: ["Data-Centric Networking Focuses on Packet Journey Through Devices.md"]
source_of_truth: []
status: seedling
tags: [networking, security, web]
title: Web Application Firewalls Protect Against Layer 7 Attacks
type: concept
uid: 
updated: 
---

## Web Application Firewalls Protect Against Layer 7 Attacks

**Summary:** WAFs inspect HTTP/HTTPS traffic to block application-layer attacks like SQL injection and XSS.

**Key functions:**
- Layer 7 traffic inspection
- Security rule enforcement
- OWASP Top 10 mitigation
- Detailed logging

**Example packet flow:**
1. POST <https://myapp.com/login> with SQLi payload
2. WAF detects ' OR '1'='1 pattern
3. Blocks request with 403 Forbidden

**Limitations:**
- Not a network firewall
- No replacement for secure coding
- Focused only on web traffic
