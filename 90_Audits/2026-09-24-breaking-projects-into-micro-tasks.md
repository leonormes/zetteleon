---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-breaking-projects-into-micro-tasks
title: 2026-09-24-breaking-projects-into-micro-tasks
type: note
---

## Positioning — [[Breaking Projects Into Micro-Tasks Reduces ADHD Overwhelm]] — 2026-09-24

### Prompt routing

Read [[00 - Prompt Library Router]]. The note is a single note with **no outbound links and two inbound** (a MoC and one claim), so it is thin and nearly orphaned. The router row for "one bare or orphan note with few or no links, to be positioned and then stress-tested" points to [[Orphan Note Positioning & Thread Audit]] (v3, one unattended run). [[Note Refresh & Link Auditor]] is for a note that already has real connections, which this did not. Run accordingly, with lexical search because 1MCP tools were unavailable.

### Baseline

- **Inbound (2):** [[MOC - ADHD Project Continuation Challenge]] §B and [[Dopamine-Aware Planning Aligns Tasks with the Brain's Reward System]].
- **Outbound:** none. **Type:** `strategy` (not canonical). **Frontmatter:** missing all claim fields. **Not a graph node.**

### Candidate connections (tests applied)

| Candidate | Use / Mention | Verdict |
|---|---|---|
| [[Micro-Stepping Reduces Cognitive Load for Task Initiation]] | Heavy overlap. Same decomposition, but aimed at activation cost, not project overwhelm. | Plain link; flagged as a merge option. Its alias is "Task Chunking", the same as this note's |
| [[Momentum-Based Re-Entry Points Ease Project Resumption]], [[A Project Playlist is a Sequence of Small Tasks to Rebuild Momentum]], [[Leaving a Task Intentionally Unfinished Creates a Clear Starting Point]], [[The Hemingway Technique - End Work With Unfinished Problems]] | The re-entry cluster; each develops one half of this claim | Plain links |
| [[The Three Rules of Starter Tasks]], [[Next Action is the Immediate Physical Step Forward]] | Size and definition of the micro-task | Plain links |
| [[ADHD Causes Deficits in Completing Long-Term Projects]] | The problem this answers | Plain link. A `depends_on` was rejected: that claim has no grounds and is not a graph node, so it would create an ungrounded foundation |
| [[ADHD Task Initiation Difficulty is a Neurological Issue Not Laziness]] | Would be a premise | Rejected as an edge: the strategy works whatever the cause, so it fails the denial test |
| [[SoT - Execution Protocol (GTD & PARA)]] | Requires every project to have an atomic next action | `implements` (structural) |
| [[ADHD Brain Wiring vs. Classic Productivity Systems]], [[Deep Dive Sessions for ADHD (Adapted GTD Next Actions)]] | Say granular action lists can cost motivation | **Tensions**, not `contradicts`: both can hold if the micro-task keeps its context |

### Patch A — typed edges

- `[implements:: [[SoT - Execution Protocol (GTD & PARA)]], confidence=medium]` on the note.
- `[supports:: [[Breaking Projects Into Micro-Tasks Reduces ADHD Overwhelm]], confidence=medium]` on the new Evidence note (below).

### Patch B/C/D — applied

| File | Change |
|---|---|
| The note | `type` `strategy` → `claim`; `proposition`, `epistemic_status: medium`, `evidence_links`, empty `contradicts`, `conformant: true`; `## Tensions` (2), `## Related` (12), `### Where It Applies in ProdOS` (4), `### Further Reading (Personal Library)` (4) |
| **New:** [[Evidence - Bandura and Schunk Chunked Maths Goals Raised Childrens Progress and Interest]] | Verbatim quote from *Think Small* (Calibre 56): the chunking group "progressed much more rapidly" and "became more interested in maths". Confidence 0.5 |
| Micro-Stepping note | reciprocal bullet |
| Protocol - Vague-to-Action | bullet in Related |

**Library hits kept** (passages read in full): *Think Small* (the chunking study), *Atomic Habits* (Two-Minute Rule), *Eat That Frog!* (momentum principle), Barkley's *Taking Charge of Adult ADHD* (ADHD as organising behaviour over time). Discarded: the software-engineering books (User Story Mapping, EventStorming, Code Complete and similar), which matched on "break down" and "project" only.

### Scope stated honestly

The Evidence note is about **children learning maths**, from a secondary account, and supports the decomposition mechanism, not the ADHD-specific claims about overwhelm, re-entry or dopamine. The claim stays `medium`.

### Claim stubs written

None.

---

## Part 3 — Thread audit

- **Verdict:** the note is now a **grounded claim node**. `--why`: supported by the Bandura and Schunk Evidence note. `--impact`: nothing rests on it, so exposure is 0. It does not appear in the audit's gap list.
- **Traversal:** out to the Execution Protocol SoT (structural); in from the Evidence note (`supports`), the MoC and Dopamine-Aware Planning (plain).
- **Pathologies:** (1) an overlap with [[Micro-Stepping Reduces Cognitive Load for Task Initiation]], which has the same alias; (2) both tension partners are untested or speculative, so the tension cannot yet be resolved; (3) the evidence is general, not ADHD-specific.

### Next action

Decide whether to merge [[Micro-Stepping Reduces Cognitive Load for Task Initiation]] into this note (or the reverse): one shared `Task Chunking` alias currently points at two notes.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2860 notes, 1385 edges). Resolver: 0 unresolved links in the note and the new Evidence note. Confidence: **medium**.
