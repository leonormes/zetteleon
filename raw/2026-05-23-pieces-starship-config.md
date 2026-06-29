---
created: 2026-05-23 20:15:00+01:00
modified: 2026-05-26 11:43:32+00:00
pieces_ids:
- 0275d582-225a-42b3-aa44-640c8a8408ca
- 215a8fa1-70cb-43bd-a6df-c95703210e3c
- 42cc21a2-ec3a-4141-b253-9e80b142af38
- 9f666d49-e2ef-45ab-97a1-ae65494c006b
source: pieces-ltm
tags:
- pieces
- raw
title: 2026-05-23-pieces-starship-config
permalink: llmeon/raw/2026-05-23-pieces-starship-config
---

## Starship Prompt Performance Tuning Analysis

### Asset 1 (Pieces: 42cc21a2-ec3a-4141-b253-9e80b142af38)

User request: give me a hermes /goal prompt to fix starship toml

### Asset 2 (Pieces: 215a8fa1-70cb-43bd-a6df-c95703210e3c)

Starship config analysis + Hermes fallback question

Your config at `/Users/leon.ormes/.local/share/chezmoi/dot_config/starship.toml` has three genuine performance bottlenecks and one misconfiguration that makes them worse.

#### Critical—fix These First

1. `command_timeout = 2000` is dangerously high

You've set a 2-second patience window. Every slow module gets a full 2000ms to respond before being aborted. The default is 500ms. Combine…

### Asset 3 (Pieces: 9f666d49-e2ef-45ab-97a1-ae65494c006b)

User request: I am now getting review my starship prompt line config. @file:dot_config/starship.toml and suggest any speed ups

API call failed after 3 retries: HTTP 402: This request requires more credits, or fewer max_tokens. You requested up to 65536 tokens, but can only afford 22146. To increase, visit Sign In | OpenRouter and upgrade to a paid account

Shouldn't hermes use a different model when this happens? Gemini flash cli for instance? or would I need to pay openRouter

### Asset 4 (Pieces: 0275d582-225a-42b3-aa44-640c8a8408ca)

Now I have both the starship.toml content and the web search results. Let me analyze the config and provide recommendations, plus address the Hermes/OpenRouter question.

Config analysis:

```toml
command_timeout = 2000  # Very high - 2 seconds!
format = "$directory $git_branch $git_status $kubernetes $azure $aws $time$line_break$character"

[kubernetes] disabled = false
[aws] disabled = false
```