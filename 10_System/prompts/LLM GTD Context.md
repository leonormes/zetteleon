---
aliases: []
conformant: true
created: 2025-10-16T08:19:54+00:00
description: Background context on the Getting Things Done (GTD) methodology — projects vs. next actions, the five phases of workflow control, and the six horizons of focus. Inject alongside planning, review, or task-triage prompts that assume GTD vocabulary.
modified: 2026-11-08T11:20:00+00:00
permalink: llmeon/10-system/prompts/llm-gtd-context
tags:
- domain/productivity
- type/context
title: LLM GTD Context
type: prompt
---

## LLM Planning Context Prompt: Getting Things Done (GTD) and Making It All Work

### 1. Foundational Philosophy and Goal

The core objective of this methodology is to achieve a state of relaxed and controlled engagement or "mind like water". This state is necessary because the mind is excellent for having ideas, but terrible for holding them. Any commitment, big or small, that remains in the psyche without clarification creates irrational and unresolvable pressure.

A core premise is: You have to think about your stuff more than you realize, but not as much as you're afraid you might. Anxiety is caused by a lack of control, organization, preparation, and action.

### 2. The Critical Distinction: Projects vs. Actions

The primary tool for transforming amorphous commitments ("stuff") into manageable work is rigorous definition using two key clarifying questions: "What is the desired outcome?" and "What is the next action?".

| Commitment Type         | Definition and Scope                                                                                                                                                                                                                            | Purpose                                                                                                                                                                                                                                       |
|:---------------------- |:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Project (Outcome)   | Any desired result that requires more than one action step to complete, usually within a year. This includes small things like "Install new set of tires" or ambiguous issues like "Resolve situation with employees A and B".            | The Projects list is a comprehensive index of open loops. You do not actually do a project; you only do action steps related to it. The list is maintained to ensure every commitment has a corresponding next action defined.     |
| Next Action (Doing) | The next physical, visible activity that progresses something toward completion. It must be specific enough to know where it happens and with what tools (e.g., "Draft email to Bob requesting meeting," not "Set meeting with Bob"). | Next Actions translate abstract goals into doable tasks. They relieve psychological pressure by finishing the thinking about what comes next. Next Actions are organized primarily by context (e.g., @Computer, @Calls, @Errands). |

### 3. Mastering Workflow: The Five Phases of Control

Gaining control of commitments requires applying a five-step process to all incoming "stuff":

1. Capture (Collect): Gather literally everything that has your attention into trusted collection tools outside your head (physical in-trays, notebooks, digital lists, etc.).
2. Clarify (Process): Decide what each captured item means. If it's actionable, determine the desired outcome (Project) and the single next physical step (Next Action).
3. Organize: Sort the results into appropriate "buckets" based on their meaning and how they need to be reviewed:
   - Calendar: Actions or information tied to a specific day or time.
   - Next Actions Lists: Actions that can be done as soon as possible, sorted by Context.
   - Projects List: Index of all multi-step outcomes.
   - Waiting For List: Items delegated or ordered from others.
   - Reference/Support: Non-actionable information.
   - Incubation (Someday/Maybe): Items tabled for later reassessment.
4. Reflect (Review): Review the system regularly to ensure it is current and functional. The Weekly Review is critical for checking the status of all projects and ensuring every open commitment has a defined next action.
5. Engage (Do): Take action by making moment-to-moment choices.

### 4. Gaining Perspective: The Six Horizons of Focus

Priorities cascade downward through six distinct "Horizons of Focus," providing vertical alignment for all commitments. Reviewing these levels provides crucial perspective:

