---
created: 2026-05-26T13:49:47+00:00
modified: 2026-08-13T10:53:25+00:00
permalink: llmeon/30-library/200-projects/how-to-use-the-prod-os-workflow
project_category: prodos
project_name: ProdOS
project_status: active
title: How to Use the prodOS Workflow
type: null
---

Your ProdOS (Productivity Operating System) has two distinct but connected faces: the personal thinking loop (daily mental processing) and the work automation loop (Jira/Teams/Todoist via Hermes Gateway). Here's how each works.

---

## Part 1—The Thinking Stream (Daily Personal lOop)

This is the "RAM" of the system—a low-friction loop for converting raw mental noise into action or structured knowledge. The governing rule is the Rule of Zero Toil: if it feels like "organising", stop. The loop is for _thinking and doing only_.

### The CRPE Cycle (Your Core lOop)

1. CAPTURE—Dump everything raw into your Daily Note (`01_journals/`) or `00_Inbox/dump.md`. No formatting required. Raw text only.
2. REFINE—If you're stuck or it's getting complex, create a `HEAD` note in `20_Thinking`. This is temporary working space.
3. PROCESS (the 120-second loop)—For each item ask three questions:
   - Goal: What is the single outcome?
   - Block: What is the exact friction?
   - MVA: What is the next physical step (<120 seconds)?
4. EXIT—Route the output:
   - Action? → Todoist (task with `@work` label, project: "Work")
   - Fact? → SoT Note in `30_Library/SoT/`
   - Skill/Project? → Hangar / Project Note in `200_projects/`
   - Trash? → DELETE the note

### The Guardrails

- NO FOLDERS in `20_Thinking`—dump everything there
- NO POLISHING—messy is fine
- NO STORAGE—if not actionable in 24h, delete

---

## Part 2—The Autonomous Action System (Agent-driven lOop)

The Protocol - Autonomous Action System is the agentic version of the loop—your AI Chief of Staff (Hermes) handles the organising so you don't have to.

### The Toolset

- Obsidian MCP—ground truth for thinking and knowledge (`/Volumes/DAL/Zettelkasten/LLMeon`)
- Todoist MCP—ground truth for physical actions and deadlines
- Hermes Gateway (v0.14.0, model: `owl-alpha`)—the active orchestrator / CoS

### The Integrated Workflow

1. Capture phase (you)—Dump everything into `00_Inbox/dump.md`. No formatting.
2. Refine phase (Hermes)—Triggered by saying `"Process my dump"` or `"I'm overwhelmed"`:
   - Reads `dump.md`
   - Identifies Projects vs. Next Actions
   - Calls Todoist MCP to create/update tasks
   - Calls Obsidian MCP to create/update project notes
3. Synthesis phase (automated)—The `Daily Synthesis` workflow runs on a cron schedule:
   - Capture: Queries Pieces LTM for today's activity
   - Distil: Filters raw data into `/raw` folder in the vault
   - Compound: Updates `/wiki` entity pages (people, projects, concepts) with backlinks to Pieces memory IDs
4. CoS Review—Hermes periodically runs a Chief of Staff review to surface open loops across Jira, Teams, and Todoist

---

## Part 3—The Work Integration Loop (Set up Today, 26 May)

This was configured this morning using the Hermes `/goal` prompt. The data flow is:

```
Jira (FTFL project, assignee = currentUser(), poll: 30m)
    +
Microsoft Teams (meetings + chat)
    +
Pieces LTM (sensory/overview layer)
         ↓
Hermes Gateway (CoS review)
         ↓
Obsidian SoT (updated outstanding work)
         ↓
Todoist (synced actions, label: @work, project: Work)
```

To trigger a CoS review manually, open Hermes TUI and use the `/goal` prompt that was generated this morning (saved in your vault at `raw/2026-05-26-pieces-prodos-workflow-design`).

---

## Quick reference—entry Points by Energy Level

| Energy | Entry point | What to do |
|---|---|---|
| High | Hermes TUI → `/goal` | Full CoS review: Jira + Teams + Todoist |
| Medium | Daily Note → CRPE loop | Process what's in your head |
| Low | `dump.md` | Brain dump only; say "Process my dump" later |
| Any | `"I'm overwhelmed"` → Hermes | Agent takes over routing |

---

## Open Questions from Your Design Session (Not yet rEsolved)

- Has the Hermes `/goal` prompt been executed yet, or only generated?
- Microsoft Teams MCP connector—is there a working connector, or does this still need to be built?
- Todoist OAuth token—is `op://Personal/todoist-api/credential` already configured in 1Password?
