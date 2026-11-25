---
aliases:
  - Todoist Time Blocking
  - Todoist Timeboxing
  - Todoist Calendar Layout
conformant: true
created: 2026-11-17T08:50:00+00:00
modified: 2026-11-17T09:20:00+00:00
permalink: llmeon/30-library/100-zettelkasten/protocol-time-blocking-in-todoist-calendar-layout-and-durations
project_category: prodos
status: seed
tags:
  - gtd
  - productivity
  - protocol
  - TheHuman/Health/ADHD
title: Protocol - Time Blocking in Todoist (Calendar Layout and Durations)
type: protocol
prodos:
  kind: protocol
  protocol:
    applies_to:
      - task-scheduling
---

> [!abstract] The rule in one paragraph
> A Todoist task becomes a time block when it has a date, a time and a duration. Todoist shows those blocks in its Calendar layout next to events from a synced calendar, so Todoist can be both the task list and the timeline. This note records how that works, how the Chief of Staff (CoS) can do it through the Todoist MCP, and the one rule in [[SoT - GTD Action System]] that it collides with.

## Why this note exists

The first design for `/daily-plan` used a separate scheduling app as the timeline. On 2026-11-17 Leon stopped using it, so the timeline has to come from somewhere else. Todoist already holds the tasks and Leon is on Todoist Pro, so it was the first candidate. [[Protocol - Daily Plan (Todoist Timeboxing)]] has since been rewritten on this evidence and adopts option 1 below provisionally. This note stays as the evidence base.

## Sources and confidence

| Source | What it gives | Confidence |
|---|---|---|
| Todoist help article "Time blocking in Todoist", fetched 2026-11-17 | Calendar layouts, how to add date, time and duration, syncing | High for what it states. It does not say which plans include these features. |
| Todoist guide "Time Blocking - Your Complete Guide to More Focused Work" (todoist.com/productivity-methods/time-blocking), clipped by Leon 2026-11-17 | Methods, process, pitfalls, tips, plan tiers, two-way calendar sync, Quick Add duration syntax | High for what Todoist states about its own product. Its research and expert quotes are cited secondhand and I have not checked them. |
| Leon's pasted summary, 2026-11-17 | Plan requirement, `Sync Tasks to Calendar` toggle, label-based theme blocks, buffer and colour tips | Medium. It is secondary. The guide above confirms the plan tier and the sync toggle. |
| Todoist MCP tool schemas, read 2026-11-17 | What the CoS can write and read | High. These are the live contracts. |
| `user-info` call, 2026-11-17 | Plan is Todoist Pro, week starts Monday, timezone Europe/London | High. |

## How Todoist time blocking works

### Two calendar layouts

- Day calendar: open Today, use the layout button at the top right and choose Calendar. On mobile, tap Today, then the three-dots icon, then View, then Calendar. All-day tasks and events sit at the top and timed ones sit in their slots.
- Week calendar: open Upcoming, choose Calendar, then the Week layout. On mobile the layout shows 3 rolling days in portrait and 7 in landscape. The week calendar schedules up to two years ahead.

### Making a time block

A block is a task with a date, a time and a duration. There are four ways to set one:

1. Drag a task onto the calendar. An all-day task gets a date, a time and a default 30-minute duration.
2. Click an empty slot in the calendar. Quick Add opens with 30 minutes already set.
3. Use natural language in Quick Add, for example "tomorrow at 10:00 AM for 25 minutes" or "next Friday 2:00 PM for 90 minutes".
4. Open the task, click the Date field and set the day, time and duration in the scheduler.

Quick Add also takes "for" and a length, for example "Team meeting today 4pm for 45min" or "Write first draft 9am for 2 hours 30 minutes". Click-dragging across an empty stretch of the calendar creates a block of that length and opens the new-task form, where project, label and priority can be set. Tasks with a date but no time sit in the All Day row until they are dragged to a time.

To change a block's length, drag its bottom edge in the calendar. Durations that arrive from a synced calendar appear the same way.

### Plan sidebar

In Upcoming, the Plan sidebar lists overdue tasks, all-day tasks and tasks that only have a deadline. Dropping one onto the calendar gives it a date, a time and a duration. A new task created by clicking a slot gets a reminder pre-filled.

