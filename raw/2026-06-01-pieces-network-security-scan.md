---
created: 2026-06-01T12:00:00+00:00
modified: 2026-07-04T10:49:27+00:00
permalink: llmeon/raw/2026-06-01-pieces-network-security-scan
pieces_ids: []
source: pieces-ltm
tags: [pieces, raw]
title: 2026-06-01-pieces-network-security-scan
---

## Asset 1 (Pieces:)

_Captured: 2026-06-01T08:53:03.847117Z_

The user has run the `dig` command and it's now returning `20.117.146.221`—their Azure origin IP, not a Cloudflare Anycast address. This means DNS-only has propagated. They should now rerun the nmap scan directly against the hostname.
