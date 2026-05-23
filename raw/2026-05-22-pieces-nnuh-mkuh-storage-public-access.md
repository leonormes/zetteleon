---
title: NNUH and MKUH Storage Accounts — Public Network Access Verification
created: 2026-05-23T00:23:00+00:00
source: pieces-ltm
pieces_ids: ["5e900cc2-d3af-43d1-ab6b-4a0fd9cdd305"]
tags: [raw, pieces]
---

# NNUH and MKUH Storage Accounts — Public Network Access Verification

User raised a question about whether the NNUH and MKUH Azure storage accounts are accessible from the public network despite being configured with private endpoints.

## Asset 1 (Pieces: 5e900cc2-d3af-43d1-ab6b-4a0fd9cdd305) — 2026-05-22 12:57 UTC

User question:

> is this true "just a reminder that the NNUH and MKUH storage accounts, although using private endpoint, are available to public network"

This suggests a potential security concern: storage accounts configured with private endpoints may still have `publicNetworkAccess` enabled at the Azure portal level, meaning they are reachable from the public internet despite the private endpoint configuration.
