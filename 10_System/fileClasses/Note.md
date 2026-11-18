---
created: 2026-07-23T18:50:52+00:00
fields:
- name: title
  id: title
  type: Input
  options:
    required: true
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
  - link_report
  - equipment
  - source
  - prompt
  - tombstone
  path: ''
- name: tags
  id: tags
  type: MultiInput
  options:
    required: true
  path: ''
- name: conformant
  id: conformant
  type: Boolean
  options:
    required: true
  path: ''
- name: non_conformance_reason
  id: non_conformance_reason
  type: Input
  path: ''
- name: created
  id: created
  type: DateTime
  path: ''
- name: modified
  id: modified
  type: DateTime
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
  - superseded
  - archived
  path: ''
- name: supersedes
  id: supersedes
  type: MultiFile
  path: ''
- name: superseded_by
  id: superseded_by
  type: MultiFile
  path: ''
- name: aliases
  id: aliases
  type: MultiInput
  path: ''
- name: see_also
  id: see_also
  type: MultiFile
  path: ''
- name: project_name
  id: project_name
  type: Input
  path: ''
- name: project_category
  id: project_category
  type: Input
  path: ''
- name: own_words
  id: own_words
  type: Boolean
  path: ''
icon: file-text
modified: 2026-11-16T22:51:00+00:00
permalink: llmeon/10-system/file-classes/note
version: '1.0'
---

## Note

Base fileClass for the vault's [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] §2 `FrontmatterContract`—the shared universal envelope every note inherits.

Not meant to be bound directly to notes; all 15 ProdOS `type` fileClasses (`claim`, `concept`, `evidence`, `question`, `procedure`, and the 10 routing classes) `extends: Note`. The optional §4 `prodos` routing object is declared only on routing classes (never on atomic classes).
