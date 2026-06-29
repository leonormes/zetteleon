---
aliases: []
created: 2025-10-31 10:49:00+00:00
last_reviewed: ''
modified: 2026-02-01 15:08:33+00:00
status: seedling
tags:
- SoftwareEngineering/Networking
- SoftwareEngineering/networking/dns
title: Glue Records Solve DNS Chicken-and-Egg Problems
type: concept
updated: null
permalink: llmeon/30-library/100-zettelkasten/glue-records-solve-dns-chicken-and-egg-problems
---

## Glue Records Solve DNS Chicken-and-Egg Problems

Summary: Glue records are special A records in parent zones that provide the IP addresses of delegated subdomain nameservers, enabling their discovery.

Problem solved:

When subdomain nameservers reside within their own subdomain (e.g., ns1.fx.movie.edu serving fx.movie.edu), resolvers cannot find their IPs without these records.

Implementation:

- Parent zone includes A records for child nameservers
- Provided during referral responses
- Not part of parent's official zone data

Example:

movie.edu zone contains:

```sh
fx.movie.edu. NS ns1.fx.movie.edu.
ns1.fx.movie.edu. A 192.253.253.1
```