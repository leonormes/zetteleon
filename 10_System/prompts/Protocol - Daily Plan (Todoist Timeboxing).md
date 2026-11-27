---
conformant: true
created: 2026-11-16T12:30:00+00:00
description: Build today's plan by reading the Todoist runway and timeboxing the chosen tasks as dated, timed and sized Todoist tasks, with Big Rocks first and a 25% buffer. Use for `/daily-plan`, "plan my day", or the start of a working session.
modified: 2026-11-25T10:30:00+00:00
permalink: llmeon/10-system/prompts/protocol-daily-plan-todoist-timeboxing
status: seed
tags:
- agent/chief-of-staff
- domain/pkm
- prodos/protocol
- topic/gtd
- type/protocol
title: Protocol - Daily Plan (Todoist Timeboxing)
type: prompt
version: 4
---

> [!info] Write scope
> This protocol writes only to Todoist (time blocks, Big Rock parent tasks, missing starter actions) and to chat. It never edits vault notes. Protected notes (`own_words: true`, `01_journals/`, `20_Thinking/`) stay read-only under [[AGENTS]] §6.

> [!warning] Draft, untested
> Version 3 replaced the earlier design that used a separate scheduling app, which Leon stopped using on 2026-11-17. Version 4 adds a read-only Spark CLI comms scan, a read-only Fantastical capacity read and a Jira starter check. The Todoist behaviour comes from [[Protocol - Time Blocking in Todoist (Calendar Layout and Durations)]]. It has not been run yet, and the `Today` list rule below is a provisional choice, not a settled one.

> Trigger: `/daily-plan`, "plan my day", or the start of a working session. For clarifying the Inbox use [[Protocol - Action-First GTD (LLM Chief of Staff)]] instead; this protocol only schedules tasks that are already clarified.

## Control plane

Todoist is the source of truth for tasks and also the timeline. A time block is a Todoist task with a date, a time and a duration. The architecture is in [[SoT - GTD Action System]].

- Provisional rule: a block is transient. The CoS sets date, time and duration for today's plan and clears them at shutdown, so no due date survives overnight. This is option 1 in the time-blocking note. The existing rule that `Today` holds only hard-landscape commitments is relaxed during the day only.
- NEVER clear or move a due date the CoS did not set itself. Tasks that were already dated by Leon, or that have a Deadline, are hard landscape and keep their dates.
- NEVER create a calendar event for work. Time blocks live on the Todoist tasks.
- Use `reschedule-tasks` to place or move a block, not `update-tasks`, so recurrence is preserved.
- **Todoist Bridge (`#todoist` checkboxes):** Todoist Bridge does not sync due dates or durations, so time blocks are set only on the Todoist task with `reschedule-tasks`. Never write a date or time into the matching Obsidian checkbox.

## Selection

Labels such as `@next_action` were purged, so use location as defined in [[SoT - GTD Action System]]:

- Next actions: the runway filter `!#Inbox & !#Someday & !#Waiting`.
- Big Rocks: this week's Big Rock parent tasks, defined in [[Protocol - Big Rocks (Weekly Quadrant II Outcomes)]]. A Todoist priority never marks a Big Rock, because p1 carries urgency and is not a signal of importance.
- Hard landscape: tasks with a true Deadline or a due date Leon set. These are fixed and go on the plan first as given.
- Renewal: a block whose only purpose is to restore physical or mental capacity, and that Leon has named as Renewal. Examples: a training session, a walk or outdoor time, a meal break away from the screen, a wind-down. Not Renewal: chores, admin, ordinary meetings. Place at least one Renewal block of 30m or more before any Big Rock block, and never shrink it to fit other work. If Leon has named none for the day, ask him for one. Do not invent it.

## Procedure

