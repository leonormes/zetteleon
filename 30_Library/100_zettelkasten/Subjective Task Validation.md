---
created: 2026-04-13T14:53:30+00:00
created_utc: '2026-04-13T11:40:00Z'
kind: heuristic
modified: 2026-07-13T08:52:31+00:00
permalink: llmeon/30-library/100-zettelkasten/subjective-task-validation
source_title: Using Karpathy’s Original Framework (Auto Research)
source_url: http://www.youtube.com/watch?v=bc4NrE0cOE0
status: seed
tags: [evaluation, llm-judge, subjectivity]
title: Subjective Task Validation
type: atom
upstream: '[[Using Karpathy’s Original Framework]]'
---

## Subjective Task Validation

Subjective or creative AI tasks—where success is a matter of nuance, tone, or style—require an LLM-based judge for automated evaluation. This approach uses a secondary LLM session to provide the qualitative judgment that deterministic scripts cannot capture, ensuring that "aesthetic" or "voice" requirements are met in optimization loops.

### Scope & Conditions

Applies to automated research or optimization workflows where criteria cannot be reduced to simple boolean code checks. It requires a well-defined prompt for the LLM judge to ensure consistency.

### Evidence

> "The system will usually recommend… an AI/LLM judge (for subjective or creative tasks)"

### Implications

- Captures nuance that deterministic scripts miss.
- Requires a secondary LLM session for validation.

### Related

- [[Optimization Criteria Must Be Binary Single-Variable Testable Conditions]]—extends: even with an LLM judge, the criteria should remain as binary as possible to guide the judge's verdict.
- [[SoT - Agentic AI Design Patterns]]—See Also.
