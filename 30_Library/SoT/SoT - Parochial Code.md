---
aliases: [Boundary Violation, Location-Unaware Code, Myopic Coding]
created: 2026-01-30T06:57:15+00:00
modified: 2026-07-13T08:45:19+00:00
permalink: llmeon/30-library/so-t/so-t-parochial-code
see_also: []
superseded_by: ''
supersedes: ''
tags: [anti-pattern, llm-failure-mode, software-architecture]
title: SoT - Parochial Code
---

## Parochial Code

Parochial Code is an architectural anti-pattern where code is written to solve a local problem without awareness of the broader system context. It is characterized by a violation of architectural boundaries—code that functions correctly in isolation but creates friction, redundancy, or technical debt at the system scale.

### The Core Mechanism

Parochial code is not defined by illogical logic, but by Myopic Scope. It occurs when the creator (human or LLM) holds a "Micro View" (implementation details) but lacks the "Macro View" (architectural coherence).

#### Key Characteristics

1. False Modularity: The code superficially adheres to formatting or file structure but violates [[SoT - Atomicity and Loose Coupling|Separation of Concerns]] by importing unrelated dependencies or leaking abstractions.
2. Defensive Redundancy: It re-implements safety checks or validations that the broader architecture (e.g., the Type System or Middleware) already guarantees. This is a primary symptom of [[SoT - Context Rot|Context Rot]].
3. Volatile Coupling: It hard-couples to specific implementation details rather than stable interfaces, making future refactoring high-risk.

> [!warning] The Parochial Paradox
> Parochial code often passes code review because it looks "safe" and "correct" when viewed in a specific PR diff. It is only when viewing the whole graph that the redundancy and coupling become visible.

### Relevance to LLMs

Parochial Code is the default failure mode of [[SoT - LLM Codebase Understanding & Hierarchy|Large Language Models]].

- Context Window Limits: LLMs often cannot "see" the entire codebase. They optimize the snippet they are currently generating (The Micro) at the expense of system coherence (The Macro).
- Perspective Drift: Without a strong "Meta-Context" or "Architectural Skeleton", the LLM regresses to the mean of its training data, ignoring project-specific constraints (e.g., introducing OOP patterns into a [[SoT - Data-Oriented Design|Data-Oriented Design]] system).

### Treatment & Prevention

The solution is Architectural Explicitization:

1. Enforce Domain Boundaries: Use linting or strict visibility modifiers (e.g., Rust's module system) to physically prevent parochial imports.
2. Meta-Context Injection: For LLMs, provide an explicit "Architectural Skeleton" or "Map" in the system prompt, rather than just raw file contents.
3. Interface-First: Shift focus from "Does this implementation work?" to "Does this interface fit the graph?"

---

See Also: [[SoT - Context Rot]], [[SoT - Context Rot|Perspective Drift]], [[SoT - Type-Driven Development (The Torvalds Loop)#The Problem: \"Shotgun Parsing\"|Shotgun Surgery]], [[SoT - Dimensions of Code Understanding]]
