---
aliases: []
confidence: 
created: 2025-10-10T08:29:40Z
epistemic: 
id: 20251008_Dynamic_Tool_Loadout
last_reviewed: 
modified: 2025-10-30T10:27:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [Optimization, Tools, topic/technology/AI, topic/technology/AI/agents]
title: Dynamic Tool Loadout
type:
uid: 
updated: 
version:
---

**Dynamic Tool Loadout** is a [[Context Engineering for LLMs]] method where an agent is only given access to the tools that are relevant for its immediate task. Instead of binding a large, static set of tools to the agent, a selection process (often semantic matching) determines the optimal "toolset" for a given objective.

This reduces the complexity of the agent's decision-making process and minimises in-context confusion, as the LLM does not need to consider irrelevant tools. This is a core feature in frameworks like `deepagents` and is considered a best practice for building efficient, multi-tool agents.

**Links:**

- [[Context Engineering for LLMs]]
- [[Deep Agents for Long Horizon Planning]]
