---
aliases: []
created: 2025-10-31T10:48:00+00:00
last_reviewed: ''
modified: 2026-07-04T10:51:52+00:00
permalink: llmeon/30-library/100-zettelkasten/dns-delegation-handles-subdomain-authority-transfers
status: seedling
tags: [SoftwareEngineering/Networking, SoftwareEngineering/networking/dns]
title: DNS Delegation Handles Subdomain Authority Transfers
type: concept
updated: null
---

## DNS Delegation Handles Subdomain Authority Transfers

Summary: DNS delegation allows parent domains to transfer authority for subdomains to different nameservers, enabling hierarchical management.

Mechanism:

1. Parent zone (e.g., movie.edu) contains NS records pointing to subdomain nameservers (e.g., fx.movie.edu)
2. Queries for the subdomain are referred to these nameservers
3. Creates separate zone of authority

Benefits:

- Enables distributed administration
- Supports organizational boundaries
- Maintains hierarchical structure
