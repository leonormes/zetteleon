---
type: atom
status: seed
kind: definition
source_title: "Every API Authentication Method Explained"
source_url: "https://youtube.com/watch?v=_lTECv25N2U"
created_utc: "2026-04-13T11:30:00Z"
confidence: high
tags:
  - authorisation
  - oauth2
  - security
  - framework
upstream: "[[HEAD Authentication Methods and Concepts]]"
---

## OAuth 2.0

OAuth 2.0 is an industry-standard authorisation framework that allows applications to access resources on behalf of a user without the application ever seeing the user's password. It focuses specifically on authorisation ("What can you do?") rather than identity verification ("Who are you?").

### Scope & Conditions

The foundational framework for modern third-party integrations and API security.

### Evidence

> "Allows applications to access resources on behalf of a user without seeing the user's password... focuses solely on authorisation, not identity verification."

### Implications

- Industry standard for third-party integrations.
- Requires an additional layer (like OIDC) for identity.

### Related

- [[SoT - Modern Authentication Standards]] — direct concept match: provides the canonical definition of OAuth 2.0 as an authorisation framework.
- [[OpenID Connect (OIDC)]] — supports: OIDC adds the identity layer that OAuth 2.0 lacks.
