---
created: 2026-04-13T14:47:45+00:00
created_utc: "2026-04-13T11:30:00Z"
kind: mechanism
modified: 2026-05-26T11:44:36+00:00
source_title: "Every API Authentication Method Explained"
source_url: "https://youtube.com/watch?v=_lTECv25N2U"
status: seed
tags: [authentication, bearer-tokens, security, stateless]
title: Bearer Tokens
type: atom
upstream: "[[HEAD Authentication Methods and Concepts]]"
---

## Bearer Tokens

Bearer Tokens grant access to any entity that possesses the token, eliminating the need for server-side session storage. This stateless approach is widely used in modern APIs but requires rigorous protection, such as short expiration times and transport encryption, to prevent impersonation if the token is stolen.

### Scope & Conditions

Fundamental to stateless architectures and modern API design.

### Evidence

> "The term 'bearer' simply means whoever holds the token is allowed access… server does not need to store session state."

### Implications

- Requires rigorous protection (e.g., short expiry, HTTPS).
- Enables stateless architecture.

### Related

- [[SoT - Modern Authentication Standards]]—See Also.
- [[JSON Web Tokens (JWT)]]—supports: JWT is the most common format for bearer tokens.
