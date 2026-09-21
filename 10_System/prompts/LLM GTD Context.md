---
aliases: []
conformant: false
created: 2025-10-16T08:19:54+00:00
description: "Background context on the Getting Things Done (GTD) methodology — projects vs. next actions, the five phases of workflow control, and the six horizons of focus. Inject alongside planning, review, or task-triage prompts that assume GTD vocabulary."
modified: 2026-09-21T12:03:22+00:00
non_conformance_reason: Type prompt is the library-wide convention for 10_System/prompts but is not in the FrontmatterContract type enum, so all prompt notes share this error and it needs a schema decision rather than a per-note fix.
permalink: llmeon/10-system/prompts/llm-gtd-context
tags: [domain/productivity, type/context]
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

## Vault Notes (not part of the injected context)

> Stop injecting at the rule above. Everything below is vault navigation for humans and agents working in the vault, not GTD context for the LLM.

### How the vault uses this note

- [[Habit 2 - Begin with the End in Mind]] and [[Habit 4 - Think Win-Win]] depend on this note for the Horizons of Focus model (Horizons 5 and 4, and Horizon 2, respectively), because no dedicated note carries it. Do not add links or edges from here back to them.
- [[Effective Productivity Comes From the Bottom Up]] develops the Bottom-Up Focus practice from the summary above.
- [[00 - Prompt Library Router]] routes to this note as the GTD methodology background. Pair it with [[leon-context-core-profile]] for the ADHD and Chief of Staff framing.

### The vault's own GTD notes, by section

- Foundational philosophy: [[GTD and the Cognitive Load of Execution]] and [[Claim - Capture is easy but processing is hard]].
- Projects versus actions: [[SoT - Execution Protocol (GTD & PARA)]] is the vault's specialisation. It adds a PARA container above each GTD project and requires projects to be named as completed outcomes. For next actions see [[A Next Action Must Be the Absolute Next Physical Visible Activity Required to Move a Situation Forward]] and the overlapping [[Next Action is the Immediate Physical Step Forward]].
- The five phases: [[The Clarification Ritual (Stuff to Action)]], [[Every Clarified Item Must Pass a Binary Actionability Test to Determine Its Categorical Flow]], [[Never Return an Item to the In-Tray Once Picked Up for Clarification]], [[The Clarify Stage Is the Executive Decision-Making Bridge Between Stuff and Action]] and [[For ADHD The Clarification Process Externalizes Decision-Making and Builds System Trust]]. For Reflect: [[The Purpose of a Weekly Review is to Restore Trust in Your System]] and [[Weekly Review Verifies Project Actionability and Context]].
- Making action choices: [[Contexts Reduce Overwhelm and Support Working Memory for ADHD]].
- Work visibility: [[Concurrent Task Overload Creates Non-Linear Administrative Overhead That Destroys Focus]].
- Best practices: [[If a Next Action Takes Less Than Two Minutes Do It Immediately Rather Than Track It]].
- Applied elsewhere: [[Protocol - Action-First GTD (LLM Chief of Staff)]], [[Optimised GTD Context Auditor for Pieces LTM]] and [[Deep Dive Sessions for ADHD (Adapted GTD Next Actions)]].

### Where this prompt and the vault differ

- The project examples above ("Install new set of tires") are not named as completed outcomes, which the Execution Protocol SoT requires.
- The "3 Ds" line (do, delegate, defer) matches no other note in the vault. The clarification notes route non-actionable items to Trash, Incubate or Reference and do not name the Ds.
- Section 6 (Work Visibility and Flow Management) is not GTD material. It follows the work-in-progress and make-work-visible literature (see Further Reading). The twenty-minute context-switch recovery figure has no source in the vault.

### Further Reading (Personal Library)

- [Getting Things Done — David Allen, Ch. 1 "A New Practice for a New Reality"](calibre://view-book/GCcalibreBooks/1608/EPUB)—_uses the phrase "mind like water" (compared with the martial arts and the athlete's "zone"), the state section 1 names as the goal._
- [Getting Things Done — David Allen, Ch. 3 "Getting Projects Creatively Under Way"](calibre://view-book/GCcalibreBooks/1608/EPUB)—_describes the next-action decision as asking what, specifically, you would physically do about something if you had nothing else to do, which is the test behind section 2._
- [Making It All Work — David Allen, Ch. 6 "Getting Control: Clarifying"](calibre://view-book/GCcalibreBooks/226/PDF)—_notes that active projects all have specific next actions determined, while the someday category has none attached._
- [Making Work Visible — Dominica DeGrandis, Section 2.4 "Committing the Perfect Crime: Unplanned Work"](calibre://view-book/GCcalibreBooks/225/EPUB)—_the source family for section 6: unplanned work that is not made visible leaves no evidence of what is displacing planned work._
