---
aliases:
- Automation as Behavior
- Externalizing Cognition
- Point of Performance Engineering
- Prosthetic Executive Function
conformant: true
created: 2026-01-12T12:25:00+00:00
last-synthesis: 2026-04-04
modified: 2026-11-14T09:30:00+00:00
non_conformance_reason: ''
permalink: llmeon/30-library/so-t/so-t-prosthetic-executive-function
tags:
- behavior-change
- prodos/sot
- systems-engineering
- TheHuman/Health/ADHD
title: SoT - Prosthetic Executive Function
type: sot
---

## Prosthetic Executive Function

If the internal executive function (willpower/working memory) is weak—whether due to ADHD or fatigue—we must engineer a "prosthetic" one outside the body. This is Point of Performance Engineering.

### 1. The Core Problem: The Performance Gap

In ADHD, the primary struggle is the Intention-Action Gap (or "Performance Gap"). The individual "knows what to do, but cannot do what they know" consistently. This deficit is rooted in the dysregulation of the 6 Domains of Executive Function: Activation, Focus, Effort, Emotion, Working Memory, and Action.

Reliance on internal memory or will at the "Point of Performance" is architectural negligence.

### 2. The Concept of the Prosthetic

Just as a physical prosthetic bears weight when a biological limb is missing, a Prosthetic Executive Function bears cognitive load when the biological mind is depleted or dysregulated.

- Goal: To make desired behavior independent of internal state.
- Principle: Offload the OS (Operating System) to the environment.

### 3. Automation: Choice Architecture

Utilizing [[Choice Architecture Designs the Environment to Make Desired Behaviors Easier|Choice Architecture]] to design the environment such that good choices become the path of least resistance.

- One-Time Choice vs. Recurring Effort:
    - _Recurring (Biological):_ "I must remember to save money every month." (High Failure Rate).
    - _One-Time (Prosthetic):_ Setting an auto-transfer once. (Zero Failure Rate).
- Beneficial Defaults: Engineer the environment so the "default" state leads to the desired outcome (e.g., placing gym shoes by the door).

### 4. The Tools of Prosthesis

1. Visual Timers (Time Blindness): Devices like the _Time Timer_ externalize the passage of time. They convert "felt" time into "visible" time to compensate for "Time Agnosia."
2. Launchpads (Working Memory): A specific physical tray for keys/wallet. Rule: "It exists here or in my hand." This eliminates the search subroutine and the load on working memory.
3. Checklists (Procedural Memory): An "external hard drive for process." It imposes binary logic (Done/Not Done) on a fuzzy biological system.
4. Digital Prosthetics:
    - AI Planners: (e.g., Motion, Saner.AI) for auto-scheduling, reducing the cognitive load of prioritization.
    - Focus Apps: (e.g., Brain.fm, Forest) to regulate focus and create a conducive auditory environment.
    - AI as Executive Assistant: Using LLMs to structure raw thinking into actionable steps (compensating for Activation and Working Memory deficits).

### 5. Conclusion: Systemic Reliability

The objective is to create a "floor" for your life that sustains itself even if your internal executive control is zero. Stop trying to "try harder"—engineer a better machine.

---

## Related Knowledge
- [[Executive Function Challenges are Central to ADHD]] — _the internal deficit: dysregulation across the 6 Domains of Executive Function creates the Intention-Action Performance Gap._
[depends_on:: [[Executive Function Challenges are Central to ADHD]], strength=5, confidence=high]
- [[Time Agnosia Impairs Planning for Developers with ADHD]] — _why visual timers (e.g., Time Timer) are required to externalise time._
[depends_on:: [[Time Agnosia Impairs Planning for Developers with ADHD]], strength=4, confidence=high]
- [[SoT - The Extended Mind]] — _philosophical foundation: external artefacts act as literal cognitive scaffolding under Active Externalism._
[depends_on:: [[SoT - The Extended Mind]], strength=5, confidence=high]
- [[SoT - Behavioral Architecture]] — _operationalises the System > Willpower stance ("Pipes over Water") through physical and digital prosthetics._
[implements:: [[SoT - Behavioral Architecture]], strength=4, confidence=high]
- [[SoT - PRODOS Core Specification]] — _realises ProdOS execution axioms through Launchpads, Checklists, and AI as Executive Assistant._
[implements:: [[SoT - PRODOS Core Specification]], strength=4, confidence=high]
- [[Choice Architecture Designs the Environment to Make Desired Behaviors Easier]] — _mechanism behind §3: beneficial defaults and one-time choices shift behaviour without willpower._
[depends_on:: [[Choice Architecture Designs the Environment to Make Desired Behaviors Easier]], strength=4, confidence=high]
- [[ADHD Executive Dysfunction Needs Triggers Decided in Advance, Not Willpower in the Moment]] — _supports pre-committing external triggers before the point of performance._
[supports:: [[ADHD Executive Dysfunction Needs Triggers Decided in Advance, Not Willpower in the Moment]], strength=4, confidence=high]
- [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]] — _theory behind A-C-T's externalised Action-Container-Thought boundaries._
[supports:: [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]], strength=4, confidence=high]
- [[Digital Tools Help Externalize Memory and Structure for ADHD Developers]] — _concrete tool catalogue implementing this prosthetic model._
- [[External Structure and ADHD]] — _timeboxing and rigid temporal boundaries as practical external structure._
- [[Externalize Memory Aggressively (cognitive offloading)]] — _capture and offloading discipline that keeps working memory clear._
- [[An External Scaffold Is the Executive Function for an ADHD System and Not an Aid to It]] — _pushes this instrumental prosthetic model to a strong constitutive reading._
- [[MOC - Action Management]] — _primary tactical action map._
- [[MOC - ProdOS]] — _system-level ProdOS map._

### Tensions

- [[The Trap of the Architect Is Sophisticated System-Building Substituting for Physical Action]] — _scope boundary, not contradiction: building launchpads and checklists is legitimate preparatory scaffolding only until blueprint refinement replaces physical execution._
