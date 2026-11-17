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
- name: protocol
  id: prodos_protocol
  type: Object
  path: prodos
- name: applies_to
  id: prodos_protocol_applies_to
  type: MultiInput
  path: prodos____prodos_protocol
- name: binary_checklist
  id: prodos_protocol_binary_checklist
  type: Boolean
  path: prodos____prodos_protocol
icon: shield-check
modified: 2026-11-16 22:51:00+00:00
version: '1.0'
permalink: llmeon/10-system/file-classes/protocol
---

## Protocol

Per [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] §2 & §4. Routing class for binary imperative procedures (`Protocol - Title.md`).