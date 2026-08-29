---
created: 2026-06-20T10:01:33+00:00
modified: 2026-08-29T09:36:13+00:00
permalink: llmeon/30-library/200-projects/fitfile-value-stream-report-2026-06-20
project_name: Pipeline
tags: []
title: FITFILE Value Stream Report - 2026-06-20
---

## FITFILE Value Stream Report

Scope: Jira project FTFL · GitLab repos `deployment` (37240723) and `InsightFILE` (22023844) · Window: last 6 sprints / 6 weeks (2026‑05‑09 → 2026‑06‑20) · Deploy signal: git tags · Calendar days throughout.

### 1. Executive Summary

- Engineering moves fast once started, but finished work doesn't ship. MRs merge in minutes-to-hours on both repos, yet 12 tickets are stuck in "Ready for Release"/"Ready for test" for 2–7 sprints. The chokepoint is downstream of coding, not coding itself.
- There is effectively no human code review on either repository. 0 of 88 MRs merged in the last 6 weeks (59 on `deployment`, 29 on `InsightFILE`) carry a single human review comment. Quality control is 100% dependent on CI—and on the main app repo, CI only passes 52% of the time.
- Sprint overcommitment is accelerating. Committed story points rose from 58 to 157 over the last four sprints while completion-by-close-date fell from ~91% to ~12%.
- A majority of "completed" work in-window was actually abandoned. In a 20-ticket sample of resolved tickets, roughly 60% closed as `Abandoned`, not delivered—current throughput/velocity numbers likely overstate real output.
- The backlog is large and ungroomed: 196 open items, 90% with no assignee, 83% with no size estimate, 126 sitting untouched 2+ weeks (some 200+ days)—this looks like a triage gap, not a capacity gap.
- WIP is concentrated and stale: one engineer is carrying 8 concurrent in-progress items against an informal limit of 3; two tickets have shown zero movement for 150 days.
- Top recommendation: fix `InsightFILE`'s broken release path (no real version tagging + 52% CI pass rate) first—it's the single chokepoint behind the largest pile of finished-but-unshipped work—then add a minimal human review step, since CI alone is not currently a reliable gate.

### 2. Value Stream Map

| Stage | Current volume | Cycle time | Wait time | Note |
|---|---|---|---|---|
| 1. Demand & Discovery | 196 backlog items | n/a | 126 items >14d unsprinted; oldest 228d | 90% no assignee, 83% no estimate |
| 2. Planning & Commitment | 29 items / 151 pts in active sprint | n/a | 19 items rolled over 2–7 sprints | Velocity 12–91% over last 6 sprints (declining) |
| 3. Development (WIP) | 36 issues in progress | avg 30.9d in status, max 150d |—| Yasir 8 WIP vs. limit 3 |
| 4. Review & Quality Gates | 88 MRs merged in-window | merge: 0.1h (deployment) / 0.42d (InsightFILE) | open MRs avg 60–100d+ | 0/88 human-reviewed; CI pass 72.7% / 52.0% |
| 5. Released & Deployed | 12 tags (deployment), 1 floating tag (InsightFILE) |—|—| ~2 deploys/week on deployment; InsightFILE frequency uncomputable |
| 6. Flow Efficiency | 20-ticket sample | avg total 52.6d | avg wait dominates (Backlog = 73% of cumulative wait) | Flow efficiency 25.1% (41.8% excl. abandons); target 40% |

### 3. Stage-by-Stage Findings

#### Stage 1—Demand & Discovery

Backlog: 196 items (statusCategory = To Do)

- By type: Task 77, Sub-task 66, Story 25, Bug 19, Epic 7, Spike 2
- By priority: Medium 163, High 18, Highest 8, Low 6, Lowest 1
- By component: unscored—the component field is unused on all 196 items; this slice can't be produced (data quality gap, see §5)

Planning debt:

| Gap | Count | % |
|---|---|---|
| No story-point estimate | 162 | 83% |
| No assignee | 176 | 90% |
| No priority | 0 | 0% |

