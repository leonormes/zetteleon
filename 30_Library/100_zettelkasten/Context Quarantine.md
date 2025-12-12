---
aliases: []
confidence: 
created: 2025-10-10T08:29:46Z
epistemic: 
id: 20251008_Context_Quarantine
last_reviewed: 
modified: 2025-10-30T10:27:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Context Quarantine
type:
uid: 
updated: 
version:
---

**Context Quarantine** is a [[Context Engineering for LLMs]] strategy used in multi-agent systems. It involves dividing a complex task across multiple specialised agents, each with its own isolated sub-context. This prevents topic clash and distraction that could occur if all information were shared in a single, large context window.

A common implementation is a supervisor-worker pattern, where a supervisor agent routes sub-tasks to specialised agents (e.g., a "researcher" agent and a "writer" agent), ensuring each remains focused. This approach is fundamental to orchestrating [[Deep Agents for Long Horizon Planning]].

**Links:**

- [[Context Engineering for LLMs]]
