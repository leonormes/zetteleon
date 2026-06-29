---
confluence_page_id: 2881290243
created: 2026-06-22 00:00:00+00:00
modified: 2026-06-22 14:30:01+00:00
project_name: Pipeline
source: https://fitfile.atlassian.net/wiki/x/AwC9qw
status: draft — needs Leon's input before copying back to Confluence
tags:
- 1
- 2
- 3
- 4
- 5
- confluence-draft
- delivery
- fitfile
- process
- review
title: FITFILE Delivery Health Review — Draft Revision (Robin's Comments)
permalink: llmeon/wiki/projects/fitfile-delivery-health-review-draft-revision-robins-comments
---

## FITFILE Delivery Health Review—Draft Revision

Pulled from Confluence page "FITFILE Delivery Health Review: Unblocking Work Flow and Improving Delivery Outcomes" (page ID `2881290243`), along with Robin Mofakham's 21 inline review comments (all currently unresolved). This note is a working revision that addresses every comment—either with a concrete edit, or with a flagged question where only you can supply the missing fact. Do not copy this to Confluence until the flagged items below are resolved.

### ⚠️ Open Questions for You (resolve before publishing)

Cross-referencing Robin's comments against the underlying `FITFILE Value Stream Report - 2026-06-20.md` resolved four of the original five flags with real data. One genuinely needs your/Robin's input—see below.

1. Reviewer checkpoint—Robin dislikes it for small teams. Still open. The Value Stream Report's own recommendation 4 already frames this as minimal—"even one async reviewer"—so the proposal in the doc isn't the heaviest version of this idea. Worth asking Robin directly what he'd prefer instead, given that framing.
2. The "OR" claim is now only partly resolved, and the rest is a judgement call for you. The Value Stream Report confirms Ollie Rushton (`OR`) is a real engineer carrying his own queue of 7 items (3 in progress, 4 awaiting review/test/release)—same shape as everyone else's overloaded WIP, not a role as a designated reviewer for other people's work. It also shows most _open_ MRs have no reviewer assigned at all on either repo (2 of 2 on `deployment`, 2 of 4 on `InsightFILE`). So the aggregate data doesn't support "tickets are stuck because OR hasn't reviewed them" as a general pattern—but Robin may be thinking of specific tickets the aggregate stats wouldn't surface. Worth checking with him directly before asserting the data contradicts him in the doc itself; I've kept the doc's wording neutral rather than rebutting him in writing.

Everything else below is now resolved with sourced data rather than left as a bracketed flag—see the coverage table.

---

### Comment-by-comment Coverage

| # | Robin's comment (on…) | What changed |
|---|---|---|
| 1 | "A note on how to read this."—_"No need for this filler"_ | Callout removed; its point folded into plain prose in the new Introduction |
| 2 | "A 30-second Glossary"—_move out of section 1_ | Moved to an Appendix at the end |
| 3 | Headline/"What the Data Shows"—_intro should state what+problem+proposal_ | Rewritten Introduction with explicit "what this is / the problem / the proposed direction" structure |
| 4 | "Theme"—_"Finding" is stronger_ | All four "Theme A–D" renamed to "Finding A–D" throughout |
| 5 | "Business impact"—_make it bold_ | Apply bold formatting to this label in Confluence when you paste it in (this vault's linter strips `**` from notes, so it won't survive here, but the label is isolated on its own line everywhere it appears, ready to bold) |
| 6 | Outage section—_be more specific_ | Rewritten with concrete facts from the FTFL-512 investigation (ticket, MR, dates, MTTR) |
| 7 | "Blocked"—_recent freeze or general?_ | Resolved with the Value Stream Report: it's `InsightFILE`'s structurally broken release path (no real version tags—just a floating `latest-release` pointer—plus a 52% CI pass rate). Chronic, not a recent freeze |
| 8 | "Building also has its own issues" | Resolved with real data: most engineers are running 5–8 concurrent items against the informal WIP limit of 3, average 30.9 days in current status (max 150), and roughly a third of branches on each repo have commits but no MR ever opened |
| 9 | "196-item to-do list, mostly unsorted"—_most belong to an epic_ | Reworded to the defensible stats only—and Robin was right: the Value Stream Report confirms "epic breakdown discipline is otherwise healthy" (only 2 of 29 epics have no child stories) |
| 10 | "No human review…52%"—_data? which repo?_ | Repo scope now confirmed: 0 of 88 merged MRs (59 on `deployment`, 29 on `InsightFILE`) have a review comment; 52% is specifically `InsightFILE`'s CI pass rate. The "OR" part of this comment is still open—see open question 2 |
| 11 | "Option 1—Do Nothing"—_put at the end as "what happens if we don't"_ | Moved to end, retitled "What Happens If We Don't Act" |
| 12 | "Option 2—Unblock the Finish Line"—_catchy title, be descriptive_ | Retitled "Build a Reliable, Repeatable Release Path for Application Work" |
| 13 | Infra comparison—_"not in my opinion! No automated testing on infra, tf plan isn't a test"_ | Reworded to compare shipping _cadence_ only, not quality/testing |
| 14 | "Clear the existing queue…"—_worded like an action, should be an intention_ | Reworded as an outcome/intention statement |
| 15 | "Make the automated checks trustworthy"—_how?_ | Made concrete: named the actual failing CI jobs from the Value Stream Report (`lint_workflows` on `deployment`; `frontend_unit_tests`/`frontend_lint`/`verify_ffcloud` on `InsightFILE`), plus the specific CI gap found in FTFL-512 |
| 16 | Reviewer checkpoint—_dislikes it for small teams_ | Flagged above (open question 1) |
| 17 | "Right-size each cycle's commitment"—_complaint, not an action_ | Reworded into a concrete, data-driven action |
| 18 | "Report delivered work separately"—_look at why Jira's resolution field is set this way_ | Reworded to investigate the "Abandoned" resolution and dashboard handling, rather than just "report separately" |
| 19 | "Regularly prune the to-do list"—_"I'd be more in favour of another space"_ | Reworded to moving stale items to a separate backlog/parking-lot rather than closing them |
| 20 | "robot"—_where?_ | Resolved: named the actual failing CI jobs (see #15) directly in Finding B's business-impact line |
| 21 | "The Options at a Glance"—_not exclusive, want a plan not options_ | Replaced the comparison table with a single sequenced "Recommended Action Plan" |
| extra | (not a Robin comment) Finding C's table only showed 4 of the 6 cycles in the reviewed period, skipping cycles 18 and 20 | Expanded to all six cycles, per the Value Stream Report. Also corrected Finding A's "two to seven cycles" to "two to six cycles"—the rollover data's actual max for the 12 stuck items is 6, not 7 |

---

#### Introduction

This is a systemic review of how work flows through the team—not a review of any individual. Names have been left out deliberately. The team is fast and capable at the core job of building software; the gaps below are in the system around them, where good work is being slowed down or wasted. Every number quoted comes directly from our own Jira and delivery data. (Engineering terms below are explained in the glossary in the Appendix.)

The problem: We build fast, but finished work struggles to reach customers. The slow point is after the work is done, not in doing it.

The proposed direction: give customer-facing application work the same reliable way to ship that our infrastructure changes already have, add a lightweight check before a change goes live, and size our commitments to what the team has actually proven it can deliver. Section 1 below sets out the evidence; Section 2 sets out how to get there.

---

#### 1. The Current Reality

The findings group into four business areas, plus one real-world example.

---

##### Finding A—We Build Fast, but Finished Work Doesn't Ship

- Once a developer finishes a parcel of work, it is accepted into the product in minutes to hours—the building step is not our problem.
- Yet 12 separate pieces of finished work (all in the customer-facing application repo, `InsightFILE`) have been sitting in a "ready to ship" state for two to six cycles (up to ~6 weeks).
- An important distinction: our infrastructure changes (the `deployment` repo) flow out smoothly—roughly twice a week, reliably. It is our customer-facing application work (`InsightFILE`) that piles up, because that side of the house has no reliable, repeatable way to ship.

Business impact: We are paying full price for work (engineering time spent building it) and then not collecting the return (the value reaching customers). Effort is being completed but not _realised_.

---

##### Finding B—Almost Nothing Gets a Second Pair of Eyes before it Ships

- Of 88 changes shipped in the six-week window (59 on `deployment`, 29 on `InsightFILE`), zero received a single human review comment.
- That leaves the automated safety net as the only line of defence—and on our main application (`InsightFILE`), that net gives a clean pass only ~52% of the time (roughly a coin-flip).

> 🚩 Note: see open question 2 at the top of this note before publishing—Robin's specific concern about a reviewer bottleneck may still need addressing here.

Business impact: A single person can push a change live with no second pair of eyes and an unreliable automated check as the only safety net—concretely, the application repo's pipeline fails most often on `frontend_unit_tests`, `frontend_lint`, and `verify_ffcloud`, which together cause over 85% of its failures. When the automated check misses something, nothing else catches it.

---

##### Finding C—We're Promising More than We Can Deliver

Over the last six cycles, the amount of work committed to climbed steadily while the amount actually finished fell just as steadily:

| Delivery cycle | Work committed | Work finished (as of this report) |
| --- | --- | --- |
| Cycle 17 (closed 13 May) | 172 units | 91% |
| Cycle 18 (closed 20 May) | 108 units | 81% |
| Cycle 19 (closed 27 May) | 58 units | 36% |
| Cycle 20 (closed 3 June) | 89 units | 21% |
| Cycle 21 (closed 10 June) | 118 units | 19% |
| Cycle 22 (closed 17 June) | 157 units | 12% |

_(The most recent cycles have had less time to complete, which flatters older cycles slightly—but the same downward trend shows up independently in the pile of rolled-over work, so the over-commitment is real, not a quirk of the maths. All six cycles in the reviewed period are shown here, not a selected subset.)_

Business impact: Plans and forecasts are drifting away from reality. When a team commits to nearly three times more than it can deliver, dates stop meaning anything, and stakeholder trust in those dates erodes.

---

##### Finding D—Our "Done" Numbers Overstate Real Progress

- In a representative sample of "completed" work, roughly 60% was actually abandoned, not delivered.
- Our to-do list has grown to 196 open items: 90% have no owner, 83% have no size estimate, and 126 have sat untouched for two weeks or more—some for over 200 days.

Business impact: Any progress dashboard that counts abandoned work as "done" is overstating real output by more than half. Meanwhile the to-do list is large, much of it unowned and unestimated, which makes it hard to tell what's actually next.

---

##### A Real-World Example: the Silent `ff-test-a` Outage (FTFL-512)

On 18 June 2026, a one-line ingress annotation change ([MR!802](https://gitlab.com/fitfile/deployment/-/merge_requests/802), 0 reviewers, 0 review comments) was squash-merged to `master`. The only CI gate on that merge request ran two jobs, neither of which touched the Helm chart or Kubernetes manifests it changed—so no automated check looked at the risky part either.

ArgoCD's admission webhook rejected the change when it tried to sync to the `ff-test-a` (staging) environment. Because `frontend` sits upstream of `certificates` and `mssql` in that environment's deploy ordering, neither of those components could sync while the failure stood—blocking deployment of unrelated work (including ticket FTFL-999) for roughly 8 hours 47 minutes, start to fix.

For about 7 hours 40 minutes of that window, the environment sat silently in a `Degraded` state—no alert fired, no retries ran. It was only fixed because an engineer working on an unrelated ticket happened to notice it and patched it in passing.

The same class of failure—a snippet annotation rejected by this same admission webhook, on this same file—had already happened twice before, undetected by any automated check either time.

See `FTFL-512 CI-CD Pipeline Incident Investigation` for the full write-up.

Business impact: This is the cost of the gaps in Findings A and B made visible: one unchecked change cost the team most of a working day, nobody was warned for almost 8 hours, and the lesson wasn't captured the first two times—so it kept happening.

---

#### Where Work Actually Gets Stuck (the Flow at a Glance)

| Stage of the journey | Is it a problem? | What's happening |
| --- | --- | --- |
| Deciding what to build | ⚠️ Cluttered | 196 open items; 90% unowned, 83% unestimated |
| Committing to a cycle | ⚠️ Over-loaded | Committing ~3× what we finish; the gap is widening |
| Building it | ✅ Comparatively strong | Fast—but not friction-free: most engineers carry 5–8 concurrent items against an informal limit of 3, and roughly a third of branches on each repo have commits but no MR ever opened |
| Checking it's safe | 🔴 Weak | 0 of 88 merged changes had a human review comment; the application repo's automated check passes only ~52% of the time |
| Shipping to customers | 🔴 Blocked | `InsightFILE` has no real release mechanism—just a rarely-repointed floating tag—so finished application work piles up with no reliable way out. This is chronic, not a recent freeze |

Building is a comparative strength in this data, but not an issue-free one: WIP is running well above the team's own informal limit, and a meaningful share of started work is abandoned mid-branch before a merge request is even opened. Even so, the data shows building it is markedly less constrained than checking and shipping it—that's where the bulk of the delay and risk in this period concentrate.

---

#### 2. Strategic Options for Moving Forward

These are not mutually exclusive—the strongest path combines them in sequence, set out below as a single plan rather than a menu. A detailed, low-risk technical plan already exists for every change below; this paper deliberately stays at the workflow level so the business decision can be made on outcomes, not configuration.

---

##### Step 1—Build a Reliable, Repeatable Release Path for Application Work

_Tackles Finding A and the shipping half of the FTFL-512 example._

The process change:

- Give the customer-facing application (`InsightFILE`) the same regular, predictable shipping cadence that our infrastructure changes (`deployment`) already have—real version tags and releases, rather than a floating pointer. (To be clear: this is about cadence, not about infrastructure's testing rigour—infrastructure changes currently rely on checks like `tf plan`, which validate that a change is well-formed, not that it's correct, so this isn't a claim that infra is fully tested either.)
- Work down the existing backlog of finished-but-unshipped work so nothing is left stranded once the new path is in place.

Why it's the highest-leverage move: three independent signals all point at this single chokepoint—it is the largest pile of finished work and the clearest bottleneck in the data.

Expected outcome:

- Finished work starts reaching customers in days, not weeks.
- We begin collecting the return on work we've already paid to build.
- Delivery becomes visible and steady, which directly rebuilds forecast credibility.

---

##### Step 2—Add a Lightweight Safety Net

_Tackles Finding B and the prevention half of the FTFL-512 example._

The process change:

- Introduce a lightweight second-pair-of-eyes checkpoint before a change goes live—even one quick reviewer. [🚩 _Robin dislikes the standard protected-branch-plus-reviewer approach for a small team; the source data's own recommendation already frames this as "even one async reviewer"—worth confirming with him what's still a concern given that framing. See open question 1_]
- Extend the automated checks to actually cover the kind of change that slipped through in FTFL-512—the CI gate that passed MR!802 ran two jobs, neither of which touched the Helm chart or manifests it changed. Closing that specific gap, plus fixing the checks already known to be unreliable—`lint_workflows` causes 86% of the infrastructure repo's CI failures, and `frontend_unit_tests`, `frontend_lint`, and `verify_ffcloud` together cause over 85% of the application repo's—is what "trustworthy" means here.
- Add alerts so that a silent failure surfaces in minutes, not hours—FTFL-512 sat silently `Degraded` for 7h40m with nothing watching.

Why it matters: right now the only safety net is an automated check that's right about half the time, with nothing behind it. FTFL-512 shows exactly what that costs.

Expected outcome:

- Far fewer changes break shared systems—a reviewer catches what the automated checks miss.
- When something does slip through, it's caught in minutes, not after most of a working day.
- The recurring class of incident stops recurring, because the lesson is captured once and enforced automatically.

---

##### Step 3—Match Our Commitments to Our Capacity

_Tackles Findings C and D._

The process change:

- Use the last six cycles' completion data (91% → 81% → 36% → 21% → 19% → 12%) to set the size of the next cycle's commitment, rather than carrying over the full backlog request as-is.
- Set and respect limits on how many things one person juggles at once.
- Investigate why so much committed work resolves as "Abandoned" in Jira—that resolution may well be the right call case-by-case, but make sure dashboards report Abandoned and Delivered as separate totals rather than counting both as "done."
- Move long-stalled or abandoned-in-place items to a separate backlog/parking-lot list, rather than mixing them with the active to-do list.

Why it matters: we're committing to ~3× what we finish, one person is juggling 8 items against an informal limit of 3, and our "done" numbers are inflated by more than half. None of this is a people problem—it's a planning-and-visibility problem.

Expected outcome:

- Commitments the team can actually meet, restoring trust in dates.
- A cleaner active to-do list where the important work is easy to find.
- Honest dashboards—leadership sees real delivery, not abandoned work dressed as progress.

---

#### What Happens If We Don't Act

Doing nothing is a legitimate choice, but it is not a neutral one—the trends above continue on their current trajectory:

- The gap between promises and delivery keeps widening. Completion has fallen in five of the last six cycles (91% → 12%). On the current line, forecasts become fiction, and planning loses credibility with stakeholders.
- Finished work keeps piling up unshipped. The "ready to ship" queue grows. We continue paying to build value we never collect.
- The to-do list keeps growing untended. More items, less sorted, harder to find what matters—planning debt compounds on itself.
- Quality incidents recur—and stay silent. FTFL-512's failure class has _already_ happened twice. With no second reviewer and an unreliable automated check, more silent, team-blocking outages are a matter of when, not if. Each one costs the whole team, not one person.
- Sustained effort-without-output is a known morale and retention risk. A capable team working hard while visible delivery falls, punctuated by recurring fire-fighting, is a recognised driver of frustration and attrition.

Expected outcome: slow, compounding decline in delivery predictability and throughput, with rising incident risk. The team keeps working hard; the system keeps wasting that effort.

---

#### Appendix: A 30-Second Glossary

A few engineering terms appear unavoidably. Here is what they mean in business terms:

| You may hear…            | It really means…                                                                                                                             |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Delivery pipeline        | The automated assembly line that takes a change from a developer's desk to customers                                                         |
| Automated quality checks | The robotic safety net that inspects every change before it ships                                                                            |
| A "change" / "merge"     | One parcel of finished work being accepted into the live product                                                                             |
| Work-in-progress (WIP)   | How many separate things one person is juggling at once                                                                                      |
| Backlog                  | The to-do list of requested work not yet started                                                                                             |
| Delivery scorecard       | The industry-standard four measures of delivery health: _how fast we ship, how often, how often we break something, and how fast we recover_ |