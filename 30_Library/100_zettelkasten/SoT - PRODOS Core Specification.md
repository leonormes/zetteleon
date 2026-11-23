---
aliases:
  - MOC - ProdOS
  - PRODOS
  - ProdOS Index
  - ProdOS Thinking Stream
  - Productivity Operating System
  - SoT - PRODOS (System Architecture)
  - SoT - ProdOS Thinking Stream
  - Start Here
conformant: true
contrasts_with:
  - "[[The Danger of Perpetual System-Building]]"
  - "[[The Trap of the Architect Is Sophisticated System-Building Substituting for Physical Action]]"
created: 2026-01-03T09:45:08+00:00
merged_from:
  - "[[SoT - ProdOS Thinking Stream]]"
  - "[[SoT - Cognitive Engineering Protocols]]"
modified: 2026-11-17T14:05:00+00:00
permalink: llmeon/30-library/so-t/so-t-prodos-core-specification
project_category: prodos
see_also:
  - "[[MOC - Action Management]]"
  - "[[MOC - ADHD (The Master Map)]]"
  - "[[MOC - Interpretation of References]]"
  - "[[SoT - The Extended Mind]]"
  - "[[SoT - Unified Writing to Think Process]]"
status: stable
tags:
  - adhd-optimization
  - execution
  - moc
  - prodos
  - SAVESTATE
  - SoftwareEngineering/Architecture
  - system-architecture
  - system/protocol
  - thinking
  - workflow
tension:
  - "[[The Three Rules of Starter Tasks]]"
  - "[[Self-Insights That Prescribe More Planning Are the Least Trustworthy Kind]]"
  - "[[Claim - Thinking Earns Its Place by Improving Model Fidelity]]"
  - "[[Claim - A Note That Does Not Help You Act Is Noise]]"
tier: 1-Foundation
title: SoT - PRODOS Core Specification
type: sot
upstream:
  - "[[Meta MOC - The Core Domains]]"
---

# PRODOS — Unified System Specification & Master Hub

> Single source of truth and entry map for ProdOS: core axioms, the PINCH dopamine engine, the Thinking Stream intake loop, execution/refinement/review protocols, and philosophical guardrails.

## 1. The Core Kernel & Architecture

### 1.1 The Definition & Dual-Axis Model

PRODOS is a Thinking Utility designed to convert Neural Potential into Kinetic Value. It treats the human as the Problem Definer and the system as the Executor.

- **The Logic–Dopamine Mismatch:** Logic provides direction (steering), but only Dopamine provides movement (fuel).
- **The Metric:** We measure **Actions Taken** vs. **Intentions Formed**. Motivation is a _result_ of action, not the cause.
- **Dual-Axis Model:** Azimuth (Time) and Elevation (Attention).

### 1.2 The Five Axioms

1. **Utility Over Truth:** If a note doesn't help you act, it is noise. _Scope: this holds inside execution (GTD tasks). It is not applied to the thinking layer, where notes earn their place by improving model fidelity at corpus level; see [[Claim - Thinking Earns Its Place by Improving Model Fidelity]], which revises [[Claim - A Note That Does Not Help You Act Is Noise]], and [[SoT - Processing IS the Work]] §6._
2. **Throughput Over Storage:** The system is for Compute, not a database.
3. **Low Maintenance:** Operates with < 10% Maintenance Load.
4. **Context is Scarcity:** Aggressively compact context to protect attention.
5. **The 70% Rule:** A 70% "perfect" action that is Done is superior to a 99% "perfect" action that is Active.

### 1.3 Theoretical & Structural Foundations

- [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]]—_Action-Container-Thought convergent kinetic valve._ [synthesizes:: [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]], confidence=high]
- [[SoT - Prosthetic Executive Function]]—_Designing environmental triggers, visual timers, and runways as external executive function._ [depends_on:: [[SoT - Prosthetic Executive Function]], confidence=high]
- [[SoT - The Cognitive Physiology of Task Execution]]—_Initiation, encoding, monitoring, and dopamine dynamics._ [depends_on:: [[SoT - The Cognitive Physiology of Task Execution]], confidence=medium]
- [[SoT - The Extended Mind]]—_Active externalism: cognition extended across digital and physical tools._ [depends_on:: [[SoT - The Extended Mind]], confidence=medium]
- [[SoT - Behavioral Architecture]]—_Environmental determinism over internal willpower ("Pipes over Water")._ [depends_on:: [[SoT - Behavioral Architecture]], confidence=medium]
- [[You Fall to the Level of Your Systems, Not Rise to Your Goals]]—_Systems-over-goals premise behind Low Maintenance & Firmware._ [depends_on:: [[You Fall to the Level of Your Systems, Not Rise to Your Goals]], confidence=high]
- [[Writing Acts as an External Working Memory]]—_Why offloading open loops onto text clears working memory capacity._ [depends_on:: [[Writing Acts as an External Working Memory]], confidence=high]

