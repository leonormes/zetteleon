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
modified: 2026-11-25T14:30:00+00:00
permalink: llmeon/30-library/100-zettelkasten/protocol-action-first-gtd-llm-chief-of-staff
project_category: prodos
see_also:
  - "[[SoT - Execution Protocol (GTD & PARA)]]"
  - "[[Protocol - Vague-to-Action]]"
status: seed
tags:
  - gtd
  - domain/llm
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

> [!info] One job
> Turn each capture in `00_Inbox/` into a next action, a vault home, or nothing. Leon captures and decides; the agent proposes and does the filing. Cut down to this one job on 2026-11-25 and not yet run in this form.

## Trigger

- The recurring Todoist task `Triage one inbox item` (weekdays, 09:15). Its completion history is the only tracking.
- Or say "triage inbox", "process 00_Inbox", "process my dump" or "I'm overwhelmed".

One item is a successful pass. Stop whenever you like.

## Scope

- Input: capture notes in `00_Inbox/`. A new brain dump is just another note there, with no formatting needed.
- On request only: first move Todoist Inbox items into `00_Inbox/` notes (`source: todoist-inbox`). Ask once before removing them from Todoist.
- Not here: planning the day ([[Protocol - Daily Plan (Todoist Timeboxing)]]), doing a block ([[Protocol - Engage Action (Prosthetic Timebox & Somatic Switch)]]) and the weekly review ([[Protocol - Weekly Command Centre]]).

## Loop

1. Count. Say how many captures are waiting and how old the oldest is.
2. Pick the oldest, or the one Leon names. Read only that one.
3. Propose in a few lines: type, destination and next action. Ask at most one question.
4. Wait for yes, change or skip. Change nothing before the answer.
5. Execute. Copy any of Leon's own wording into the destination, check it arrived, then delete the capture.
6. Report the count left and offer the next one.

If one capture holds several open loops, handle them as separate items. If a dump holds more than 10, triage the 10 loudest and leave the rest captured.

## Decision Matrix

| Type | Criteria | Obsidian | Todoist |
|---|---|---|---|
| 1. Under 2 minutes | Can be done now | None | None. Prompt Leon to do it |
| 2. Single action | One physical step, no project needed | No note, unless the step belongs in one (`- [ ] … #todoist`) | 1 task in `#Work` or `#Personal` |
| 3. Small project | 2–5 steps | Checkboxes in one note, or `30_Library/200_Projects/Project - [Outcome].md` from [[Template - Project]] (`prodos.lifecycle: active`) | The first step only |
| 4. Large project | Multi-stage or needs deep thinking | If unsettled, a `HEAD - [Question]?` note per [[SoT - HEAD Note Contract (The Workbench)]]; once settled, a project note with ordered checkboxes | The first unblocked step only |
| 5. Work ticket | Work bug or feature | None. Draft a Jira ticket | A starter only if Leon takes the first step |
| 6. Waiting | Blocked on someone else | `- [ ] … #waiting` in the project note (or its own note), naming who and what | None |
| 7. Problem | Recurring fault, no root cause yet | `Problem - [Undesirable Effect].md` (`type: problem`, `role: symptom`, `status: captured`), then `/capture-problem` → `/clarify-problem` | None |
| 8. Reference | Knowledge worth keeping | Stub or file in `30_Library/100_zettelkasten/`; never write claims as Leon | None |
| 9. Someday | Real, not now | Project note with `prodos.lifecycle: someday` | None |
| 10. Noise | No outcome and no value | None | None |

## Rules

### Where Things Live

- Obsidian holds thinking, outcomes, checklists, sequencing, `#waiting` states and problems. Only the chosen next action is tagged `#todoist`. Todoist Bridge mirrors it (default project `Personal`); completion and renames sync both ways, dates do not.
- Todoist holds a flat runway with at most one unblocked starter per outcome. Triage creates no subtasks, nested projects or due dates. The architecture is [[SoT - GTD Action System]].

### What a Good Next Action Looks Like

- It starts with a physical verb, can be started in under 5 minutes and is plainly done or not done.
- Each project states its definition of done as a visible state, for example "new fence panels installed and painted".
- If it still feels vague, run [[Protocol - Vague-to-Action]].

### Priority

Check each proposed action against [[The Time Management Matrix (Eisenhower Matrix)]]. Urgent and important gets the highest Todoist priority. Important but not urgent still gets a real priority, so it is not crowded out. Urgent but unimportant gets a low priority or is challenged as delegatable. Neither urgent nor important is usually dropped.

### Agent Tools

- Vault: `obsidian-llmeon_1mcp_*`, falling back to `obsidian vault="LLMeon" …`.
- Todoist: `add-tasks`, `find-tasks`, `find-projects`, `update-tasks`, `complete-tasks`.
- Never edit a protected note ([[AGENTS]] §6).

## Stalled-Project Check (on Request)

1. Find notes in `30_Library/200_Projects/` with `prodos.lifecycle: active` and no unchecked `- [ ]` line.
2. For each, propose one starter checkbox tagged `#todoist`. Write it after a yes.
3. Report how many project notes have no `prodos.lifecycle`, so an empty result cannot pass as healthy.

## Earning Its Keep

Review on 2026-12-11. These thresholds are proposed, not yet tested.

| Measure | Keep if |
|---|---|
| `Triage one inbox item` completed, 26 November to 9 December | At least 6 of 10 weekdays |
| Captures waiting in `00_Inbox/` on the review day | 5 or fewer |

If either fails, change the trigger or retire this protocol. Do not add steps.

---

## Related

- [[SoT - Think Like a Man of Action, Act Like a Man of Thought]]—_Philosophy of decoupling generation from organisation._ [depends_on:: [[SoT - Think Like a Man of Action, Act Like a Man of Thought]], confidence=medium]
- [[SoT - PRODOS Core Specification#3. The Thinking Stream (RAM & 120s Intake Loop)|SoT - PRODOS Core Specification (§3 Thinking Stream)]]—_Supplies the capture loop and starter-task rules this protocol applies._ [implements:: [[SoT - PRODOS Core Specification]], confidence=high]
- [[The Time Management Matrix (Eisenhower Matrix)]] [depends_on:: [[The Time Management Matrix (Eisenhower Matrix)]], confidence=medium]—_The triage logic behind the Priority rule._
- [[SoT - Execution Protocol (GTD & PARA)]]—_Defines the project and task vocabulary this protocol sorts input into._ [implements:: [[SoT - Execution Protocol (GTD & PARA)]], confidence=medium]
- [[Writing Acts as an External Working Memory]]—_Why offloading open loops into text frees cognitive capacity._ [depends_on:: [[Writing Acts as an External Working Memory]], confidence=high]
- [[SoT - GTD Action System]]—_The tool architecture and flat Todoist runway this protocol feeds._ [implements:: [[SoT - GTD Action System]], confidence=high]
