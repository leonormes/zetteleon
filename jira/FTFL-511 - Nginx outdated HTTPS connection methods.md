---
title: '[API-5] Nginx allows outdated HTTPS connection methods'
type: jira-ticket
tags:
- jira
- fitfile
- ftfl-511
- security
- nginx
- tls
- api
status: To Do
priority: High
issue_id: '28766'
issue_key: FTFL-511
url: https://fitfile.atlassian.net/browse/FTFL-511
api_control: API-5
created: 2026-05-07
permalink: llmeon/jira/ftfl-511-nginx-outdated-https-connection-methods
---

# FTFL-511: [API-5] Nginx allows outdated HTTPS connection methods

## Metadata

| Field       | Value |
|-------------|-------|
| **Key**     | FTFL-511 |
| **Issue ID** | 28766 |
| **Type**    | Security / Infrastructure |
| **Status**  | To Do |
| **Priority** | High |
| **Created** | 2026-05-07T12:25:45+0100 |
| **URL**     | [FTFL-511](https://fitfile.atlassian.net/browse/FTFL-511) |
| **API Control** | API-5 |
| **Report**  | [SharePoint Assessment Report](https://fitfileltd.sharepoint.com/:b:/s/FitfileTeam/IQD*mi2t-qYxTaz9IyQ4c7uTAVY-IRoSIUweZLh9-aQb7u4) |

## Summary

Nginx API server accepts outdated and suboptimal HTTPS cipher suites, including CBC-mode encryption, RSA key exchange, and non-forward-secrecy configurations.

## Description

### Problem

Several ciphers are accepted by the API server when connecting over HTTPS that are considered outdated or suboptimal by modern standards because they:

- Rely on **CBC-mode encryption** — vulnerable to padding oracle attacks, slower and less secure than GCM-mode (authenticated encryption)
- Use **RSA key exchange** (`TLS_RSA_*`) — no perfect forward secrecy (PFS), meaning if the server's private key is ever compromised, all past communications could be decrypted
- Use **SHA-1/SHA-2 variants** that don't provide forward secrecy guarantees in some contexts

Only **ECDHE** (Elliptic Curve Diffie-Hellman Ephemeral) variants provide PFS, but many still use CBC instead of the more secure AEAD modes like AES-GCM.

### Scan Results — 20 Accepted Cipher Suites

| Cipher Suite | Key Size | Notes |
|---|---|---|
| TLS_RSA_WITH_AES_256_GCM_SHA384 | 256-bit | RSA key exchange (no PFS) |
| TLS_RSA_WITH_AES_256_CBC_SHA256 | 256-bit | CBC + RSA key exchange |
| TLS_RSA_WITH_AES_256_CBC_SHA | 256-bit | CBC + RSA key exchange |
| TLS_RSA_WITH_AES_128_GCM_SHA256 | 128-bit | RSA key exchange (no PFS) |
| TLS_RSA_WITH_AES_128_CBC_SHA256 | 128-bit | CBC + RSA key exchange |
| TLS_RSA_WITH_AES_128_CBC_SHA | 128-bit | CBC + RSA key exchange |
| TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 | 256-bit | ✅ ECDHE (PFS), X25519 (253-bit) |
| TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | 256-bit | ✅ ECDHE (PFS) + AEAD, secp256r1 |
| TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384 | 256-bit | ECDHE (PFS) but CBC mode |
| TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA | 256-bit | ECDHE (PFS) but CBC mode |

*(10 additional cipher suites truncated — 20 total accepted)*

## Remediation Recommendations

### 1. Remove all `TLS_RSA_*` cipher suites (6 listed above)
These offer no forward secrecy. Replace with ECDHE variants.

### 2. Remove all CBC-mode cipher suites
- `AES_128_CBC`, `AES_256_CBC` — vulnerable to padding oracle attacks (BEAST, Lucky13, POODLE)

### 3. Keep only AEAD cipher suites
Recommended modern cipher list:
```
TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256
```

### 4. Nginx configuration example
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
ssl_prefer_server_ciphers on;
```

## Related Standards
- **API-5**: Security assessment control
- NIST SP 800-52 Rev. 2: Guidelines for TLS configuration
- Mozilla SSL Configuration Generator (Modern profile)

## Comments
_Comments retrieved from Jira — last updated 2026-05-07T12:25:45+0100 (single comment)_

## Actions Required
- [ ] Review current Nginx SSL/TLS configuration across all environments
- [ ] Restrict cipher suites to AEAD-only (GCM + ChaCha20-Poly1305)
- [ ] Disable TLS < 1.2
- [ ] Re-run security scan to confirm remediation
- [ ] Document agreed cipher suite policy