---
created: 2026-04-14T20:25:06+00:00
created_utc: "2026-04-14T13:00:00Z"
kind: mechanism
modified: 2026-05-26T11:44:36+00:00
source_title: "Azure Entra Identity Best Practices & Remediation Plan"
source_url: "https://gemini.google.com/app/90721765fb79ed7a"
status: seed
tags: [cae, security, session-management, zero-trust]
title: Continuous Access Evaluation (CAE)
type: atom
upstream: "[[SoT - Microsoft Entra Identity]]"
---

## Continuous Access Evaluation (CAE)

Continuous Access Evaluation (CAE) allows Microsoft Entra to revoke user sessions in near real-time when the account's security posture changes or the user's location shifts significantly. By moving beyond a fixed token lifespan, CAE ensures that critical security events—such as an account being disabled or a password reset—result in immediate session termination.

### Scope & Conditions

Requires both the identity provider (Entra) and the client service (e.g., SharePoint, Exchange) to support the CAE protocol.

### Evidence

> "Ensure CAE is enabled so that if a user's account is disabled or their location changes significantly, their session is revoked in near real-time…"

### Implications

- Dramatically reduces the window of opportunity for an attacker to use a stolen session token.
- Provides a more dynamic enforcement of zero-trust security policies by reacting to real-time signals.

### Related

- [[SoT - Zero Trust Architecture]]—direct concept match: CAE is a foundational technology for continuous verification.
- [[SoT - Microsoft Entra Identity]]—shared mechanism: identified as a critical tool for real-time risk-based access.

### See Also

- [[SoT - Network Security Architecture]]
