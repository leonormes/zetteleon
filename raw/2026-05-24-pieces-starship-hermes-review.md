---
title: Starship Tuning Completion & Hermes Config Self-Review (2026-05-24)
created: 2026-05-24T20:15:00+01:00
source: pieces-ltm
pieces_ids:
  - c0f950bd-e3a2-4754-a5cd-d88f543b76df
  - 765deb6b-7808-43d9-9741-507fabf8407e
  - 2b045ae4-4b49-4f85-a499-6e48f1c5e27c
  - ce8debb5-fe1a-4507-88fa-1cb38b368d16
  - 8bbed588-e456-49fe-905c-d4137ea9f152
  - 0f61f3fc-37a9-46c7-9053-7a25c761201c
  - 26fa2824-fe54-4147-a3cf-82cdba2957ac
  - c9977711-9381-44ed-bbaa-12bd86cda419
tags: [raw, pieces]
---

# Starship Tuning Completion & Hermes Config Self-Review (2026-05-24)

## Asset 1 (Pieces: c0f950bd-e3a2-4754-a5cd-d88f543b76df)

Captured at 20:11. Starship `/goal` prompt for grounded starship.toml fixing:

```
/goal

- Input: Use pieces LTM MCP to understand context
- Output: Apply specific, evidence-based changes to starship.toml
- Constraints:
  - Use `chezmoi diff` to verify changes
  - Wait for user approval before running `chezmoi apply`
  - Do not speculate — only apply changes with direct evidence from Pieces
- Working Dir: ~/.local/share/chezmoi/dot_config/
```

## Asset 2 (Pieces: 765deb6b-7808-43d9-9741-507fabf8407e)

Captured at 20:11. Unused TTS config audit prompt:

```
/goal

Read ~/.hermes/config.yaml. Identify ALL TTS-related configuration.
List every TTS provider, model, and setting.
Flag which are active vs dormant.
```

## Asset 3 (Pieces: 2b045ae4-4b49-4f85-a499-6e48f1c5e27c)

Captured at 20:10. Starship performance fix execution confirmation:

```
starship_perf_fixed successfully.

WORKFLOW: starship-perf-fix
TASK: Fix starship.toml performance issues
TIMESTAMP: 2026-05-24T20:05:00
STATUS: completed

Changes applied:
- command_timeout: 2000 -> 500
- kubernetes: disabled
- azure: directory-scoped
- aws: directory-scoped
- git_status: ignore_submodules: true
```

## Asset 4 (Pieces: ce8debb5-fe1a-4507-88fa-1cb38b368d16)

Captured at 20:10. Starship worker completion summary:

```
Starship Worker Summary

Summary: Starship Worker successfully fixed starship.toml.
The fix was applied and verified.
```

## Asset 5 (Pieces: 8bbed588-e456-49fe-905c-d4137ea9f152)

Captured at 15:09. Hermes Config Self-Review Prompt:

```
/goal

You are a Hermes workstation auditor. Review ~/.hermes/config.yaml.

TASK: Comprehensive self-review covering:
1. Provider configuration (active providers, model IDs, fallbacks)
2. Toolset audit (enabled vs actually used)
3. Memory configuration (active provider, honcho/edge cases)
4. Skill inventory (active skills, categories, unused)
5. TTS/STT configuration (active, dormant, conflicts)
6. MCP server configuration (active, transport types)
7. Personality and display settings
8. Cron job configuration

For each area:
- State current config
- Flag redundancy, conflict, or optimisation opportunity
- Priority: HIGH / MEDIUM / LOW
```

## Asset 6 (Pieces: 0f61f3fc-37a9-46c7-9053-7a25c761201c)

Captured at 13:34. Gemini prompt validation result for GitOps pipeline:

```
gemini:"prompt validation complete — four key metrics baseline established"
```

## Asset 7 (Pieces: 26fa2824-fe54-4147-a3cf-82cdba2957ac)

Captured at 13:33. Reading SOUL.md and mission prompt:

```
Read ~/.hermes/SOUL.md, ~/.hermes/mission.md
Understand workspace context before proceeding
```

## Asset 8 (Pieces: c9977711-9381-44ed-bbaa-12bd86cda419)

Captured at 13:33. Session context setup:

```
session_context = read(SOUL.md, mission.md, CLAUDE.md)
Working directory: ~/.hermes/hermes-agent
```
