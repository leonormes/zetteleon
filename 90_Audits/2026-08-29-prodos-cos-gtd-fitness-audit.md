---
conformant: true
created: 2026-08-28T23:00:00+00:00
modified: 2026-08-29T10:49:50+00:00
non_conformance_reason: ''
permalink: llmeon/90-audits/2026-08-29-prodos-cos-gtd-fitness-audit
tags: [1, adhd, audit, cos, executive-function, gtd, prodos]
title: 2026-08-29-prodos-cos-gtd-fitness-audit
type: note
---
> [!warning] Superseded in part — see [[2026-08-29-execution-vs-thinking-boundary]]
> This audit treats ProdOS as one system. It is two: an **execution** system (GTD, CoS, EF prosthetic) and a **thinking** system (PKM, Zettelkasten, synthesis). Two findings below are miscategorised as a result:
>
> - **§4 (journal collapse)** is not ProdOS degrading. It is the execution system winning a substrate it shares with the thinking system. Nothing malfunctioned.
> - **§7** scores "Daily dump / Thinking Stream" as a failed EF-prosthetic component. It belongs to the other system and should not be judged by prosthetic criteria.
>
> The behavioural findings in §3 (bulk dismissal, On Stop, the anti-pattern) are execution-side and stand unchanged.


## ProdOS CoS & GTD—Fitness Audit Against Evidenced Need

> Output Contract: [[Protocol - Typed Answer Contract (TAC) for Vault Agents]]. Confidence stated per section; evidence linked; uncertainty flagged in §8.

---

## Verdict

The diagnosis in ProdOS is sound. The design has diverged from the need in one measurable way: every component that is scripted works, and every component that requires you to write something at a specific moment has failed—without exception.

The failed components are all on the _closing_ half of the loop. That matters because your own most-repeated, most-specific self-report is not about starting. It is about returning.

ProdOS is, right now, an authoring prosthetic. It is not yet an executive-function prosthetic, because the executive function it externalises is the half you were already doing.

Confidence: high on the behavioural findings (§3, §5—direct Todoist/journal/filesystem data). Medium on the causal reading in §4.

---

## 1. What You Actually Report—First-person Evidence

Filtered to notes where you write in first person about your own experience, not general ADHD literature.

| #   | Difficulty                                            | Your words                                                                                                                               | Source                                                                          |
| --- | ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| 1   | Continuity / project return                           | "I always want to start again… When I come back to it my thoughts are no longer wrapped up in it and it doesn't have that same feeling." | [[My Main PKM Problem Is the Continuity of Thinking]]                           |
| 2   | Shame drives the system-building                      | "my obsession with GTD and Zettelkasten and trying to understand everything is driven by my shame."                                      | [[I have a lot of shame about my life]]                                         |
| 3   | Non-acceptance of the diagnosis                       | "I still see it as me being lazy, or incompetent… I am refusing to allow these things to be an excuse."                                  | [[I Have Not Really Accepted the ADHD Difficulties I Have Had]]                 |
| 4   | Missing workflow adds friction _on top of_ initiation | "As I don't have one there is extra resistance to capturing and processing on top of my normal ADHD task initiation woes."               | [[My Main PKM Problem Is the Continuity of Thinking]]                           |
| 5   | Mundane tasks return no dopamine                      | "I can't do little, detached tasks. So building habits is a bust."                                                                       | [[MOC - Procrastination Triggers]]                                              |
| 6   | Disengagement is approach-avoidance, not residue      | Lingering in the resolved "green" state to avoid re-entering the dissonant one; plus post-focus fatigue.                                 | [[ProdOS CoS & ADHD Task-Authoring Protocol]] (your correction to the research) |
| 7   | You have not measured the proportions                 | "Don't theorise the proportions—measure them." Position dated 2026-05-31, confidence: low.                                               | [[Q — What Am I Actually Struggling With]]                                      |

### The Central Divergence

Items 1 and 4 are your most specific and most repeated complaints. They are about _return_, not _start_.

ProdOS is built almost entirely around _start_:

