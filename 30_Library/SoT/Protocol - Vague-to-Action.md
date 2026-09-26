---
aliases: [Task Decomposition Protocol, Vague-to-Action]
conformant: true
created: 2026-04-04T12:00:00+00:00
last-synthesis: 2026-04-04
modified: 2026-09-26T08:46:10+00:00
non_conformance_reason: ""
permalink: llmeon/30-library/so-t/protocol-vague-to-action
status: evergreen
tags: [execution, prodos, protocol, task-decomposition, task-initiation, TheHuman/Health/ADHD]
title: Protocol - Vague-to-Action
trigger: A captured task feels heavy or vague, or you notice you are avoiding it
type: protocol
---

## Objective

To convert "heavy" or undefined tasks that trigger avoidance into physical, binary actions that can be executed immediately.

---

## The Algorithm

### Phase 1: Define the Endpoint

1. Identify the Problem Statement: Write down the vague task exactly as captured (e.g., "Sort out taxes").
2. Define "Done": Describe a tangible, physical outcome that proves the task is finished (e.g., "A submitted PDF confirmation on the HMRC portal").
3. Name the Outcome: Give this outcome a clear project name in your system.

### Phase 2: Capture the Steps

1. Set a 5-Minute Timer: This reduces the perceived "bigness" of the planning phase.
2. Brain Dump: Write every question, idea, and micro-step without filtering.
3. Organize into Phases: Group the dump into 3-5 logical stages (e.g., Gather Docs, Data Entry, Review, Submit).

### Phase 3: Activate the MVA

1. Identify Phase 1: Look at the first group of steps.
2. Identify the MVA: What is the _very next physical action_?
    - It must be small, visible, and doable now (e.g., "Find the login password," "Create a folder named 'Taxes 2024'").
3. Commit: Write this single MVA on your 'Next Actions' list. The entire project is now represented by this one task.

---

## Unit Test

- Binary Outcome: Can you say "Yes/No" to whether the step is finished in < 120 seconds?
- No Planning: Does the step require further "thinking" or "deciding"? If yes, it is not an MVA.

---

## Why It Works

Each phase answers a specific reason a heavy task gets avoided.

- Phase 1, the endpoint. A task with no visible finish line has no boundary, so it feels endless. [[The Done State as a Boundary for ADHD Projects]]—_A concrete done state acts as a boundary and reduces stress; its worked example turns a vague aim into a two-page comparison document, the same move as "Sort out taxes" becoming a submitted HMRC confirmation._ [[Any Desired Outcome Requiring More Than One Step Is a Project and Must Be Tracked]]—_The rule behind "Name the Outcome": anything needing more than one step is a project and belongs in the system._ [[Habit 2 - Begin with the End in Mind]]—_The same principle at life scale: create the outcome mentally before creating it physically._
- Phase 2, the timed dump. The timer makes planning feel finite and stops it becoming a project of its own. [[The 5-Minute Action Overcomes Initiation Barriers]]—_A short, physically timed commitment with explicit permission to stop, the same device applied to the planning step._ [[Distraction Management in Timeboxing (Catch-All List)]]—_A place to jot intrusive thoughts and return to the task, which is what the unfiltered dump gives you._
- Phase 3, the MVA. The step has to be so small that starting needs no decision or motivation. [[Minimum Viable Experiment (MVE)]]—_The same under-two-minutes design: an action small enough to bypass the mind's resistance to effort._ [[Next Action is the Immediate Physical Step Forward]]—_The GTD next action this protocol tightens with a 120-second unit test._ [extends:: [[Next Action is the Immediate Physical Step Forward]], confidence=medium] [[The Neurological Divide Between Procrastination and Task Initiation]]—_Initiation failure is a mechanical difficulty switching focus to the task, which is why a mechanical first step works where motivation does not._

## When It Fails or Is the Wrong Tool