| Horizon Level (Altitude)  | Scope and Question                                                                                                                                                  | Function                                                                   |
|:------------------------ |:------------------------------------------------------------------------------------------------------------------------------------------------------------------ |:------------------------------------------------------------------------- |
| Horizon 5 (50,000 ft) | Purpose and Principles: Ultimate intention and core values ("Why are we doing this?").                                                                         | Defines the ultimate criteria for decisions and success.                  |
| Horizon 4 (40,000 ft) | Vision: Long-term success scenarios (3–5 years) ("What would long-term success look, sound, and feel like?").                                                  | Provides the blueprint for the final result, guiding subsequent planning. |
| Horizon 3 (30,000 ft) | Goals and Objectives: Outcomes to achieve (1–2 years).                                                                                                         | Aligns shorter-term actions toward the long-term vision.                  |
| Horizon 2 (20,000 ft) | Areas of Focus and Accountability: Roles, responsibilities, and areas to maintain (e.g., Staff Development, Health, Finances) ("What do I need to maintain?"). | Serves as a checklist to ensure balance and prevent neglect.              |
| Horizon 1 (10,000 ft) | Current Projects: All multi-step outcomes.                                                                                                                     | Index of open loops that require weekly attention to drive Next Actions.  |
| Ground (Runway)       | Current Actions: The physical tasks you can do right now.                                                                                                      | The final expression of all higher-level commitments.                     |

### 5. Making Action Choices

Assuming all commitments are captured, clarified, and organized, daily choices about what to do in the moment are determined by four practical criteria:

1. Context: What tools or location are available (e.g., at the phone, at the office).
2. Time Available: How much time is free before the next scheduled commitment.
3. Energy Available: Mental, emotional, or physical capacity (e.g., tackling simple tasks when energy is low, complex tasks when energy is high).
4. Priority: Based on the context and energy, choose the action that best aligns with the higher Horizons of Focus.

### 6. Work Visibility and Flow Management

The principle of making work visible optimizes flow and prevents capacity overload, integrating well with GTD:

- Make Work Visible: When work is invisible, capacity is obscured, leading to mental overload and stress.
- WIP (Work-in-Progress): Too much WIP occurs when demand exceeds capacity, resulting in clashing priorities, increased dependencies, and interruptions.
- Limit WIP: Limiting WIP creates the necessary tension to complete work, rather than starting new items, which shortens cycle time.
- Conflicting/Unplanned Work: Unplanned work (interruptions, fires) must be made visible and planned for by reserving capacity.
- Context Switching: Interruptions force context switches, which can take up to twenty minutes to recover from, draining energy and reducing flow.

### Summary of Best Practices for Planning

- Finish Your Thinking: For every item, immediately define the concrete next action to move it forward.
- Do It, Delegate It, or Defer It (The 3 Ds): If an action takes less than two minutes, do it immediately. If it takes longer, delegate it or defer it into your trusted system.
- Weekly Review is Non-Negotiable: Dedicate time (ideally weekly) to review projects, clean up inputs, and ensure systems are current; this is the key to sustainability.
- Bottom-Up Focus: In times of high confusion or stress, focus on fixing Ground-level issues (e.g., clearing the in-tray) before tackling high-level strategic planning, as control facilitates perspective.

---

## Vault Notes (Not part of the Injected Context)
> Stop injecting at the rule above. Everything below is vault navigation and ProdOS protocol comparison for humans and agents working in the vault, not GTD context for the LLM.

### How the Vault Uses This Note (Incoming Edges)

- [[Habit 2 - Begin with the End in Mind]], [[Habit 4 - Think Win-Win]], and [[Effective Productivity Comes From the Bottom Up]] each carry an incoming `depends_on` edge to this note for the Six Horizons of Focus model (Horizons 5–4, Horizon 2, and the Ground-level Bottom-Up Focus practice, respectively), because no dedicated `30_Library/` note carries that hierarchy. Do not add reverse justification edges from here back to them (doing so creates a justification cycle in `edge_lint.py`).
- [[00 - Prompt Library Router]] routes to this note as the GTD methodology background (`10_System/prompts/`—outside `30_Library/`). Pair it with [[leon-context-core-profile]] and [[Optimised GTD Context Auditor for Pieces LTM]] when triaging open loops.

