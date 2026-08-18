---
title: Nous Research Ships Bot Mode for Hermes Agent, Turning Agent Profiles Into
  a Roster of Named Bots
source: https://www.marktechpost.com/2026/08/17/nous-research-hermes-bot-mode/
captured: 2026-08-18T16:43:05+01:00 2026-08-18T16:43:05+01:00
status: processing
tags:
- input
type: head
permalink: llmeon/00-inbox/head-nous-research-ships-bot-mode-for-hermes-agent-turning-agent-profiles-into-a-roster-of-named-bots
---

## Nous Research Ships Bot Mode for Hermes Agent, Turning Agent Profiles Into a Roster of Named Bots

- [Editors Pick](https://www.marktechpost.com/category/editors-pick/)
- [Agentic AI](https://www.marktechpost.com/category/editors-pick/agentic-ai/)
- [AI Agents](https://www.marktechpost.com/category/editors-pick/ai-agents/)
- [Technology](https://www.marktechpost.com/category/technology/)
- [AI Shorts](https://www.marktechpost.com/category/technology/ai-shorts/)
- [Artificial Intelligence](https://www.marktechpost.com/category/technology/artificial-intelligence/)
- [Applications](https://www.marktechpost.com/category/technology/artificial-intelligence/applications/)
- [Language Model](https://www.marktechpost.com/category/technology/artificial-intelligence/language-model/)
- [Large Language Model](https://www.marktechpost.com/category/technology/artificial-intelligence/large-language-model/)
- [New Releases](https://www.marktechpost.com/category/editors-pick/new-releases/)
- [Open Source](https://www.marktechpost.com/category/technology/open-source/)
- [Tech News](https://www.marktechpost.com/category/tech-news/)

[Nous Research](https://nousresearch.com/) has shipped **Bot Mode** for [Hermes Agent](https://github.com/NousResearch/hermes-agent), its MIT-licensed open source agent. Bot Mode replaces the single-agent session list with a roster of named bots. Each bot is a real Hermes profile, with its own chat, memory, skills, and pinned model. Bots message each other through a persistent Agent Inbox and hand work off by `@mention`. The feature launched as a [one-day public beta plugin](https://x.com/Teknium/status/2088003994904113614) from co-founder Teknium. It now ships bundled and default-on inside Hermes Desktop, in [Hermes Agent v0.20.3](https://github.com/NousResearch/hermes-agent/releases).

## Is it deployable?

**Yes — today, on a desktop, at no license cost.** [Bot Mode](https://github.com/NousResearch/Hermes-Bot-Mode) shipped first as a one-day public beta plugin. It is now bundled and default-on inside Hermes Desktop, under Settings → Plugins. Both [Hermes Agent](https://github.com/NousResearch/hermes-agent) and the plugin are MIT licensed.

**Which companies**: Solo builders, startups, and small-to-mid engineering teams can adopt it immediately. Enterprises should treat it as a workstation tool, not managed infrastructure. There is no admin console, no SSO, no central audit log, and no policy layer. Regulated buyers will need their own controls around it.

**Industries**: Software engineering, AI research labs, technical media and content operations, developer relations, quantitative research, and IT operations.

**Applications**: A research bot pinned to a reasoning model beside a writing bot on a cheaper one. Scheduled inbox digests and nightly reports. Per-project agents that never leak context into each other. Handoff chains where a scout, a reviewer, and a publisher pass work by `@mention`.

## How it works under the hood

The interesting point here is that a bot **is** a Hermes profile. Each one lives under `~/.hermes/profiles/<name>/` with isolated config, memory, skills, credentials, and chat history. The plugin is a user interface over a primitive Hermes already shipped.

That choice keeps the surface area small. Creation and editing ride the `profiles.*` gateway RPCs: `list`, `create`, `describe`, `configure`. Avatar generation uses the `image.generate` RPC over local and remote gateways. Routines are ordinary Hermes cron jobs, namespaced `[bot:<name>] <routine>`. They still appear in `hermes cron list`.

Bot-to-bot messaging is the same story. Every bot has a persistent Agent Inbox conversation. Messages between bots are real CLI handoffs: `hermes -p <bot> chat -c "Agent Inbox" -q "..."`. They arrive with attribution, and each bot’s SOUL.md teaches the reply protocol. Typing `@researcher have a look at this` makes the active bot hand off and report back.

## Configuration you actually get per bot

The New Agent dialog asks for name, title, and description. An Advanced disclosure opens the full profile config. You can clone an existing profile, pin a provider and model, write a custom SOUL.md, or skip skills. Right-clicking a bot exposes Edit Profile, which edits the live profile. That covers per-skill and per-toolset enablement, the model pin, and the SOUL.md. Duplicate clones config, skills, SOUL.md, memory, and appearance.

Avatars are geometric faces in seven shapes and ten colors. You can also upload an image, generate a portrait, or attach a pixel pet. The eyes scan while the bot works.

## From one-day beta to bundled default

The rollout was fast. Teknium ran a one-day public beta through the standalone plugin and asked for bug reports. He committed to folding it into the main desktop app. That has now happened. Per hermes-agent PR #87886, Bot Mode is bundled and default-on, and the standalone repository is archived. Development continues in-tree at `apps/desktop/src/plugins/hermes-bots/`. The bundled plugin and its core teammate protocol landed in [Hermes Agent v0.20.3](https://github.com/NousResearch/hermes-agent/releases).

The in-tree version added capability the beta did not have. Groups organise the roster into labeled sections that sync across machines. Group chats open a shared room for two to six bots. Your message triggers up to three serial rounds of member turns. Mentioned bots respond, everyone responds when nobody is mentioned, and each bot replies briefly or passes. A multi-source roster pulls bots from every connection under Settings → Connections.

## Interactive explainer

## Key Takeaways

- Bot Mode turns each Hermes profile into a named bot with its own chat, memory, and model.
- A bot is just a profile at `~/.hermes/profiles/<name>/` — no new storage layer.
- Bots message each other through real CLI handoffs into a persistent Agent Inbox.
- Group chats coordinate two to six bots over a maximum of three serial rounds.
- It shipped from one-day beta to bundled default-on Desktop plugin in Hermes Agent v0.20.3.
![](https://x.com/i/status/2089429432612147572)

---

Check out the **[Hermes-Bot-Mode repository](https://github.com/NousResearch/Hermes-Bot-Mode), [hermes-agent](https://github.com/NousResearch/hermes-agent), [Hermes Agent site](https://hermes-agent.nousresearch.com/), [Hermes Agent docs](https://hermes-agent.nousresearch.com/docs/),** and **[Teknium’s announcement](https://x.com/Teknium/status/2088003994904113614)**.Also, feel free to follow us on **[==Twitter==](https://x.com/intent/follow?screen_name=marktechpost)** and don’t forget to join our **[150k+ML SubReddit](https://www.reddit.com/r/machinelearningnews/)** and Subscribe to **[our Newsletter](https://magic.beehiiv.com/v1/f5e63dd4-5653-4f09-83e2-321a8b1ba526?email={{email}})**. Wait! are you on telegram? **[now you can join us on telegram as well.](https://t.me/machinelearningresearchnews)**

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? **[==Connect with us==](https://forms.gle/wbash1wF6efRj8G58)**