---
created: 2026-06-02 00:00:00+00:00
modified: 2026-06-08 11:49:24+00:00
project_category: prodos
project_name: ProdOS
project_status: active
source: Distilled from the processing note "HEAD — Gaining Control The 5 Stages of
  Work Flow" (Claude + Gemini sessions, 2026-06-02)
status: active
tags:
- 5
- gtd
- jira
- obsidian
- productivity
- system
- todoist
- workflow
title: gtd-action-system
type: practice
permalink: llmeon/30-library/200-projects/gtd-action-system
---

> [!abstract] The system in one paragraph
> Three tools at three altitudes, plus a calendar. Obsidian holds knowledge and personal project thinking. Jira holds work outcomes and status. Todoist holds the single next physical action across all of life—a flat, fast _runway_. The native calendar holds only date-specific commitments (the _hard landscape_). The job of the system is to finish your thinking _once_—externalising both the outcome and the next action—so that when you sit down to work, the runway is a menu of executable sparks and your brain can simply act.

---

## Part 1—The Architecture

### The Four Tiers

| Tier | Tool | Holds | GTD term |
|---|---|---|---|
| Knowledge | Obsidian | What you know, think, claim; personal-project brainstorming and outcomes | The "extended mind" / personal 10,000-ft support |
| Outcomes (work) | Jira | Work results, status, acceptance criteria, "is it done" | Projects list (work), 10,000-ft view |
| Actions | Todoist | The single next physical action, across _all_ of life | The runway |
| Hard landscape | Native calendar | Only date/time-specific, must-happen commitments | The calendar |

### The Rule that Kills the Jira/Todoist "duplication"

The overlap between Jira and Todoist _feels_ real but is an illusion—they sit at different altitudes:

- Jira says _what_ / _whether-done_.
- Todoist says _what-I-touch-next_.

Therefore:

- Todoist never mirrors Jira. It holds only the single next physical action per active ticket—never the ticket itself.
- At most one open Todoist task per active ticket. (If a ticket is already atomic, a 1:1 mapping is fine—most are not.)
- Finish the action → reopen the ticket → define the _next_ next action → write _one_ new Todoist line.

They cannot drift, because they describe different things. Nothing to sync.

---

## Part 2—Core Principles

_The breakthroughs from the sessions, each stated once._

### 1. Clarifying is the Engine Room

Every captured item has two halves, and both must be externalised:

- The anchor (desired outcome). What does "done" look like? Pushed into Jira (work) or Obsidian (personal).
- The spark (next action). The next physical, visible step. Pushed into Todoist.

The classic failure mode—and your named trap—is writing a fragmented action while leaving the _why_ and the _finish line_ in your head. That forces your brain to re-clarify the task every time it sees the list, which is precisely the friction that produces stall.

### 2. The next Action is a Spark, not a Plan

You do not tick off next actions all day like a robot. The next action exists to drop the barrier to entry so low you cannot say no—it is _kindling_, a _task starter_. Once it gets you moving, momentum takes over and you carry on organically ("Captain and Commander" mode: light touch on the tiller, adjusting as you go).

You only return to your lists when:

- you hit a hard roadblock and must define the _new_ next action, or
- you finish a sprint and switch to a different project, or
- you lose perspective and need to capture fresh thoughts.

As long as you are flowing, keep flowing. The system is there to catch you when you stop.

### 3. Capture and Clarify Are Two Different Concerns

Conflating raw "stuff" with clarified next actions is the single biggest source of overwhelm. Treat Todoist as two zones with a hard boundary:

- Inbox = raw capture. Ambiguous stuff is _only_ allowed here. You are not permitted to work from it.
- Runway = clarified actions. Only items that have survived the Clarify stage live here.

### 4. Flatten the Runway

Nested projects, intricate labels and elaborate filters are the Micromanager trap—form overtaking function, where you tweak the system instead of playing the bigger game. Because outcomes now live in Jira and Obsidian, Todoist is freed of intellectual baggage and can be flat and fast. Organise by context (how/when you can act), not by project tree.

### 5. Metadata Minimalism

In a flat runway, tagging an item `@project` or `@next_action` is like labelling every item in the fridge "food". Redundant. Actionability is determined by location, not by a tag:

