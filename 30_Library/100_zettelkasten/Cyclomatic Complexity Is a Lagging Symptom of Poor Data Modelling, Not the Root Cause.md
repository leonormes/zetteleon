---
conformant: true
created: 2026-09-19T15:24:57+00:00
created_utc: 2026-09-19 00:00:00+00:00
definition: The McCabe cyclomatic complexity metric counts independent paths through a program control-flow graph and so measures excessive branching as a symptom, while the Chapin data complexity metric measures the complexity of the data being manipulated, which sits closer to the underlying cause.
distinguishes_from: []
modified: 2026-09-25T16:29:20+00:00
non_conformance_reason: ''
permalink: llmeon/00-inbox/cyclomatic-complexity-is-a-lagging-symptom-of-poor-data-modelling-not-the-root-cause
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [chapin, cyclomatic-complexity, mccabe, metrics]
title: Cyclomatic Complexity Is a Lagging Symptom of Poor Data Modelling, Not the Root Cause
type: concept
upstream: '[[tmp_atoms_data-structures-vs-control-flow]]'
used_in_claims: []
---

## Cyclomatic Complexity Is a Lagging Symptom of Poor Data Modelling, Not the Root Cause

McCabe's cyclomatic complexity metric counts independent paths through a program's control-flow graph and so measures excessive branching as a symptom, while Chapin's data complexity metric measures the complexity of the data being manipulated, which sits closer to the underlying cause.

### Scope & Conditions

A measurement-theory distinction between two 1970s-era software metrics.

### Evidence

> "While a high cyclomatic complexity indicates that a function is difficult to test and prone to defects, it is ultimately a lagging indicator. It measures the symptom (excessive branching) rather than the disease (poor data modeling)."

### Implications

- Driving cyclomatic complexity down without addressing the underlying data model risks treating the symptom, not the disease.

### See Also

- [[SoT - Conservation of Complexity]]—tag cluster: general complexity-metrics context; no note in the vault currently covers cyclomatic/data-complexity metrics directly.
- [[SoT - LLM Codebase Understanding & Hierarchy]]—_its CFG layer ("The Graph", §ii) is explicitly named as what cyclomatic complexity is calculated from; this note supplies the McCabe-vs-Chapin metric distinction that layer presupposes but doesn't unpack._