0. **Step 0 — Morning Reset & Shutdown Guard**: Before scheduling, audit `(overdue | today) & no deadline` in Todoist, stripping stale CoS-set `Today` dates back to the flat runway via `update-tasks` (`dueString: "remove"`), while never clearing dates Leon set or Deadlines. Never roll soft tasks to tomorrow.0b. **Active ADHD Experiment Check**: Read `[[MOC - ADHD Experiments & Protocols]]` and any active `experiment` `HEAD` note in `20_Thinking/21_Workbench/` (e.g. `[[HEAD - Do 75m Deep Dive Sessions Outperform Granular Next Actions for ADHD?]]`). Apply its active test conditions to today's plan as a controlled scientific test (hypothesis → controlled test → `[[How to Test an ADHD Scaffold Using ABAB Withdrawal]]` → keep/reject in `[[MOC - ADHD Experiments & Protocols]]`), rather than ad-hoc "whatever feels best" scheduling.
1. Read the runway and today's hard landscape from Todoist: `find-tasks-by-date` for today, and the runway filter.
2. Read this week's Big Rock parent tasks and their subtasks. Read-only Jira starter check: search for open tickets assigned to Leon that are In Progress or in the active sprint (project FTFL). For each, check the runway for one starter action and list tickets with none as "no starter". Never create a task that mirrors a ticket ([[SoT - GTD Action System]]: one starter per active ticket, never the ticket itself).
3. Monday proposal: if today is Monday or the first working day of the week and there are no Big Rock parents for this week, run the proposal below before anything else.
4. **Capacity (Fantastical MCP, read-only).** Todoist's own tools do not return calendar events. Read today's events with `queryCalendarItems` and filter by `calendarId`. Only two calendars block by default (allowlist): `Leon's Calendar` (`c39d06bd8790ee3c2ace48eb595d02d92dc7f57d`) and the Microsoft 365 work `Calendar` (`ca527ed60799e8ed9a9152cf74b1ee6c3237ecd0`). Everything else is non-blocking, including `Family` (`8c9e512f747bfa02894fbf91e1aa876a8fefbd9f`), `zofjaormes@gmail.com` (`d9a6f2d2febff41140cffc547fcff7f12bc1df65`), the legacy `Todoist` calendar (`07138e3b64452ed6902b56af0d8679ec060769e7`) and the sports, holiday and birthday calendars. Two exceptions on the Family calendar: a pick-up from a family class (such as cheerleading or gymnastics) blocks when it falls inside the working window or constrains it, and if the event does not state the pick-up time, ask Leon for it; and an `Archery` event blocks, which means every other Wednesday when it is scheduled. Hard landscape is every blocking event plus Todoist tasks with a Deadline or a due date Leon set. Free windows are the working window `09:00–17:00` (Europe/London, unless Leon states another today) minus hard landscape, ignoring any window under 15m. Report total free minutes, then reserve 25% of them as buffer. If the call fails, say so and ask Leon for the day's events. Never guess capacity. Never write to the calendar.
4b. **Comms scan (`spark` CLI, read-only).** Run `spark emails --filter "is:unread newer_than:1d" Inbox` for the unified inbox, and read a thread with `spark thread <id>` only when the subject is not enough. Both accounts are read-only in Spark. Never use `spark draft`, `spark action` or `spark comment`, and never send, archive, label or mark read. Return at most 8 candidates as `sender — subject — proposed type`, where type is one of: `Runway task` (actionable over 2 min, no date), `Waiting` (`Waiting: <who> — <what>`, chase-by date in the description only), `Jira` (already ticketed, no Todoist task), `Do now` (under 2 min) or `Skip`. Create nothing until Leon answers accept, swap or reject per candidate. Accepted tasks go to the runway or `#Waiting` with no due date. Reply work lands in the two 20m Comms Triage Boxes.
5. Fill free time in strict protection order: `Renewal > Big Rocks (subtasks of this week's Big Rock parents) > Other Actions (Runway: !#Inbox & !#Someday & !#Waiting) > Two 20m Comms Triage Boxes (10:30 & 15:30) > 25% Unscheduled Buffer`. Stop when only the 25% buffer remains.
6. Size standard execution boxes at `15m`, `30m`, or `60m`. Call `reschedule-tasks` with `date` as `YYYY-MM-DDTHH:MM:SS` and `duration: "15m"` | `"30m"` | `"60m"`. Group `<120s` MVA tasks and `<5m` starter tasks from one vertical project context into a single execution box, placed on the first task with the others named in its description.
7. **Parallel Agent Blocks**: Where a block runs concurrent terminal agent supervision (`Zellij` + `agy` / `Claude Code`), name the foreground task and list the background tasks in the plan table. They share one foreground block without allocating separate time.
8. Do not schedule over an event Leon has said is busy. Skip the NUH-style calls Leon says he is not attending.

