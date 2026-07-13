---
aliases: [Agent Capabilities, AI Agent Skills, Claude Code Skills]
created: 2026-03-28T17:00:00+00:00
modified: 2026-07-13T08:45:09+00:00
permalink: llmeon/30-library/so-t/so-t-ai-agent-skill-architecture
tags: [agents, ai, architecture, claude, mcp, skills]
title: SoT - AI Agent Skill Architecture
---

## Minimum Viable Understanding (MVU)

An AI Agent Skill is a set of modular instructions and resources that teach an agent how to handle specific workflows. Unlike MCP servers (which provide tools) or Subagents (which provide isolated execution), Skills focus on behavioral patterns and progressive disclosure. They allow an agent to maintain a lean context while having deep knowledge available on demand.

---

## Working Knowledge

### 1. Skill vs. MCP vs. Subagent

| Component | Analogy | Purpose |
|:---|:---|:---|
| MCP Server | The Kitchen (Tools) | Provides external capabilities (e.g., "Send a Slack message"). |
| Skill | The Recipe (Workflow) | Teaches the agent _how_ to use tools to achieve an outcome. |
| Subagent | The Sous-Chef (Execution) | Runs a task in a separate, independent context window. |

### 2. Progressive Disclosure Architecture

To maintain context efficiency, skills are fetched in stages:

1. Metadata (Name/Description): Always in the primary context (~100 tokens). Used by the LLM to decide whether to trigger the skill.
2. Body (`SKILL.md`): Loaded only when the skill is activated.
3. Resources (`scripts/`, `references/`): Loaded on-demand by the agent when specific steps are reached.

### 3. Implementation Patterns

#### Pattern A: Prompt-Only (Markdown)

The simplest form. Pure instructions in `SKILL.md`.

- Use Case: Brand guidelines, coding standards, commit message formatting.
- Benefit: No dependencies; zero execution overhead.

#### Pattern B: Prompt + Scripts (Deterministic)

Instructions that delegate logic to Python or Node.js scripts in the `scripts/` directory.

- Use Case: Data transformation, PDF/Excel processing, complex math.
- Benefit: Ensures reliability for tasks where LLMs are probabilistic (e.g., counting rows, parsing structured data).

#### Pattern C: Skill + MCP (Integrative)

Instructions that orchestrate calls to external MCP servers.

- Use Case: "Create Issue → Fix Code → Open PR" workflows.

---

## Current Understanding

### The "Triggering" Problem

An agent only activates a skill based on its description. Vague descriptions (e.g., "Helps with data") fail to trigger. Descriptions must be "pushy" and list specific trigger keywords or file patterns (e.g., "Trigger when user mentions profit margins or uploads.xlsx files").

### Distribution Patterns

- Local Project: `.claude/skills/` (shared with teammates via git).
- Manual Upload: ZIP upload to settings (must contain the folder itself at root).
- Skill Marketplace: Programmatic management for broader reach.

## Related Documentation

- [[Protocol - Action-First GTD (LLM Chief of Staff)]]
- [[SoT - Gemini CLI Operations & Workflow]]
- [[SoT - Flow Engineering]]—Pattern B is an instance of this broader orchestration discipline
- [[SoT - LLM Semantic-Statistical Mismatch]]—Why Pattern B (scripts for deterministic tasks) is necessary
