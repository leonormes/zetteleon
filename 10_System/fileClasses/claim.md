---
extends: Note
icon: gavel
version: "1.0"
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
permalink: llmeon/10-system/file-classes/claim-1
baseFile: 02_bases/claim.base
baseView: claim
---

# Claim

Per [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] §3.1 `ClaimNote`. `title` should be a single declarative sentence — the claim itself.