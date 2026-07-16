---
aliases: [Flow Engineering, LLM Orchestration, Programmatic Gates, Prompt Engineering vs Flow Engineering]
created: 2026-04-06T17:00:00+00:00
last-synthesis: 2026-04-06
modified: 2026-07-13T08:52:48+00:00
permalink: llmeon/30-library/so-t/so-t-flow-engineering
see_also: []
source_of_truth: true
superseded_by: ''
supersedes: ''
tags: [ai-engineering, architecture, llm, orchestration, sot]
title: SoT - Flow Engineering
type: sot
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## Minimum Viable Understanding (MVU)

Flow Engineering is the discipline of enforcing LLM workflow constraints through a deterministic orchestration layer (code), rather than natural language prompt text. The LLM is reduced to what it actually is—a pure text-in/text-out transformation function—while all state management, gate enforcement, and feedback loops are handled by the surrounding programme.

The distinction:

- Prompt Engineering: Trying to _talk_ the model into following a methodology.
- Flow Engineering: Building a deterministic wrapper that _forces_ the model to comply, making non-compliance structurally impossible.

---

## Working Knowledge

### The Core Architecture

A Flow-Engineered system separates two concerns that prompt-based skills incorrectly conflate:

| Layer | Responsibility | Implementation |
|---|---|---|
| Orchestrator | State management, gate enforcement, feedback loops | Python/TypeScript script |
| LLM | Single-task text transformation | Stateless API call, scoped prompt |

The orchestrator treats the LLM as a function: `f(context) → text`. It calls this function, evaluates the output mechanically (run tests, check exit codes, parse structure), and decides what to do next. The LLM never manages its own state.

### The TDD Flow Engineering Pattern

A concrete implementation of TDD as a programmatic state machine, replacing the anthropomorphic "skill" approach:

#### Node 1: Test Generator

1. Orchestrator sends prompt: _"Here is a requirement. Output exactly one failing unit test. Return ONLY valid code. No markdown, no implementation."_
2. Orchestrator writes output to `test_feature.py`.
3. Mechanical Gate: Run `pytest test_feature.py`.
   - Test passes → LLM hallucinated implementation or wrote a vacuous test. Feed result back: _"Error: test must fail. Rewrite."_ Loop.
   - Test syntax error → Feed traceback back to LLM to fix. Loop.
   - Test fails with `AssertionError`/`NameError` → Gate cleared. Advance to Node 2.
   - LLM is forced through the gate by the execution environment, not by its own discipline.

#### Node 2: Implementation

1. Open a fresh LLM session (critical—wipe prior context so the model is not biased by its own verbosity).
2. Feed _only_ the failing test code and error trace: _"Write the minimum implementation to make this test pass. Output ONLY implementation code."_
3. Orchestrator writes output to `feature.py`.
4. Mechanical Gate: Run full test suite.
   - LLM cannot modify the test file—the orchestrator controls the filesystem. Physical impossibility replaces the prompt instruction "do not modify tests."
   - Test fails → Feed traceback, loop.
   - Exit code `0` → Gate cleared. Save state. Advance to Node 3.

#### Node 3: Refactor

1. Feed passing implementation: _"Optimise this code for readability. Do not change the function signature."_
2. Write output, run test suite.
3. Mechanical Gate: If tests fail → discard LLM output, revert to Node 2 artefact. The orchestrator's version control acts as the safety net. The LLM does not need to "know how to safely refactor."

### Why This Works

The Semantic-Statistical Mismatch means LLMs cannot self-enforce sequential state. Flow Engineering removes the requirement. The model's only job is generating a probable token sequence given a highly constrained single-task prompt. All methodology is offloaded to the deterministic execution environment.

Each LLM call is:

- Stateless: No memory of prior phases.
- Scoped: Receives only the artefact relevant to its current task.
- Evaluated mechanically: Exit codes and test results, not LLM self-assessment.

---

## Current Understanding

### Relationship to Skill Architecture

[[SoT - AI Agent Skill Architecture]] Pattern B ("Prompt + Scripts: Deterministic") is a partial instance of Flow Engineering—it recognises that scripts should handle tasks where LLMs are probabilistic. Flow Engineering extends this to the _entire workflow_, applying the orchestrator model to the control flow itself, not just isolated computation steps.

### The Correct Division of Labour

A prompt-based "skill" attempts to build a state machine in English. Flow Engineering correctly splits the concern:

- Natural language prompts: Single-task instructions with highly constrained output scope. Use few-shot examples and mechanical constraints (not philosophical ones).
- Orchestration code: All state, all gates, all feedback loops, all file system operations.

---

## Tensions & Gaps

- Adds engineering overhead: every Flow-Engineered workflow requires a wrapper script. Trade-off is acceptable for repeated, high-stakes workflows but overkill for one-shot tasks.
- The boundary between "safe to prompt" and "requires orchestration" is a useful design question without a fully formalised answer yet.

---

## Related Knowledge

- [[SoT - LLM Semantic-Statistical Mismatch]]—The epistemological foundation: why prompt-based gates fail
- [[SoT - AI Agent Skill Architecture]]—Pattern B as a partial instance
- [[SoT - Agentic AI Design Patterns]]—Broader taxonomy of agentic architectural patterns
- [[MOC - AI Software Engineering]]—The broader engineering map
