---
created: 2026-04-14T11:22:35+00:00
created_utc: "2026-04-14T11:05:00Z"
kind: heuristic
modified: 2026-04-19T20:11:47+00:00
source_title: "Martin Fowler & Kent Beck: Frameworks for reinventing software, again and again"
source_url: "http://www.youtube.com/watch?v=CZs8J1ZD0CE"
status: seed
tags: [ai-agents, architecture, maintainability, modularisation]
title: Modularisation for Agents
type: atom
upstream: "[[MOC - Software Architecture Principles]]"
---

## Modularisation for Agents

Small, well-defined modules are as beneficial for AI agent consumption as they are for human maintainability. Clean, decoupled architecture facilitates better context management for LLMs, reducing the cognitive complexity agents must navigate simultaneously.

### Scope & Conditions

Architectural requirement for effectively integrating AI agents into a professional codebase.

### Evidence

> "Modularisation for Agents: Small, well-defined modules are as beneficial for AI agents as they are for human maintainers."

### Implications

- Traditional "clean code" principles (SRP, decoupling) are now functional requirements for AI-agent compatibility.
- Highly coupled codebases create an "agent context trap" that hinders automated reasoning.

### Related

- [[SoT - LLM Reasoning Obeys the Complexity Conservation Law]]—shared mechanism: modularisation reduces the "procedural entropy" the agent must process.
- [[MOC - AI Software Engineering]]—shared mechanism: describes the architectural requirements for the "cognitive bridge."

### See Also

- [[SoT - Test-Driven Development]]
