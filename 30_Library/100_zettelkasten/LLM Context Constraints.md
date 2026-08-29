---
created: 2026-04-13T14:41:15+00:00
created_utc: 2026-04-13 11:20:00+00:00
kind: constraint
modified: 2026-08-29T09:36:02+00:00
permalink: llmeon/30-library/100-zettelkasten/llm-context-constraints
source_title: AI Agent Architecture and the Modern Tech Stack
source_url: https://gemini.google.com/app/509937047bd0b955
status: seed
tags: [context-window, llm, memory, tokens]
title: LLM Context Constraints
type: atom
upstream: '[[HEAD The Failure of Human-Centric Design]]'
---

## LLM Context Constraints

Large Language Models are restricted by a finite token-based context window that serves as the model's immediate short-term memory. Because expanding this window increases both latency and operational cost, external memory solutions and efficient context management are required for long-term or data-intensive projects.

### Scope & Conditions

Applies to all transformer-based models. It necessitates the use of external storage (e.g., vector databases) when the total information exceeds the model's native capacity.

### Evidence

> "LLMs are constrained by a context window (measured in tokens), which functions as short-term memory. Expanding this window increases latency and cost…"

### Implications

- Long-term information must be stored externally (e.g., vector databases).
- Developers must prioritise and compress information to fit within token limits.

### Related

- [[Context Volume Plateau]]—shared mechanism: both identify the technical limitations of the context window.
- [[SoT - The RPI Workflow (Context Engineering)]]—shared mechanism: uses "Context Economics" to manage these specific constraints.
- [[MOC - AI Software Engineering]]—See Also.
