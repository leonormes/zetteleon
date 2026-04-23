---
created: 2026-04-14T20:26:10+00:00
created_utc: "2026-04-14T13:20:00Z"
kind: mechanism
modified: 2026-04-22T16:15:21+00:00
source_title: "Archon and Extreme Harness Engineering"
source_url: "https://youtube.com/watch?v=qMnClynCAmM"
status: seed
tags: [archon, automation, devops, yaml]
title: Workflow-as-YAML
type: atom
upstream: "[[SoT - Agentic AI Design Patterns]]"
---

## Workflow-as-YAML

Software development processes can be codified as YAML files consisting of discrete nodes that represent AI prompts, deterministic bash commands, or human approval gates. This approach allows the Software Development Life Cycle (SDLC) to be version-controlled and executed as a structured graph of operations.

### Scope & Conditions

Used within frameworks like Archon to define the execution logic of agentic harnesses.

### Evidence

> "Development processes are defined using YAML files. These workflows consist of 'nodes,' which can be AI prompts, deterministic bash commands, or human-in-the-loop approval gates."

### Implications

- SDLC processes become version-controllable and subject to the same rigour as application code.
- Enables the seamless mixing of high-level LLM reasoning with deterministic code execution and local environment manipulation.

### Related

- [[Graph-Based Orchestration]]—direct concept match: YAML serves as the persistence format for the orchestration graph.
- [[CLI Interoperability for Agents]]—shared mechanism: YAML nodes often trigger the small, interoperable tools required for agent execution.

### See Also

- [[SoT - Generative Infrastructure Configuration Framework]]