Stale & unsprinted (>14d, never sprinted): 126 items. Oldest cluster is a coherent abandoned feature set—FTFL-286/287/289/290/291/292/293 ("Delete Data Source" / data-deletion flow), all 184–228 days old, never touched. Other long-stale items: FTFL-159 (149d, liveness probes), FTFL-173/175 (148d, OMOP vocab sync), FTFL-184 (147d), FTFL-190 (143d), FTFL-199/206 (141d).

Epics: 29 total, only 2 with zero child stories—FTFL-644 ("Node Implementation (NUH)") and FTFL-662 ("Report on unmapped source values"). Epic breakdown discipline is otherwise healthy.

Incident issue type: does not exist in this project—no native signal for Change Failure Rate (see §5).

#### Stage 2—Planning & Commitment

Sprint velocity, last 6 closed sprints (board 281, weekly cadence):

| Sprint | Closed | Committed (issues/pts) | Done-as-of-today (issues/pts) | % pts done |
|---|---|---|---|---|
| 17 | 05-13 | 57 / 172 | 54 / 156 | 90.7% |
| 18 | 05-20 | 36 / 108 | 32 / 87 | 80.6% |
| 19 | 05-27 | 17 / 58 | 10 / 21 | 36.2% |
| 20 | 06-03 | 21 / 89 | 8 / 19 | 21.3% |
| 21 | 06-10 | 22 / 118 | 6 / 22 | 18.6% |
| 22 | 06-17 | 30 / 157 | 7 / 19 | 12.1% |

_Caveat: "done" is measured as-of-today, so newer sprints are structurally penalized for having less elapsed time. Even so, the trend (committed points 58→157 while completion falls 91%→12%) is corroborated independently by the rollover list below—this is a real, not just measurement-artifact, overcommitment trend._

Rollover (stuck 2+ closed sprints, not Done): 19 issues. Worst: FTFL-142/140 and FTFL-622 (7 sprints, ~7 weeks). 12 of the 19 are "Ready for Release"/"Ready for test"—functionally finished work stuck before shipping (FTFL-663–667, 672–676, 504, 506)—this is the clearest signal of a release-step bottleneck, not a dev-capacity one.

Active sprint (Sprint 23, 29 issues / 151 pts): Ready for Release 12, In Progress 7, Backlog 3, Ready for test 3, Blocked 2, Ready for review 1, Done 1. Zero unassigned.

Sprint stories with no detected GitLab activity: cross-referencing all 29 active-sprint keys against both repos' branches/MRs/commits/tags (FTFL-\d+ regex), roughly half show no match. Notably, 8 of the 12 "Ready for Release" tickets (FTFL-665–667, 672, 674–677—all Faro/observability and Data-Ops-UI work) have no matching branch, MR, or commit in either repo. This is either: work that lives in a third repo/config system not covered (plausible for Grafana/Faro dashboard config), a Jira status set prematurely, or a ticket-key/branch-naming mismatch—flagged as a gap, not asserted as a defect (see §5).

#### Stage 3—Development (WIP & Stale bRanches)

WIP per assignee (limit Z=3):

| Assignee | Coding (In Progress) | Queue (Ready for review/test/Release) | Total |
|---|---|---|---|
| Yasir Mansoor | 1 | 7 | 8 |
| Ollie Rushton | 3 | 4 | 7 |
| Pavlo Kotov | 3 | 4 | 7 |
| Robin Mofakham | 5 | 0 | 5 |
| Weronika Jastrzebska | 5 | 0 | 5 |
| Leon Ormes | 1 | 2 | 3 |

Avg time in current status: 30.9 days, max 150 days (FTFL-1, FTFL-98—both unmoved since Jan 21). FTFL-168 (124d) and FTFL-510 (81d) are also dead-still outliers.

Stale branches:

- `deployment`: no in-window open MRs are stale by age (only 2 open MRs total, both pre-date the window, both stale:!634 at 211d,!713 at 96d). 10 FTFL-ticketed branches have commits but no MR ever opened (18–115 days stale)—orphaned WIP.
- `InsightFILE`: 14 branches still exist; 10 have no open MR (18.7–155.8 days stale); of the 4 tied to open MRs, 2 are stale by the 7d/3d rule (!2188 at 145d,!2302 at 36.8d).

