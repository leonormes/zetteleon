---
aliases: [ADHD Creation Cycle, Breaking the Loop, Continuation Protocol]
conformant: true
created: 2025-11-13T00:00:00+00:00
modified: 2026-10-22T15:11:12+00:00
non_conformance_reason: ''
permalink: llmeon/30-library/so-t/so-t-breaking-the-creation-cycle
tags: [developer_workflow, mental_model, TheHuman/Health/ADHD, topic/productivity]
title: SoT - Breaking the Creation Cycle
type: sot
---

## 1. The Core Problem: "The Fresh Start Loop"

> The Pattern: " You start a project with high dopamine and a rich mental model. When you stop, the mental model evaporates. Returning feels \"flat\" and confusing because the context is gone."
> The Maladaptive Response: " You start fresh (re-write, re-factor, new repo) to generate dopamine and a clean mental model, abandoning the previous work."

---

## 2. The Solution: Scaffolding Continuity

The goal is not to fight the brain but to build scaffolds that reduce the cost of context restoration.

### A. The "Session Snapshot" (Exit Ritual)

Make it trivial to reload your mental model. Never close a session without a State Snapshot.

Format: `SESSION.md`

- Now: Bullet points of what was just completed.
- Next: 1-3 concrete steps for the _next_ session (≤ 15 mins each).
- Why: The design intent and constraints (Plain English).
- WTF Guide: Traps, open questions, and things you are avoiding.
- Links: Critical file paths, commands, logs.

> Developer Tip: Use commit messages like `feat: done X; NEXT: do Y; WHY: constraint Z` so `git log -1` acts as a context loader.

### B. The "Re-entry Ritual" (Entry Ritual)

Make returning low-friction and dopamine-friendly.

1. Read: Review the last `SESSION.md` or `git log`.
2. Warm Start: Run a single command to boot the environment (e.g., `make dev`).
3. Micro-Step: Do the smallest "Next" task (≤ 15 mins) immediately. Do not scope, do not plan. Just execute to generate momentum.

---

## 3. Managing the Urge to Restart

### A. Novelty Sprints (The 80/20 Rule)

Don't suppress the urge to innovate; channel it.

- 80%: Continue the main branch.
- 20%: Time-boxed "Spikes" (`spike/wild-idea-date`).
  - Max 60-90 mins.
  - Must end with a decision: Adopt, Park, or Archive.

### B. The "MPD" (Minimal Path to Demo)

Big ideas stall because "done" is vague. Define a Minimal Path to Demo.

- Contract: User can do X, sees Y, we log Z.
- Tasks: 5-9 tasks, each 1-2 hours.
- Rule: If a task is bigger, slice it until it is "sit-down sized."

### C. The Restart Guardrails

If you _must_ restart, you must pass these gates:

1. One-Pager Rule: The new plan must fit on one page (Scope, Sketch, MPD).
2. Reuse-First: You must reuse at least one core component/test from the old version.
3. 48-Hour Cooling Off: Write the idea down, wait 2 days. If it's still better, spike it.

---

## 4. Environment & Dopamine Hacks

- Return Anchor: A physical sticky note on the monitor: "Next Step: Run tests for payment flow."
- Cliffhangers: Stop a session in the middle of an _easy_ task. This makes starting the next day automatic.
- Streak Board: Track "Touches" (15 mins), not just big wins.

---

## 5. The "Continuation Copilot" Prompt

A specific prompt structure to load into an LLM to help regain context.

> Context: "I am a developer with ADHD. I have lost the mental model. Help me reload."
> Output A (Context): 100-word summary, Architecture diagram, Current MPD.
> Output B (Re-entry): Warm start commands, Smallest Next Task (≤ 15 mins).
> Output C (Queue): MPD Tasks, Parked Ideas.
> Output D (Novelty): Optional Spike proposal.

---

## 6. Stall-Break Diagnosis (Mid-Session)

Added 2026-11-09 from the archived `Operating Protocol for High-Friction Engineering Work`. Use it when you stall for more than five minutes of zero progress mid-session. Do not push through. Name the stall in one word, then apply the matching response.

| Diagnosis | Meaning | Response |
| --- | --- | --- |
| Unclear | I don't know what I'm doing | Stop. Write the next 3 actions in plain English in a scratch file, then return. |
| Hard | I know what to do but the step is genuinely difficult | Step the problem down: smallest possible test, draw it on paper, or explain it aloud to someone or an LLM. |
| Boring | I know what and how, but my brain refuses | Engineer novelty: change scenery, change music, narrate aloud, or body-double. |
| Anxious | I'm avoiding it out of fear (breaking something, judgement, failure) | Name the fear in writing. Find the smallest reversible action that tests it. |
| Depleted | Tank's empty | Run the exit ritual, go outside, and come back tomorrow. |

Log each stall with date and diagnosis. After a month the pattern points at structural fixes.

