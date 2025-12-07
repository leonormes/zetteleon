---
aliases: [Action Dependencies, DAG Model for Actions]
confidence: 0.8
created: 2025-11-01T20:30:10Z
epistemic: principle
last_reviewed: 2025-11-01
modified: 2025-12-07T18:13:32Z
purpose: Explain how individual actions compose into larger workflows using the DAG model.
review_interval: 90
see_also: ["[[Atomic Actions Have Four Core Properties]]", "[[Next Action is the Immediate Physical Step Forward]]"]
source_of_truth: [/Volumes/DAL/Zettelkasten/LLMeon/200_projects/LLMPKM/04 - Atomic Actions and Next Actions.md]
status: seedling
tags: [dependencies, productivity, systems, workflow]
title: Action Sequences Form Directed Acyclic Graphs
type: concept
uid: 2025-11-01T20:30:10Z
updated: 2025-11-01T20:30:10Z
---

**Summary:** Individual atomic actions compose into larger workflows using a Directed Acyclic Graph (DAG) model, where actions have dependencies and can run in sequence or parallel, but never form circular dependencies.

**The DAG Model:**

A Directed Acyclic Graph is a structure where:

- **Directed:** Actions flow in one direction (from prerequisite to dependent)
- **Acyclic:** No action can depend on itself directly or indirectly (no loops)
- **Graph:** Multiple actions can connect in complex patterns

**Core Concepts:**

**1. Action Sequences:**

A series of actions that must be completed in a specific order. Each action depends on the completion of the previous one.

**Example:**

```sh
Action 1: Draft email → 
Action 2: Get feedback from manager → 
Action 3: Revise email → 
Action 4: Send email
```

In a task manager like Todoist, this can be represented as a list of tasks within a Section, where order matters.

**2. Dependencies:**

An action is "blocked" until its prerequisite actions are complete. Only actions without incomplete prerequisites are available to work on.

**Example:**

- Action: "Review mockups with client"
- Dependency: "Create mockups" (must be done first)
- Status: BLOCKED until dependency completes

**3. The "Head" of a Sequence:**

The first uncompleted action in a sequence—the only one currently actionable. This is your "next action" for that sequence.

**Example Sequence:**

1. ✅ Research competitor pricing (DONE)
2. ✅ Draft pricing proposal (DONE)
3. ➡️ **Get manager approval** (HEAD - actionable now)
4. ⏸️ Update pricing on website (BLOCKED)
5. ⏸️ Notify customers of changes (BLOCKED)

Only action is actionable; 4 and 5 are blocked by dependencies.

**4. Concurrency (Parallel Sequences):**

A project can consist of multiple parallel action sequences that don't depend on each other. You can work on the next available action from any parallel sequence.

**Example: Product Launch Project**

**Development Sequence:**

- ➡️ Fix bug 247 (actionable)
- ⏸️ Deploy to staging
- ⏸️ Run QA tests

**Marketing Sequence:**

- ➡️ Draft launch email (actionable)
- ⏸️ Get email approved
- ⏸️ Schedule email send

**Legal Sequence:**

- ➡️ Review terms of service (actionable)
- ⏸️ Get legal sign-off

All three "head" actions (bug fix, draft email, review terms) are simultaneously actionable because they're in parallel sequences.

**Why the DAG Model Matters:**

**For Clarity:**

- Makes dependencies explicit
- Shows what can be worked on now vs. what's blocked
- Prevents working on actions out of order

**For Focus:**

- Only surfaces actionable next actions
- Hides blocked actions to reduce cognitive load
- Makes it clear when multiple options are available

**For Progress:**

- Completing one action automatically reveals the next
- Parallel sequences enable concurrent progress
- No time wasted on blocked work

**For ADHD:**

- **Reduces Overwhelm:** Only see what's actionable now
- **Prevents Context Switching:** Clear sequencing prevents jumping around
- **Provides Choice:** Parallel sequences offer options when one path is blocked
- **Externalizes Planning:** Dependency tracking happens in the system, not your head

**Implementation in Task Managers:**

**Todoist Example:**

- Project: "Product Launch"
- Section 1: "Development"
  - Task: Fix bug 247 (actionable)
  - Task: Deploy to staging (depends on above)
- Section 2: "Marketing"
  - Task: Draft launch email (actionable)
  - Task: Get approval (depends on above)

The sections represent parallel sequences. Within each section, tasks are sequential.

**The Power of Visualization:**

When action sequences are modeled as a DAG, you can visualize:

- What's currently workable (head nodes)
- What's blocked and why (dependency arrows)
- Which sequences are parallel (independent branches)
- Overall project structure and flow

**Avoiding Circular Dependencies:**

The "acyclic" property is critical. Circular dependencies create deadlock:

**Bad (Circular):**

- Action A: "Get client approval" (depends on B)
- Action B: "Update design based on approval" (depends on A)
- Result: Deadlock! Neither can start.

**Good (Acyclic):**

- Action A: "Share design with client"
- Action B: "Get client approval" (depends on A)
- Action C: "Update design based on approval" (depends on B)
- Result: Clear sequence, no deadlock.

**Practical Application:**

When planning a project:

1. List all required actions
2. Identify dependencies between actions
3. Organize into sequences (what must happen in order?)
4. Identify parallel work (what can happen simultaneously?)
5. Focus only on "head" actions (current next steps)
