---
created: 2026-04-13T14:47:45+00:00
created_utc: '2026-04-13T11:30:00Z'
kind: definition
modified: 2026-07-13T08:52:28+00:00
permalink: llmeon/30-library/100-zettelkasten/json-web-tokens-jwt
source_title: Every API Authentication Method Explained
source_url: https://youtube.com/watch?v=_lTECv25N2U
status: seed
tags: [authentication, digital-signatures, jwt, tokens]
title: JSON Web Tokens (JWT)
type: atom
upstream: '[[HEAD Authentication Methods and Concepts]]'
---

## JSON Web Tokens (JWT)

JSON Web Tokens (JWT) are a digitally signed format for transmitting structured JSON payloads. They allow servers to verify user information and permissions without querying a database for every request, making them a primary tool for scalable, stateless authentication.

### Scope & Conditions

Used as a token format, not an authentication protocol. Revocation before expiry typically requires additional infrastructure (e.g., blacklisting).

### Evidence

> "A JWT contains a structured JSON payload with user information and is digitally signed by the server… verify requests without having to query a database."

### Implications

- Reduces database load through self-contained validation.
- Difficult to revoke before expiry without additional infrastructure.

### Related

- [[SoT - VSO Authentication (JWT vs AppRole)]]—shared mechanism: compares JWT-based OIDC discovery with static credential methods.
- [[SoT - Modern Authentication Standards]]—extends: describes the role of the ID Token as a JWT in the OIDC flow.
- [[Bearer Tokens]]—supports: JWT is the standard implementation for bearer tokens.
