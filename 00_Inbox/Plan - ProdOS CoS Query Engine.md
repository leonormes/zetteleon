---
created: 2026-08-18T16:46:00+00:00
modified: 2026-08-18T16:46:00+00:00
permalink: llmeon/00-inbox/plan-prodos-cos-query-engine
title: "Plan — ProdOS CoS Query Engine"
tags: [prodos/plan, state/planning, domain/prodos]
type: plan
---

# Plan: ProdOS CoS Query Engine (LLM-Backed Chief of Staff)

## The Vision

A single, unified protocol where the LLM sweeps **all your inboxes**, aggregates open loops, prioritises them, and pushes ADHD-optimised starter tasks to Todoist — **one pass, zero context switching**.

| Inbox | Data Source | What It Contains |
|---|---|---|
| Teams Calendar | Events API / calendar scan | Meetings, deadlines, time blocks |
| Pieces LTM | REST API (`:39300/messages`) | Ambient context, recent work fragments |
| Fitfile Email | ?? (needs scoping) | Actionable emails, requests, decisions |
| Jira (FTFL board) | `cos-jira-fetch.py` (REST API) | Open tickets, sprint work, blockers |
| GitKraken / GitLab | `gk pr list` (gk CLI) | Open MRs needing review, CI status |
| Todoist | Todoist REST API v1 | Stale starter tasks, unprocessed captures |
| Obsidian vault | `obsidian files` / MCP | Unprocessed inbox notes, open HEAD notes |

---

## Current State (18 Aug 2026)

### What Already Exists

| Component | Status | Notes |
|---|---|---|
| `cos-work-review` skill | ✅ Production | Periodic Jira + GitLab + Pieces scan. Writes SoT. 7-step workflow. |
| `routine-cos-synthesis.md` | ✅ Production | Older simpler CoS run routine (Jira → Teams → Operon → Todoist → journal). |
| `gk` CLI for GitLab/Jira | ✅ Working (today) | Jira (4), GitKraken/GitLab (4), Todoist (3) gathered in today's runs. |
| 2 successful runs today | ✅ Proven | 12:26 and 12:57 — both pushed starter tasks to Todoist. |
| HEAD note (unification question) | ✅ Open | `20_Thinking/21_Workbench/HEAD - How to unify the CoS Query Engine.md` |

### What's Missing

| Gap | Impact | How to Close |
|---|---|---|
| Teams Calendar not polled | Meeting-aware prioritisation missing | AppleScript / `icalbuddy` / calendar API |
| FF Email not checked | Actionable email items missed | `mutt` / `neomutt` / Gmail API / Apple Mail scripting |
| Pieces query not unified in cron flow | Ambient context not always gathered | Wire `cos-pieces-scan.py` into the sweep |
| No prioritisation engine | Flat list, no ranking | LLM-rerank: urgency × impact × effort |
| Todoist push not asked first | AGENTS.md requires permission | Add confirmation step or auto-push with `[Y/N]` |
| No single trigger command | User has to know which skill to call | Create `"cos sweep"` or daily cron trigger |
| Obsidian inbox (00_Inbox/) not checked | Raw captures sit unprocessed | Scan modified files in 00_Inbox for new entries |

---

## Proposed Architecture: Gather → Synthesise → Prioritise → Push → Log

