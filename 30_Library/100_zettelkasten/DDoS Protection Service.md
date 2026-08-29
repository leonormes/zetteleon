---
aliases: [AWS Shield, Azure DDoS Protection]
conformant: true
created: 2025-12-24T12:00:00+00:00
epistemic_status: high
modified: 2026-08-29T09:35:59+00:00
permalink: llmeon/30-library/100-zettelkasten/ddo-s-protection-service
prodos.kind: atomic
prodos.lifecycle: stable
proposition: "DDoS Protection services ensure network availability by filtering volumetric and application-layer attacks before they exhaust protected resources."
tags: [SoftwareEngineering/Networking, SoftwareEngineering/Security]
title: DDoS Protection Service
type: claim
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

%%[implements:: [[SoT - Network Security Architecture]]]%%
