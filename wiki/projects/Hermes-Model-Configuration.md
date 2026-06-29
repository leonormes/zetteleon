---
title: Hermes Model Configuration
wiki_type: dossier
entity_kind: project
created: 2026-05-23 20:15:00+01:00
modified: 2026-05-29 15:33:41+00:00
tags:
- wiki
- dossier
sources:
- raw/2026-05-23-pieces-hermes-model-error.md
- raw/2026-05-27-pieces-hermes-model-config
- raw/2026-05-29-pieces-hermes-openrouter
permalink: llmeon/wiki/projects/hermes-model-configuration
---

# Hermes Model Configuration

## Summary

Diagnosis and resolution of the `qwen/qwen3.5:cloud is not a valid model ID` error appearing when running Hermes. Both the live config and chezmoi source already had the correct model ID; the stale reference was traced to a profile YAML file.

## Key Facts

- Both `~/.hermes/config.yaml` (live) and `~/.local/share/chezmoi/private_dot_hermes/private_config.yaml` (chezmoi source) show `default: qwen/qwen3.5-plus-20260420` — a valid OpenRouter model ID — [[raw/2026-05-23-pieces-hermes-model-error.md]] (Pieces: eca53792)
- The stale `qwen/qwen3.5:cloud` string lives in two profile YAML files: `~/.hermes/profiles/ops.yaml` and `~/.hermes/profiles/jira.yaml` — both set `model: qwen3.5:cloud` — [[raw/2026-05-23-pieces-hermes-model-error.md]] (Pieces: eca53792)
- The fix requires changing `model: qwen3.5:cloud` → `model: qwen/qwen3.5-plus-20260420` in both profile files, then updating the chezmoi source at `~/.local/share/chezmoi/private_dot_hermes/profiles/` — [[raw/2026-05-23-pieces-hermes-model-error.md]] (Pieces: eca53792)
- The error `qwen/qwen3.5:cloud is not a valid model ID` was triggered during a `/goal` prompt execution, not during normal Hermes startup — [[raw/2026-05-23-pieces-hermes-model-error.md]] (Pieces: 731b9ccf)
- The correct model ID `qwen/qwen3.5-plus-20260420` was already in both config files — the fix requires updating the stale profile YAML reference — [[raw/2026-05-23-pieces-hermes-model-error.md]] (Pieces: e0116cd3)

- **2026-05-27**: User enquired about using OpenRouter with Hermes to access different AI models — Hermes was timing out when trying to use Claude Code CLI, and the user wanted to use OpenRouter as a fallback for multi-model access — [[raw/2026-05-27-pieces-hermes-model-config]] (Pieces: 3a8ea5cd-a70b-4f68-83a9-49803a16b8d3)

- **2026-05-27**: Research initiated into OpenRouter free model list, pay-per-use pricing tiers, and multi-model orchestration patterns — [[raw/2026-05-27-pieces-hermes-model-config]] (Pieces: c66f274f-ba9c-411a-b534-a2c682bb76b7)

- **2026-05-29**: User enquired about whether to keep Ollama subscription alongside OpenRouter — current Hermes config uses `openrouter/owl-alpha` as default (free), context 128k — [[raw/2026-05-29-pieces-hermes-openrouter]] (Pieces: 3737d524-416b-485c-8fe6-cd84aed42784)

- **2026-05-29**: OpenRouter usage this month: DeepSeek V4 Flash (2.06T tokens), Owl Alpha (1.35T), DeepSeek V4 Pro (643B), MiniMax M2.7 (550B) — cost-tiered routing pattern working well — [[raw/2026-05-29-pieces-hermes-openrouter]] (Pieces: d6f89dd3-b969-4efe-86bc-32bf76afbf76)

- **2026-05-29**: User hit HTTP 402 on 23 May when default model was `qwen/qwen3.5-plus-20260420`; fix was switching to `openrouter/owl-alpha` as default — [[raw/2026-05-29-pieces-hermes-openrouter]] (Pieces: d6f89dd3-b969-4efe-86bc-32bf76afbf76)


## Connections

- [[Hermes Config Production-Ready Audit]] — broader config audit project
- [[Hermes Iteration Limit Configuration]] — related Hermes config debug workstream
- [[Chezmoi]] — config files are chezmoi-managed
- [[Hermes-Multi-Model-Routing-Strategy]] — multi-model routing research and design

## Timeline

- **2026-05-23** — Project page created; `qwen/qwen3.5:cloud` error traced to stale profile YAML files
- **2026-05-27** — OpenRouter research initiated; multi-model orchestration patterns explored
- **2026-05-29** — Ollama vs OpenRouter subscription question raised; cost-tiered routing confirmed working well

## Contradictions

_(none)_

## Open Questions

- Which specific profile YAML file contains the stale `qwen3.5:cloud` reference?
- Has the profile file been updated to use the correct model ID?
- Should Hermes validate profile YAML model references at startup?