```
┌─────────────────────────────────────────────┐
│               1. GATHER                      │
│  ┌──────┬──────┬──────┬──────┬──────┬──────┐ │
│  │Jira  │GitLab│Pieces│Todoist│Cal   │Email│ │
│  └──────┴──────┴──────┴──────┴──────┴──────┘ │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│           2. SYNTHESISE                      │
│  Deduplicate · Cross-reference · Collapse    │
│  → Unified Open Loops Register              │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│          3. PRIORITISE                       │
│  Urgency × Impact × Effort × Staleness      │
│  → Top 3-5 Next Actions                     │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│          4. GENERATE + PUSH                  │
│  ADHD Starter Tasks (verb + object + timebox)│
│  → Push to Todoist Today / Work              │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│             5. LOG                           │
│  Daily journal entry + SoT upsert           │
│  → 01_journals/ + SoT - Work Open Loops     │
└─────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: Wire Existing Components into One Trigger (1-2 sessions)

**Goal:** One `"cos sweep"` command that runs all existing pipelines in sequence.

**Tasks:**
1. Create unified `cos-sweep` Hermes skill that calls existing routines in order:
   - `cos-work-review` (Jira + GitLab + Pieces)
   - Todoist inbox scan (stale tasks, unprocessed captures)
   - Obsidian 00_Inbox scan (new .md files modified in last 24h)
2. Add prioritisation step: LLM ranks items by urgency × impact × effort
3. Add starter task generation: verb + object + ≤15m timebox
4. Add journal append with summary
5. Test a complete end-to-end run

**Deliverable:** `"cos sweep"` or `cos-run` cron job fires → output appears in chat.

### Phase 2: Add Calendar & Email Awareness (2-3 sessions)

**Goal:** CoS knows about meetings and email obligations.

**Tasks:**
1. Add Teams/Apple Calendar polling via `icalbuddy` or EventKit
2. Add email inbox scan — determine best approach:
   - **Option A:** `neomutt` + IMAP for Fitfile email
   - **Option B:** Gmail API (if Fitfile uses G Suite)
   - **Option C:** Apple Mail scripting
3. Surface time-conflicts: "You have 3 meetings today, total 4h — remaining work window is 3h"
4. Detect email-embedded action items ("Can you review X by EOD?")

**Deliverable:** CoS reports calendar pressure + surfaces email action items.

### Phase 3: Decision — Build vs Wire (Determined this Phase)

**The unresolved tension from the HEAD note:**

| Approach | Pros | Cons |
|---|---|---|
| **Wire MCP tools** (existing Hermes pattern) | Zero new code, uses proven skill infrastructure | Each new source needs a new tool/wiring; brittle to tool changes |
| **Build custom script** (Python orchestrator) | Single binary, deterministic, easier to test, can parallelise | New code to maintain; outside the skill ecosystem |
| **Hybrid** — shell script wraps MCP calls + Python fetchers | No new infra; leverages both patterns | Ugly but pragmatic |

**Recommended:** Start with **wiring existing skills** (Phase 1). If the command chain gets too long or fragile, **switch to a single Python orchestration script** that calls each data source API directly and pipes results to the LLM for synthesis.

### Phase 4: Productionise (Ongoing)

**Tasks:**
1. Add cadence-based cron jobs (morning sweep, lunch sweep, EOD sweep)
2. Add "what's changed since last run" delta detection (already partially done in `cos-work-review` with Tier 1/2 shortcuts)
3. Add ADHD starter task format verification (verb + object + timebox)
4. Add "push to Todoist" confirmation gate (per AGENTS.md — ask before pushing)

---

## Starter Task Format Standard

Every generated task MUST follow this template:

```
<action verb> + <object> + <timebox> [≤15m]
```

Examples:
- `Open MR !2404 and check the CI pipeline status. [5m]`
- `Run terraform plan in fitfile-non-production-infrastructure/fitapp-demo-ukw/. [10m]`
- `Read the PR summary for InsightFILE MR 2405. [8m]`
- `Open `HEAD - How to unify the CoS Query Engine.md` and write a 3-bullet outline. [5m]`

Rules:
- Each task is ≤15 minutes
- First word is a concrete physical verb (Open / Run / Read / Draft / Check / Message)
- Contains the exact path, URL, or file reference
- Timebox in brackets at the end

---

## Verification

After Phase 1, a successful run produces:

```
[CoS Sweep — 16:46] ✓ 4 inboxes swept (Jira:4, GitLab:4, Todoist:3, Obsidian:1)
                        → 3 starter tasks pushed to Todoist Work
                        → Journal updated
```

---

## Key Constraints (from AGENTS.md + vault rules)

| Rule | Impact on CoS |
|---|---|
| Never write to 00_Inbox as agent | CoS reads 00_Inbox but generates elsewhere (plan note is an exception directed by user) |
| Never push Todoist without asking first | CoS must ask `[Y/N]` before pushing — or this rule needs amending for the CoS use case |
| Never edit body prose of human HEAD notes | CoS can create new HEAD notes but not rewrite existing ones |
| `gk whoami` expiry blocks GitLab/Jira | CoS must detect stale gk auth and fall back to direct Jira API (`cos-jira-fetch.py`) |
| Pieces REST API is the reliable cron path | CoS uses `cos-pieces-scan.py` with the REST API, not CLI/MCP |
| Journal append uses read-combine-write, not patch | CoS appends to daily journal via Python in terminal |