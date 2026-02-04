---
aliases: [AI Agent Roles, Multi-Agent Architecture, The Surgical Team]
created: 2026-01-30T12:00:00+00:00
modified: 2026-02-01T15:08:02+00:00
tags: [agents, architecture, context-engine, roles]
title: SoT - Agentic Roles
---

## The Surgical Team (Agentic Roles)

To execute [[SoT - Macro-Micro Unification]], we divide the cognitive load across specialized agent roles. No single agent can hold the entire context; therefore, we rely on a Role-Based Architecture.

### The Core Team

| Role | Mental Model | Responsibility | Tools |
|:--- |:--- |:--- |:--- |
| The Architect | General Relativity | Guardian of the Macro. Defines constraints, boundaries, and interfaces. Enforces [[The Architectural Guardian]]. | `write_file` (Specs), `grep` (Boundaries) |
| The Scout | The Territory | Mapping the codebase. Generating [[SoT - Structural Intelligence|RepoMaps]]. Providing the "Skeleton" to the Architect. | `tree-sitter`, `ls -R`, `find` |
| The Cartographer | The Graph | Pruning the Control Flow Graph. Calculating [[SoT - Temporal Projection|Blast Radius]]. Injecting only the "Relevant Subgraph". | `ast-grep`, `lsp-query` |
| The Historian | The Timeline | Analyzing Churn and Volatility. "Who touched this last?" "Is this code calcified?" | `git log`, `git blame` |
| The Coder | Quantum Mechanics | The implementation engine. Writes the actual syntax within the constraints defined by the Architect. | `write_file` (Code) |

### The Workflow (The Pipeline)

1. Ingest: The Scout maps the territory.
2. Plan: The Architect defines the interface and constraints.
3. Prune: The Cartographer injects the specific subgraph needed for the task.
4. Execute: The Coder implements the function.
5. Verify: The Architect reviews the output against the constraints.

---

See Also: [[SoT - The Context Engine]], [[SoT - Macro-Micro Unification]]
