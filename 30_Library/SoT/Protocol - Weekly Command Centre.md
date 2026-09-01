---
aliases: [The Floor, Weekly Command Centre, Weekly Reset, Weekly Review]
conformant: true
created: 2025-12-20T00:00:00+00:00
modified: 2026-08-31T15:01:22+00:00
permalink: llmeon/30-library/so-t/protocol-weekly-command-centre
tags: [gtd, productivity, protocol, system/reset, TheHuman/Health/ADHD]
title: Protocol - Weekly Command Centre
trigger: "Friday 16:30 — recurring Todoist reminder fires"
type: protocol
---

> [!warning] Read this before changing anything
> This protocol was cut down on 2026-08-31 from an 18-step, four-phase ritual to a 10-minute floor. It is deliberately smaller than you think it should be. Do not add anything to it until you have run it four Fridays in a row. Extending a protocol you have not yet run is system-building displacing doing—the exact pattern named in [[gtd-action-system]] §Verdict. The escalation ladder below tells you when you have earned the right to add a step.

## Minimum Viable Understanding (MVU)

The weekly review exists to make the system trustworthy, not to make the week tidy ([[The Purpose of a Weekly Review is to Restore Trust in Your System]]). A review you skip restores nothing, so the binding constraint is not thoroughness—it is whether it happens at all. This protocol therefore optimises for completion rate: a fixed environmental trigger, a hard 10-minute box, four moves, and a definition of done that a bad week cannot break.

---

## The Trigger

Not a time you choose. A cue that fires at you.

> If the Todoist reminder "Weekly Command Centre" fires at Friday 16:30, then I set a 10-minute timer and open Todoist → Completed.

That format is load-bearing: a specific observable cue paired with a first physical action requiring zero decisions ([[Implementation Intentions Elevate ADHD Response Inhibition Toward Neurotypical Levels]]). "Friday PM or Sunday AM" was a decision at the point of performance, which is where executive function is least available ([[SoT - Prosthetic Executive Function]]).

Setup, once: create a recurring Todoist task `Weekly Command Centre`—`every Friday at 16:30`, reminder on. Its completion history is your streak record. No other tracking.

---

## Tier 0—The Floor

Ten minutes. Four moves. This _is_ the protocol; everything below Tier 0 is optional extra.

### Move 1—Bank the Win (60s)

Do: Open Todoist → Completed → last 7 days. Read the list top to bottom.

Do not: judge it, count it, or compare it to what you intended.

Done when: you have read to the bottom of the list.

> Why it is first: the ADHD brain runs on rapid feedback, not retrospective virtue ([[Rapid Feedback Loops are Essential for ADHD Motivation]]), and visible evidence of progress bypasses the working-memory gap that makes a productive week feel like nothing happened ([[Externalizing Progress Makes it Tangible and Motivational]]). This move funds the other nine minutes.

### Move 2—Empty the Inbox (5 Min)

Do: Todoist Inbox only. Each item takes exactly one of four exits:

| Exit | Condition |
|:--|:--|
| Do it | Under 2 minutes |
| Runway | Rewrite the title to start with a physical verb (Draft, Open, Call, Read, Run, Message), drop into `#Work` or `#Personal` |
| Someday | Real, but not now |
| Delete | Be honest |

Do not: do the work. Clarifying is the work here ([[The Clarification Ritual (Stuff to Action)]]).

Done when: the timer rings or the Inbox is empty—whichever comes first. Overflow stays in the Inbox. It is captured, so nothing is lost, so nothing has failed.

### Move 3—One Action per Live Commitment (3 Min)

Do: Open Jira → assigned to me. For each active ticket with no corresponding line on the runway, write one physical-verb starter in Todoist.

Cap: three. Stop at three even if there are more.

Done when: three fixed, or none needed.

> This is the cross-reference [[gtd-action-system]] names as the weekly review's actual job. One Todoist line per active ticket—never the ticket itself. A commitment with no next action is the specific thing that makes a list untrustworthy ([[Weekly Review Verifies Project Actionability and Context]]).

### Move 4—One Friction Fix (60s)

Ask: _What one thing made this week harder than it needed to be?_

Write: one line in today's daily note—the friction, and the single 1% change to the environment.

> [!important] Audit the system, never the self
> If your answer is a sentence about your character ("I was lazy about X", "I keep avoiding Y"), you have answered the wrong question. Rewrite it as a sentence about the environment: what was missing, misplaced, unclear, or too many clicks away. Behaviour is a function of environment, and environment is the only half of that equation you can actually edit ([[SoT - Behavioral Architecture]]). A weekly ritual that ends in a verdict on yourself is a ritual you will learn to avoid.

