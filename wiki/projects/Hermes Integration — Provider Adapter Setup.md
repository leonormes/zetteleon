---
title: Hermes Integration — Provider Adapter Setup
wiki_type: dossier
entity_kind: project
created: 2026-05-06T12:50:00+01:00
modified: 2026-05-06T12:50:00+01:00
tags: [wiki, dossier]
sources: [raw/2026-05-06-pieces-hermes-integration]
---

## Summary

A focused implementation project to wire Claude and Gemini as first-class providers within the existing Hermes agent setup. The goal is to keep Hermes as the central orchestrator, memory hub, and PKM integrator while routing inference tasks to Claude or Gemini via provider adapters. This work sits under the umbrella of the broader Unified LLM Router Cockpit initiative.

## Key Facts

- Hermes already has a gateway, skill system, and a “provider/model” selection switch, but Claude Code CLI and Gemini CLI are used directly today, bypassing Hermes orchestration.
  > “Hermes can act as the orchestration backbone that lets you keep the benefits you get from Hermes (stateful sessions, memory, routing, sensors/guides) while using Claude or Gemini under the hood.” — [[raw/2026-05-06-pieces-hermes-integration]] (Pieces: 260ac1fc-3163-449b-be2d-82cb16cd1e46)
- Concrete starter configs for Anthropic Claude and Gemini providers have been drafted with endpoints, auth token env-var interpolation, and default models (claude-sonnet-4, gemini-2.5-flash).
  > “Minimal starter config … `hermes/providers/claude.yaml` … `hermes/providers/gemini.yaml`” — [[raw/2026-05-06-pieces-hermes-integration]] (Pieces: 260ac1fc-3163-449b-be2d-82cb16cd1e46)
- A proposed wiring pattern routes User prompt → Hermes gateway → router → provider adapter (Claude | Gemini) → response → Pieces LTM → Obsidian/wiki.
  > “Wiring summary: User prompt —> Hermes gateway —> router (task classifier) —> provider adapter … —> Pieces LTM —> Obsidian/wiki” — [[raw/2026-05-06-pieces-hermes-integration]] (Pieces: 260ac1fc-3163-449b-be2d-82cb16cd1e46)
- Five practical adoption patterns are identified: CLI aliases via `hermes run task --provider claude`, Zellij pane wiring, Pieces LTM ingestion from all CLIs, tiered routing rules, and a provider-model status sensor.
  > “Practical patterns to adopt next … 1. Create `hermes run task "<task>" --provider claude` alias … 5. Add a ‘provider model’ sensor to Hermes” — [[raw/2026-05-06-pieces-hermes-integration]] (Pieces: 260ac1fc-3163-449b-be2d-82cb16cd1e46)
- Security measures include managing API keys through environment variables or a secret store, restricting tokens, and monitoring usage.
  > “In Step 5, I'll focus on security by managing API keys through environment variables or a secret store, restricting tokens, and monitoring usage.” — [[raw/2026-05-06-pieces-hermes-integration]] (Pieces: 9bb443c9-9cbd-40af-ac17-cde84d20b553)
- Steps outlined include creating a `route-task.md` skill mapping, installing/configuring the CLI, restarting the `ai.hermes.gateway` service, building provider wrapper skills, and implementing compounding sessions for memory transfer between Claude and Gemini.
  > “Step 3 involves building skills, potentially by creating a ‘Claude’ skill wrapper … Step 4, I’ll implement ‘compounding sessions’ for memory transfer between Claude and Gemini.” — [[raw/2026-05-06-pieces-hermes-integration]] (Pieces: c867f159-ae8e-476c-8da5-25926a26f7b5)
- Prerequisites require Hermes installed with Docker Compose or Kubernetes support, plus valid API keys for Claude and Gemini.
  > “First, the prerequisites include ensuring Hermes is installed along with Docker Compose or Kubernetes. It’s essential that the Hermes gateway can support multiple providers and that I have the necessary API keys for Claude and Gemini.” — [[raw/2026-05-06-pieces-hermes-integration]] (Pieces: ef0b7cf3-f2a6-4f46-99c7-8d01d9af5fc9)

## Connections

- [[wiki/projects/Unified LLM Router Cockpit]] — parent initiative; this project is the concrete implementation phase for provider adapters within the cockpit
- [[raw/2026-05-06-pieces-hermes-integration]]

## Contradictions

_(none identified)_

## Open Questions

- Which secret store should hold provider API keys (1Password CLI, built-in Hermes secret manager, or system keychain)?
- Should the provider wrapper be a single generic `provider` skill or separate `claude` and `gemini` skills?
- How will cost attribution and token usage be surfaced to the user per provider/model per session?
- Is there a Zellij layout already defined in the Cockpit project that can be repurposed for the provider-switching workflow?