### Related: Vault GTD & ProdOS Notes (Outgoing Typed Edges)

#### Core GTD & Flow Atoms Synthesised Here

- [synthesizes:: [[GTD and the Cognitive Load of Execution]], confidence=high]—_Section 1 & 2: separating planning decisions from physical execution avoids simultaneous DMN/TPN conflict._
- [synthesizes:: [[Cognitive Offloading Frees Mental Resources for Decision-Making and Problem-Solving]], confidence=high]—_Section 1 & 3: externalising commitments frees bounded working memory ("the mind is for having ideas, not holding them")._
- [synthesizes:: [[Any Desired Outcome Requiring More Than One Step Is a Project and Must Be Tracked]], confidence=high]—_Section 2: the >1-step Project rule and master Projects index._
- [synthesizes:: [[A Next Action Must Be the Absolute Next Physical Visible Activity Required to Move a Situation Forward]], confidence=high]—_Section 2: concrete physical-activity test ("Draft email to Bob…")._
- [synthesizes:: [[Next Action is the Immediate Physical Step Forward]], confidence=high]—_Section 2: overlapping Next Action claim closing the psychological initiation gap._
- [synthesizes:: [[The Clarify Stage Is the Executive Decision-Making Bridge Between Stuff and Action]], confidence=high]—_Section 3 (Phase 2): discrete decision bridge between raw stuff and organised buckets._
- [synthesizes:: [[Every Clarified Item Must Pass a Binary Actionability Test to Determine Its Categorical Flow]], confidence=high]—_Section 3 (Phase 2): mandatory binary actionability gate routing non-actionable items to Trash, Reference, or Someday/Maybe._
- [synthesizes:: [[Never Return an Item to the In-Tray Once Picked Up for Clarification]], confidence=high]—_Section 3 (Phase 2): one-pass inbox rule preventing repeated non-decision._
- [synthesizes:: [[The Purpose of a Weekly Review is to Restore Trust in Your System]], confidence=high]—_Section 3 (Phase 4) & Summary: keeping lists current so the mind can let go._
- [synthesizes:: [[Core Actions of a GTD Weekly Review]], confidence=high]—_Section 3 (Phase 4): Allen's full Get Clear, Get Current, Get Creative weekly drill._
- [synthesizes:: [[Weekly Review Verifies Project Actionability and Context]], confidence=high]—_Section 3 (Phase 4): per-project check for done state, next action, context, and starter task._
- [synthesizes:: [[Context Tags Enable Efficient Batching and Reduce Context Switching]], confidence=high]—_Section 2, 3 & 5: `@Context` sorting to batch similar work and cut switching costs._
- [synthesizes:: [[Concurrent Task Overload Creates Non-Linear Administrative Overhead That Destroys Focus]], confidence=high]—_Section 6: limiting WIP because concurrent open loops generate compounding overhead._
- [synthesizes:: [[If a Next Action Takes Less Than Two Minutes Do It Immediately Rather Than Track It]], confidence=high]—_Summary: the `<2 minute` efficiency threshold during Clarification._

#### ProdOS Protocols & ADHD Adaptations Grounded by This Baseline

