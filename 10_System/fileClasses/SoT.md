---
aliases: []
created: 2025-12-24T22:15:02Z
fields:
  - name: status
    type: Select
    options:
      - "seedling": "🌱 Seedling"
      - "incubating": "🥚 Incubating"
      - "stable": "🌳 Stable"
      - "archived": "🗃️ Archived"
  - name: epistemic
    type: Select
    options:
      - "synthesis": "🧩 Synthesis"
      - "theory": "🧪 Theory"
      - "strategy": "♟️ Strategy"
      - "operational": "⚙️ Operational"
      - "scientific": "🔬 Scientific"
      - "process": "🔄 Process"
  - name: confidence
    type: Select
    options:
      - "1/5": "Low"
      - "2/5": "Medium-Low"
      - "3/5": "Medium"
      - "4/5": "High"
      - "5/5": "Very High"
  - name: type
    type: Input
    options:
      template: "SoT"
  - name: review_interval
    type: Cycle
    options:
      - "1 month"
      - "3 months"
      - "6 months"
      - "1 year"
  - name: purpose
    type: Input
  - name: last_reviewed
    type: Date
  - name: see_also
    type: MultiFile
  - name: source_of_truth
    type: MultiFile
last_reviewed: ""
modified: 2026-02-01T15:09:15+00:00
status: ""
tags: []
title: SoT
type: ""
updated: 
---
