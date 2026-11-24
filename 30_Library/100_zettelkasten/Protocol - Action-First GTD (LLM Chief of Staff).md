---
aliases:
  - Action-First GTD
  - Agent GTD
  - Autonomous Action
  - Dump Don't Organize
  - LLM Chief of Staff
  - Todoist MCP Integration
conformant: true
contrasts_with:
  - "[[SoT - Processing IS the Work]]"
created: 2026-02-11T11:40:00+00:00
merged_from:
  - "[[SoT - Cognitive Engineering Protocols]]"
modified: 2026-11-17T10:12:44+00:00
permalink: llmeon/30-library/so-t/protocol-action-first-gtd-llm-chief-of-staff
project_category: prodos
see_also:
  - "[[SoT - Execution Protocol (GTD & PARA)]]"
  - "[[Protocol - Vague-to-Action]]"
status: stable
tags:
  - gtd
  - llm
  - system/protocol
  - TheHuman/Health/ADHD
title: Protocol - Action-First GTD (LLM Chief of Staff)
type: protocol
upstream:
  - "[[SoT - PRODOS Core Specification]]"
prodos:
  kind: protocol
  protocol:
    applies_to:
      - inbox-triage
      - task-management
---

## Logic Map

- Objective: To bypass executive function fatigue by decoupling _Generation_ (Human) from _Organization_ (LLM).
- Dependency: Requires a "Daily Dump" note in Obsidian and a Task Manager (Todoist).
- Core Philosophy: "Dump, Don't Organize."

## The Algorithm

### 1. Rapid Capture (Generator Mode)

- Tool: Obsidian `Daily Dump` note.
- Action: Throughout the day, capture 100% of open loops (worries, ideas, tasks, status updates) without formatting or tagging.
- Rule: HUMAN WRITE, MACHINE READ. Do not attempt to organize while capturing.

### 2. The Handoff (Chief of Staff Protocol)

- Trigger: Once a day or when overwhelmed.
- Action: Copy the `Daily Dump` content and send it to the LLM with the Chief of Staff Prompt.
- Priority criterion: the `!!Priority` in the Todoist syntax below is not free judgement—triage it against [[The Time Management Matrix (Eisenhower Matrix)]]. Urgent+Important (Quadrant I) gets the highest priority; Important-not-Urgent (Quadrant II) still gets a real priority level so it survives against louder Quadrant I noise, rather than being deferred indefinitely; Urgent-not-Important (Quadrant III) gets a low priority or gets challenged as delegatable; Quadrant IV items should usually be dropped during extraction rather than turned into a Next Action at all.

#### The Prompt

