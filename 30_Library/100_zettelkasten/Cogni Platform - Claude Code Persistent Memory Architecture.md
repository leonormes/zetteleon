---
conformant: true
created: 2026-07-28T00:00:00+00:00
epistemic_status: medium
modified: 2026-08-13T10:54:44+00:00
permalink: llmeon/30-library/100-zettelkasten/cogni-platform-claude-code-persistent-memory-architecture
prodos.kind: atomic
prodos.lifecycle: stable
proposition: Cogni is a platform that adds persistent memory layers to Claude Code,
  enabling agents to retain discoveries and architectural context across isolated
  sessions via knowledge graphs with two-way memory writes and selective retrieval.
tags: [domain/llm, product/cogni, topic/agent-architecture, topic/persistent-memory, topic/tools]
title: Cogni Platform - Claude Code Persistent Memory Architecture
type: claim
---

## Cogni Platform - Claude Code Persistent Memory Architecture

Cogni is a wrapper around Claude Code that solves the session-isolation problem by adding a persistent memory layer. Rather than each Claude Code invocation starting from scratch, Cogni maintains a knowledge graph of prior discoveries, architectural decisions, and learned patterns.

### Core Features

1. Multi-session memory: Survives across Claude Code invocations
2. Bidirectional writes: Sessions can record new discoveries into the knowledge graph
3. Selective retrieval: Agents query the memory for task-relevant context, not full history
4. Knowledge graph structure: Information is indexed for fast, semantic retrieval

### How It Solves Claude Code's Constraint

- Before (Claude Code alone): Each session reloads codebase context → wasteful token use → slow startup → architectural amnesia
- After (Cogni): Sessions retrieve cached architectural summaries and prior patterns → selective context → fast startup → compounding knowledge

### Scope & Conditions

Platform-specific implementation. The architectural patterns Cogni uses (layered memory, selective retrieval, bidirectional writes) are general; Cogni is one instantiation.

### Related

- [[Claude Code Session Isolation Forces Context Reloading Across Invocations]]—solves: directly addresses this constraint.
- [[Persistent Memory Layers Enable Multi-Session Agent Continuity]]—implements: Cogni is a concrete implementation of this pattern.
- [[Agent Feedback Loops Require Bidirectional Memory Writes]]—implements: Cogni's bidirectional write capability.
- [[Selective Memory Retrieval Reduces Token Cost in Multi-Session Workflows]]—implements: Cogni's selective retrieval mechanism.
- [[Layered Knowledge Architecture]]—implements: Cogni follows the three-layer pattern (raw sources, synthesized wiki, schema).

### See Also

- Video source: "Turning Claude Fable 5 Into The Ultimate Second Brain!" by WorldofAI

%%[implements:: [[Persistent Memory Layers Enable Multi-Session Agent Continuity]]]%%

%%[implements:: [[Agent Feedback Loops Require Bidirectional Memory Writes]]]%%

%%[implements:: [[Selective Memory Retrieval Reduces Token Cost in Multi-Session Workflows]]]%%
