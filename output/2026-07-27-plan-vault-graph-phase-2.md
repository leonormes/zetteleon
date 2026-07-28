---
title: 'Vault Graph Phase 2 — Ground the Foundations, Close the Loop'
output_type: plan
created: 2026-07-27 00:00:00+00:00
wiki_sources: []
tags:
- output
- knowledge-graph
- typed-edges
- domain/llm
- domain/pkm
permalink: llmeon/output/2026-07-27-plan-vault-graph-phase-2
---

> **Output Contract:** [[Protocol - Typed Answer Contract (TAC) for Vault Agents]]. Confidence stated per section; evidence is a vault path or a command output; `UNSURE` items listed in §Validation.
> **Write scope:** proposal-only. This file plus Todoist tasks are the entire write footprint. No note, edge, `axiom:` flag or SoT was created or edited (AGENTS.md §2.3).
> **Predecessor:** `output/2026-07-27-report-llm-graph-bootstrap.md`. **Driver:** [[Prompt - Vault Graph Programme (Session Driver)]].

## Verdict

**Phase 1 did the work it set out to do. Two of its three headline metrics moved for the wrong reason, and a second automated gate was built during it that is currently red across 587 files.**

The LLM/PKM cluster is genuinely in the justification graph now — that was the point of the programme and it is done. But the C1 gap list did not fall from 23 to 2 because 21 claims got grounded. It fell because 24 claims got declared as axioms, and **30 of the 35 axiom notes carry `non_conformance_reason: Bulk inferred type. Needs review.`** The vault's foundational premises are, for the most part, notes an earlier bulk migration guessed the type of and flagged for review, which nobody reviewed before promoting them to bedrock.

Phase 2 therefore has two jobs, in this order: **make the foundations honest, then make the loop run without you.** Expect the gap count to go *up* in the first half of the phase. That is the phase working, not failing.

---

## State Delta

Measured this session with `python3 10_System/scripts/edge_lint.py --audit` (§9.2 — compiler, not memory).

| Metric | Baseline 2026-07-27 14:00 | Now | Δ | Read |
|---|---|---|---|---|
| Notes scanned | 2,310 | 2,316 | +6 | Growth is stubs and tombstones, not note sprawl. Good. |
| Typed edges / notes carrying them | 288 / 71 | 316 / 93 | +28 / +22 | Edges spread wider than they grew — the wiring is less concentrated. Healthy. |
| Justification edges (`supports`+`depends_on`) | 177 | 192 | **+15** | The only number that represents new grounding. |
| Graph nodes | 158 | 179 | +21 | |
| C1 gaps | 23 | **2** | −21 | **Suspect. See §1 below.** |
| Declared axioms | 11 | **35** | **+24** | **The −21 gaps and the +24 axioms are the same event.** |
| Non-claim bedrock | 23 | 30 | +7 | |
| Contradiction edges | 5 | 5 | **0** | Flat. |
| Live tensions | 1 | 1 | **0** | Flat, despite a completed task naming it. |
| Cycles | 2 | 2 | **0** | Flat, despite a completed task naming it. |
| Lint errors / warnings | 0 / 0 | 0 / 0 | — | Genuinely clean. |
| LLM-domain notes carrying justification edges | 0 | **~16** | +16 | **The programme's actual objective. Achieved.** |

Todoist: **33 of 38 tasks complete.** Two real tasks remain open (both P5 pipeline), plus three reference cards.

Confidence: **high** — every figure above is compiler output or a `grep` count run this session, not a recollection.

---

## Three Things That Are Not What They Look Like

### 1 · The gap list was cleared by declaration, not by grounding

**Evidence:**

```
grep -rh '^axiom:' --include='*.md' 30_Library/ | sort | uniq -c
     8 axiom: "true"
    27 axiom: true
```

35 axiom declarations. Of those:

- **30 carry `non_conformance_reason`** — the frontmatter field an earlier bulk migration wrote to mean *"I guessed this note's type; a human should check."* These notes were never checked. They are now the vault's premises.
- **31 carry a `source`, `source_title` or `source_url` field.** That is the signature of an *empirical* claim — something read somewhere — not a *chosen premise*. `Dopamine Neurons Encode Reward Prediction Error, Not Pleasure` has `source_title: "Neuro-Variable Execution, Spatial Cognition & Knowledge Architecture: An Investigative Report"`. It is a finding from a document. It wants an `evidence` note and a `supports` edge. Marking it `axiom: true` converts a citation gap into permanent silence — the compiler will never ask about it again.
- **8 use `axiom: "true"` — a quoted string.** AGENTS.md §9.3 licenses setting *"the `axiom: true` frontmatter boolean"*. These pass only because `edge_lint._truthy()` is lenient about strings. The contract says boolean; the vault has strings.

