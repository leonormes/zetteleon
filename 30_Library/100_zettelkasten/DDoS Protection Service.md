---
aliases: ["AWS Shield", "Azure DDoS Protection"]
confidence: "0.9"
created: 2025-12-24T12:00:00Z
epistemic: "fact"
last_reviewed: ""
modified: 2025-12-28T18:49:33+00:00
purpose: "Explain DDoS mitigation in cloud networking."
review_interval: "90"
see_also: ["Web Application Firewalls Protect Against Layer 7 Attacks.md"]
source_of_truth: []
status: "seedling"
tags: ["security", "topic/technology/networking"]
title: DDoS Protection Service
type: "concept"
uid: 
updated: 
---

## DDoS Protection Service

**Summary:** DDoS Protection services detect and mitigate volumetric, protocol, and application-layer attacks by absorbing and filtering malicious traffic before it reaches protected resources.

**Key Mitigation Techniques:**
- **SYN Proxy:** Intercepts SYN packets and challenges the client to prove legitimacy before establishing a connection to the backend.
- **Rate Limiting:** Restricts the number of requests per IP or globally to prevent resource exhaustion.
- **Anomaly Detection:** Uses machine learning to establish traffic baselines and flag deviations.

**Comparison:**
- **AWS:** Shield (Standard/Advanced).
- **Azure:** DDoS Protection (Basic/Standard).
