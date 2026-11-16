---
aliases:
  - Automation as Behavior
  - Cognitive Prosthetics
  - Digital Tools Help Externalize Memory and Structure for ADHD Developers
  - External Brain
  - External Structure and ADHD
  - Externalizing Cognition
  - Point of Performance Engineering
  - Prosthetic Executive Function
conformant: true
created: 2026-01-12T12:25:00+00:00
domain: "[[MOC - ADHD (The Master Map)]]"
merged_from:
modified: 2026-11-15T10:42:00+00:00
permalink: llmeon/30-library/so-t/so-t-prosthetic-executive-function
project_category: prodos
review_cycle: quarterly
scope: Structural framework and empirical boundary conditions for compensating for adult ADHD executive dysfunction through external environmental, digital, and human scaffolding, distinguishing EF-independent push floors from EF-dependent pull tools.
status: stable
tags:
  - cognitive-scaffolding
  - extended-mind
  - prosthetic-ef
  - sot
  - TheHuman/Health/ADHD
  - topic/productivity
title: SoT - Prosthetic Executive Function
type: sot
---

# SoT - Prosthetic Executive Function

> Core Thesis: Because adult ADHD impairs executive self-regulation at the point of performance, effective compensation requires shifting load from internal willpower to external scaffolding. However, an external tool is only a true **prosthetic floor** to the degree that it is **EF-independent**—pushed by the environment, automated with visible failure alarms, or anchored by a human. Any tool that must be remembered, opened, maintained, and obeyed by the user is a **point-of-performance aid (pull tool)** that remains bounded by the very executive function it is meant to replace.

---

## 1. Theoretical Foundation: Point-of-Performance Deficit & The Circularity Problem

### 1.1 The Point-of-Performance Deficit (Barkley & Brown)

Russell Barkley frames ADHD not as a deficit of knowledge or skill, but as a disorder of self-regulation and executive execution **at the point of performance**—knowing what to do, yet failing to initiate or sustain it in the moment it matters. Thomas Brown organises these impairments into six functional clusters:

1. **Activation**: Organising, prioritising, and initiating work.
2. **Focus**: Sustaining and shifting attention to tasks.
3. **Effort**: Regulating alertness, sustaining effort, and processing speed.
4. **Emotion**: Managing frustration and modulating affect.
5. **Memory**: Utilizing working memory and accessing recall.
6. **Action**: Monitoring and self-regulating action.

Standard executive-function taxonomies (Miyake & Friedman) separate **working-memory updating**, **inhibition**, and **set-shifting**. Across clinical and cognitive models, **remembering a task (prospective memory)** and **initiating the task (activation)** are distinct bottlenecks: a reminder can fire in full view while the user remains unable to start.

### 1.2 Instrumental Offloading vs. Constitutive Extended Mind

Clark and Chalmers's [[SoT - The Extended Mind|Extended Mind Thesis]] argues that when an external store is reliably present, trusted, and directly accessible, it functions as part of the cognitive system. For adult ADHD, two readings must be kept distinct:

- **Instrumental Reading (Cognitive Offloading — Risko & Gilbert, 2016)**: Externalizing memory and triggers into physical artefacts reduces working-memory demand and improves prospective-memory fulfilment, provided the person actually uses the store.
- **Constitutive Reading**: Treating the external scaffold as literally *being* the user's executive function ([[An External Scaffold Is the Executive Function for an ADHD System and Not an Aid to It]]). Under adversarial audit, this strong claim fails whenever the coupling between brain and notebook breaks: unlike Otto's passive memory notebook, executive control includes noticing cues, resisting distractions, and initiating action—functions that an unassisted notebook cannot execute on its own.

### 1.3 The Circularity Problem (Why Most "Prosthetics" Fail)

Clinical guidelines (NICE NG87) confirm that non-pharmacological strategies cannot be assumed to replace core ADHD treatment (where stimulants show adult SMD $\approx -0.72$ to $-0.79$, Cortese et al., 2018), because environmental modifications generally require the user's own executive function to set up, remember, maintain, and obey:

