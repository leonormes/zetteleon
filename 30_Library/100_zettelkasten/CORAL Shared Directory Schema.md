---
created: 2026-04-10T12:00:00+00:00
modified: 2026-04-16T11:55:59+00:00
tags: [automation, coral, data-structure, knowledge-management]
title: CORAL Shared Directory Schema
---

## CORAL Shared Directory Schema

The shared persistent memory in the CORAL multi-agent framework is organised into three typed elements: Attempts (a ledger of every function evaluation, keyed by commit hash), Notes (markdown files in which agents record textual hypotheses about what is and is not working), and Skills (reusable executable code modules abstracted from successful localised runs). Together these three stores separate raw execution logs from qualitative reasoning from permanent capability assets.

### Scope & Conditions

Foundational data structure for agents running in parallel Git workspaces. The three-way split is specific to CORAL's research optimisation context; the underlying separation of concerns (logs vs. notes vs. reusable code) is a transferable principle.

### Evidence

> "This directory is categorised into three main elements: Attempts… Notes… Skills…" [04:10]

### Implications

- Separates raw execution traces (Attempts) from qualitative reasoning (Notes), preventing the two from polluting each other as agents iterate.
- Promotes successful localised logic into permanent, reusable assets (Skills), converting ephemeral experimentation into durable capability.

### Related

- [[Virtual File System for Agent Concurrency]]—shared mechanism: both model multi-agent shared state as a structured, typed filesystem abstraction; CORAL's three-element schema is a concrete domain-specific instantiation of the general virtual-filesystem coordination pattern.
- [[SoT - Agentic AI Design Patterns]]—extends: the three-element schema is a concrete implementation of the "Memory Management" pattern (short-term notes → long-term skills) within an agentic system.
