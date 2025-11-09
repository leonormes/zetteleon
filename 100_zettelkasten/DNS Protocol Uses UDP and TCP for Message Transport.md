---
aliases: []
confidence: 0.9
created: 2025-10-31T11:06:00Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T11:06:00Z
purpose: "Explain DNS transport protocols."
review_interval: 90
see_also: ["DNS is a distributed database.md", "DNS Message Format Contains Header and Sections.md"]
source_of_truth: []
status: seedling
tags: [dns, networking, protocols]
title: DNS Protocol Uses UDP and TCP for Message Transport
type: concept
uid: 
updated: 
---

## DNS Protocol Uses UDP and TCP for Message Transport

**Summary:** DNS primarily uses UDP port 53 for queries/responses, with TCP for zone transfers and large messages.

**UDP Usage:**
- Default for standard queries
- Maximum 512 byte payload (without EDNS)
- Low overhead, connectionless

**TCP Usage:**
- Zone transfers (AXFR/IXFR)
- Messages > 512 bytes
- EDNS extensions

**EDNS (Extension Mechanisms):**
- Allows larger UDP payloads
- Additional flags and options
- Backward compatible
