---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-deep-dive-sessions
title: 2026-09-24-deep-dive-sessions
type: note
---

## Value check and ProdOS linking — [[Deep Dive Sessions for ADHD (Adapted GTD Next Actions)]] — 2026-09-24

> Method note: 1MCP tools were unavailable, so checks were lexical (`rg`) plus file reads and `edge_lint.py`. At 285 words the note is already one idea, so there was nothing to atomise; this is the value-check and linking routine.

### Verdict: keep as a candidate experiment, but it has never been run

- **What it is:** a one-week experiment (hide the Todoist Next Actions list; two 75-minute project blocks a day; success is 8 of 10 blocks completed). It sits in the vault's experiment lifecycle in [[MOC - ADHD Experiments & Protocols]].
- **Never run:** created 2025-06, last reviewed 2025-12-16, and the Results Log is still the placeholder. It has not been tested.
- **Relevant to ProdOS:** it is a live challenge to the system's unit of work. The 2026-08-29 fitness audit lists "75-minute Deep Dive block" as one of four incompatible definitions of an atomic action (alongside the sub-120-second MVA, 5 to 15 minute starter tasks and the 15 minute Chief of Staff starter task).

### Finding: two `contradicts` edges were mis-typed

The 2026-07-30 run wrote these two edges on the note; both appeared in the compiler's conflict list.

| Edge | Test result |
|---|---|
| vs [[Replace Deep Focus Marathons With Repeatable Micro-Pipelines]] (25 to 50 minute sprints) | Conflicting *prescriptions*, but both can hold if people differ in how well they sustain flow. An untested hypothesis cannot logically negate a claim. |
| vs [[A Next Action Must Be the Absolute Next Physical Visible Activity Required to Move a Situation Forward]] | The experiment suspends next actions for a week; it does not deny the definition of one. |

Under the contradiction-versus-tension test in [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]], both are tensions. I removed the two edges and wrote them as a `## Tensions` section with the reasoning. The compiler's contradiction count fell from 38 to 36. This reverses an earlier decision.

### Changes

| File | Change |
|---|---|
| The note | two `contradicts` edges replaced by a `## Tensions` section; 6 new annotated Related links (Flow State, Newport Deep Work, Five-Item To-Do List, Three Rules of Starter Tasks, Execution Protocol SoT, Action-First GTD) |
| Cal Newport Deep Work note | Related bullet pointing here |

### Vault-wide findings, not changed

1. **The experiment dashboards are empty.** [[MOC - ADHD Experiments & Protocols]] lists experiments with Dataview on `status` of `active`, `pending`, `validated` or `rejected`. All 11 hypothesis-type notes carry `status: draft` (10) or none (this one), so none appear in any list. The MoC's statuses are also not in the frontmatter contract's `status` enum (`draft`, `seed`, `stable`, `evergreen`, `stale`, `superseded`). One of them has to give.
2. **`type: hypothesis` is not in the contract's type enum.** It is a deliberate species (11 notes, one hub), so this note stays `conformant: false` with that reason. Adding `hypothesis` to the enum would be a contract decision for you.
3. **The dashboards also read a `purpose` field** that none of the notes have.

### Left alone

- **Status:** I did not set `status`, because choosing between `pending` and `active` means deciding whether you are running the experiment.
- **Broken links elsewhere:** [[Replace Deep Focus Marathons With Repeatable Micro-Pipelines]] links to `Timeboxing for ADHD Management`, `Exit Ritual For ADHD Time Boxes` and `ADHD Behavioral Strategies for Productivity`, which I could not find as notes.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2855 notes, 1382 edges).
