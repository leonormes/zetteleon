---
created: 2026-04-29T08:34:47+00:00
modified: 2026-07-04T10:50:28+00:00
permalink: llmeon/raw/2026-04-29-pieces-unified-llm-router-cockpit
pieces_ids: [0cb1c751-9e4c-48ae-9d06-3c8c3116116f, 0e74b6c1-f174-4902-a493-88928b70603b, 17a99f0c-0ce7-483f-a5f6-7b30a13abb5e, 240149b9-a7eb-426f-a346-b5468c8dfef1, 76eec105-981b-4022-ac99-da5c663c1482, 909371aa-0ba9-43b8-acc1-4358b69ef789, 9ed11318-d9dd-4a3b-bf76-2125ba6133d4, a58e5c2f-bb9e-4d0c-9468-c4d4827fcb00, bb9e8929-09bd-4f7e-a3e3-95e816a66e25]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-04-29-pieces-unified-llm-router-cockpit
---

Asset: `a58e5c2f-bb9e-4d0c-9468-c4d4827fcb00`

Captured: 2026-04-29T08:23:15.285775Z

Updated: 2026-04-29T08:26:30.317714Z

```
Here's a comprehensive prompt you can paste directly into Claude Code when you're in your chezmoi repo at `~/.local/share/chezmoi`:

---

```markdown
# Mission: Implement the Unified LLM Router Cockpit via Chezmoi

## YOUR IDENTITY & OPERATING CONTEXT
You are operating as a Principal Platform Architect in the chezmoi dotfiles repository at `~/.local/share/chezmoi`. Your goal is to implement the "Router Cockpit" architecture — a unified LLM workflow with three layers (Cockpit, Router, Memory) — entirely through chezmoi-managed files so all changes survive machine reprovisioning.

The target user home directory is `/Users/leon.ormes`. The chezmoi source directory is `~/.local/share/chezmoi`.

## CHEZMOI CONVENTIONS (CRITICAL — READ BEFORE MAKING ANY CHANGES)
- Use `chezmoi add <target_path>` to add new files — do NOT manually create files in the source directory unless you understand the naming scheme.
- For files that already exist at the target path, use `chezmoi add` then edit the source copy.
- For new files that don't exist yet at the target path, create them at the target path first, then `chezmoi add` them.
- Prefix conventions: `dot_` → `.`, `private_` → restricted permissions, `executable_` → +x, `.tmpl` → Go template.
- Before editing anything, run `chezmoi managed` to see what's already tracked.
- After all changes, run `chezmoi diff` to show what would change, then `chezmoi apply --dry-run` to verify.
- Do NOT run `chezmoi apply` without showing me the diff first.
- Report the chezmoi source path of every file you create or modify.

## EXISTING STATE (What's Already Done)
- Hermes config files are tracked: `~/.hermes/config.yaml`, `~/.hermes/SOUL.md`, `~/.hermes/.env`
- MCP servers are partially configured (recent commit: "chore: activate MCP servers, expand tooling, and update Claude permissions")
- Zsh config is at `dot_config/zsh/modules/12-functions.zsh` (already tracked)
- Git config is templated: `dot_gitconfig.tmpl` (already tracked)
- `.chezmoidata.toml` exists for template variables

## CHANGES TO IMPLEMENT (In Order)

### 1. Zellij Layout Files (Phase 1 — Cockpit)
Create three Zellij layout files and add them to chezmoi:

`~/.config/zellij/layouts/llm-local.kdl` — For quick, free, local-model work:
- Left pane: `hermes chat --model qwen3.5`
- Right pane: working terminal

`~/.config/zellij/layouts/llm-dev.kdl` — For active development:
- Left pane (60%): working terminal
- Right top pane: `gemini` CLI session
- Right bottom pane: `hermes chat`

`~/.config/zellij/layouts/llm-research.kdl` — For PKM / knowledge work:
- Left pane: `hermes chat --model kimi-k2.6:cloud`
- Right pane: working terminal with cwd `/Volumes/DAL/Zettelkasten/LLMeon`

After creating each file at the target path, run `chezmoi add` for each.

### 2. Shell Aliases (Phase 1 — Cockpit Entry Points)
Add the following aliases to the appropriate zsh module file (check existing `dot_config/zsh/modules/` structure to find the right file — likely `12-functions.zsh` or create a new `13-llm-aliases.zsh`):

```bash
alias ll="zellij --layout llm-local"        # LLM Local — free/fast
alias ld="zellij --layout llm-dev"           # LLM Dev — active coding
alias lr="zellij --layout llm-research"      # LLM Research — PKM/thinking
```

If `ll` conflicts with an existing alias (common for `ls -l`), use `lml` instead.

