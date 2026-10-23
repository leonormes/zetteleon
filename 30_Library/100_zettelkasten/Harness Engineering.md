---
conformant: true
created: 2026-04-14T20:26:00+00:00
created_utc: '2026-04-14T13:20:00Z'
definition: Harness engineering is the orchestration of multiple AI agent sessions through deterministic workflows to ensure repeatable and verifiable software development outcomes, representing a shift from single prompt or context quality to system-level harnesses that coordinate agent interactions toward a specific goal.
distinguishes_from: ["[[SoT - Context Engineering]]"]
kind: definition
modified: 2026-10-22T15:11:16+00:00
non_conformance_reason: ""
permalink: llmeon/30-library/100-zettelkasten/harness-engineering
source_title: Archon and Extreme Harness Engineering
source_url: https://youtube.com/watch?v=qMnClynCAmM
status: seed
tags: [ai-agents, harness-engineering, methodology, orchestration]
title: Harness Engineering
type: concept
upstream: '[[SoT - Agentic AI Design Patterns]]'
used_in_claims: ["[[Harness Engineering Splits into an Inner Harness and an Outer Harness]]", "[[The Prompt-Context-Harness-Loop Hierarchy Scales LLM Control Structures by Task Duration]]"]
---

## Harness Engineering

Harness engineering is the orchestration of multiple AI agent sessions through deterministic workflows to ensure repeatable and verifiable software development outcomes. It represents a shift from focusing on individual prompt or context quality to designing system-level harnesses that coordinate agent interactions toward a specific goal.

### Scope & Conditions

Applies to AI-assisted development seeking to move beyond the non-deterministic nature of single-prompt interactions.

### Evidence

> "It represents a shift from prompt and context engineering to harness engineering, where multiple AI agent sessions are coordinated to make coding tasks deterministic and repeatable."

### Implications

- Shifts the primary engineering focus from prompt crafting to system-level workflow architecture.
- Requires the creation of explicit nodes within the workflow for context curation, automated testing, and human review.

### Related

- [[Graph-Based Orchestration]]—supports: providing the structural framework for complex agentic harnesses.
- [[SoT - Context Engineering]]—extends: the stage this note says harness engineering moves on from; context engineering optimises the information reaching the model. [extends:: [[SoT - Context Engineering]]]
- [[Red-Teaming System Design Before Implementation Surfaces Guardrail Gaps]]—_applies adversarial review at design time, a harness-level safeguard._

### See Also

- [[SoT - AI Agent Skill Architecture]]

### Update (2026-09-21)

The definition above treats a harness as a single layer of deterministic control. Later notes in the vault refine it:

### Maps

- [[MOC - Agentic AI & LLM Agents]]—_Lists the related Agent Harness note; it does not yet list this one._