- **App Abandonment**: Unguided mental-health and productivity apps show a median **15-day retention of ~3.9%** and 30-day retention of ~3.3% (Baumel et al., 2019).
- **The Coaching Confound**: Randomised trials of smartphone organisation tools in adult ADHD (e.g., *Living SMART*, Moëll et al., 2015) succeeded when paired with a **human coach** and structured curriculum—testing coached human accountability rather than standalone app efficacy.
- **Metacognitive Selection Bias**: Deciding *when* and *how* to offload is itself a metacognitive decision sensitive to confidence and perceived effort cost (Risko & Gilbert, 2016). Under stress, fatigue, or shame, offloaded systems are abandoned first.

---

## 2. The Prosthetic Taxonomy: True Floor (Push) vs. Point-of-Performance Aids (Pull)

To prevent [[The Trap of the Architect Is Sophisticated System-Building Substituting for Physical Action|The Trap of the Architect]]—mistaking complex tool configuration for an executive floor—interventions must be classified by **who or what supplies the activation energy**:

| Dimension | Tier 1: True Prosthetic Floor (EF-Independent / Push) | Tier 2: Point-of-Performance Aid (EF-Dependent / Pull) |
| :--- | :--- | :--- |
| **Activation Source** | Triggered by the environment, automation, or another human without user initiation. | Requires the user to remember, open, update, or start the tool. |
| **Daily Maintenance** | Zero or externally maintained; configured once on a high-capacity day. | Requires daily triage, inbox zeroing, time-block adjusting, or streak upkeep. |
| **Failure Mode** | Fails visibly via external alarm or human check-in if disrupted. | Fails silently via abandonment, snooze blindness, or compulsive re-planning. |
| **Primary Target** | Task elimination, environmental defaults, and externally pushed initiation. | Working-memory offloading, time visualisation, and micro-step decomposition *after* engagement. |
| **Examples** | Direct debits with balance alerts, medication blister packs on the kettle, scheduled human body-doubling/coaching, NeuroPage-style pushed pages. | Task managers (Todoist), notes vaults (Obsidian), visual timers, LLMs, focus audio, auto-schedulers. |

---

## 3. Mapping Executive Clusters to Evidence-Calibrated Interventions

| Brown Cluster | Target Bottleneck | Tier 1: EF-Independent Floor (Push / Delete) | Tier 2: EF-Dependent Aid (Pull / Assist) | Empirical Evidence & Failure Modes |
| :--- | :--- | :--- | :--- | :--- |
| **1. Activation** | Crossing the initiation threshold (`E_a`) | **Scheduled human body-doubling / CBT-MCT coaching**; fixed **If–Then implementation intentions** tied to physical path cues. | **LLM task decomposer** ("break this into a 2-minute physical step"); [[Protocol - Vague-to-Action]]. | **CBT/MCT RCTs** (Safren et al., 2010 OR 4.29; Solanto et al., 2010 OR 5.41; Lopez et al., 2018 Cochrane) show strong adult efficacy. **LLMs** have qualitative support only (7-day diary study, $n=13$, ACM) and risk planning-as-avoidance. **Auto-schedulers** (Motion, Saner.AI) have **zero** peer-reviewed ADHD trials and hide failure by auto-rescheduling. |
| **2. Focus** | Resisting distraction & sustaining attention | **Physical device removal** (phone in another room/timed lockbox); OS-level hard blocks configured once. | **White/pink noise**; gamified focus timers (Forest); commercial focus audio (Brain.fm). | **White/pink noise** shows a small significant laboratory benefit in youth ($g = 0.249$, Nigg et al., 2024 *JAACAP*). **Brain.fm** (Woods et al., 2024) is company-led in general population; **Forest** has no ADHD clinical trials. |
| **3. Effort & Time** | Time blindness & temporal discounting | **Externally bounded commitments** (co-working sessions, fixed transit/meeting deadlines). | **Physical visual timers** (Time Timer) and micro-sprints ([[Sprint Journaling Prevents Overwhelm in ADHD]]). | **Time perception deficit** is well-established in youth ($g = 0.688$, Zheng et al., 2022) and present in adults (Ptacek et al., 2019), but **Time Timer RCTs** exist only in children (Janeslätt et al., 2014; Wennberg et al., 2018). Timers require remembering to start them. |
| **4. Emotion** | Frustration, shame spirals & RSD | **Pre-committed recovery defaults** and human co-regulation (pair programming, coaching review). | Written cognitive-reframing checklists and shutdown rituals. | Unguided digital tools can *worsen* shame when overdue badges accumulate; human-anchored CBT protocols explicitly target avoidance and negative automatic thoughts. |
| **5. Memory** | Prospective & working memory drop-out | **Task deletion / automation** (direct debits, standing orders) and **physical launchpads** placed in the doorway. | **Single trusted capture inbox** ([[Externalize Memory Aggressively (cognitive offloading)]]) and point-of-action checklists. | **Defaults** show robust real-world effect ($d \approx 0.68$, Mertens et al., 2022), but are **not zero-failure**—expired cards or low balances fail silently unless paired with an external failure alarm. **NeuroPage** (Wilson et al., 2001) worked in brain injury because messages were externally maintained and pushed. |
| **6. Action** | Impulse control & error monitoring | **Hard friction gates** (24-hour purchase holds, CI/CD pre-commit hooks, linter blocks). | Pre-flight review checklists in the physical or code path. | Automated linters and pre-commit gates act as true floors in software engineering because they trigger automatically on commit without relying on recall. |

