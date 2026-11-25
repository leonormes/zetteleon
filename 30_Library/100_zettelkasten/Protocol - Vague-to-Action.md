---
aliases:
  - Task Decomposition Protocol
  - Vague-to-Action
conformant: true
contrasts_with:
  - "[[SoT - Perfectionism and Analysis Paralysis]]"
created: 2026-04-04T12:00:00+00:00
modified: 2026-11-15T10:30:00+00:00
permalink: llmeon/30-library/so-t/protocol-vague-to-action
project_category: prodos
see_also:
  - "[[Protocol - Action-First GTD (LLM Chief of Staff)]]"
status: draft
tags:
  - execution
  - prodos
  - protocol
  - task-decomposition
  - task-initiation
  - TheHuman/Health/ADHD
title: Protocol - Vague-to-Action
trigger: A captured task feels heavy or vague, or you notice you are avoiding it
type: protocol
upstream:
  - "[[SoT - PRODOS Core Specification]]"
  - "[[SoT - Execution Protocol (GTD & PARA)]]"
prodos:
  kind: protocol
  protocol:
    applies_to:
      - task-clarification
      - adhd
---

> Trigger: a task feels too heavy or undefined to start, or you notice you are avoiding it.

## Objective

To convert "heavy" or undefined tasks that trigger avoidance into physical, binary actions (`< 120 seconds`) that can be executed immediately.

---

## The Algorithm

### Phase 1: Define the Endpoint

1. **Identify the Problem Statement:** Write down the vague task exactly as captured (e.g., "Sort out taxes").
2. **Define "Done":** Describe a tangible, physical outcome that proves the task is finished (e.g., "A submitted PDF confirmation on the HMRC portal").
3. **Name the Outcome:** Give this outcome a past-tense GTD Project name in your system (`[[SoT - Execution Protocol (GTD & PARA)]]`).

### Phase 2: Capture the Steps

1. **Set a 5-Minute Timer:** Bounds the planning step so decomposition does not become avoidance.
2. **Brain Dump:** Write every question, idea, and micro-step without filtering (acting as a distraction catch-all pad).
3. **Organise into Phases:** Group the dump into 3–5 logical stages (e.g., Gather Docs, Data Entry, Review, Submit).

### Phase 3: Activate the MVA

1. **Identify Phase 1:** Look at the first group of steps.
2. **Identify the MVA (Minimum Viable Action):** What is the _very next physical action_?
   - It must be small, visible, and doable now (e.g., "Open 1Password and copy the HMRC login," "Create a folder named `Taxes`").
3. **Commit to the Runway:** Write this single physical-verb MVA on your Todoist runway (`#Work` or `#Personal`). The entire project is now represented by this one starter task.

---

## Unit Test

- **Binary Outcome:** Can you answer "Yes/No" to whether the step is finished in `< 120 seconds`?
- **No Planning:** Does the step require further thinking or deciding? If yes, it is not an MVA—shrink it again.

---

## Why It Works

Each phase counters a specific mechanism of ADHD task avoidance:

- **Phase 1 — The Endpoint:** A task with no visible finish line has no boundary, so it feels endless.
  - [[The Done State as a Boundary for ADHD Projects]]—_A concrete done state acts as a boundary and reduces stress (e.g., turning "sort out taxes" into a submitted HMRC PDF confirmation)._ [synthesizes:: [[The Done State as a Boundary for ADHD Projects]], confidence=high]
  - [[Any Desired Outcome Requiring More Than One Step Is a Project and Must Be Tracked]]—_The rule behind "Name the Outcome": anything needing more than one step is a project and belongs in the system._ [synthesizes:: [[Any Desired Outcome Requiring More Than One Step Is a Project and Must Be Tracked]], confidence=high]
  - [[Habit 2 - Begin with the End in Mind]]—_The same principle at life scale: define the outcome mentally before executing it physically._ [synthesizes:: [[Habit 2 - Begin with the End in Mind]], confidence=medium]
- **Phase 2 — The Timed Dump:** The timer makes planning finite and prevents preparation from replacing action.
  - Five-minute timed commitment—_A short, physically timed commitment with explicit permission to stop, applied here to the decomposition step itself._
  - [[SoT - Indistractable Model (Focus Management)]]—_The unfiltered 5-minute dump acts as a timebox catch-all pad: jotting down intrusive steps offloads working memory so you stay on traction._ [implements:: [[SoT - Indistractable Model (Focus Management)]], confidence=high]
- **Phase 3 — The MVA:** The step must be small enough that starting requires neither decision nor motivation.
  - [[Next Action is the Immediate Physical Step Forward]]—_The core GTD next action, tightened here by a `< 120-second` binary unit test._ [extends:: [[Next Action is the Immediate Physical Step Forward]], confidence=high]
  - [[Minimum Viable Experiment (MVE)]]—_The same under-two-minutes design: an action small enough to bypass limbic resistance to effort._ [synthesizes:: [[Minimum Viable Experiment (MVE)]], confidence=high]
  - [[The Neurological Divide Between Procrastination and Task Initiation]]—_Initiation failure is a mechanical difficulty switching from DMN to TPN, which is why a mechanical first step works where willpower does not._ [synthesizes:: [[The Neurological Divide Between Procrastination and Task Initiation]], confidence=high]

---

## When It Fails or Is the Wrong Tool

