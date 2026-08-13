---
aliases: [AI Coding MOC, LLM Engineering Map]
created: 2026-01-30T08:00:00+00:00
last-synthesis: 2026-04-04
modified: 2026-08-13T10:53:35+00:00
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

### 1. The Cognitive Bridge

The successful isomorphism between a repository's Static Analysis Graph (RIG) and the model's transient attention state—defined in full by [[SoT - LLM Codebase Understanding & Hierarchy]]. It is the process of reducing prompt entropy by encoding relationships as explicit structure.

### 2. Context Rot

The progressive decay of system-wide intent over a session.

- In Coding: The loss of architectural resolution as the "Micro View" dominates.
- In Knowledge Bases: The accumulation of redundant, stale, or "Parochial" commands and playbooks. See: [[prompt - DevOps Knowledge Architect]].

### 3. Perspective Drift

The regression of an LLM to its training mean. Prevented via Meta-Context (The Superego)—injecting a "Domain Manifesto" to enforce architectural priors over generic patterns.

### 4. The Curator (The "Problem Definer")

The shift from "Generating Code" to "Curating Context." The human value migrates to Context Engineering—framing the right problem and curating the information environment.

- See: [[SoT - AI-Resilient Task Taxonomy (Human 3.0)|The Four Resilient Roles]].

### 5. The Anthropomorphism Trap

The fundamental category error of treating a probabilistic token-prediction engine as a cognitive agent. Human-centric instructions ("write clean code", "use TDD") are statistical filters, not cognitive directives—they produce structural mimicry of methodology, not execution of it.

- [[SoT - LLM Semantic-Statistical Mismatch]]—The epistemological foundation.

### 6. Flow Engineering

The architectural response to the Anthropomorphism Trap: enforce all workflow constraints (gates, state, feedback loops) through a deterministic orchestration layer, reducing the LLM to a stateless single-task text transformation function.

- [[SoT - Flow Engineering]]—Pattern, implementation, and TDD case study.

### 7. The LLM Wiki Pattern

Standard RAG is stateless—nothing accumulates. The LLM Wiki Pattern flips this: the LLM maintains a persistent, structured wiki as a middle layer between raw sources and queries. Knowledge compounds across sessions instead of being discarded. This vault implements this pattern via ProdOS.

- [[SoT - LLM Wiki Pattern]]—Architecture, three core operations, and ProdOS isomorphism.

### 8. The Typed Answer Contract (TAC)

Free-text output is the same liability on the output side that stateless RAG is on the retrieval side: confident-sounding prose is indistinguishable from grounded prose until a human catches the error. TAC forces every answer into a small contract instead—stated confidence, cited evidence, and an explicit "insufficient context" flag—so ungrounded output is caught at generation time rather than after it has already been written into a note. This vault enforces a markdown-native version of TAC across its governed prompt library via [[Protocol - Typed Answer Contract (TAC) for Vault Agents]].

- [[SoT - Typed Answer Contract (TAC) for LLM Output]]—Schema fields, production results, and the code-to-markdown adaptation for this vault.

---

Status: 🌿 Growing
