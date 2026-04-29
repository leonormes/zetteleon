---
created: 2026-04-29T08:26:02+00:00
Here's a comprehensive prompt you can paste directly into Claude Code when you're in your chezmoi repo at `~/.local/share/chezmoi`:
modified: 2026-04-29T08:29:41+00:00
title: Implement the Unified LLM Router Cockpit via Chezmoi
---

## YOUR IDENTITY & OPERATING CONTEXT

You are operating as a Principal Platform Architect in the chezmoi dotfiles repository at `~/.local/share/chezmoi`. Your goal is to implement the "Router Cockpit" architecture—a unified LLM workflow with three layers (Cockpit, Router, Memory)—entirely through chezmoi-managed files so all changes survive machine reprovisioning.

The target user home directory is `/Users/leon.ormes`. The chezmoi source directory is `~/.local/share/chezmoi`.

## CHEZMOI CONVENTIONS (CRITICAL—READ BEFORE MAKING ANY CHANGES)

- Use `chezmoi add <target_path>` to add new files—do NOT manually create files in the source directory unless you understand the naming scheme.
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

### 1. Zellij Layout Files (Phase 1—Cockpit)

Create three Zellij layout files and add them to chezmoi:

`~/.config/zellij/layouts/llm-local.kdl`—For quick, free, local-model work:

- Left pane: `hermes chat --model qwen3.5`
- Right pane: working terminal

`~/.config/zellij/layouts/llm-dev.kdl`—For active development:

- Left pane (60%): working terminal
- Right top pane: `gemini` CLI session
- Right bottom pane: `hermes chat`

`~/.config/zellij/layouts/llm-research.kdl`—For PKM / knowledge work:

- Left pane: `hermes chat --model kimi-k2.6:cloud`
- Right pane: working terminal with cwd `/Volumes/DAL/Zettelkasten/LLMeon`

After creating each file at the target path, run `chezmoi add` for each.

### 2. Shell Aliases (Phase 1—Cockpit Entry Points)

Add the following aliases to the appropriate zsh module file (check existing `dot_config/zsh/modules/` structure to find the right file—likely `12-functions.zsh` or create a new `13-llm-aliases.zsh`):

```bash
alias ll="zellij --layout llm-local"        # LLM Local — free/fast
alias ld="zellij --layout llm-dev"           # LLM Dev — active coding
alias lr="zellij --layout llm-research"      # LLM Research — PKM/thinking
```

If `ll` conflicts with an existing alias (common for `ls -l`), use `lml` instead.

### 3. Hermes Model Routing (Phase 2—Router)

Edit the chezmoi-managed `~/.hermes/config.yaml` to add tiered model routing:

- Tier 0 (Local): Ollama → `qwen3.5` at `http://127.0.0.1:11434/v1`—for drafts, summaries, commit messages, triage
- Tier 1 (Cheap Cloud): Ollama Cloud → `minimax-m2.7:cloud`—for code review, refactoring, medium analysis
- Tier 2 (Premium): Anthropic → `claude-sonnet`—for architecture, security, complex reasoning

Default to local. Fallback chain: local → cloud_light → cloud_heavy.

IMPORTANT: Do NOT overwrite existing config.yaml content. Read the current file first, understand its schema, then add/merge the routing configuration into the existing structure. If the schema doesn't support the exact keys above, adapt to whatever Hermes actually uses.

### 4. Hermes Router Skill (Phase 2—Task Classification)

Create `~/.hermes/skills/route-task.md` with task classification logic:

- Quick/Draft → local qwen3.5
- Code work → minimax-m2.7:cloud
- Critical (architecture, security, infrastructure) → claude-sonnet
- Research/PKM (wiki updates, knowledge synthesis) → kimi-k2.6:cloud

State which tier is being used and why before proceeding. Escalate on failure.

After creating, run `chezmoi add ~/.hermes/skills/route-task.md`.

### 5. Template Variables (Optional Enhancement)

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
