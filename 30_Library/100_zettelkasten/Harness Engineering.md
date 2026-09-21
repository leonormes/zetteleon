---
conformant: true
created: 2026-04-14T20:26:00+00:00
created_utc: '2026-04-14T13:20:00Z'
definition: Harness engineering is the orchestration of multiple AI agent sessions through deterministic workflows to ensure repeatable and verifiable software development outcomes, representing a shift from single prompt or context quality to system-level harnesses that coordinate agent interactions toward a specific goal.
distinguishes_from: ["[[SoT - Context Engineering]]"]
kind: definition
modified: 2026-09-21T11:14:03+00:00
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

- [[Agentic Collaboration Shift]]—shared mechanism: both describe the move from autocomplete to agent management.
- [[Graph-Based Orchestration]]—supports: providing the structural framework for complex agentic harnesses.
- [[SoT - Context Engineering]]—extends: the stage this note says harness engineering moves on from; context engineering optimises the information reaching the model. [extends:: [[SoT - Context Engineering]]]
- [[Context Engineering Fails Beyond Short-Duration Tasks]]—shared mechanism: names the duration boundary past which a further layer, this one, becomes necessary.
- [[Agent Harness - Wrapping LLMs in Deterministic Software Controls]]—shared mechanism: describes the same harness idea as wrapping a probabilistic model in deterministic software. The two notes overlap heavily.
- [[Specialized Sub-Agent Roles Divide Research, Context Retrieval, and Code Editing]]—shared mechanism: a concrete harness in which a coordinating layer splits work across specialised sub-agents.
- [[Code as Zero-Cost Deterministic Actor Alongside Engineers and Agents in Workflows]]—shared mechanism: the deterministic steps of a workflow are best written as plain code, which is the deterministic part of a harness.
- [[Intentional Compaction Clears History and Reseeds a Fresh Session with One Compressed Artifact]]—shared mechanism: a concrete context-curation step that a harness can place between phases.
- [[Engineer Involvement Compresses to Planning and Review as Agentic Workflows Mature]]—shared mechanism: describes where the human planning and review nodes sit once validation is automated.
- [[Lenient Harness Parsing Removes the Negative-Reinforcement Signal for Malformed Tool Output]]—shared mechanism: a design pitfall for harnesses, where silently repairing malformed output removes the signal that would discourage it.
- [[Loop Engineering Is Built From Six Components - Automation, Worktrees, Skills, Plugins, Sub-Agents, and State]]—extends: the next stage of the hierarchy, built from a concrete list of components.
- [[Loop Engineering Is a Rebrand of Existing SDLC Concepts, Not a New Paradigm]]—shared mechanism: a terminology critique of the neighbouring label; the same question, whether this is a new discipline or existing practice renamed, can be asked of this note's "shift" framing.

### See Also

- [[SoT - AI Agent Skill Architecture]]

### Update (2026-09-21)

The definition above treats a harness as a single layer of deterministic control. Later notes in the vault refine it:

- [[Harness Engineering Splits into an Inner Harness and an Outer Harness]]—_Describes itself as a refinement of this concept: a harness is two layers with different jobs, the tools the model touches and the surrounding validation and integration._
- [[Harness Engineering Prevents Context Degradation and Memory Leaks Over Prolonged Runtimes]]—_Isolates one job of a harness: countering context degradation over long runs by keeping state outside the model._
- [[The Prompt-Context-Harness-Loop Hierarchy Scales LLM Control Structures by Task Duration]]—_Places harness engineering between context engineering and loop engineering, ordered by task duration._

### Maps

- [[MOC - Agentic AI & LLM Agents]]—_Lists the related Agent Harness note; it does not yet list this one._
