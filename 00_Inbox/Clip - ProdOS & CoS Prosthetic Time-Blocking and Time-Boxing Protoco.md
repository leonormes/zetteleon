---
captured: 2026-11-17T09:34:36+00:00 2026-11-17T09:34:36+00:00
conformant: false
created: 2026-11-17T09:34:51+00:00
modified: 2026-11-17T10:10:43+00:00
non_conformance_reason: raw web capture awaiting triage
permalink: llmeon/00-inbox/clip-prod-os-co-s-prosthetic-time-blocking-and-time-boxing-protoco
source: https://gemini.google.com/app/21fa50a38bb82ef2
status: seed
tags: [source/web-clip]
title: New chat
type: concept
---

## New Chat

You

based on the notebooklms draw up a protocol for the prodOS and CoS systems to optimise time blocking/boxing for my ADHD executive function protheses. Output full context llm prompt so my local llm can update the vault files and instructions

---

Gemini

### Part 1: ProdOS & CoS Prosthetic Time-Blocking and Time-Boxing Protocol

In a neuro-variable profile, executive dysfunction stems from a structural bottleneck between the Default Mode Network (DMN, internal noise) and the Task Positive Network (TPN, focused execution). Open-ended tickets cause both networks to fire simultaneously, inducing initiation paralysis, while completed or stalled work creates "attention residue" and switching inertia.

To act as an external executive function prosthesis, ProdOS and the Chief of Staff (CoS) enforce a strict operational distinction between Time Blocking and Time Boxing:

- Time Blocking (Macro-Container / "When"): Reserves calendar capacity in advance to protect Quadrant II work from shallow encroachment. Governed by `/daily-plan` via Sunsama and native calendars.
	Time Blocking vs Timeboxing: What's the Difference? - Planzer.io+ 1
- Time Boxing (Micro-Constraint / "How Long + Done Means"): Allocates a fixed, unyielding duration (15, 30, or 60 minutes) paired with a binary, visualisable output ("acceptable rather than perfect") and a mandatory hard stop when the timer rings. Governed by `/engage-action` and the CoS Constraint Guardian.
	Time Blocking vs Timeboxing: What's the Difference? - Planzer.io+ 2

#### Phase 1: Macro-Allocation (Time Blocking via /daily-plan)

1. Control Plane Separation: Obsidian and Todoist remain the canonical Source of Truth (`!#Inbox & !#Someday & !#Waiting`); Sunsama is strictly a transient daily execution surface. Never create standalone tasks in Sunsama via MCP (`create_task` and `create_calendar_event` are forbidden).
2. Morning Hard-Landscape Reset (Step 0): Before building today's schedule, run the reset logic (`(overdue | today) & no deadline`). Strip arbitrary `Today` dates back to the unscheduled runway and return uncompleted soft timeboxes to the backlog via `move_task_to_backlog` so `Today` never accumulates zombie tasks.
3. Protection Priority & Big Rock Alignment: Schedule blocks in strict hierarchy: `Renewal > Big Rocks > Other Actions > Buffer`. Big Rocks are weekly Quadrant II outcomes stored in `sunsama://objectives` (capped at 3 per week, or 1–2 if existing calendar commitments leave <20 hours of open work blocks), never Todoist `p1` urgent firefighting.
	ProdOS System Overview and Development Progress.md
4. Capacity Math & Parallelism: Leave a mandatory 25% unscheduled buffer across the workday. When orchestrating concurrent CLI agents (`Zellij` + `agy` / `Claude Code`), group background agent runs into a single calendar block using Sunsama's `set_task_parallel` so capacity math stays accurate.
	ProdOS System Overview and Development Progress.md+ 1
5. Batched Shallows (Drain the Shallows): Contain reactive communication (NHS trust threads, Teams, email) inside two fixed 20-minute timeboxes (e.g., 10:30 and 15:30). Apply the 2-minute rule immediately; turn >2-minute actionable items into undated runway tasks and blocked threads into `#Waiting` items.
	Time Blocking vs Timeboxing: What's the Difference? - Planzer.io+ 1

