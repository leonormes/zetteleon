---
created: 2026-04-14T20:25:18+00:00
created_utc: "2026-04-14T13:00:00Z"
kind: procedure
modified: 2026-04-16T11:56:04+00:00
source_title: "Azure Entra Identity Best Practices & Remediation Plan"
source_url: "https://gemini.google.com/app/90721765fb79ed7a"
status: seed
tags: [break-glass, disaster-recovery, security-ops]
title: Emergency Access Account Protocol
type: atom
upstream: "[[SoT - Microsoft Entra Identity]]"
---

## Emergency Access Account Protocol

Organizations must maintain "break-glass" emergency access accounts that are cloud-only and excluded from standard MFA and Conditional Access policies. These accounts serve as a final recovery path if primary authentication or identity services fail; as high-risk assets, they must be rigorously monitored for any sign-in activity.

### Scope & Conditions

Used exclusively during catastrophic identity failure scenarios.

### Evidence

> "Maintain two 'Emergency Access' accounts that are excluded from MFA and Conditional Access. These should be cloud-only… and be monitored for any login activity."

### Implications

- Provides an essential recovery path during a system-wide identity lockout.
- Represents a deliberate security exception that must be mitigated by intense logging, alerting, and physical security for credentials.

### Related

- [[SoT - Microsoft Entra Identity]]—direct concept match: details the security and storage requirements for break-glass accounts.
- [[Byzantine Fault Tolerance Requirements]]—shared mechanism: both provide the necessary redundancy for survival in failure states.

### See Also

- [[Global Administrator Limit]]
