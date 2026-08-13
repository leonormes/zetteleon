---
created: 2026-04-14T11:11:48+00:00
created_utc: '2026-04-14T10:35:00Z'
kind: claim
modified: 2026-08-13T10:54:44+00:00
permalink: llmeon/30-library/100-zettelkasten/connectivity-specificity
source_title: Networking Is Label Transformation Under Policy
source_url: N/A
status: seed
tags: [connectivity, debugging, firewall-policy, protocols]
title: Connectivity Specificity
type: atom
upstream: '[[SoT - Network Security Architecture]]'
---

## Connectivity Specificity

Network connectivity is specific to the exact combination of destination, protocol, TLS behaviour, and policy, rather than a monolithic "up" or "down" state. "The cluster has internet" is an insufficient mental model for debugging complex failures.

### Scope & Conditions

Applicable when some services or protocols work while others fail within the same network environment.

### Evidence

> "Connectivity is specific to destination, protocol, TLS behaviour, proxy handling, SNI, and firewall policy."

### Implications

- Debugging must use tests granular to the specific protocol and destination (e.g., `curl` with SNI vs. simple `ping`).
- Success in one protocol (e.g., ICMP) does not imply success in others (e.g., HTTPS on a custom port).

### Related

- [[SoT - Zero Trust Architecture]]—shared mechanism: security decisions are made based on granular session context rather than network location.
- [[Protocol - HIE--NNUH Network Debugging]]—shared mechanism: promotes granular testing to isolate protocol-specific failures.

### See Also

- [[SoT - Network Security Architecture]]
