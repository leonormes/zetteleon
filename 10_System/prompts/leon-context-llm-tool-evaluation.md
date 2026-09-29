---
aliases: []
created: 2026-09-29T00:00:00+00:00
description: "Leon's actual LLM stack, model-routing tiers, and cost/flow goals — inject before evaluating any new AI tool, framework, or technique clip so the verdict is grounded against what's already running, not a generic take."
modified: 2026-09-29T07:56:45+00:00
permalink: llmeon/10-system/prompts/leon-context-llm-tool-evaluation
tags: [domain/llm-tooling, system/prompt, type/context]
title: leon-context-llm-tool-evaluation
type: prompt
---

## Context: Evaluating a New LLM Tool/Technique

### What's Actually Running

- Agent: Nous Research's Hermes Agent (`~/.hermes/`, chezmoi-managed at `private_dot_hermes/`), not a bespoke build—config, profiles, skills, and terminology (toolsets, `delegate_task`, `hermes-launch`) all come from that product.
- Orchestration doc: `SOUL.md` defines the "Mechanical Lead" persona and Prime Directive: resolve locally first, escalate to paid cloud CLIs only when complexity demands it.
- Routing skill: `route-task` (preloaded) enforces a Bucket 1 (mechanical, free tier, direct) vs Bucket 2 (reasoning, gather-then-`delegate_task`) split before any tool call—any new tool has to fit this classification, not bypass it.
- Integration hub: 1MCP (`http://127.0.0.1:3050/mcp`) aggregates Jira/Confluence, Obsidian, Todoist, GitKraken, 1Password, memory, semble/serena/ast-grep code-intelligence. A new tool that duplicates something 1MCP already fronts is redundant by default—check `~/.config/1mcp/mcp.json` first.
- PKM substrate: Obsidian vault `/Volumes/DAL/Zettelkasten/LLMeon` (PRODOS) + Basic Memory MCP for semantic recall (projects `llmeon` curated, `hermes-memory` raw). Both are markdown/embedding-shaped, not SQL/OLAP.

### Model Tiers (Cost hierarchy—cheapest First)

| Tier | Model | Provider | When |
|---|---|---|---|
| Free default | `openrouter/owl-alpha` | OpenRouter | Bucket 1 mechanical work, 1M context, DEFAULT for most profiles |
| Local/cloud-hybrid | `qwen3.5:cloud` | `ollama-launch` | `thin`/`jira`/`research` profiles—lightweight, low-tool-access sessions |
| Cheap aux | `deepseek/deepseek-v4-flash`, `google/gemini-3-flash` | OpenRouter | Classification, titling, approval checks, skills-hub—never the main loop |
| Reasoning | `anthropic/claude-sonnet-4-6` | OpenRouter (not Anthropic direct—avoids double-billing against the separate Claude subscription) | `pkm`/`coding` profiles, `delegate_task` sub-agents |
| Premium CLI | Claude Code, other Tier 1A-1D CLIs | Separate subscriptions | Autonomous codebase traversal only—explicitly the most expensive, last-resort tier |

Fallback chain is already configured per-profile (`fallback_providers`), so "add a fallback model" is not itself a novel pitch.

### The Two Goals, Made Concrete

- Reduce cost = keep more work on the free/cheap tiers without losing capability, or cut spend on a tier already in heavy use. Note: `display.show_cost: false` and `dashboard.show_token_analytics: false` are currently OFF—there's no active spend visibility today. A tool that adds real cost observability (not just another dashboard skin) is a genuine gap, not a nice-to-have.
- Improve flow = reduce context-switching, manual routing decisions, or Maintenance Load (PRODOS Axiom 3: <10%)—not "more features." A tool that adds config surface without removing an existing manual step is a flow cost, not a flow win.

### Standing Bottleneck (The One Thing Worth Solving)

Named in Hermes mission context: the Memory Bridge—context retrieval speed/accuracy across sessions. If a tool doesn't touch recall latency/accuracy, cost, or maintenance load, it's probably not worth adopting regardless of how interesting it is.

### Known Rough Edges (Fair Game to Solve)

- `ollama-launch` provider profiles exist but the Ollama daemon isn't reliably running—verify before crediting any Ollama-dependent tool with "already covered."
- No cost/token observability turned on anywhere in the stack.
- Multiple partially-overlapping memory layers (Obsidian vault, Basic Memory, Hermes `memory` toolset, `curator` auto-consolidation)—a new memory tool needs to name which layer it replaces, not add a fifth.

### Evaluation Filter (Apply before Recommending Anything)

1. Redundancy check—does 1MCP, `route-task`, an existing profile, or an existing skill already do this? If yes, the value is zero unless it's strictly better on cost or maintenance.
2. PRODOS axioms as veto power—Utility over Truth, Throughput over Storage ("system is for compute, not a database"), Low Maintenance (<10%), Context is Scarcity, 70% Rule. A tool that fails any of these needs an explicit justification, not a pass.
3. Single-user, single-machine reality—no multi-writer/team-collaboration need exists today. Server/platform tools pitched on concurrency or team-scale are solving a problem Leon doesn't have.
4. Local-first constraint—cloud API calls are a cost, not a default. A tool that moves work from free/local to paid/cloud needs to earn that with a capability gain, not just convenience.
5. Where it plugs in—name the specific config file/profile it would touch (`private_config.yaml`, a `profiles/*.yaml`, `mcp.json`, a skill under `dot_hermes_custom_skills`), not a vague "you could use this for X."

### Expected Output Shape when Evaluating a Clip

Verdict first (adopt / reference-only / skip), then: what it replaces or duplicates, which cost tier it affects, which config it would touch, and whether the named bottleneck (Memory Bridge / cost visibility / maintenance load) is actually what it solves.
