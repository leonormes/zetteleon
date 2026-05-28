---
title: FTFL-511 Nginx HTTPS Hardening
wiki_type: dossier
entity_kind: project
created: 2026-05-28T18:05:00+00:00
modified: 2026-05-28T18:05:00+00:00
tags: [wiki, dossier]
sources:
  - raw/2026-05-28-pieces-ftfl511-jira-ticket.md
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

## Timeline

- **2026-04-16** — Ticket created (priority Low, 3 story points)
- **2026-05-05** — Yasir Mansoor opened MR !757
- **2026-05-07** — Discussion with Ollie Rushton — original solution deemed incorrect; moved back to backlog
- **2026-05-27** — CoS run: FTFL-511 appeared as "Selected for Development" on Sprint 20 board
- **2026-05-28** — Leon reviewed ticket; MR !757 confirmed declined; Hermes attempted Jira MCP fetch (failed due to injection gap)

## Connections

- [[FITFILE Testing Infrastructure]] — parent FITFILE infrastructure project
- [[MCP Proxy Robustness and High Availability]] — Hermes MCP tool failure during ticket fetch
- [[FTFL-510 Pentest Actions API]] — parent ticket (implied by Jira hierarchy)
- [[FTFL-512 Nginx Security]] — companion Nginx security ticket (appeared same time)

## Contradictions

None identified.

## Open Questions

- Who is the DevOps engineer that will re-pick the FTFL-511 fix?
- Should the TLS hardening be applied via Helm values override or directly in the Helm chart?
- Does the cipher suite hardening need to be applied to production ingress-nginx as well, or just the sandbox/testing environment?
- Is FTFL-512 a similar Nginx TLS ticket that can be batched with FTFL-511?
