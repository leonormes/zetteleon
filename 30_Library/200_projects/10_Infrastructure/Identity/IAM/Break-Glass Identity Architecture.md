---
aliases: []
confidence: 
created: 2025-03-13T08:36:24Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [IAM]
title: Break-Glass Identity Architecture
type: 
uid: 
updated: 
version: 
---

Root Emergency Account

- Create 2 cloud-only accounts (.onmicrosoft.com) with permanent Global Admin rights
- Secure with FIDO2 security keys (2 keys per account, 4 total)
- Exclude from all Conditional Access policies except dedicated break-glass CA rules
- Store credentials in physically secured safe accessible only to company owner
- Enable Azure AD Privileged Identity Management for usage monitoring

[[We have a small team of developers in a small comp]]
