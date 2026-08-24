---
author: Claude (read-only investigation)
created: 2026-08-24T12:20:00+01:00
date: 2026-08-24
modified: 2026-08-24T12:20:00+01:00
permalink: llmeon/work/ftfl-865-problem-definition-secure-or-not-looking
related_ticket: FTFL-865
status: Call to action for refinement 13:00, 2026-08-24
tags: [fitfile, ftfl-865, vulnerability-management, problem-definition, call-to-action, trivy, automation, security]
title: FTFL-865 Problem Definition — Secure or Not Looking
---

## FTFL-865 — The problem we are actually solving

Companion to [[FTFL-865 Vulnerability Management — Refinement Brief 2026-08-24]]. That note ranks the work; this one makes the case for why it is worth doing at all.

Published as a shareable page: https://claude.ai/code/artifact/5c7c95f2-2b9e-4e17-b36a-86e4148c76ce

---

### The thesis

> **We cannot tell the difference between "we are secure" and "we are not looking."**

The problem is not that we have 7,399 vulnerabilities. It is not even that we cannot fix them fast enough. It is that **every safety mechanism we own can fail without telling anyone** — and several of them currently are.

A control that reports success while doing nothing is worse than no control at all: it consumes attention *and* manufactures confidence. Our security posture is currently **unfalsifiable**. There is no observation that would tell us we are in trouble, because silence is exactly what a broken control produces.

---

### The exhibit — nine mechanisms, all reporting success while doing nothing

Every one of these was found in the last two weeks. Every one was found by hand. None raised an alarm.

| What it reported | What was actually true |
|---|---|
| Dashboard showing a full set of severity counts | Scan jobs erroring continuously — 3,132 failures across six working days, still failing this morning |
| Tier 0 gate passed: "scan jobs green for 72h" | The check ran over a weekend when the cluster was off. It could only ever have returned zero |
| No alerts firing | The alert sits in `NoData` when healthy — indistinguishable from the log pipeline being broken |
| Terraform apply succeeded | The running pod served the old config for ~1.5h; a ConfigMap change restarts nothing |
| Export CronJob deployed and healthy | Scheduled at 02:17 on a cluster that sleeps at night. Had never fired once |
| Merge requests passing CI | `ude-cli` MRs created no pipeline at all — a Rust `rsa` **security** update merged with zero tests |
| Renovate configured against our private registry | `DOCKER_REGISTRY_PASSWORD` was never set. It has never once authenticated, so no FitFile image or mirrored chart has ever been checked |
| Trivy scanning our images clean | Third-party-repo packages are skipped by design — they do not show as Unknown, they do not appear at all |
| Gates and dashboards keyed on Critical/High | 51% of findings carry no CVSS score, so they are invisible to every control we have designed |

**This is the argument.** Nine, in two weeks, each surfaced only because a person went looking by hand — which is precisely the resource we are trying to stop spending.

---

### Why this framing matters

If our controls were trustworthy, 7,399 findings would be a **capacity problem** — unpleasant, tractable, solvable with a filter.

Because they are not trustworthy, it is an **epistemics problem**: we do not know what the real number is, so we cannot tell whether any work we do is moving it.

That distinction decides how we spend the quarter. A capacity problem is solved by working harder. **An epistemics problem gets worse when you work harder**, because you accumulate confidence that was never earned.

---

### Six problems, one root

