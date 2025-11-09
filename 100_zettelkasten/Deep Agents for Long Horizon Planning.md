---
aliases: []
confidence: 
created: 2025-10-10T08:34:04Z
epistemic: 
id: 20251008_Deep_Agents_for_Long_Horizon_Planning
last_reviewed: 
modified: 2025-10-30T10:27:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [LangGraph, Planning, topic/technology/AI, topic/technology/AI/agents]
title: Deep Agents for Long Horizon Planning
type:
uid: 
updated: 
version:
---

**Deep Agents** is a framework built on `LangGraph` for creating agents capable of long-horizon planning and complex problem-solving. These agents use a loop to reason about a task, take actions, and reflect on the results.

Key architectural features include:

- **Sub-Agent Orchestration**: A main agent can delegate tasks to specialised sub-agents, each with its own tailored prompt and toolset. This is a form of [[Context Quarantine]].
- **Stateful Operation**: The agent's state tracks message history, a to-do list for planning, and a [[Virtual File System for Agent Concurrency]].
- **Planning Tools**: Agents are equipped with tools to manage their own to-do list, though a notable limitation is that the planning tool often overwrites the entire list rather than performing incremental updates.

**Links:**

- [[Context Quarantine]]
- [[Virtual File System for Agent Concurrency]]
- [[Dynamic Tool Loadout]]