- [supports:: [[ProdOS System Overview and Development Progress]], confidence=medium]—_integrates GTD's "Mind Like Water", Horizontal Control vs Vertical Perspective, and Capture-Now/Clarify-Later model into the ProdOS Triad (Todoist + Obsidian + AI Chief of Staff)._
- [supports:: [[SoT - Execution Protocol (GTD & PARA)]], confidence=high]—_the vault's canonical GTD+PARA hybrid: adds PARA Containers above GTD Projects, enforces past-tense outcome naming, and formalises Project/Task Definition of Done._
- [supports:: [[gtd-action-system]], confidence=high]—_the live four-tier GTD implementation across Obsidian (knowledge/personal outcomes), Jira (work outcomes), Todoist (flat next-action runway), and Calendar (hard landscape)._
- [supports:: [[Protocol - Action-First GTD (LLM Chief of Staff)]], confidence=medium]—_outsources GTD's Clarify and Organise stages ("Dump, Don't Organize") to the LLM Chief of Staff._
- [supports:: [[Protocol - Autonomous Action System]], confidence=medium]—_agentic GTD loop via Obsidian and Todoist MCP (`00_Inbox/dump.md` → Refine → Context Restoration → Weekly Health Check)._
- [supports:: [[Protocol - Vague-to-Action]], confidence=medium]—_applies GTD outcome-plus-next-action decomposition (Define Done → 5-minute dump → `<120s` MVA) to heavy, avoided tasks._
- [supports:: [[Protocol - Weekly Command Centre]], confidence=medium]—_executes GTD's Reflect stage as a fixed Friday 16:30, 10-minute, four-move Tier 0 floor._
- [supports:: [[SoT - ProdOS Thinking Stream]], confidence=low]—_adapts GTD Capture → Clarify → Organise into the 120-second CRPE loop under the Rule of Zero Toil._
- [supports:: [[SoT - PRODOS Core Specification]], confidence=low]—_retains GTD externalised capture and physical starter actions in §3 while re-architecting execution around the Logic–Dopamine Mismatch._
- [supports:: [[SoT - Temporal Management (Blocking and Boxing)]], confidence=medium]—_operationalises GTD's hard-landscape Master Calendar, 100% capture pipeline, and nested temporal horizons._
- [supports:: [[For ADHD The Clarification Process Externalizes Decision-Making and Builds System Trust]], confidence=medium]—_GTD's discrete Clarify stage supplies the pre-decided actionability that spares ADHD executive function at execution._
- [supports:: [[Contexts Reduce Overwhelm and Support Working Memory for ADHD]], confidence=medium]—_GTD's `@Context` filtering narrows visible tasks to what matches current tools and energy._

### Deep Comparison: Canonical GTD Prompt vs ProdOS Protocol (`30_Library/`)

