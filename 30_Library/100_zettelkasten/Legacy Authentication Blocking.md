---
created: 2026-04-14T20:24:56+00:00
created_utc: '2026-04-14T13:00:00Z'
kind: mechanism
modified: 2026-08-08T10:29:20+00:00
permalink: llmeon/30-library/100-zettelkasten/legacy-authentication-blocking
source_title: Azure Entra Identity Best Practices & Remediation Plan
source_url: https://gemini.google.com/app/90721765fb79ed7a
status: seed
tags: [conditional-access, legacy-auth, microsoft-entra, security]
title: Legacy Authentication Blocking
type: atom
upstream: '[[SoT - Microsoft Entra Identity]]'
---

## Legacy Authentication Blocking

Blocking legacy authentication protocols (e.g., IMAP, POP3, SMTP) via Conditional Access is a critical security measure to prevent attackers from bypassing Multi-Factor Authentication. These outdated protocols do not support modern MFA challenges, making them the primary entry point for automated credential stuffing and brute-force attacks.

### Scope & Conditions

Essential for all Entra ID environments where modern authentication clients are supported and deployed.

### Evidence

> "Block outdated protocols (IMAP, POP3, SMTP) via Conditional Access. These bypass MFA and are the primary entry point for credential stuffing."

### Implications

- Closes one of the most significant and easily exploitable attack vectors in cloud identity systems.
- Mandates the use of modern, secure authentication flows (e.g., OAuth 2.0) across all client applications.

### Related

- [[SoT - Microsoft Entra Identity]]—shared mechanism: identifies Conditional Access as a core tool for dynamic security enforcement.
- [[Byzantine Fault Tolerance Requirements]]—See Also.

### See Also

- [[SoT - Network Security Architecture]]