Done when: one line exists in today's daily note.

---

## Definition of Done

Binary. No partial credit, no perfect version.

The review succeeded if Move 1 and Move 4 are done and the timer has rung.

Moves 2 and 3 are best-effort inside the box. They are the unbounded ones, so they are never what the streak depends on. Tick `Weekly Command Centre` in Todoist. Close the laptop.

---

## Standing Rules

1. Process, never produce. If you catch yourself doing a task, writing a note, or refactoring the vault, you have left the protocol.
2. The timer is the authority. Not the state of the list.
3. Overflow is safe. Anything unprocessed is still captured. Capture is the trust guarantee; processing is just throughput.
4. One pass only. No going back to improve a move you already finished.

---

## Escalation Ladder

The protocol grows on evidence, not on enthusiasm.

| When | What you may change |
|:--|:--|
| Weeks 1–4 | Nothing. Run it as written. |
| Inbox fails to empty inside the box 3 weeks running | Extend the box to 15 minutes. This is the _only_ permitted change before week 4. |
| After 4 consecutive clean runs | Promote one Tier 1 item. One. Then four more weeks. |
| After a missed week | Do not add anything. Run Tier 0 again. |

### Tier 1—Candidates (Promote oNe at a tIme)

- Waiting review—open `@waiting`, bump or close each item.
- Calendar look-forward—next 7 days only: identify hard constraints, block one deep-work session for the top project.
- One stale task—sort Todoist by oldest, take exactly one item older than 14 days, rewrite it or delete it.

### Tier 2—Not yet

Calendar look-back (past 7 days) · Obsidian project anchor check (60-second read of `## Current State`) · physical desk triage.

---

## What Was Removed, and Why

Kept here so the deletions are arguable rather than silent.

| Removed | Reason |
|:--|:--|
| Thinking Loop Closure (squash-and-merge `20_Thinking` into SoT) | That is intellectual work, not review—it violated the protocol's own "do not DO work" rule from inside the protocol. It belongs to [[Protocol - Workbench Compliance Sweep]] on its own cadence. |
| Obsidian `00_Inbox` flush | Vault ingest is a separate loop with its own router. Reviewing two systems in one sitting doubled the box and halved the completion rate. |
| The Ikigai check ("Eudaimonia or cheap dopamine?") | A values verdict attached to the end of a habit conditions avoidance of the habit. Shame reliably produces the avoidance it is meant to correct. Values review is worth doing—monthly, in its own note, where it cannot poison the weekly streak. |
| "Friday PM or Sunday AM" | A choice at the point of performance. Replaced by a fixed cue. |
| Phase ordering (reflection last) | The highest-value move was positioned where energy runs out. Move 1 and Move 4 are now the two cheapest and the two mandatory ones. |

---

## Open Risk

The honest weak point: a 10-minute box may not empty a large Inbox, and an Inbox that never empties does not restore trust. The bet is that a 60%-complete review that runs 40 times a year beats a 100%-complete one that runs 5 times, and that Inbox size falls on its own after three or four consistent runs. The escalation ladder's 3-week rule is the tripwire if that bet is wrong.

---

## See Also

- [[SoT - Execution Protocol (GTD & PARA)]]—_the Weekly Command Centre executes the Reflect stage of this hybrid workflow._
%%[implements:: [[SoT - Execution Protocol (GTD & PARA)]]]%%
- [[gtd-action-system]]—_the four-tier tool architecture (Obsidian / Jira / Todoist / calendar) this protocol reviews._
%%[depends_on:: [[gtd-action-system]]]%%
- [[The Clarification Ritual (Stuff to Action)]]—_this protocol scales the daily clarification ritual into a weekly reset._
%%[extends:: [[The Clarification Ritual (Stuff to Action)]]]%%
- [[SoT - Prosthetic Executive Function]]—_the design principle: offload the trigger and the boundary to the environment._
%%[implements:: [[SoT - Prosthetic Executive Function]]]%%
- [[SoT - Behavioral Architecture]]—_friction management and the System > Willpower axiom behind the fixed box._
- [[MOC - Why Task Initiation is Difficult in ADHD]]—_why the ramp, the cap, and the timer exist._
- [[MOC - Breaking the ADHD Overthinking-Procrastination Cycle]]—_the shame-avoidance loop the Ikigai check was feeding._
- [[Protocol - Workbench Compliance Sweep]]—_where the thinking-loop closure work went._
