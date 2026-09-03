---
aliases: [Context Compression, Context Engineering, High-Signal Prompting, Information Density, Prompt Optimization]
conformant: false
created: 2026-01-30T11:00:00+00:00
modified: 2026-08-29T09:36:35+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-context-engineering
tags: [ai-engineering, context-management, discipline, prompt-engineering]
title: SoT - Context Engineering
type: sot
---

> Open threads: [[HEAD - Do declarative rules or few-shot demonstrations constrain LLM output better?]]

[depends_on:: [[The Architectural Guardian]], strength=4, confidence=high]

## Context Engineering

Context Engineering is the technical discipline of optimizing the information flow between a codebase and an LLM. Its goal is to maximize Architectural Signal while minimizing Token Noise.

### The Golden Rule: Compression > Accumulation

Effective prompting is not about providing _more_ information; it is about providing _higher-density_ information.

- Context Accumulation (Noise): Dumping raw files, logs, and documentation into the prompt. This leads to [[SoT - Context Rot]] as the model's attention is diluted across low-value tokens.
- Context Compression (Signal): Distilling the codebase into invariants, interfaces, and constraints. This encodes the Physics of the system rather than its Matter.

### Core Principles

#### 1. The Information Density Law

Every token must justify its existence. If a line of code does not clarify a boundary or an interface, it is "Noise" and should be skeletonized.

#### 2. Encode Relationships, Not Files

An LLM understands the system better through a Dependency Graph than a list of file contents.

- _Instead of:_ "Here is `auth.rs` and `db.rs`."
- _Use:_ "`AuthService` calls `DatabasePool`. `DatabasePool` is a singleton."

#### 3. Summarization of Invariants

Prompts should resemble a Domain Manifesto. State the "Laws of the Universe" (e.g., "All data is immutable," "No UI logic in the Service layer") to enforce the [[SoT - Dimensions of Code Understanding|Constraint Dimension]].

### Implementation Artifacts

- [[SoT - Structural Intelligence|RepoMap]]: A compressed AST-based map of the project.
- Architectural Skeleton: A living document mapping interfaces and flows.
- Meta-Context: The persistent "Superego" injected via [[The Architectural Guardian]].

---

See Also: [[SoT - Context Rot]], [[SoT - Macro-Micro Unification]], [[SoT - Structural Intelligence]]
