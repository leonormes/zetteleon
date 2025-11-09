---
aliases: []
confidence: 
created: 2025-10-10T08:29:17Z
epistemic: 
id: 20251008_Context_Engineering_for_LLMs
last_reviewed: 
modified: 2025-10-30T10:27:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Context Engineering for LLMs
type:
uid: 
updated: 
version:
---

**Context Engineering** is the practice of managing and optimising the information (the "context") provided to a Large Language Model (LLM) to improve its performance, reliability, and efficiency. Poor context management leads to several failure modes:

- **Context Poisoning:** The model repeatedly includes hallucinated or incorrect information in its context, reinforcing errors.
- **Distraction:** An overly large or noisy context window causes the model to focus on irrelevant details.
- **Confusion/Clash:** Contradictory information in the context harms the agent's reasoning and behaviour.

There are six primary methods for effective context engineering:

1. [[Dynamic Tool Loadout]]: Provides the agent with access to only the tools relevant for the current task.
2. [[Context Pruning]]: Uses logic or another LLM call to strip irrelevant information from the context.
3. [[Context Quarantine]]: Isolates different contexts across multiple specialised agents to prevent topic clash, often managed by a supervisor agent.

**Links:**

- [[Dynamic Tool Loadout]]
- [[Context Pruning]]
- [[Context Quarantine]]
