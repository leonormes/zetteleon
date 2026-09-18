---
created: 2026-09-16T00:00:00+00:00 work packages ahead of a cost/planning review with Robin
modified: 2026-09-16T10:58:24+00:00
permalink: llmeon/work/ftfl-backlog-reorg-ci-cd-entra-iam-pentest-2026-09-16
title: FTFL Backlog Reorg — CI-CD, Entra IAM & Pentest (2026-09-16[[FTFL Work Packages — ROI-Prioritised Rework (2026-09-16)]] - entra-iam
  - fitfile
  - jira
  - pentest
  - roi
---

## Source

Reworked from the raw extract in [[FTFL Backlog Reorg — CI-CD, Entra IAM & Pentest (2026-09-16)]]—that note has the full ticket-by-ticket detail, epic descriptions, and the observations that shaped the groupings below. This note re-packages the same ~270 points of currently open work (Done/Closed tickets excluded—they don't need prioritising) into 11 outcome-based packages, tiered by value vs. effort, instead of 7 epics that don't map to how the work should actually be sequenced.

How to read the cost column: points are Jira Story Points. Where marked _(draft)_, no team estimate existed on the ticket—Claude estimated it earlier today on a 1/2/3/5/8/13 scale, and it should be treated as a placeholder for the team to confirm, not a committed number. This applies to all of FTFL-1029 (Robin's identity epic never had any estimates at all) and a handful of others called out below.

---

## Bigger picture—Robin's Company-wide Priority List

Robin keeps his own [Confluence page, "Upcoming technical work"](https://fitfile.atlassian.net/wiki/x/BQDlt), last updated today (2026-09-16). In his own words: _"some suggested values have been populated but this has been done in a silo"_—i.e. not yet reconciled with the team's own view, which is exactly what this note and its source are for.

This is the critical thing to see before using the packages below: everything in this review (7 Jira epics, ~270 open points) covers only 2 of Robin's 17 line items. The other 15—Nginx EOL, Postgres major-version upgrades, Netbird, Firewall, the wider Grafana/alerting estate (686 rules, 29 firing, largely broken dashboards), multi-zone availability, backup restore testing, business backups, quality-check coverage, node divergence, SSO, Intune migration, and the HDRS expertise gap—aren't in Jira under any epic this review touched, so they aren't costed anywhere in this note. Don't read the 270-point total as "the technical backlog"—it's a slice of it.

### Robin's Full List

| Title                           | Effort    | Importance | Urgency | Status      | Outsource | Maps to this review?                                                                                                                              |
| ------------------------------- | --------- | ---------- | ------- | ----------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| HDRS - support (expertise)      | Large     | High       | High    | —           | —         | No—not in Jira scope reviewed                                                                                                                     |
| Gitlab Cost Optimisation        | Low       | High       | High    | Started     | —         | Yes—FTFL-1025 + Package 3                                                                                                                         |
| Improve FITFILE Release Process | High      | High       | High    | —           | Yes       | Yes—FTFL-759/971/1000/1065, most of Packages 1, 3, 4, 7, 8, 9, 11                                                                                 |
| Nginx ingress - EOL             | Large     | High       | High    | Overdue     | Yes       | No                                                                                                                                                |
| Container updates - Postgres    | Large     | High       | High    | —           | —         | No                                                                                                                                                |
| Netbird                         | Medium    | Medium     | Medium  | —           | TechAhoy  | No                                                                                                                                                |
| Firewall                        | Medium    | High       | Medium  | —           | —         | No                                                                                                                                                |
| Observability and Alerting      | Large     | High       | High    | —           | —         | Partially—Package 4 (CI heartbeat/telemetry) is a small slice of a much bigger Grafana/alerting problem (686 rules, 29 firing, dashboards broken) |
| Vulnerability management        | Medium    | High       | Medium  | In Progress | —         | No—this is FTFL-865, a separate epic not pulled into this review                                                                                  |
| Pen Test                        | Medium    | High       | Medium  | Started     | —         | Yes—FTFL-584, Packages 5 + 10                                                                                                                     |
| Multi-zone availability         | Medium    | Medium     | Medium  | —           | —         | No                                                                                                                                                |
| Node Backup Restore             | Small     | High       | High    | Started     | —         | No                                                                                                                                                |
| Business Backups                | Small     | High       | High    | Started     | —         | No                                                                                                                                                |
| Quality checks                  | Medium    | High       | High    | —           | —         | No                                                                                                                                                |
| Node divergence                 | Med-Large | High       | Medium  | Started     | —         | No                                                                                                                                                |
| SSO                             | Small     | Medium     | Medium  | —           | —         | No                                                                                                                                                |
| Intune Migration                | Medium    | High       | High    | —           | —         | No                                                                                                                                                |

_(Entra IAM—FTFL-1029/1030—doesn't appear anywhere on Robin's list at all, under any name. Worth flagging to him directly: either it's meant to be folded into "Pen Test" implicitly, or it's a genuine gap in his own tracking that only exists because the Entra audit happened on 2026-09-07, after this Confluence page was first created.)_

### Two Things that Change how the Packages below Should Be Read

1. "Improve FITFILE Release Process" is tagged `Outsource: Yes`. That's FTFL-759 by name—the epic that FTFL-971 (security hardening), FTFL-1000 (pipeline performance), and FTFL-1065 (async Argo gating) all sit under or beside. If Robin is seriously considering outsourcing this whole area, that's a live input for Packages 1, 3, 4, 7, 8, 9, and 11 below (roughly 137 of the 270 points in this note)—worth raising explicitly before assuming this is all internal-team capacity planning. Package 2 is under `PenTest`, package 5 and 6 are the only pieces of this review that don't sit under either of Robin's two flagged line items.
2. Robin's own fallback for the cost problem is bigger than anything ticketed. His Gitlab Cost Optimisation note says: _"if [current optimisations] are ineffective—further work may need to be undertaken—such as migrating to our private cloud on a 'serverless' model."_ Nothing in Jira today reflects that option—it's a strategic alternative sitting one level above Package 3's runner-caching work, not a ticket. Worth a one-line mention if Package 3's savings don't land as expected.

Robin's own effort/importance/urgency tags corroborate the split this note already landed on independently: "Gitlab Cost Optimisation" is tagged Low effort (matches Package 3 being in the Now tier) while "Improve FITFILE Release Process" is tagged High effort (matches Packages 7/8/9/11, the largest and most speculative packages, mostly landing in Next/Later).

---

## Top-line view for Prioritisation

| Tier  | Package                                                   | Points         | Tickets      | Why this tier                                                                           |
| ----- | --------------------------------------------------------- | -------------- | ------------ | --------------------------------------------------------------------------------------- |
| Now   | 1. Close the last CI/CD security gaps                     | 12             | 3            | Finishes work that's already 90% shipped; closes a live unprotected-secret gap          |
| Now   | 2. Quick identity wins                                    | 12 _(draft)_   | 6            | Small, well-scoped, 3 already Highest priority, one is Blocked and gating other work    |
| Now   | 3. Stop paying for idle CI runners                        | 18 _(1 draft)_ | 3            | Direct answer to the GitLab cost problem; design already PoC'd                          |
| Next  | 4. See when the pipeline goes quiet                       | 16             | 2            | Closes a real blind spot—silent CI failures go unnoticed today                          |
| Next  | 5. Finish the pentest quick wins                          | 18 _(1 draft)_ | 4            | Closes 4 of the remaining 9 pentest findings; one already "Ready for review"            |
| Next  | 6. Reduce standing privilege—main rollout                 | 37 _(draft)_   | 6            | The bulk of Robin's own top-priority security epic                                      |
| Next  | 7. Make releases safe to roll back                        | 16 _(draft)_   | 2            | Epic's own research calls this "the single largest untracked MTTR risk"                 |
| Next  | 8. Speed up how code ships                                | 26 _(draft)_   | 4            | Attacks the single-owner approval bottleneck + long-lived-branch merge skew             |
| Next  | 9. Close out Entra-as-code                                | 8 _(1 draft)_  | 2            | Nearly-finished epic—cheap to fully close before package 6 ramps up                     |
| Later | 10. Remaining big pentest findings (logging/network/disk) | 65 _(2 draft)_ | 5            | Large, and one item may be partly duplicate work—investigate before committing          |
| Later | 11. Contract testing & progressive delivery               | 42 _(draft)_   | 4            | Longest horizon, most speculative value of everything in this view                      |
| —     | _Unscoped_                                                | —              | 1 (FTFL-884) | No description exists—can't be costed or prioritised until someone writes what it's for |

Totals: Now = 42 pts (12 tickets) · Next = 121 pts (16 tickets) · Later = 107 pts (9 tickets) · Grand total = 270 points across 27 open tickets, plus one ticket that needs scoping before it can even join this table.

---

## Now

### 1. Close the Last CI/CD Security gaps—12 Pts

Tickets: [FTFL-1057](https://fitfile.atlassian.net/browse/FTFL-1057) (2, protect GCR_PASSWORD/RUNTIME_ACCESS_TOKEN) · [FTFL-986](https://fitfile.atlassian.net/browse/FTFL-986) (8, Trivy+SAST gate before push on InsightFILE) · [FTFL-984](https://fitfile.atlassian.net/browse/FTFL-984) (2, fix InsightFILE merge-train verification gap)

Why now: These are the only three things standing between FTFL-971 and being a fully closed epic—Wave 0 and Wave 1 (18 tickets) are already done. Low effort, no dependencies, converts an "In Progress" epic into "Done."

Risk if skipped: InsightFILE ships without a pre-push vulnerability scan gate; the merge-train verification gap stays open.

### 2. Quick Identity wins—12 Pts _(draft — no Existing estimates)_

Tickets: [FTFL-1031](https://fitfile.atlassian.net/browse/FTFL-1031) (2, remove Privileged Role Administrator from JumpCloud connector) · [FTFL-1032](https://fitfile.atlassian.net/browse/FTFL-1032) (3, decide CIPP-SAM permission scope—currently Blocked) · [FTFL-1042](https://fitfile.atlassian.net/browse/FTFL-1042) (2, decide Entra P2 seat count) · [FTFL-1040](https://fitfile.atlassian.net/browse/FTFL-1040) (1, diary the 2027 PIM expiry cliff) · [FTFL-1041](https://fitfile.atlassian.net/browse/FTFL-1041) (2, identify 2 unexplained managed identities with Contributor on Production) · [FTFL-1043](https://fitfile.atlassian.net/browse/FTFL-1043) (2, directory role housekeeping)

Why now: Six small, mostly-independent items from Robin's own High-priority epic—three are already tagged Highest. FTFL-1032 is Blocked and is what's stopping FTFL-1042 from moving; unblocking it (a scope decision on an MSP tool's permissions, not code) should be the very first thing looked at here.

Risk if skipped: Two unexplained identities with Contributor on Production stay uninvestigated; the JumpCloud connector keeps GA-equivalent access it doesn't need.

### 3. Stop Paying for Idle CI runners—18 Pts _(1 draft)_

Tickets: [FTFL-1065](https://fitfile.atlassian.net/browse/FTFL-1065) (10 draft, async Argo gating—removes a 30-min runner hold on every InsightFILE merge-train run) · [FTFL-987](https://fitfile.atlassian.net/browse/FTFL-987) (3, BuildKit registry cache for deployment Argo builds) · [FTFL-988](https://fitfile.atlassian.net/browse/FTFL-988) (5, InsightFILE BuildKit yarn cache + always-on install_dependencies)

Why now: This is the most direct lever on the GitLab bill outside FTFL-1025 (already handled this week). FTFL-1065's design is fully PoC'd against a real merge train—this is "go implement," not "go research." Cross-checked against Robin's own tracking: his Confluence page independently tags this whole area (his "Gitlab Cost Optimisation" line) as Low effort / High importance / High urgency / Started—matching this package's Now placement.

Risk if skipped: Every merge-train run keeps holding a runner idle for ~30 minutes; build caching stays unoptimised.

---

## Next

### 4. See when the Pipeline Goes quiet—16 Pts

Tickets: [FTFL-990](https://fitfile.atlassian.net/browse/FTFL-990) (8, Pushgateway/heartbeat + Prometheus absent() alerting) · [FTFL-989](https://fitfile.atlassian.net/browse/FTFL-989) (8, telemetry emitters across named CI controls)

Why next, not now: Real value (catches silent CI failures before they become incidents) but not urgent—nothing is on fire today. Same underlying skill (observability/alerting) as package 10's FTFL-569/570 (Azure diagnostic logging)—worth considering whether one person tackles both back-to-back rather than context-switching between CI and Azure observability separately. Also worth noting: this is a small slice of a much bigger problem—Robin's page separately flags the production Grafana estate itself as broken (686 alert rules, 29 firing, several dashboards not reporting data), which isn't touched by anything in this review at all.

### 5. Finish the Pentest Quick wins—18 Pts _(1 draft)_

Tickets: [FTFL-575](https://fitfile.atlassian.net/browse/FTFL-575) (8, AKS local accounts not disabled—already "Ready for review") · [FTFL-583](https://fitfile.atlassian.net/browse/FTFL-583) (5, 39 app registrations with credentials) · [FTFL-765](https://fitfile.atlassian.net/browse/FTFL-765) (3, review app registrations—this is the scoping spike that feeds FTFL-583, do it first) · [FTFL-1056](https://fitfile.atlassian.net/browse/FTFL-1056) (2 draft, increase log analytics retention)

Why next: Closes 4 of the 9 remaining findings from an April pentest report cheaply. FTFL-765 should be sequenced before FTFL-583 since it's the investigation that scopes it. Robin's page notes a retest is required and that 2027's pen test needs preparing for—both packages 5 and 10 together are what stands between here and that retest being clean.

### 6. Reduce Standing privilege—main rollout—37 Pts _(all draft)_

Tickets: [FTFL-1033](https://fitfile.atlassian.net/browse/FTFL-1033) (8, reduce Application.ReadWrite.All grants) · [FTFL-1034](https://fitfile.atlassian.net/browse/FTFL-1034) (8, constrain privileged Azure RBAC on automation identities) · [FTFL-1035](https://fitfile.atlassian.net/browse/FTFL-1035) (5, remove User Access Administrator at tenant root) · [FTFL-1037](https://fitfile.atlassian.net/browse/FTFL-1037) (8, migrate engineers from standing Owner to PIM-eligible) · [FTFL-1038](https://fitfile.atlassian.net/browse/FTFL-1038) (3, second break-glass account + tested runbook) · [FTFL-1039](https://fitfile.atlassian.net/browse/FTFL-1039) (5, leaver cleanup—39 disabled accounts + guest review)

Why next: This is the bulk of Robin's own top-priority epic (FTFL-1029)—everything here removes a standing privileged grant that bypasses PIM entirely. All estimates are drafts since none existed; worth a team estimation pass before treating this number as real. Not on Robin's Confluence list under any name—worth raising with him directly since it's his own epic.

Risk if skipped: Engineers keep standing (not just-in-time) Azure Owner access; the tenant root still has a broader User Access Administrator grant than it needs.

### 7. Make Releases Safe to Roll back—16 Pts _(draft)_

Tickets: [FTFL-1006](https://fitfile.atlassian.net/browse/FTFL-1006) (8 draft, rollback procedure for migration-bearing releases) · [FTFL-1008](https://fitfile.atlassian.net/browse/FTFL-1008) (8, publish/version Helm charts to ACR—already Selected for Development with 2 phases merged)

Why next: FTFL-1000's own research explicitly names the lack of a rollback procedure as "the single largest untracked MTTR risk" today. Hard dependency: FTFL-1006 can't work without versioned charts, which is exactly what FTFL-1008 delivers—sequence 1008 first (it's already most of the way there). Sits under Robin's "Improve FITFILE Release Process" (Outsource: Yes)—see the note at the top of this document.

### 8. Speed up how Code ships—26 Pts _(all draft)_

Tickets: [FTFL-1004](https://fitfile.atlassian.net/browse/FTFL-1004) (8, select feature-flag platform) · [FTFL-1005](https://fitfile.atlassian.net/browse/FTFL-1005) (5, trunk-based dev pilot) · [FTFL-1010](https://fitfile.atlassian.net/browse/FTFL-1010) (8, decentralise PR approvals) · [FTFL-1007](https://fitfile.atlassian.net/browse/FTFL-1007) (5, move customer-specific config into its own repo)

Sequencing matters here: FTFL-1004 (feature flags) must land before FTFL-1005 (trunk-based pilot)—the epic's own notes say trunk-based dev depends on flags existing first. FTFL-1010 has an unticketed dependency: the source research says PR-approval decentralisation should wait until flaky tests are stabilised, but no ticket exists for that—worth raising before scheduling this one. Sits under Robin's "Improve FITFILE Release Process" (Outsource: Yes).

### 9. Close out Entra-as-code—8 Pts _(1 draft)_

Tickets: [FTFL-1052](https://fitfile.atlassian.net/browse/FTFL-1052) (3, dynamic groups for baseline access—In Progress) · [FTFL-1053](https://fitfile.atlassian.net/browse/FTFL-1053) (5 draft, group naming standard + import ~95 remaining groups—In Progress)

Why next: Cheap to finish—these are the only two open items left in an otherwise-complete epic (9 of 11 children already Done). Worth closing out before package 6 ramps up the identity work, since a clean, fully-Terraformed group structure makes that rollout easier.

---

## Later

### 10. Remaining Big Pentest Findings (Logging, Network, disk)—65 Pts _(2 draft)_

Tickets: [FTFL-569](https://fitfile.atlassian.net/browse/FTFL-569) (21, no diagnostic settings/activity log export) · [FTFL-570](https://fitfile.atlassian.net/browse/FTFL-570) (21, no activity log alerts—11 missing) · [FTFL-580](https://fitfile.atlassian.net/browse/FTFL-580) (13, 7 disks not encrypted with customer-managed keys) · [FTFL-572](https://fitfile.atlassian.net/browse/FTFL-572) (5 draft, unrestricted outbound on all NSGs) · [FTFL-577](https://fitfile.atlassian.net/browse/FTFL-577) (5 draft, AKS OIDC issuer disabled)

Before committing to this package's cost: FTFL-577 may substantially overlap with the Azure OIDC workload-identity work already completed under FTFL-971/978-981—recommend a 30-minute check before treating its 5 points as real additional work; it could shrink this package.

Why later: Largest package in the view (65 pts) and the two biggest items (569/570, 42 pts combined) are High/Medium priority but not urgent—no active exploit path, just missing observability.

### 11. Contract Testing & Progressive delivery—42 Pts _(all draft)_

Tickets: [FTFL-1012](https://fitfile.atlassian.net/browse/FTFL-1012) (8, consumer-driven contract testing + provider verification) · [FTFL-1013](https://fitfile.atlassian.net/browse/FTFL-1013) (8, contract registry + can_i_deploy gate) · [FTFL-1014](https://fitfile.atlassian.net/browse/FTFL-1014) (13, Istio dark launches + automated canary) · [FTFL-1009](https://fitfile.atlassian.net/browse/FTFL-1009) (13, ephemeral environments per branch)

Why later: Longest horizon and most speculative value of anything in this view—these are capability investments, not fixes for a known-broken thing. Good candidate for "not this quarter" without further discussion, unless Robin has a specific reason to pull one forward. Sits under Robin's "Improve FITFILE Release Process" (Outsource: Yes)—arguably the strongest candidate in this whole note for actually outsourcing, given its low urgency and the specialised Istio/contract-testing expertise it needs.

---

## Needs Scoping before it Can Be Prioritised

[FTFL-884](https://fitfile.atlassian.net/browse/FTFL-884) ("Investigate the needed approach") has no description at all. It can't be sized or valued until someone writes what it's actually for—recommend either scoping it in five minutes in the prioritisation meeting or closing it as stale.

---

## Notes for the Prioritisation Conversation

- The Now tier (42 pts, 12 tickets) is deliberately small and low-risk—everything in it either finishes already-90%-done work or has a completed design/PoC behind it. It's a reasonable "do this regardless of what else gets decided" set.
- Package 6 (identity rollout, 37 pts) is entirely draft-estimated. Before using it in a real capacity plan, it's worth a quick team estimation pass—these numbers are Claude's best guess from ticket titles/descriptions, not a considered estimate.
- Two cross-package dependencies are worth flagging explicitly in the meeting: package 7 needs package-7-internal sequencing (1008 before 1006), and package 8 needs 1004 before 1005. Neither blocks starting the package, just the order within it.
- If Robin wants a single number for "how much identity/security work is left" across his two epics (FTFL-1029 + FTFL-584), that's packages 2 + 5 + 6 + 10 = 132 points—roughly half of everything in this view.
- The outsourcing question is the biggest open variable. Robin's own page tags "Improve FITFILE Release Process"—which covers Packages 1, 3, 4, 7, 8, 9, and 11 (137 of 270 points, just over half this review)—as a candidate for outsourcing. Worth resolving that question early in the prioritisation conversation, since it changes whether these packages are a capacity-planning exercise or a vendor-scoping exercise.
- This review is a fraction of Robin's actual list. 15 of his 17 tracked workstreams (Nginx EOL, Postgres upgrades, Netbird, Firewall, the broader Grafana/alerting estate, multi-zone availability, backup restore testing, business backups, quality checks, node divergence, SSO, Intune, HDRS expertise, plus vulnerability management under FTFL-865) aren't costed anywhere in this note. Treat this as one input to his prioritisation, not the whole picture.

## Source

Board query (reverse-engineered): [FTFL board 281 backlog, filtered to 7 epic parents](https://fitfile.atlassian.net/jira/software/c/projects/FTFL/boards/281/backlog?epics=visible&issueParent=37135%2C37324%2C38034%2C33632%2C37773%2C37774%2C29950)

The `issueParent` param is a comma-separated list of numeric issue IDs (not keys)—Jira board URLs address issues by internal ID, not by key, so the list isn't readable at a glance. Resolved:

| ID | Key | Epic |
|---|---|---|
| 33632 | FTFL-759 | Improve FITFILE Release Process |
| 37135 | FTFL-971 | GitLab Optimisation |
| 37324 | FTFL-1000 | Pipeline Performance & Reliability |
| 38034 | FTFL-1065 | Make GitLab→Argo integration test gating asynchronous |
| 37773 | FTFL-1029 | Entra IAM: Zero Standing Privilege |
| 37774 | FTFL-1030 | Entra IAM as Code |
| 29950 | FTFL-584 | Pentest Actions - Cloud/Entra |

This is a wider view than "the CI/CD sprawl" discussed earlier today—it's whatever Robin (or whoever built this filter) considers one connected pile of infra/security/cost work: CI/CD cost & reliability, Entra identity security, and pentest remediation. ~101 issues total (7 epics + 94 children).

Extracted 2026-09-16 via the Jira API. Story points = `customfield_10028` ("Story Points"), populated inconsistently across the org—see the gaps noted per epic below. Where a points figure below is marked _(draft)_, it was estimated by Claude earlier today, not agreed by the team.

---

## Epic Overview

| Epic | Name | Owner | Priority | Status | Children | Points done | Points open (scored) | Headline issue |
|---|---|---|---|---|---|---|---|---|
| [FTFL-759](https://fitfile.atlassian.net/browse/FTFL-759) | Improve FITFILE Release Process | unassigned | Medium | Selected for Development | 2 | ~3 | unscoped | Mostly superseded by 971/1000; only real content left is FTFL-1025 (done) and an unscoped placeholder |
| [FTFL-971](https://fitfile.atlassian.net/browse/FTFL-971) | GitLab Optimisation _(actually CI/CD security hardening)_ | Leon | Medium | In Progress | 25 | ~54 | 36 | Name doesn't match content—no cost/perf work here |
| [FTFL-1000](https://fitfile.atlassian.net/browse/FTFL-1000) | Pipeline Performance & Reliability | unassigned | Medium | In Progress | 15 | ~6 | 91 | Barely started as a delivery workstream—mostly unscoped research findings |
| [FTFL-1065](https://fitfile.atlassian.net/browse/FTFL-1065) | Async Argo gating (stop blocking runners) | unassigned | High | Backlog | 0 (no subtasks) | 0 | ~10 _(draft)_ | PoC passed, zero subtasks, no parent epic at all |
| [FTFL-1029](https://fitfile.atlassian.net/browse/FTFL-1029) | Entra IAM: Zero Standing Privilege | Robin | High | In Progress | 13 | 0 | 0 scored (13 tickets, zero estimates) | Every single child ticket is unestimated |
| [FTFL-1030](https://fitfile.atlassian.net/browse/FTFL-1030) | Entra IAM as Code | Leon | Medium | In Progress | 11 | ~15 | ~3 (+5 unscored) | Furthest along of the three security epics—mostly done |
| [FTFL-584](https://fitfile.atlassian.net/browse/FTFL-584) | Pentest Actions - Cloud/Entra | Robin | Medium | In Progress | 30 | ~49 | ~71 | Oldest epic (opened April), 26 original pentest findings, still ~9 open |

Known/scored effort across the whole view: ~338 points, of which ~127 done and ~211 still open. That excludes every ticket with no estimate at all—which is most of FTFL-1029 (13/13), a chunk of FTFL-971's Wave 0/1 done items, and several FTFL-584/1030 items—so true remaining effort is higher than 211 suggests. Getting estimates onto FTFL-1029 in particular would meaningfully improve the accuracy of any total Robin sees.

Ownership split worth noting for the rework session: Robin owns FTFL-1029 and FTFL-584 (identity/pentest). Leon owns FTFL-971 and FTFL-1030 (CI/CD security + Entra-as-code). FTFL-1000 and FTFL-1065 are unassigned. The Entra epics (1029/1030) and the pentest epic (584) overlap in subject matter (both touch Azure/Entra hardening) but have different definitions of done and different owners—FTFL-1029's own description explicitly says it was kept separate from FTFL-584 on purpose ("merging them would either drag the pentest deadline or truncate this work to fit it").

---

## FTFL-759—Improve FITFILE Release Process

_Umbrella epic for release-process pain points. No solution ever selected; real work now happens under FTFL-971/FTFL-1000 instead._

| Key | Summary | Type | Status | Priority | Points |
|---|---|---|---|---|---|
| [FTFL-1025](https://fitfile.atlassian.net/browse/FTFL-1025) | Investigate and reduce CI/CD compute-minute usage spike (Renovate backlog) | Task | Ready for test | Medium | 3 |
| [FTFL-884](https://fitfile.atlassian.net/browse/FTFL-884) | Investigate the needed approach | Task | Backlog | Medium |—(no description at all—needs scoping before it can be costed) |

---

## FTFL-971—GitLab Optimisation (CI/CD Security Hardening)

_Secrets protection, OIDC migration off static Azure credentials, scan gates. Wave 0 + Wave 1 done; Wave 2 mostly open._

| Key | Summary | Type | Status | Priority | Points |
|---|---|---|---|---|---|
| [FTFL-1061](https://fitfile.atlassian.net/browse/FTFL-1061) | Migrate sync_argo_app ArgoCD auth off ARGOCD_STAGING_* password | Task | Done | Medium | 5 |
| [FTFL-1059](https://fitfile.atlassian.net/browse/FTFL-1059) | Configure Azure AD federated credential subjects (ude-cli, hutch-cohort-discovery, mesh-mailbox-sandbox) | Task | Closed | Medium | 3 |
| [FTFL-1058](https://fitfile.atlassian.net/browse/FTFL-1058) | Audit projects still using deleted group vars ACR_SERVICE_PRINCIPLE_PASS / AZ_CLIENT_SECRET | Task | Done | High | 5 |
| [FTFL-1057](https://fitfile.atlassian.net/browse/FTFL-1057) | Confirm and protect GCR_PASSWORD / RUNTIME_ACCESS_TOKEN group CI/CD variables | Task | Backlog | Medium | 2 |
| [FTFL-1022](https://fitfile.atlassian.net/browse/FTFL-1022) | Configure Azure AD federated credential for trivy-epss-kev-exporter | Task | Done | High | 1 |
| [FTFL-991](https://fitfile.atlassian.net/browse/FTFL-991) | get_staging_images.sh silently produces empty overrides when image tags are missing | Task | Done | High | 2 |
| [FTFL-990](https://fitfile.atlassian.net/browse/FTFL-990) | Pushgateway/heartbeat endpoint + Prometheus absent() alerting | Task | Backlog | Medium | 8 |
| [FTFL-989](https://fitfile.atlassian.net/browse/FTFL-989) | Positive-control telemetry emitters across named CI controls | Task | Backlog | Medium | 8 |
| [FTFL-988](https://fitfile.atlassian.net/browse/FTFL-988) | InsightFILE BuildKit yarn cache mounts + always-on install_dependencies + pin amd64 | Task | Backlog | Medium | 5 |
| [FTFL-987](https://fitfile.atlassian.net/browse/FTFL-987) | BuildKit registry cache for deployment Argo image builds | Task | Backlog | Medium | 3 |
| [FTFL-986](https://fitfile.atlassian.net/browse/FTFL-986) | Trivy + SAST gate before push (InsightFILE); remove silent audit/sonar fallbacks | Task | Backlog | High | 8 |
| [FTFL-985](https://fitfile.atlassian.net/browse/FTFL-985) | Trivy image scan gate before push (deployment Argo images) | Task | Closed | High | 5 |
| [FTFL-984](https://fitfile.atlassian.net/browse/FTFL-984) | Fix InsightFILE merge-train verification gap and compare_to target | Task | Backlog | High | 2 |
| [FTFL-983](https://fitfile.atlassian.net/browse/FTFL-983) | Add workflow: rules to deployment.gitlab-ci.yml | Task | Closed | Medium | 2 |
| [FTFL-982](https://fitfile.atlassian.net/browse/FTFL-982) | Confirm and correctly configure CI job-token inbound allowlist (InsightFILE ↔ deployment) | Task | Closed | High | 3—_closed with two items explicitly left unresolved in its own last comment; worth a look_ |
| [FTFL-981](https://fitfile.atlassian.net/browse/FTFL-981) | Delete AZ_CLIENT_SECRET / ACR_SERVICE_PRINCIPLE_PASS after OIDC cutover | Task | Done | High | 3 |
| [FTFL-980](https://fitfile.atlassian.net/browse/FTFL-980) | Configure Azure AD federated credential subjects (default branch + MR/train refs) | Task | Done | High | 3 |
| [FTFL-979](https://fitfile.atlassian.net/browse/FTFL-979) | GitLab CI OIDC for Azure in InsightFILE | Task | Closed | Highest | 5—_comment shows this was already implemented before the described fix started_ |
| [FTFL-978](https://fitfile.atlassian.net/browse/FTFL-978) | GitLab CI OIDC for Azure in deployment repo | Task | Done | Highest | 5 |
| [FTFL-977](https://fitfile.atlassian.net/browse/FTFL-977) | Strip leftover debug fallbacks in staging integration-test job | Task | Done | Medium | 1 |
| [FTFL-976](https://fitfile.atlassian.net/browse/FTFL-976) | Protect ARGOCD_STAGING_* group CI/CD variables | Task | Done | High | 3 |
| [FTFL-975](https://fitfile.atlassian.net/browse/FTFL-975) | Enable "pipelines must succeed" on deployment + InsightFILE | Task | Done | High | 3 |
| [FTFL-974](https://fitfile.atlassian.net/browse/FTFL-974) | Rotate ACR service principal credentials (JWT was logged) | Task | Done | Highest | 2 |
| [FTFL-973](https://fitfile.atlassian.net/browse/FTFL-973) | Remove token echo log leak in get_staging_images.sh (InsightFILE) | Task | Closed | Highest | 2 |
| [FTFL-972](https://fitfile.atlassian.net/browse/FTFL-972) | Remove $STAGING_VALUE_OVERRIDES log leak (deployment) | Task | Done | Highest | 1 |

Open (Wave 2) total: ~36 points across 7 tickets (1057, 990, 989, 988, 987, 986, 984).

---

## FTFL-1000—Pipeline Performance & Reliability

_Structural/DORA work: concurrency, trunk-based dev, rollback, contract testing. 3 done, 12 still open—this epic hasn't really started as delivery._

| Key | Summary | Type | Status | Priority | Points |
|---|---|---|---|---|---|
| [FTFL-1014](https://fitfile.atlassian.net/browse/FTFL-1014) | Decouple deploy from release—Istio dark launches + automated canary | Task | Backlog | Low | 13 _(draft)_ |
| [FTFL-1013](https://fitfile.atlassian.net/browse/FTFL-1013) | Contract registry + can_i_deploy deployment gate | Task | Backlog | Medium | 8 _(draft)_ |
| [FTFL-1012](https://fitfile.atlassian.net/browse/FTFL-1012) | Stand up consumer-driven contract testing (CDCT) + mandatory provider verification in CI | Task | Backlog | Medium | 8 _(draft)_ |
| [FTFL-1011](https://fitfile.atlassian.net/browse/FTFL-1011) | Adopt DAG (needs:) YAML architecture for parallel pipeline execution | Task | Done | Medium | 2 _(draft)_ |
| [FTFL-1010](https://fitfile.atlassian.net/browse/FTFL-1010) | Decentralise PR approvals—automated compliance checks + peer review | Task | Backlog | Medium | 8 _(draft)_ |
| [FTFL-1009](https://fitfile.atlassian.net/browse/FTFL-1009) | Ephemeral environments per branch | Task | Backlog | Low | 13 _(draft)_ |
| [FTFL-1008](https://fitfile.atlassian.net/browse/FTFL-1008) | Publish and version Helm charts to ACR | Task | Selected for Development | Medium | 8—_already has real progress (2 phases merged, 1 in an open draft MR) not reflected in its stored status_ |
| [FTFL-1007](https://fitfile.atlassian.net/browse/FTFL-1007) | Move customer-specific config into its own repo(s) | Task | Backlog | Medium | 5 _(draft)_ |
| [FTFL-1006](https://fitfile.atlassian.net/browse/FTFL-1006) | Build rollback procedure for migration-bearing releases | Task | Backlog | High | 8 _(draft)_—flagged in the epic itself as "the single largest untracked MTTR risk" |
| [FTFL-1005](https://fitfile.atlassian.net/browse/FTFL-1005) | Trunk-based dev pilot: one feature, 2-week Lead Time/CFR measurement | Task | Backlog | Medium | 5 _(draft)_ |
| [FTFL-1004](https://fitfile.atlassian.net/browse/FTFL-1004) | Select feature-flag platform and implement Release Toggles | Task | Backlog | Medium | 8 _(draft)_ |
| [FTFL-1003](https://fitfile.atlassian.net/browse/FTFL-1003) | Set resource limits on integration/API test pods | Task | Backlog | Medium | 2 _(draft)_ |
| [FTFL-1002](https://fitfile.atlassian.net/browse/FTFL-1002) | Parameterise integration tests to run in parallel | Task | Backlog | High | 5 _(draft)_—depends on FTFL-1001, which turned out to need no fix (see below) |
| [FTFL-1001](https://fitfile.atlassian.net/browse/FTFL-1001) | Fix merge-train serialization on resource_group: staging lock | Task | Done | High | 2 _(draft)_—no code change was actually needed; already correctly scoped |
| [FTFL-897](https://fitfile.atlassian.net/browse/FTFL-897) | Renovate: merge trains serialise on the shared testing ArgoCD environment | Task | Closed (Abandoned) | Medium | 2 _(draft)_—investigation-only, feeds FTFL-1001 |

Open total: ~91 points across 12 tickets.

---

## FTFL-1065—Async Argo Gating (No Parent Epic)

Standalone—PoC passed, High priority, but zero implementation subtasks exist yet. Full design writeup is on the ticket itself. Draft estimate: ~8–13 points, roughly a week, once broken into real subtasks. Candidate for either its own home or folding under FTFL-1000 as a sibling to FTFL-1006 (both are "runner/pipeline cost + reliability" work).

---

## FTFL-1029—Entra IAM: Zero Standing Privilege (Owned by Robin)

_Remove standing privileged access outside PIM: a JumpCloud sync account with Privileged Role Administrator, an MSP tool (CIPP-SAM) with ~120 Graph permissions including RoleManagement.ReadWrite.Directory, an unconstrained Terraform SP with User Access Administrator at the management-group root, and Global-Admin elevate-access residue. Deliberately separate from FTFL-584 (different definition of done, no fixed deadline)._

None of these 13 tickets have a story-point estimate. Numbering follows a `[EntraIAM-NN]` convention.

| Key | Summary | Type | Status | Priority |
|---|---|---|---|---|
| [FTFL-1031](https://fitfile.atlassian.net/browse/FTFL-1031) | [01] Remove Privileged Role Administrator from JumpCloud Connector | Task | Selected for Development | Highest |
| [FTFL-1032](https://fitfile.atlassian.net/browse/FTFL-1032) | [02] Decide and document CIPP-SAM permission scope | Task | 🚫 Blocked | Highest |
| [FTFL-1033](https://fitfile.atlassian.net/browse/FTFL-1033) | [03] Reduce Application.ReadWrite.All grants across the tenant | Task | Backlog | High |
| [FTFL-1034](https://fitfile.atlassian.net/browse/FTFL-1034) | [04] Constrain or remove privileged Azure RBAC on automation identities | Task | Backlog | High |
| [FTFL-1035](https://fitfile.atlassian.net/browse/FTFL-1035) | [05] Remove User Access Administrator at tenant root scope | Task | Backlog | High |
| [FTFL-1036](https://fitfile.atlassian.net/browse/FTFL-1036) | [06] Confirm or remediate nine standing Owners on NNUHFT-SDE | Task | Closed | High | _(withdrawn—finding was from a customer's own tenant, swept in by mistake; see closing comment)_ |
| [FTFL-1037](https://fitfile.atlassian.net/browse/FTFL-1037) | [07] Migrate engineers from standing Azure Owner to PIM-eligible | Task | Backlog | High |
| [FTFL-1038](https://fitfile.atlassian.net/browse/FTFL-1038) | [08] Second break-glass account and a tested, recorded runbook | Task | Backlog | High |
| [FTFL-1039](https://fitfile.atlassian.net/browse/FTFL-1039) | [09] Leaver cleanup: 39 disabled member accounts and guest review | Task | Backlog | Medium |
| [FTFL-1040](https://fitfile.atlassian.net/browse/FTFL-1040) | [10] Diary the mid-2027 PIM eligibility expiry cliff | Task | Backlog | Medium |
| [FTFL-1041](https://fitfile.atlassian.net/browse/FTFL-1041) | [11] Identify two GUID-named managed identities with Contributor on Production | Task | Backlog | Medium |
| [FTFL-1042](https://fitfile.atlassian.net/browse/FTFL-1042) | [12] Decide Entra ID P2 seat count (blocks PIM extension) | Task | Selected for Development | Highest |
| [FTFL-1043](https://fitfile.atlassian.net/browse/FTFL-1043) | [13] Directory role housekeeping: deprecated role and GA activation review | Task | Backlog | Low |

---

## FTFL-1030—Entra IAM as Code

_Bring Entra config under Terraform so IAM changes go through reviewed MRs. Companion to FTFL-1029 (this epic explicitly excludes standing-privilege reduction). Furthest along of the three security epics—most children already Done._

| Key | Summary | Type | Status | Priority | Points |
|---|---|---|---|---|---|
| [FTFL-1044](https://fitfile.atlassian.net/browse/FTFL-1044) | [20] Unblock identity discovery reads (Graph consent) | Task | Done | Highest | 3 |
| [FTFL-1045](https://fitfile.atlassian.net/browse/FTFL-1045) | [21] Identify which Terraform-managed groups are PIM-managed | Spike | Done | Highest |—|
| [FTFL-1046](https://fitfile.atlassian.net/browse/FTFL-1046) | [22] Terraform overwrites PIM-managed group membership, converting JIT access to standing | Bug | Done | Highest |—|
| [FTFL-1047](https://fitfile.atlassian.net/browse/FTFL-1047) | [23] HCP Terraform to Azure workload identity federation (retire client secret) | Task | Done | High | 3 |
| [FTFL-1048](https://fitfile.atlassian.net/browse/FTFL-1048) | [24] Upgrade azuread provider v2.46→v3.x and azurerm 3.108→4.x | Task | Done | High | 3 |
| [FTFL-1049](https://fitfile.atlassian.net/browse/FTFL-1049) | [25] Split Tier 0 control plane from Tier 1 access plane | Task | Done | High | 3 |
| [FTFL-1050](https://fitfile.atlassian.net/browse/FTFL-1050) | [26] Role-assignable groups and PIM policies as code | Task | Done | Medium | 3 |
| [FTFL-1051](https://fitfile.atlassian.net/browse/FTFL-1051) | [27] Make JumpCloud the user source of truth; remove azuread_user resources | Task | Done | Medium |—|
| [FTFL-1052](https://fitfile.atlassian.net/browse/FTFL-1052) | [28] Dynamic groups for baseline access (removes Terraform churn per joiner) | Task | In Progress | Medium | 3 |
| [FTFL-1053](https://fitfile.atlassian.net/browse/FTFL-1053) | [29] Group naming standard, retire duplicates, import remaining ~95 groups | Task | In Progress | Low |—|
| [FTFL-1054](https://fitfile.atlassian.net/browse/FTFL-1054) | [30] Commit a dated identity and RBAC state snapshot as audit evidence | Task | Done | Medium |—|

Remaining open work: FTFL-1052 + FTFL-1053 (per the epic's own 2026-09-15 comment, these are the only two children still open).

---

## FTFL-584—Pentest Actions - Cloud/Entra (Owned by Robin)

_Original pentest report: 26 findings (2 critical, 10 high, 13 medium, 1 low). Opened April 2026—the oldest epic in this view by five months. Numbering follows `[EntraFF-NN]`. ~9 still open._

| Key | Summary | Type | Status | Priority | Points |
|---|---|---|---|---|---|
| [FTFL-542](https://fitfile.atlassian.net/browse/FTFL-542) | [01] Remove Global Administrator from Tech Ahoy contractor account | Task | Done | Highest |—|
| [FTFL-543](https://fitfile.atlassian.net/browse/FTFL-543) | [05] Fix MFA Conditional Access exclusions across user and service accounts | Task | Done | Highest | 3 |
| [FTFL-545](https://fitfile.atlassian.net/browse/FTFL-545) | [03] Review and update FITFILE Terraform Cloud Provisioner SP permissions | Task | Done | High | 8 |
| [FTFL-546](https://fitfile.atlassian.net/browse/FTFL-546) | [04] Remove User Access Administrator from DevOpsEngineers group | Task | Done | High | 3 |
| [FTFL-547](https://fitfile.atlassian.net/browse/FTFL-547) | [02] Reduce Global Administrator count | Task | Done | High | 5 |
| [FTFL-548](https://fitfile.atlassian.net/browse/FTFL-548) | [02] Enable Privileged Identity Management | Task | Done | Medium | 5 |
| [FTFL-563](https://fitfile.atlassian.net/browse/FTFL-563) | [06] User Consent for Applications Not Restricted | Task | Done | High | 1 |
| [FTFL-564](https://fitfile.atlassian.net/browse/FTFL-564) | [07] Non-Admin Users Can Create Security Groups | Task | Done | High | 1 |
| [FTFL-565](https://fitfile.atlassian.net/browse/FTFL-565) | [08] Non-Admin Users Can Register Applications | Task | Done | High | 1 |
| [FTFL-566](https://fitfile.atlassian.net/browse/FTFL-566) | [09] Non-Admin Users Can Create Tenants | Task | Done | Medium | 1 |
| [FTFL-567](https://fitfile.atlassian.net/browse/FTFL-567) | [10] Guest User Access Not Restricted | Task | Done | Medium |—|
| [FTFL-568](https://fitfile.atlassian.net/browse/FTFL-568) | [11] Guest Invite Restrictions Not Enforced | Task | Done | Medium |—|
| [FTFL-569](https://fitfile.atlassian.net/browse/FTFL-569) | [12] No Diagnostic Settings or Activity Log Export | Task | Selected for Development | High | 21 |
| [FTFL-570](https://fitfile.atlassian.net/browse/FTFL-570) | [13] No Activity Log Alerts Configured (11 Missing) | Task | Selected for Development | Medium | 21 |
| [FTFL-571](https://fitfile.atlassian.net/browse/FTFL-571) | [14] No Application Insights Configured | Task | Done | Low |—|
| [FTFL-572](https://fitfile.atlassian.net/browse/FTFL-572) | [15] Unrestricted Outbound on All NSGs | Task | Backlog | Highest |—|
| [FTFL-573](https://fitfile.atlassian.net/browse/FTFL-573) | [16] AKS NSG Allows Internet Ingress on Port 80 | Task | Closed | Medium | 5 |
| [FTFL-574](https://fitfile.atlassian.net/browse/FTFL-574) | [17] Network Watcher Not Enabled for All Regions | Task | Closed | Medium |—|
| [FTFL-575](https://fitfile.atlassian.net/browse/FTFL-575) | [18] AKS Local Accounts Not Disabled | Task | Ready for review | High | 8 |
| [FTFL-576](https://fitfile.atlassian.net/browse/FTFL-576) | [19] AKS Auto-Upgrade Channel Disabled | Task | Done | Medium | 5 |
| [FTFL-577](https://fitfile.atlassian.net/browse/FTFL-577) | [20] AKS OIDC Issuer Disabled / Workload Identity Not Enabled | Task | Backlog | Highest |——_overlaps conceptually with FTFL-971's OIDC work; worth checking these aren't duplicating effort_ |
| [FTFL-578](https://fitfile.atlassian.net/browse/FTFL-578) | [21] Inconsistent Encryption at Host on AKS Node Pools | Task | Done | Highest |—|
| [FTFL-579](https://fitfile.atlassian.net/browse/FTFL-579) | [22] Jumpbox VM–Password Authentication Enabled | Task | Done | High | 8 |
| [FTFL-580](https://fitfile.atlassian.net/browse/FTFL-580) | [23] Disks Not Encrypted with Customer-Managed Keys (7 Disks) | Task | Selected for Development | Medium | 13 |
| [FTFL-581](https://fitfile.atlassian.net/browse/FTFL-581) | [24] Jumpbox Not Protected by Azure Backup | Task | Closed | Low |—|
| [FTFL-582](https://fitfile.atlassian.net/browse/FTFL-582) | [25] Trusted Launch Disabled on Jumpbox | Task | Done | Medium | 3 |
| [FTFL-583](https://fitfile.atlassian.net/browse/FTFL-583) | [26] 39 App Registrations with Credentials | Task | Selected for Development | Highest | 5 |
| [FTFL-765](https://fitfile.atlassian.net/browse/FTFL-765) | Review App Registrations | Spike | Selected for Development | Medium | 3 |
| [FTFL-810](https://fitfile.atlassian.net/browse/FTFL-810) | Remove all Tech Ahoy Entra accounts | Task | Closed | Medium |—|
| [FTFL-1056](https://fitfile.atlassian.net/browse/FTFL-1056) | [99] Increase log analytics retention | Task | Backlog | Medium |—|

Open total: ~71 points across 9 tickets (569, 570, 572, 575, 577, 580, 583, 765, 1056—last 2 unscored).

---

## Cross-cutting Observations for the Rework Session

1. Epic names don't describe their contents. FTFL-971 ("GitLab Optimisation") is security work, not cost/performance. FTFL-1000's name is accurate but its scope reads more like a research backlog than a plan. If renaming is in scope for a future pass, this is the highest-value fix for stakeholder legibility on its own.
2. FTFL-1065 has no parent epic despite being clearly pipeline-performance/cost work—it doesn't surface under FTFL-1000 at all unless someone knows to look for it by key.
3. Estimate coverage is wildly inconsistent. FTFL-1029 (13 tickets, Robin's, High priority) has zero story points anywhere. FTFL-584's older items are reasonably well-estimated; its newest addition (FTFL-1056) isn't. Any ROI/cost conversation built on Story Points today will systematically under-represent FTFL-1029.
4. Two "closed but not actually resolved" tickets: FTFL-1001 (no fix was needed) and FTFL-982 (closed with two open items still unresolved per its own last comment)—worth a quick look before using their "Done" status as evidence of anything.
5. Possible duplicate/overlapping effort: FTFL-577 ("AKS OIDC Issuer Disabled") in the pentest epic and FTFL-971/978-981's OIDC migration work both touch Azure workload identity federation for AKS/CI—worth confirming these aren't solving the same problem twice under two different epics and owners.
6. Two different owners, same subject matter. Robin owns the Entra/pentest side (FTFL-1029, FTFL-584); Leon owns the CI/CD and Entra-as-code side (FTFL-971, FTFL-1030). FTFL-1029's own description notes it was deliberately kept separate from FTFL-584 to avoid dragging the pentest deadline—that's a documented decision, not an oversight, but worth restating explicitly if epics get reorganised so it isn't re-merged by accident.
7. Highest-value remaining items by priority + points: FTFL-1006 (rollback procedure, called out in FTFL-1000's own text as "the single largest untracked MTTR risk"), FTFL-569/570 (log/alerting gaps, 21 points each, High priority, still Selected not started), and FTFL-1032 (CIPP-SAM permission scope, Highest priority, currently Blocked) stand out as candidates for whatever gets reprioritised first.

---

## Suggested Angle for Reworking into Work Packages

Not prescriptive—for Leon to adapt in the actual rework session:

- Package by outcome, not by epic-of-origin. E.g. "Stop paying for idle CI" (FTFL-1025 follow-ups + FTFL-1065 + FTFL-987/988) vs. "Close the standing-privilege gaps" (FTFL-1029 + the identity-shaped parts of FTFL-584) vs. "Make releases safe to roll back" (FTFL-1006 + FTFL-984).
- Surface the ~211+ points of scored-but-open work plus the ~13 completely unscored FTFL-1029 tickets as one number for Robin, rather than seven separate epic totals—that's the "quickly see cost" view he's asking for.
- FTFL-1032 being Blocked and Highest priority is worth a one-line callout on its own—it's gating FTFL-1029's PIM extension work (FTFL-1042 depends on the P2 seat-count decision, which depends on this).
