---
created: 2026-04-14T20:25:26+00:00
created_utc: '2026-04-14T13:00:00Z'
kind: failure_mode
modified: 2026-08-13T10:56:59+00:00
permalink: llmeon/30-library/100-zettelkasten/shared-account-interactive-access-restriction
source_title: Azure Entra Identity Best Practices & Remediation Plan
source_url: https://gemini.google.com/app/90721765fb79ed7a
status: seed
tags: [access-control, hardening, security, service-accounts]
title: Shared Account Interactive Access Restriction
type: atom
upstream: '[[SoT - Microsoft Entra Identity]]'
---

## Shared Account Interactive Access Restriction

Interactive sign-in should be disabled for all service and shared accounts to prevent unauthorized human access to identities intended for automation. Allowing human login to these accounts circumvents individual accountability and increases the risk of credential leakage.

### Scope & Conditions

Standard security hardening for any shared infrastructure or service identity.

### Evidence

> "Disable interactive sign-in for all service or shared accounts (e.g., fitfile-service, support, appleid)."

### Implications

- Forces the adoption of secure, token-based or workload-based authentication for all automated processes.
- Reduces the attack surface of automated identities by ensuring they cannot be used as entry points for human attackers.

### Related

- [[SoT - Microsoft Entra Identity]]—shared mechanism: aligns with the principle of Managed Identities which lack human passwords.
- [[Workload Identity Governance]]—supports: by ensuring automated accounts remain strictly for automation.

### See Also

- [[Least Privilege (General Engineering Principle)]]
