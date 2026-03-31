---
aliases: [Autonomous Action, Agent GTD, Todoist MCP Integration]
created: 2026-03-31T13:00:00+00:00
modified: 2026-03-31T13:00:00+00:00
status: head
tags: [adhd, gtd, llm, system/protocol, todoist]
title: HEAD - Protocol - Autonomous Action System (ProdOS Agent)
type: head
---

## Objective
To eliminate the cognitive load of "managing the system." The user captures; the Agent organizes, routes, and prompts.

## The Toolset
- **Obsidian MCP:** Ground truth for thinking and knowledge.
- **Todoist MCP:** Ground truth for physical actions and deadlines.
- **Gemini CLI:** The active orchestrator (The Chief of Staff).

## The Integrated Workflow

### 1. The Capture Phase (Human)
- **Action:** Dump everything into `00_Inbox/dump.md`.
- **Constraint:** No formatting required. Just raw text.

### 2. The Refine Phase (Agent)
- **Trigger:** User says "Process my dump" or "I'm overwhelmed."
- **Action:** 
    1. Read `00_Inbox/dump.md`.
    2. Identify Projects vs. Next Actions.
    3. **Todoist MCP Call:** `add-tasks` to create projects and actions.
    4. **Obsidian MCP Call:** Append a "Processed" header to `dump.md` or move the content to `99_Archive/Processed_By_Agent/`.
    5. **CLI Output:** Present a "Clean Runway" (top 3 actions).

### 3. The Context Restoration Phase (Agent)
- **Trigger:** Start of a new session.
- **Action:** 
    1. **Todoist MCP Call:** `find-tasks-by-date(startDate='today')`.
    2. **CLI Output:** "Welcome back. Today's priority is [X]. Here are your next 3 actions."

### 4. The Health Check (Agent)
- **Trigger:** Weekly review or user request.
- **Action:** 
    1. **Todoist MCP Call:** `get-project-health`.
    2. **CLI Output:** Flag stalling projects or overdue items with a "Next Test" proposal.

## Next Action for Implementation
- [ ] Finalize authentication for Todoist MCP (Ensure `TODOIST_API_TOKEN` is persistent).
- [ ] Test the `Process my dump` command with the current `00_Inbox/dump.md`.
- [ ] Update `GEMINI.md` to include the "Autonomous Action" mandate.
