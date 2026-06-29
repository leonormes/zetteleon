---
title: ProdOS Workflow Design
wiki_type: dossier
entity_kind: project
created: 2026-05-26 12:00:00+00:00
modified: 2026-05-26 12:00:00+00:00
tags:
- wiki
- dossier
sources:
- raw/2026-05-26-pieces-prodos-workflow-design.md
permalink: llmeon/wiki/projects/prod-os-workflow
---

## Summary

Design session for the ProdOS (Productivity Operating System) work-loop — an AI Chief of Staff bridge between Todoist (action engine) and Obsidian (knowledge/source-of-truth layer). The project defines requirements and produces a Hermes `/goal` prompt for configuring Hermes Gateway to periodically check Jira and Microsoft Teams, update Obsidian with outstanding work, keep Todoist in sync, and run CoS reviews. Designed on 2026-05-26 to be deliberately simple and tool-agnostic.

## Key Facts

- **User request (09:17)**: "I need my local llm to help setup my prodOS workflow. I get my work tasks from jira. I also have teams for meetings and chat. I need the CoS llm to review open tasks and info from my work teams and jira as part of the bringing together of all open loops" — [[raw/2026-05-26-pieces-prodos-workflow-design]] (Pieces: 7b5ffddd-40e0-450d-81cc-e2c2d71eb7a8)
- **ProdOS philosophy**: Keep the system deliberately simple and tool-agnostic. ProdOS is the AI Chief of Staff bridge between Todoist and Obsidian, not another over-engineered infrastructure project — [[raw/2026-05-26-pieces-prodos-workflow-design]] (Pieces: 9d3580da-5501-49f8-a21d-bd2d2c44e302)
- **Core architecture**: Hermes Gateway periodically checks Jira (work tasks) + Microsoft Teams (meetings and chat) → updates Obsidian Source of Truth → keeps Todoist up to date — [[raw/2026-05-26-pieces-prodos-workflow-design]] (Pieces: 7b5ffddd-40e0-450d-81cc-e2c2d71eb7a8)
- **Pieces LTM integration**: Uses Pieces LTM for an overview/sensory input layer — [[raw/2026-05-26-pieces-prodos-workflow-design]] (Pieces: 7b5ffddd-40e0-450d-81cc-e2c2d71eb7a8)
- **Jira config captured**: `base_url: "https://fitfile.atlassian.net"`, project key `FTFL`, JQL filter `assignee = currentUser() AND statusCategory != Done ORDER BY updated DESC`, `poll_interval: 30m` — [[raw/2026-05-26-pieces-prodos-workflow-design]] (Pieces: 4c07fa14-4e4d-483b-b08d-78f26061c256)
- **Todoist config captured**: `default_project: "Work"`, `prodos_label: "@work"`, `sync_on_update: true` — [[raw/2026-05-26-pieces-prodos-workflow-design]] (Pieces: 4c07fa14-4e4d-483b-b08d-78f26061c256)
- **Hermes setup documented**: Hermes v0.14.0, primary model `openrouter/owl-alpha`, config managed via chezmoi — [[raw/2026-05-26-pieces-prodos-workflow-design]] (Pieces: 17d6a7d9-e663-4976-9393-c4b56b436d05)
- **Full requirements document + LLM prompt delivered**: A complete, copy-paste-ready Hermes `/goal` prompt was synthesised covering the entire ProdOS work-loop — [[raw/2026-05-26-pieces-prodos-workflow-design]] (Pieces: 56fb26e6-2a2d-403a-9a06-22c775f56f6f)

## Timeline

- **2026-05-26 09:17** — User requested ProdOS workflow setup requirements and LLM prompt
- **2026-05-26 ~09:21–09:32** — Requirements document and Hermes `/goal` prompt synthesised and delivered
- **2026-05-26 09:24** — User requested "give me the hermes prompt to set this up properly" — confirmed delivery

## Connections

- [[wiki/projects/CoS-Work-Review-System]] — The CoS work-review system is the operational implementation of the ProdOS design
- [[wiki/projects/Obsidian-PKM]] — Obsidian as the Source of Truth layer in the ProdOS architecture
- [[wiki/projects/Hermes-Agent]] — Hermes as the orchestrator/Gateway in the ProdOS architecture
- [[wiki/projects/Terraform IaC Modules]] — FITFILE infrastructure work managed through Jira tickets

## Contradictions

_(none)_

## Open Questions

- Has the Hermes `/goal` prompt been executed yet, or only generated?
- Microsoft Teams integration — is there a working Teams MCP connector, or does this need to be built?
- Todoist OAuth token setup — is `op://Personal/todoist-api/credential` already configured in 1Password?