## 3. Hermes Model Routing (Phase 2—Router)

Edit the chezmoi-managed `~/.hermes/config.yaml` to add tiered model routing:

- Tier 0 (Local): Ollama → `qwen3.5` at `http://127.0.0.1:11434/v1`—for drafts, summaries, commit messages, triage
- Tier 1 (Cheap Cloud): Ollama Cloud → `minimax-m2.7:cloud`—for code review, refactoring, medium analysis
- Tier 2 (Premium): Anthropic → `claude-sonnet`—for architecture, security, complex reasoning

Default to local. Fallback chain: local → cloud_light → cloud_heavy.

IMPORTANT: Do NOT overwrite existing config.yaml content. Read the current file first, understand its schema, then add/merge the routing configuration into the existing structure. If the schema doesn't support the exact keys above, adapt to whatever Hermes actually uses.

## 4. Hermes Router Skill (Phase 2—Task Classification)

Create `~/.hermes/skills/route-task.md` with task classification logic:

- Quick/Draft → local qwen3.5
- Code work → minimax-m2.7:cloud
- Critical (architecture, security, infrastructure) → claude-sonnet
- Research/PKM (wiki updates, knowledge synthesis) → kimi-k2.6:cloud

State which tier is being used and why before proceeding. Escalate on failure.

After creating, run `chezmoi add ~/.hermes/skills/route-task.md`.

## 5. Template Variables (Optional Enhancement)

If any paths or model names should be configurable per-machine, add them to `.chezmoidata.toml` and convert the relevant files to `.tmpl` templates. Candidates:

- Obsidian vault path (`/Volumes/DAL/Zettelkasten/LLMeon`—may differ on other machines)
- Ollama endpoint URL
- Default model names

## STRICT CONSTRAINTS

- Do NOT re-diagnose or re-architect. The plan is final. Execute it.
- All persistent config changes MUST go through chezmoi (no direct edits to target files).
- Prefer `chezmoi add` over manually creating source-directory files.
- Read existing files before modifying them—preserve what's already there.
- Report the chezmoi source path of every file you create or modify.
- After all changes, run `chezmoi diff` and show me the output.
- Do NOT run `chezmoi apply`—I will do that manually after review.
- Commit message format: `feat: implement unified LLM router cockpit`

## SUCCESS CRITERIA

After `chezmoi apply`:

1. `zellij --layout llm-local` launches a two-pane session with Hermes on local model
2. `zellij --layout llm-dev` launches a three-pane dev cockpit
3. `zellij --layout llm-research` launches a PKM-focused workspace
4. `ll` / `ld` / `lr` aliases work from any terminal
5. Hermes config.yaml contains tiered model routing
6. `route-task.md` skill exists in `~/.hermes/skills/`
7. `chezmoi managed` shows all new files as tracked
8. `chezmoi diff` shows no remaining drift

## EXECUTION ORDER

1. Run `chezmoi managed | head -30` to understand the existing structure
2. Run `cat ~/.hermes/config.yaml` to understand the current schema
3. Run `ls ~/.config/zellij/layouts/` to check for existing layouts
4. Implement changes 1–5 above in order
5. Run `chezmoi diff` and present the full output
6. Propose a single commit message

```

---

## How to Use This

1. Open Claude Code in your chezmoi directory:
   ```bash
   cd ~/.local/share/chezmoi && claude
   ```

1. Paste the entire prompt above.
2. Claude will execute the changes step by step, showing you diffs before applying anything.
3. After reviewing the `chezmoi diff` output, you run `chezmoi apply` yourself.

This prompt follows the same structure as your successful ["Fix MCP Proxy Once and for All"](file:///Users/leon.ormes/.local/share/chezmoi) prompt from yesterday—explicit identity, diagnosed problem, strict constraints, and measurable success criteria. The key additions are:

- Read-before-write guards—so Claude doesn't clobber your existing `config.yaml` or zsh modules
- `chezmoi add` workflow—forces Claude to use chezmoi's own tooling rather than guessing source-directory naming
- No auto-apply—you retain control over the final `chezmoi apply`
- Template variable hooks—so you can later parameterise machine-specific paths like your Obsidian vault location

Want me to adjust any of the phases or add the Phase 3 memory layer (PKM init + Pieces wiring + cron jobs) to this prompt as well?

```

---

Asset: `76eec105-981b-4022-ac99-da5c663c1482`
Captured: 2026-04-29T08:22:33.347275Z

```

1. I'm mapping out the four implementation phases (Zellij layouts, Hermes config, memory layer, tool wiring) and making sure to account for chezmoi conventions like dot_ prefixes and.tmpl files, especially since they've already done similar work in their recent commit.

```