---

## 4. Eight Principles for Survivable ADHD Scaffolds

1. **Delete Before You Assist**: Eliminating a recurring task (automation, standing orders, unsubscribing) beats building a tracking workflow for it.
2. **Push, Not Pull**: Any scaffold that waits for you to open a dashboard or app is a pull tool, not a floor. Prefer cues that interrupt you at the time and place of action.
3. **One-Off Setup on a Good Day, Zero Daily Maintenance**: If a system requires daily curation to stay functional, it will collapse during the next low-capacity week.
4. **Fail Visibly**: Automated systems fail silently when inputs change (expired cards, insufficient funds, revoked tokens). Pair every automation with an external failure alert or monthly human check.
5. **Use Humans for Activation**: When initiation is the bottleneck, a scheduled person (coach, colleague, body double) outperforms a solo app notification.
6. **Put Physical Cues in the Path of Action**: Pills on the kettle, launchpad by the door, and paper stack-traces on the keyboard beat items buried in a submenu.
7. **Degrade Gracefully (Minimum-Day Floor)**: Design every protocol with a "bad-day mode" (one physical next action, one capture bucket) so a missed day does not create a backlog wall.
8. **Cap Architect Time (<10%)**: Spend less than 10% of task time configuring or refactoring the system. When system maintenance exceeds execution, invoke [[Protocol - Vague-to-Action]].

---

## 5. N-of-1 Verification Protocol (ABAB Withdrawal Test)

Before promoting any tool or workflow as a permanent "prosthetic" in ProdOS, test it against three falsifiable criteria over a 4-week **ABAB withdrawal design** (1 week baseline → 1 week scaffold on → 1 week scaffold withdrawn → 1 week scaffold restored):

1. **30-Day Durability Gate**: Is the scaffold still active after 30 days without rebuilding or migrating apps?
2. **Bad-Day Survival Gate**: Does it still function on the worst 20% of sleep, mood, or unmedicated days?
3. **Primary Outcome Tracking**: Measure objective target completion (e.g., on-time starts per day, latency from alarm to first physical action in minutes, or missed recurring obligations per week) rather than subjective feeling of organisation.

---

## 6. Knowledge Graph & Typed Edges

### Foundations (North — `depends_on` / `implements`)

