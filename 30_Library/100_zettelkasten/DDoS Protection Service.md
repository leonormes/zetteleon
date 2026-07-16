---
aliases: [AWS Shield, Azure DDoS Protection]
created: 2025-12-24T12:00:00+00:00
modified: 2026-07-13T08:52:25+00:00
permalink: llmeon/30-library/100-zettelkasten/ddo-s-protection-service
tags: [SoftwareEngineering/Networking, SoftwareEngineering/Security]
title: DDoS Protection Service
type: concept
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
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
