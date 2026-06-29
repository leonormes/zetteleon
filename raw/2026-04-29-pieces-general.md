---
created: 2026-04-29 08:34:47+00:00
modified: 2026-05-26 11:43:52+00:00
pieces_ids:
- 18052b1a-3d8b-43cc-8b02-f0bac29324f5
- 3a5452ee-f7cc-45fe-b1d1-c302d2736975
- 4b15e9a5-1ec5-444f-86ac-552acf466ffd
- 4b491f1c-b2b7-4e11-8bd5-318ca651967b
- a0f6c57f-f04a-4e3c-937b-e307b1a296d1
- abb574af-d887-4611-bbdf-5b15aabf7339
- b8cb073f-dd7b-4efa-bd4d-6ae1e94e7a3c
- c29b18d3-cefa-4937-9987-62546deaccfe
- dd2b39c3-3e7a-4e4b-867e-56235b825c43
source: pieces-ltm
tags:
- pieces
- raw
title: 2026-04-29-pieces-general
permalink: llmeon/raw/2026-04-29-pieces-general
---

Asset: `3a5452ee-f7cc-45fe-b1d1-c302d2736975`

Captured: 2026-04-29T08:22:33.444170Z

```
Now I'm drafting a comprehensive, structured prompt they can paste directly into Claude Code that covers all these changes systematically.
```

---

Asset: `4b491f1c-b2b7-4e11-8bd5-318ca651967b`

Captured: 2026-04-29T07:56:55.335488Z

```
The real insight is that Zellij layouts become the control plane — each work mode gets a preconfigured workspace that launches the right combination of tools. I'm mapping out a week-long iteration plan starting with Zellij as the foundation, then layering in Hermes as the persistent orchestrator, followed by cost-tiered routing logic, and finally connecting everything through MCP. The unified concept is that Zellij handles workspace orchestration while the tiered routing system ensures tasks land on the most appropriate and economical tool for the job.
```

---

Asset: `abb574af-d887-4611-bbdf-5b15aabf7339`

Captured: 2026-04-29T07:56:53.709509Z

```
For Leon's design, I'm thinking he's a deterministic reasoner who wants clear, predictable routing rather than vague "vibe coding" — the system needs to be intentional and cost-conscious, routing cheaper tasks to local or budget models while keeping things in small, iterative steps rather than a big bang approach. I'm sketching out a tiered routing architecture where tasks flow to the right tool based on cost, capability, and context: local models like Ollama for quick lookups and summarization, cheaper cloud options for medium-complexity work, and premium models only when needed.
```

---

Asset: `c29b18d3-cefa-4937-9987-62546deaccfe`

Captured: 2026-04-29T07:56:37.049435Z

```
His tools:
1. Ollama (local models + cloud subscription) — runs qwen3.5, gemma4, kimi-k2.6 etc.
2. Hermes Agent (just installed, via Ollama) — autonomous agent with skills, cron, gateway, memory
3. Claude (paid subscription) — likely Claude Code CLI + Cursor integration
```

---

Asset: `b8cb073f-dd7b-4efa-bd4d-6ae1e94e7a3c`

Captured: 2026-04-29T07:56:30.432795Z

```
Leon is asking me to help him build a unified, incremental workflow that ties together his diverse LLM tooling. Let me inventory what he has and what I know from his memories, then build a practical, iterative plan.
```

---

Asset: `a0f6c57f-f04a-4e3c-937b-e307b1a296d1`

Captured: 2026-04-29T07:56:12.643184Z

Updated: 2026-04-29T08:22:19.399546Z

```
I have installed hermes. I use lots of different llm tools. I want to build a unified single workflow that adapts to different requirements. I have ollama, I pay for claud and gemini and ollama cloud and pieces for developers ltm and gemini cli and cursor. I have zellij for managing workspaces as I can program start scripts for it. How can I use these tools via agent harnesses and create automated agents for different tasks that I can run easily? How do I combine all the tools into a unified system that is cost effective and powerful? Suggest ideas and build a plan we can start iterating on. We don't need to do a big finished system in one go, just small steps I can try each day to build it up
```

---

Asset: `dd2b39c3-3e7a-4e4b-867e-56235b825c43`

Captured: 2026-04-29T07:03:58.340159Z

Updated: 2026-04-29T07:05:42.957689Z

```
Message Saved As Workstream Summary
```

---

Asset: `4b15e9a5-1ec5-444f-86ac-552acf466ffd`

Captured: 2026-04-29T07:02:55.400008Z

Updated: 2026-04-29T07:03:06.136714Z

```
this needs to be a platform and application security. BOth quartly and sprint allocation.
```

---

Asset: `18052b1a-3d8b-43cc-8b02-f0bac29324f5`

Captured: 2026-04-29T06:39:24.888349Z

```
Creating a clear action list

I need to mention the clip titled "Everybody has 2 topics to present for the future roadmap" recorded at 7:37 AM, ensuring it's in 12-hour time format. I also have to follow guidelines about hyperlinking files — which currently, I don’t have. Instead, I'll hyperlink memories with relevant URLs like the OHDSI omock and Miro board. My goal is to provide a succinct action list that anyone can easily copy and follow.
```

---