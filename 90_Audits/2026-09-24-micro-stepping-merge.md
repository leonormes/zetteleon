---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-micro-stepping-merge
title: 2026-09-24-micro-stepping-merge
type: note
---

## Merge — three micro-step notes into one parent claim — 2026-09-24

Leon approved the merge proposed in [[2026-09-24-micro-stepping]]. Method: [[sys_merger]] logic (fixed sources, no discovery), applied by hand because the notes carry typed edges. 1MCP tools were unavailable.

### Result

| Role | Note |
|---|---|
| **Survivor (parent claim)** | [[Micro-Stepping Reduces Cognitive Load for Task Initiation]], chosen because it had the most inbound links (13 files) and the typed edges from the task-initiation MoC and [[SoT - ADHD Management Protocols]] |
| Absorbed | `Master Micro-Actions & Starter Tasks` (an axiom claim that was really an untested experiment) |
| Absorbed | `Breaking Projects Into Micro-Tasks Reduces ADHD Overwhelm` |

### How the content was combined

| Section of the parent | Came from |
|---|---|
| Opening definition and Psychological Basis | the parent, unchanged |
| The Rule of the First Step | Master Micro-Actions (under two minutes, purely physical, below the Wall of Awful) |
| At Project Level | Breaking Projects (Details paragraph, verbatim) |
| Evidence | the Bandura and Schunk Evidence note, with its scope caveat |
| Test Protocol (Untested) | Master Micro-Actions (three-day protocol and expected outcome, Results Log still empty) |
| Tensions, Related, Where It Applies in ProdOS, Further Reading | union of both notes' sections, deduplicated (19 Related, 5 ProdOS, 4 books) |

**Frontmatter:** `proposition` widened to cover both scopes; `evidence_links` points at the Bandura and Schunk note; no `axiom`; `epistemic_status: medium`; aliases now include every absorbed title and alias (`Micro-Actions`, `Starter Tasks`, `Micro-Tasks for ADHD`, `Task Chunking Strategy`, and both old titles), so existing links keep resolving.

### Typed edges

- `[implements:: [[SoT - Execution Protocol (GTD & PARA)]], confidence=medium]` came from Breaking Projects.
- `[supports:: [[SoT - ADHD Management Protocols]]]` came from Master Micro-Actions.
- The `supports` edge Master Micro-Actions had pointed at the parent is gone (it merged into it).
- The Evidence note's `supports` edge and `supports_claims` were retargeted to the parent.
- [[Practice - Micro-tasking and time-boxing]] `implements` was retargeted from Master Micro-Actions to the parent.

### Links repointed (6 files)

