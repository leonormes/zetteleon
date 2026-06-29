---
title: Hermes Iteration Limit Configuration
wiki_type: dossier
entity_kind: project
created: 2026-05-16 21:27:00+00:00
modified: 2026-05-16 21:27:00+00:00
tags:
- wiki
- dossier
sources:
- raw/2026-05-16-pieces-hermes-iteration-limit.md
permalink: llmeon/wiki/projects/hermes-iteration-limit-configuration
---

## Summary

Debugging and configuration workstream focused on resolving Hermes agent's iteration limit freeze at 10/10 turns. The issue stems from confusion between two distinct configuration parameters: `max_turns` (main chat loop limit) and `max_iterations` (background delegation limit).

## Key Facts

- > "Hermes has two different iteration limits: `max_turns` (which controls the main chat loop) and `max_iterations` (which controls background delegation)" — [[raw/2026-05-16-pieces-hermes-iteration-limit]] (Pieces: 964cf4d4-6e04-491f-89fd-03826dc37244)

- > "You previously updated the delegation limit to 30, but your main agent is still restricted by `max_turns: 10`" — [[raw/2026-05-16-pieces-hermes-iteration-limit]] (Pieces: 964cf4d4-6e04-491f-89fd-03826dc37244)

- > "The previous change to 'max_iterations' didn't fix the 10/10 freeze because that controls delegation" — [[raw/2026-05-16-pieces-hermes-iteration-limit]] (Pieces: b8abffcd-79b5-434a-b7fb-3d2c931b6d8e)

- User request: "I keep getting stuck at 10/10 interations. And have to ask it to carry on" — [[raw/2026-05-16-pieces-hermes-iteration-limit]] (Pieces: b8abffcd-79b5-434a-b7fb-3d2c931b6d8e)

## Connections

- [[wiki/projects/Unified LLM Router Cockpit]] — Hermes configuration management via chezmoi
- [[wiki/concepts/Hermes Configuration Architecture]] — relates to config.yaml structure and parameter semantics

## Timeline

- **2026-05-16T17:04** — User attempted to change iteration limit from 10 to 30; agent incorrectly modified `max_iterations` instead of `max_turns`
- **2026-05-16T17:04** — Diagnostic output identified the root cause: two separate limits control different aspects of agent behaviour

## Contradictions

_None identified_

## Open Questions

- What is the recommended default value for `max_turns` for typical development workflows?
- Should the configuration schema include comments distinguishing `max_turns` vs `max_iterations` to prevent future confusion?
- Are there other iteration-related limits in the Hermes configuration that could cause similar confusion?