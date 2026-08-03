---
title: HEAD - Should agent context isolation come from lazy loading or separate processes?
type: question
tension: Two of my own SoTs prescribe opposite architectures for the same problem,
  and neither states the decision rule.
candidate_answers:
- Lazy loading (progressive disclosure) within one agent
- Separate processes per specialised role
- Both, split by task horizon
related_claims:
- '[[SoT - AI Agent Skill Architecture]]'
- '[[SoT - Agentic Roles]]'
sources:
- '[[SoT - AI Agent Skill Architecture]]'
- '[[SoT - Agentic Roles]]'
- '[[Continuous Autonomous Agent Loops Incur Significant API Cost]]'
tags:
- state/thinking
- prodos/head
conformant: true
status: open
prodos:
  kind: head
  lifecycle: active
created: 2026-08-03 13:20:30+01:00
modified: 2026-08-03 13:20:30+01:00
permalink: llmeon/20-thinking/21-workbench/head-should-agent-context-isolation-come-from-lazy-loading-or-separate-processes
---

## The Question

[[SoT - AI Agent Skill Architecture]] keeps one agent lean by loading skills on demand. [[SoT - Agentic Roles]] divides cognitive load across five specialised roles in separate processes. Both are mine, both are canonical, and they prescribe different answers to the same question: is context isolation achieved by *lazy loading* or by *separate processes*?

## Why It Matters

This is not academic — it determines how I build agent tooling at FitFile and in this vault. Getting it wrong costs either context pollution (one fat agent) or API spend and coordination overhead (many thin ones). [[Continuous Autonomous Agent Loops Incur Significant API Cost]] documents the cost ceiling of the multi-agent side, which is the strongest argument against it.

## What I Currently Think

The Skill/MCP/Subagent table in [[SoT - AI Agent Skill Architecture]] nearly resolves this — it stops one sentence short of stating the rule. My lean: lazy loading is the default because it is cheaper and simpler; separate processes earn their cost only when two roles need genuinely *conflicting* context (different system prompts, different tool sets), not merely a lot of it.

## What Would Settle It

Write the decision rule as a single sentence and put it in [[SoT - AI Agent Skill Architecture]], with a `contradicts` or `extends` typed edge to [[SoT - Agentic Roles]] so the graph records that the conflict was adjudicated rather than dropped. Test it against one real case: does the Hermes pipeline need separate processes, or would skills have done?

## Sources

- [[SoT - AI Agent Skill Architecture]]
- [[SoT - Agentic Roles]]
- [[Continuous Autonomous Agent Loops Incur Significant API Cost]]