- [[SoT - PRODOS Core Specification]] §3.2—MVA, activation energy → 0
- [[SoT - Protocol - The Launch Sequence]]—"bypassing initiation paralysis"
- PINCH model—task engagement
- [[ProdOS CoS & ADHD Task-Authoring Protocol]] §3—all three named mechanisms (DMN paralysis, delay discounting, attention residue) are initiation-or-switching mechanisms

The continuity problem has exactly one canonical note—[[SoT - Breaking the Creation Cycle]], with a fully specified Session Snapshot and Re-entry Ritual—and it is not wired into the CoS at all. The CoS knows which repo, branch and ticket you last touched. It generates nothing from that.

You also hold the honest hedge yourself: [[ADHD Task Initiation is Not Universally the Hardest Symptom Due to Individual Variation]]. You wrote the counter-argument to your own system's premise and then built the system on the premise anyway.

---

## 2. What the Protocols Currently Claim

| Document | Created | Role |
|---|---|---|
| [[gtd-action-system]] | 2026-06-02 | The GTD architecture—four tiers, flat runway, metadata minimalism |
| [[SoT - Execution Protocol (GTD & PARA)]] | 2026-01-08 | PARA/GTD harmonisation, Definition of Done |
| [[Protocol - Action-First GTD (LLM Chief of Staff)]] | 2026-02-11 | "Dump, Don't Organize"—human generates, LLM organises |
| [[Protocol - Weekly Command Centre]] | 2025-12-20 | The system reset ritual. Status: `stable` |
| [[ProdOS CoS & ADHD Task-Authoring Protocol]] | 2026-08-26 | CoS Query Engine + the six-field authoring gate |
| [[Operating Protocol for High-Friction Engineering Work]] | 2026-05-15 | Five-layer operating protocol (daily/weekly/session/project/stall) |
| [[SoT - PRODOS Core Specification]] | 2026-01-03 | The kernel |

325 notes in the vault mention ProdOS. 336 SoT notes exist. The corpus is large enough that divergence is the expected state, not a surprise.

---

## 3. Behavioural Evidence—Todoist, August 2026

62 completions in the Work project, 1–29 August. Real work is happening. But the shape of it is diagnostic.

### 3.1 Bulk Dismissal, not Execution

24 of 62 completions (39%) occurred in bursts of three or more within a single minute.

| Cluster | Tasks | Window |
|---|---|---|
| 2026-08-27 09:39:13–09:39:48 | 14 | 35 seconds |
| 2026-08-26 14:34:32–14:34:34 | 4 | 3 seconds |
| 2026-08-26 09:00:38–09:00:47 | 3 | 9 seconds |
| 2026-08-18 17:38:53–17:38:59 | 3 | 6 seconds |

The 3-second cluster on 26 August is the important one. It contains all four of the tasks the six-field gate was built to be validated on—FTFL-868, FTFL-619, FTFL-942, and the ArgoCD task. Including the ArgoCD task, which §7 of your own protocol had declared _"⚠ Incomplete—blocker masquerading as a task… Not startable until the Application is named."_

The protocol's §9 immediate next step was: _"test one task this week (FTFL-868) and report: did the six-field gate pull you in more? did the If-stuck blocker occur?"_

That test was never run. The task was swept.

### 3.2 "On Stop" Has never been filled

Six of the 62 completions carried a full six-field description and therefore _had_ an On Stop field: FTFL-868, FTFL-619, FTFL-942, the ArgoCD task, and the two drydock tasks of 28 August.

0 of those 6 was filled. Every one still carries the untouched placeholder—`On Stop: done / not done — blocker — next step`.

This is the field §4 designates as the Ready-to-Resume mechanism, and the field §8 designates as the _safeguard against the cognitive-offloading risk_: "the On-stop field captures what you did, not just whether; reviewing those notes builds metacognitive awareness."

The safeguard is inert. It has never once operated.

### 3.3 The Named Anti-pattern is Still Being Generated

15 of 62 completions (24%) were `"Check status of X — re-assess next steps"`—the exact wording §6 names as the founding failure ("asking you to redo the executive-function deciding at the moment the task should have done it for you").

