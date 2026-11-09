---
aliases: [Action-First GTD, Agent GTD, Autonomous Action, Dump Don't Organize, LLM Chief of Staff, Todoist MCP Integration]
conformant: true
created: 2026-02-11T11:40:00+00:00
modified: 2026-10-22T15:11:12+00:00
non_conformance_reason: ''
permalink: llmeon/30-library/so-t/protocol-action-first-gtd-llm-chief-of-staff
status: stable
tags: [gtd, llm, system/protocol, TheHuman/Health/ADHD]
title: Protocol - Action-First GTD (LLM Chief of Staff)
type: protocol
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
- Todoist target: Clarified actions go to the runway and unclarified items stay in the Inbox, as defined in [[gtd-action-system]]. Actionability is location, not a tag.

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

- Trigger: start of a new session. Query Todoist for tasks due today, then say which action is the priority and list the next three.

### B4. Health Check (Agent)

- Trigger: weekly review or on request. Check project health in Todoist and flag stalled projects or overdue items with a proposed next test.

### B5. Surrounding Loops (Hermes Gateway)

Where the agent runs under the Hermes Gateway, these run alongside Mode B (recorded from the 2026-05-26 design session; whether each is live is not confirmed here):

- Daily Synthesis (cron): query Pieces LTM for the day's activity, distil it into `/raw` in the vault, and update `/wiki` entity pages with backlinks to Pieces memory IDs.
- Chief of Staff review: surface open loops across Jira (FTFL project, assigned to me), Microsoft Teams and Todoist, write the outstanding work back to an Obsidian SoT, and sync actions to Todoist (project Work, label `@work`).
- Open questions from that session: whether the Hermes `/goal` prompt has been run or only generated; whether a working Teams MCP connector exists; whether the Todoist token is configured in 1Password.

### B Unit Test

1. Run "Process my dump" with a test entry in `00_Inbox/dump.md`.
2. Confirm the task appears in Todoist.
3. Confirm the content moved to the archive.

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
- [[SoT - Cognitive Engineering Protocols]]—_Module A (The Brain Dump) provides the raw input mechanism._ [depends_on:: [[SoT - Cognitive Engineering Protocols]], confidence=medium]
- [[The Time Management Matrix (Eisenhower Matrix)]] [depends_on:: [[The Time Management Matrix (Eisenhower Matrix)]], confidence=medium]—_the triage logic behind this protocol's `!!Priority` step; that note's own Related section explains the mapping quadrant-by-quadrant._
- [[SoT - Execution Protocol (GTD & PARA)]]—_Defines the Project, Container and Task vocabulary this protocol sorts input into, and the Definition of Done its unit test checks._
- [[gtd-action-system]]—_The live four-tier operational architecture and flat Todoist runway targeted by this protocol._ [implements:: [[gtd-action-system]], confidence=high]

[implements:: [[SoT - Execution Protocol (GTD & PARA)]], confidence=medium]
