---
aliases: []
created: 2025-03-13T08:36:24Z
last_reviewed: ""
modified: 2026-02-01T15:08:18+00:00
status: ""
tags: ["IAM"]
title: Break-Glass Identity Architecture
type: ""
updated: 
---

Root Emergency Account

- Create 2 cloud-only accounts (.onmicrosoft.com) with permanent Global Admin rights
- Secure with FIDO2 security keys (2 keys per account, 4 total)
- Exclude from all Conditional Access policies except dedicated break-glass CA rules
- Store credentials in physically secured safe accessible only to company owner
- Enable Azure AD Privileged Identity Management for usage monitoring

[[We have a small team of developers in a small comp]]