```
!#Inbox & !#Someday & !#Waiting
```

Anything outside those three buckets _is_ a clarified next action, by definition.

### 6. Dates Are the Hard Landscape only

- Assign a due date only if there is a real-world negative consequence on that specific day (_"Pay vehicle tax by midnight"_).
- A true next action is a date-free, ASAP item—done as soon as you have the time, energy and context.
- Arbitrary "wish-list" dates destroy trust: you start dragging tasks forward day after day and the list stops being believed.
- Consequences already applied: the Todoist → Google Calendar sync was severed; Fantastical was rejected (no Android support, and its task-on-calendar feature reintroduces exactly this trap).

### 7. GTD is an Executive-function offload—not anti-ADHD

The belief that GTD demands you map every step upfront is the misconception that makes it feel overwhelming. Done correctly, the system _offloads_ the working-memory burden your brain handles poorly. Refusing to over-plan is working _with_ the ADHD brain, not against it.

---

## Part 3—The Workflow in Practice

The five GTD stages mapped onto your tools.

### Capture → Todoist Inbox

Todoist is the capture engine because it is everywhere: Global Quick Add, natural-language parsing, and Ramble voice-to-text. A newly assigned Jira ticket is an open loop—drop a placeholder (e.g. _"Review newly assigned IP ticket"_) into the Inbox.

### Clarify → Empty the Inbox (daily)

For each item, ask "Is it actionable?"

- No → trash it, file as reference (Obsidian), or park on Someday.
- Yes → define the outcome (Jira or Obsidian) _and_ the next physical action (Todoist).

Routing decisions:

| If the item is… | Route to… |
|---|---|
| Resolvable in under 2 minutes | Do it now, then delete the capture |
| A work bug / feature | Draft a Jira ticket, then delete the capture (add a clean starter back if _you_ take the first step) |
| A complex personal project | Open an Obsidian note, brainstorm there, delete the capture |
| Already a clear physical step | Leave as a Todoist task starter (add a prefix for scanning) |

### Organise

Flat projects + context labels. Delegated items → Waiting. Only true time-bound commitments → the calendar.

### Review → the Weekly Review

The keystone habit. Cross-reference every open Jira ticket against Todoist and ensure each active ticket has a corresponding next action or Waiting item. Empty your head. _(See open question 5—not yet scheduled.)_

### Engage

Trust the runway, because the heavy thinking is already done. Choose by context, time, energy and priority—then drop into flow.

### Task-writing Conventions

Bind every action to its "why" using one of:

1. Prefix—`[Merge Train] Message the engineering channel about the pipeline failure`
2. Verb–Asset–Outcome (self-contained)—`Log into Azure to check the logs for the private network routing bug`
3. Description-field link—Title is the strict next action; description carries `Outcome: … / Reference: [Obsidian note] / [ticket]`

> [!tip] The Golden Rule of the runway
> Never let an item live on the runway unless it starts with a physical, high-momentum verb: Draft, Call, Open, Type, Read, Message, Run. If it starts with _Plan_, _Sort out_, _Improve_ or _Have a look at_, it is an unclarified project wearing a task's clothes.

---

## Part 4—Current Implementation State

What "Dave" (your Todoist-connected LLM) has already built. The architecture is done.

### Project structure—flat, 7 Nodes

```
Inbox
├── Personal
├── Family  (+ Shopping list sub-project — intentional)
├── Work
├── Waiting
└── Someday
```

Deleted: `🎯AoF`, `Education`, `Family Chores` (19 chore tasks migrated into Family).

### Operational labels—9 only

- Context: `@computer`, `@home`
- Flag: `@question`
- GTD bucket: `@waiting`
- Affinity: `@work`, `@personal`
- Family: `Rae`, `Bessie`, `Pearl`

Purged: `@project`, `@next_action`, `@deep_work`, plus ~11 dormant labels and all casing duplicates (`Computer`/`computer`, etc.).

### Filters—actionability-first

All operational filters were rewritten to anchor on `!#Inbox &!#Someday &!#Waiting`, removing the dead `@project` / `@next_action` dependencies.

### The Master Next-action Filter

The single view that shows absolute truth—every ASAP action on your runway, nothing else:

```
!#Inbox & !#Someday & !#Waiting & no date
```

---

## Part 5—Reference: Canonical GTD (condensed)

A keep-forever refresher so you needn't re-read Allen.

### The 5 Stages of Workflow

1. Capture—collect everything pulling on your attention into a trusted external place.
2. Clarify—process each item: _Is it actionable?_ If yes, decide the outcome and the next action.
3. Organise—park results in the right lists: Projects, Next Actions (by context), Waiting For, Calendar.
4. Reflect (Review)—keep the system current and trusted; the Weekly Review is the critical habit.
5. Engage (Do)—make trusted choices about what to do now, given context, time, energy and priority.

### The 6 Horizons of Focus

- Runway—concrete next physical actions.
- 10,000 ft—current projects (short-term outcomes).
- 20,000 ft—areas of focus and responsibility (roles, standards).
- 30,000 ft—goals and objectives (3–24 months).
- 40,000 ft—vision (3–5 years).
- 50,000 ft—purpose and principles (core values).

### The Natural Planning Model

For anything needing more than a single next action:

1. Purpose & principles → 2. Vision / outcome → 3. Brainstorm → 4. Organise → 5. Next actions.

---

## Open Questions / Unresolved Decisions

Genuinely undecided in the transcript—flagged here rather than left buried.

Polish (small decisions, not blockers)

1. The redundant `@work` / `@personal` labels. Tasks already live in the `#Work` / `#Personal` projects, yet these labels survived the purge and still appear in filter logic (e.g. `& personal`). This is the _same_ redundant metadata the purge was meant to remove. Decide: drop the labels and rely on project location, or keep them for cross-project filtering?
2. The role of `@question`. It survived but its job is undefined—context, or task-type flag? It sits slightly outside the "actionability by location" model.
3. The family labels (`Rae` / `Bessie` / `Pearl`). Retained as "family assignments", but their function is unpinned—delegation (→ should they feed `@waiting`?), agendas, or shared-task ownership?
4. Context granularity. The sessions floated `@terminal` / `@gitlab` as a deep-focus context, but the final stack kept only `@computer`. Decide: is `@computer` granular enough, or do you want a deep-work context back?

Habit design (matters for trust; quick to set)

1. Daily clarify cadence. "Empty the Inbox once a day" is asserted but no trigger or time is committed. (Gemini asked repeatedly; never answered.)
2. The Weekly Review. Named as the keystone habit but never actually scheduled or defined for _your_ week.
3. The Todoist → team-comms loop. When you tick a Todoist action, how does the Jira ticket / Slack get updated? Undefined.

Not design—the actual work the system was built to do

1. The "terrible" `@Work Next` list. It is full of amorphous projects—_"Security needs more rigour"_, _"The pipeline needs improving"_, _"Plan stress testing"_. These were diagnosed and the rewrite was _started_ but never finished. This is live clarifying, not a design question.
2. The stuck Inbox. ~7 of the 12 Inbox items are well-scoped work next-actions sitting without a home or label. Pure processing; never completed.

---

## The Verdict—Open Questions vs. Committing

> [!success] You asked: open questions, or just commit?
> The architecture is finished and already implemented. There is no more system to design.

- Items 1–4 are cosmetic polish—minutes of decision, not blockers.
- Items 5–7 are habit design (cadence, review, comms). They matter for trust, but each is a quick, one-off setup.
- Items 8–9 are not design at all. They are the GTD work—clarifying—that you built this entire machine to do.

So it is roughly 90% committing, 10% loose ends. And the honest pattern worth naming, without judgement: the _system-building_ was the novel, interesting part—and it is done, well. What remains is the un-novel _doing_. The gap now is execution, not design. Every further hour spent refining the system instead of clarifying one item is the displacement to watch for.

The cheapest possible proof that the system works is a single clarified item lighting up your `@Work Next` filter.

---

## Your Next Physical Action

> [!todo] One item. That is the whole ask.
> Open Todoist → Inbox → take the single easiest item → rewrite its title so it begins with a physical verb (Draft / Open / Call / Read / Message / Run) → tap it into Work or Personal.
>
> Stop there. One item is the entire instruction—it instantiates the whole architecture in under two minutes.