### Calendar sync

- Set up the Calendar integration to sync Todoist with a calendar app. Synced Todoist tasks appear in a calendar named "Todoist".
- Events from the calendar app appear inside Todoist in their original colours, so overlaps are visible.
- Task colours in the calendar layout can follow priority, label or project.
- The sync is two-way only if the `Sync Tasks to Calendar` option is on when the calendar is linked. Otherwise it is one-way, and calendar events show in Todoist but Todoist blocks do not show in the calendar. With it on, the external calendar shows Leon as busy during Todoist blocks, so meeting requests do not land in them.
- The guide names Outlook and Google Calendar as the supported integrations. Fantastical is not named, so Todoist blocks would reach Fantastical only through a linked Google or Outlook account. That is my inference and is untested.
- The calendar layout is a paid feature on the Pro and Business plans. Leon is on Pro, so it is available.
- Month and week views both exist, and the guide says time blocking works best in the week view.

### Timeblocking versus timeboxing

Leon's summary draws this line, and the vault should use it consistently.

- Timeblocking reserves a chunk of time for a category of work, such as Deep Work or Admin.
- Timeboxing gives one task a hard limit so it cannot expand.
- Todoist supports timeboxing directly through durations. For timeblocking by theme, the summary suggests labels (`@deep_work`, `@admin`, `@calls`) plus recurring blocks, then filtering by the label when a block starts. The vault purged `@next_action`-style labels, so a theme label would be a new, deliberate exception.

### Weekly review tip

The help article suggests one hour at the end of the week to review what was done and plan the next week. That overlaps [[Protocol - Weekly Command Centre]], which is deliberately a 10-minute floor, so do not add this hour there.

## Four methods and how Todoist supports each

| Method | Meaning | In Todoist |
|---|---|---|
| Time blocking | A block of time for one task or activity, and only that | A task with date, time and duration in the calendar layout |
| Task batching | Similar, usually small, tasks grouped into one block to cut context switching | A block for the category, plus a label or filter listing its tasks |
| Day theming | One theme or project per day | Same labels or projects, checked at the start of the day |
| Time boxing | A limit on how long a task may take | A duration on the task |

- Time blocking and time boxing differ only in framing. Blocking sets time aside for a task ("work on the draft 9 to 11"). Boxing caps the task ("finish the draft by 11"). The guide treats a Todoist duration as serving both.
- Batching example from the guide: two 20-minute email blocks a day beat checking every 15 minutes. It pairs with blocking because only the batch needs a place in the calendar, not each task.
- Day theming is a stricter batching. The guide's example themes are meetings, creative work and admin, or a client or project per day. Urgent off-theme work is allowed, but it should be moved to the next day whose theme fits, and a 30 to 60 minute admin or email block at the start or end of a themed day catches the rest.
- The guide's batching setup is: list categories, block them in a calendar using time-tracking data to size them, create one label per category, label every task, and open the label list when its block starts. Tasks with dates appear first, and priority colours order the rest. A filter such as `@personal_admin & next 7 days` narrows it.

## Process and practice rules from the guide

The five-step process:

1. Identify the tasks for the week and rank them by importance and urgency, using [[The Time Management Matrix (Eisenhower Matrix)]].
2. Create work blocks and map them on a calendar: high-priority work in the morning, meetings midday, admin and email late afternoon.
3. Balance the plan with personal errands, breaks and leisure.
4. Stick to the plan, and if a task is unfinished move it to a future block instead of stretching the current one.
5. Review at the end of each day and adjust the rest of the week.

Practice rules:

- Pad the schedule. Until estimates improve, block too much time, not too little. Add "conditional blocks", spare time at the end of the day or between big tasks that is used only if needed and is otherwise free.
- Protect peak hours. Find the hours when concentration is best and put the most demanding work there. The guide suggests RescueTime or Toggl to find them. Leon's peak hours are not recorded in the vault.
- Plan for unforeseen demands. If other people's requests are part of the job, block time for them so they do not break the rest of the day. Open-ended reactive work can itself be blocked like any other obligation.
- Do not overschedule leisure. Leave some free time unplanned.
- Treat the plan as a guide, not a contract. Edit blocks through the day.
- Make Deep Work visible. On a shared calendar a block that shows as busy keeps meetings out. The guide quotes one designer who names such blocks "Do Not Book".
- Known pitfalls: underestimating time, rigidity, overscheduled leisure, treating everything as equally important, and ignoring interruptions.