Average MR-created→merged is fast on both repos (0.1h / 0.42d)—confirming the bottleneck is _before_ MR or _after_ merge, not the merge step itself. "Ticket → In Progress → first MR opened" cycle time could not be computed—it requires joining per-ticket changelog timestamps to per-branch first-commit timestamps, which wasn't in scope for either side's data pull this pass.

#### Stage 4—Review & Quality Gates

| | `deployment` | `InsightFILE` |
|---|---|---|
| MRs merged in-window | 59 | 29 |
| With ≥1 human review comment | 0 | 0 |
| With a recorded approval | 0 (0 required) | 3 of 29 |
| Avg created→merged | 0.1h (median 0.1h, max 1.2h) | 0.42 days |
| Currently open MRs (all-time) | 2 | 4 |
| Open MR age range | 96d, 211d | 36.8d–173.5d |
| Open MRs with no reviewer | 2 of 2 | 2 of 4 |
| Pipeline pass rate (in-window) | 72.7% (96/132) | 52.0% (66/129, +2 cancelled) |
| Top failing job(s) | `lint_workflows` (31 of 36 failures, 86%) | `frontend_unit_tests` (40), `frontend_lint` (35), `verify_ffcloud` (24) |

`InsightFILE`'s!2282 (FTFL-506 pen-test fix) is the one MR showing genuine review activity (66 notes, 29 human comments between two engineers)—the exception that confirms review _can_ happen, it just essentially never does.

#### Stage 5—Released & Deployed

- `deployment`: real versioned releases—12 semver tags cut in-window (v1.8.61→v1.9.1) ≈ 2.0 deploys/week. 8 of 9 trust environments promoted in-window; `mcnft-prod-1` has not moved in ~110 days (since 2026-03-02)—worth a business check on whether that trust is still active. MR→ticket linkage is strong (58/59, 98%), though two tags reference placeholder keys `FTFL-999`/`FTFL-9999` (broken linkage, not real tickets).
- `InsightFILE`: no real release mechanism. GitLab Releases API is empty; Deployments API is dead since 2022; the only "tag" is a floating `latest-release` pointer, re-pointed once in-window (2026-06-19, an automated package-update commit). Deployment frequency cannot be computed from this signal. Best available proxy: 80 commits landed on `development` in-window referencing 9 tickets (FTFL-494, 504, 512, 608, 631, 663, 664, 725, 999).
- DORA: Deployment Frequency is measurable for `deployment` (~2/wk) but not `InsightFILE`. Lead Time for Changes is only partially computable (MR-merge timestamps exist; tag/release timestamps exist for `deployment`; but joining to Jira ticket-created dates for the specific tagged tickets wasn't pulled in this pass—flagged in §5). Change Failure Rate and MTTR are not computable at all—no Incident issue type, no incident/postmortem tracking found.

#### Stage 6—Flow Efficiency & Bottleneck Summary

20 tickets resolved in-window; full wait/active changelog breakdown computed for 10 (cost-capped—see §5).

| Key | Total (d) | Active (d) | Wait (d) | Flow Eff. | Outcome |
|---|---|---|---|---|---|
| FTFL-712 | 4.0 | 4.0 | 0.0 | 100% | Abandoned |
| FTFL-685 | 2.6 | 2.0 | 0.6 | 75.8% | Done |
| FTFL-476 | 92.0 | 29.9 | 62.1 | 32.5% | Abandoned |
| FTFL-684 | 8.8 | 2.0 | 6.7 | 23.2% | Done |
| FTFL-609 | 58.9 | 9.0 | 49.9 | 15.3% | Done |
| FTFL-604 | 58.1 | 2.3 | 55.8 | 4.0% | Abandoned |
| FTFL-635 | 49.7 | 0 | 49.7 | 0% | Abandoned |
| FTFL-478 | 92.0 | 0 | 92.0 | 0% | Abandoned |
| FTFL-690 | 4.0 | 0 | 4.0 | 0% | Abandoned |
| FTFL-707 | 0.1 | 0 | 0.1 | 0% | Abandoned |

Average flow efficiency: 25.1% (10 detailed) / 41.8% excluding zero-progress abandons. Target is >40%—the sample misses it once abandoned work is included.

Top 3 wait stages by cumulative time: 1) Backlog—219.3 days (73% of all wait), 2) Selected for Development—71.6 days, 3) 🚫Blocked—29.1 days (entirely from one ticket, FTFL-476).

