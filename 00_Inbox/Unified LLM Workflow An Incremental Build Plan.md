---
created: 2026-04-29T07:58:21+00:00
modified: 2026-04-29T08:01:30+00:00
title: Unified LLM Workflow An Incremental Build Plan
---

This is a great project, Leon—and based on what I can see from your recent research (your [NotebookLM Hermes notebook](https://notebooklm.google.com/notebook/f3d35cc0-7083-4751-b2c8-4779015f9ee8), your Gemini CLI explorations yesterday morning around 9:08 AM, and the [Obsidian PKM prompt](file:///Volumes/DAL/Zettelkasten/LLMeon) you drafted yesterday afternoon), you've already laid significant groundwork. Let me synthesise everything into a coherent architecture and a daily iteration plan.

---

## The Core Concept: "The Router Cockpit"

The unifying idea is three layers:

| Layer | Role | Tools |
|---|---|---|
| Cockpit | Workspace orchestration—launch the right tools for the right job | Zellij (layout scripts) |
| Router | Task routing—send work to the cheapest capable model | Hermes (model fallback + skills) |
| Memory | Persistent context—every tool contributes to one knowledge base | Pieces LTM + Obsidian vault + Hermes memory.md |

The key insight: no single tool does everything well, but every tool is excellent at one thing. Your job is to wire them together so the right tool handles the right task, and they all feed into a shared memory.

---

## Your Tool Inventory—Mapped to Strengths

| Tool | Best At | Cost | Use For |
|---|---|---|---|
| Ollama local (qwen3.5, gemma4) | Quick, private, zero-cost inference | Free | Drafts, summaries, commit messages, code review, triage |
| Ollama Cloud (minimax-m2.7, kimi-k2.6) | Mid-range tasks with good speed | Low | Medium-complexity code gen, refactoring, longer context work |
| Gemini CLI | Deep codebase reasoning, MCP integration | Moderate | Infrastructure work, Terraform, multi-file analysis |
| Claude (via Cursor + Claude Code) | Complex architecture, long-context reasoning, precision | Premium | Architecture decisions, security analysis, critical code, pen-test work |
| Hermes | Autonomous execution, skills, cron, self-improving memory | Depends on backing model | Orchestration, automation, PKM maintenance, scheduled tasks |
| Cursor | Interactive coding with inline AI | Premium | Active development sessions |
| Pieces LTM | Cross-app contextual memory | Subscription | The "sensory cortex"—captures what you see, hear, copy |
| GitKraken | Agent Sessions (v12.0.0—parallel agent workstreams) | Subscription | Spinning up isolated agent sessions per branch/task |

---

## The Incremental Plan—Small Steps, Compounding Value

### Phase 1: The Cockpit (Days 1–2)

Goal: Zellij becomes your single entry point for all LLM work.

Step 1—Create three Zellij layout files:

```kdl
// ~/.config/zellij/layouts/llm-local.kdl
// For quick, free, local-model work
layout {
    pane split_direction="vertical" {
        pane {
            command "hermes"
            args "chat" "--model" "qwen3.5"
        }
        pane {
            // Your working terminal
        }
    }
}
```

```kdl
// ~/.config/zellij/layouts/llm-dev.kdl
// For active development — Gemini CLI + working terminal
layout {
    pane split_direction="vertical" {
        pane size="60%" {
            // Your code/working terminal
        }
        pane size="40%" split_direction="horizontal" {
            pane {
                command "gemini"
                // Gemini CLI session
            }
            pane {
                command "hermes"
                args "chat"
            }
        }
    }
}
```

```kdl
// ~/.config/zellij/layouts/llm-research.kdl  
// For PKM / knowledge work — Hermes + Obsidian vault context
layout {
    pane split_direction="vertical" {
        pane {
            command "hermes"
            args "chat" "--model" "kimi-k2.6:cloud"
        }
        pane {
            cwd "/Volumes/DAL/Zettelkasten/LLMeon"
        }
    }
}
```

Step 2—Create shell aliases to launch them:

```bash
# ~/.zshrc or equivalent
alias ll="zellij --layout llm-local"        # "LLM Local" — free/fast
alias ld="zellij --layout llm-dev"           # "LLM Dev" — active coding
alias lr="zellij --layout llm-research"      # "LLM Research" — PKM/thinking
```

Why this matters: Instead of context-switching between terminals and remembering which tool to open, you type `ll`, `ld`, or `lr` and the right cockpit materialises. This is deterministic, not vibes.

---

### Phase 2: The Router (Days 3–5)

Goal: Hermes becomes your cost-aware model router.

Your Hermes config at `~/.hermes/config.yaml` (which you set up [yesterday morning around 9:08 AM](https://docs.ollama.com/integrations/hermes)) supports multi-provider fallback. Configure it in tiers:

Step 3—Configure tiered model routing in Hermes:

```yaml
# ~/.hermes/config.yaml — model routing strategy
models:
  # Tier 0: Local — free, fast, private
  local:
    provider: ollama
    endpoint: http://127.0.0.1:11434/v1
    model: qwen3.5
    use_for: [drafts, summaries, commit_messages, triage]
    
  # Tier 1: Cheap cloud — good enough for most tasks  
  cloud_light:
    provider: ollama_cloud
    model: minimax-m2.7:cloud
    use_for: [code_review, refactoring, medium_analysis]
    
  # Tier 2: Premium — when precision matters
  cloud_heavy:
    provider: anthropic
    model: claude-sonnet
    use_for: [architecture, security, complex_reasoning]

routing:
  default: local
  fallback_chain: [local, cloud_light, cloud_heavy]
```

> Note: The exact YAML schema depends on your Hermes version—check `hermes model` for the current config format. The principle is: default to local, escalate only when needed.

Step 4—Create a simple "router" skill for Hermes:

Hermes skills are stored in `~/.hermes/skills/`. Create one that encodes your routing logic:

```markdown
# ~/.hermes/skills/route-task.md
# Skill: Route Task

When I ask you to do something, first classify the task:
- Quick/Draft (summary, commit message, quick question) → Use local qwen3.5
- Code work (review, refactor, generate) → Use minimax-m2.7:cloud  
- Critical (architecture, security, infrastructure) → Use claude-sonnet
- Research/PKM (wiki updates, knowledge synthesis) → Use kimi-k2.6:cloud

State which tier you're using and why before proceeding.
If the local model fails or gives poor results, escalate to the next tier.
```

Why this matters: You control costs explicitly. Local models handle 60-70% of tasks at zero marginal cost. Premium models are reserved for work that demands them—like your FITFILE pen-test remediation or MESH API architecture.

---

### Phase 3: The Memory Layer (Days 5–7)

Goal: All tools feed into one persistent knowledge base.

You've already drafted the architecture for this—your [Claude Code PKM prompt](file:///Volumes/DAL/Zettelkasten/LLMeon) from yesterday at 3:41 PM outlines the three-layer `/raw → /wiki → /output` structure. Now wire the tools into it:

Step 5—Execute your existing PKM initialization prompt:

Run the Claude Code prompt you already wrote in your Obsidian vault to create the `/raw`, `/wiki`, `/output` directories and the `AGENTS.md` governance file.

Step 6—Wire Pieces LTM as the sensory input layer:

This is the critical integration. Pieces captures what you see, copy, and hear across all your tools. Hermes can query it:

```bash
# Verify the Pieces MCP integration works
hermes sync /Volumes/DAL/Zettelkasten/LLMeon/AGENTS.md
```

Then add a §7 Pre-Task Context Rule to your `AGENTS.md` (as you were researching [yesterday around 4:49 PM](https://gemini.google.com/app/994daf8341dca322)):

```markdown
## §7 Pre-Task Context Rule
Before starting any non-trivial task, query Pieces LTM for recent context 
related to the task domain. Include relevant snippets in the working context.
All synthesised notes must include Pieces ID backlinks for traceability.
```

Step 7—Set up your first Hermes cron job:

```bash
# Daily morning synthesis — pulls Pieces context into Obsidian
hermes cron add --schedule "0 8 * * *" --skill "daily-synthesis" \
  --instruction "Query Pieces LTM for yesterday's activity. Ingest highlights into /raw. Update any affected /wiki pages. Write a daily brief to /output/daily/$(date +%Y-%m-%d).md"
```

Then install the gateway so it runs autonomously:

```bash
hermes gateway install
```

---

### Phase 4: Tool-Specific Wiring (Week 2+)

Goal: Each tool has a clear lane and they share context.

Step 8—GitKraken Agent Sessions for branch-level work:

GitKraken 12.0.0 (which you were reviewing [yesterday at 9:18 AM](file:///)) now supports Agent Sessions—it creates worktrees, installs dependencies, and launches a coding agent per session. Use this for:

- One agent session per Jira ticket (e.g., FTFL-596)
- Each session can launch Claude Code, Gemini CLI, or another agent
- The session is isolated to a worktree, so agents can't interfere with each other

Step 9—Cursor for interactive, Claude for autonomous:

Establish a clear rule: Cursor is for hands-on-keyboard coding. Claude Code CLI is for autonomous multi-file tasks. Don't use both on the same files simultaneously.

Step 10—Gemini CLI for infrastructure work:

You were already exploring Gemini CLI with MCP proxy integration yesterday. Once the MCP proxy auth issues are resolved, Gemini CLI becomes your go-to for:

- Terraform plans and reviews
- Multi-file infrastructure analysis
- Jira ticket context (via MCP → Jira integration)

---

## The Daily Iteration Cadence

| Day | Do This | Time |
|---|---|---|
| Today | Create the three Zellij layout files and aliases. Test `ll`, `ld`, `lr`. | 30 min |
| Tomorrow | Configure Hermes model routing in `config.yaml`. Test fallback chain. | 30 min |
| Day 3 | Create the `route-task.md` skill. Run 5 real tasks through the router. | 30 min |
| Day 4 | Execute the PKM init prompt in Obsidian. Verify `/raw`, `/wiki`, `/output`. | 30 min |
| Day 5 | Wire the first Hermes cron job. Install the gateway. Test manual run. | 30 min |
| Day 6 | Test Pieces → Hermes → Obsidian pipeline end-to-end. Fix any gaps. | 45 min |
| Day 7 | Review what worked. Adjust the routing tiers based on actual usage. | 30 min |

---

## The North Star Architecture

Once the phases are complete, your workflow looks like this:

```
┌─────────────────────────────────────────────────────────┐
│                    ZELLIJ COCKPIT                        │
│  ll (local)  │  ld (dev)  │  lr (research)              │
└──────┬───────┴─────┬──────┴──────┬──────────────────────┘
       │             │             │
       ▼             ▼             ▼
┌─────────────────────────────────────────────────────────┐
│                   HERMES ROUTER                          │
│  Tier 0: Ollama Local  →  Tier 1: Ollama Cloud          │
│  Tier 2: Claude/Gemini  →  Skills + Cron + Gateway      │
└──────┬───────┬──────┬───────────────────────────────────┘
       │       │      │
       ▼       ▼      ▼
┌──────────┐ ┌──────────┐ ┌──────────────┐
│ Cursor   │ │ Gemini   │ │ GitKraken    │
│ (editor) │ │ CLI      │ │ Agent Sess.  │
└────┬─────┘ └────┬─────┘ └──────┬───────┘
     │             │              │
     ▼             ▼              ▼
┌─────────────────────────────────────────────────────────┐
│                  MEMORY LAYER                            │
│  Pieces LTM (capture) → Hermes memory.md (synthesis)    │
│  Obsidian /raw → /wiki → /output (knowledge)            │
└─────────────────────────────────────────────────────────┘
```

The principle: Structure is truth. Every tool has one job. Every output feeds the memory layer. Every task starts with context and ends with a trace. No vibes—just deterministic routing with explicit escalation.

Start with the Zellij layouts today. That's your cockpit. Everything else plugs into it. Want me to flesh out any specific phase in more detail?