- **Decomposition becomes avoidance:** Phase 2 is preparation, which easily displaces real execution. The 5-minute timer and unfiltered dump are the guard; stop at Phase 3 even if the plan feels incomplete.
  - [[The Core Problem Confusing Preparation with Action]]—_Deciding and planning feel like progress but change nothing in the world ("painting the bullock cart wheels")._
  - [[Tool tinkering is a form of productive procrastination]]—_Meta-work that feels productive while avoiding the real commitment._
- **Preparation turns into open-ended research:** Before Phase 1, a vague task can trigger rabbit-hole reading.
  - [[Time-Boxing Research Prevents Productive Procrastination]]—_Bound research to one specific question and a fixed timer, then act on what you found._
- **The block is emotional, not structural:** Decomposing a task blocked by fear or shame will stall. Run [[SoT - The 3-Switch Protocol (Emotional Reset)]] first, then return here.
  - [[SoT - The Emotional Bottleneck Hypothesis]]—_Argues that "What am I afraid of?" must be answered before "What is the next MVA?" when avoidance is driven by threat._
  - [[Rejection Sensitive Dysphoria (RSD)]]—_Explains why imperfect initiation can feel existentially dangerous._
- **Run at the point of performance:** Asking yourself to decompose a task when executive function is already depleted fails; run decomposition earlier (during [[Protocol - Weekly Command Centre]] or via [[Protocol - Action-First GTD (LLM Chief of Staff)]]) so the runway already holds the MVA.
  - [[ADHD Executive Dysfunction Needs Triggers Decided in Advance, Not Willpower in the Moment]]—_Move the decision to when you have capacity and let the external list carry the cue._
- **The MVA is still too big:** Shrink it again until it takes under 120 seconds.
  - [[Micro-Stepping Reduces Cognitive Load for Task Initiation]]—_Breaks a project into micro-tasks with low activation energy and clear re-entry points._ [synthesizes:: [[Micro-Stepping Reduces Cognitive Load for Task Initiation]], confidence=high]
  - [[The Three Rules of Starter Tasks]]—_A starter task exists solely to build momentum and carries a strict maximum duration._ [synthesizes:: [[The Three Rules of Starter Tasks]], confidence=high]

---

## Where It Runs

- [[Protocol - Weekly Command Centre]]—_Move 3 writes one physical-verb starter per active Jira commitment that has no line on the Todoist runway (capped at three)._
- [[Weekly Review Verifies Project Actionability and Context]]—_Satisfies the weekly check that every active project has at least one identified next action._
- [[If a Next Action Takes Less Than Two Minutes Do It Immediately Rather Than Track It]]—_Intersects the 120-second unit test: if the resulting MVA can be finished right now in under two minutes, do it immediately._
- [[SoT - Protocol - The Launch Sequence]]—_Downstream physical/kinetic initiation protocol when the `< 120s` MVA is already defined on the runway but motor/arousal resistance remains high (emits `depends_on` → this protocol)._

---

## Related

- [[SoT - PRODOS Core Specification]]—_Defines the Logic-Dopamine Mismatch and the §3.4 Decomposition Protocol that this note operationalises._ [implements:: [[SoT - PRODOS Core Specification]], confidence=high]
- [[SoT - Execution Protocol (GTD & PARA)]]—_Supplies the past-tense Project outcome rule and Task Definition of Done applied in Phase 1 and Phase 3._ [implements:: [[SoT - Execution Protocol (GTD & PARA)]], confidence=high]
- [[SoT - The Cognitive Physiology of Task Execution]]—_Deconstructs why heavy tasks trigger avoidance and how mechanical MVA execution generates dopamine for momentum._ [extends:: [[SoT - The Cognitive Physiology of Task Execution]], confidence=high]
- [[Chaining Starter Tasks Creates a Momentum Ramp]]—_Complements Phase 3 by chaining low-cost starter tasks into behavioural momentum._ [synthesizes:: [[Chaining Starter Tasks Creates a Momentum Ramp]], confidence=high]
- [[The Framework Solves Task Initiation Difficulties]]—_Explains how atomic decomposition removes ambiguity and lowers activation energy._ [synthesizes:: [[The Framework Solves Task Initiation Difficulties]], confidence=high]
- [[An Action Can Be Formally Modeled as a State Transformation Function]]—_Formal state-transition model underpinning the conversion from vague states to binary physical actions._ [synthesizes:: [[An Action Can Be Formally Modeled as a State Transformation Function]], confidence=medium]
- [[MOC - Action Management]]—_Hub note mapping ProdOS execution protocols and starter-task strategies._

### Further Reading (Personal Library)

Semantic-similarity matches; each passage was read in full, but they are corroboration, not confirmed on-topic study.

- [Getting Things Done — David Allen, "How Much Planning Do You Really Need to Do?", pp. 117-118](calibre://view-book/GCcalibreBooks/1608/EPUB)—_Plan only as much as needed to get the project off your mind; most projects need just an outcome and a next action, and when things are stuck you move down from vision to brainstorming to organising to next action, the same order as the three phases here._
- [The Now Habit — Neil Fiore, Ch. 5 "Overcoming Blocks to Action", p. 120](calibre://view-book/GCcalibreBooks/693/PDF)—_Overwhelm grows when you insist on knowing the one right place to start; recognising that several starting points are adequate is what lets the MVA be any small first step._
- [The Art of Taking Action — Gregg Krech, "Procrastination Disguised as Busyness", p. 60](calibre://view-book/GCcalibreBooks/685/EPUB)—_Avoided tasks get replaced by busywork, which is the failure the Phase 2 timer guards against._
