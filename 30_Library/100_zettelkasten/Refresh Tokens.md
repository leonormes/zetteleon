---
created: 2026-04-13T14:47:45+00:00
created_utc: '2026-04-13T11:30:00Z'
kind: mechanism
modified: 2026-08-29T09:36:05+00:00
permalink: llmeon/30-library/100-zettelkasten/refresh-tokens
source_title: Every API Authentication Method Explained
source_url: https://youtube.com/watch?v=_lTECv25N2U
status: seed
tags: [authentication, tokens, user-experience]
title: Refresh Tokens
type: atom
upstream: '[[HEAD Authentication Methods and Concepts]]'
---

## Refresh Tokens

Refresh tokens are long-lived credentials used to obtain new access tokens once they expire, allowing users to maintain their session without being forced to repeatedly enter their credentials. Because of their longevity, they must be stored more securely than short-lived access tokens.

### Scope & Conditions

Used in conjunction with Access Tokens to improve user experience while maintaining a high security posture.

### Evidence

> "Refresh tokens are longer-lived and are used to request new access tokens without forcing the user to repeatedly enter their credentials."

### Implications

- Improves user experience by maintaining sessions.
- Increases risk if the storage medium is compromised.

### Related

- [[Access Tokens]]—supports: enables the continued use of an application as short-lived access tokens expire.
- [[SoT - Modern Authentication Standards]]—See Also.
