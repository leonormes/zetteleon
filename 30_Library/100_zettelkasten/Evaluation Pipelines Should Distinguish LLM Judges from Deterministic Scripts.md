---
created: 2026-04-10T00:00:00+00:00
modified: 2026-07-13T08:52:26+00:00
permalink: llmeon/30-library/100-zettelkasten/evaluation-pipelines-should-distinguish-llm-judges-from-deterministic-scripts
tags: [automation, evaluation, llm-judge, system-design]
title: Evaluation Pipelines Should Distinguish LLM Judges from Deterministic Scripts
---

## Evaluation Pipelines Should Distinguish LLM Judges from Deterministic Scripts

Evaluation pipelines must select their evaluation mechanism based on the nature of the task: subjective or creative tasks require an LLM judge capable of nuanced interpretation, while objective tasks—those with a ground truth or a binary pass/fail—are better handled by a deterministic script. Using an LLM to evaluate an objectively measurable outcome wastes tokens, introduces non-determinism, and creates a risk of the LLM rationalising rather than measuring.

### Scope & Conditions

Applies during the design phase of any automated evaluation loop. The distinction becomes especially important in recursive optimization pipelines where evaluation cost and consistency compound across many iterations. The boundary between "subjective" and "objective" can shift with task formulation—a task that seems subjective can sometimes be decomposed into objective sub-criteria.

### Evidence

> "AI/LLM judge (for subjective or creative tasks) or a standard deterministic script (for objective tasks) [16:46]"

### Implications

- Improves reliability for technical and objective checks by removing probabilistic noise from the evaluation signal.
- Reduces token usage by offloading verifiable checks to local code, reserving LLM calls for tasks that genuinely require interpretive judgement.

### Related

- [[SoT - Agentic AI Design Patterns]]—direct concept match: the "Evaluation & Monitoring" pattern (quality gates and test suites) is the architectural context this distinction operates within; the atom refines that pattern with an explicit mode-selection rule.
- [[SoT - Test-Driven Development]]—shared mechanism: TDD's distinction between automated unit tests (objective/deterministic) and human code review (subjective/evaluative) mirrors this atom's evaluation split; both separate mechanical verification from interpretive judgement.
- [[SoT - ML Engineering for AI Agents]]—shared mechanism: the "Double-Blind verifier" fix for the Mirroring Trap (using an independent verification script rather than the same agent) is an application of preferring deterministic verification for objective correctness—matching this atom's principle.

### Tensions

- [[Optimization Criteria Must Be Binary Single-Variable Testable Conditions]]—extends with productive interaction: if evaluation criteria are defined as binary and single-variable (Atom 1), many tasks that appear to require an LLM judge can be converted into deterministic script checks; the two atoms together form a design sequence.
