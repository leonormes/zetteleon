---
title: FTFL-511 Nginx HTTPS Hardening
wiki_type: dossier
entity_kind: project
created: 2026-05-28 18:05:00+00:00
modified: 2026-06-02 02:22:11+00:00
tags:
- wiki
- dossier
sources:
- raw/2026-05-28-pieces-ftfl511-jira-ticket.md
- raw/2026-06-01-pieces-ftfl-511-tls-cipher-remediation.md
- raw/2026-06-01-pieces-ftfl-511-tls-retest
permalink: llmeon/wiki/projects/ftfl-511-nginx-https-hardening
---

## Summary

FITFILE security ticket to harden the TLS configuration of the `ingress-nginx` controller on the `sandbox-testing-1.fitfile.net` environment. Triggered by a penetration test that identified 14 outdated/insecure TLS cipher suites out of 20 accepted. Parent ticket: FTFL-510 (Pentest Actions - API), Epic: API-5, Sprint 20.

## Key Facts

- **Jira:** [FTFL-511](https://fitfile.atlassian.net/browse/FTFL-511) — "Nginx allows outdated HTTPS connection methods" — Status: In Progress, Priority: Low, Story Points: 3, Assignee: Leon Ormes, Reporter: Ollie Rushton
  > "Nginx allows outdated HTTPS connection methods" — [[raw/2026-05-28-pieces-ftfl511-jira-ticket]] (Pieces: 2cd0a5fc-9388-4ed5-9ac5-8a25a732089c)

- **Pentest source:** `FIL090226JH - API Testing v1.0.pdf` — found 20 TLS cipher suites accepted, 14 flagged as outdated/insecure across three vulnerability classes: CBC-mode ciphers (Padding Oracle attacks), RSA key exchange (no PFS), weak ECDH curves (secp521r1)
  > "14 are considered outdated or insecure. Three vulnerability classes were found: CBC-mode ciphers, RSA key exchange ciphers, Weak ECDH curves" — [[raw/2026-05-28-pieces-ftfl511-jira-ticket]] (Pieces: 2cd0a5fc-9388-4ed5-9ac5-8a25a732089c)

- **Fix attempt:** GitLab MR !757 (branch `feature/FTFL-511-nginx-all` → `master`, author Yasir Mansoor) applied `ssl-ciphers: "ECDHE+AESGCM:ECDHE+CHACHA20"`, `ssl-ecdh-curve: "X25519:secp384r1:secp256r1"`, `ssl-prefer-server-ciphers: "on"` to `charts/ingress-nginx-config/templates/configmap.yaml`
  > "ssl-ciphers: "ECDHE+AESGCM:ECDHE+CHACHA20"  # ECDHE + AEAD only" — [[raw/2026-05-28-pieces-ftfl511-jira-ticket]] (Pieces: 2cd0a5fc-9388-4ed5-9ac5-8a25a732089c)

- **MR !757 was declined** (as of 2026-05-28): The implementation was deemed incorrect — too heavy devops approach. Awaiting a DevOps engineer to re-pick.
  > "MR !757 was declined ... awaiting a DevOps engineer to re-pick" — [[raw/2026-05-28-pieces-ftfl511-jira-ticket]] (Pieces: 2cd0a5fc-9388-4ed5-9ac5-8a25a732089c)

- **MCP proxy failure during fetch:** On 2026-05-28 Hermes attempted to fetch the ticket via Jira MCP but the injected tools were not available as native calls. Raw HTTP to port 8000 timed out. User was asked to paste the ticket content — demonstrating the MCP injection gap in production.
  > "The MCP proxy timed out ... the injected tools aren't natively listed" — [[raw/2026-05-28-pieces-hermes-mcp-proxy-fix]] (Pieces: 577c3a10-8547-4a61-b115-2f724012ed55)

- **2026-06-01T11:21** — nmap scan from local machine confirmed clean TLS — only AEAD suites (ECDHE+AESGCM, ECDHE+CHACHA20), no CBC, no RSA key exchange, cipher preference server, grade A
  > "nmap scan from local machine confirmed clean TLS — only AEAD suites (ECDHE+AESGCM, ECDHE+CHACHA20), no CBC, no RSA key exchange, cipher preference server, grade A" — [[raw/2026-06-01-pieces-ftfl-511-tls-cipher-remediation]] (Pieces: ec9c756a-55c3-4760-9b16-f0da1bcf9f6c)
- **2026-06-01T08:53** — Jumpbox nmap scan confirmed only 3 TLSv1.2 AEAD ciphers (GCM + ChaCha20) and 3 TLSv1.3 suites; A grade; server controls cipher preference
  > "Jumpbox nmap scan confirmed clean TLS — 3 AEAD suites, A grade" — [[raw/2026-06-01-pieces-ftfl-511-tls-retest]] (Pieces: 480f2d8a-ccf4-4b1d-9d04-a75b69c29a7d)
- **2026-06-01T08:53** — nmap scan from local machine confirmed clean TLS — only AEAD suites (ECDHE+AESGCM, ECDHE+CHACHA20), no CBC, no RSA key exchange, cipher preference server, grade A
  > "nmap scan from local machine confirmed clean TLS — only AEAD suites (ECDHE+AESGCM, ECDHE+CHACHA20), no CBC, no RSA key exchange, cipher preference server, grade A" — [[raw/2026-06-01-pieces-ftfl-511-tls-cipher-remediation]] (Pieces: 92b022c0-fd8a-4418-9442-8cca2cefe6f3)
- **2026-06-01T08:53** — Root cause identified: pentest scanned Cloudflare edge, not nginx origin — Cloudflare was serving the outdated cipher suites
  > "Root cause identified: pentest scanned Cloudflare edge, not nginx origin — Cloudflare was serving the outdated cipher suites" — [[raw/2026-06-01-pieces-ftfl-511-tls-cipher-remediation]] (Pieces: 92b022c0-fd8a-4418-9442-8cca2cefe6f3)
- **2026-06-01T08:53** — DNS-only propagation confirmed — sandbox-testing-1.fitfile.net now resolves to Azure origin IP 20.117.146.221, no Cloudflare in path
  > "DNS-only propagation confirmed — sandbox-testing-1.fitfile.net now resolves to Azure origin IP 20.117.146.221, no Cloudflare in path" — [[raw/2026-06-01-pieces-ftfl-511-tls-cipher-remediation]] (Pieces: be2e3a5e-3c95-46b1-a6dc-ce5b958490b7)
- **2026-06-01T08:39** — DNS-only propagation confirmed — sandbox-testing-1.fitfile.net now resolves to Azure origin IP 20.117.146.221, no Cloudflare in path
  > "DNS-only propagation confirmed — sandbox-testing-1.fitfile.net now resolves to Azure origin IP 20.117.146.221, no Cloudflare in path" — [[raw/2026-06-01-pieces-ftfl-511-tls-cipher-remediation]] (Pieces: b023b25d-0208-4bd5-8bba-e5b2291ad098)
- **2026-06-01T08:39** — nmap scan from local machine confirmed clean TLS — only AEAD suites (ECDHE+AESGCM, ECDHE+CHACHA20), no CBC, no RSA key exchange, cipher preference server, grade A
  > "nmap scan from local machine confirmed clean TLS — only AEAD suites (ECDHE+AESGCM, ECDHE+CHACHA20), no CBC, no RSA key exchange, cipher preference server, grade A" — [[raw/2026-06-01-pieces-ftfl-511-tls-cipher-remediation]] (Pieces: b023b25d-0208-4bd5-8bba-e5b2291ad098)
- **2026-06-01T08:39** — Root cause identified: pentest scanned Cloudflare edge, not nginx origin — Cloudflare was serving the outdated cipher suites
  > "Root cause identified: pentest scanned Cloudflare edge, not nginx origin — Cloudflare was serving the outdated cipher suites" — [[raw/2026-06-01-pieces-ftfl-511-tls-cipher-remediation]] (Pieces: b023b25d-0208-4bd5-8bba-e5b2291ad098)
- **2026-06-01T08:38** — DNS-only propagation confirmed — sandbox-testing-1.fitfile.net now resolves to Azure origin IP 20.117.146.221, no Cloudflare in path
  > "DNS-only propagation confirmed — sandbox-testing-1.fitfile.net now resolves to Azure origin IP 20.117.146.221, no Cloudflare in path" — [[raw/2026-06-01-pieces-ftfl-511-tls-cipher-remediation]] (Pieces: 6ba298d9-2ca1-4ead-a773-dbf27b164efd)
- **2026-06-01T08:38** — nmap scan from local machine confirmed clean TLS — only AEAD suites (ECDHE+AESGCM, ECDHE+CHACHA20), no CBC, no RSA key exchange, cipher preference server, grade A
  > "nmap scan from local machine confirmed clean TLS — only AEAD suites (ECDHE+AESGCM, ECDHE+CHACHA20), no CBC, no RSA key exchange, cipher preference server, grade A" — [[raw/2026-06-01-pieces-ftfl-511-tls-cipher-remediation]] (Pieces: 6ba298d9-2ca1-4ead-a773-dbf27b164efd)
- **2026-06-01T08:27** — DNS-only propagation confirmed — sandbox-testing-1.fitfile.net now resolves to Azure origin IP 20.117.146.221, no Cloudflare in path
  > "DNS-only propagation confirmed — sandbox-testing-1.fitfile.net now resolves to Azure origin IP 20.117.146.221, no Cloudflare in path" — [[raw/2026-06-01-pieces-ftfl-511-tls-cipher-remediation]] (Pieces: 3314644d-e59b-4d73-a611-cd57e8ae2c49)
- **2026-06-01T08:27** — nmap scan from local machine confirmed clean TLS — only AEAD suites (ECDHE+AESGCM, ECDHE+CHACHA20), no CBC, no RSA key exchange, cipher preference server, grade A
  > "nmap scan from local machine confirmed clean TLS — only AEAD suites (ECDHE+AESGCM, ECDHE+CHACHA20), no CBC, no RSA key exchange, cipher preference server, grade A" — [[raw/2026-06-01-pieces-ftfl-511-tls-cipher-remediation]] (Pieces: 3314644d-e59b-4d73-a611-cd57e8ae2c49)
- **2026-06-01T08:27** — Root cause identified: pentest scanned Cloudflare edge, not nginx origin — Cloudflare was serving the outdated cipher suites
  > "Root cause identified: pentest scanned Cloudflare edge, not nginx origin — Cloudflare was serving the outdated cipher suites" — [[raw/2026-06-01-pieces-ftfl-511-tls-cipher-remediation]] (Pieces: 3314644d-e59b-4d73-a611-cd57e8ae2c49)
- **2026-06-01T08:26** — DNS-only propagation confirmed — sandbox-testing-1.fitfile.net now resolves to Azure origin IP 20.117.146.221, no Cloudflare in path
  > "DNS-only propagation confirmed — sandbox-testing-1.fitfile.net now resolves to Azure origin IP 20.117.146.221, no Cloudflare in path" — [[raw/2026-06-01-pieces-ftfl-511-tls-cipher-remediation]] (Pieces: 9ba83f8a-8a43-4419-bede-b79d9b8f82a2)
- **2026-06-01T08:26** — nmap scan from local machine confirmed clean TLS — only AEAD suites (ECDHE+AESGCM, ECDHE+CHACHA20), no CBC, no RSA key exchange, cipher preference server, grade A
  > "nmap scan from local machine confirmed clean TLS — only AEAD suites (ECDHE+AESGCM, ECDHE+CHACHA20), no CBC, no RSA key exchange, cipher preference server, grade A" — [[raw/2026-06-01-pieces-ftfl-511-tls-cipher-remediation]] (Pieces: 9ba83f8a-8a43-4419-bede-b79d9b8f82a2)
- **2026-06-01T08:26** — Root cause identified: pentest scanned Cloudflare edge, not nginx origin — Cloudflare was serving the outdated cipher suites
  > "Root cause identified: pentest scanned Cloudflare edge, not nginx origin — Cloudflare was serving the outdated cipher suites" — [[raw/2026-06-01-pieces-ftfl-511-tls-cipher-remediation]] (Pieces: 9ba83f8a-8a43-4419-bede-b79d9b8f82a2)
- **2026-06-01T08:19** — Root cause identified: pentest scanned Cloudflare edge, not nginx origin — Cloudflare was serving the outdated cipher suites
  > "Root cause identified: pentest scanned Cloudflare edge, not nginx origin — Cloudflare was serving the outdated cipher suites" — [[raw/2026-06-01-pieces-ftfl-511-tls-cipher-remediation]] (Pieces: 247ed4ba-d561-45e4-9dbb-a54b6f8ddc6f)

## Timeline

- **2026-04-16** — Ticket created (priority Low, 3 story points)
- **2026-05-05** — Yasir Mansoor opened MR !757
- **2026-05-07** — Discussion with Ollie Rushton — original solution deemed incorrect; moved back to backlog
- **2026-05-27** — CoS run: FTFL-511 appeared as "Selected for Development" on Sprint 20 board
- **2026-05-28** — Leon reviewed ticket; MR !757 confirmed declined; Hermes attempted Jira MCP fetch (failed due to injection gap)
- **2026-06-01** — DNS-only propagation completed; nmap scan from local machine confirmed only AEAD ciphers at origin (remediation validated)
- **2026-06-01** — FTFL-511 rooted cause confirmed: pentest hit Cloudflare edge serving outdated ciphers; switching to DNS-only mode resolved the issue at the origin

## Connections

- [[FITFILE Testing Infrastructure]] — parent FITFILE infrastructure project
- [[MCP Proxy Robustness and High Availability]] — Hermes MCP tool failure during ticket fetch
- [[FTFL-510 Pentest Actions API]] — parent ticket (implied by Jira hierarchy)
- [[FTFL-512 Nginx Security]] — companion Nginx security ticket (appeared same time)

## Contradictions

None identified.

## Open Questions

- ~~Who is the DevOps engineer that will re-pick the FTFL-511 fix?~~ **Resolved: No DevOps engineer needed — the issue was Cloudflare edge, not nginx origin.**
- ~~Should the TLS hardening be applied via Helm values override or directly in the Helm chart?~~ **Resolved: Switching Cloudflare to DNS-only mode and validating at the origin was sufficient.**
- Does the cipher suite hardening need to be applied to production as well?