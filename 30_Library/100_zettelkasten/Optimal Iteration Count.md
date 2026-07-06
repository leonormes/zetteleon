---
created: 2026-04-13T14:53:30+00:00
created_utc: '2026-04-13T11:40:00Z'
kind: constraint
modified: 2026-07-04T10:51:48+00:00
permalink: llmeon/30-library/100-zettelkasten/optimal-iteration-count
source_title: Using Karpathy’s Original Framework (Auto Research)
source_url: http://www.youtube.com/watch?v=bc4NrE0cOE0
status: seed
tags: [cost-management, efficiency, iteration]
title: Optimal Iteration Count
type: atom
upstream: '[[Using Karpathy’s Original Framework]]'
---

## Optimal Iteration Count

Automated optimization loops for AI agents should be capped at approximately 10 iterations to balance output quality with cost-efficiency. Exceeding 15 iterations often leads to diminishing returns, potential output degradation through over-fitting, and unnecessary accumulation of API token costs.

### Scope & Conditions

Iterative improvement cycles for AI agents. It applies to recursive tasks where the agent attempts to refine its own output based on feedback.

### Evidence

> "The creator recommends running 5 to 10 iterations; going beyond 15 can degrade the output and unnecessarily increase your token costs."

### Implications

- Prevents model over-fitting.
- Manages API spend during automated research.

### Related

- [[SoT - Agentic AI Design Patterns]]—extends: provides a heuristic constraint for the "Recursive Self-Improvement" pattern.
- [[Recursive Agent Improvement]]—shared mechanism: identifies the practical limit for autonomous refinement loops.