Blocked tickets (12 found—note: status is named `🚫Blocked`, easy to miss with a literal-text query):

| Key | Summary | Assignee | ~Days blocked |
|---|---|---|---|
| FTFL-249 | Data Operations Page bug (customer-reported) | Weronika | ~131 |
| FTFL-279 | Prepare Query Test Script | Unassigned | ~123 |
| FTFL-414/415/416 | MCNFT inbound routes/certs/connectivity | Unassigned | ~109 |
| FTFL-584/590 | Pentest Actions—Cloud/Entra | Robin | ~64 |
| FTFL-632 | Release OMOP vocab in SDE PROD | Weronika | ~53 |
| FTFL-142/140 | NUH design doc/prep | Robin | ~39 |
| FTFL-658 | [SPIKE] MKUH Terraform (timeboxed 2–3d) | Leon | ~12 (4–6x over its own timebox) |
| FTFL-525 | Ensure backups are ZRS | Leon | ~10 |

### 4. Bottleneck Analysis (Ranked)

1. `InsightFILE` has no working release mechanism, and its CI gate fails ~half the time (floating tag only; pass rate 52%, dominated by `frontend_unit_tests`/`frontend_lint`/`verify_ffcloud`). Cross-validated by the Jira rollover list (12 tickets stuck "Ready for Release," several for 3–7 sprints). This is the highest-confidence, highest-impact finding—three independent signals point at the same chokepoint.
2. Zero human code review on either repo. 0/88 merged MRs in-window have a review comment; CI is the _only_ quality gate, and it's unreliable on the app repo (finding 1). Risk compounds: nothing is catching what CI misses.
3. Backlog triage debt, not capacity debt. 196 open items, 90% unassigned, 83% unestimated, 126 untouched 2+ weeks. The FTFL-286/287/289–293 cluster (184–228 days) looks like a fully abandoned feature nobody closed.
4. WIP concentrated and stalling. Yasir at 8 concurrent items (limit 3); FTFL-1 and FTFL-98 untouched 150 days—these read as abandoned-in-place rather than active work soaking time.
5. Throughput numbers are inflated by abandonment. ~60% of "resolved" tickets in the flow-efficiency sample are `Abandoned`, not delivered—any velocity/throughput dashboard that doesn't split this out is overstating real output.

### 5. Data Quality Gaps

- Component field is 100% unused on the 196-item backlog—Stage 1's "by component" breakdown can't be produced.
- Placeholder ticket keys (`FTFL-999`, `FTFL-9999`) appear in commit messages and release-tag linkage on `deployment`—breaks Jira↔GitLab traceability for those specific releases.
- `InsightFILE`'s GitLab Deployments/Releases APIs are dead (Deployments stale since 2022, Releases empty)—true deploy frequency/lead time can't be computed for this repo from GitLab data alone.
- "Approved: true" on several MRs despite zero recorded approvers—almost certainly an "approval not required" project setting rather than a real human gate; don't read this field at face value.
- `statuscategorychangedate`-based duration estimates (used for blocked/in-progress days) only capture category-boundary crossings—same-category status hops (e.g., bouncing within "To Do") aren't reflected, so some durations may understate true elapsed time.
- Stage 6 changelog analysis is partial: full wait/active breakdown computed for 10 of 20 sampled tickets (changelog-walk cost scaling was the limiter); the other 10 only have total elapsed time.
- No Incident issue type and no incident/postmortem tracking found in Jira—Change Failure Rate and MTTR are not computable from available data, full stop.
- ~half of active-sprint tickets (notably 8 of 12 "Ready for Release" items) have no GitLab artifact matched by ticket-key regex across the two repos checked—could mean a third repo/config system, premature status-setting, or branch-naming variance. Not asserted as any one of these—flagged for follow-up.
- Lead Time for Changes (ticket-created → deployed) could only be partially joined—GitLab-side merge/tag timestamps exist, but per-ticket Jira `created` dates for the specific tagged tickets weren't pulled in this pass.

