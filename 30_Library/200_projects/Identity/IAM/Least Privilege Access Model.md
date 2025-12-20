---
aliases: []
confidence: 
created: 2025-03-13T08:36:15Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Least Privilege Access Model
type:
uid: 
updated: 
version:
---

**RBAC Structure**

| Role | Scope | Members | Approval Process |
| :-- | :-- | :-- | :-- |
| **Global Reader** | Tenant | All devs | Automatic |
| **Contributor** | Resource Groups | Team Leads (2) | PR + Owner Approval |
| **Security Admin** | Entra ID | SecOps Lead | Break-Glass Access Only |
| **Key Vault Admin** | Key Vaults | CI/CD Service Account | Automated Rotation |

**Implementation Steps**

1. **Audit existing privileges** using Azure AD Access Reviews[^2]
2. **Revoke direct owner assignments** from individual accounts[^2]
3. Implement **JIT access** via PIM for elevated roles[^1]
4. Create **security groups** for role assignments (not individual users)[^1]

[[We have a small team of developers in a small comp]]
