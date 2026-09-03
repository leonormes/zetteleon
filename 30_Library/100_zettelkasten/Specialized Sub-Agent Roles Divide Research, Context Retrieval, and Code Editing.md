---
created: 2026-07-28T00:00:00+00:00
epistemic_status: medium
modified: 2026-08-29T09:36:05+00:00
permalink: llmeon/30-library/100-zettelkasten/specialized-sub-agent-roles-divide-research-context-retrieval-and-code-editing
proposition: Spec-driven development (as opposed to vibe coding) turns developer intent
  into strict specifications, then deploys an agent harness with specialized sub-agents
  — one for researching dependencies, one for pulling context via MCP servers, and
  one for code editing — rather than a single monolithic agent handling the whole
  task.
tags: [domain/llm, topic/agent-architecture, topic/spec-driven-development, topic/sub-agents]
title: Specialized Sub-Agent Roles Divide Research, Context Retrieval, and Code Editing
type: claim
---

## Specialized Sub-Agent Roles Divide Research, Context Retrieval, and Code Editing

Spec-driven development replaces the vibe-coding pattern ("describe roughly what you want, get code back") with an explicit intermediate artifact: a strict specification the AI must satisfy. But turning that specification into working code is itself decomposed—not handled by one agent doing everything, but by a harness coordinating specialized sub-agents:

- Research sub-agent: investigates dependencies, libraries, and prior art relevant to the task
- Context sub-agent: interacts with MCP servers to pull relevant codebase context, documentation, or external data
- Editing sub-agent: performs the actual code modification, working from the specification and the context the other two sub-agents assembled

Each sub-agent has a narrower job than "write the feature," which makes its output easier to verify and its failures easier to isolate.

### Scope & Conditions

Applies to agent harness designs for non-trivial coding tasks—tasks where research and context-gathering are separable, verifiable sub-problems from the code-writing itself. Overkill for small, self-contained changes where research and context-gathering add coordination overhead without benefit.

### Evidence

Source: "AI in the SDLC: Rethinking AI Coding Tools & AI Agents" (IBM Technology). Quote: "Move away from 'vibe coding' and focus on turning intents into strict specifications. Developers can use agent harnesses that deploy specialized sub-agents: one for researching dependencies, one interacting with MCP servers to pull context, and one for code editing" [05:57].

### Implications

- Decomposition improves reviewability: a human reviewing "what did the research sub-agent find" and "what did the editing sub-agent change" separately can catch errors more precisely than reviewing one large diff with mixed research and implementation reasoning baked in.
- Specification becomes the contract: the strict spec is what each sub-agent is ultimately accountable to, replacing the vague "did this feel right" judgment vibe coding relies on.
- Coordination overhead is real: multiple sub-agents require an orchestrating harness to sequence their work and pass context between them—this is not free.

### Related

- [[Agent Harness - Wrapping LLMs in Deterministic Software Controls]]—implements: the harness is the deterministic coordination layer across sub-agents.
- [[Deep Agents for Long Horizon Planning]]—related: sub-agent orchestration with specialized prompts/toolsets is the same pattern this note describes, generalized beyond coding.
- [[Vibe Coding - Rapid AI-Assisted Code Generation Without Engineering Rigor]]—contrast: spec-driven development is explicitly positioned against vibe coding.
- [[Model Context Protocol Standardises the LLM-to-Tool Interface]]—depends_on: the context sub-agent's MCP interaction requires this standardized interface.
- [[Overdelegation and Underdelegation Are Symmetric Failure Modes in AI-Assisted Coding]]—related: sub-agent role division is a structural mechanism for landing in the productive middle between the two extremes.

### See Also

- [[Architecture First Approach to AI Development]]

[implements:: [[Agent Harness - Wrapping LLMs in Deterministic Software Controls]], strength=4, confidence=high]

[depends_on:: [[Model Context Protocol Standardises the LLM-to-Tool Interface]], strength=3, confidence=medium]
