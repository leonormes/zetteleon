---
title: Network Security Scan — Pieces LTM Capture 2026-06-01
created: 2026-06-01T12:00:00+00:00
source: pieces-ltm
pieces_ids: []
tags: [raw, pieces]
---
## Asset 1 (Pieces: )
*Captured: 2026-06-01T08:53:03.847117Z*

The user has run the `dig` command and it's now returning `20.117.146.221` — their Azure origin IP, not a Cloudflare Anycast address. This means DNS-only has propagated. They should now rerun the nmap scan directly against the hostname.
