---
created: 2026-02-01 20:57:13+00:00
modified: 2026-02-04 07:27:42+00:00
status: evergreen
tags:
- architecture
- concept/attention
- domain/ai
title: Targeting LLM Attention Requires Encoding Relevance as Structure
permalink: llmeon/30-library/100-zettelkasten/targeting-llm-attention-requires-encoding-relevance-as-structure
---

## Targeting LLM Attention Requires Encoding Relevance as Structure

LLM attention should be targeted by structural constraints rather than content volume. The goal is for the model to traverse meaning, never to search for it.

### The Three-Layer Attention Model

1. Structural Constraint (Mandatory): High-level graphs and symbol tables that define what is allowed to exist in the model's world.
2. Semantic Anchors (Mandatory): High-signal names and Skeletons that define what entities mean and their intent.
3. Procedural Detail (Surgical/Optional): The actual code bodies or data values required for a specific mutation.

### The Operational Rule

Every token not structurally justified is adversarial noise. If a piece of information does not define an identity, a relationship, or a constraint, it should be excluded to prevent Attention Dilution.

---

rel:: supports [[Minimum Viable Context for LLMs Prevents Hallucination via Structural Boundaries]]

rel:: explains [[Targeting LLM Attention via Structural Constraints]]