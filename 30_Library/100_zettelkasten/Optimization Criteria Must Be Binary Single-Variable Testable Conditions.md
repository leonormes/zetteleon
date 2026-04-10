---
created: 2026-04-10T00:00:00+00:00
modified: 2026-04-10T16:52:03+00:00
tags: [criteria, evaluation, optimization, prompt-engineering]
title: Optimization Criteria Must Be Binary Single-Variable Testable Conditions
---

## Optimization Criteria Must Be Binary Single-Variable Testable Conditions

When defining goals for automated research or agentic evaluation loops, each optimization criterion must be formulated as a clear, testable, true/false condition with only one variable per criterion. Fuzzy or compound criteria (e.g., "make it short and clear and engaging") cannot be evaluated objectively by an automated system because they conflate multiple dimensions into a single ambiguous judgement. Binary, single-variable criteria eliminate this ambiguity and make success measurable.

### Scope & Conditions

Applies at the task-setup stage of any agentic or recursive optimization workflow. The constraint is most critical when an LLM or script must evaluate its own output—the evaluation signal is only as clean as the criterion it tests against. Does not preclude having multiple criteria; it requires that each individual criterion be atomic.

### Evidence

> "Define your specific criteria… These must be clear, testable, true/false conditions with only one variable per criterion [10:08]"

### Implications

- Eliminates ambiguity in "fuzzy" requests, making automated success/failure determination reliable.
- Enables objective measurement of quality in agentic loops without requiring a human judge for every iteration.

### Related

- [[SoT - Test-Driven Development]]—shared mechanism: TDD's Red-Green-Refactor cycle is grounded in binary pass/fail tests written before implementation; defining evaluation criteria as binary conditions follows the same structural logic—both transform ambiguous requirements into verifiable propositions.
- [[LLM Reasoning Efficiency is Proportional to Structural Constraint]]—shared mechanism: both assert that removing ambiguity (binary conditions / structural constraints) improves automated system performance; the "one variable per criterion" rule is an instance of providing structural constraint to prevent entropy.
- [[SoT - Agentic AI Design Patterns]]—extends: the "Goal Setting & Monitoring" pattern requires measurable targets; this atom provides the constraint for what makes a target measurable in automated loops.

### See Also

- [[Minimum Viable Context for LLMs Prevents Hallucination via Structural Boundaries]]
