---
AoL: System
candidate_answers: []
closing_condition: true
conformant: true
created: 2026-08-18T11:17:00+00:00
modified: 2026-08-18T11:17:57+00:00
permalink: llmeon/20-thinking/21-workbench/head-how-to-unify-the-co-s-query-engine
related_claims: ["[[Protocol - Action-First GTD (LLM Chief of Staff)]]", "[[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]]"]
sources: []
status: open
tags: [prodos/head, state/thinking]
tension: The components for the CoS Query Engine exist (Jira, GitKraken, Todoist,
  Pieces LTM), but they are siloed. There is no unified protocol to sweep all tools,
  assign importance, and push ADHD-optimised starter tasks to Todoist in one pass.
title: HEAD - How to unify the CoS Query Engine
type: question
---

## The Question

How do we wire together the existing siloed components (GTD Context Auditor, CoS Work Review, Pieces LTM, Jira, GitKraken, and Todoist) into a single unified LLM CoS Query Engine?

## Why It Matters

Without a unified protocol, open loops remain scattered across tools, requiring manual context switching and high executive function to aggregate. A unified engine is the core mechanism of prodOS to lower activation energy by presenting a single, deduplicated list of ADHD-optimised starter tasks.

## What I Currently Think

The proposed architecture (Gather → Synthesise → Generate → Push → Log) is sound. The primary unresolved tension is the implementation path: whether to build a custom script/plugin to orchestrate this sweep programmatically, or to rely purely on wiring existing MCP tools together via a single LLM prompt/skill (like the `work-review-launchpad` skill).

## What Would Settle It

A decision brief evaluating the "build vs. wire-existing" approaches, followed by the implementation of the chosen path and a successful test run that pulls from Jira/GitKraken/Pieces and pushes a starter task to Todoist.

## Sources
