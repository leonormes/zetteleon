---
title: Calibre Semantic Ebook Research — Skill Design & Implementation
created: 2026-05-22T13:30:00+01:00
source: pieces-ltm
pieces_ids: ["61d5ea5e-9ce6-4f7b-b94b-a5db310038fc", "9a160297-7df1-48ab-8e90-a13a63e0fe90", "3b698fd5-a1d3-4fed-a9bd-2798d6a50dfa", "c033815c-da14-4a08-8349-fe1dbdf7e85b", "10a3d3e1-1cd2-4777-92ac-aae9c9a6dffe", "add67161-349a-4c86-96c8-23d07ffec735", "f8aac3ee-37b9-46fc-a23f-cb05c8e7694c", "47332891-902c-4b0a-badf-6cbd31e69336", "8b06088b-d3cc-4b76-930f-f2b311008b6c", "7c890f05-212c-4e8c-99c3-3ec4b73a369a", "9b2e947b-4970-49e5-874a-1cd317022ab9", "32b9c984-dcfe-41f9-b896-a9680c02b8c3", "6f2dc9ac-6ad4-41ed-b9c8-7b5e1e86e830"]
tags: [raw, pieces]
---

# Calibre Semantic Ebook Research — Skill Design & Implementation

User is building a Hermes skill for semantic search across their Calibre ebook library, integrating with Obsidian PKM.

## Asset 1 (Pieces: 61d5ea5e-9ce6-4f7b-b94b-a5db310038fc) — 2026-05-22 09:18 UTC

User's original request:

> I have hermes set up. I also have a obsidian vault with my pkm. I have a large collection of ebooks in calibre. Calibre has tools to allow llm to interact with it. What I want is to be able to have hermes agents search and analyse the ebooks and find content about a particular subject. For instance, currently I am learning about prime numbers. I would like a skill in hermes that would semantically search my ebooks and find books that have content about primes. It should create a reading list/index.

## Asset 2 (Pieces: 9a160297-7df1-48ab-8e90-a13a63e0fe90) — 2026-05-22 09:18 UTC

Agent analysis of the request — designing the skill architecture.

## Asset 3 (Pieces: 3b698fd5-a1d3-4fed-a9bd-2798d6a50dfa) — 2026-05-22 09:35 UTC

User instruction:

> create a clear hermes /goal to work through this implementation step by step. make sure to test each stage and that the system is working as we iterate

## Asset 4 (Pieces: c033815c-da14-4a08-8349-fe1dbdf7e85b) — 2026-05-22 09:35 UTC

Agent context gathering for the /goal design — searching memory for Hermes skill templates and implementation patterns.

## Asset 5 (Pieces: 10a3d3e1-1cd2-4777-92ac-aae9c9a6dffe) — 2026-05-22 09:27 UTC

Delivered: `calibre-topic-research` TRANSFER artifact — a reusable Hermes skill that performs semantic search across the Calibre library and generates structured output.

## Asset 6 (Pieces: add67161-349a-4c86-96c8-23d07ffec735) — 2026-05-22 09:41 UTC

Delivered: `/goal` command for the Calibre Library Indexer Pipeline — a multi-stage implementation plan with testing gates.

## Asset 7 (Pieces: f8aac3ee-37b9-46fc-a23f-cb05c8e7694c) — 2026-05-22 12:42 UTC

Session status: Hermes stopped mid-execution during a Patch operation on `private_config.yaml`. Chezmoi patch was partially applied.

## Asset 8 (Pieces: 47332891-902c-4b0a-badf-6cbd31e69336) — 2026-05-22 12:43 UTC

Session analysis after interruption:
- Stage 1 ✅ — `calibre_raw_export/` has 13 text files (~7.5MB)
- Config patched ✅ — graphify added to `private_config.yaml`
- Session stopped during continuation

## Asset 9 (Pieces: 8b06088b-d3cc-4b76-930f-f2b311008b6c) — 2026-05-22 12:47 UTC

Evaluator requesting SKILL.md output for `~/.hermes/skills/custom/library-indexer/SKILL.md`.

## Asset 10 (Pieces: 7c890f05-212c-4e8c-99c3-3ec4b73a369a) — 2026-05-22 12:47 UTC

Agent preparing to write the `library-indexer` SKILL.md.

## Asset 11 (Pieces: 9b2e947b-4970-49e5-874a-1cd317022ab9) — 2026-05-22 12:48 UTC

Delivered: `library-indexer` SKILL.md content — semantically searches the Calibre book graph and generates structured output.

## Asset 12 (Pieces: 32b9c984-dcfe-41f9-b896-a9680c02b8c3) — 2026-05-22 13:10 UTC

Assessment of completed gates:
- Gate 1 ✅ — `calibre_raw_export/` exists with 13 `.txt` files
- Gate 2 ✅ — `private_config.yaml` patched with graphify MCP entry, `chezmoi apply` confirmed
- Gate 4 ✅ — Graph query returns correct books (Music of the Primes + crypto books)

## Asset 13 (Pieces: 6f2dc9ac-6ad4-41ed-b9c8-7b5e1e86e830) — 2026-05-22 13:10 UTC

User instruction:

> turn this into a hermes /goal to complete the work of setting up the semantic search of the calibre library