Timing matters: the protocol was consolidated 2026-08-26 at 07:16. These tasks were generated at 15:48 that same day, and again on 27 August. The spec was written and then violated within nine hours by the pipeline it governs.

### 3.4 Duplicate Generation

FTFL-938 appeared three times (completed 25th, 26th, 27th). FTFL-903 three times (24th ×2, 25th). This violates [[gtd-action-system]] Part 1: _"At most one open Todoist task per active ticket."_

### 3.5 The Contrast case—what Working Looks like

2026-08-11. Eight tasks, authored in one batch the previous evening, each with a long, specific, context-rich description. Completed across the day at 07:31, 09:26, 09:32, 10:31, 10:58, 11:15, 15:21, 15:22.

That is genuine execution spacing. Those tasks had no six-field template at all.

### 3.6 The Discriminator is not the Template

FTFL-868, FTFL-619 and FTFL-942 had all six fields, written well, and were dismissed in three seconds. The 11 August batch had no template and was worked all day.

What the 11 August batch had that the others did not: you were in the conversation that produced them, they formed one coherent thread, and they were your live problem at that moment.

> Working claim (medium confidence): task _executability_ is being driven by authoring provenance and thread-coherence, not by task structure. The six-field gate improves the artefact; it does not appear to improve engagement.

This is falsifiable and worth testing before more is invested in the gate.

---

## 4. The Journal Collapse

Human-authored lines in the daily note, excluding frontmatter, Templater code, and machine `CoS Gather`/`CoS Run` blocks:

| Month | Days | Days with human text | Human lines | Machine lines |
|---|---|---|---|---|
| 2026-04 | 30 | 29 | 82 | 0 |
| 2026-05 | 30 | 7 | 71 | 122 |
| 2026-06 | 28 | 4 | 49 | 576 |
| 2026-07 | 30 | 8 | 126 | 3 |
| 2026-08 | 29 | 2 | 12 | 192 |

In August the daily note is 94% machine, 6% human, across two days out of twenty-nine.

This is load-bearing, because three protocols take the daily note as their input:

- [[Protocol - Action-First GTD (LLM Chief of Staff)]]—_"Dependency: Requires a 'Daily Dump' note in Obsidian."_ The whole algorithm starts there.
- [[SoT - ProdOS Thinking Stream]]—_"CAPTURE: Dump mental noise into the Daily Note."_
- The CoS `--journal` step, which writes _into that same note_.

The machine now occupies the space the human input was supposed to fill. And the single most revealing data point in this audit is that one of the only two things you wrote in August was a complaint about exactly this:

> "I don't like the masses of text or adds to daily note. Seems pointless."—2026-08-25

You diagnosed it yourself, in the one place you still write, on one of the two days you wrote.

---

## 5. Internal Consistency—Divergences Found

| # | Divergence | Evidence | Severity |
|---|---|---|---|
| 1 | The atomic unit of action is defined four incompatible ways—<120s MVA ([[SoT - ProdOS Thinking Stream]], [[SoT - PRODOS Core Specification]] §3.2); 5–15 min ([[The Three Rules of Starter Tasks]]); ≤15m CoS starter task; 75-minute Deep Dive block ([[Deep Dive Sessions for ADHD (Adapted GTD Next Actions)]])—plus GTD's 2-minute rule | Four SoT-tier notes | High—the system cannot state what "a task" is |
| 2 | "At most one open Todoist task per active ticket" vs CoS duplicate generation | [[gtd-action-system]] Pt 1 vs §3.4 above | High, live |
| 3 | "Never let an item live on the runway unless it starts with a physical, high-momentum verb… _Plan / Sort out / Have a look at_ = an unclarified project wearing a task's clothes" vs _"Check status of X—re-assess next steps"_ | [[gtd-action-system]] Golden Rule vs §3.3 | High |
| 4 | Todoist Inbox is capture-only—"You are not permitted to work from it"—vs CoS pushing `⚠ unclarified Source: The New Stack` into the Work runway | [[gtd-action-system]] Pt 2 §3 | Medium |
| 5 | Metadata minimalism / flatten the runway vs six-field descriptions + `cos-sweep` label + priorities + timeboxes | [[gtd-action-system]] Pt 2 §4–5 | Low-medium—probably reconcilable (description ≠ label), but unreconciled in writing |
| 6 | The weekly review is named the keystone habit in three documents, has a complete protocol at `status: stable` since 2025-12-20, and has never run | 0 mentions across all journals; no recurring review task exists in Todoist (only bins, Monoro, Fluox) | Critical |
| 7 | The role split has silently inverted. [[SoT - PRODOS Core Specification]] §1.1: _"the human as the Problem Definer and the system as the Executor."_ The CoS now defines the problems—it generates the tasks—and you execute or dismiss. Nothing in the corpus records this inversion. | Core Spec vs CoS §5 pipeline | High—this is §8's offloading risk, already realised |

