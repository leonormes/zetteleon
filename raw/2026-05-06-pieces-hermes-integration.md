---
created: 2026-05-06T11:50:00+00:00
modified: 2026-07-20T16:33:26+00:00
permalink: llmeon/raw/2026-05-06-pieces-hermes-integration
pieces_ids: [02bf7ea4-d449-4977-bd64-f07096475b59, 260ac1fc-3163-449b-be2d-82cb16cd1e46, 9bb443c9-9cbd-40af-ac17-cde84d20b553, bab757b9-71eb-497b-a309-b2b97dd40f12, c867f159-ae8e-476c-8da5-25926a26f7b5, ef0b7cf3-f2a6-4f46-99c7-8d01d9af5fc9, ff5a8d3b-41b3-47c4-8c8d-30396e59c12f]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-05-06-pieces-hermes-integration
---

## Asset 1 (Pieces: 260ac1fc-3163-449b-be2d-82cb16cd1e46)

Great question. From your long-term memories, you're already running Hermes in your environment (gateway, skills, and a "provider/model" switch in Hermes), and you've been using Claude or Gemini directly via their CLI. Hermes can act as the orchestration backbone that lets you keep the benefits you get from Hermes (stateful sessions, memory, routing, sensors/guides) while using Claude or Gemini under the hood. Below is a concrete plan to get you there, plus a minimal starter config and practical patterns you can adopt.

What to aim for

- Use Hermes as the central orchestrator and memory hub that routes tasks to Claude or Gemini as needed.
- Treat Claude and Gemini as interchangeable providers (via Hermes adapters) so you can pick the best tool for the job without losing Hermes advantages (session continuity, context carryover, sensors, and guided workflows).
- Keep your Exocortex workflow (CLI-first, Zellij, Obsidian, etc.) intact by wiring Hermes' outputs and memories into your PKM setup.

What you already have (context from your memories)

- Hermes gateway and agent components are present, with the ability to select provider/model (e.g., "You can now select a provider and model: h…").
- Hermes skills, cron, routing, and Pieces LTM memory are already configured and in use.
- Claude Code CLI and Gemini CLI are used directly today, bypassing Hermes orchestration.

Minimal starter config

```yaml
# hermes/providers/claude.yaml (or inline in config.yaml)
kind: provider
name: claude
base_url: https://api.anthropic.com/v1
auth:
  type: token
  token: ${CLAUDE_API_KEY}
default_model: claude-sonnet-4
models:
  claude-sonnet-4:
    id: anthropic/claude-sonnet-4
    max_tokens: 8192
    temperature: 0.2

---
# hermes/providers/gemini.yaml
kind: provider
name: gemini
base_url: https://generativelanguage.googleapis.com/v1beta/openai
auth:
  type: token
  token: ${GEMINI_API_KEY}
default_model: gemini-2.5-flash
models:
  gemini-2.5-flash:
    id: google/gemini-2.5-flash-preview-05-06
    max_tokens: 8192
    temperature: 0.2
```

Wiring summary

```
User prompt —> Hermes gateway —> router (task classifier) —> provider adapter (Claude | Gemini) —> response —> Pieces LTM —> Obsidian/wiki
```

Practical patterns to adopt next

1. Create a `hermes run task "<task>" --provider claude` alias (e.g., `hc`) to keep CLI ergonomics.
2. Use a Zellij layout that launches Hermes in one pane and Claude/Gemini CLI in another, wiring the panes together via Hermes's task file or a named pipe.
3. Set Pieces LTM to ingest both Hermes session logs and Claude/Gemini CLI outputs so everything compounding into your PKM.
4. Define tiered routing rules in Hermes config (local models for fast autocomplete, Claude for deep reasoning, Gemini for multi-modal).
5. Add a "provider model" sensor to Hermes that exposes current provider + model to your status bar / prompt.

## Asset 2 (Pieces: bab757b9-71eb-497b-a309-b2b97dd40f12)

Tailoring an Integration Plan

I'm planning to create a tailored integration plan for the user's environment, which shows that the Hermes "ai.hermes.gateway" service is in place. I'll suggest configuring it within their Ghostty/Zellij setup by starting with their long-term memories and project context.

I'll note that Hermes is already present in their environment, as indicated by the logs showing provider selections. I want to reference the Hermes Masterclass video and summarize that Hermes can effectively work with Claude and Gemini through provider adapters.

Next, I'll outline actionable steps, provide example configuration snippets, and set clarifying questions to refine the approach further.

## Asset 3 (Pieces: 9bb443c9-9cbd-40af-ac17-cde84d20b553)

Providing Integration Steps

I'm outlining recommended patterns, starting with creating a "route-task.md" to map the skill chain.

In Step 5, I'll focus on security by managing API keys through environment variables or a secret store, restricting tokens, and monitoring usage.

For Step 6, I'll provide example commands, like "hermes run task 'summarize this doc' --provider claude."

In Step 7, I need to ensure prompts are unified and integrate memory "Pieces" for session management.

For Step 8, I'll outline potential compatibility issues with Claude and Gemini.

Finally, in Steps 9 and 10, I'll suggest creating provider wrappers and provide a checklist for next steps.

## Asset 4 (Pieces: c867f159-ae8e-476c-8da5-25926a26f7b5)

Steps for Hermes Integration

I'm considering how Hermes employs the "providers" concept, reflected in the "providers/public" section of the config.

In Step 2, I need to install and configure the CLI; I'll restart the "ai.hermes.gateway" service and use CLI commands like "hermes provider set claude" or "hermes model Claude-3" to select the provider.

Step 3 involves building skills, potentially by creating a "Claude" skill wrapper to call Claude's API via Hermes or utilizing a multi-provider approach.

Lastly, in Step 4, I'll implement "compounding sessions" for memory transfer between Claude and Gemini.

## Asset 5 (Pieces: ef0b7cf3-f2a6-4f46-99c7-8d01d9af5fc9)

Creating a Setup Guide

I'm drafting a step-by-step guide for integrating providers with Hermes.

First, the prerequisites include ensuring Hermes is installed along with Docker Compose or Kubernetes. It's essential that the Hermes gateway can support multiple providers and that I have the necessary API keys for Claude and Gemini, along with proper network allowances and existing provider modules.

For Step 1, I'll update the Hermes configuration by editing `hermes/config.yaml` to include Claude and Gemini as providers, complete with their models, endpoints, and authentication tokens.

## Asset 6 (Pieces: 02bf7ea4-d449-4977-bd64-f07096475b59)

Structuring Hermes Integration

I'm thinking about how Hermes can use multiple providers through a gateway to select both provider and model. First, I need to clarify the goals, aiming for Hermes to orchestrate LLMs like Claude and Gemini while utilizing features such as stateful sessions, memory, and task routing. Then, I'll propose architecture options where Hermes acts as an orchestration layer that integrates these models effectively through skill modules, context storage, and routing tasks.

## Asset 7 (Pieces: ff5a8d3b-41b3-47c4-8c8d-30396e59c12f)

I want to improve my hermes agent usage. Currently I just use claude code in the cli or gemini cli. How can I incoporate hermes and use claude of gemini but have the benefits of hermes
