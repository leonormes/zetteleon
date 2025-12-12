---
aliases: []
confidence: 
created: 2025-10-10T08:29:43Z
epistemic: 
id: 20251008_Context_Pruning
last_reviewed: 
modified: 2025-10-30T10:27:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Context Pruning
type:
uid: 
updated: 
version:
---

**Context Pruning** is a [[Context Engineering for LLMs]] technique used to control context window bloat. It involves using an LLM prompt or other logic to analyse the existing context and remove information that is irrelevant to the current task. This is often applied to the output of tools before it is added to the agent's message history.

**Caveat**: This method carries a risk of information loss. Over-aggressive pruning can remove mission-critical facts, so it must be implemented with care. A related, less risky technique is Context Summarisation.

**Links:**

- [[Context Engineering for LLMs]]