| GTD Prompt Section | Canonical GTD Baseline (This Prompt) | ProdOS Protocol Adaptation & Divergence (`30_Library/`) |
|:---|:---|:---|
| **1. Philosophy & Roles** | Assumes one human operator achieves "Mind Like Water" once open loops are externalised, clarified, and organised. | Diagnoses the **Logic–Dopamine Mismatch** (logic steers, dopamine fuels; motivation follows action) in [[SoT - PRODOS Core Specification]] and splits roles across **The Triad** in [[ProdOS System Overview and Development Progress]]: Human Problem Definer, Obsidian Zettelkasten ("Computed Truth"), Todoist Action Engine, and AI Chief of Staff. Enforces a hard **Learning vs Execution** boundary in [[SoT - Processing IS the Work]] §6: PKM friction must stay human, whereas GTD organising toil is offloaded to the LLM ("Rule of Zero Toil", [[SoT - ProdOS Thinking Stream]]). |
| **2. Projects vs Next Actions** | Two-tier model: Project (`>1` step, e.g. imperative `"Install new set of tires"`) and physical/visible Next Action (`"Draft email to Bob…"`). | **Three-tier hierarchy & naming:** [[SoT - Execution Protocol (GTD & PARA)]] adds a PARA Container above GTD Projects, mandates **past-tense Completed Outcome titles** (`"Tax Return Submitted"`), and enforces binary Project/Task DoDs. **Tool split:** [[gtd-action-system]] separates outcomes (Jira for work, Obsidian for personal) from Todoist's flat action-only runway (max one Todoist starter per active Jira ticket; `@project` and `@next_action` tags were purged in favour of `!#Inbox & !#Someday & !#Waiting`, superseding the older `@next_action`/`@now` tag note in [[ProdOS System Overview and Development Progress]]). **Granularity:** ProdOS shrinks Next Actions into `<120s` binary **Minimal Viable Actions (MVAs)** / kindling sparks ([[SoT - PRODOS Core Specification]] §3.2, [[Protocol - Vague-to-Action]]). |
| **3. Five Workflow Phases** | Manual Capture → Clarify → Organise (6 buckets) → Full Weekly Review → Engage. | **Clarify modes:** Replaced by agentic handoff ([[Protocol - Action-First GTD (LLM Chief of Staff)]], [[Protocol - Autonomous Action System]]), the 120s CRPE stream with a 24h delete/archive rule ([[SoT - ProdOS Thinking Stream]]), or timed decomposition ([[Protocol - Vague-to-Action]]). **Calendar & Contexts:** [[gtd-action-system]] enforces strict Hard-Landscape dates (stripping overdue wish-list dates back to no-date) and compresses contexts to `@computer`/`@home`. **Reflect:** [[Protocol - Weekly Command Centre]] cuts Allen's ~2-hour [[Core Actions of a GTD Weekly Review]] down to a **10-minute Tier 0 floor** (60s read Completed wins for dopamine, 5m Todoist Inbox, 3m cap of 3 Jira starters, 60s environmental friction fix), deferring `@waiting`, calendar, and Someday reviews to earned Tier 1–2 escalations. |
| **4. Six Horizons of Focus** | Static six-altitude cascade from Runway up to 50,000 ft Purpose & Principles. | ProdOS replaces top-down altitude checklists with **problem-first lineage**: the **Clarity Framework** ([[ProdOS System Overview and Development Progress]]) and [[SoT - The Telos Method]]'s 7-layer DAG (_Problems → Mission → Narratives → Goals → Challenges → Strategies → Projects_), paired with [[SoT - Goal Architecture (Vision and Alignment)]]'s dissociated NLP Compass (set, ecology-check, then release from conscious rehearsal) and 10-week seasonal Quintiles in [[SoT - Temporal Management (Blocking and Boxing)]]. |
| **5. Action Choice Criteria** | Evaluate Context → Time → Energy → Priority in the moment of execution. | [[SoT - Prosthetic Executive Function]] rejects multi-criteria decisions at the Point of Performance under ADHD depletion. ProdOS adds **missing initiation fuel** via the **PINCH Dopamine Engine** and **Ignition Protocol** (Mystery, Urgency, Spite) in [[SoT - PRODOS Core Specification]] §2–3.3, routes workflow entry points directly by energy state, binds Priority to the Eisenhower Matrix in [[Protocol - Action-First GTD (LLM Chief of Staff)]], and caps daily focus via Top-One Priority and binary Energy Check in [[SoT - Principles for Peaceful Productivity]]. |
| **6. WIP, Flow & Heuristics** | Mixes DeGrandis (*Making Work Visible*: WIP limits, unplanned work, unsourced "20-minute" switch cost) with Allen's `<2m` rule and "3 Ds" (Do, Delegate, Defer). | **WIP & Switching:** Concurrency is bounded via One-Note-Containers in [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]], Cryosleep `#SAVESTATE` dumps in [[SoT - PRODOS Core Specification]] §4, and phase batching / Boring Breaks in [[SoT - The Cognitive Physiology of Task Execution]] (the 20-minute recovery figure has no vault source). **2-Minute Rule:** Kept in [[SoT - Execution Protocol (GTD & PARA)]] and [[gtd-action-system]], repurposed as the `<120s` MVA ceiling, and suspended in strict clarification experiments. **"3 Ds":** Absent across `30_Library/`; vault gates branch first on binary actionability (Trash / Reference / Incubate) before `<2m`, `#Waiting`, or Runway. |

### Tensions (Where ProdOS Diverges Under ADHD Assumptions)