#### Phase 2: Pre-Flight Negotiation (Entering the Timebox via /engage-action)

You never arrive at a timebox cold or with an amorphous goal. Before the timer starts, the CoS enforces the Task-Authoring Gate:

1. The Constraint Prompt (`Done means`): The CoS asks: _"You have [15 | 30 | 60] minutes in this box. What is the exact, visualisable artifact or state you will ship to an acceptable—not perfect—standard when the timer rings?"_ If the answer is vague, the CoS rejects it and slices the scope smaller.
	Timeboxing_ The Power of Doing One Thing a - Marc Zao-Sanders.pdf
2. Two-Tier Ignition (`Steps`):
	- The MVA (<120 Seconds): A zero-decision, bodily physical spark that crosses static friction (e.g., _"Open terminal in Zellij and run `kubectl get pods` "_), verified by a binary Yes/No unit test.
		- The Starter Task (1–15 Minutes): The initial momentum ramp launched immediately by the MVA.
3. PINCH Catalyst & Pacts (`If stuck`): If the task lacks natural dopamine pull, inject a PINCH catalyst (_Play, Interest, Novelty, Competition, Hurry_—such as a Roosevelt Dash countdown challenge) and activate an Effort Pact (notifications off, comms closed, click through the `sunsama://action/details/<id>` deep link).
	Indistractable_ How to Control Your Attent - Nir Eyal.pdf+ 1

#### Phase 3: Environmental Containment (In-Box Execution)

1. Single-Task Focus Lock: Work vertically inside the single agreed slice.
2. Internal Trigger & Rabbit-Hole Surfing: If an impulse to check feeds or refactor unrelated code hits, do not switch windows. Jot the distraction or tangential question onto a scratchpad (`00_Inbox/` or a `HEAD - …?` candidate) and return to the active box without self-judgment.
	Indistractable_ How to Control Your Attent - Nir Eyal.pdf+ 3

#### Phase 4: The Guillotine & Somatic Switch (On Stop / Box Exit)

When the timer rings, working past the boundary without an explicit decision is forbidden:

1. The Triage Decision: Immediately choose one of three exits:
	Time Blocking vs Timeboxing: What's the Difference? - Planzer.io
	- Ship It: The acceptable standard is met; mark complete.
		Time Blocking vs Timeboxing: What's the Difference? - Planzer.io+ 1
		- Extend Once (On Purpose): Allocate one bounded, shorter box _only_ if you explicitly name which downstream block moves to absorb the cost.
		Time Blocking vs Timeboxing: What's the Difference? - Planzer.io
		- Park It (`#SAVESTATE`): Stop immediately and execute State Capture.
		Time Blocking vs Timeboxing: What's the Difference? - Planzer.io
2. State Capture (`#SAVESTATE`): Write a single sentence logging the current state and the exact physical MVA required to resume next time, offloading working memory residue.
	Deep Work_ Rules for Focused Success in a - Cal Newport.pdf
3. The Somatic Switch Protocol: To sever lingering attention residue from the previous task and force the TPN back online, execute an immediate, unrelated physical movement (e.g., 60-second isometric hold, balance drill, or stepping away from the desk) before touching the next timebox.

### Part 2: Full-Context Prompt for Your Local LLM / CLI Agent

Copy and paste the prompt block below into your local LLM / CLI agent (`Claude Code`, `agy`, or local Ollama/vLLM harness with MCP/filesystem access to `/Volumes/DAL/Zettelkasten/LLMeon/`). It includes batched file-reading rules to prevent local LLM context degradation and enforces all `AGENTS.md`, TAC frontmatter, and `edge_lint.py` invariants.

