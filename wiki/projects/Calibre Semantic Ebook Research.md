---
title: Calibre Semantic Ebook Research
wiki_type: dossier
entity_kind: project
created: 2026-05-22 13:30:00+01:00
modified: 2026-05-22 13:30:00+01:00
tags:
- wiki
- dossier
sources:
- raw/2026-05-22-pieces-calibre-semantic-search.md
permalink: llmeon/wiki/projects/calibre-semantic-ebook-research
---

# Calibre Semantic Ebook Research

## Summary

A Hermes skill system for semantic search across a Calibre ebook library. The agent searches ebooks by topic (e.g. prime numbers), identifies relevant passages, and generates structured reading lists/research notes integrated with the Obsidian PKM vault. Combines Calibre's LLM interaction tools with graph-based semantic search (via graphify MCP) and a custom `library-indexer` skill.

## Key Facts

- User has a large Calibre ebook collection with tools allowing LLM interaction — [[raw/2026-05-22-pieces-calibre-semantic-search]] (Pieces: 61d5ea5e-9ce6-4f7b-b94b-a5db310038fc)
- The goal is to find content about specific subjects across all ebooks — "currently I am learning about prime numbers" — and generate a reading list/index — [[raw/2026-05-22-pieces-calibre-semantic-search]] (Pieces: 61d5ea5e-9ce6-4f7b-b94b-a5db310038fc)
- Implementation uses graphify MCP for semantic graph queries over the book collection — [[raw/2026-05-22-pieces-calibre-semantic-search]] (Pieces: 47332891-902c-4b0a-badf-6cbd31e69336)
- Initial raw export completed: `calibre_raw_export/` contains 13 `.txt` files (~7.5MB of book content) — [[raw/2026-05-22-pieces-calibre-semantic-search]] (Pieces: 47332891-902c-4b0a-badf-6cbd31e69336)
- A `library-indexer` custom skill is being created at `~/.hermes/skills/custom/library-indexer/SKILL.md` — [[raw/2026-05-22-pieces-calibre-semantic-search]] (Pieces: 9b2e947b-4970-49e5-874a-1cd317022ab9)
- A `calibre-topic-research` TRANSFER artefact was delivered defining the reusable skill — [[raw/2026-05-22-pieces-calibre-semantic-search]] (Pieces: 10a3d3e1-1cd2-4777-92ac-aae9c9a6dffe)
- A `/goal` command was produced for step-by-step implementation with testing gates — [[raw/2026-05-22-pieces-calibre-semantic-search]] (Pieces: add67161-349a-4c86-96c8-23d07ffec735)
- A prior Hermes session was interrupted mid-execution during a chezmoi patch to `private_config.yaml` — [[raw/2026-05-22-pieces-calibre-semantic-search]] (Pieces: f8aac3ee-37b9-46fc-a23f-cb05c8e7694c)

## Connections

- [[Obsidian-PKM]] — research output feeds into the vault
- [[Pieces-LTM]] — captures the design and implementation sessions
- [[Hermes-Agent]] — the skill system being extended

## Contradictions

_(none yet)_

## Open Questions

- Is graphify MCP a persistent service or does it need re-indexing on each session?
- How does the book graph handle incremental updates when new books are added to Calibre?
- What is the final output format — markdown reading list, Obsidian note per book, or structured PKM entry?
- Status of completion — some gates were verified as done (raw export, config patch, graph query) but the `library-indexer` SKILL.md may not have been written to disk yet after the session interruption.

## Timeline

- **2026-05-22 09:18 UTC** — User requests the feature; agent begins design
- **2026-05-22 09:27 UTC** — `calibre-topic-research` TRANSFER artefact delivered
- **2026-05-22 09:41 UTC** — `/goal` command for iterative implementation delivered
- **2026-05-22 12:42 UTC** — Session interrupted during chezmoi patch
- **2026-05-22 12:43 UTC** — Continuation session assesses completed gates
- **2026-05-22 12:47 UTC** — Evaluator requests `library-indexer` SKILL.md output
- **2026-05-22 13:10 UTC** — User requests conversion to `/goal` format; Gate 1/2/4 confirmed done; session continues