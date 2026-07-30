---
conformant: false
created: 2026-04-10T12:00:00+00:00
modified: 2026-07-28T09:12:43+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/advanced-intelligence-adi-architecture
tags: [adi, agents, ai-architecture, orchestration]
title: Advanced Intelligence (ADI) Architecture
type: concept
---

## Advanced Intelligence (ADI) Architecture

Advanced Intelligence (ADI) is an architectural stance in which the core Large Language Model remains frozen—its weights are never updated—while all open-ended capability growth is handled by the surrounding multi-agent infrastructure. Intelligence, in this framing, is a property of the system, not the model.

### Scope & Conditions

Applies to AI system design where retraining is impractical or undesirable. The architecture assumes external orchestration (file systems, shared memory, skill libraries) can substitute for in-weights learning. Does not apply to scenarios requiring genuine model-level generalisation.

### Evidence

> "The presenter refers to this approach as 'Advanced Intelligence' (ADI), as the core LLM remains frozen while the surrounding infrastructure handles the open-ended complexity" [01:15]

### Implications

- Decouples reasoning (LLM) from memory and capability acquisition (infrastructure), allowing each to evolve independently.
- Shifts AI development effort from training pipelines to system engineering—infrastructure becomes the primary locus of capability improvement.

### Related

- [[Architecture First Approach to AI Development]]—shared mechanism: both disciplines keep a core layer stable (frozen model / upfront design) and invest complexity in the surrounding infrastructure rather than the core artefact.
- [[Deep Agents for Long Horizon Planning]]—shared mechanism: LangGraph-based deep agents similarly keep the LLM layer stable while building stateful orchestration infrastructure around it to manage long-horizon complexity.
- [[SoT - Agentic AI Design Patterns]]—extends: ADI names the design philosophy that the full agentic pattern taxonomy assumes; it is the architectural premise rather than a specific pattern.