**Why this matters more than it sounds.** An axiom is a promise: *"I accept this without vault-internal justification, deliberately."* `--why` traversal stops there and reports the chain as grounded. Thirty undeliberate axioms means thirty places where `--why` returns a confident answer that nobody ever decided. This is the same failure the project's own Baseline card already caught once, on `The Architectural Guardian`: *"The metric moved; the grounding didn't."* It recurred at 24× the scale, and this time it recurred through the sanctioned workflow.

**The honest distinction to apply:**

| If the claim is… | Then it is… | Treatment |
|---|---|---|
| A finding from a paper, book, report or article you read | **Empirical** | Write an `evidence` note citing the source; `supports` edge from evidence → claim. Remove `axiom:`. |
| A position you hold that the vault chooses not to argue for | **Axiom** | Keep `axiom: true` (boolean), and add a one-line prose note saying *why* it is a chosen premise. |
| Neither — you can't tell | **Unreviewed** | Remove `axiom:`. Let it return to the C1 gap list. A visible gap beats an invisible assumption. |

Confidence: **high** on the counts and the contract violation; **medium-high** on the interpretation — it is possible a batch of ADHD-neurology claims was reviewed deliberately and the `non_conformance_reason` field simply never cleared. `log.md` would settle it. Either way the boolean/string split and the `source_title` evidence stand.

### 2 · A second gate was built, and it is red across 587 files

`10_System/scripts/validate_note_frontmatter.py` was written and closed in Phase 1 — correctly, it was a real gap the Frontmatter Contract §9 named. Run it now:

```
python3 10_System/scripts/validate_note_frontmatter.py --folder 30_Library/100_zettelkasten
→ 587 file(s) with errors, 1190 total error(s)
```

