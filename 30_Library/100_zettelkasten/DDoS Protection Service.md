---
aliases:
- AWS Shield
- Azure DDoS Protection
created: 2025-12-24 12:00:00+00:00
modified: 2026-07-11 12:34:00+01:00
permalink: llmeon/30-library/100-zettelkasten/ddo-s-protection-service
tags:
- SoftwareEngineering/Networking
- SoftwareEngineering/Security
title: DDoS Protection Service
prodos:
  kind: atomic
  atomic:
    form: concept
  lifecycle: seedling
  review:
    last_reviewed: ''
---


## DDoS Protection Service

Summary: DDoS Protection services detect and mitigate volumetric, protocol, and application-layer attacks by absorbing and filtering malicious traffic before it reaches protected resources.

Key Mitigation Techniques:

- SYN Proxy: Intercepts SYN packets and challenges the client to prove legitimacy before establishing a connection to the backend.
- Rate Limiting: Restricts the number of requests per IP or globally to prevent resource exhaustion.
- Anomaly Detection: Uses machine learning to establish traffic baselines and flag deviations.

Comparison:

- AWS: Shield (Standard/Advanced).
- Azure: DDoS Protection (Basic/Standard).