### 6. Recommended Actions (Prioritized)

1. Fix `InsightFILE`'s release process—adopt real version tags/Releases (mirroring how `deployment` already works) instead of the floating `latest-release` pointer. _Directly addresses bottleneck 1._
2. Triage `frontend_unit_tests` / `frontend_lint` / `verify_ffcloud`—together >85% of `InsightFILE`'s pipeline failures, pass rate is only 52%. Until fixed, CI can't function as the team's sole quality gate. _Addresses bottleneck 1/#2._
3. Quarantine/fix `lint_workflows` on `deployment` (86% of its CI failures)—likely a quick, low-risk fix.
4. Introduce a minimal required-review rule on both repos—even one async reviewer. Right now 0/88 merged MRs had any human review. _Addresses bottleneck 2._
5. Run a backlog triage pass—126 items stale >14d with no assignee/estimate; explicitly close or recommit the FTFL-286/287/289–293 cluster (184–228 days, looks fully abandoned) rather than letting it silently age. _Addresses bottleneck 3._
6. Cap and rebalance WIP—Yasir's 8 concurrent items need active triage; close out or reassign FTFL-1 and FTFL-98 (150 days, zero movement) rather than letting them sit "in progress." _Addresses bottleneck 4._
7. Split `Abandoned` out of any velocity/throughput reporting—current "Done" counts conflate delivered and abandoned work, inflating apparent throughput by ~60% in the sampled window. _Addresses bottleneck 5._
8. Confirm whether `mcnft-prod-1` is still a live trust—no promotion in ~110 days; if inactive, drop it from the deploy pipeline.
9. Stop using placeholder ticket keys (`FTFL-999`/`9999`) in commit messages—cheap fix, restores traceability for future analyses like this one.

### 7. Appendix—Raw Metrics

Sprint velocity (full table): see §3 Stage 2.

WIP per assignee (full table): see §3 Stage 3.

Active sprint full roster (29 tickets, key/status/assignee): FTFL-735 Backlog/Ollie · 734 Backlog/Pavlo · 725 Ready-for-Release/Ollie · 693 In-Progress/Ollie · 677/676/675/674 Ready-for-Release/Yasir · 673 Ready-for-Release/Leon · 672 Ready-for-Release/Yasir · 671/670 In-Progress/Pavlo · 669 Backlog/Pavlo · 668 In-Progress/Pavlo · 667/666/665 Ready-for-Release/Pavlo · 664 Ready-for-test/Pavlo · 663 Ready-for-Release/Ollie · 658 Blocked/Leon · 657 Ready-for-review/Leon · 622 In-Progress/Yasir · 609 Done/Leon · 525 Blocked/Leon · 512 In-Progress/Leon · 506 Ready-for-test/Yasir · 504 Ready-for-Release/Ollie · 39 Ready-for-test/Ollie · 38 In-Progress/Ollie.

Rollover list (19 tickets): FTFL-142, 140 (7 sprints, Blocked) · 622 (7, In Progress) · 506 (6, Ready for test) · 504 (6, Ready for Release) · 559 (5, In Progress) · 667, 666, 665, 664, 663 (4, Ready for Release/test) · 512 (4, In Progress) · 675, 674, 672 (3, Ready for Release) · 658 (3, Blocked) · 676, 673 (2, Ready for Release) · 525 (2, Blocked).

Release tags in-window (`deployment`, 12): v1.8.61 (05-12, FTFL-496/549/608/638) → v1.9.1 (06-19, FTFL-39)—full table in §3 Stage 5.

Blocked tickets (12): see §3 Stage 6 table.

Stage 6 sample (20 tickets, totals only for the other 10): FTFL-555 (56.0d), 602 (50.9d), 683 (3.3d), 634 (38.1d), 608 (46.0d), 430 (89.0d), 428 (89.1d), 191 (125.1d), 216 (118.1d), 643 (27.2d).
