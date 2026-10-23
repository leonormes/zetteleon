---
baseFile: 02_bases/claim.base
baseView: claim
created: 2026-08-24T15:26:16+00:00
extends: Note
fields:
  - name: proposition
    id: proposition
    type: Input
    path: ""
  - name: epistemic_status
    id: epistemic_status
    type: Select
    options:
      - high
      - medium
      - low
      - unknown
    path: ""
  - name: evidence_links
    id: evidence_links
    type: MultiFile
    path: ""
  - name: contradicts
    id: contradicts
    type: MultiFile
    path: ""
icon: gavel
modified: 2026-10-22T15:11:08+00:00
permalink: llmeon/10-system/file-classes/claim-1
version: "1.0"
---

## Claim

Per [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] §3.1 `ClaimNote`. `title` should be a single declarative sentence—the claim itself.