---

## 2. The Dopamine Engine (The PINCH Model & Ignition)

### 2.1 The Five PINCH Drivers

When a task lacks intrinsic motivation, the Problem Definer must "gamify" execution using one of these five drivers:

- **Play / Passion:** Can I make this fun?
- **Interest:** Can I learn something new?
- **Novelty:** Can I do this in a weird way?
- **Challenge / Competition:** Can I beat my high score / the clock?
- **Hurry:** Can I beat the alarm?

### 2.2 The Ignition Protocol ("Heat")

If you are stuck in "Logic Mode," use one of these to generate movement via the PINCH Model:

1. **Mystery:** "I wonder if I can do this without using [Tool]?"
2. **Urgency:** "I have 5 minutes. How much can I get done?"
3. **Spite:** "I'm going to finish this to prove [Idea] wrong."

---

## 3. The Thinking Stream (RAM & 120s Intake Loop)

The Thinking Stream is the "RAM" of ProdOS—a low-friction, high-throughput loop for converting raw mental noise into structured knowledge or physical action. It relies on the **Rule of Zero Toil**: if it feels like "organizing," stop. The goal is rapid context restoration and momentum generation.

### 3.1 The Core Lifecycle (CRPE)

1. **CAPTURE:** Dump mental noise into the Daily Note (`00_Inbox/dump.md` in agent Mode B). Raw text, no formatting, no judgment. Translating abstract feeling and unprocessed noise into linear syntax activates the Prefrontal Cortex (PFC), dampening Amygdala/Mid-Cingulate stress loops and freeing Working Memory RAM (_Neuro-Synchronization_). If the dump is overwhelming, cap it at the top 10 loudest items and triage via [[Protocol - Action-First GTD (LLM Chief of Staff)]].
2. **REFINE:** If an idea is complex or "stuck" and leaves a question that needs your judgement, open a `HEAD - <question>?` note in `20_Thinking/21_Workbench/`. Admission rules live in [[SoT - HEAD Note Contract (The Workbench)]].
3. **PROCESS (The 120s Loop as Cognitive Defrag):** Bypasses the "Dumb Zone" of over-deliberation by shifting from Logic Mode (direction) to Dopamine Mode (fuel):
   - **Goal:** What is the single, physical outcome desired?
   - **Block:** What is the exact friction preventing progress?
   - **MVA:** What is the next physical step that takes < 120 seconds?
4. **EXIT:**
   - Action? $\rightarrow$ Move to Todoist (see [[SoT - GTD Action System]]).
   - Fact / Insight? $\rightarrow$ Extract into atomic `claim` (or `concept`/`evidence`/`procedure`) notes in `30_Library/100_zettelkasten/` first, then compile/transclude into an `SoT -` argument thread (`![[...]]` + `[depends_on:: [[Claim]]]` / `[synthesizes:: [[Note]]]`) via [[Prompt - ProdOS Chronos Synthesizer]], and archive the HEAD note (leave a tombstone if other notes cite it; see HEAD Note Contract §3.1).
   - Skill / Project? $\rightarrow$ Move to the Hangar (`30_Library/200_projects/`).
   - Noise? $\rightarrow$ DELETE (raw captures only; never delete a HEAD note cited as `upstream`).

### 3.2 Thinking Stream Guardrails

- **FLAT WORKBENCH:** No sub-folders inside `20_Thinking/21_Workbench/`; it is a flat queue of questions.
- **NO POLISHING:** Clarity of thought is superior to aesthetics of layout.
- **NO SILENT ROT:** A thought that cannot name what would settle it is debt. Fix it in place, resolve it, or archive it per [[SoT - HEAD Note Contract (The Workbench)]]; do not leave it open by default.

- [[SoT - HEAD Note Contract (The Workbench)]] [depends_on:: [[SoT - HEAD Note Contract (The Workbench)]], confidence=medium]
- [[SoT - Unified Writing to Think Process]] [supports:: [[SoT - Unified Writing to Think Process]], confidence=high]

---

## 4. Phase 1: Capture & Execution Protocols (Action Mode)

