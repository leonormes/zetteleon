---
aliases:
- Big Rocks
- Weekly Big Rocks
- Big Rock Proposal
conformant: true
created: 2026-11-16T13:00:00+00:00
modified: 2026-11-17T10:16:40+00:00
permalink: llmeon/30-library/100-zettelkasten/protocol-big-rocks-weekly-quadrant-ii-outcomes
project_category: prodos
status: draft
tags:
- gtd
- productivity
- protocol
- TheHuman/Health/ADHD
title: Protocol - Big Rocks (Weekly Quadrant II Outcomes)
type: protocol
---

> [!abstract] The rule in one paragraph
> A Big Rock is one finishable outcome for the week that matters but is not yet urgent. Leon never has to hold the list in his head or invent it: the Chief of Staff (CoS) proposes up to three on the first working day of the week, Leon answers accept, swap or reject, and the rock then lives in Todoist as a parent task whose subtasks `/daily-plan` schedules first.

## Definition

A Big Rock is a weekly Quadrant II (Important, Not Urgent) outcome aligned to a Horizon of Focus or a strategic project. It is never a reactive Quadrant I crisis. [[The Time Management Matrix (Eisenhower Matrix)]] gives the quadrants and [[Habit 3 - Put First Things First]] gives the reason to protect this work.

- A Big Rock is an outcome, not a task. It is phrased as a finishable state ("Draft of the FTFL-xxx design reviewed"), and one or more Todoist next actions move it forward.
- Todoist priority does not mark a Big Rock. Priority carries urgency, so p1 mostly picks out Quadrant I and III work.
- Anything urgent and important is not a Big Rock. Handle it as a hard-landscape commitment ([[gtd-action-system]]).

## Cap

At most 3 Big Rocks per week. Trigger the reduced cap of 1–2 Big Rocks deterministically when existing fixed calendar commitments leave < 20 hours of open work capacity for the week (otherwise cap at 3 Big Rocks). The CoS measures the open blocks from the calendar (see [[Protocol - Daily Plan (Todoist Timeboxing)]] for the source), states the figure, and Leon can override it. The cap exists because a list longer than three stops being a list of priorities.

## Zero-Blank-Page Monday Proposal

Leon is not asked to think up Big Rocks. [[SoT - Prosthetic Executive Function]] explains why: choosing from nothing is the step where executive function is weakest.

- Trigger: `/daily-plan` runs on Monday or the first working day of the week, and there are no Big Rock parent tasks in Todoist for the week.
- Inputs the CoS reads: active vault projects (`project_status: active` in `30_Library/200_Projects/`), Horizons of Focus as recorded in [[gtd-action-system]], Jira tickets assigned to Leon, the Todoist runway, and `[[MOC - ADHD Experiments & Protocols]]` plus any active `experiment` `HEAD` note in `20_Thinking/21_Workbench/` (e.g. `[[HEAD - Do 75m Deep Dive Sessions Outperform Granular Next Actions for ADHD?]]`).
- Experiment alignment (scientific loop): Review/update the active experiment's evidence from last week (or promote the next candidate from `[[MOC - ADHD Experiments & Protocols]]` if settled via `[[How to Test an ADHD Scaffold Using ABAB Withdrawal]]`), and frame this week's Big Rock execution as a controlled test of that hypothesis rather than ad-hoc "whatever feels best".
- Output: up to 3 candidates, each with an outcome in finishable wording, the source it came from, and a time estimate in minutes.
- Decision: a binary choice per candidate, which is accept, swap (name a replacement) or reject. Nothing is created until Leon answers.
- This sits in `/daily-plan`, not in [[Protocol - Weekly Command Centre]]. That protocol is deliberately a 10-minute floor and must not grow until it has been run four Fridays in a row.

## Alignment and scheduling

Once accepted, the CoS does the following through [[Protocol - Daily Plan (Todoist Timeboxing)]]:

1. Creates each rock as a parent task in the Todoist Work project, section `Big Rocks`, titled `BIG ROCK: <outcome>`, with `Estimate: <minutes> min` in its description. A Todoist duration needs a date and time, so the estimate lives in the description.
2. Adds physical-verb starter actions as subtasks of the parent through the Todoist MCP. An existing runway task can be moved under the parent instead.
3. Sets a date, time and duration on a subtask only when the daily plan reaches it.
4. Schedules aligned tasks first each day, immediately after Renewal and before other actions.

## Visibility

Every `/daily-plan` output shows `Big Rock time planned: X of Y minutes`.

- `X` is the cumulative weekly minutes of `duration` scheduled on subtasks of this week's Big Rock parents (including today).
- `Y` is the sum of the `Estimate` values on those Big Rock parent tasks.
- With no Big Rocks set it reads `0 of 0 minutes (none set)`, and the CoS says so instead of leaving a gap.

The line makes neglect visible without Leon tracking anything.

## Settled parameters

Decided 2026-11-17:

- **Week Start Day**: Locked to Monday (`weekStartDay` = Monday), aligning with the Monday CoS candidate proposal and the Friday 16:30 [[Protocol - Weekly Command Centre]] floor.
- **Reduced Cap Threshold (1–2 Big Rocks)**: Triggers deterministically when existing fixed calendar commitments leave < 20 hours of open work capacity for the week (otherwise cap at 3 Big Rocks).
- **Visibility Metric (`X of Y minutes`)**: Locked to `X` = cumulative weekly minutes of `duration` scheduled on subtasks of this week's Big Rock parents (including today), and `Y` = sum of the `Estimate` values on those Big Rock parent tasks.

## Related

- [[Habit 3 - Put First Things First]]—_The principle: put first things first, and schedule the big rocks first._ [depends_on:: [[Habit 3 - Put First Things First]], confidence=high]
- [[The Time Management Matrix (Eisenhower Matrix)]]—_Defines Quadrant II, which a Big Rock must sit in._ [depends_on:: [[The Time Management Matrix (Eisenhower Matrix)]], confidence=high]
- [[Protocol - Daily Plan (Todoist Timeboxing)]]—_Runs the Monday proposal and schedules Big Rock subtasks first._ [supports:: [[Protocol - Daily Plan (Todoist Timeboxing)]], confidence=medium]
- [[SoT - Temporal Management (Blocking and Boxing)]]—_The timeboxing technique that places Big Rocks first on the calendar._ [depends_on:: [[SoT - Temporal Management (Blocking and Boxing)]], confidence=medium]