- [[Claim - Capture is easy but processing is hard]]—_tension with Section 3: standard GTD treats Capture and Clarify as symmetric workflow habits, whereas in ADHD capture demands near-zero executive function while clarifying overloads working memory—justifying ProdOS's LLM Chief of Staff offload._
- [[The Clarification Ritual (Stuff to Action)]]—_tension with the 2-Minute Rule: prescribes a strict 15-minute daily "Do NOT do the work, just clarify" mode to prevent ADHD task-hijacking, deliberately suspending GTD's `<2m` immediate-execution exception._
- [[Deep Dive Sessions for ADHD (Adapted GTD Next Actions)]]—_tension with Section 2 & 3: an experiment hiding granular Next Action lists in favour of 75-minute single-project blocks to preserve ADHD flow._
- [[Horizontal vs Vertical Execution in the ADHD Mind]]—_tension with Section 2 & 5 (`axiom: true`): argues that horizontal `@Context` interleaving across disparate projects incurs context-reloading friction and starves ADHD dopamine compared to vertical single-project sessions._
- [[SoT - Prosthetic Executive Function]]—_tension with Section 5: argues that evaluating Context, Time, Energy, and Priority in the moment of doing relies on depleted prefrontal resources at the Point of Performance rather than pre-committed environmental cues._

### See Also (ProdOS Hubs & Orthogonal Frameworks)

- [[MOC - ProdOS]]—_master architectural map of the ProdOS kernel, cognitive pipeline, and operational protocols._
- [[MOC - Action Management]]—_navigation hub separating Obsidian thinking from Todoist execution._
- [[SoT - The Telos Method]]—_7-layer Problem-to-Project Chain of Explainability replacing GTD Horizons 3–5._
- [[SoT - Goal Architecture (Vision and Alignment)]]—_NLP Compass protocol for encoding and releasing Horizon 4–5 vision without outcome obsession._
- [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]]—_convergent Action–Container–Thought loop preventing collector's fallacy and scope creep._
- [[SoT - Processing IS the Work]]—_defines why PKM synthesis requires human cognitive friction while GTD execution forbids it._
- [[SoT - Principles for Peaceful Productivity]]—_ten daily behavioural rules (including Top-One Priority and Energy Check) sitting beneath ProdOS protocols._
- [[SoT - The Cognitive Physiology of Task Execution]]—_five neurological phases of execution (Initiation, Encoding, Execution, Monitoring, Completion) behind ProdOS's tool boundaries._

### Further Reading (Personal Library)

- [Getting Things Done — David Allen, Ch. 1 "A New Practice for a New Reality"](calibre://view-book/GCcalibreBooks/1608/EPUB)—_uses the phrase "mind like water" (compared with martial arts and the athlete's "zone"), the state Section 1 names as the goal._
- [Getting Things Done — David Allen, Ch. 3 "Getting Projects Creatively Under Way"](calibre://view-book/GCcalibreBooks/1608/EPUB)—_describes the next-action decision as asking what, specifically, you would physically do about something if you had nothing else to do, which is the test behind Section 2._
- [Getting Things Done — David Allen, Ch. 9 "Engaging: Making the Best Action Choices", p. 279](calibre://view-book/GCcalibreBooks/1608/EPUB)—_semantic-similarity match (0.318): connects area-of-focus shifts to defining new projects and choosing actions in Section 4 & 5._
- [Making It All Work — David Allen, Ch. 6 "Getting Control: Clarifying"](calibre://view-book/GCcalibreBooks/226/PDF)—_notes that active projects all have specific next actions determined, while the someday category has none attached._
- [Making It All Work — David Allen, Ch. 14 "Getting Perspective at Twenty Thousand Feet: Areas of Focus and Responsibility", p. 14](calibre://view-book/GCcalibreBooks/226/PDF)—_semantic-similarity match (0.327): elaborates Horizon 2 role/accountability maintenance in Section 4._
- [Making Work Visible — Dominica DeGrandis, Section 2.4 "Committing the Perfect Crime: Unplanned Work"](calibre://view-book/GCcalibreBooks/225/EPUB)—_the source family for Section 6: unplanned work that is not made visible leaves no evidence of what is displacing planned work._