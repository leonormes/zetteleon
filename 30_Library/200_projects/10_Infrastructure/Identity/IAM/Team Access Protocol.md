---
aliases: []
created: 2025-03-13T08:35:46Z
last_reviewed: ""
modified: 2026-02-01T15:08:17+00:00
status: ""
tags: ["IAM"]
title: Team Access Protocol
type: ""
updated: 
---

Daily Workflow

1. Developers work through Ephemeral Azure Bastion hosts
2. Code changes via branch protections:
    - Require successful `terraform plan`
    - Enforce NHS data tagging policies
3. Production deployments use Azure Managed Identities (no personal credentials)

Emergency Process

```mermaid
graph LR
A[Break-Glass Trigger] --> B{2FA Auth}
B -->|FIDO2 Key 1| C[Access Request]
C --> D[Owner SMS Approval]
D --> E[Temporary CA Policy Bypass]
E --> F[Time-bound Session]
```

This model reduces attack surface by 89% compared to individual admin accounts,[^1] while meeting NHS England's requirement for "strict access controls with data minimization".[^8] All changes remain auditable through Git commit history and Azure Activity Logs.[^5][^7]
