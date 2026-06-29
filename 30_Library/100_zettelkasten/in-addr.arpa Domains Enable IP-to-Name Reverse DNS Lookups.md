---
aliases:
- Reverse DNS
created: 2025-10-31 10:50:00+00:00
last_reviewed: ''
modified: 2026-02-01 15:08:23+00:00
status: seedling
tags:
- SoftwareEngineering/Networking
- SoftwareEngineering/networking/dns
title: in-addr.arpa Domains Enable IP-to-Name Reverse DNS Lookups
type: concept
updated: null
permalink: llmeon/30-library/100-zettelkasten/in-addr.arpa-domains-enable-ip-to-name-reverse-dns-lookups
---

## in-addr.arpa Domains Enable IP-to-Name Reverse DNS Lookups

Summary: The in-addr.arpa domain provides a hierarchical namespace for mapping IP addresses back to hostnames using PTR records.

Format:

- IPv4: Reverse octets +.in-addr.arpa (e.g., 1.253.253.192.in-addr.arpa for 192.253.253.1)
- Queries return PTR records with canonical names

Uses:

- Authentication (e.g., mail servers)
- Logging
- Troubleshooting

Delegation:

Like forward zones, in-addr.arpa subdomains must be properly delegated to network administrators.