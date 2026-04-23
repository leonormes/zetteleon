---
created: 2026-04-14T20:25:14+00:00
created_utc: "2026-04-14T13:00:00Z"
kind: constraint
modified: 2026-04-22T16:16:02+00:00
source_title: "Azure Entra Identity Best Practices & Remediation Plan"
source_url: "https://gemini.google.com/app/90721765fb79ed7a"
status: seed
tags: [blast-radius, governance, identity-management]
title: Global Administrator Limit
type: atom
upstream: "[[SoT - Microsoft Entra Identity]]"
---

## Global Administrator Limit

To limit the blast radius of a compromised identity, organizations should maintain fewer than five Global Administrator accounts. Adhering to this "Rule of 5" simplifies the auditing process for high-privilege changes and forces the use of more granular, lower-privilege roles for everyday administrative tasks.

### Scope & Conditions

General governance rule for all Microsoft Entra ID tenants.

### Evidence

> "The 'Rule of 5': Microsoft recommends having fewer than five Global Administrators."

### Implications

- Reduces the surface area for catastrophic compromise within a tenant.
- Drives the adoption of role-based access control (RBAC) and least privilege principles.

### Related

- [[SoT - Microsoft Entra Identity]]—direct concept match: explicitly mentions the "Rule of 5" as a governance protocol.
- [[Byzantine Fault Tolerance Requirements]]—shared mechanism: both seek to mitigate the impact of component (account) failure.

### See Also

- [[Just-In-Time (JIT) Admin Access]]