- The decomposition becomes the avoidance. Phase 2 is preparation, and preparation is a classic way to dodge the real work. [[The Core Problem Confusing Preparation with Action]]—_Deciding and planning feel like progress but change nothing in the world; the "painting the bullock cart wheels" story._ [[Tool tinkering is a form of productive procrastination]]—_Meta-work that feels productive but is not the task._ The 5-minute timer and the "without filtering" instruction are the guard; stop at Phase 3 even if the plan feels incomplete.
- The preparation is research, not planning. Before Phase 1 a vague task can turn into open-ended reading. [[Time-Boxing Research Prevents Productive Procrastination]]—_One specific question, a fixed timer, then act on what you found._
- The block is emotional, not a missing step. [[SoT - The Emotional Bottleneck Hypothesis]]—_Argues that "What am I afraid of?" is often the better question than "What is the next MVA?", so decomposing a task that is blocked by fear will stall._ In that case run [[SoT - The 3-Switch Protocol (Emotional Reset)]] first, then return here. [[Rejection Sensitive Dysphoria (RSD)]]—_One specific way starting can feel dangerous._
- It is run at the point of performance. [[Claim - Stripping Away Systems Under-Weights the Need for Pre-Committed External Prosthetics]]—_Asking yourself for the smallest next action at the moment of need relies on exactly the executive resource that is depleted; move the decomposition earlier, when you have capacity, and let the list carry the MVA._ The weekly review is the natural time (see below).
- The MVA is still too big. Shrink it again: [[Micro-Stepping Reduces Cognitive Load for Task Initiation]]—_Break a task into the smallest possible act._ [[The Three Rules of Starter Tasks]]—_A starter task exists only to build momentum and has a maximum duration._

## Where It Runs

- [[Protocol - Weekly Command Centre]]—_Move 3 writes one physical-verb starter per active ticket that has no line on the runway, which is Phase 3 applied to live commitments; it is capped at three._
- [[Weekly Review Verifies Project Actionability and Context]]—_Its second check, at least one identified next action per project, is the check this protocol satisfies._
- [[If a Next Action Takes Less Than Two Minutes Do It Immediately Rather Than Track It]]—_Overlaps the 120-second unit test: GTD says an action under two minutes should be done at once rather than tracked._

---

## Related

- [[Micro-Stepping Reduces Cognitive Load for Task Initiation|Breaking Projects Into Micro-Tasks Reduces ADHD Overwhelm]]—_The claim behind the decomposition: small specific steps with milestones make a large project startable and give re-entry points._
- [[SoT - Execution Protocol (GTD & PARA)]]—_Supplies the outcome-naming rule and the Project and Task Definition of Done that Phase 1 (Define the Endpoint) applies to a vague item._
- [[SoT - PRODOS Core Specification]]—_The kernel specification that defines the "Logic-Dopamine Mismatch" and provides the theoretical basis for the 120-second MVA loop; its §3.4 Decomposition Protocol points to this note._ [implements:: [[SoT - PRODOS Core Specification]]]
- [[Engineering Action and Bypassing Resistance]]—_The wider claim that action can be engineered around resistance, with the Minimum Viable Action as one of its levers._
- [[MOC - Action Management]]—_The central hub for ProdOS execution strategies, mapping this protocol to the broader goal of transforming intent into reality._
- [[SoT - The Cognitive Physiology of Task Execution]]—_Deconstructs why "heavy" tasks trigger avoidance and how mechanical execution of an MVA generates the necessary dopamine for momentum._
- [[Chaining Starter Tasks Creates a Momentum Ramp]]—_A complementary technique for building behavioral momentum using a sequence of low-cost wins._
- [[The Framework Solves Task Initiation Difficulties]]—_Explains how atomic decomposition removing ambiguity lowers the activation energy required to begin._
- [[An Action Can Be Formally Modeled as a State Transformation Function]]—_The formal mathematical model underpinning the transition from vague states to physical actions._

### Further Reading (Personal Library)

Semantic-similarity matches; each passage was read in full, but they are corroboration, not confirmed on-topic study.

- [Getting Things Done — David Allen, "How Much Planning Do You Really Need to Do?", pp. 117-118](calibre://view-book/GCcalibreBooks/1608/EPUB)—_Plan only as much as needed to get the project off your mind; most projects need just an outcome and a next action, and when things are stuck you move down from vision to brainstorming to organising to next action, the same order as the three phases here._
- [The Now Habit — Neil Fiore, Ch. 5 "Overcoming Blocks to Action", p. 120](calibre://view-book/GCcalibreBooks/693/PDF)—_Overwhelm grows when you insist on knowing the one right place to start; recognising that several starting points are adequate is what lets the MVA be any small first step._
- [The Art of Taking Action — Gregg Krech, "Procrastination Disguised as Busyness", p. 60](calibre://view-book/GCcalibreBooks/685/EPUB)—_Avoided tasks get replaced by busywork, which is the failure the Phase 2 timer guards against._
