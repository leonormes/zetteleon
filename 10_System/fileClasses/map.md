---
baseFile: 02_bases/MOCx.base
baseView: Active Maps
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
- name: moc
  id: prodos_moc
  type: Object
  path: prodos
- name: hub_for
  id: prodos_moc_hub_for
  type: Input
  path: prodos____prodos_moc
- name: entry_points
  id: prodos_moc_entry_points
  type: MultiFile
  path: prodos____prodos_moc
icon: map
modified: 2026-11-16 22:51:00+00:00
version: '1.0'
permalink: llmeon/10-system/file-classes/map
---

## Map

Per [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] §2 & §4. Routing class for Maps of Content (`MOC - Title.md`).