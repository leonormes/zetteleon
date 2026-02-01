---
aliases: []
created: 2025-10-31T11:06:00Z
last_reviewed: ""
modified: 2026-02-01T15:08:35+00:00
status: "seedling"
tags: ["protocols", "SoftwareEngineering/Networking", "SoftwareEngineering/networking/dns"]
title: DNS Protocol Uses UDP and TCP for Message Transport
type: "concept"
updated: 
---

## DNS Protocol Uses UDP and TCP for Message Transport

Summary: DNS primarily uses UDP port 53 for queries/responses, with TCP for zone transfers and large messages.

UDP Usage:

- Default for standard queries
- Maximum 512 byte payload (without EDNS)
- Low overhead, connectionless

TCP Usage:

- Zone transfers (AXFR/IXFR)
- Messages > 512 bytes
- EDNS extensions

EDNS (Extension Mechanisms):

- Allows larger UDP payloads
- Additional flags and options
- Backward compatible
