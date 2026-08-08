---
created: 2026-04-13T14:47:45+00:00
created_utc: '2026-04-13T11:30:00Z'
kind: definition
modified: 2026-08-08T10:29:21+00:00
permalink: llmeon/30-library/100-zettelkasten/open-id-connect-oidc
source_title: Every API Authentication Method Explained
source_url: https://youtube.com/watch?v=_lTECv25N2U
status: seed
tags: [authentication, identity, oauth2, oidc]
title: OpenID Connect (OIDC)
type: atom
upstream: '[[HEAD Authentication Methods and Concepts]]'
---

## OpenID Connect (OIDC)

OpenID Connect (OIDC) is an identity layer built on top of the OAuth 2.0 framework that provides verified user information via an ID token. It standardizes how identity is shared across different platforms, enabling modern "Sign in with…" features.

### Scope & Conditions

Enables interoperable identity management across various providers (e.g., Google, Microsoft) and applications.

### Evidence

> "An identity layer built on top of OAuth 2.0. It introduces an 'ID token' containing verified information about the user…"

### Implications

- Standardises identity across different platforms.
- Leverages OAuth 2.0 flows for secure transport.

### Related

- [[SoT - Modern Authentication Standards]]—direct concept match: defines OIDC as the standardized identity layer.
- [[OAuth 2.0]]—extends: adds authentication capabilities to the underlying authorisation framework.
- [[SoT - VSO Authentication (JWT vs AppRole)]]—shared mechanism: uses OIDC discovery for secure, ephemeral token verification.
