---
title: GitKraken `gk issue list` Output Format Investigation
created: 2026-06-05 13:23:20+00:00
source: pieces-ltm
pieces_ids:
- fe4f9ec1-e4e2-40b8-8985-c2076255d4d9
- 55699589-ac61-4ece-be76-8d1f2e7f66ff
tags:
- raw
- pieces
permalink: llmeon/raw/2026-06-05-pieces-gk-issue-list-format
---

# GitKraken `gk issue list` Output Format Investigation

## Asset 1 — User Prompt (13:23:20)

does gk issues list have different output formats? The table it outputs is truncated

## Asset 2 — Agent Synthesis (13:26:34)

Memory is `sufficient` — pagination is done. All three pages are clear: the memory has no additional `gk issue list` format data beyond what was in page 1. The relevant signal was already in page 1 (your Obsidian note `gitkraken-gk-cli-for-llm-assistants` and the `gk issue list` call itself). Pages 2 and 3 are entirely Monaco GP audio transcripts — no additional `gk` format information.

**Conclusion:** `gk issue list` does not appear to have alternative output formats. The table truncation is the expected behaviour. The Obsidian note `gitkraken-gk-cli-for-llm-assistants` already contains the relevant documentation.