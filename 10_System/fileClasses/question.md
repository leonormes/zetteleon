---
extends: Note
icon: help-circle
version: "1.0"
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
permalink: llmeon/10-system/file-classes/question-1
baseFile: 02_bases/Question.base
baseView: Question
---

# Question

Per [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] §3.4 `QuestionNote`. `title` is the question itself and must end with '?'.