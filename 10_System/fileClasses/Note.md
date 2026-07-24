---
icon: file-text
version: '1.0'
fields:
- name: title
  id: title
  type: Input
  path: ''
- name: type
  id: type
  type: Select
  options:
  - claim
  - concept
  - evidence
  - question
  - procedure
  - protocol
  - map
  - journal
  - project
  - sot
  path: ''
- name: project_name
  id: project_name
  type: Input
  path: ''
- name: project_category
  id: project_category
  type: Input
  path: ''
- name: status
  id: status
  type: Select
  options:
  - draft
  - seed
  - stable
  - evergreen
  - stale
  path: ''
- name: tags
  id: tags
  type: MultiInput
  path: ''
- name: conformant
  id: conformant
  type: Boolean
  path: ''
- name: non_conformance_reason
  id: non_conformance_reason
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
permalink: llmeon/10-system/file-classes/note
created: 2026-07-23T18:50:52+00:00
modified: 2026-07-23T19:07:52+00:00
---

# Note

Base fileClass for the vault's [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] §2 `FrontmatterContract` — the shared envelope every note inherits, plus the §4 `prodos` routing object.

Not meant to be bound directly to notes; the five canonical knowledge-node fileClasses (`Claim`, `Concept`, `Evidence`, `Question`, `Procedure`) each `extends: Note`.