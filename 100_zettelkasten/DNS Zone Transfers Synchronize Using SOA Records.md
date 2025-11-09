---
aliases: []
confidence: 0.9
created: 2025-10-31T10:47:00Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T10:47:00Z
purpose: "Explain DNS zone transfer mechanism."
review_interval: 90
see_also: ["DNS is a distributed database.md"]
source_of_truth: []
status: seedling
tags: [dns, networking]
title: DNS Zone Transfers Synchronize Using SOA Records
type: concept
uid: 
updated: 
---

## DNS Zone Transfers Synchronize Using SOA Records

**Summary:** DNS slave servers use zone transfers to synchronize with masters, controlled by the SOA (Start of Authority) record's metadata.

**Key SOA fields:**
- **Serial number:** Version indicator (must increment for changes)
- **Refresh:** How often slaves check for updates
- **Retry:** Re-attempt interval if master unreachable
- **Expire:** When stale data should be discarded
- **Negative TTL:** Cache duration for "not found" responses

**Protocol Details:**
- Uses TCP for reliability
- AXFR for full zone transfers
- IXFR for incremental updates
- Controlled by SOA serial numbers

**Process:**
1. Slave compares its SOA serial with master's
2. Initiates AXFR (full) or IXFR (incremental) transfer if master has newer data