1. **Manual remediation does not converge.** Ten days of the whole team's effort moved Critical by eighteen findings (213 → 195). 1,682 sit at High or above. New CVEs arrive faster than hand-triage clears them. There is no headcount at which this closes.
2. **A hand-maintained view of risk is stale on arrival.** This epic's own page asserted the detect layer was repaired for seven days while it failed daily. Nobody was careless — the state changed after the page was written, and nothing tells a document it has become wrong.
3. **Half the estate is invisible to every control we planned.** Unknown = 3,797, larger than Critical + High + Medium + Low combined (3,602). NIST stopped universally scoring CVEs in April 2026, so for most of it a severity is never coming. Every gate and SLA we have specified keys on CVSS tiers.
4. **We only ever find things after they ship.** Zero references to Trivy, Grype, Syft or Cosign in any pipeline in the estate. Every CVE we know about was already running in production when we learned of it.
5. **Even the fixable findings have no automated route.** Renovate covers direct dependencies only, so transitive vulnerabilities appear as Trivy findings with no MR. And it has never been able to read our own private registry. Three VEX statements against 7,399 findings.
6. **The deadline may not be ours to set.** If we are in scope for Cyber Essentials Plus: a mandated 14-day window for anything CVSS 7.0+, against 1,682 findings. DSPT wants a written policy with an approval workflow; DTAC wants a clean annual pen test. Nobody has confirmed whether these apply to us.

---

### The counter-argument, answered

Someone will propose staffing it. Have all three answers ready.

- **It never finishes.** Even at ten times our current remediation rate, arrivals outpace triage. Running to stand still, permanently — and the standing still is invisible because the count barely moves either way.
- **People are the component that fails silently.** All nine failures above were a human reading a signal as evidence when it was not. That is not a training gap: those signals are genuinely ambiguous. Nobody can tell a working scanner from a broken one by looking at a dashboard, because both produce a dashboard.
- **It burns the one resource we actually need.** Judgement is scarce. Spent on enumeration — reading lists, checking counts, deciding whether 3,797 things matter — it is not available for the twenty findings that genuinely need a decision.

---

### The ask

**Build a control system we can trust, then let it do the counting.**

Three commitments. The order is not negotiable: you cannot automate a filter on top of a detector you do not trust, and you cannot trust a detector that cannot prove it ran.

1. **No control ships until it can prove it ran.** Every check emits a positive signal — "I ran, I covered N workloads, here is when" — never merely an absence of errors. Absence of errors is what a dead control produces. This single rule would have caught all nine failures above. → FTFL-938 reopened until it proves itself across working days; FTFL-942 promoted off Low.
2. **Automate the filter before automating the fix.** Get from 7,399 to a number a person can hold in their head. Establish what the unscored half is, then let EPSS and CISA KEV do the bulk filtering — neither needs per-CVE human analysis. The weekly list should be tens, not thousands. → FTFL-954 + FTFL-955, then FTFL-947.
3. **Move detection in front of the merge.** Confirm our pipelines actually run first — a scan gate on a repo whose MRs create no pipeline is decoration. Then ship scanning report-only, so it breaks nothing while building the inventory everything else scopes against. → FTFL-891, then FTFL-856 report-only.

---

### How we will know it worked

- Every control can answer **"when did you last actually run, and over what?"** — and something shouts when the answer gets old.
- The weekly list a person reads is **short enough to act on in ten minutes**, and everything on it is genuinely exploitable.
- New Critical and known-exploited findings are **blocked at merge**, not discovered in production.
- **"Are we getting better?" has a chart**, not an opinion.
- **Nobody's calendar has "check the vulnerability dashboard" on it.**

---

### The line to hold

> **Human judgement is for exceptions, never for enumeration.**

Every hour someone spends counting, checking or confirming is an hour the system should have handed back. We are not asking for time to burn down a backlog. We are asking to build something that can be trusted to tell us the truth without being asked.

---

### Provenance

Severity figures measured live from Prometheus at 10:45 UTC on 2026-08-24: 195 Critical, 1,487 High, 1,496 Medium, 424 Low, 3,797 Unknown — 7,399 total. Scan-job failure counts from Loki over the same estate, cross-checked at two query resolutions.

**Not established:** the root cause of the current scan-job regression, and how much of the finding set is missing while jobs are erroring. Both are the first tasks on the reopened FTFL-938. Every number here should be treated as a floor, not a total.