Reasons the guide gives, with the evidence it cites:

- Estimates are unreliable because of the planning fallacy and present bias. A calendar makes the cost of saying yes concrete.
- Time boxing counters perfectionism by setting a "good enough" limit.
- Shallow work (urgent, not important) is time-boxed so it does not spread, and batched so it costs less switching. That matches Quadrant III in [[The Time Management Matrix (Eisenhower Matrix)]].
- Specific plans improve follow-through. The guide cites Rogers, Milkman, John and Norton, who review studies where writing down a place, date and time raised follow-through. I have not read the paper.

## How this fits ProdOS

- Batching is already in the plan. [[Protocol - Daily Plan (Todoist Timeboxing)]] groups `<120s` MVA and `<5m` starter tasks from one project into a 30-minute block. That is task batching.
- Labels conflict with the vault. The guide batches by label, but the vault purged `@next_action`-style labels and treats location as actionability. Batch by project, section or a saved filter instead, unless Leon decides a small set of mode labels is worth the exception.
- Day theming already has a note: [[Day Theming is a Macro Time Blocking Strategy]]. It is not part of `/daily-plan`.
- The guide's buffer ("conditional blocks") matches the 25% unscheduled buffer. The 25% figure is the vault's own rule and the guide gives no number.
- Rollover differs. The guide says to move unfinished work to a future block. ProdOS says no rollover. They are compatible if the CoS clears blocks at shutdown and proposes a fresh plan the next morning, so a "future block" is a new proposal and not an automatic carry-over.
- Todoist has no actual-time tracking, which the earlier scheduling app had. The guide suggests RescueTime or Toggl, so that part would need another tool, and only if Leon wants it.
- Visible Deep Work blocks help here. With two-way sync on, a Big Rock block shows Leon as busy to colleagues, which protects it from meeting invites.

## What the CoS can do through the Todoist MCP

Tool names below are as exposed through 1MCP (`mcp__1mcp__todoist_1mcp_*`).

| Need | Tool and field | Notes |
|---|---|---|
| Create a task with a block | `add-tasks` with `dueString` such as "tomorrow at 9:30am" and `duration` such as "30m" | `duration` accepts `30m`, `1h`, `2h30m`. |
| Move or resize a block | `reschedule-tasks` with `date` as `YYYY-MM-DDTHH:MM:SS` and `duration` | Date-only keeps an existing time. Preferred over `update-tasks` because it preserves recurrence. |
| Clear a block | `update-tasks` with `dueString: "remove"` | Used at shutdown. Refused on recurring tasks unless `replaceRecurrence` is set. |
| Read a day or week | `find-tasks-by-date` with `startDate` and `daysCount` up to 30 | `startDate: today` includes overdue by default. |
| Warn before a block | `add-reminders` with a `relative` `minuteOffset` | Optional. |
| Hard constraint | `deadlineDate` on `add-tasks` or `update-tasks` | A deadline is separate from the due date a block uses. |

### Limits

- Todoist apps only display durations under 24 hours. A longer duration is stored but shows as no duration.
- The Todoist MCP has no tool that reads calendar events. The CoS cannot see meetings from Todoist alone, so capacity has to come from another source, such as the Fantastical MCP in 1MCP. That server is configured and the daily plan reads it read-only, but it has not yet been run end to end.
- Today's view of the whole day needs a call to `find-tasks-by-date`. The Calendar layout itself is a UI and has no MCP equivalent.

## Where this clashes with the existing system

[[SoT - GTD Action System]] keeps the Todoist `Today` list for hard-landscape commitments only, with a morning reset and no rollover. A time block needs a due date and time, so every block puts a task on `Today`. These are the options, and Leon has not chosen one:

