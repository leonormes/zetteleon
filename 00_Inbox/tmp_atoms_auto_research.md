---
captured_utc: "2026-04-09T09:02:42Z"
created: 2026-04-09T09:10:07+00:00
modified: 2026-04-09T10:01:45+00:00
signal_to_noise: "85% signal / 15% noise"
source_title: "How to set up and use the Auto Research framework"
source_url: "http://www.youtube.com/watch?v=bc4NrE0cOE0"
status: tmp
title: tmp_atoms_auto_research
type: tmp_atoms
---

## Atomic Knowledge Units

### Noise Removed

- Specific UI navigation steps (e.g., "click the '+' icon").
- Download instructions for specific external "Accelerator" programs.
- Generic "DIY Route" vs "Pre-built" marketing distinctions.

### Atoms

#### Atom 1: Atomic Optimization Criteria

- kind: constraint
- statement: Optimization criteria must be defined as clear, testable, binary (true/false) conditions containing only one variable per criterion.
- scope_and_conditions: Used when defining goals for automated research or agentic evaluation loops.
- evidence: "Define your specific criteria… These must be clear, testable, true/false conditions with only one variable per criterion [10:08]"
- implications:
  - Eliminates ambiguity in "fuzzy" requests (e.g., "make it short").
  - Enables objective measurement of success for automated agents.
- confidence: high
- tags: [prompt-engineering, optimization, criteria, evaluation]

#### Atom 2: Evaluation Mode Selection

- kind: distinction
- statement: Evaluation pipelines should distinguish between subjective tasks requiring an LLM judge and objective tasks suited for deterministic scripts.
- scope_and_conditions: Selecting the evaluation mechanism during task setup.
- evidence: "AI/LLM judge (for subjective or creative tasks) or a standard deterministic script (for objective tasks) [16:46]"
- implications:
  - Improves reliability for technical/objective checks.
  - Reduces token usage by offloading objective checks to local code.
- confidence: high
- tags: [evaluation, llm-judge, automation, system-design]

#### Atom 3: Iteration Loop Diminishing Returns

- kind: heuristic
- statement: Effective automated optimization typically requires 5 to 10 iterations; exceeding 15 iterations tends to degrade output quality and increase token costs without gain.
- scope_and_conditions: Setting the loop count for recursive optimization tasks.
- evidence: "recommends running 5 to 10 iterations; going beyond 15 can degrade the output and unnecessarily increase your token costs [17:00]"
- implications:
  - Prevents "drift" or over-fitting in long loops.
  - Serves as a primary constraint for cost-management in agentic workflows.
- confidence: high
- tags: [optimization, iterations, token-management, quality-control]

#### Atom 4: Manual Framework Adaptation

- kind: procedure
- statement: Adapting machine-learning-specific frameworks for general knowledge tasks requires iterative collaboration with an LLM to redefine context and logic.
- scope_and_conditions: When repurposing specialized code (like Karpathy's original repository) for broader use cases.
- evidence: "Because the original framework was built specifically for machine learning, you will need to collaborate with Claude to adapt it for your specific use cases [06:11]"
- implications:
  - Frameworks are not "plug-and-play" across domains without logic restructuring.
  - LLMs can be used to refactor their own optimization logic.
- confidence: medium
- tags: [auto-research, implementation, adaptation, logic]
