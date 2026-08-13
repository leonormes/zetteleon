---
created: 2026-04-14T11:22:35+00:00
created_utc: '2026-04-14T11:05:00Z'
kind: claim
modified: 2026-08-13T10:54:52+00:00
permalink: llmeon/30-library/100-zettelkasten/shift-to-verification
source_title: 'Martin Fowler & Kent Beck: Frameworks for reinventing software, again and again'
source_url: http://www.youtube.com/watch?v=CZs8J1ZD0CE
status: seed
tags: [ai-development, reliability, tdd, verification]
title: Shift to Verification
type: atom
upstream: '[[SoT - Test-Driven Development]]'
---

## Shift to Verification

The primary constraint in AI-driven development is the capacity to validate non-deterministic code rather than the ability to generate it. As the cost of generation approaches zero, the value of engineering shifts from syntax production to the rigorous auditing and validation of probabilistic outputs.

### Scope & Conditions

Applies to software engineering workflows where LLMs are used to generate code.

### Evidence

> "Verification over Creation: Prioritise the ability to validate code over the ability to generate it."

### Implications

- Automated verification (e.g., TDD) becomes the primary bottleneck for system reliability.
- The engineer's role transitions from "writer" to "editor and auditor."

### Related

- [[MOC - AI Software Engineering]]—shared mechanism: engineering the "cognitive bridge" requires strong verification.
- [[SoT - Pragmatism vs Rigour in Software]]—shared mechanism: verification is the tool for maintaining rigour in a probabilistic world.

### See Also

- [[SoT - AI-Resilient Task Taxonomy (Human 3.0)]]
