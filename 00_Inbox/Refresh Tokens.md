---
type: atom
status: seed
kind: mechanism
source_title: "Every API Authentication Method Explained"
source_url: "https://youtube.com/watch?v=_lTECv25N2U"
created_utc: "2026-04-13T11:30:00Z"
confidence: high
tags:
  - authentication
  - tokens
  - user-experience
upstream: "[[HEAD Authentication Methods and Concepts]]"
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

- [[Access Tokens]] — supports: enables the continued use of an application as short-lived access tokens expire.
- [[SoT - Modern Authentication Standards]] — See Also.