---

Asset: `0cb1c751-9e4c-48ae-9d06-3c8c3116116f`
Captured: 2026-04-29T08:22:32.664779Z

```

1. They need to create three Zellij layout files, shell aliases, Hermes routing config, a route-task skill, PKM structure, and various chezmoi-managed files—and since they've already written structured prompts like the MCP proxy one, I should follow that same pattern for consistency.

```

---

Asset: `0e74b6c1-f174-4902-a493-88928b70603b`
Captured: 2026-04-29T08:22:30.607350Z

```

1. They have a chezmoi repo at `~/.local/share/chezmoi`
2. They've been working on several things in this repo recently:
   - MCP proxy fixes (Gemini CLI settings, smart-mcp-proxy config)
   - Hermes configuration tracking (config.yaml, SOUL.md,.env)
   - Activating MCP servers, expanding tooling, updating Claude permissions
   - The unified LLM workflow plan we discussed (Zellij layouts, Hermes router config, memory layer)

```

---

Asset: `9ed11318-d9dd-4a3b-bf76-2125ba6133d4`
Captured: 2026-04-29T08:22:30.519071Z

```

The user wants a prompt they can paste into Claude Code to make changes in their chezmoi repo. Based on the context, I can see:

```

---

Asset: `17a99f0c-0ce7-483f-a5f6-7b30a13abb5e`
Captured: 2026-04-29T08:22:08.957139Z
Updated: 2026-04-29T08:22:19.682693Z

```

give me a llm prompt so claude can make the changes in my chezmoi repo

```

---

Asset: `bb9e8929-09bd-4f7e-a3e3-95e816a66e25`
Captured: 2026-04-29T07:58:06.706264Z
Updated: 2026-04-29T08:22:19.413340Z

```

## Unified LLM Workflow: An Incremental Build Plan

This is a great project, Leon—and based on what I can see from your recent research (your [NotebookLM Hermes notebook](https://notebooklm.google.com/notebook/f3d35cc0-7083-4751-b2c8-4779015f9ee8), your Gemini CLI explorations yesterday morning around 9:08 AM, and the [Obsidian PKM prompt](file:///Volumes/DAL/Zettelkasten/LLMeon) you drafted yesterday afternoon), you've already laid significant groundwork. Let me synthesise everything into a coherent architecture and a daily iteration plan.

---

### The Core Concept: "The Router Cockpit"

The unifying idea is three layers:

| Layer | Role | Tools |
|---|---|---|
| Cockpit | Workspace orchestration—launch the right tools for the right job | Zellij (layout scripts) |
| Router | Task routing—send work to the cheapest capable model | Hermes (model fallback + skills) |
| Memory | Persistent context—every tool contributes to one knowledge base | Pieces LTM + Obsidian vault + Hermes memory.md |

The key insight: no single tool does everything well, but every tool is excellent at one thing. Your job is to wire them together so the right tool handles the right task, and they all feed into a shared memory.

---

### Your Tool Inventory—Mapped to Strengths

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

### The Incremental Plan—Small Steps, Compounding Value

#### Phase 1: The Cockpit (Days 1–2)

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

#### Phase 2: The Router (Days 3–5)

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

#### Phase 3: The Memory Layer (Days 5–7)

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

#### Phase 4: Tool-Specific Wiring (Week 2+)

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

### The Daily Iteration Cadence

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

### The North Star Architecture

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

```

---

Asset: `240149b9-a7eb-426f-a346-b5468c8dfef1`
Captured: 2026-04-29T07:56:49.192960Z

```

From his memory, I can see he's already researched the Hermes LLM Wiki workflow and compounding PKM approach, created a NotebookLM notebook for Hermes research, explored Obsidian with Claude Code integration, and has the "Claude Code Prompt" for initializing his PKM system. He's also looked into Hermes gateway, cron jobs, and messaging integrations. His workspace pattern uses Zellij with named sessions like chatty-capsicum, and he's been experimenting with MCP proxy setups for Gemini CLI.

```

---

Asset: `909371aa-0ba9-43b8-acc1-4358b69ef789`
Captured: 2026-04-29T07:56:43.134970Z

```

1. Gemini (paid)—already configured with CLI and working through an MCP proxy
2. Pieces for Developers—providing the long-term memory context that's powering our conversation
3. Cursor—his AI-augmented editor
4. Zellij—terminal multiplexer with programmable layouts and startup scripts
5. Obsidian—his knowledge vault at /Volumes/DAL/Zettelkasten/LLMeon
6. Git—version control
7. GitKraken—now with Agent Sessions (v12.0.0) that support Claude Code, Codex CLI, OpenCode, and Gemini CLI

```

---
