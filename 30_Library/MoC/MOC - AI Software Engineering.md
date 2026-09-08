---
aliases: [AI Coding MOC, LLM Engineering Map]
created: 2026-01-30T08:00:00+00:00
last-synthesis: 2026-04-04
modified: 2026-08-29T09:36:28+00:00
permalink: llmeon/30-library/mo-c/moc-ai-software-engineering
tags: [ai-engineering, map-of-content, moc]
title: MOC - AI Software Engineering
---

Core Theme: [[SoT - LLM Codebase Understanding & Hierarchy|Engineering the "Cognitive Bridge"]] between probabilistic AI models and deterministic software systems.

## 🌌 The "Unified Field" Theory

_Reconciling the "Quantum" (Micro-Logic) with "Relativity" (Macro-Architecture)._

- [[SoT - Macro-Micro Unification]] - The fundamental theory: Why architectural integrity fails during "zoomed-in" coding.
- [[SoT - Parochial Code]] - The primary failure mode: Code that is locally correct but globally "blind."
- [[SoT - Dimensions of Code Understanding]] - The evaluation framework: Navigating the 6 dimensions of true system awareness.
- [[SoT - LLM Codebase Understanding & Hierarchy]] - The technical implementation: Using RIG/AST to force token alignment with architecture.

## 🛠️ Core Engineering Concepts
## 🛠️ Core Engineering Concepts

### 1. The Cognitive Bridge

The successful isomorphism between a repository's Static Analysis Graph (RIG) and the model's transient attention state—defined in full by [[SoT - LLM Codebase Understanding & Hierarchy]]. It is the process of reducing prompt entropy by encoding relationships as explicit structure.

- [[SoT - Macro-Micro Unification]]—the underlying "Cognitive Physics" theory: why holding Architecture (Macro) and Syntax (Micro) in mind simultaneously is a fundamental cognitive limit, not a discipline failure.
- [[SoT - Parochial Code]]—the anti-pattern that results when the bridge fails: code that is locally correct but globally blind.
- [[SoT - Dimensions of Code Understanding]]—the six-dimensional framework (Structural, Causal, Idiomatic, Constraint, Intent, Temporal) for evaluating whether an agent has actually crossed the bridge, as a behavioural outcome rather than declarative recall.
- [[SoT - Structural Intelligence]]—the technical mechanism: treating code as a deterministic graph (AST/CFG/RepoMap) rather than a probabilistic token stream, so the bridge is built on ground truth.
- [[SoT - Temporal Projection]]—the "Blast Radius" metric for judging whether a bridge, once built, will hold under future change.
- [[SoT - Atomicity and Loose Coupling]]—the same macro/micro tension restated for knowledge notes rather than code: atoms must be independently legible yet interconnected.
- [[The Architectural Guardian]]—the concrete mechanism (a persistent meta-context prompt) that operationalises the bridge inside an agent pipeline.

### 2. Context Rot

The progressive decay of system-wide intent over a session, formally defined in [[SoT - Context Rot]].

- In Coding: The loss of architectural resolution as the "Micro View" dominates, driven by limited context windows, drift toward "Generic Internet Code," and fragmentation.
- In Knowledge Bases: The accumulation of redundant, stale, or "Parochial" commands and playbooks. See: [[prompt - DevOps Knowledge Architect]].

### 3. Perspective Drift

The regression of an LLM to its training mean, one of Context Rot's specific mechanisms—prevented via Meta-Context (The Superego): injecting a "Domain Manifesto" via [[The Architectural Guardian]] to enforce architectural priors over generic patterns.

### 4. The Curator (The "Problem Definer")

The shift from "Generating Code" to "Curating Context." The human value migrates to Context Engineering—framing the right problem and curating the information environment.

- [[SoT - Context Engineering]]—the discipline itself: compression over accumulation, encoding relationships rather than files, summarising invariants as a Domain Manifesto.
- [[SoT - The Context Engine]]—a concrete implemented system that applies Context Engineering: its own history (a deprecated "Shadow Database" phase, superseded by the current AST/RepoMap-based "Structural" phase) is itself a worked example of retiring outdated architectural thinking rather than letting it linger undocumented.
- See: [[SoT - AI-Resilient Task Taxonomy (Human 3.0)|The Four Resilient Roles]].

### 5. The Anthropomorphism Trap

The fundamental category error of treating a probabilistic token-prediction engine as a cognitive agent. Human-centric instructions ("write clean code", "use TDD") are statistical filters, not cognitive directives—they produce structural mimicry of methodology, not execution of it.

- [[SoT - LLM Semantic-Statistical Mismatch]]—The epistemological foundation.
- [[SoT - Human vs AI Cognition]]—Why the trap is so hard to resist even for experts: the Eliza Effect, the Language-Intelligence Link, and the Symbol Grounding Problem that separates human grounded cognition from LLM distributional semantics.

> **Tension, not resolved:** [[MOC - Agentic AI & LLM Agents]] routinely uses role/autonomy language ("the agent decides," "escalates ambiguous decisions," "the Architect enforces") for architectural convenience—see especially [[SoT - Agentic Roles]]. That framing is functional shorthand for a state machine and its control flow, not a claim that the underlying model exercises judgment. The two MOCs are not in conflict, but a reader moving between them should not mistake the Agentic MOC's operational vocabulary for a retraction of this section.

### 6. Flow Engineering

The architectural response to the Anthropomorphism Trap: enforce all workflow constraints (gates, state, feedback loops) through a deterministic orchestration layer, reducing the LLM to a stateless single-task text transformation function.

- [[SoT - Flow Engineering]]—Pattern, implementation, and TDD case study.

### 7. The LLM Wiki Pattern

Standard RAG is stateless—nothing accumulates. The LLM Wiki Pattern flips this: the LLM maintains a persistent, structured wiki as a middle layer between raw sources and queries. Knowledge compounds across sessions instead of being discarded. This vault implements this pattern via ProdOS.

- [[SoT - LLM Wiki Pattern]]—Architecture, three core operations, and ProdOS isomorphism.

### 8. The Typed Answer Contract (TAC)

Free-text output is the same liability on the output side that stateless RAG is on the retrieval side: confident-sounding prose is indistinguishable from grounded prose until a human catches the error. TAC forces every answer into a small contract instead—stated confidence, cited evidence, and an explicit "insufficient context" flag—so ungrounded output is caught at generation time rather than after it has already been written into a note. This vault enforces a markdown-native version of TAC across its governed prompt library via [[Protocol - Typed Answer Contract (TAC) for Vault Agents]].

- [[SoT - Typed Answer Contract (TAC) for LLM Output]]—Schema fields, production results, and the code-to-markdown adaptation for this vault.