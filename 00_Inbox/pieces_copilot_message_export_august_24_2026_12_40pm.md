---
title: pieces_copilot_message_export_august_24_2026_12_40pm
type: note
permalink: llmeon/00-inbox/pieces-copilot-message-export-august-24-2026-12-40pm
---

*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Monday Aug 24, 2026 - 12:40 PM*
---
## Implementing self-verifying alerts for CI/CD pipelines

This connects directly to work already in flight on your side — `FTFL-942` (currently **High**, promoted off Low on 24 Aug) is explicitly framed in your Jira notes as "the durable fix for that blind spot," and the underlying pattern it needs is the same one used industry-wide for exactly this failure mode: **the dead-man's-switch / heartbeat alert**.

**The specific bug this needs to fix (grounded in your own tickets)**

Your own diagnosis, verbatim from the Claude session transcript on `FTFL-865`:

> "The TrivyImageScanFailed alert sits in NoData when everything is healthy, because the healthy state produces no matching log lines. That's indistinguishable from the log pipeline breaking. Don't read 'no alerts over the weekend' as proof — run the query."

That is the textbook dead-man's-switch failure: a **log-based, absence-triggered alert** cannot distinguish "nothing bad happened" from "the thing that would tell me something bad happened is itself broken." `FTFL-942`'s own description confirms the fix direction: "Currently only log-based alerts exist, and both are broken... Add metric-based alerts for: new Critical appearing, Critical count crossing threshold, scan coverage dropping, reports going stale (>24h age)."

**The general implementation pattern (dead-man's-switch / heartbeat)**

The standard approach, confirmed against current Prometheus/Grafana/Alertmanager practice:

- **A synthetic, always-firing alert rule** — not "alert if X breaks," but "alert if the *proof that X is fine* stops arriving." A minimal Prometheus rule:

```yaml
groups:
- name: watchdog
  rules:
  - alert: Watchdog
    expr: vector(1)
    labels:
      severity: critical
    annotations:
      summary: "Alerting pipeline is broken if this alert stops firing"
```

- **Route it through Alertmanager on a short repeat interval** (commonly 15 minutes), to an external heartbeat receiver:

```yaml
route:
  receiver: dead-mans-switch
  routes:
  - receiver: dead-mans-switch
    match:
      alertname: Watchdog
    repeat_interval: 15m
```

- **An external watchdog service** (e.g. Dead Man's Snitch, or a webhook receiver you own) expects that heartbeat on a schedule and raises *its own* alarm the moment a check-in is missed — meaning the alert path is monitored by something outside the system it's monitoring.
- This is deliberately **separate from your business-metric alerts** (Critical count, coverage, staleness). The watchdog only answers one question: "is the alerting pipeline itself still alive?"

**Mapping this onto your three broken mechanisms**

| Ticket | Current failure mode | Fix shape (per your own scoping) |
|---|---|---|
| `FTFL-938` | Scan jobs fail silently (3,132 log lines over 6 working days, undetected until manual check) | Needs a positive "I ran, I covered N workloads, here is when" signal — not absence-of-error |
| `FTFL-942` | Alert sits in NoData when healthy — indistinguishable from broken | Metric-based alerts on new Critical, threshold crossing, coverage drop, staleness >24h |
| Tier 0 exit gate | "72h green" gate evaluated over a weekend the cluster is off — guaranteed false-positive pass | Rewritten (per today's changelog) to "three consecutive working days at zero," not wall-clock hours |

The commitment already logged in today's Claude session states the underlying principle precisely: **"No control ships until it can prove it ran. Every check must emit a positive signal... never merely an absence of errors. Absence of errors is exactly what a dead control produces."** That's the dead-man's-switch principle stated in your own words before you'd necessarily connected it to the named pattern.

**Concrete next steps, sequenced against what you've already scoped**

1. **`FTFL-942`** — implement the metric-based alerts as scoped (new Critical, threshold crossing, coverage drop, staleness) — these replace the broken log-based ones, not supplement them.
2. **Add a watchdog/heartbeat alert on the scan job itself** — a Prometheus rule that fires only when `trivy_resource_configaudits` (or equivalent coverage metric) *hasn't updated* within an expected window, rather than relying on error-log absence. This is the piece not yet explicitly ticketed — it would sit alongside `FTFL-942` rather than inside it.
3. **`FTFL-938`** — stays reopened until it proves itself across three consecutive working days per the rewritten gate, giving the watchdog something real to validate against.
4. **Coverage staleness (`>24h age`)** already named in `FTFL-942`'s scope covers the archive-export failure mode too — `FTFL-893`'s CronJob "looked correctly deployed all day and would never have fired once," which a staleness-based heartbeat would have caught immediately rather than requiring a manual check.

The common thread across all of this — both in your tickets and in the general pattern — is the same: **an alert that can only tell you "bad" is incomplete; you also need something that tells you "the telling mechanism is alive."** That second signal is what turns "detect-only" into something you can actually trust without a human re-verifying it by hand.