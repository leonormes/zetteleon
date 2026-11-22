---
title: <% tp.file.title %>
type: problem
role: symptom
status: captured
impact: 3
created: <% tp.date.now("YYYY-MM-DDTHH:mm:ssZ") %>
modified: <% tp.date.now("YYYY-MM-DDTHH:mm:ssZ") %>
conformant: true
tags:
  - prodos/problem
aliases: []
see_also: []
permalink: llmeon/10-system/templates/template-problem
---

**Role:** `INPUT[inlineSelect(option(symptom), option(root-cause), option(constraint)):role]` · **Status:** `INPUT[inlineSelect(option(captured), option(clarifying), option(active-project), option(mitigated), option(accepted-constraint)):status]` · **Impact:** `INPUT[inlineSelect(option(1), option(2), option(3), option(4), option(5)):impact]`

## Undesirable Effect (Symptom)

<!-- What concrete, observable friction, failure, or constraint is occurring? -->

- 

## Root Cause Analysis (Clarity Framework)

<!-- Trace why this symptom persists. Distinguish symptoms from underlying root causes or fixed constraints. -->

- 

## Candidate Interventions / Next Action Readiness

<!-- Once a solvable root cause is identified, promote to a Project in 30_Library/200_Projects/ with a single unblocked Next Action. -->

- 

## Reference Links

- 
