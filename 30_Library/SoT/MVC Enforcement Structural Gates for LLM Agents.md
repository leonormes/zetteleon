---
created: 2026-02-01T20:57:22+00:00
modified: 2026-02-04T07:27:25+00:00
status: evergreen
tags: [domain/ai, governance, type/protocol]
title: MVC Enforcement Structural Gates for LLM Agents
---

## MVC Enforcement: Structural Gates for LLM Agents

Minimum Viable Context (MVC) must be enforced by structural gates, not by human discipline or prompt instructions. Agents should be physically unable to receive information that violates MVC.

### The Three Gates of MVC Enforcement

#### 1. The Structural Interface Gate (Pull vs. Push)

The agent never receives a "context dump." It receives access to a set of typed queries.

- Allowed: `SCOUT_LOOKUP(Symbol)`, `FETCH_SKELETON(Symbol)`.
- Forbidden: Raw file injections, "Here is the code" pre-ambles.
- Effect: Prevents the agent from hallucinating dependencies that don't exist in the queryable graph.

#### 2. The Phase Gate (Planning vs. Surgery)

A strict separation of concerns between thinking and acting.

- Planning Phase: Access to Skeletons, Graphs, and Manifestos ONLY.
- Surgery Phase: Access to a single code body/file ONLY after a plan is approved.
- Effect: Forces the agent to reason about global constraints before getting lost in local procedural detail.

#### 3. The Context Budget Gate (Eviction Policy)

Context is not additive; it is a sliding window.

- Rule: Every new piece of context acquired must evict an old piece of context.
- Effect: Eliminates context rot and forces the agent to be intentional about what it "knows."

### Detection of Violations

If an agent mentions a symbol not found in its current structural interface, or proposes a change that violates a previously hidden invariant, the system should trigger a Structural Fault rather than attempting to recover via chat.

---

rel:: enforces [[Minimum Viable Context for LLMs Prevents Hallucination via Structural Boundaries]]

rel:: justifies [[Agentic REPL]]
