---
title: Antigravity CLI Migration
wiki_type: dossier
entity_kind: project
created: 2026-05-26T12:00:00+00:00
modified: 2026-05-26T12:00:00+00:00
tags: [wiki, dossier]
sources: [raw/2026-05-26-pieces-antigravity-migration.md]
---

## Summary

Migration from Google's Gemini CLI to the new Antigravity CLI (`agy`), prompted by Google's announcement that Gemini CLI and Gemini Code Assist IDE extensions will stop serving requests for individual/free tier users on June 18, 2026. This project covers the setup of Antigravity CLI and the creation of a Claude Code prompt to automate the chezmoi config migration (removing Gemini config, adding agy).

## Key Facts

- **June 18, 2026 deadline**: Google announced Gemini CLI will stop serving requests for Google One and unpaid tiers on this date — [[raw/2026-05-26-pieces-antigravity-migration]] (Pieces: 2ba7704d-8aa4-4d6b-a87b-8fa3fbc5f27e)
- **Antigravity CLI (`agy`)**: Google's unified multi-agent platform replacing Gemini CLI for individual users — [[raw/2026-05-26-pieces-antigravity-migration]] (Pieces: 929cf490-53d1-42c0-9506-76c03758605f)
- **Claude Code chezmoi prompt created**: A self-contained prompt for Claude Code CLI to manage the chezmoi config migration — install agy, remove Gemini CLI configuration, aliases, env vars, and obsolete files, with safety constraints (no deletion without backup) — [[raw/2026-05-26-pieces-antigravity-migration]] (Pieces: 6e732984-2448-4492-bb37-f84127da8193)
- **Chezmoi source directory**: `~/.local/share/chezmoi/` — the prompt targets this for safe, reversible changes — [[raw/2026-05-26-pieces-antigravity-migration]] (Pieces: 59f45708-051d-4165-91f2-0a23b53b0bc1)
- **Enterprise tier unaffected**: Google's enterprise/Standard/Enterprise customers are not forced off the old路径 yet — [[raw/2026-05-26-pieces-antigravity-migration]] (Pieces: 929cf490-53d1-42c0-9506-76c03758605f)

## Timeline

- **2026-05-26 ~08:57–09:03** — User researched Antigravity CLI setup requirements, received setup checklist, and requested Claude Code prompt for chezmoi migration
- **2026-05-26 09:03** — Claude Code prompt delivered

## Connections

- [[wiki/projects/Unified LLM Router Cockpit]] — overarching LLM tooling unification project
- [[wiki/projects/Chezmoi]] — chezmoi dotfile management that the migration targets
- [[wiki/projects/Hermes-Agent]] — Hermes as the orchestrator that will use agy post-migration

## Contradictions

_(none)_

## Open Questions

- Has the Antigravity CLI actually been installed yet, or only researched?
- Does the Claude Code prompt need to be run, or was it just generated for future use?