> "I am sending you a raw brain dump. Act as my GTD Chief of Staff. Process this text into two lists for Todoist.
>
> List 1: Projects (The Definition of Done)
> Identify every 'Project' (multi-step outcome). For each, write a clear 'Definition of Done'—a physical state that must be true for the project to be closed (e.g., instead of 'Garden', write 'Outcome: New fence panels installed and painted').
>
> List 2: Next Actions (The Runway)
> Extract the immediate, physical next step for each project. Start every action with a verb. If a task takes less than 2 minutes, label it [DO NOW].
>
> Format for Todoist:
> Use Todoist Quick Add syntax into flat projects (#Work or #Personal) with minimal context labels (@computer, @home) and priority (!!Priority). Do not add dead metadata tags like @project or @next_action.
>
> Here is the dump:"

### 3. Execution (CD Mode)

- Tool: Todoist Board View (Kanban).
- Action: Paste the LLM output into Todoist.
- Workflow: Focus only on the "Next Actions" list. The LLM has already performed the cognitive work of defining "Done."

## Mode B: Agent-Run (MCP)

Consolidated 2026-11-09 from the former `Protocol - Autonomous Action System`, which ran the same dump-to-Todoist workflow with an agent instead of copy-and-paste. Sections above are Mode A (manual hand-off). Mode B removes the copy step.

- Dependencies: Obsidian MCP (ground truth for thinking and knowledge), Todoist MCP (ground truth for physical actions and deadlines), and an orchestrating agent acting as Chief of Staff (Hermes or Gemini CLI).
- Todoist target: Clarified actions go to the runway and unclarified items stay in the Inbox, as defined in [[SoT - GTD Action System]]. Actionability is location, not a tag.

### B1. Capture (Human)

- Dump everything into `00_Inbox/dump.md`. No formatting.

### B2. Refine (Agent)

- Trigger: "Process my dump" or "I'm overwhelmed."
    1. Read `00_Inbox/dump.md`.
    2. Separate Projects from Next Actions.
    3. Create them in Todoist through the Todoist MCP.
    4. Move processed content to `99_Archive/Processed_By_Agent/`.
    5. Present a "Clean Runway" (top 3 actions).

### B3. Context Restoration (Agent)

- Trigger: start of a new session.
- **Lead with Active ADHD Experiment**: Read `[[MOC - ADHD Experiments & Protocols]]` and any active `experiment` `HEAD` note in `20_Thinking/21_Workbench/` (e.g. `[[HEAD - Do 75m Deep Dive Sessions Outperform Granular Next Actions for ADHD?]]`). Open every CoS brief with an **Active ADHD Experiment** reminder: (1) the hypothesis being tested, (2) today's concrete behavioural test, and (3) what evidence would settle it. Frame all scaffolding choices as a scientific loop (hypothesis → controlled test → evidence / `[[How to Test an ADHD Scaffold Using ABAB Withdrawal]]` → keep/reject in `[[MOC - ADHD Experiments & Protocols]]`), not ad-hoc "whatever feels best".
- Then query Todoist for tasks due today, say which action is the priority, and list the next three.

### B4. Health Check (Agent)

- Trigger: weekly review or on request.
- Search active projects in `30_Library/200_Projects/` (`prodos.lifecycle: active`) for notes with no unchecked `- [ ]` line (`obsidian-llmeon_1mcp_search_regex`); for each stalled project propose **1 starter checkbox** in the project note plus **1 date-free physical-verb Todoist runway item**, which gets `#todoist` so Todoist Bridge creates it (or `todoist_1mcp_add-tasks` when the agent writes to Todoist directly).
- Check the Todoist `Waiting` project and any unchecked `#waiting` checkboxes in the vault for delegated/externally blocked items needing a follow-up chase, and check project health in Todoist (`todoist_1mcp_find-tasks`, `todoist_1mcp_find-projects`) for overdue/soft-timeboxed drift.
- Check whether the active ADHD experiment has logged evidence or is ready for ABAB withdrawal / promotion in `[[MOC - ADHD Experiments & Protocols]]`.

### B5. Surrounding Loops (Hermes Gateway)

Where the agent runs under the Hermes Gateway, these run alongside Mode B (recorded from the 2026-05-26 design session; whether each is live is not confirmed here):

- Daily Synthesis (cron): query Pieces LTM for the day's activity, distil it into `/raw` in the vault, and update `/wiki` entity pages with backlinks to Pieces memory IDs.
- Chief of Staff review: surface open loops across Jira (FTFL project, assigned to me), Microsoft Teams and Todoist, write the outstanding work back to an Obsidian SoT, and sync actions to Todoist (project Work, label `@work`).
- Open questions from that session: whether the Hermes `/goal` prompt has been run or only generated; whether a working Teams MCP connector exists; whether the Todoist token is configured in 1Password.

### B6. Daily Plan (Todoist Timeboxing)

- Trigger: `/daily-plan`. The procedure lives in [[Protocol - Daily Plan (Todoist Timeboxing)]].
- The agent reads the runway and the week's Big Rocks ([[Protocol - Big Rocks (Weekly Quadrant II Outcomes)]]) from Todoist, then gives the chosen tasks a date, time and duration in Todoist. Uncompleted soft timeboxes lose their date at shutdown rather than rolling to tomorrow.

### B7. Engage Action (Prosthetic Timebox Loop)

- Trigger: `/engage-action` (hand-off from `/daily-plan` macro blocking into single-block execution). The procedure lives in [[Protocol - Engage Action (Prosthetic Timebox & Somatic Switch)]].
- Once `/daily-plan` has set the day's macro blocks, `/engage-action` selects the active block, narrows to a single somatic starter, and runs a bounded prosthetic timebox loop with explicit friction/re-entry handling.

### B Unit Test

1. Run "Process my dump" with a test entry in `00_Inbox/dump.md`.
2. Confirm the task appears in Todoist.
3. Confirm the content moved to the archive.

## Inbox Triage & Todoist Bridge Routing Protocol

- Trigger: `"triage inbox"` or `"process 00_Inbox"` (after CoS drains Todoist Inbox into individual notes inside `00_Inbox/`).
- Mode: **One item at a time** (interactive loop—never dump a giant wall of text). Read one `00_Inbox/` note, propose its classification below (asking **at most 1 clarifying question** if intent or Definition of Done is ambiguous), wait for confirmation, execute the Obsidian/Todoist mutations, and **delete** the processed `00_Inbox/` note before moving to the next.
- Active MCP tools: `obsidian-llmeon_1mcp_*` (Vault I/O; fallback `obsidian vault="LLMeon" ...`), `todoist_1mcp_add-tasks`, `todoist_1mcp_find-tasks`, `todoist_1mcp_find-projects`, `todoist_1mcp_update-tasks`, `todoist_1mcp_complete-tasks`.

### Control-Plane Separation (Non-Negotiable)

- **Obsidian** (`30_Library/200_Projects/`, `20_Thinking/21_Workbench/`, `30_Library/100_zettelkasten/`) is the sole home for thinking, project outcomes, multi-step checklists, sequencing, `#waiting` states, and problem analysis. Tasks are plain `- [ ]` checkboxes. Only the one next action you choose to send gets `#todoist`, and the Todoist Bridge plugin then mirrors it to Todoist (default project `Personal`; completion and rename sync both ways, due dates do not). Everything untagged stays Obsidian-only.
- **Todoist** (`#Work` or `#Personal`) is a **flat, date-free execution runway** holding **at most one unblocked physical starter verb** (`<120s` MVA / `<5m` starter) per active outcome. Never create Todoist subtasks, nested projects, or fake wish-list due dates.

### The 7-Type `00_Inbox/` Triage Decision Matrix

| Type | Criteria | Obsidian Action | Todoist Runway (`todoist_1mcp_add-tasks`) | Cleanup |
|---|---|---|---|---|
| **1. `< 2-Minute Action`** | Resolvable in under 2 minutes | None | None — prompt human to do it immediately | Delete `00_Inbox/` note |
| **2. Simple Next Action** | 1 standalone physical step; no project container needed | Do **not** create a Project note. No note needed | Push **1 date-free physical-verb task** to `#Work` or `#Personal` (via the Todoist MCP, or as a `- [ ] … #todoist` checkbox when it belongs in a vault note) | Delete `00_Inbox/` note |
| **3. Small Project** | 2–5 steps; finishes within days/weeks; minimal research | Offer two paths:<br>• *Lightweight:* the 2–5 steps as `- [ ]` checkboxes in a single note.<br>• *Standard:* `30_Library/200_Projects/Project - [Outcome].md` (`type: project`, `prodos.lifecycle: active`) from `[[Template - Project]]` with the steps as `- [ ]` checkboxes under `## Tasks` | Push **only the single immediate Next Action** | Delete `00_Inbox/` note |
| **4. Large / Complex Project** | Multi-stage, architecture work, Jira-backed, or deep thinking | If unsettled, open `HEAD - [Question]?.md` in `20_Thinking/21_Workbench/` per `[[SoT - HEAD Note Contract (The Workbench)]]`. Once settled, create `30_Library/200_Projects/Project - [Outcome].md` (`type: project`, `prodos.lifecycle: active`) from `[[Template - Project]]` with the steps as ordered `- [ ]` checkboxes under `## Tasks`; only the first unblocked one is tagged `#todoist` | Push **only the unblocked Next Action** | Delete `00_Inbox/` note |
| **5. Waiting For / Blocked** | Externally blocked (e.g. NHS/MKUH email thread, Jira dependency) | Add an untagged `- [ ] … #waiting` checkbox to the parent `Project - ...` note (or a standalone note), noting who or what it waits on | **None** — keep off active Todoist runway | Delete `00_Inbox/` note |
| **6. Unresolved Problem** | Recurring bug, broken workflow, or constraint | Route to Clarity Framework (`/capture-problem` → `/clarify-problem`): create `Problem - [Undesirable Effect].md` (`type: problem`, `role: symptom`, `status: captured`) rather than prematurely creating a project; promote to `30_Library/200_Projects/` only once a solvable root cause is identified | **None** until solvable root cause yields a Next Action | Delete `00_Inbox/` note |
| **7. Reference / Someday** | Knowledge, reference, or parked project | • *Knowledge/Concept:* Stub or route to `30_Library/100_zettelkasten/` (respect `own_words: true` — never write substantive claims for the human).<br>• *Parked Project:* Create `30_Library/200_Projects/Project - [Outcome].md` with `prodos.lifecycle: someday` (ignored by the B4 stalled-project check) | **None** | Delete `00_Inbox/` note |

## Error Handling

- If dump is too large: The LLM may hallucinate or skip items. _Fix:_ Break the dump into smaller sections or ask for the "top 10 loudest items."
- If output is vague: Re-run with: "You were too vague. I need physical, binary outcomes I can verify with my eyes."

## Unit Test

- [ ] Is there a physical artifact or state for every project in Todoist?
- [ ] Are all next actions binary (Done/Not Done)?
- [ ] Did the human spend < 5 minutes organizing?

---

## Related

- [[SoT - Think Like a Man of Action, Act Like a Man of Thought]]—_Philosophy of decoupling generation from organization._ [depends_on:: [[SoT - Think Like a Man of Action, Act Like a Man of Thought]], confidence=medium]
- [[SoT - PRODOS Core Specification#3. The Thinking Stream (RAM & 120s Intake Loop)|SoT - PRODOS Core Specification (§3 Thinking Stream)]]—_Supplies the raw RAM-clearing Brain Dump (Neuro-Synchronization) input mechanism and core Context is Scarcity / Starter Task rules._ [implements:: [[SoT - PRODOS Core Specification]], confidence=high]
- [[The Time Management Matrix (Eisenhower Matrix)]] [depends_on:: [[The Time Management Matrix (Eisenhower Matrix)]], confidence=medium]—_the triage logic behind this protocol's `!!Priority` step; that note's own Related section explains the mapping quadrant-by-quadrant._
- [[SoT - Execution Protocol (GTD & PARA)]]—_Defines the Project, Container and Task vocabulary this protocol sorts input into, and the Definition of Done its unit test checks._ [implements:: [[SoT - Execution Protocol (GTD & PARA)]], confidence=medium]
- [[Writing Acts as an External Working Memory]]—_Why offloading open loops onto paper/text frees cognitive capacity._ [depends_on:: [[Writing Acts as an External Working Memory]], confidence=high]
- [[Protocol - Daily Plan (Todoist Timeboxing)]]—_Schedules the clarified runway as timed Todoist blocks (B6)._ [extends:: [[Protocol - Daily Plan (Todoist Timeboxing)]], confidence=medium]
- [[Protocol - Engage Action (Prosthetic Timebox & Somatic Switch)]]—_Micro-execution prosthetic timebox and somatic switch loop handed off from `/daily-plan` macro blocking (B7)._ [extends:: [[Protocol - Engage Action (Prosthetic Timebox & Somatic Switch)]], confidence=high]
- [[SoT - GTD Action System]]—_The live four-tier operational architecture and flat Todoist runway targeted by this protocol._ [implements:: [[SoT - GTD Action System]], confidence=high]