Dominant failures: `missing required field: 'conformant'`, and `invalid type 'permanent'` (a legacy type not in the contract's ten-value enum).

**This is not a bug in the validator.** It is the accurate measurement the vault has never had. But a gate that returns 1,190 errors is a gate nobody runs, and an ungated router will emit notes into a folder where nothing conforms — so there is no baseline against which a malformed router output would even stand out. `edge_lint.py` is trustworthy precisely *because* it sits at 0/0. The frontmatter validator has no such standing yet.

**The decision Phase 2 must force:** either the enum absorbs `permanent` and `conformant` becomes optional (the contract bends to the vault), or a bulk migration fixes the 587 (the vault bends to the contract). Doing neither leaves two compilers, one of which is ignored.

Confidence: **high** — this is direct command output.

### 3 · Cycles, tensions and contradictions did not move

`Run the Justification Graph Audit prompt on the 23 non-LLM C1 gaps` (completed 17:39) explicitly scoped *"Also clear the 2 circular-reasoning cycles (both in the Logotherapy/Values cluster) and review the 1 live tension."* Cycles: still 2. Live tension: still 1. Contradiction edges: still 5.

The gap half of that task was executed (via axiom declaration, per §1). The cycle and tension half was not. This is the third instance of the pattern the project has already caught twice — `Write the FOUR structural edges` was reopened for the same reason, and `log.md` 16:02 claimed the whole project complete with 29 tasks open.

**The structural read:** a task whose description contains "also" reliably loses everything after the "also". That is a task-design problem, not a diligence problem, and it is cheap to fix — one verifiable outcome per task. Phase 2 tasks below are written that way deliberately.

The two cycles are both `SoT - Values and Eudaimonia` ↔ `SoT - Logotherapy and the Will to Meaning`. A two-node cycle between two SoTs means each is cited as the other's justification — one of the two edges is doing work the other should do.

Confidence: **high** on the counts; **medium** on the cycle diagnosis (I read the audit output, not the notes).

---

## What Phase 1 Did Achieve

Stated plainly, because the critique above is not the whole picture:

- **The programme's stated objective is met.** Zero LLM-domain nodes → ~16 notes carrying justification edges, including `SoT - Flow Engineering`, `SoT - Context Engineering`, `SoT - Agentic Roles`, `SoT - The Context Engine`, `MVC Enforcement Structural Gates for LLM Agents`, `Context Volume Plateau`, `MCP Token Noise`.
- **Every SoT-level duplicate merged.** `SoT - Complexity Conservation` gone; `SoT - Conservation of Complexity` survives. Same for the Jevons, iteration-ceiling, oversight-shift and LLM-corollary pairs — verified by directory listing this session.
- **20 notes now carry `## Tensions` sections**, capturing assumption differences in prose rather than forcing bad edges. That is the report's hardest recommendation and it was followed.
- **`Prompt - Vault Ingest Router` exists and is registered** in `00 - Prompt Library Router` line 36 as the front door.
- **The linter stayed at 0/0 throughout.** 28 new edges, zero regressions. The §9.4 gate held.
- **The governance conflicts got resolved rather than worked around** — §2.4/§6 stub immutability, the HEAD-note link rule, the `10_System` edge-emission gap. Those were the tasks it would have been easiest to skip.

Four of the five target-state criteria in the Session Driver are met. The fifth — *"the C1 gap list is empty or every remaining entry is a deliberate `axiom: true`"* — is met on the letter and failed on the word **deliberate**.

---

## Phase 2 — Definition of Done

The programme ends when content flows in without ceremony and the graph it lands in can be trusted. Concretely, all six:

1. **Every `axiom: true` is deliberate.** No `non_conformance_reason` on any axiom note. Every axiom is either a stated chosen premise or has been demoted and either grounded by an `evidence` note or returned to the C1 list. Value is the boolean, not the string.
2. **`validate_note_frontmatter.py` has a defensible baseline** — either 0 errors, or a documented, counted allowlist of legacy notes with a decision recorded in the Frontmatter Contract. Not 1,190 silent errors.
3. **`edge_lint.py --route "<proposition>"` exists** and returns nearest claims + their grounding status. The routing decision is structurally checkable, not a request for the model to be careful.
4. **Zero cycles. The live tension is adjudicated or recorded as deliberate.**
5. **The loop has run unattended for five consecutive days** and produced at least one stub or edge you kept. Not "the loop is built" — the loop has *run*.
6. **`--why` on any LLM-cluster SoT bottoms out on something you'd defend out loud.**

Criterion 5 is the one that matters. [[LLMeon Vault Pattern Report]] counted four complete systems built and abandoned in this vault. The disease is not incomplete systems; it is completed systems that never got used. **A Phase 2 that ends with a perfect router and no run history has failed**, however clean the audit is.

---

## Task Breakdown

Two sections, sequenced. **P6 before P7** — a router that files new content into a graph resting on 30 unreviewed axioms will faithfully propagate the problem, and `--route` has to report each candidate's grounding status, which is meaningless until the axioms mean something.

### Section P6 — Foundations Audit

| # | Pri | Task | Est | Verifiable outcome |
|---|---|---|---|---|
| 1 | p1 | Triage the 30 axioms carrying `non_conformance_reason` | 2h | Every axiom note is empirical / chosen / unreviewed. Decision brief only — no writes. |
| 2 | p1 | Demote the empirical axioms and write their `evidence` notes | 2h | `axiom:` removed; `evidence` note + `supports` edge per demoted claim. Gap count rises; that is correct. |
| 3 | p2 | Normalise the 8 `axiom: "true"` strings to booleans | 20m | `grep '^axiom:' 30_Library/` returns only `axiom: true`. |
| 4 | p1 | Decide the frontmatter validator's baseline | 45m | A recorded decision in the Frontmatter Contract: absorb `permanent`/`conformant`, or migrate. Nothing else. |
| 5 | p2 | Execute that decision | 2h | Validator reports 0 errors or a counted, documented allowlist. |
| 6 | p2 | Break the Values/Logotherapy cycle | 30m | `--audit` reports 0 cycles. |
| 7 | p3 | Adjudicate the `ADHD Systems Fail When They Become Monotonous` tension | 30m | Either the contradiction edge is justified in prose, or it is dropped. |

### Section P7 — Loop Closure

| # | Pri | Task | Est | Verifiable outcome |
|---|---|---|---|---|
| 8 | p1 | `edge_lint.py --route "<proposition>"` *(carried from P5)* | 3h | Command returns nearest claims, each tagged grounded / axiom / C1 gap, plus what would become dangling or newly-supported. |
| 9 | p2 | Wire `--route` into the Ingest Router's Gate 1 | 45m | Gate 1 calls the script. Lexical fallback becomes the deterministic path, not the degraded one. |
| 10 | p1 | Wire the router into daily capture *(carried from P5)* | 2h | A cron/scheduled job processes `00_Inbox/` in small batches, propose-only, `UNSURE` by default. |
| 11 | p1 | **Run the loop for five days and keep a run log** | 5×10m | Five dated entries in `log.md`. At least one kept stub or edge. |
| 12 | p2 | Post-run review: what did the router get wrong? | 1h | A list of misroutes, each traced to a gate. Fix the gate, not the instance. |
| 13 | p3 | Re-baseline: `--audit` + validator + the six criteria | 30m | Updated Baseline card in Todoist. Programme closed or Phase 3 scoped. |

**Task-design rule applied throughout, in response to §3:** one verifiable outcome per task, and no task description contains the word "also". Anything that would have been an "also" is its own row.

---

## Sequencing Rationale, and the Case Against It

**The case for P6 first:** `--route` must report each candidate's grounding status. If 30 of those statuses are "grounded" because of an unreviewed bulk-migration flag, the router will confidently file new evidence *away from* the claims that most need it — the claims it thinks are already settled. Building the loop first means building it against a distorted signal and then rebuilding it.

**The strongest case against, which you should weigh:** P6 is seven tasks of graph hygiene with no user-visible output, in a vault whose documented failure mode is *"20+ bespoke AI prompts exist to fix the vault rather than notes that use it."* An entire phase of vault-fixing before anything runs is precisely the shape of the four abandoned systems. There is a real argument for doing tasks 8, 10 and 11 first, getting the loop running against an imperfect graph, and folding P6 in as the loop surfaces which axioms actually block routing decisions.

**Where I land:** P6 tasks 1–3 first (the axiom triage — about half a day, and it is the thing that makes `--route` meaningful), then jump to P7 tasks 8, 10, 11 to get the loop running, then return for P6 4–7 while the loop accumulates run history. That gets something running by mid-phase without building the router on a distorted graph.

**What would change my view:** if task 1's triage finds the 30 axioms were in fact deliberately reviewed and the `non_conformance_reason` field simply never got cleared, then §1 collapses to an 8-string cleanup and P6 shrinks to tasks 3–7. Check `log.md` around the 17:39 entry before starting task 1 — it is a ten-minute check that could remove four hours of work.

---

## Risks

| Risk | Mitigation |
|---|---|
| **The gap count rising feels like regression and stalls the phase.** It is the honest number. | Record the pre-demotion count in the Baseline card *before* starting task 2, so the rise is expected rather than discovered. |
| **1,190 validator errors are demoralising enough to make the gate get ignored permanently.** | Task 4 forces the decision before task 5 does any work. The contract bending is a legitimate outcome — it is not surrender. |
| **The loop gets built and never runs** — the documented failure mode of this vault. | Task 11 is the only task in Phase 2 that cannot be satisfied by building something. Its outcome is five dated `log.md` entries. Treat it as the phase's actual deliverable. |
| **`--route` becomes a two-week project.** It needs to return nearest-claims-plus-status, nothing more. | Timebox to 3h. If it overruns, ship the lexical version and note the limitation. A crude deterministic index beats an elegant unbuilt one. |
| **Phase 2 drifts into redesigning the taxonomy.** | The Session Driver already names this. If a session proposes a new note type or a new edge type, that is the drift — say so out loud and return to the task. |

---

## Validation

- **`edge_lint.py --audit`: run this session, clean.** 2,316 notes · 316 edges in 93 notes · 0 errors, 0 warnings. Argument audit: 192 justification + 5 contradiction edges among 179 nodes; 2 gaps, 35 axioms, 30 bedrock, 1 live tension, 2 cycles.
- **`validate_note_frontmatter.py --folder 30_Library/100_zettelkasten`: run this session.** 587 files with errors, 1,190 total errors.
- **Axiom counts:** `grep -rh '^axiom:' --include='*.md' 30_Library/` → 27 `true`, 8 `"true"`. Cross-reference for `non_conformance_reason` → 30 of 35. Cross-reference for `source`/`source_title`/`source_url` → 31 of 35.
- **Merge verification:** directory listing of `30_Library/SoT/` and `30_Library/100_zettelkasten/` confirms `SoT - Complexity Conservation`, `Shift to High-Level Oversight`, `Software Jevons Paradox`, `Optimal Iteration Count` and `LLM Reasoning Efficiency is Proportional to Structural Constraint` are absent. `Research-Plan-Implement Workflow.md` **still exists** — the completed task said "merge *or subordinate*", so this may be correct. **UNSURE — not opened this session.**
- **Tooling tier reached: 3 (filesystem).** `obsidian-mcp-tools` via 1MCP not reachable from this sandbox (network-isolated; `127.0.0.1:3050` is on the host, not here); `obsidian` CLI not present. Every claim above is a command output or a directory listing — none rests on semantic search — so this tier limitation does not weaken the findings, but it does mean **no semantic check for missed notes was possible.**
- **`UNSURE` items:** whether the 30 `non_conformance_reason` axioms were deliberately reviewed (check `log.md`); whether `Research-Plan-Implement Workflow` was subordinated correctly; the specific edge in the Values/Logotherapy cycle that should be dropped.
- **Write footprint:** this file, and Todoist tasks. Nothing in `30_Library/`, `raw/`, `wiki/`, `10_System/`. No edge, no `axiom:` flag, no note.

**Overall confidence: high** on the state delta and the three critiques (all mechanically verified this session); **medium-high** on the axiom interpretation, pending the `log.md` check; **medium** on the sequencing recommendation, which is a judgement call with a real counter-argument stated above.

---

## Next Physical Action

Run this, and read what the 17:39 entry says about how the 21 gaps were closed:

```
grep -n -A20 '17:3' log.md | head -60
```

If it records a deliberate review of each claim, Phase 2 shrinks by four hours. If it records a bulk pass, start P6 task 1.
