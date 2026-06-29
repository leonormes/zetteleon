---
captured: 2026-06-01T21:16:25+01:00 2026-06-01T21:16:25+01:00
created: 2026-06-01 20:16:43+00:00
modified: 2026-06-05 22:09:50+00:00
source: https://claude.ai/chat/70c8d419-143e-425f-9d90-5413b8fa7ae7
status: processing
tags:
- input
title: HEAD Managing focus with ADHD amid competing priorities
type: head
permalink: llmeon/20-thinking/21-workbench/head-managing-focus-with-adhd-amid-competing-priorities
---

## Raw Output / Content

You

My work tasks are tracked on Jira. They are not next action oriented. My prodOS system and the GTD next action tasks I want to keep on todoist. The problem is it seems to be duplicating the job of tracking work. How can I consolidate the systems and have a single GTD next actions. What should I do to clarify

---

Gemini

The tension between corporate tracking tools and personal productivity systems is a classic problem. Jira is designed to track states, outcomes, and team visibility. Todoist is designed to track personal execution. When you try to make them do the same job, you end up doing double the administrative work.

To stop duplicating effort, you need to establish a strict separation of concerns between the two platforms.

## The Consolidation Strategy: Link, Don't Sync

Instead of copying the entire Jira ticket into Todoist, treat Jira as your GTD "Project List" and "Reference Material." Treat Todoist strictly as your "Next Actions" list.

| Platform | Role in GTD | Example |
| --- | --- | --- |
| Jira | The Project (Outcome) | `PROJ-104: Fix pipeline merge train skew` |
| Todoist | The Next Action (Execution) | `Read GitLab logs from Tuesday's failed pipeline (🔗 PROJ-104)` |

By only keeping the immediate physical action in Todoist and hyperlinking back to the Jira ticket, you maintain a single source of truth for the work's history (Jira) while keeping your daily focus uncluttered (Todoist).

## How to Clarify Jira Tickets into Next Actions

The GTD "Clarify" step is where you bridge the gap between a bulky Jira ticket and a truly executable task. If a task sits in Todoist and you find yourself resisting it, it usually means it hasn't been clarified into a true next action.

The secret to building strong task initiation habits is making the next action so undeniably small and specific that the friction to start drops to zero. Here is how to clarify your Jira workload:

1. Review your assigned Jira tickets daily. Treat your Jira queue as an inbox.
2. Ask the clarifying question. For each active ticket, ask: _"What is the very next physical, visible action required to move this forward?"_
3. Filter out the "planning" tasks. If the answer is "figure out the private network IP allocation," that is not an action; that is a mini-project. The true next action is likely "Draft an email to the network admin asking for the current IP subnet ranges."
4. Create the Todoist task. Write that specific next action in Todoist, starting with a strong verb (_Draft_, _Call_, _Review_, _Run_, _Read_).
5. Paste the Jira URL. Drop the link to the Jira ticket in the Todoist task description or directly in the task title.
6. Execute and Update. When you complete the task in Todoist, click the link, update the Jira ticket with your findings, and either close the ticket or clarify the _new_ next action back into Todoist.

## Preventing System Drift

To keep this ecosystem healthy, your GTD Weekly Review is critical. Once a week, you must synchronise the two systems:

- Sweep Jira: Are there any assigned tickets that don't have a corresponding next action in Todoist?
- Sweep Todoist: Are there any completed next actions that you forgot to update on the Jira side?

By maintaining this hard boundary, Todoist remains your sacred, fast-moving space for getting things done, while Jira remains the formal catalogue of your professional responsibilities.

Want to look at automating the handover from Jira to Todoist?

## Raw Output / Content

You

Today was a good example of my ADHD/attention distractibility. I had 1 thing to do, but then had a meeting about the sprint and had lots of different work assigned to me. After that, I couldn't focus on anything. That feeling of clarity is gone and I am stuck feeling unsettled and confused. It is the fault of the team not having enough people and the leadership not knowing how to prioritise. But I am responsible for what happens re my focus and productivity. What can I do

---

Claude

This is recoverable, and it's quick—five minutes, not a write-off of the day. And your read is correct: the org problem is real _and_ your focus is the lever you actually control. Hold both. Here's what's mechanically going on, then the single move.

### Why the Clarity Vanished