---

## 6. Your Own Vault Predicted This

[[Operating Protocol for High-Friction Engineering Work]], written 2026-05-15. §4.9 lists four symptoms of protocol decay. All four are currently true:

| Symptom (your words) | Current state |
|---|---|
| "No weekly review for three weeks running" | 15 weeks. Never scheduled. |
| "WIP back at 4+" | 5–7 open Jira, 13 dirty repos, 4 unpushed, multiple parallel streams |
| "`inbox.md` is a wall of unprocessed lines" | 47KB research note unprocessed in `00_Inbox` since 11 August |
| "Sessions starting without pre-flight" | No pre-flight evidence anywhere in the corpus |

And the prescription you wrote for that exact state:

> "When you notice decay, don't restart from zero with a new protocol. One weekly review fixes it. Restarting from zero is its own avoidance pattern."

What was built between 15 May and now: the CoS Query Engine, `cos-sweep.py`, `cos-gather.py`, `cos-prioritise.py`, `cos-context.py`, the six-field gate, drydock integration, a GitKraken/Kepler evaluation, and the ADHD Prosthetic Executive Function research pass.

That is a restart from zero. Your own document named it in advance as the avoidance pattern—in a section titled §4.10 The Over-engineering Trap, which closes: _"The protocol as written is sufficient. Do not iterate it."_

Its §5 asked for one thing: _"When this week is my weekly review going to live? Pick a 30-minute slot, put it in your calendar now, recurring weekly."_

Fifteen weeks. Not done.

This is not a character observation. It is the [[I have a lot of shame about my life]] mechanism operating exactly as you described it, and [[Tool tinkering is a form of productive procrastination]] and [[System Tweaking as a Form of Procrastination in ADHD]] are your own names for it. The system-building is the novel, interesting, dopamine-returning work. The review is the un-novel work. Predictably, one happened and the other didn't.

Corroborating: your `#Someday` project holds nine items, all captured 2026-08-02, all PKM/Hermes meta-work, all still open, zero personal-life items. Including one you wrote yourself: _"Personal check: am I actually reading raw/ sources, or just trusting the wiki summaries?"_—with the note that you deliberately refused to make it a tracked field, because _"bolting a checkbox onto it would be the exact cognitive-offloading the video warns against."_

You were right. It is also still open.

---

## 7. Is This an Executive-function Prosthetic?

Judged against your own criterion in [[SoT - Prosthetic Executive Function]]: _"make desired behavior independent of internal state"_, one-time choice over recurring effort, _"a floor that sustains itself even if your internal executive control is zero."_

| Component | Type | Verdict |
|---|---|---|
| `cos-sweep` pipeline + cron | One-time choice (scripted) | ✅ True prosthetic |
| Todoist architecture—7 projects, 9 labels | One-time choice | ✅ True prosthetic—verified live and exactly as specified in [[gtd-action-system]] Pt 4 |
| Six-field task _authoring_ | One-time choice (scripted) | ✅ Prosthetic for the artefact |
| Drydock git-hygiene detection | One-time choice | ✅ Working—the 28 Aug tasks carried full descriptions and were completed ~2h after creation |
| "On Stop" capture | Recurring human effort | ❌ 0 / 6 tasks that had the field |
| Weekly review | Recurring human effort | ❌ 0 runs in 15 weeks |
| Daily dump / Thinking Stream | Recurring human effort | ❌ 2 / 29 days |
| HEAD note capture | Recurring human effort | ❌ 2 live notes, both work-technical; personal thinking notes stopped ~July; 11 stranded in `200_Projects` |
| Choosing which pushed task to actually do | Recurring human effort | ❌ Unsupported by anything |

