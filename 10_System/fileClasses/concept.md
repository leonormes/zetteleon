---
extends: Note
icon: lightbulb
version: "1.0"
fields:
  - name: definition
    id: definition
    type: Input
    path: ""
  - name: distinguishes_from
    id: distinguishes_from
    type: MultiFile
    path: ""
  - name: used_in_claims
    id: used_in_claims
    type: MultiFile
    path: ""
permalink: llmeon/10-system/file-classes/concept
baseFile: 02_bases/concept.base
baseView: concept
---

# Concept

Per [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] §3.2 `ConceptNote`. `title` is the term or distinction being defined.