_From unclarified capture to binary Minimal Viable Actions (MVAs) and physical execution._

### 4.1 The Scope-Lock & Starter Task (MVA)

The Minimal Viable Action (MVA) is the atomic unit of execution:

- **Rule:** The MVA must be a physical, binary task so small it is impossible to fail (e.g., "Open the code editor").
- **Energy:** Reduce Activation Energy to $\approx 0$.
- **The Unit Test:** Can you say "Yes/No" to success in < 120 seconds?
- **Checklist Firmware:** Use Instruction SoTs to offload working memory for complex tasks.
- **Open tension:** [[The Three Rules of Starter Tasks]] allows a starter task 5 to 15 minutes against the 120 seconds here; the two are not yet reconciled.

### 4.2 State Management (Cryosleep / `#SAVESTATE`)

- **Timestamp:** `YYYY-MM-DD-HHmm`
- **The Conflict:** What perfectionist block did we hit?
- **The Current State:** The new hypothesis.
- **The Next Test:** The immediate next Starter Task.

### 4.3 Execution, Decomposition & Launch Protocols

- [[Protocol - Action-First GTD (LLM Chief of Staff)]]—_Decoupling raw capture (Human) from task sorting (LLM/MCP, including Mode B agent orchestration)._ [synthesizes:: [[Protocol - Action-First GTD (LLM Chief of Staff)]], confidence=high]
- [[SoT - Execution Protocol (GTD & PARA)]]—_Harmonized PARA containers, GTD outcome projects, 5-stage workflow, and Definition of Done._ [synthesizes:: [[SoT - Execution Protocol (GTD & PARA)]], confidence=high]
- [[SoT - GTD Action System]]—_The live four-tier operational implementation across Obsidian, Jira, Todoist, and the native calendar._ [synthesizes:: [[SoT - GTD Action System]], confidence=high]
- [[Protocol - Vague-to-Action]]—_Three-phase algorithm decomposing vague/heavy avoidance items into <120s binary MVAs._ [synthesizes:: [[Protocol - Vague-to-Action]], confidence=high]
- [[SoT - Protocol - The Launch Sequence]]—_Situated, embodied, and distributed scaffolding to bypass task initiation paralysis._ [synthesizes:: [[SoT - Protocol - The Launch Sequence]], confidence=high]
- [[SoT - PRODOS Black Box Protocol]]—_Open-loop post-mortems, pre-mortems, marginal gains, and checklist simplification._ [synthesizes:: [[SoT - PRODOS Black Box Protocol]], confidence=high]
- [[SoT - Temporal Management (Blocking and Boxing)]]—_Time-blocking vs. time-boxing constraints._ [synthesizes:: [[SoT - Temporal Management (Blocking and Boxing)]], confidence=medium]
- [[SoT - ADHD Management Protocols]]—_Dopamine menu and neurodivergent operating toolkit._ [synthesizes:: [[SoT - ADHD Management Protocols]], confidence=medium]

---

## 5. Phase 2: Thinking, Refinement & Data Schema (Architect Mode)

_Converting messy drafts and research into verified atomic propositions, structured graphs, and agent contracts._

### 5.1 Data Schema & Context Architecture

- **HEAD Notes:** Active thinking and open-question queue in `20_Thinking/21_Workbench/`. Admission and lifecycle: [[SoT - HEAD Note Contract (The Workbench)]].
- **SoT & Atomic Notes:** Proposition cards (`claim`, `concept`, `evidence`, `procedure`) hold evidenced, falsifiable assertions and know-how in `30_Library/100_zettelkasten/`. `SoT` notes are compiled logical argument threads built from those atomic notes via transclusion (`![[...]]`), alongside Instruction SoTs (Checklists).
- **The Context Cache (`.ai/`):** Not built. Agent context today comes from `AGENTS.md`, the Prompt Library Router, and 1MCP; see [[SoT - AI Agent Skill Architecture]].

### 5.2 Refinement, Graph & Agent Governance Standards

