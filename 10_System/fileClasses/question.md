---
baseFile: 02_bases/Question.base
baseView: Question
created: 2026-08-24T15:26:16+00:00
extends: Note
fields:
  - name: tension
    id: tension
    type: Input
    path: ""
  - name: candidate_answers
    id: candidate_answers
    type: MultiInput
    path: ""
  - name: related_claims
    id: related_claims
    type: MultiFile
    path: ""
icon: help-circle
modified: 2026-10-22T15:11:08+00:00
permalink: llmeon/10-system/file-classes/question-1
version: "1.0"
---

## Question

Per [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] §3.4 `QuestionNote`. `title` is the question itself and must end with '?'.
