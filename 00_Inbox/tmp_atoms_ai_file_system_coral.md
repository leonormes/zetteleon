---
captured_utc: "2026-04-09T10:03:23+01:00"
created: 2026-04-09T09:42:22+00:00
modified: 2026-04-09T10:01:45+00:00
signal_to_noise: "75% signal / 25% noise"
source_title: "SuperIntelligence: Why the Future of AI is a File System (CORAL)"
source_url: "http://www.youtube.com/watch?v=7n5EVMtYA4I"
status: tmp
title: tmp_atoms_ai_file_system_coral
type: tmp_atoms
---

## Atomic Knowledge Units

### Noise Removed

- "SuperIntelligence" clickbait framing in the title.
- Phrases like "next leap in capability" and "fascinating 'sideways' evolution".
- General excitement about the "future of AI" without specific architectural grounding.

### Atoms

#### Atom 1: Advanced Intelligence (ADI) Architecture

- kind: definition
- statement: Advanced Intelligence (ADI) is an architectural approach where the core Large Language Model (LLM) remains "frozen" while open-ended complexity and skill acquisition are handled by the surrounding multi-agent infrastructure.
- scope_and_conditions: Applies to AI system design where model weights are not updated; focuses on external orchestration.
- evidence: "The presenter refers to this approach as 'Advanced Intelligence' (ADI), as the core LLM remains frozen while the surrounding infrastructure handles the open-ended complexity" [01:15]
- implications:
  - Decouples reasoning (LLM) from memory and capability (infrastructure).
  - Shifts the focus of AI development from training to system engineering.
- confidence: high
- tags: [ai-architecture, adi, agents, orchestration]

#### Atom 2: Implicit Multi-Agent Coordination

- kind: mechanism
- statement: Global coordination between multiple autonomous agents is achieved implicitly through a shared, hierarchical file system directory (a ledger) rather than direct agent-to-agent communication.
- scope_and_conditions: Specifically used in the CORAL framework to manage 4–8 homogeneous agents.
- evidence: "Global coordination between agents is achieved implicitly through a shared public directory, rather than direct communication" [04:10]
- implications:
  - Reduces communication overhead and state synchronization complexity.
  - Provides a deterministic audit trail of all agent actions and hypotheses.
- confidence: high
- tags: [multi-agent-systems, coordination, file-system, determinism]

#### Atom 3: CORAL Shared Directory Schema

- kind: structure
- statement: The CORAL shared persistent memory is organised into three primary elements: 'Attempts' (function evaluation ledger), 'Notes' (textual hypotheses), and 'Skills' (reusable executable code).
- scope_and_conditions: Foundational data structure for agents running in parallel Git workspaces.
- evidence: "This directory is categorised into three main elements: Attempts… Notes… Skills…" [04:10]
- implications:
  - Separates raw execution logs (Attempts) from qualitative reasoning (Notes).
  - Enables the abstraction of successful logic into permanent assets (Skills).
- confidence: high
- tags: [knowledge-management, data-structure, coral, automation]

#### Atom 4: Heartbeat Intervention Protocol

- kind: procedure
- statement: An asynchronous background runtime that manages agent interrupts using interval and plateau triggers to prevent agents from repeating failed approaches or stagnating.
- scope_and_conditions: Controls the autonomous loop of agents to ensure progress and forced synthesis.
- evidence: "CORAL introduces a Heartbeat Intervention Protocol… This background runtime manages asynchronous interrupts using two distinct triggers" [05:42]
- implications:
  - Prevents agents from getting trapped in local minima or infinite loops.
  - Automates the transition from raw experience (notes) to abstracted knowledge (skills).
- confidence: high
- tags: [autonomous-agents, loops, optimization, protocol]

#### Atom 5: Plateau Trigger (Thermal Noise Heuristic)

- kind: heuristic
- statement: When an agent reaches a performance plateau, it is commanded to attempt an orthogonal mathematical approach to provide a "thermal noise" impulse, pushing it into unexplored territory.
- scope_and_conditions: Triggered by the Heartbeat Protocol when an agent's progress stalls.
- evidence: "Plateau Triggers: If an agent reaches a dead end, it is commanded to attempt a completely orthogonal mathematical approach, providing a 'thermal noise' impulse to push it into new territory" [06:46]
- implications:
  - Forces divergence in reasoning when convergence fails.
  - Mimics simulated annealing principles in an agentic workflow.
- confidence: high
- tags: [optimization, exploration, heuristics, problem-solving]

#### Atom 6: Cost Constraint of Continuous Autonomy

- kind: constraint
- statement: Continuous autonomous agent loops without human-in-the-loop intervention incur significant operational costs, estimated at approximately $20 per hour per agent.
- scope_and_conditions: Applies to commercial LLM API usage in persistent agentic frameworks.
- evidence: "a single three-hour run for one agent can cost around $60, while a multi-agent setup can quickly exceed hundreds of dollars in a single day" [28:34]
- implications:
  - Financial risk of "runaway loops" requires robust early-exit or monitoring protocols.
  - Barriers to entry for developers without significant API compute budgets.
- confidence: high
- tags: [economics, api-costs, scalability, constraints]
