---
created: 2026-11-16 22:51:00+00:00
extends: Note
fields:
- name: source_reference
  id: source_reference
  type: Input
  path: ''
- name: authors
  id: authors
  type: MultiInput
  path: ''
- name: year
  id: year
  type: Number
  path: ''
- name: calibre_id
  id: calibre_id
  type: Input
  path: ''
- name: calibre_link
  id: calibre_link
  type: Input
  path: ''
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
icon: book-marked
modified: 2026-11-16 22:51:00+00:00
version: '1.0'
permalink: llmeon/10-system/file-classes/source
---

## Source

Per [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] §2 & §4. Routing class for book/article source notes (`Source - Title.md`).