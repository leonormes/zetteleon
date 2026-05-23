---
title: Hermes Config Production-Ready Audit
wiki_type: dossier
entity_kind: project
created: 2026-05-23T12:52:00+00:00
modified: 2026-05-23T12:52:00+00:00
tags: [wiki, dossier]
sources: [raw/2026-05-23-pieces-config-audit.md]
---

## Summary

Configuration audit of `~/.hermes/config.yaml` (12,397 bytes) to identify redundancies, conflicts, and optimisations. Produced a `/goal` instruction set for converging the Hermes workstation to a production-ready state. Focused on removing messaging platform overhead, audio bloat, unused toolsets, and resolving memory provider ambiguity.

## Key Facts

- **Config file:** `~/.hermes/config.yaml`, 12,397 bytes, `_config_version: 22` — [[raw/2026-05-23-pieces-config-audit]] (Pieces: d8d6bdcc-bbd2-400f-ae0b-ef936b251e4c)
- **Active model:** `openrouter/owl-alpha` with single provider, zero fallback providers — [[raw/2026-05-23-pieces-config-audit]] (Pieces: ff8ec9bd-41bd-4497-86de-a374967ef2e9)
- **Key redundancies found:**
  - Single-model providers block with no routing diversity (35+ providers available during setup, none enrolled)
  - Six TTS providers configured, only edge active (`auto_tts: false`)
  - Three STT backends, only local whisper active
  - Dual personalities (concise + technical) with `display.personality: technical` making concise unused
  — [[raw/2026-05-23-pieces-config-audit]] (Pieces: ff8ec9bd-41bd-4497-86de-a374967ef2e9)
- **Key conflicts found:**
  - `memory.provider: ''` but empty `honcho: {}` block exists (previous honcho setup reverted by chezmoi apply)
  - MCP transport: mcp-proxy uses HTTP SSE (previously unreliable), graphify uses stdio
  - `hermes-homeassistant` in toolsets but zero HA usage in 30 days
  - Slack + Discord both configured but user workflow is 100% terminal + Teams
  — [[raw/2026-05-23-pieces-config-audit]] (Pieces: ff8ec9bd-41bd-4497-86de-a374967ef2e9)
- **Recommended removals:** hermes-homeassistant, slack, discord, whatsapp, telegram, all TTS except edge, stt.openai/mistral, concise personality, bedrock config — estimated ~40% config reduction — [[raw/2026-05-23-pieces-config-audit]] (Pieces: ff8ec9bd-41bd-4497-86de-a374967ef2e9)
- **/goal instruction set produced:** 7-phase PRODUCTION-READY WORKSTATION CONVERGENCE covering messaging excision, audio bloat removal, toolset cleanup, memory provider resolution, MCP transport fix, fallback model addition, and verification — [[raw/2026-05-23-pieces-config-audit]] (Pieces: ff8ec9bd-41bd-4497-86de-a374967ef2e9)

## Timeline

- 2026-05-23: Config audit completed; /goal instruction set produced

## Connections

- [[Hermes-Agent]] — parent Hermes project
- [[Chezmoi]] — config management tool (honcho conflict arose from chezmoi apply reverting manual edits)
- [[MCP Proxy Robustness and High Availability]] — related MCP transport concerns
- [[Unified LLM Router Cockpit]] — related LLM tooling unification project

## Contradictions

None identified.

## Open Questions

- Should Honcho be activated as memory provider, or should all Honcho config be removed entirely?
- Is mcp-proxy running via native SSE or mcp-remote bridge?
- Should `google/gemini-3-flash` be added as fallback provider?
- Should the `/goal` instruction set be executed immediately or scheduled?
