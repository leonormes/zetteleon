---
aliases: [Context Degradation, Perspective Drift, Session Entropy]
conformant: false
created: 2026-01-30T08:30:00+00:00
modified: 2026-07-20T16:33:52+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-context-rot
tags: [context-engineering, llm-failure-mode, prompt-engineering]
title: SoT - Context Rot
type: sot
---

## Context Rot

Context Rot is the progressive loss of high-level architectural awareness during an LLM session. It is the primary cause of [[SoT - Parochial Code]]. As the conversation extends, the model's attention shifts from the "System Map" (Macro) to the "Current Snippet" (Micro), leading to code that is syntactically correct but architecturally invalid.

### The Mechanism

Context Rot is not a bug; it is a function of Token Entropy.

1. Limited Window: As the session grows, earlier instructions (Architecture) are evicted or diluted by recent tokens (Implementation details).
2. Drift: The model regresses from "Your Project's Dialect" back to "Generic Internet Code" (The Mean).
3. Fragmentation: The model begins to treat the current file as the entire universe, ignoring cross-module constraints.

### Prevention Strategies

We cannot "solve" Context Rot, but we can manage it through Context Engineering:

#### 1. Compressed Representation

Do not feed raw files. Feed Rules & Relationships. The model needs the _Physics_ of the system, not just the _Matter_.

#### 2. Concentrated Detail

Use high-density prompts. Provide a Symbol Table or Interface Map instead of full implementation code. This maximizes the information-to-token ratio.

#### 3. The Architectural Skeleton

Maintain a living artifact (e.g., `architecture_skeleton.md`) that is re-injected at the start of every new task.

- Contains: Dependency Graph, Interface Contracts, Forbidden Patterns.
- Excludes: Implementation details of unrelated modules.

#### 4. Active Traversal

Force the model to "Zoom Out." Before writing code, ask it to:

- "List all files that depend on this interface."
- "Trace the data flow through the type system."
- "Simulate the [[SoT - Temporal Projection|Blast Radius]] of this change."

---

See Also: [[SoT - Parochial Code]], [[SoT - Macro-Micro Unification]], [[Context Engineering]]
