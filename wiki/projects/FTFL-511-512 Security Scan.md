---
title: FTFL-511-512 Security Scan
wiki_type: dossier
entity_kind: project
created: 2026-05-29 11:05:35+00:00
modified: 2026-06-01 22:06:18+00:00
tags:
- wiki
- dossier
- security
- ftfl
- nmap
sources:
- raw/2026-05-29-pieces-ftfl-511-512-security-scan
- raw/2026-06-01-pieces-ftfl-511-tls-cipher-remediation
- raw/2026-06-01-pieces-ftfl-512-nginx-infodisclosure
permalink: llmeon/wiki/projects/ftfl-511-512-security-scan
---

## Summary

Security scanning and analysis for FTFL-511 and FTFL-512 tickets, investigating external access to a private cluster via jumpbox in the testing subnet. Discovered Cloudflare proxy (not nginx) responding on scanned ports.

## Key Facts

> "No direct user quotes captured — analysis performed from terminal outputs." — [[2026-05-29-pieces-ftfl-511-512-security-scan]]

## Timeline

- **2026-05-29**: Ran nmap scans from jumpbox in testing subnet against private cluster resources
- **2026-05-29**: Analysed scan results — discovered Cloudflare proxy response instead of nginx on expected ports
- **2026-05-29**: Diagnosed IdentitiesOnly=yes backfiring — excluded AAD certificate authentication

## Connections

- [[FTFL-511 Nginx HTTPS Hardening]] — Predecessor ticket, HTTPS hardening work
- [[Azure-AKS]] — AKS cluster infrastructure
- [[FITFILE-Testing-Infrastructure]] — Testing environment context

## Contradictions

- None identified

## Open Questions

- Is the Cloudflare proxy intentional or a misconfiguration?
- What is the correct access path to the private cluster services?