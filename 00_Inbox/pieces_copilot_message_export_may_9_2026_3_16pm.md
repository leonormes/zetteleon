*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Saturday May 9, 2026 - 3:16 PM*
---
# Why Hermes Frustrated You (and How to Fix It)

Your frustration is completely valid, Leon. Looking at your sessions from Thursday and Friday, I can identify several compounding problems that turned what should have been a clean orchestration experiment into a thrashing mess. The good news: you actually diagnosed most of these issues yourself in your [Gemini conversation on Thursday](https://gemini.google.com/app/de7a8fa29b794105) — but then jumped straight into a complex Jira task before applying the fixes.

---

## What Went Wrong: A Post-Mortem

### 1. **You gave a weaker model a harder job than Claude gets**
Your Jira session (~4:22 PM Friday) ran on `kimi-k2.6:cloud` and the earlier session used `qwen3.5:latest`. These models were asked to:
- Navigate MCP proxy discovery
- Handle Jira's `additional_fields` validation quirks ("Clinical Safety Considered is required")
- Distinguish between chezmoi source paths and live `~/.config` paths
- Manage batch issue creation with epic linking

That 37-minute session produced **88 messages with 84 tool calls and only 3 user messages** — the agent was in a pure thrash loop. Claude Code would have solved this in 3-4 turns because it has vastly better tool-use reasoning. You essentially gave the intern a senior architect's debugging task.

### 2. **Tool overload crushed the local models**
Your Gemini conversation on Thursday at ~1:25 PM nailed this: *"Hermes presents all 47+ tools to Qwen every turn. For a local model, this 'cognitive load' is heavy."* Your sessions consistently showed **29-35 tools and 92-94 skills** loaded. Every turn, the model has to reason about which of those to use. For models like Qwen 3.5, this is debilitating.

### 3. **No incremental validation**
You went from "just configured mcp-proxy in chezmoi" straight to "create a Jira ticket with epic links, subtasks, custom fields, and story point justifications." There was no intermediate step where you confirmed a basic `atlassian_jira_search` even worked cleanly.

### 4. **The SOUL.md routing protocol wasn't enforced**
You designed a beautiful orchestration protocol in the Gemini session — tiered routing, plan-first workflow, delegation to Claude Code for heavy work — but the Hermes sessions show the agent attempting to do everything itself, including complex Jira field debugging.

---

## How to Build Reliable Orchestration: Small Experiments First

Here's a staged approach, from trivial to complex, where each stage **must pass before moving on**:

### Stage 1: Prove the Plumbing (10 minutes)

Run Hermes with a **thin profile** as your Gemini conversation suggested:

```bash
hermes --profile terminal,read_file,write_file,plan
```

Give it ONE trivial task:
```
Read ~/.hermes/config.yaml and tell me how many MCP servers are configured.
```

**Pass criteria:** Completes in < 30 seconds, correct answer, no tool thrashing.

### Stage 2: Prove One MCP Tool Works (10 minutes)

Load *only* the MCP tools:
```bash
hermes --tools mcp-proxy
```

Give it ONE atomic MCP call:
```
Use atlassian_jira_search to find issue FTFL-652. Return only the summary and status.
```

**Pass criteria:** Single tool call, correct result, < 60 seconds.

### Stage 3: Prove Plan Mode Works (15 minutes)

Start with `/plan` mode and give it a *slightly* complex task:
```
/plan
Create a Jira Task in project FTFL with summary "Test orchestration" and description "Validation ticket - delete after test". Write the plan only, do not execute.
```

**Pass criteria:** Writes a clean plan to `hermes/plans/`, does NOT attempt to call the Jira API.

### Stage 4: Prove Delegation Works (15 minutes)

Now test the actual routing concept — have Hermes delegate ONE thing:
```
Execute the plan in hermes/plans/[plan-file].md. Use only the mcp-proxy jira tool. Create the ticket with basic fields only — no custom fields, no epic links.
```

**Pass criteria:** Creates ticket successfully. If Jira throws a validation error (like the "Clinical Safety Considered" field), the agent stops and reports the error rather than looping for 84 tool calls.

### Stage 5: Build the Router Cockpit

Only after stages 1-4 pass cleanly should you implement the full tiered routing in SOUL.md:

```markdown
# Routing Protocol

You are the TRIAGE ORCHESTRATOR. You run on a cost-effective model.

## Rules
1. NEVER attempt complex coding, debugging, or multi-step API operations yourself.
2. For ANY task, first write a plan to hermes/plans/.
3. Classify each plan step:
   - **Tier 1 (Self):** File reads, simple searches, text formatting
   - **Tier 2 (MCP):** Single atomic API calls via mcp-proxy
   - **Tier 3 (Claude Code):** Architecture, debugging, complex logic
   - **Tier 4 (Gemini):** Web research, documentation lookup
4. If a Tier 2 call fails ONCE, stop and report. Do NOT retry with variations.
5. Maximum 5 tool calls per user message. If you exceed this, stop and ask.
```

The **critical addition** here is rule 4 and 5 — hard guardrails against the thrash loops you saw. Your Jira session made 84 tool calls trying to work around the `additional_fields` bug. A 5-call limit would have surfaced the error in under a minute.

---

## The Honest Assessment

| Capability | Hermes + Local Model | Claude Code CLI |
|---|---|---|
| Complex debugging | ❌ Thrashes | ✅ Excellent |
| Multi-step API orchestration | ⚠️ Needs guardrails | ✅ Reliable |
| Routing/triage of simple tasks | ✅ Its sweet spot | ❌ Overkill/expensive |
| Parallel subagent spawning | ✅ Designed for this | ❌ Not its model |
| Token cost for trivial tasks | ✅ Free (local) | ❌ Burns premium quota |

Hermes isn't meant to *replace* Claude Code — it's meant to be the **cheap dispatcher** that prevents you from burning Claude tokens on `cat ~/.hermes/config.yaml`. The mistake was asking it to be the executor of a complex task that even Claude would need careful prompting for.

**Your next session should be Stage 1 above. Nothing more.** Build trust in the plumbing before you build the cockpit.