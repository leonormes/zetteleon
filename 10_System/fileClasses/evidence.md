---
baseFile: 02_bases/evidence.base
baseView: evidence
created: 2026-09-22T10:00:25+00:00
extends: Note
fields:
- name: source_quote
  id: source_quote
  type: Input
  path: ''
- name: source_reference
  id: source_reference
  type: Input
  path: ''
- name: supports_claims
  id: supports_claims
  type: MultiFile
  path: ''
- name: confidence
  id: confidence
  type: Number
  options:
    min: 0
    max: 1
    step: 0.1
  path: ''
icon: search
modified: 2026-10-22T15:11:08+00:00
permalink: llmeon/10-system/file-classes/evidence-1
version: '1.0'
---

## Evidence

Per [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] §3.3 `EvidenceNote`. `title` is a descriptive title of the evidence; `source_quote` is a direct extraction only, not a paraphrase.