Every scripted component works. Every component requiring you to write something at a moment of your choosing has failed. There is no counter-example in the data.

That is not a discipline problem. It is precisely what [[Claim - Stripping Away Systems Under-Weights the Need for Pre-Committed External Prosthetics]] predicts: asking for executive resource at the point of performance is architectural negligence—_and the CoS does this in four places._

### The Reframe

You describe the goal as "creating the LLM executive function prosthetic." The evidence says the LLM half is already working well. The failure is that the design keeps routing the critical steps back through a human writing action at the moment of depletion. More LLM capability will not fix that. Removing the human writing requirements will.

---

## 8. Where I May Be Wrong

- The bulk clusters may be legitimate. Fourteen git-hygiene tasks ticked in 35 seconds is plausible if the stashing and committing happened first in one terminal session and the ticking came after. → What would settle it: check commit/stash timestamps across those 13 repos around 2026-08-27 08:00–09:39. If the work exists, my reading is wrong _for that cluster_. The 26 August 3-second cluster still stands regardless, because the ArgoCD task was declared not-startable by the protocol itself.
- Pieces LTM is screen-capture weighted—heavily terminal/Obsidian/Todoist. I cannot see offline work, meetings, whiteboarding or thinking time. Low confidence on total time allocation.
- The journal figures are about the daily note specifically, as a designed input to three protocols. They are not a claim that you stopped thinking or writing—you clearly write a great deal, in Claude conversations and in Jira. The claim is narrower: _the designated input channel has gone quiet while three protocols still depend on it._
- Bulk `modified:` timestamps (2026-08-29T09:36) across the corpus mean modification dates are unusable for recency; I used `created` and behavioural data instead.
- §3.6 is a hypothesis, not a finding. n is small and provenance is confounded with thread-coherence and recency.

---

## 9. Three Changes—Not a Fourth System

Deliberately surgical. Per §4.9 of your own protocol, the correct response to decay is not a new protocol.

1. Stop asking for "On Stop". It has failed on every task that ever carried it—6 of 6, including all four the gate was built to prove. The CoS already reads git state, Jira transitions and Pieces signals—it can _infer_ the resume line and present it for one-tap confirm/correct. That converts a writing task at peak depletion into a decision at low demand, which is what [[SoT - Prosthetic Executive Function]] §3 actually prescribes.
2. Make the weekly review a machine-run event you attend, not a ritual you initiate. You have not initiated it once in 15 weeks across two protocol documents. Treat that as settled evidence, not a discipline failure. Minimum version: a cron that emits the §3.2 WIP=1 table pre-filled from Jira/git/Todoist, and pushes exactly one task—_"Read the review, name next week's one project."_
3. Re-point the CoS at continuity. Your 1 self-reported problem is return, not start. [[SoT - Breaking the Creation Cycle]] already specifies the Session Snapshot and Re-entry Ritual, and the CoS has all the inputs to generate them. Currently it generates none. This is the largest unexploited fit between what you've written and what you've built.

---

## 10. Next Action

> Open Todoist. Add one recurring task to `#Personal`: "Read the CoS review, name next week's one project"—every Friday, 16:00.
>
> Do not build `cos-review` first. The calendar slot is the thing that has been missing for fifteen weeks, and it is the single next action §5 of [[Operating Protocol for High-Friction Engineering Work]] asked for on 15 May.

One honest tension, flagged rather than hidden: this next action is itself a recurring human commitment, and §7 above argues those keep failing. The difference is that a recurring Todoist entry is an external trigger rather than an intention—and it takes under two minutes now, at a moment when your executive function is available. That is the design principle, applied to itself.

---

_Audit generated 2026-08-29. Sources: Todoist API (62 Work completions, 1–29 Aug), 29 daily journals, 325 ProdOS-referencing notes, Pieces LTM (127 events, 1–29 Aug), Todoist project/label/recurring-task state._