Retargeted to the parent, with the old title kept as the display text: [[Dopamine-Aware Planning Aligns Tasks with the Brain's Reward System]], [[SoT - Principles for Peaceful Productivity]], [[Protocol - Vague-to-Action]], [[MOC - ADHD Project Continuation Challenge]]. Typed and frontmatter references (the Evidence note, Practice - Micro-tasking) were retargeted without display text. No `[[Master Micro-Actions & Starter Tasks]]` or `[[Breaking Projects Into Micro-Tasks Reduces ADHD Overwhelm]]` link remains in `30_Library` or `10_System`. Older audit files still use the old titles; they resolve through the aliases.

### Graph effect

| Metric | Before | After |
|---|---|---|
| Axioms | 139 | 138 (the Master Micro-Actions axiom is gone) |
| Foundation gaps | 39 | 39 |
| Cycles | 34 | 34 |
| Contradictions | 36 | 36 |

The parent is now grounded by evidence (a general chunking study) instead of resting on an unevidenced axiom.

**Watch-out:** the parent `supports` [[SoT - ADHD Management Protocols]], which has a large downstream tree, so that tree now rests on one general study of children's maths chunking plus three books. The old arrangement rested it on an axiom. Better evidence for the ADHD-specific mechanism would make this sturdier.

### Not changed

- The Master Micro-Actions experiment was never run (Results Log empty); its claim had been marked `high` and `axiom: true` without evidence. That is why it was folded in as an untested protocol, not kept as an axiom.
- [[The Three Rules of Starter Tasks]] and [[The 5-Minute Action Overcomes Initiation Barriers]] overlap with the parent but are distinct rules; they remain separate notes, linked.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2860 notes, 1384 edges). Resolver: 0 unresolved links in the parent.

### Originals (for recovery)

Both absorbed notes were deleted. Their full text follows; the parent's pre-merge text is in git history and the vault backup commits.

#### Master Micro-Actions & Starter Tasks

````markdown
---
aliases: [Micro-Actions, Starter Tasks]
axiom: true
conformant: true
contradicts: []
created: 2025-12-16T13:15:00+00:00
epistemic_status: high
evidence_links: []
modified: 2026-09-24T09:20:40+00:00
permalink: llmeon/30-library/100-zettelkasten/master-micro-actions-starter-tasks
prodos.kind: atomic
prodos.lifecycle: stable
proposition: Breaking a daunting task down until the first step is absurdly small (< 2 minutes, purely physical) lowers the activation energy below the threshold of the Wall of Awful, triggering immediate task initiation.
tags: [experiment, focus, momentum, TheHuman/Health/ADHD, topic/productivity]
title: Master Micro-Actions & Starter Tasks
type: claim
---

## 1. The Hypothesis

> If I break a daunting task down until the first step is absurdly small (< 2 minutes, purely physical),
> Then I will initiate the task immediately,
> Because this lowers the activation energy below the threshold of the [[SoT - ADHD Neurology & Core Concepts|The Wall of Awful]].

---

## 2. Experiment Protocol

- Duration: 3 Days.
- Trigger: Procrastination on a "Big Task" (e.g., "Write Report").
- Action:

    1. Refuse to do the task.
    2. Define a "Micro-Action" that is purely physical and takes < 2 minutes (e.g., "Open document and type title," "Put on running shoes").
    3. Commit ONLY to that micro-action.
    4. After the micro-action, I have permission to stop.

---

## 3. Expected Outcome

- Metric: 80% conversion rate from Micro-Action to Continued Work (Newton's Law of Inertia).
- Qualitative: "Starting felt easy."

---

## 4. Results Log

- _(Log results here)_

[supports:: [[SoT - ADHD Management Protocols]]]

[supports:: [[Micro-Stepping Reduces Cognitive Load for Task Initiation]]]

## Related

- [[SoT - ADHD Management Protocols]]
- [[SoT - ADHD Neurology & Core Concepts]]
````

#### Breaking Projects Into Micro-Tasks Reduces ADHD Overwhelm

````markdown
---
aliases: [Micro-Tasks for ADHD, Task Chunking Strategy]
conformant: true
contradicts: []
created: 2025-10-30T15:00:39+00:00
epistemic_status: medium
evidence_links: ["[[Evidence - Bandura and Schunk Chunked Maths Goals Raised Childrens Progress and Interest]]"]
last_reviewed: '2025-10-30'
modified: 2026-09-24T00:00:00+00:00
non_conformance_reason: ""
permalink: llmeon/30-library/100-zettelkasten/breaking-projects-into-micro-tasks-reduces-adhd-overwhelm
proposition: Breaking a large project into specific micro-tasks with clear milestones reduces overwhelm for people with ADHD, because the next concrete action becomes visible and each completed step gives momentum and a re-entry point.
status: seed
tags: [overwhelm, project-management, task-management, TheHuman/Health/ADHD]
title: Breaking Projects Into Micro-Tasks Reduces ADHD Overwhelm
type: claim
updated: null
---

## Breaking Projects Into Micro-Tasks Reduces ADHD Overwhelm

Summary: Decomposing large, complex projects into specific, actionable micro-tasks with clear milestones makes work more manageable for ADHD individuals and reduces initiation barriers.

Details: Large projects overwhelm the ADHD brain because their scope obscures the next concrete action. By creating lists of specific, achievable steps with defined milestones, the pathway forward becomes visible. This approach enables picking up where you left off more easily, as each micro-task represents a clear re-entry point. Focusing on completing one small task at a time generates momentum and provides frequent dopamine rewards, sustaining engagement across work sessions.

> Status gates
>
> - seedling → growing: has summary + details + at least 1 inbound link.
> - growing → evergreen: has 2+ inbound links from structural notes, purpose set, confidence justified, 1–3 `see_also`.

[implements:: [[SoT - Execution Protocol (GTD & PARA)]], confidence=medium]

## Tensions

- [[ADHD Brain Wiring vs. Classic Productivity Systems]]—_argues that a long pre-defined list of granular actions can extinguish motivation by stripping out context and momentum. Both can hold: this claim is about specific steps that keep their milestone and context, that one is about a decontextualised list. The gap is whether a micro-task keeps its "why"._
- [[Deep Dive Sessions for ADHD (Adapted GTD Next Actions)]]—_an untested experiment that hides the granular next-actions list for project blocks. A direct test of how far this strategy should go._

## Related

- [[Micro-Stepping Reduces Cognitive Load for Task Initiation]]—_Overlaps heavily. That note is about the activation cost of starting; this one is about project-level overwhelm, a visible path and re-entry. Kept separate because the mechanisms differ; a candidate to merge under one parent if you prefer._
- [[Momentum-Based Re-Entry Points Ease Project Resumption]]—_The re-entry half of this claim, developed on its own._
- [[A Project Playlist is a Sequence of Small Tasks to Rebuild Momentum]]—_A curated short list of shallow wins built from the same decomposition._
- [[Leaving a Task Intentionally Unfinished Creates a Clear Starting Point]]—_Where the next micro-task comes from at the end of a session._
- [[The Hemingway Technique - End Work With Unfinished Problems]]—_The same idea: stop mid-task so the restart point is obvious._
- [[The Three Rules of Starter Tasks]]—_Sizes the micro-task: 5 to 15 minutes, simple, physical, and only meant to build momentum._
- [[Next Action is the Immediate Physical Step Forward]]—_The GTD definition of what each micro-task should be._
- [[ADHD Causes Deficits in Completing Long-Term Projects]]—_The problem this strategy answers: long projects lose momentum partway through._
- [[Limbic Friction is the Activation Energy for Habits]]—_The general term for the barrier a small first step lowers._
- [[Celebrate Small Successes to Build Routine Momentum]]—_The reward side of finishing small tasks._
- [[Dopamine-Aware Planning Aligns Tasks with the Brain's Reward System]]—_The planning approach that relies on the frequent small wins these tasks provide._
- [[MOC - ADHD Project Continuation Challenge]]—_The hub, section B (low-friction re-entry), where this note already sits._

### Where It Applies in ProdOS

- [[Protocol - Vague-to-Action]]—_The operational version: define the endpoint, brain-dump the steps, then pick the single physical first action._
- [[SoT - Execution Protocol (GTD & PARA)]]—_Requires every GTD Project to have at least one atomic next action, which is this strategy applied to a whole project._
- [[Protocol - Weekly Command Centre]]—_Move 3 writes one physical-verb starter per live commitment, so no project sits without its next micro-task._
- [[Protocol - Autonomous Action System]]—_Its Refine phase splits a dump into projects and next actions, which automates the decomposition._

### Further Reading (Personal Library)

- [Think Small — Owain Service](calibre://view-book/GCcalibreBooks/56/EPUB)—_Chunking a goal into smaller parts made children progress faster and become more interested (the Bandura and Schunk study; see the Evidence note above)._
- [Atomic Habits — James Clear, The Two-Minute Rule](calibre://view-book/GCcalibreBooks/690/EPUB)—_Scale any task down until it takes under two minutes to start, for example "fold one pair of socks"._
- [Eat That Frog! — Brian Tracy, Build Up a Sense of Momentum](calibre://view-book/GCcalibreBooks/1591/EPUB)—_It takes far more energy to get started than to keep going, which is why an easy first step matters._
- [Taking Charge of Adult ADHD — Russell A. Barkley](calibre://view-book/GCcalibreBooks/1593/EPUB)—_Frames ADHD as a problem of organising behaviour over time (time blindness), not of knowledge, which is why visible near-term steps help._
````
