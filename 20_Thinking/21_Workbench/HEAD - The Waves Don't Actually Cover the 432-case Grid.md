---
aliases: []
created: 2026-06-11T00:00:02+00:00
modified: 2026-07-04T10:52:03+00:00
permalink: llmeon/20-thinking/21-workbench/head-the-waves-dont-actually-cover-the-432-case-grid
tags: [prodos/head, state/thinking]
title: "HEAD - The Waves Don't Actually Cover the 432-case Grid"
---

## 🔴 Blocking Issues (Fix before cIrculating)

### 1. The Waves Don't Actually Cover the 432-case Grid

-1, §12 and FTFL-480 all say the programme runs "the full 432-case grid". §8.2 doesn't deliver that—and can't, by design:

- Variable E (Extract cap) is never the "one thing added" by any wave. Baseline fixes `E=Uncapped`, and no wave switches it. `E=Capped` is never exercised. One of your six variables is dead in the run plan.
- The cumulative wave design (A = baseline + X, B = A + P, …) tests a single path through the grid, not the Cartesian product. e.g. `P=On, X=Off` never runs.
- Some combinations are invalid anyway: `C=5NodeFull` at `L=L1` is nonsensical, so "432" overstates the valid space.

The principle: one-factor-at-a-time is the _right_ design under Position B time pressure—the error is the framing, not the method. Reword everywhere to "a structured subset of the 432-case grid, sequenced one variable at a time", and either add `E=Capped` to a wave or explicitly drop E with a rationale. Ollie will spot this; Weronika will quote "432" in the AS05 report.

### 2. "Max cOncurrency" Success Criteria Vs Sequential-only Workload

- §4.3 Workload Profile: _"Discrete test cases run sequentially within a wave. No concurrent or bursty request modelling."_
- Axis B success criterion: _"document max concurrency before SLA breach."_ §4.1 example: _"five federated nodes break at Z concurrency."_

You cannot measure a concurrency limit with a sequential load generator. Either the harness needs a concurrency dimension (it isn't in the grid), or the Axis B criterion must be rewritten to something measurable—e.g. "federation latency overhead per additional node at sequential load". This directly affects what FTFL-480's harness (NEW4) must support, so it needs resolving before Ollie builds it.

---

## 🟡 Structural Issues (Confusing, not fAtal)

### 3. "Phase" Means Two Different Things

Execution Phases 0–4 collide with the _connectivity_ phases in §6.2, §7.3, D3, and Axis B ("Cross-cloud overhead—Phase 2 only"). A reader will parse "cross-cloud is Phase 2 only" as _the single-node baseline phase_, which is exactly backwards. Rename the connectivity staging—e.g. "intra-region first; cross-cloud as a conditional follow-on stage".

### 4. D1 Vs D-a—is the Topology Decided or Not?

Decision log D1 says "start with single oversized node hosting 5 co-located DBs" (decided 7 May). Open item D-a asks "single oversized node vs 5 separate nodes?" (open). One of these is wrong. Mark D1 as _superseded / under review pending D-a_, or close D-a.

### 5. The Primary SLA Gate is Undefined but Used Everywhere

D-c/D-h correctly notes the internal FITFILE SLA should replace HDRUK's 5-min as primary gate—but it's only P1, while H1 and the Axis B criteria _use_ a 5-min threshold now. You can't gate Phase 2 results against an SLA that doesn't exist. Promote this to P0 blocker alongside B1–B4.

### 6. AS05's ≥500M-row Requirement Has no Explicit Gate

The hard deadline requires ≥2 nodes with ≥500M-row MEASUREMENT tables. Phase 0's manifest captures row counts, but nowhere does the plan say "verify ≥2 datasets meet the 500M bar—stop if not". With 1M–3M Synthea patients you need ~170–500 measurements/patient; that's plausible but not guaranteed. Add it as an explicit Phase 0 check—discovering a shortfall at Phase 4 would be unrecoverable before 31 July.

---

## 🟢 Minor

- Phase 3 arithmetic: waves sum to 5–9 days; the §2 table says 3–7. Pick one.
- H4 contradicts itself: written as a controlled condition ("CPU-throttled to 50%") then disclaimed as observe-only. Reword as an observation protocol, not a hypothesis.
- H1 may be pre-falsified by §8.4: you predict a sequential scan from a missing covering index, but §8.4 mandates the OHDSI index set + Jakub's three indexes _before_ loading. Either H1 tests a deliberately un-indexed node, or the hypothesis needs updating.
- Cost-per-query methodology is required by NEW11 AC but never defined anywhere in the document. Even two sentences (subscription burn ÷ queries per run window?) would do.
- Appendix W9 references "Phase 5 report" (stale numbering)—fine since the appendix is deleted before publication.

---
