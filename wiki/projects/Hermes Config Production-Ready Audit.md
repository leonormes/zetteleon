---
title: Hermes Config Production-Ready Audit
wiki_type: dossier
entity_kind: project
created: 2026-05-23T12:52:00+00:00
modified: 2026-05-30T08:33:27+00:00
tags: [wiki, dossier]
sources: [raw/2026-05-23-phermes-config-audit.md, raw/2026-05-24-pieces-hermes-starship-config.md, raw/2026-05-24-pieces-starship-hermes-review.md, raw/2026-05-24-pieces-hermes-discovery-report.md, raw/2026-05-24-pieces-hermes-discovery-report-full.md, raw/2026-05-28-pieces-ftfl511-jira-ticket.md, raw/2026-05-28-pieces-hermes-config-validation.md, raw/2026-05-30-pieces-hermes-mcp-config.md]
---

## Summary

Configuration audit of `~/.hermes/config.yaml` (12,397 bytes) to identify redundancies, conflicts, and optimisations. Produced a `/goal` instruction set for converging the Hermes workstation to a production-ready state. Focused on removing messaging platform overhead, audio bloat, unused toolsets, and resolving memory provider ambiguity. A remediation plan was executed on 2026-05-23 with all HIGH and MEDIUM priority items landing successfully.

## Key Facts

- **Config file:** `~/.hermes/config.yaml`, 12,397 bytes, `_config_version: 22` — [[raw/2026-05-23-phermes-config-audit]] (Pieces: d8d6bdcc-bbd2-400f-ae0b-ef936b251e4c)
- **Active model:** `openrouter/owl-alpha` with single provider, zero fallback providers — [[raw/2026-05-23-phermes-config-audit]] (Pieces: ff8ec9bd-41bd-4497-86de-a374967ef2e9)
- **Key redundancies found:**
  - Single-model providers block with no routing diversity (35+ providers available during setup, none enrolled)
  - Six TTS providers configured, only edge active (`auto_tts: false`)
  - Three STT backends, only local whisper active
  - Dual personalities (concise + technical) with `display.personality: technical` making concise unused
  — [[raw/2026-05-23-phermes-config-audit]] (Pieces: ff8ec9bd-41bd-4497-86de-a374967ef2e9)
- **Key conflicts found:**
  - `memory.provider: ''` but empty `honcho: {}` block exists (previous honcho setup reverted by chezmoi apply)
  - MCP transport: mcp-proxy uses HTTP SSE (previously unreliable), graphify uses stdio
  - `hermes-homeassistant` in toolsets but zero HA usage in 30 days
  - Slack + Discord both configured but user workflow is 100% terminal + Teams
  — [[raw/2026-05-23-phermes-config-audit]] (Pieces: ff8ec9bd-41bd-4497-86de-a374967ef2e9)
