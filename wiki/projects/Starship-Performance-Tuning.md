---
title: Starship Performance Tuning
wiki_type: dossier
entity_kind: project
created: 2026-05-23T20:15:00+01:00
modified: 2026-05-24T20:15:00+01:00
tags: [wiki, dossier]
sources: [raw/2026-05-23-pieces-starship-config.md, raw/2026-05-24-pieces-starship-hermes-review.md]
---

# Starship Performance Tuning

## Summary

Analysis and optimisation of the Starship prompt configuration (`starship.toml`) managed via chezmoi. The project identified critical performance bottlenecks in the shell prompt configuration that were causing slow directory navigation, particularly in cloud/IaC working directories.

## Key Facts

- The current `starship.toml` is managed via chezmoi at `~/.local/share/chezmoi/dot_config/starship.toml` — [[raw/2026-05-23-pieces-starship-config.md]] (Pieces: 215a8fa1)
- `command_timeout = 2000` is dangerously high (default is 500ms) — every slow module gets a full 2 seconds to respond before abort — [[raw/2026-05-23-pieces-starship-config.md]] (Pieces: 215a8fa1)
- `$kubernetes` runs `kubectl` on every prompt render, causing significant latency — [[raw/2026-05-23-pieces-starship-config.md]] (Pieces: 215a8fa1)
- `$azure` and `$aws` modules run CLI reads every prompt with no directory scoping — [[raw/2026-05-23-pieces-starship-config.md]] (Pieces: 215a8fa1)
- `git_status` is missing `ignore_submodules` which adds unnecessary latency in repos with submodules — [[raw/2026-05-23-pieces-starship-config.md]] (Pieces: 215a8fa1)
- The user also asked about Hermes model fallback behaviour when OpenRouter returns HTTP 402 (insufficient credits) — [[raw/2026-05-23-pieces-starship-config.md]] (Pieces: 9f666d49)
- **Fix applied 2026-05-24T20:05:00:** All five performance bottlenecks resolved — `command_timeout` 2000→500, `$kubernetes` disabled, `$azure`/`$aws` directory-scoped, `git_status.ignore_submodules: true` added — [[raw/2026-05-24-pieces-starship-hermes-review.md]] (Pieces: 2b045ae4)
- Grounded `/goal` prompt used for the fix: evidence-based approach using Pieces LTM context, `chezmoi diff` verification, user approval gate before `chezmoi apply` — [[raw/2026-05-24-pieces-starship-hermes-review.md]] (Pieces: c0f950bd)
- Unused TTS config audit also run as a parallel `/goal` prompt targeting dormant TTS provider identification — [[raw/2026-05-24-pieces-starship-hermes-review.md]] (Pieces: 765deb6b)

## Timeline

- 2026-05-23: Initial audit completed — identified 5 performance bottlenecks in starship.toml
- 2026-05-24T20:05:00: Fix applied — all 5 bottlenecks resolved via grounded `/goal` prompt

## Connections

- [[Chezmoi]] — starship.toml is chezmoi-managed
- [[Hermes Config Production-Ready Audit]] — TTS config audit run in parallel

## Contradictions

_(none)_

## Open Questions

- ~~Has the starship.toml been updated with the recommended fixes?~~ ✅ Fix applied 2026-05-24T20:05:00
- Should Hermes implement automatic model fallback on OpenRouter 402 errors?
- Did the TTS config audit produce actionable results?
