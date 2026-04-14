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
  - api-keys
  - application-identity
upstream: "[[HEAD Authentication Methods and Concepts]]"
---

## API Keys

API Keys are unique identifiers assigned to applications to authenticate the application itself rather than an individual user. They are frequently used for public APIs (e.g., weather or mapping services) to track usage and enforce rate limits.

### Scope & Conditions

Typically used for service-to-service communication or public data access. They offer low security for accessing sensitive user-specific data.

### Evidence

> "A unique identifier is assigned to an application... API keys typically identify the application rather than the individual user."

### Implications

- Easy to implement for rate limiting and usage tracking.
- Low security for user-specific data access.

### Related

- [[SoT - Modern Authentication Standards]] — See Also.
