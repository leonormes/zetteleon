---
aliases: []
conformant: false
created: 2025-10-31T10:47:00+00:00
modified: 2026-08-13T10:54:45+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/dns-zone-transfers-synchronize-using-soa-records
tags: [SoftwareEngineering/Networking, SoftwareEngineering/networking/dns]
title: DNS Zone Transfers Synchronize Using SOA Records
type: claim
---

## DNS Zone Transfers Synchronize Using SOA Records

Summary: DNS slave servers use zone transfers to synchronize with masters, controlled by the SOA (Start of Authority) record's metadata.

Key SOA fields:

- Serial number: Version indicator (must increment for changes)
- Refresh: How often slaves check for updates
- Retry: Re-attempt interval if master unreachable
- Expire: When stale data should be discarded
- Negative TTL: Cache duration for "not found" responses

Protocol Details:

- Uses TCP for reliability
- AXFR for full zone transfers
- IXFR for incremental updates
- Controlled by SOA serial numbers

Process:

1. Slave compares its SOA serial with master's
2. Initiates AXFR (full) or IXFR (incremental) transfer if master has newer data