```
# Role & Objective
You are my Principal Knowledge Architect and Systems Engineer operating on the LLMeon / ProdOS v5.0 vault at `/Volumes/DAL/Zettelkasten/LLMeon/`.

Your objective is to update our ProdOS source-of-truth notes, Chief of Staff (CoS) protocols, and prompt router to codify our ADHD Executive Function Prosthetic Time-Blocking & Time-Boxing Protocol.

---

## 1. Non-Negotiable Vault Governance & Safety Guards (`AGENTS.md`)

> [!warning] Own-words guard
> Never edit, merge into, rename, move, or delete a protected note, and never set or change `own_words` (`[[AGENTS]]` §6). Protected notes are any note with `own_words: true` and every existing note in `01_journals/` and `20_Thinking/`. Skip them as write targets and put suggestions in chat or in a new `00_Inbox/` note. This overrides any instruction below.

1. Local LLM Context Window Protection (Batched I/O): Do NOT read more than 3–4 files into context in a single turn. Inspect files in small batches, summarise exact line targets, and apply unified diffs incrementally.
2. Typed Edge Syntax (`edge_lint.py` Compliance): Use the vault's canonical un-commented inline edge syntax `[verb:: [[Target]], confidence=high|medium|low]` using only the 7 valid verbs (`supports`, `depends_on`, `implements`, `contradicts`, `extends`, `revises`, `rel`). Do NOT wrap edges in `%%...%%` comments.Canonical SoTs (`type: sot`) must never emit downward `depends_on` edges to protocols; downstream `type: protocol` notes must emit `[implements:: [[SoT - ...]]]` upward to SoTs.
3. Frontmatter Contract (TAC): Every created or modified note must pass `10_System/scripts/validate_note_frontmatter.py` (`conformant: true`, valid closed `type` enum such as `sot` or `protocol`, valid `tags` array, updated `modified` ISO timestamp). If any prompt note's `OUTPUT FORMAT` contains a YAML template, it must explicitly include `conformant` and `non_conformance_reason`.
4. No Inline `## Tensions` in Canonical Notes: Per `[[SoT - HEAD Note Contract (The Workbench)]]` §4, never add `## Tensions` prose blocks to SoTs or Protocols; use `> Open threads: [[HEAD - ...]]` callouts if needed.

---

## 2. Phase 1: Batched Read-Only Discovery

Read the following files in two small batches using your filesystem/MCP read tools to verify current structure and line numbers before proposing edits:

- Batch A (Core Specs & Temporal SoTs):
  1. `AGENTS.md`
  2. `30_Library/SoT/SoT - Temporal Management (Blocking and Boxing).md`
  3. `30_Library/SoT/SoT - PRODOS Core Specification.md`
  4. `30_Library/200_Projects/gtd-action-system.md`
- Batch B (CoS Execution Protocols & Prompt Router):
  1. `10_System/prompts/Protocol - Daily Plan (Sunsama Timeboxing).md`
  2. `30_Library/100_zettelkasten/Protocol - Big Rocks (Weekly Quadrant II Outcomes).md`
  3. `30_Library/100_zettelkasten/Protocol - Action-First GTD (LLM Chief of Staff).md`
  4. `10_System/prompts/00 - Prompt Library Router.md`

Stop after reading Batch A and Batch B and verify that none of the target files carry `own_words: true`.

---

## 3. Phase 2: Exact Architectural Specifications to Implement

Update or create the following vault files to establish a seamless macro-to-micro prosthetic pipeline:

### Target 1: Update `30_Library/SoT/SoT - Temporal Management (Blocking and Boxing).md`
Ensure this SoT serves as the canonical theoretical and operational contract for time management in ProdOS:
1. Formal Distinction (Blocking vs. Boxing):
   - Time Blocking ("When" / Macro-Reservation): Reserving calendar space in advance to protect Quadrant II capacity from shallow encroachment (Cal Newport *Deep Work* rhythmic/journalistic scheduling).
   - Time Boxing ("How Long + Done Means" / Micro-Constraint): Allocating a fixed maximum duration (`15m`, `30m`, or `60m`) paired with an explicit, "acceptable rather than perfect" deliverable and an unyielding hard stop (Marc Zao-Sanders / Nir Eyal *Indistractable* traction model).
