---
aliases: []
conformant: false
created: 2025-10-31T11:06:00+00:00
modified: 2026-09-26T08:45:29+00:00
non_conformance_reason: "missing schema field proposition for type claim (required when conformant - true); missing schema field contradicts for type claim (required when conformant - true); missing schema field evidence_links for type claim (required when conformant - true); missing schema field epistemic_status for type claim (required when conformant - true)"
permalink: llmeon/30-library/100-zettelkasten/dns-protocol-uses-udp-and-tcp-for-message-transport
tags: [protocols, SoftwareEngineering/Networking, SoftwareEngineering/networking/dns]
title: DNS Protocol Uses UDP and TCP for Message Transport
type: claim
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
