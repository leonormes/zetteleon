---
aliases: []
conformant: true
created: 2025-10-10T08:29:26+00:00
definition: "A disciplined methodology for developing AI agent systems that prioritises planning and documentation — a Product Requirement Document, a project structure, decision records, and type/test contracts — before code generation, on the premise that unmaintainable, context-less code is the default outcome of jumping straight to autonomous agent execution."
distinguishes_from: []
id: 20251008_Architecture_First_Approach_to_AI_Development
modified: 2026-09-09T12:34:08+00:00
permalink: llmeon/30-library/100-zettelkasten/architecture-first-approach-to-ai-development
tags: [domain/llm, topic/agent-architecture, topic/planning]
title: Architecture First Approach to AI Development
type: concept
used_in_claims: ["[[The Unit of Software Engineering Is Shifting from Code Lines to Intent Expressions]]"]
---

## Architecture First Approach to AI Development

An Architecture-First Approach is a disciplined methodology for developing AI agent systems that prioritises planning and documentation before code generation. This counters the tendency to jump directly to autonomous agents, which often results in unmaintainable code that lacks context.

The core components include:

- Product Requirement Document (PRD): Defines the context, scope, and requirements for the agent's task.
- Project Structure: A clear plan for the directory and file layout.
- Architectural Decision Records (ADRs): A log where agents document key decisions, preserving context for future iterations or other agents.
- Type Definitions and Tests: These serve as crucial, ensuring outputs are structured and reliable.

By establishing a robust architecture upfront, development can be accelerated by running parallel agents on independent, well-defined tasks.

[implements:: [[SoT - Agentic AI Design Patterns]], strength=2, confidence=medium]

### Related

- [[Agent-First Implementation Cycle]]—shared mechanism: both prioritise high-level design and planning as the primary human contribution before agent execution; that note focuses on the _ordering_ of drafting vs. review, this one on the _artefacts_ (PRD, ADRs, types/tests) that make the ordering safe.
- [[The Unit of Software Engineering Is Shifting from Code Lines to Intent Expressions]]—extends this note: the macro-delegation shift it describes is the natural endpoint of the architecture-first movement, once planning and specification become the primary human activity.
- [[Software Factory Pattern - Specialized Sandboxed Agents Autonomously Own Feature, Bugfix, and Incident Lifecycles]]—related: "running parallel agents on independent, well-defined tasks" is the entry-level version of the fuller autonomous-lifecycle-ownership pattern this note describes.

### See Also

- [[MOC - AI Software Engineering]]
- [[MOC - Agentic AI & LLM Agents]]

> Unresolved reference: `[[Architectural Decision Records ADRs for AI Agents]]` (a dedicated note on AI-specific ADR practice) has no matching note in the vault—converted to plain text above rather than left as a broken link. Worth authoring as a standalone concept note if this practice gets used enough to need its own worked examples; not fabricated here since none exist yet.