- **Recommended removals:** hermes-homeassistant, slack, discord, whatsapp, telegram, all TTS except edge, stt.openai/mistral, concise personality, bedrock config — estimated ~40% config reduction — [[raw/2026-05-23-phermes-config-audit]] (Pieces: ff8ec9bd-41bd-4497-86de-a374967ef2e9)
- **/goal instruction set produced:** 7-phase PRODUCTION-READY WORKSTATION CONVERGENCE covering messaging excision, audio bloat removal, toolset cleanup, memory provider resolution, MCP transport fix, fallback model addition, and verification — [[raw/2026-05-23-phermes-config-audit]] (Pieces: ff8ec9bd-41bd-4497-86de-a374967ef2e9)
- **Plan executed 2026-05-23:** All HIGH and MEDIUM items landed — (I-01) Default model changed to `qwen/qwen3.5:cloud` ✅, (I-02) Pieces MCP server added (SSE, localhost:39300) ✅, (I-05) §1.5 Pre-Task Context Rule added to SOUL.md ✅ — doctor issue count dropped from 2→1, remaining issue is pre-existing (missing API keys) — [[raw/2026-05-24-pieces-hermes-starship-config.md]] (Pieces: 9054377c)
- **Self-review prompt created 2026-05-24T15:09:** Comprehensive 8-area audit prompt covering provider config, toolset audit, memory config, skill inventory, TTS/STT, MCP servers, personality/display, and cron jobs — each area graded HIGH/MEDIUM/LOW priority — [[raw/2026-05-24-pieces-starship-hermes-review.md]] (Pieces: 8bbed588)
- **Gemini blog post validation session 2026-05-23T15:05:** User requested a /goal prompt for Hermes to self-review config and fix inconsistencies — prompt directed Hermes to use Gemini and Claude CLI for coding tasks after cheaper models build full context, and to analyse the chezmoi codebase for model usage optimisation — [[raw/2026-05-24-pieces-hermes-starship-config.md]] (Pieces: 96d5bb83)
- **Discovery Report commissioned 2026-05-24T18:00:** User asked Hermes to consolidate all captured knowledge about its own configuration into a structured 6-section discovery report — covering Project Identity, Architectural State, Design Decisions, Pending Work, Known Issues, and External References — grounding all claims to specific tool results with citations — [[raw/2026-05-24-pieces-hermes-discovery-report]] (Pieces: 70503f11)
- **Discovery Report delivered 2026-05-24T18:09:** Full report delivered after multi-wave LTM synthesis — confirmed 14 personalities (technical active), _config_version: 23, context_length: 128000, memory.provider: honcho — documented 4-layer memory architecture (built-in → session state → honcho → Obsidian vault) — identified Apfel rejection rationale (4K context floor vs 64k Hermes minimum) — catalogued pending work: Voice Note Ingestion Skill, /digest quick-command, brain-mcp upgrade, Infrastructure Wiki Directory — [[raw/2026-05-24-pieces-hermes-discovery-report]] (Pieces: ee492eb2)
- **New open questions from discovery report:** (1) Whether intelligent model routing policy YAML was ever implemented in config, (2) Whether brain-mcp cognitive layer migration executed, (3) Whether daily digest cron delivery to messaging platforms works end-to-end — [[raw/2026-05-24-pieces-hermes-discovery-report]] (Pieces: ee492eb2)
- **Version history confirmed:** `v0.11.0 (2026.4.23)` → `v0.12.0 (2026.4.30)` → `v0.13.0 (2026.5.7)` → `v0.14.0 (2026.5.16)` — tracked via `hermes --version`, `hermes doctor`, and GitKraken events — [[raw/2026-05-24-pieces-hermes-discovery-report-full]] (Pieces: c8c5de20-42b9-45d4-a2b4-07c43e6c83fc)
- **TUI startup performance target:** under 10 seconds — baseline at time of diagnosis was 30–40 seconds (timing out after 15s in test) — [[raw/2026-05-24-pieces-hermes-discovery-report-full]] (Pieces: c8c5de20-42b9-45d4-a2b4-07c43e6c83fc)
- **Context length target ≥128k:** cited following OpenClaw comparison review (11 May 2026); current was 64,000, recommended 128,000+ — addressed by switching primary model to `qwen/qwen3.5-plus-20260420` (1M context, May 23) — [[raw/2026-05-24-pieces-hermes-discovery-report-full]] (Pieces: c8c5de20-42b9-45d4-a2b4-07c43e6c83fc)
- **max_turns: 30** set as functional threshold for long-running agentic tasks after repeated freeze complaints (May 16–18); `max_turns` (main loop) and `max_iterations` (delegation) distinguished as separate parameters — [[raw/2026-05-24-pieces-hermes-discovery-report-full]] (Pieces: c8c5de20-42b9-45d4-a2b4-07c43e6c83fc)
- **Profiles inventory confirmed:** `cowork.yaml`, `ops.yaml`, `research.yaml`, `thin.yaml`, `creative.yaml`, `infra.yaml`, `pkm.yaml` — confirmed by GitKraken and chezmoi file-explorer captures — [[raw/2026-05-24-pieces-hermes-discovery-report-full]] (Pieces: c8c5de20-42b9-45d4-a2b4-07c43e6c83fc)
- **brain-mcp cognitive layer:** proposed in a May 18 Gemini session as a future upgrade; no evidence of implementation as of 2026-05-24 — [[raw/2026-05-24-pieces-hermes-discovery-report-full]] (Pieces: c8c5de20-42b9-45d4-a2b4-07c43e6c83fc)
- **Voice-capture skill:** discussed as a planned enhancement on 23 May 2026; no evidence of implementation — [[raw/2026-05-24-pieces-hermes-discovery-report-full]] (Pieces: c8c5de20-42b9-45d4-a2b4-07c43e6c83fc)