- [[SoT - The Extended Mind]]—_provides the cognitive-offloading and extended-cognition framework that this SoT constrains with ADHD coupling conditions._ [depends_on:: [[SoT - The Extended Mind]], strength=5, confidence=high]
- [[Executive Function Challenges are Central to ADHD]]—_defines the point-of-performance executive deficit that necessitates external scaffolding._ [depends_on:: [[Executive Function Challenges are Central to ADHD]], strength=5, confidence=high]
- [[Time Agnosia Impairs Planning for Developers with ADHD]]—_establishes the temporal-myopia deficit addressed by external temporal boundaries and visual timers._ [depends_on:: [[Time Agnosia Impairs Planning for Developers with ADHD]], strength=4, confidence=high]
- [[ADHD Causes Task Initiation Deficits Due to Dopamine Hyposensitivity]]—_explains why prospective-memory reminders alone fail to trigger task initiation without an activation scaffold._ [depends_on:: [[ADHD Causes Task Initiation Deficits Due to Dopamine Hyposensitivity]], strength=4, confidence=high]
- [[Task Management Systems Have Limited Efficacy for ADHD Productivity]]—_grounds the Circularity Problem: pull-based task managers fail when they demand the exact executive functions ADHD impairs._ [depends_on:: [[Task Management Systems Have Limited Efficacy for ADHD Productivity]], strength=5, confidence=high]
- [[Choice Architecture Designs the Environment to Make Desired Behaviors Easier]]—_implements environmental defaults, physical path cues, and friction gates to reduce executive load._ [depends_on:: [[Choice Architecture Designs the Environment to Make Desired Behaviors Easier]], strength=4, confidence=high]
- [[Externalize Memory Aggressively (cognitive offloading)]]—_implements aggressive cognitive offloading while distinguishing passive storage from active initiation._ [implements:: [[Externalize Memory Aggressively (cognitive offloading)]], strength=5, confidence=high]
- [[SoT - Behavioral Architecture]]—_operationalises the System > Willpower stance ("Pipes over Water") through EF-independent push scaffolds._ [implements:: [[SoT - Behavioral Architecture]], strength=4, confidence=high]
- [[SoT - PRODOS Core Specification]]—_realises ProdOS execution axioms through Launchpads, Checklists, and externalised triggers._ [implements:: [[SoT - PRODOS Core Specification]], strength=4, confidence=high]

### Synthesised Claims & Protocols (South — `synthesizes` / `supports`)

- [[ADHD Executive Dysfunction Needs Triggers Decided in Advance, Not Willpower in the Moment]]—_synthesises pre-committed implementation intentions and external push triggers as the core activation mechanism._ [synthesizes:: [[ADHD Executive Dysfunction Needs Triggers Decided in Advance, Not Willpower in the Moment]], confidence=high]
- [[The Trap of the Architect Is Sophisticated System-Building Substituting for Physical Action]]—_synthesises the primary failure mode of Tier 2 pull tools: compulsive system-building disguised as executive scaffolding._ [synthesizes:: [[The Trap of the Architect Is Sophisticated System-Building Substituting for Physical Action]], confidence=high]
- [[Protocol - Vague-to-Action]]—_synthesises the 3-step physical launch protocol used to cross the initiation threshold when a pull system stalls._ [synthesizes:: [[Protocol - Vague-to-Action]], confidence=high]
- [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]]—_supports A-C-T's externalised Action-Container-Thought boundaries._ [supports:: [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]], strength=4, confidence=high]

### Tensions & Maps

- [[An External Scaffold Is the Executive Function for an ADHD System and Not an Aid to It]]—_strong constitutive thesis contrasted in §1.2: whereas that seed claim treats the scaffold as literally being the executive function, this SoT holds that an external tool is only a true floor when its coupling is EF-independent (push/automated/human-anchored)._
- [[Digital Tools Cannot Replace the Cognitive Processes of Understanding and Connecting Ideas]]—_bounds cognitive offloading: external tools can hold prospective reminders and structural boundaries, but cannot perform comprehension or synthesis on the user's behalf._
- [[MOC - Action Management]]—_primary tactical action map._
