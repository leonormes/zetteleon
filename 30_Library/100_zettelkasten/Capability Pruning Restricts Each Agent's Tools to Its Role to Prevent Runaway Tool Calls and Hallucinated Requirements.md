---
conformant: true
contradicts: []
created: 2026-09-14T15:32:01+00:00
created_utc: '2026-09-14T00:00:00Z'
epistemic_status: medium
evidence_links: []
modified: 2026-09-19T15:44:32+00:00
permalink: llmeon/30-library/100-zettelkasten/capability-pruning-restricts-each-agents-tools-to-its-role-to-prevent-runaway-tool-calls-and-hallucinated-requirements
prodos.kind: atomic
prodos.lifecycle: seed
proposition: "Deliberately restricting each specialised agent's available tools and skills to only what its role requires reduces token consumption and prevents agents from hallucinating requirements for capabilities they don't actually have, and getting caught in expensive, endless tool-call loops."
source_title: Shared Memory Layer for Agentic AI
source_url: unknown — see [[tmp_atoms_shared-memory-agentic-ai]]
status: seed
tags: [domain/llm, domain/pkm, topic/agent-architecture, topic/agentic-autonomy]
title: "Capability Pruning Restricts Each Agent's Tools to Its Role to Prevent Runaway Tool Calls and Hallucinated Requirements"
type: claim
upstream: '[[tmp_atoms_shared-memory-agentic-ai]]'
---

## Capability Pruning Restricts Each Agent's Tools to Its Role to Prevent Runaway Tool Calls and Hallucinated Requirements

Deliberately restricting each specialised agent's available tools and skills to only what its role requires—e.g. a Researcher agent has no task-delegation or cron access, an Orchestrator has no web-browsing tool—reduces token consumption and prevents agents from hallucinating requirements for capabilities they don't actually have or need, and getting caught in expensive, endless tool-call loops.

### Scope & Conditions

A multi-agent design practice, distinct from simply giving every agent full tool access "in case it's needed"—the restriction is itself the safety and efficiency mechanism.

### Evidence

> "A critical best practice for multi-agent setups is tightly restricting the tools and skills each bot can access… Disabling these prevents agents from hallucinating requirements and getting caught in expensive, endless loops."

### Implications

- When an agent starts making unexpected or repeated tool calls, checking whether its toolset is over-provisioned for its actual role is a cheap first diagnostic step.

### Related

- [[Full-Autonomy Agent Execution Requires Sandboxing for Safety and Data Privacy, Not Just Concurrency]]—shared mechanism: both restrict what an autonomous agent can do as the primary safety lever, rather than trusting behaviour alone.
- [[SoT - Agentic AI Design Patterns]]—extends: a specific role-scoping discipline that complements that SoT's routing pattern.