1. Neuro-Physiological Mechanism: Document why both are required for ADHD: Time blocking eliminates point-of-performance scheduling decisions, while time boxing caps perfectionism, visualises hidden WIP, and pairs with the Somatic Switch to toggle from the Default Mode Network (DMN) to the Task Positive Network (TPN) and clear attention residue.
2. Two-Window Batched Shallows ("Drain the Shallows"): Define the two daily 20-minute comms triage boxes (10:30 and 15:30) for email/Teams/NHS trust threads (<2m reply immediately; >2m actionable -> undated Todoist runway; blocked on external party -> `#Waiting`).
3. Canonical Edges: Strip any legacy bare `rel::` lines and ensure upward/lateral links use valid `[depends_on:: [[SoT - The Cognitive Physiology of Task Execution]], confidence=high]` and `[depends_on:: [[SoT - PRODOS Core Specification]], confidence=high]`.

### Target 2: Update `30_Library/100_zettelkasten/Protocol - Big Rocks (Weekly Quadrant II Outcomes).md`
Resolve the documented open questions so `/daily-plan` has deterministic rules:
1. Week Start Day: Lock to Monday (aligning with the Monday CoS candidate proposal and the Friday 16:30 Weekly Command Centre floor).
2. Reduced Cap Threshold (1–2 Big Rocks): Trigger deterministically when existing fixed calendar commitments leave < 20 hours of open work capacity for the week (otherwise cap at 3 Big Rocks).
3. Visibility Metric (`X of Y minutes`): Lock `X` = cumulative weekly minutes scheduled on tasks aligned to Sunsama weekly objectives (`align_task_with_objective`), and `Y` = sum of the weekly objectives' target time estimates in `sunsama://objectives`.

### Target 3: Update `10_System/prompts/Protocol - Daily Plan (Sunsama Timeboxing).md`
Refine `/daily-plan` so macro time-blocking and micro time-boxing hand off cleanly:
1. Step 0 Morning Reset & Shutdown Guard: Before scheduling, audit `(overdue | today) & no deadline` in Todoist (stripping stale `Today` dates back to the flat runway) and return any leftover uncompleted soft tasks in Sunsama to the backlog (`move_task_to_backlog`). Never roll soft tasks to tomorrow.
2. Protection Priority & Sizing: Schedule in strict order: `Renewal > Big Rocks (aligned to sunsama://objectives) > Other Actions (Runway) > Two 20m Comms Triage Boxes > 25% Unscheduled Buffer`. Size standard execution boxes at `15m`, `30m`, or `60m`.
3. Parallel Agent Blocks: Use `set_task_parallel` when scheduling concurrent terminal agent supervision (`Zellij` + `agy` / `Claude Code`).
4. Task-Authoring Gate Stubs & Deep Links: For every scheduled Big Rock or deep-work timebox, output the `sunsama://action/details/<task-id>` link alongside a pre-populated MVA (<120s) prompt stub ready for `/engage-action`.
5. Typed Edges: Add `[implements:: [[SoT - Temporal Management (Blocking and Boxing)]], confidence=high]` and `[implements:: [[SoT - Execution Protocol (GTD & PARA)]], confidence=high]`.

