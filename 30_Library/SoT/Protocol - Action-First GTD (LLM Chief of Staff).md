---
aliases: ["Dump Don't Organize", Action-First GTD, LLM Chief of Staff]
conformant: false
created: 2026-02-11T11:40:00+00:00
modified: 2026-08-13T10:53:38+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/protocol-action-first-gtd-llm-chief-of-staff
status: active
tags: [adhd, gtd, llm, system/protocol]
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