### Monday proposal

1. Read active vault projects, Horizons of Focus, Jira tickets assigned to Leon, and the Todoist runway.
2. Propose up to 3 Big Rock candidates. Each is a Quadrant II outcome in finishable wording with its source and a time estimate in minutes. Propose 1 or 2 when existing calendar commitments leave less than 20 hours of open work blocks for the week, and state the figure.
3. Wait for a binary answer per candidate: accept, swap or reject. Create nothing before that.
4. For each accepted rock, call `add-tasks` for a parent task in the Work project, section `Big Rocks`, with content `BIG ROCK: <outcome>` and the estimate in its description as `Estimate: <minutes> min`. Todoist durations need a date and time, so the estimate is not stored as a duration.
5. Add physical-verb starter actions as subtasks of the parent. Do not schedule them until the plan reaches that day.

## Output

Return in chat:

- **Active ADHD Experiment** (always first): name the active `HEAD` experiment from `[[MOC - ADHD Experiments & Protocols]]` / `20_Thinking/21_Workbench/`, the hypothesis being tested, today's concrete behavioural test, and what evidence would settle it (scientific test, not ad-hoc intuition).
- A table of block time, task, Big Rock (if any) and a Todoist link `https://app.todoist.com/app/task/<task-id>`. State that the link format has not been checked against the app.
- **Task-Authoring Gate Stubs & Deep Links**: For every scheduled Big Rock or deep-work timebox, output the Todoist link `https://app.todoist.com/app/task/<task-id>` alongside a pre-populated MVA (`<120s`) prompt stub ready for `/engage-action` ([[Protocol - Engage Action (Prosthetic Timebox & Somatic Switch)]]).
- The line `Big Rock time planned: X of Y minutes`. X is the weekly minutes of `duration` on scheduled subtasks of this week's Big Rock parents, including today. Y is the sum of the `Estimate` values on those parents. With no Big Rocks it reads `0 of 0 minutes (none set)`.
- The buffer in minutes, plus anything assumed.

Per [[SoT - Typed Answer Contract (TAC) for LLM Output]], state confidence, say plainly when a tool call failed or a link format is unverified, and never guess a task ID.

## End-of-day shutdown (16:45)

Soft timeboxes are not rolled forward.

- For each uncompleted task the CoS blocked today, call `update-tasks` with `dueString: "remove"`. Skip tasks whose date Leon set and tasks with a Deadline.
- NEVER set tomorrow's date on an uncompleted task. Tomorrow starts with a fresh proposal from the runway.
- If the CoS cannot tell whether a date was its own, it asks Leon before clearing.

## Todoist tools used

`find-tasks-by-date`, `find-tasks`, `reschedule-tasks`, `update-tasks`, `add-tasks`, and optionally `add-reminders` for a warning before a block.

## Related

- [[SoT - Temporal Management (Blocking and Boxing)]]—_Canonical distinction between macro time blocking, micro time boxing, and two-window batched shallows._ [implements:: [[SoT - Temporal Management (Blocking and Boxing)]], confidence=high]
- [[SoT - Execution Protocol (GTD & PARA)]]—_Canonical GTD and PARA execution model that this daily planning protocol implements._ [implements:: [[SoT - Execution Protocol (GTD & PARA)]], confidence=high]
- [[SoT - GTD Action System]]—_The four-tier architecture and flat runway this protocol schedules from._ [implements:: [[SoT - GTD Action System]], confidence=high]
- [[Protocol - Action-First GTD (LLM Chief of Staff)]]—_Inbox triage loop that clarifies the tasks this protocol timeboxes._ [depends_on:: [[Protocol - Action-First GTD (LLM Chief of Staff)]], confidence=high]
- [[Protocol - Big Rocks (Weekly Quadrant II Outcomes)]]—_Defines Big Rocks, the weekly cap and the Monday proposal that this protocol runs._ [depends_on:: [[Protocol - Big Rocks (Weekly Quadrant II Outcomes)]], confidence=high]
- [[Protocol - Time Blocking in Todoist (Calendar Layout and Durations)]]—_How Todoist blocks, durations and calendar sync work, and the options this protocol chooses between._ [depends_on:: [[Protocol - Time Blocking in Todoist (Calendar Layout and Durations)]], confidence=high]
