---
aliases: []
created: 2025-10-31 10:46:00+00:00
last_reviewed: ''
modified: 2026-02-01 15:08:35+00:00
status: seedling
tags:
- SoftwareEngineering/Networking
- SoftwareEngineering/networking/dns
title: DNS Resolver Search Lists Complete Unqualified Domain Names
type: concept
updated: null
permalink: llmeon/30-library/100-zettelkasten/dns-resolver-search-lists-complete-unqualified-domain-names
---

## DNS Resolver Search Lists Complete Unqualified Domain Names

Summary: DNS resolvers use a search list to automatically append domains to unqualified names (without dots), attempting resolution through multiple possible FQDNs.

Operation:

1. User enters name without dots (e.g., "telnet carrie")
2. Resolver tries:
   - carrie.domain1
   - carrie.domain2
   - etc.

Configuration:

- Set via `search` or `domain` in `/etc/resolv.conf`
- Bypassed with trailing dot (e.g., "carrie.movie.edu.")