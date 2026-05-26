---
created: 2026-04-14T20:24:52+00:00
created_utc: "2026-04-14T13:00:00Z"
kind: procedure
modified: 2026-05-26T11:44:33+00:00
source_title: "Azure Entra Identity Best Practices & Remediation Plan"
source_url: "https://gemini.google.com/app/90721765fb79ed7a"
status: seed
tags: [identity, mfa, phishing-resistance, security]
title: Phishing-Resistant MFA
type: atom
upstream: "[[SoT - Microsoft Entra Identity]]"
---

## Phishing-Resistant MFA

Organisations should transition to phishing-resistant Multi-Factor Authentication (MFA) methods such as FIDO2 security keys, Windows Hello for Business, or certificate-based passkeys. These methods provide significantly higher security than traditional SMS or voice-based MFA by eliminating the possibility of credential interception or social engineering at the authentication step.

### Scope & Conditions

Applies to all user accounts, with absolute priority given to those with privileged or administrative access.

### Evidence

> "Microsoft now strongly recommends FIDO2 security keys (like YubiKeys), Windows Hello for Business, or Microsoft Authenticator (certificate-based/Passkeys)."

### Implications

- Mitigates the risk of credential stuffing and sophisticated man-in-the-middle phishing attacks.
- Reduces organizational reliance on insecure legacy communication channels for identity verification.

### Related

- [[SoT - Microsoft Entra Identity]]—direct concept match: lists FIDO2 and passwordless as core authentication pillars.
- [[Encryption vs Digital Signatures - Confidentiality vs Authenticity]]—shared mechanism: certificate-based passkeys rely on the same cryptographic principles.

### See Also

- [[SoT - Zero Trust Architecture]]
