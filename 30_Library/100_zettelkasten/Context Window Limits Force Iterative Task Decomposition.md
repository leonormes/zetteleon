---
created: 2026-07-28T00:00:00+00:00
epistemic_status: high
modified: 2026-08-29T09:35:59+00:00
permalink: llmeon/30-library/100-zettelkasten/context-window-limits-force-iterative-task-decomposition
proposition: LLM context windows are finite. When a developer attempts to have the
  "LLM reason about an entire application at once, the context fills and the LLM's"
  reasoning degrades. Production-grade AI-assisted development requires breaking work
  into discrete, context-bounded tasks and addressing them iteratively.
tags: [domain/llm, topic/architecture, topic/context-engineering, topic/task-decomposition]
title: Context Window Limits Force Iterative Task Decomposition
type: claim
---

## Context Window Limits Force Iterative Task Decomposition

A developer tempted by Vibe Coding might try to hand the LLM a 50-page requirements document and say "build my app." The LLM will consume tokens until the context window fills, at which point its ability to reason about earlier requirements degrades. Earlier context is forgotten, contradictions emerge, and the "complete" solution is actually incoherent.

The alternative is to break the work into stories and tasks small enough that the LLM can reason about each one in isolation, with fresh context, without the load of prior work bleeding in.

### Scope & Conditions

Applies to any task where the full scope exceeds the LLM's available context window. For small projects or well-defined subproblems, a single LLM invocation might suffice. For applications of realistic complexity, iteration is mandatory.

### Evidence

Source: "Nobody Pages the LLM: Engineering Rigour for Vibe Coding" (Ritesh Modi). Direct quote: "Don't bombard the LLM with 10 things at once, as its context window and memory will fail" [18:15].

### Implications

- Planning becomes load-bearing: Breaking work into tasks requires explicit planning and architecture upfront. Vibe coding's fantasy of "no planning" becomes impossible at scale.
- Iterative review points: Each task boundary is a natural review point. Completing one task, reviewing it, then moving to the next is more expensive (in time) but catches problems earlier.
- Architectural coherence: If tasks are decomposed correctly (at architecture boundaries), the resulting code is more likely to fit together. If decomposition is ad-hoc, the risk of integration failures rises sharply.

### Related

- [[Vibe Coding - Rapid AI-Assisted Code Generation Without Engineering Rigor]]—context: describes why naive vibe coding fails.
- [[AI-Generated Code Without Human Review Creates Production Risk]]—consequence: unmanaged context leads to coherence failures.
- [[Persistent Memory Layers Enable Multi-Session Agent Continuity]]—related: persistent memory is one strategy to make task decomposition less expensive (agent remembers prior decisions).
- [[Claude Code Session Isolation Forces Context Reloading Across Invocations]]—related: similar constraint at the session layer.

### See Also

- [[SoT - Iterative Implementation Protocol]]
