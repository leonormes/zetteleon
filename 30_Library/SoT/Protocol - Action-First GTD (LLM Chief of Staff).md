---
aliases: [Action-First GTD, Dump Don't Organize, LLM Chief of Staff]
conformant: true
created: 2026-02-11T11:40:00+00:00
modified: 2026-09-23T00:00:00+00:00
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
> Use Todoist Quick Add syntax (e.g., ProjectName @Context!!Priority).
>
> Here is the dump:"

### 3. Execution (CD Mode)

- Tool: Todoist Board View (Kanban).
- Action: Paste the LLM output into Todoist.
- Workflow: Focus only on the "Next Actions" list. The LLM has already performed the cognitive work of defining "Done."

## Error Handling

- If dump is too large: The LLM may hallucinate or skip items. _Fix:_ Break the dump into smaller sections or ask for the "top 10 loudest items."
- If output is vague: Re-run with: "You were too vague. I need physical, binary outcomes I can verify with my eyes."

## Unit Test

- [ ] Is there a physical artifact or state for every project in Todoist?
- [ ] Are all next actions binary (Done/Not Done)?
- [ ] Did the human spend < 5 minutes organizing?

---

## Related

- rel:: [[SoT - Think Like a Man of Action, Act Like a Man of Thought]]
- rel:: [[SoT - Cognitive Engineering Protocols]] (Module A)
- [[The Time Management Matrix (Eisenhower Matrix)]] [depends_on:: [[The Time Management Matrix (Eisenhower Matrix)]], confidence=medium]—_the triage logic behind this protocol's `!!Priority` step; that note's own Related section explains the mapping quadrant-by-quadrant._
- [[SoT - Execution Protocol (GTD & PARA)]]—_Defines the Project, Container and Task vocabulary this protocol sorts input into, and the Definition of Done its unit test checks._

[implements:: [[SoT - Execution Protocol (GTD & PARA)]], confidence=medium]
