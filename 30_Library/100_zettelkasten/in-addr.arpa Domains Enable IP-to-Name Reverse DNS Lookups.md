---
aliases: ["Reverse DNS"]
created: 2025-10-31T10:50:00Z
last_reviewed: ""
modified: 2026-02-01T15:08:23+00:00
status: "seedling"
tags: ["SoftwareEngineering/Networking", "SoftwareEngineering/networking/dns"]
title: in-addr.arpa Domains Enable IP-to-Name Reverse DNS Lookups
type: "concept"
updated: 
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