- You began the day with a loaded mental stack—the one task plus all the context around it. That state lives in working memory and is fragile.
- The sprint meeting wasn't just "more work." It was a context bomb: it reassigned priorities, which forced your brain to dump the stack and try to hold several new, undefined items at once.
- An ADHD working-memory profile rebuilds that loaded state slowly and holds multiple open items poorly. So instead of a fresh clear stack, you got thrash—every item half-loaded, none of them actionable.
- The "unsettled and confused" feeling _is_ that thrash. Your brain is rehearsing the open items on a loop because it doesn't trust they're recorded anywhere, so it refuses to let any of them go. That rehearsal is the noise.
- This is why "just focus" is impossible right now: there's no single thing to focus _on_ yet—only a cloud.

### The Fix, in One Principle

Get the cloud out of your head and onto a surface. The instant the items live somewhere your brain trusts, the rehearsal loop quiets, the noise drops, and you can pick one. Capture isn't admin—it's the thing that buys back the silence. And you already have the ideal surface open: Obsidian.

### The 5-minute Reset

1. Dump (~90 seconds). One note. List every item from the meeting _plus_ the original task. One line each, no order, no detail. You're emptying, not organising.
2. Anchor it. Find the original task—the one you had before the meeting—and mark it. That's where your clarity lived; that's home base.
3. Two buckets. Split the list into _Today_ and _Not today_. Be ruthless—most sprint assignments are Not today. Park the org/prioritisation frustration here too as a line like "raise prioritisation with \[lead\]"; it's a real conversation, just not this minute. Parking it stops it becoming a rumination loop.
4. Pick one—ideally the anchor task—and write its first physical action as a verb you could do in the next ten minutes.
5. Collapse the note so only that one action is left on screen.

### Right now—the only Thing You Do

Open a note in Obsidian, type a heading like `## Reset — 1 June`, and make the first line the one task you had before the meeting.

Then keep dumping the rest underneath—but that first line is the entire ask. Writing it down is you walking back to where you were standing when things were still clear.

---

You

My work tasks are tracked on Jira. They are not next action oriented. My prodOS system and the GTD next action tasks I want to keep on todoist. The problem is it seems to be duplicating the job of tracking work. How can I consolidate the systems and have a single GTD next actions. What should I do to clarify

---

Claude

The duplication is an illusion—and you already have the tool to see why.

Jira and Todoist _feel_ like the same job because both contain "things to do." But they sit at different altitudes, and that gap _is_ the resolution.

This is the same shape as the Single Source of Truth mechanism in your vault—except there, two notes genuinely cover the same content and you pick one canonical. Here the overlap is fake. Each tool is already a single source of truth, just for a different layer.

### Three Layers, Three Jobs, Zero Overlap

- Obsidian—knowledge. What you know, think, claim. Not tasks at all.
- Jira—outcomes & status. Work _results_; shared; the record of "is it done." In GTD terms, this is your Projects list for work.
- Todoist—next physical actions. The one move you make next, across _all_ of life—work, personal, prodOS. Your single GTD Next Actions runway. ✓ exactly what you asked for.

The key distinction:

- A Jira ticket is a project—an _outcome_ needing more than one action ("implement rate limiting"). It is not a next action.
- A next action is a physical, visible verb you could start in ten minutes ("sketch the middleware interface in a scratch file").

### The One Rule that Kills the Duplication

Todoist never mirrors Jira. It holds only the single next physical action per active ticket—never the ticket itself.

In practice:

- Ticket `PROJ-123 "Implement rate limiting"` stays in Jira as the outcome of record.
- Todoist gets _one_ line: `Sketch rate-limit middleware interface [PROJ-123]`.
- Finish it → reopen the ticket → define the _next_ next action → one new Todoist line.

Nothing to sync, because they aren't copies. Jira says _what / whether-done_; Todoist says _what-I-touch-next_. They can't drift—they describe different things. At most one open Todoist task per active ticket. (If a ticket is already atomic, it maps 1:1—fine, but most aren't.)

### Why This Dissolves Yesterday's Thrash

The cloud yesterday came from holding five undefined _outcomes_ in working memory. Under this split you don't hold them—Jira does. You promote one next action per active ticket, and "what do I do now?" has exactly one answer in exactly one place.

### One Guardrail

Designing this is structural and novel—easy to disappear into for an afternoon. The system is worth ~20 minutes, not a day. Don't build labels, contexts, or filters yet; prove the pattern with one ticket, refine only if it earns it.

### Your next Physical Action

Open one active Jira ticket. In Todoist, write its single next physical action as a verb with the ID in brackets:

`<verb> <object> [PROJ-XXX]`

That one line instantiates the whole architecture. You're not building a system—you're making one move.

---

Claude

Knowledge