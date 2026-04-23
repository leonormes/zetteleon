---
created: 2026-04-14T20:25:31+00:00
created_utc: "2026-04-14T13:00:00Z"
kind: constraint
modified: 2026-04-22T16:15:48+00:00
source_title: "Azure Entra Identity Best Practices & Remediation Plan"
source_url: "https://gemini.google.com/app/90721765fb79ed7a"
status: seed
tags: [access-control, directory-hardening, governance]
title: Directory Creation Restrictions
type: atom
upstream: "[[SoT - Microsoft Entra Identity]]"
---

## Directory Creation Restrictions

Non-administrative users should be restricted from performing directory-level actions such as creating security groups, registering new applications, or consenting to third-party applications. These restrictions prevent the proliferation of "shadow IT" and limit the ability of an attacker to move laterally through user-controlled assets.

### Scope & Conditions

Standard hardening protocol for tenant-wide directory settings.

### Evidence

> "Restrict the ability for non-admin users to create security groups, register applications, create new tenants, or consent to third-party applications."

### Implications

- Ensures that all group and application lifecycles remain under the oversight of trained administrators.
- Prevents users from accidentally or intentionally granting broad permissions to unvetted external applications.

### Related

- [[SoT - Microsoft Entra Identity]]—shared mechanism: identifies group and application management as core administrative functions.
- [[SoT - Microsoft Entra Application Model]]—See Also.

### See Also

- [[Least Privilege (General Engineering Principle)]]
