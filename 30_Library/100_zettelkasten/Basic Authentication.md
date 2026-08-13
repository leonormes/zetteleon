---
created: 2026-04-13T14:47:45+00:00
created_utc: '2026-04-13T11:30:00Z'
kind: mechanism
modified: 2026-08-13T10:54:42+00:00
permalink: llmeon/30-library/100-zettelkasten/basic-authentication
source_title: Every API Authentication Method Explained
source_url: https://youtube.com/watch?v=_lTECv25N2U
status: seed
tags: [authentication, basic-auth, http, security]
title: Basic Authentication
type: atom
upstream: '[[HEAD Authentication Methods and Concepts]]'
---

## Basic Authentication

Basic Authentication transmits user credentials as a Base64-encoded string within the HTTP authorisation header of every request. Due to the lack of encryption in the encoding itself, this method requires HTTPS to prevent credential interception and is generally avoided in modern production environments.

### Scope & Conditions

Requires HTTPS for minimal security. It is suitable for legacy systems or simple internal tools but carries a high risk of credential exposure if transport security fails.

### Evidence

> "The client sends a username and password with every HTTP request via the authorisation header. The credentials are only Base64 encoded…"

### Implications

- High risk of credential exposure if transport security fails.
- Simplest implementation for legacy systems.

### Related

- [[SoT - Modern Authentication Standards]]—See Also.
