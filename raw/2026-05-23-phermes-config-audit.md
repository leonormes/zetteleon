---
created: 2026-05-23 11:38:34+00:00
modified: 2026-05-26 11:43:32+00:00
pieces_ids:
- c0418ed9-8a4a-4091-9d41-3ff994acbdc2
- d8d6bdcc-bbd2-400f-ae0b-ef936b251e4c
- ff8ec9bd-41bd-4497-86de-a374967ef2e9
source: pieces-ltm
tags:
- pieces
- raw
title: 2026-05-23-phermes-config-audit
permalink: llmeon/raw/2026-05-23-phermes-config-audit
---

## Hermes Config YAML—Production-Ready Audit & Optimisation

Analysis session of `~/.hermes/config.yaml` (12,397 bytes). User requested identification of redundancies, conflicts, and optimisations based on recent DevOps work with Kubernetes and Azure.

### Asset 1 (Pieces: c0418ed9-8a4a-4091-9d41-3ff994acbdc2)

User query: "Analyze my current ~/.hermes/config.yaml and the history of my recent configuration changes stored in my snippets and workflow activity. Identify: Redundancies, Conflicts, Optimizations (based on K8s/Azure DevOps work), and produce an Invisible Architecture instruction set for the Hermes /goal command for production-ready workstation state."

### Asset 2 (Pieces: d8d6bdcc-bbd2-400f-ae0b-ef936b251e4c)

Intermediate analysis confirming `~/.hermes/config.yaml` structure (12,397 bytes). Top-level sections confirmed: model, providers, fallback_providers, credential_pool_strategies, toolsets, agent, terminal, web, browser, checkpoints, file_read_max_chars, tool_output, tool_loop_guardrails, compression, prompt_caching, openrouter, bedrock, auxiliary (with sub-slots: vision, web_extract, compression, skills_hub, approval, mcp, title_generation, triage_specifier, kanban_decomposer, profile_describer, curator, session_search, goal_judge), display, dashboard, privacy, tts (edge, elevenlabs, openai, xai, mistral, neutts, piper), stt, voice, human_delay, context, memory, delegation, prefill_messages_file, goals, skills, curator, honcho, timezone, slack, discord, whatsapp, telegram.

### Asset 3 (Pieces: ff8ec9bd-41bd-4497-86de-a374967ef2e9)

Complete audit output:

#### Config Summary

- Model: `default: openrouter/owl-alpha`, `provider: openrouter`, `context_length: 128000`
- Providers: Single entry `openrouter` with `openrouter/owl-alpha` only
- Toolsets: `hermes-cli`, `terminal`, `file`, `hermes-homeassistant`
- Terminal: `backend: local`
- Memory: `provider: ''` (empty), `memory_enabled: true`, `memory_char_limit: 2200`
- Honcho: `{}` empty, not configured
- Auxiliary: web_extract, compression, title_generation, approval, session_search, goal_judge on `openrouter` + `google/gemini-3-flash`; vision, skills_hub, mcp, triage_specifier, kanban_decomposer, profile_describer, curator all `provider: auto`
- MCP servers: `mcp-proxy` (HTTP SSE at 127.0.0.1:8000) + `graphify` (stdio)
- Agent personalities: `concise` + `technical` defined; `display.personality: technical`
- Slack + Discord both configured
- TTS: Six providers (edge, elevenlabs, openai, xai, mistral, neutts, piper)
- STT: local (Whisper base), openai, mistral
- Delegation: `max_iterations: 50`, `max_concurrent_children: 3`
- Fallback providers: `[]` (none)

#### Redundancies Found

1. Single-model providers block with zero failover (no second provider enrolled despite 35+ being available during setup)
2. Six TTS providers configured, only edge active (`auto_tts: false`, voice killed at session start)
3. Three STT backends, only local whisper active
4. Dual personalities (concise + technical) with no activation; `display.personality: technical` makes concise unused

#### Conflicts Found

1. Built-in memory vs Honcho—`memory.provider: ''` but `honcho: {}` exists empty; previous honcho setup (May 18, `dialectic_cadence: 2`) was reverted by chezmoi apply
2. MCP transport mismatch: mcp-proxy uses HTTP SSE, graphify uses stdio; SSE transport was previously unreliable
3. `hermes-homeassistant` in toolsets but zero HA interactions in 30 days
4. Slack + Discord both configured but user's workflow is 100% terminal + Teams

#### Optimisations Recommended

Remove: hermes-homeassistant from toolsets, slack block, discord block, whatsapp, telegram partial config, all TTS except edge, stt.openai + stt.mistral, agent.personalities.concise, bedrock full config block.

Estimated config reduction: ~40% of 12,397 bytes.

#### /goal Instruction Set

Full 7-phase /goal command produced for "PRODUCTION-READY WORKSTATION CONVERGENCE":

1. Excise messaging platform overhead (slack, discord, whatsapp, telegram)
2. Strip audio bloat (keep only edge TTS, local STT)
3. Remove unused toolsets (hermes-homeassistant)
4. Resolve memory provider ambiguity (either remove honcho or activate it)
5. Fix MCP transport (verify mcp-proxy SSE or switch to mcp-remote bridge)
6. Add production fallback model (google/gemini-3-flash)
7. Apply and verify (chezmoi diff, apply, hermes config show, hermes mcp list)