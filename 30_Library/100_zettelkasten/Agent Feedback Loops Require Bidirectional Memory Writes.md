---
created: 2026-07-28T00:00:00+00:00
epistemic_status: high
modified: 2026-08-13T10:56:48+00:00
permalink: llmeon/30-library/100-zettelkasten/agent-feedback-loops-require-bidirectional-memory-writes
proposition: Agents that learn across sessions require not only memory retrieval (reading
  prior discoveries) but also memory writes (recording new discoveries). Unidirectional
  memory (read-only) is inert; bidirectional memory enables agents to compound knowledge
  and avoid repeating failed patterns.
tags: [domain/llm, topic/agent-architecture, topic/feedback-loops, topic/learning, topic/persistent-memory]
title: Agent Feedback Loops Require Bidirectional Memory Writes
type: claim
---

## Agent Feedback Loops Require Bidirectional Memory Writes

A persistent memory that only allows reads is a museum—agents can consult the past but not record what they discover. True agent learning across sessions requires write access: agents must be able to record discoveries, decisions, failed attempts, and refined patterns back into the persistent store.

This creates a feedback loop where Session N writes discoveries that Session N+1 reads and builds upon.

### Scope & Conditions

Applies to iterative or learning-oriented agent workflows where the goal is to improve or discover patterns across multiple runs. Does not apply to stateless, single-run inference.

### Evidence

Source: Cogni platform design emphasises two-way memory writes as a core feature distinguishing persistent memory from static read-only documentation.

### Implications

- Knowledge compounding: Each session adds to the persistent store; knowledge grows with each iteration.
- Failure avoidance: Agents record "we tried this and it failed" so subsequent sessions don't retrace failed paths.
- Pattern discovery: Across multiple sessions, an agent can identify patterns ("X works better when Y is present") that emerge only from aggregate data.
- Reduced exploration cost: Agents don't explore the full search space every time if prior sessions have mapped parts of it.

### Counterargument

Write access to memory introduces risk:

- Agents might write corrupted, hallucinated, or contradictory information.
- Malicious or buggy agents could poison the knowledge base.
- Management overhead: deciding what deserves to be written, validating writes, resolving conflicts.

This is why structured schemas matter—writes should be constrained to a defined contract (frontmatter, structured fields) rather than free-form prose.

### Related

- [[Persistent Memory Layers Enable Multi-Session Agent Continuity]]—enables: write access is the missing half of that architecture.
- [[SoT - Evolutionary Note System]]—implements: provides a protocol for how memory entries evolve (draft → stable → archived) under write pressure.
- [[Layered Knowledge Architecture]]—related: the "schema layer" enforces contracts that validate writes.

%%[supports:: [[Persistent Memory Layers Enable Multi-Session Agent Continuity]], strength=5, confidence=high]%%

%%[implements:: [[SoT - Evolutionary Note System]], strength=3, confidence=medium]%%
