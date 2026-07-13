---
aliases: []
created: 2025-10-31T10:49:00+00:00
modified: 2026-07-13T08:52:27+00:00
permalink: llmeon/30-library/100-zettelkasten/glue-records-solve-dns-chicken-and-egg-problems
tags: [SoftwareEngineering/Networking, SoftwareEngineering/networking/dns]
title: Glue Records Solve DNS Chicken-and-Egg Problems
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
