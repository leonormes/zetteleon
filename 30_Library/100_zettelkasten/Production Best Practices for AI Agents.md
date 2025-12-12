---
aliases: []
confidence: 
created: 2025-10-10T08:29:59Z
epistemic: 
id: 20251008_Production_Best_Practices_for_AI_Agents
last_reviewed: 
modified: 2025-10-30T10:27:47Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [DevOps, Production, Reliability, topic/technology/AI]
title: Production Best Practices for AI Agents
type:
uid: 
updated: 
version:
---

Deploying [[AI Agentic Workflows]] to production requires a unique set of best practices beyond standard software engineering, focusing on reliability, security, and maintainability.

- **Use Staging Environments**: Never connect an AI agent directly to a production database or service. Always test thoroughly in a secure staging environment with real data.
- **Graceful Failure and Fallbacks**: Build in logic for retries, API failovers, and the ability to fall back to a simpler model or a default state if an agent fails.
- **Cost and Performance Optimisation**: Use caching for repeated queries to reduce costs and latency. Prefer the smallest, most efficient model that is suitable for each sub-task.
- Embrace [[Test Driven Development for AI Agents]]: Make evaluation a first-class engineering concern from the start.
