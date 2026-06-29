---
tags:
- hermes
- solution
- configuration
- model-routing
- openrouter
source: claude-sonnet-4-6; OWL (link remediation)
date: 2026-05-30
modified: 2026-05-30
permalink: llmeon/wiki/2026-05-30-hermes-model-routing
---

# Hermes Model Routing — Cost-Aware Multi-Model Setup

## Problem

Hermes was using `openrouter/owl-alpha` for every session type — PKM synthesis, coding, infra debugging, and reasoning all ran on the same free model. When instructing it to "use Claude", the SOUL.md hard rule forced it to invoke `claude --print` as a CLI subprocess instead of routing via the OpenRouter API.

## Root Causes

1. `providers.openrouter.models` only listed `openrouter/owl-alpha` — other models weren't registered as available.
2. `pkm.yaml` explicitly set `model.default: openrouter/owl-alpha` — PKM sessions never escalated.
3. SOUL.md contained a hard rule: *"never configure Claude as an API provider"* — written before OpenRouter credits were added, now incorrectly blocking API routing.
4. No `coding` profile existed.
5. SOUL.md Tier 0 label still said "qwen3.5 via Ollama" (stale, never updated after switching to owl-alpha).

## Solution

### Files changed

| File | Change |
|---|---|
| `private_dot_hermes/private_config.yaml` | Expanded `providers.openrouter.models` to include `anthropic/claude-sonnet-4-6`, `deepseek/deepseek-v4-flash`, `google/gemini-3-flash`. Updated model roles comment block. Added `/model-status` quick command. |
| `private_dot_hermes/profiles/pkm.yaml` | Changed `model.default` from `openrouter/owl-alpha` → `anthropic/claude-sonnet-4-6`. |
| `private_dot_hermes/profiles/coding.yaml` | **New profile.** Claude Sonnet via OpenRouter, `reasoning_effort: high`, 30-turn limit, preloads `code-delegate` + `route-task`. |
| `private_dot_hermes/SOUL.md` | Fixed Tier 0 label. Replaced hard rule with API vs CLI distinction block. Rewrote routing decision tree to include PKM branch and model selection table. Updated Tier 1.5 description to clarify owl-alpha is for gather/mechanical, not PKM synthesis. |
| `dot_hermes_custom_skills/custom/route-task/SKILL.md` | Added model routing table. Added `[ROUTING]` log block requirement. Added "Use Claude" disambiguation. Updated pre-flight checklist to include task classification + model match announcement. |

### Model routing map

| Session type | Command | Model |
|---|---|---|
| General / gather / mechanical | `hermes` | `openrouter/owl-alpha` (free, default) |
| PKM / Obsidian / synthesis | `hermes -p pkm` | `anthropic/claude-sonnet-4-6` |
| Coding / refactoring | `hermes -p coding` | `anthropic/claude-sonnet-4-6` |
| Infra / ops | `hermes -p infra` or `-p ops` | `openrouter/owl-alpha` |
| Bounded reasoning sub-task | `delegate_task` | `anthropic/claude-sonnet-4-6` |

### Key distinction fixed

> **Claude via OpenRouter API** = valid, uses OR credits, select via profile or `/model anthropic/claude-sonnet-4-6`  
> **Claude via CLI** = `claude --print`, uses subscription, only for autonomous codebase traversal

## Architecture Note

`~/.hermes/profiles/` is in `.chezmoiignore.tmpl` — profiles are git-tracked in the chezmoi source (`private_dot_hermes/profiles/`) but NOT auto-applied by `chezmoi apply`. Profile changes must be manually copied to `~/.hermes/profiles/` after editing the source.

## Verification

```bash
# Check pkm profile uses Claude Sonnet
grep "default:" ~/.hermes/profiles/pkm.yaml
# → anthropic/claude-sonnet-4-6

# Check coding profile exists
cat ~/.hermes/profiles/coding.yaml

# Start a PKM session and verify model at top of response
hermes -p pkm
/model-status
```

## Related

- [[wiki/projects/Hermes-Multi-Model-Routing-Strategy]] _Parent project dossier tracking the broader Hermes multi-model orchestration strategy, including Claude Code CLI timeout debugging and OpenRouter affordability analysis._
- [[wiki/projects/Hermes-Model-Configuration]] _Sibling dossier covering Hermes model configurationdebug, model error investigation, and OpenRouter provider setup — the immediate predecessor problem space that motivated this routing fix._
- [[2026-05-29-chezmoi-dotfiles-audit]] _Structural sibling: the chezmoi dotfiles audit references the same `private_config.yaml` substrate and goal_judge model mismatch that this routing fix resolved._