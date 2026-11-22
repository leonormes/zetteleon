---
created: 2026-11-22T16:00:00+00:00
extends: Note
fields:
  - name: role
    id: role
    type: Select
    options:
      - symptom
      - root-cause
      - constraint
    path: ""
  - name: status
    id: status
    type: Select
    options:
      - captured
      - clarifying
      - active-project
      - mitigated
      - accepted-constraint
    path: ""
  - name: impact
    id: impact
    type: Number
    options:
      min: 1
      max: 5
      step: 1
    path: ""
icon: alert-triangle
modified: 2026-11-22T16:00:00+00:00
permalink: llmeon/10-system/file-classes/problem
version: "1.0"
---

## Problem

Per [[Protocol - Action-First GTD (LLM Chief of Staff)]] and [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]. Clarity Framework problem node (`Problem - [Undesirable Effect].md`) tracking `role`, `status`, and `impact` (1–5) before promotion to an actionable project.
