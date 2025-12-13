---
aliases: []
confidence: 
created: 2025-03-13T08:35:57Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: NHS Data Compliance Controls
type:
uid: 
updated: 
version:
---

Mandatory Protections

- Enable Azure Policy with NHS England blueprints[^7][^8]
- Implement Private Link for all NHS data services
- Deploy Azure Confidential Computing for PHI processing
- Use NHS Privacy Enhancing Technology patterns for anonymization[^8]

Auditing Requirements

1. Log Analytics Workspace collecting:
    - Azure Activity Logs
    - AAD Sign-In Logs
    - Key Vault Access Logs
2. Azure Sentinel alerts for:

```kusto
AADSignInEvents 
| where RiskLevelDuringSignIn == "high"
| where UserType == "Member"
```

3. Weekly access reviews documented in NHS Data Protection Impact Assessments[^7]

[[We have a small team of developers in a small comp]]
