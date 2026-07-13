---
created: 2026-04-14T20:27:29+00:00
created_utc: '2026-04-14T13:20:00Z'
kind: claim
modified: 2026-07-13T08:52:30+00:00
permalink: llmeon/30-library/100-zettelkasten/prompt-injected-non-functional-requirements
source_title: Archon and Extreme Harness Engineering
source_url: https://youtube.com/watch?v=qMnClynCAmM
status: seed
tags: [architecture, engineering-standards, observability, security]
title: Prompt-Injected Non-Functional Requirements
type: atom
upstream: '[[SoT - Agentic AI Design Patterns]]'
---

## Prompt-Injected Non-Functional Requirements

Reliability, observability, and security requirements can be durably encoded into agent operating procedures through high-level prompt instructions rather than manual, per-case implementation. This approach ensures that architectural standards—such as mandatory timeouts or logging—are consistently applied by the agents across the entire codebase.

### Scope & Conditions

Requires an agentic harness that consistently applies these global, prompt-level instructions to all agent actions.

### Evidence

> "Reliability, observability, and security are 'prompt-injected' into the agents. For example, a single instruction to 'require timeouts on all network calls' is durably encoded."

### Implications

- Ensures the uniform application of complex engineering standards across large or rapidly evolving codebases.
- Significantly reduces human error in enforcing essential architectural constraints and non-functional requirements.

### Related

- [[Closed Type Definitions]]—shared mechanism: both use high-level constraints to prevent architectural drift.
- [[SoT - AI Agent Skill Architecture]]—supports: by defining how these requirements are stored and applied.

### See Also

- [[Harness Engineering]]