1. Transient blocks. The CoS sets date, time and duration for the day's plan and clears them at shutdown with `dueString: remove`, so no due date survives overnight. The `Today` list is then noisy during the day but clean each morning.
2. Blocks on a calendar, not on Todoist. The CoS writes blocks to Fantastical and leaves Todoist due dates alone. This keeps the Todoist rule intact but needs the Fantastical MCP to work, and needs a way to link a block back to its task.
3. Amend the rule. Allow soft due dates for planned blocks, and rely on deadlines for the hard landscape.

Option 1 is closest to the original design. Option 2 is closest to the existing rule. I recommend deciding after testing option 1 for one day.

## Proposed procedure for the CoS (draft)

This is the draft behind [[Protocol - Daily Plan (Todoist Timeboxing)]], which adopts option 1 provisionally. It is untested.

1. Read the runway and today's hard landscape from Todoist.
2. Read capacity from the calendar source. Treat the Family calendar as non-blocking.
3. Reserve 25% of the free minutes as buffer.
4. Fill free time in this order: Renewal (defined in [[Protocol - Daily Plan (Todoist Timeboxing)]]), then Big Rock tasks, then other actions, then buffer.
5. Use 30-minute blocks. Group `<120s` MVA tasks and `<5m` starter tasks from one project into one block. Set each with `reschedule-tasks`.
6. Mark Parallel work by a `parallel` label, which has no scheduling effect and is only a reading cue for the CoS.
7. Report the plan as a table of block, task and a Todoist link `https://app.todoist.com/app/task/<id>`.
8. At shutdown, clear the date and time from each uncompleted task. Never move one to tomorrow.

## Open questions

- Which of the three options above resolves the `Today` list clash?
- Is a Google or Outlook calendar linked to Todoist with `Sync Tasks to Calendar` on, and does Fantastical show those blocks? Todoist's guide names only Google and Outlook.
- Should Big Rock blocks show as busy to colleagues through two-way sync?
- Should the CoS batch by project or filter, or does Leon want a small set of mode labels as an exception to the label purge?
- What are Leon's peak hours, and is it worth measuring them with a time tracker?
- Is a parent task per rock, in the Work project's `Big Rocks` section, the right home for Big Rocks? That is the current choice in [[Protocol - Big Rocks (Weekly Quadrant II Outcomes)]], and the parents will also appear in the runway filter.
- Does the Fantastical MCP work for reading capacity?

## Related

- [[SoT - Temporal Management (Blocking and Boxing)]]—_The timeblocking and timeboxing technique this note applies in Todoist._ [depends_on:: [[SoT - Temporal Management (Blocking and Boxing)]], confidence=high]
- [[SoT - GTD Action System]]—_Owns the Todoist runway and the Today-list rule this note collides with._ [depends_on:: [[SoT - GTD Action System]], confidence=high]
- [[Protocol - Daily Plan (Todoist Timeboxing)]]—_The protocol built on this evidence._ [supports:: [[Protocol - Daily Plan (Todoist Timeboxing)]], confidence=medium]
- [[Protocol - Big Rocks (Weekly Quadrant II Outcomes)]]—_Defines the rocks that would be scheduled first in a Todoist plan._ [supports:: [[Protocol - Big Rocks (Weekly Quadrant II Outcomes)]], confidence=medium]
- [[Day Theming is a Macro Time Blocking Strategy]]—_The vault's existing note on theming days, which the guide treats as the strictest form of batching._ [supports:: [[Day Theming is a Macro Time Blocking Strategy]], confidence=medium]
- [[Cal Newport's Deep Work Method Involves Rigorous Time Blocking to Maximize Concentration]]—_The deep-work reasoning behind protected, single-task blocks._ [supports:: [[Cal Newport's Deep Work Method Involves Rigorous Time Blocking to Maximize Concentration]], confidence=medium]
- [[The Time Management Matrix (Eisenhower Matrix)]]—_Step 1 of the guide's process ranks tasks with this matrix._ [depends_on:: [[The Time Management Matrix (Eisenhower Matrix)]], confidence=medium]
- [[Estimating Time for ADHD (Tripling Estimates)]]—_Why block estimates should be padded, which the 25% buffer rule addresses._ [supports:: [[Estimating Time for ADHD (Tripling Estimates)]], confidence=medium]
