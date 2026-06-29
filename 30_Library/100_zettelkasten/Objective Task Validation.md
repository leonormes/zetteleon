---
created: 2026-04-13 14:53:30+00:00
created_utc: '2026-04-13T11:40:00Z'
kind: heuristic
modified: 2026-05-26 11:44:34+00:00
source_title: Using Karpathy’s Original Framework (Auto Research)
source_url: http://www.youtube.com/watch?v=bc4NrE0cOE0
status: seed
tags:
- automation
- evaluation
- reliability
title: Objective Task Validation
type: atom
upstream: '[[Using Karpathy’s Original Framework]]'
permalink: llmeon/30-library/100-zettelkasten/objective-task-validation
---

## Objective Task Validation

Objective AI tasks, such as generating code with specific syntax or verifying factual accuracy, should be validated using deterministic scripts rather than LLMs. This ensures 100% reliability in verification while minimizing token costs and avoiding the probabilistic errors inherent in LLM-based judging.

### Scope & Conditions

Selection of evaluation tools in optimization loops for tasks with measurable, verifiable facts or structural requirements.

### Evidence

> "a standard deterministic script (for objective tasks)"

### Implications

- Reduces token costs by avoiding unnecessary LLM calls.
- Provides 100% reliable verification for facts or code syntax.

### Related

- [[Optimization Criteria Must Be Binary Single-Variable Testable Conditions]]—shared mechanism: deterministic scripts are the most effective way to enforce binary criteria.
- [[SoT - Test-Driven Development]]—shared mechanism: matches the TDD requirement for deterministic pass/fail states.