- **2026-05-28 ~14:21**: Post-Cursor update validation confirmed all changes present and correct — `approvals.mode: smart` ✅, delegation lockdown (`inherit_mcp_toolsets: false`, `toolsets: [file]`, `max_iterations: 20`, `child_timeout_seconds: 120`, `reasoning_effort: high`) ✅, MCP tool filters (`mcp-proxy.tools.exclude: []`, `pieces.tools.include: [ask_pieces_ltm, search_pieces, save_to_pieces]`) ✅, Model Roles comment block (`free_main = owl-alpha / paid_reason = claude-sonnet-4-6`) ✅, 4 new infra skill files (`argocd-unstick`, `crashloop-triage`, `helm-validate`, `loki-label-audit`) ✅, `route-task.md` Infra/Debugging Protocol section ✅, `claude-code.md` "When NOT to use" section ✅, `cost-routing-pilot.md` Phase A+B ✅ — full validation report with 7-step test plan delivered — [[raw/2026-05-28-pieces-hermes-config-validation]] (Pieces: e987359e-137c-41e4-9d84-e9b63f7cddd5, 2c964efb-aca8-44ae-80f6-9a9517445ed2, d7a00c51-b046-4deb-b3a1-cfa991a5a526)

- **2026-05-30**: User requested a Hermes `/goal` prompt to audit and fix its own MCP server configuration — the prompt should direct Hermes to review the chezmoi repo for legacy MCP server settings and remove them from both the home directory and the chezmoi repo to prevent confusing LLM clients — [[raw/2026-05-30-pieces-hermes-mcp-config]] (Pieces: 97f2e103-f3f5-4c2c-8e9d-4e5f6a7b8c9d)

- **2026-05-30**: A complete `/goal` prompt was produced for the Hermes MCP self-fix mission, instructing Hermes to identify and remove stale MCP server entries from `~/.hermes/config.yaml` and the chezmoi template at `~/.local/share/chezmoi/dot_config/mcpproxy/` — [[raw/2026-05-30-pieces-hermes-mcp-config]] (Pieces: 19808e94-4125-4e3d-8e9f-4e5f6a7b8c9d)

## Timeline
- **2026-05-28**: Post-Cursor config update validation — all Cursor-applied changes confirmed present and correct
- **2026-05-30**: User requested Hermes `/goal` prompt for MCP self-fix; prompt produced to clean legacy MCP settings from chezmoi repo and home dir

- 2026-05-23: Config audit completed; /goal instruction set produced
- 2026-05-23: Remediation plan executed — all HIGH/MEDIUM items landed, 2→1 doctor issues
- 2026-05-24T15:09: Comprehensive self-review prompt created for 8-area config audit
- 2026-05-24T18:00-18:09: User commissioned and received comprehensive Discovery Report — 6-section synthesis of all captured Hermes configuration knowledge from LTM
- 2026-05-24T18:11: Full Discovery Report text captured — version history, TUI targets, context length targets, max_turns threshold, profiles inventory, brain-mcp proposal status, voice-capture skill status all confirmed

## Connections

- [[Hermes-Agent]] — parent Hermes project
- [[Hermes-Model-Configuration]] — model config error (qwen3.5:cloud) discovered during plan execution
- [[Hermes-TUI-Startup-Performance]] — slow startup investigation
- [[Chezmoi]] — config management tool (honcho conflict arose from chezmoi apply reverting manual edits)
- [[MCP Proxy Robustness and High Availability]] — related MCP transport concerns
- [[Unified LLM Router Cockpit]] — related LLM tooling unification project

## Contradictions

None identified.

## Open Questions

- Should Honcho be activated as memory provider, or should all Honcho config be removed entirely?
- Is mcp-proxy running via native SSE or mcp-remote bridge?
- Should `google/gemini-3-flash` be added as fallback provider?
- The plan changed default model to `qwen/qwen3.5:cloud` but the error referenced this exact ID as invalid — was the corrected ID applied?
- Which specific profile YAML file contained the stale `qwen3.5:cloud` reference and has it been updated?
- What are the findings of the 8-area self-review prompt created 2026-05-24T15:09?