### Target 4: Create `10_System/prompts/Protocol - Engage Action (Prosthetic Timebox & Somatic Switch).md`
Create the missing operational companion prompt for `/engage-action` ("start box", "engage", "help me start/switch") that governs a single active timebox from Pre-Flight to Hard Stop:
- Frontmatter:
  ```yaml
  ---
  title: Protocol - Engage Action (Prosthetic Timebox & Somatic Switch)
  description: Run the CoS prosthetic executive function loop for a single 15m/30m/60m timebox: Pre-Flight Task-Authoring Gate (Done means, <120s MVA, 1-15m Starter Task, PINCH/Effort Pact), Environmental Containment, and Guillotine Hard Stop (#SAVESTATE + Somatic Switch).
  type: protocol
  status: active
  tags:
    - agent/chief-of-staff
    - domain/prodos
    - type/protocol
  conformant: true
  ---

- Required Callouts at Top of Body:
	- Include the mandatory `> [!warning] Own-words guard` block.
		- Include `> Trigger: /engage-action, "start timebox", "I'm stuck on this ticket", or "time's up / switch". For full-day macro scheduling, use [[Protocol - Daily Plan (Sunsama Timeboxing)]].`
		- Include `> Output Contract: follow [[Protocol - Typed Answer Contract (TAC) for Vault Agents]]—confidence, evidence (linked source notes), and an explicit uncertainty flag replace free prose in every output.`
- Body Phases:
	1. Phase 1: Pre-Flight Negotiation (The Task-Authoring Gate):
		- Refuse to start the timer until the user defines:
			- `Done means:` The single visualisable, "acceptable rather than perfect" artifact achievable within `15m`, `30m`, or `60m`. Slice scope if too broad.
						- `Steps (Two-Tier Ignition):` (a) MVA (<120s) bodily action with binary Yes/No check; (b) Starter Task (1–15m) momentum ramp.
						- `If stuck (PINCH + Effort Pact):` Select one PINCH catalyst (*Play, Interest, Novelty, Competition, Hurry*) + confirm external triggers are blocked and `sunsama://action/details/<id>` timer is active.
		2. Phase 2: In-Box Containment (Urge Surfing):
		- Instruct the user that if an internal trigger (boredom, uncertainty, perfectionism) or rabbit-hole urge fires during the box, they must dump a 1-line note into `00_Inbox/` (or a `HEAD - ...?` candidate) and stay inside the box until the timer rings.
		3. Phase 3: The Guillotine (`On stop` / Box Exit & Somatic Switch):
		- When the timer rings, mandate an immediate hard stop and force one of three choices:
			1. Ship It: Mark task complete in Sunsama/Todoist.
						2. Extend Once (Conscious Trade-off): Add one bounded 15m/30m box *only* after naming which block comes off today's schedule.
						3. Park It (`#SAVESTATE`): Write a 1-sentence state capture + next `<120s` MVA into the task comment/note so working memory can release the loop.
				- Mandatory Somatic Switch: Prescribe an immediate 60-second physical reset (isometric hold, balance exercise, hydration walk) to clear attention residue and re-engage the TPN before starting the next block.
- Related Links Section:
	- `[implements:: [[SoT - Temporal Management (Blocking and Boxing)]], confidence=high]`
		- `[implements:: [[SoT - PRODOS Core Specification]], confidence=high]`
		- `[depends_on:: [[SoT - The Cognitive Physiology of Task Execution]], confidence=high]`
		- `[extends:: [[Protocol - Daily Plan (Sunsama Timeboxing)]], confidence=high]`

### Target 5: Wire Into Protocol - Action-First GTD (LLM Chief of Staff).md & 00 - Prompt Library Router.md

1. In `30_Library/100_zettelkasten/Protocol - Action-First GTD (LLM Chief of Staff).md`:
	- Under `### B6. Daily Plan (Sunsama Execution Surface)` (or a new `### B7. Engage Action (Prosthetic Timebox Loop)`), add the hand-off from `/daily-plan` (macro blocking) to `/engage-action` (`[[Protocol - Engage Action (Prosthetic Timebox & Somatic Switch)]]`) and add the corresponding `[extends:: ...]` typed edge in the Related section.
2. In `10_System/prompts/00 - Prompt Library Router.md`:
	- Add `conformant: true` to the router's YAML frontmatter if still missing so it passes `validate_note_frontmatter.py`.
		- Under `### Daily Execution (Todoist → Sunsama)`, add the routing row for `/engage-action` → `[[Protocol - Engage Action (Prosthetic Timebox & Somatic Switch)]]`.

## 4. Phase 3: Apply Changes & Run Vault Validators

1. Show concise unified `diff` blocks for each modified/created file and apply the edits cleanly.
2. Run the vault validators from the root directory:
	- `python3 10_System/scripts/validate_note_frontmatter.py` on all touched files.
		- `python3 10_System/scripts/edge_lint.py` and verify 0 new errors in any touched file.
3. Output a TAC-compliant completion summary stating confidence, exact files modified/created, validator exit codes, and any open flags.
```