- [[Reference - File Structure]]—_`AGENTS.md` §0 vault topology (Inbox, Journals, Bases, System, Workbench, flattened Zettelkasten, Projects, Ops)._ [synthesizes:: [[Reference - File Structure]], confidence=high]
- [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]—_Authoritative YAML note schemas driving Fileclass and Bases._ [synthesizes:: [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]], confidence=high]
- [[SoT - HEAD Note Contract (The Workbench)]]—_The four compliance tests, tension pointers, and exit lifecycle for `20_Thinking/21_Workbench/`._ [synthesizes:: [[SoT - HEAD Note Contract (The Workbench)]], confidence=high]
- [[SoT - Processing IS the Work]]—_Processing, linking, and synthesis as the core intellectual product (bounded to PKM/learning)._ [synthesizes:: [[SoT - Processing IS the Work]], confidence=high]
- [[SoT - Unified Writing to Think Process]]—_Six-stage writing-to-think pipeline (Stages 0–5), culminating in [[Stage 5 Synthesise (The Outcome Layer)]]._ [synthesizes:: [[SoT - Unified Writing to Think Process]], confidence=high]
- [[SoT - Atomic Note Standard (The Proposition Card)]]—_Proposition-card structure and atomicity validation._ [synthesizes:: [[SoT - Atomic Note Standard (The Proposition Card)]], confidence=high]
- [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]] & [[SoT - Knowledge Compiler (Argument Graph Spec)]]—_The 7 canonical predicates and argument-graph compiler._ [synthesizes:: [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]], confidence=high] [synthesizes:: [[SoT - Knowledge Compiler (Argument Graph Spec)]], confidence=high]
- Context Engineering—_Signal density over accumulation for LLM workflows._
- [[SoT - Research-to-Action Protocol]]—_Time-boxed 20-minute technical research with hard start and `#SAVESTATE` exit._ [synthesizes:: [[SoT - Research-to-Action Protocol]], confidence=high]
- [[SoT - Perfectionism and Analysis Paralysis]]—_Breaking the all-or-nothing fear loop with MVA, messy HEAD drafts, and iterative synthesis._ [synthesizes:: [[SoT - Perfectionism and Analysis Paralysis]], confidence=high]
- [[SoT - Typed Answer Contract (TAC) for LLM Output]]—_Unified 4-rule output contract, RAG schema ceiling, and two-tier structural validation gates for vault agents._ [synthesizes:: [[SoT - Typed Answer Contract (TAC) for LLM Output]], confidence=high]

---

## 6. Phase 3: Review, Maintenance & Dashboards (Reflect Mode)

_Recalibrating the system without letting system maintenance turn into avoidance._

- [[Protocol - Weekly Command Centre]]—_Fixed 10-minute Friday reset loop for Todoist triage and runway repair._ [synthesizes:: [[Protocol - Weekly Command Centre]], confidence=high]
- [[Protocol - Workbench Compliance Sweep]]—_Auditing `20_Thinking/21_Workbench/` against the four HEAD tests and routing stale threads._ [synthesizes:: [[Protocol - Workbench Compliance Sweep]], confidence=high]
- [[SoT - Principles for Peaceful Productivity]]—_Ten day-level operating principles grounded in environment engineering._ [synthesizes:: [[SoT - Principles for Peaceful Productivity]], confidence=high]

### 6.1 System Dashboards (`.base` HUD)

- [[Thinking.base|Active Thinking Threads (RAM)]]
- [[SoT.base|All Source of Truth Notes]]
- [[MOCx.base|All Maps of Content]]

---

## 7. Philosophical Foundations & Guardrails

_Purpose lineage, cognitive limits, and anti-bloat boundary conditions._

- The Telos Method—_Seven-layer Chain of Explainability (`Problem -> Mission -> Narratives -> Goals -> Challenges -> Strategies -> Projects`)._
- [[SoT - The User Interface of the Self]]—_Consciousness as retrospective integration UI rather than central executive command._ [synthesizes:: [[SoT - The User Interface of the Self]], confidence=high]
- [[SoT - Material Symbols]]—_Language, notation, and templates as cognitive scaffolding enabling second-order inspection._ [synthesizes:: [[SoT - Material Symbols]], confidence=high]
- [[Self-Insights That Prescribe More Planning Are the Least Trustworthy Kind]]—_Scope guardrail against mistaking architectural planning for execution._ [depends_on:: [[Self-Insights That Prescribe More Planning Are the Least Trustworthy Kind]], confidence=high]
- [[Claim - Thinking Earns Its Place by Improving Model Fidelity]]—_Thinking-side counter-balance revising [[Claim - A Note That Does Not Help You Act Is Noise]] (retired execution-only position)._

### 7.1 Related System Maps

- [[MOC - ADHD (The Master Map)]]—_Strategies for the neurodivergent brain._
- [[MOC - Action Management]]—_Mechanics of task flow and execution._
- [[MOC - Interpretation of References]]—_Semantics of reference types and epistemic standing._
