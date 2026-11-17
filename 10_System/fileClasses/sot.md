---
baseFile: 02_bases/SoT.base
baseView: All Active SoTs & Protocols
created: 2026-11-16 22:51:00+00:00
extends: Note
fields:
- name: prodos
  id: prodos
  type: Object
  path: ''
- name: kind
  id: prodos_kind
  type: Select
  options:
  - head
  - sot
  - protocol
  - moc
  - atomic
  - project
  - ops
  - prompt
  - journal
  path: prodos
- name: lifecycle
  id: prodos_lifecycle
  type: Select
  options:
  - seedling
  - active
  - stable
  - evergreen
  - archived
  path: prodos
- name: trust
  id: prodos_trust
  type: Select
  options:
  - low
  - working
  - stable
  - authoritative
  path: prodos
- name: id
  id: prodos_id
  type: Input
  path: prodos
- name: review
  id: prodos_review
  type: Object
  path: prodos
- name: interval
  id: prodos_review_interval
  type: Input
  path: prodos____prodos_review
- name: last_reviewed
  id: prodos_review_last_reviewed
  type: Date
  path: prodos____prodos_review
- name: chronos
  id: prodos_chronos
  type: Object
  path: prodos
- name: last_synthesis
  id: prodos_chronos_last_synthesis
  type: Date
  path: prodos____prodos_chronos
- name: synthesis_count
  id: prodos_chronos_synthesis_count
  type: Number
  path: prodos____prodos_chronos
icon: book-open
modified: 2026-11-16 22:51:00+00:00
version: '1.0'
permalink: llmeon/10-system/file-classes/sot
---

## SoT

Per [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] §2 & §4. Routing class for Source-of-Truth synthesis notes (`SoT - Title.md`).