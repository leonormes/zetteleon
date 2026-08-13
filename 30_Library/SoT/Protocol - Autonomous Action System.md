---
aliases: [Agent GTD, Autonomous Action, Todoist MCP Integration]
conformant: false
created: 2026-04-02T11:00:00+00:00
last-synthesis: 2026-04-02
modified: 2026-08-13T10:53:38+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/protocol-autonomous-action-system
source_of_truth: true
status: evergreen
synthesis-count: 1
tags: [adhd, gtd, llm, prodos, system/protocol, todoist]
title: Protocol - Autonomous Action System
trust-level: stable
type: protocol
---

## Logic Map

Objective: To eliminate the cognitive load of "managing the system" by using an LLM-Agent to organize, route, and prompt the user.

Dependencies:

- Obsidian MCP: Ground truth for thinking and knowledge.
- Todoist MCP: Ground truth for physical actions and deadlines.
- Gemini CLI: The active orchestrator (Chief of Staff).

## The Algorithm (MVAs)

### 1. The Capture Phase (Human)

- MVA: Dump everything into `00_Inbox/dump.md`.
- Constraint: No formatting required. Just raw text.

### 2. The Refine Phase (Agent)

- Trigger: User says "Process my dump" or "I'm overwhelmed."
- Action Sequence:
    1. Read `00_Inbox/dump.md`.
    2. Identify Projects vs. Next Actions.
    3. Use `todoist_add_task` to create projects and actions.
    4. Move processed content to `99_Archive/Processed_By_Agent/`.
    5. Present a "Clean Runway" (top 3 actions).

### 3. The Context Restoration Phase (Agent)

- Trigger: Start of a new session.
- Action Sequence:
    1. Use `todoist_search` for tasks due 'today'.
    2. Output: "Welcome back. Today's priority is [X]. Here are your next 3 actions."

### 4. The Health Check (Agent)

- Trigger: Weekly review or user request.
- Action Sequence:
    1. Use `todoist_get_project_health` (or equivalent).
    2. Flag stalling projects or overdue items with a "Next Test" proposal.

## Unit Test

1. Run `Process my dump` with a test entry in `00_Inbox/dump.md`.
2. Verify task appears in Todoist.
3. Verify content is moved to Archive.
