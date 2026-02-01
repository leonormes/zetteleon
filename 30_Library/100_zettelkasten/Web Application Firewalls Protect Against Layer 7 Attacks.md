---
aliases: ["WAF"]
created: 2025-10-31T10:35:00Z
last_reviewed: ""
modified: 2026-02-01T15:08:24+00:00
status: "seedling"
tags: ["SoftwareEngineering/Networking", "SoftwareEngineering/Security", "web"]
title: Web Application Firewalls Protect Against Layer 7 Attacks
type: "concept"
updated: 
---

## Web Application Firewalls Protect Against Layer 7 Attacks

Summary: Web Application Firewalls (WAFs) are specialized security appliances or services designed to protect web applications and APIs by inspecting OSI Layer 7 (Application Layer) traffic, primarily HTTP/HTTPS.

Deployment Models:

- Hardware Appliances: Traditional network-based devices for data centers.
- Software/Virtual Appliances: Host-based solutions for flexible server deployments.
- Cloud-Based Services: Most common modern model (e.g., Cloudflare, AWS WAF), acting as a reverse proxy.

Key functions:

- OWASP Top 10 Mitigation: Specifically tuned to block SQL Injection, Cross-Site Scripting (XSS), and File Inclusion.
- Protocol Decoding: Analyzes HTTP requests/responses, cookie poisoning, and API manipulation.
- Bot Mitigation & API Protection: Identifies and blocks malicious automated traffic.
- Reverse Proxy Operation: Sits in front of web servers to terminate and inspect connections before they reach the application.

Example packet flow:

1. POST <https://myapp.com/login> with SQLi payload (`' OR '1'='1`)
2. WAF performs Deep Packet Inspection (DPI) on the payload.
3. WAF detects the malicious pattern.
4. Request is blocked with a 403 Forbidden before reaching the backend server.

Limitations:

- Scope: Focused only on web/API traffic; does not replace general [[Network Firewalls]].
- False Positives: Complex rules can occasionally block legitimate user traffic.
- Management: Requires continuous tuning to keep up with application changes.
