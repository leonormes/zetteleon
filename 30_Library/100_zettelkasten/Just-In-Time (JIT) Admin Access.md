---
created: 2026-04-14T20:25:10+00:00
created_utc: '2026-04-14T13:00:00Z'
kind: heuristic
modified: 2026-08-13T10:54:48+00:00
permalink: llmeon/30-library/100-zettelkasten/just-in-time-jit-admin-access
source_title: Azure Entra Identity Best Practices & Remediation Plan
source_url: https://gemini.google.com/app/90721765fb79ed7a
status: seed
tags: [jit, least-privilege, pim, security]
title: Just-In-Time (JIT) Admin Access
type: atom
upstream: '[[SoT - Microsoft Entra Identity]]'
---

## Just-In-Time (JIT) Admin Access

High-privilege administrative rights, such as Global Administrator, should never be assigned as permanent permissions. Instead, these roles should be configured as "Just-In-Time" (JIT) eligible roles through Microsoft Entra Privileged Identity Management (PIM). This model ensures that administrative access is granted only when needed, is time-bound, and is subject to rigorous verification.

### Scope & Conditions

Applies to all high-privilege administrative roles within an Entra tenant.

### Evidence

> "No one should have permanent 'Global Administrator' or 'Security Administrator' rights. Use Microsoft Entra Privileged Identity Management (PIM) to grant 'Just-In-Time' (JIT) access…"

### Implications

- Minimises the attack surface by reducing the number of users with standing privileged access.
- Ensures all administrative actions are explicitly activated and audited within a specific timeframe.

### Related

- [[SoT - Microsoft Entra Identity]]—direct concept match: identifies PIM/JIT as a core security feature for high-compliance environments.
- [[Least Privilege (General Engineering Principle)]]—supports: JIT is the primary mechanism for enforcing least privilege for humans.

### See Also

- [[SoT - Zero Trust Architecture]]
