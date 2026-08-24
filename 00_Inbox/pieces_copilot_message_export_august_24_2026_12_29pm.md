---
title: pieces_copilot_message_export_august_24_2026_12_29pm
type: note
permalink: llmeon/00-inbox/pieces-copilot-message-export-august-24-2026-12-29pm
---

*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Monday Aug 24, 2026 - 12:29 PM*
---
A note on process: `browser_lookup` isn't available as a tool on this session's leased toolkit — only `search_memory`, `ask_memory`, and `web_search` were provided. However, `search_memory` already surfaced the actual rendered Jira page content for FTFL-865 multiple times (August 7 through August 24), including the live description, Definition of Done, and changelog verbatim — this is direct ground-truth on the ticket, just retrieved via the LTM's captured browser snapshots rather than a live re-fetch. That's sufficient grounding to proceed.

## Problem definition: FTFL-865 — Vulnerability Management

**The literal ticket state, for reference**

[FTFL-865: Vulnerability Management](https://fitfile.atlassian.net/browse/FTFL-865) — reporter Leon Ormes, priority High, due 31 Aug 2026. Current baseline as of the 2026-08-24 changelog: **195 Critical / 1,487 High / 3,797 Unknown / 7,399 total** flagged vulnerabilities across the estate. The epic exists because the program sits at "detect-only" maturity — no shift-left scanning gate, no automated remediation loop, no supply-chain integrity controls, and Gatekeeper installed but only in audit/dry-run mode.

**Why "7,399 vulnerabilities" is the wrong headline**

Your instinct is correct, but the evidence in your own workstream points to something sharper than "we have a lot of CVEs" or even "we can't fix them fast enough." A Claude session transcript from today (24 Aug) captures the problem definition you'd already arrived at independently, and it's worth quoting verbatim because it's the strongest version of the argument in your own memory:

> "We cannot tell secure from not looking. The problem is not that we have 7,399 vulnerabilities. It is not even that we cannot fix them fast enough. It is that every safety mechanism we own can fail without telling anyone — and several of them currently are. A control that reports success while doing nothing is worse than no control at all. It consumes attention and manufactures confidence."

That statement is backed by hard evidence sitting in the same ticket's changelog, not just rhetoric:

- **Nine separate control mechanisms found reporting success while doing nothing** — all nine found by manual inspection, none raised an alarm.
- `FTFL-938` (the detect layer) was marked repaired on 14 Aug, held for ~5h40m, then silently failed again from **05:10:16 UTC on 17 Aug**, and has failed every working day since — undetected until someone went and looked.
- The Tier 0 exit gate ("72h green scan run") **could not have been mechanically satisfied as written** — it measured a 72-hour window over a weekend on a cluster that's switched off Fri 20:00–Mon 06:00 UTC. The gate was passing on a technicality, not on reality.
- `FTFL-942`'s log-based alert sits in **Nodata when healthy** — meaning the alerting system itself can't distinguish "everything is fine" from "the alert pipeline is broken."

**The fundamental problem, stated as a call to action**

> FitFile's vulnerability management program cannot currently distinguish between "we are secure" and "we have stopped looking." Every layer of this system — detection, gating, alerting, exception tracking — is presently unfalsifiable: a broken control and a healthy one produce the *same silence*. Nine controls have already been caught doing exactly this, all found by hand, none raised automatically. As long as humans are the only mechanism verifying the mechanisms, the estate's actual risk posture is unknowable at any given moment, not just slow to fix.

This reframes your two instincts correctly:

- **"We need to automate as much as possible, and trust it"** — true, but the current gap isn't a lack of automation per se (Trivy, Renovate, and Gatekeeper already exist); it's that none of the automation is *self-verifying*. Trust requires the system to alert on its own failure, not just on the CVEs it finds. The Definition of Done already encodes this correctly: "Trivy scan jobs running reliably, **with an alert that actually fires when they don't**" — that's the trust mechanism, not the scan itself.
- **"It changes too fast for humans to maintain a constant view"** — also true, and evidenced directly: the estate produced five new Renovate-driven CVE remediation MRs in the last two weeks alone (`postcss` [4 CVEs](https://gitlab.com/fitfile/apps/InsightFILE/-/merge_requests/2416), `cryptography` [5 CVEs](https://gitlab.com/fitfile/data-and-analytics/-/merge_requests/644), `pyarrow`, `black` [2 CVEs]) — a volume and cadence no person can track by dashboard-checking. But the deeper failure mode isn't volume, it's that the *tracking mechanism itself* degrades silently under that same rate of change (the scan-job failures, the Nodata alert) — so the system erodes exactly where you'd need it to hold steady.

**Compelling problems beyond your framing, worth including in the definition**

- **Prioritization is currently severity-only, not risk-based.** `FTFL-947` (EPSS + CISA KEV prioritization) exists precisely because raw Critical/High counts don't reflect actual exploitability — industry research reinforces this is a common failure mode: teams burn effort on high-CVSS/low-exploitability findings while KEV-listed actively-exploited CVEs go untriaged in the same queue ([Deloitte, "Vulnerability management in the AI era"](https://www2.deloitte.com); [LinkedIn, "The Many Problems of Vulnerability Management"](https://linkedin.com)).
- **No CI-stage gate means every fix is post-deploy cleanup, not prevention.** The grep across every `gitlab-ci.yml` in `Application/` and `Deployment/deployment/` confirmed zero references to Trivy, Grype, Syft, or Cosign in any pipeline — meaning today's "detection" happens only after code is already running in production. This is the shift-left gap the epic names directly.
- **Supply-chain trust is itself compromised, not just theoretical.** The epic is explicitly also driven by the March 2026 Trivy supply-chain compromise (`CVE-2026-33634`) — meaning the scanning tool itself has already demonstrated it can be the vector, not just the shield. Image signing (Cosign) and SBOM/provenance attestation in the DoD address this, but neither is live yet.
- **Automation-without-context risk (the flip side of your "trust automation" point).** External research is consistent on this: automated scanners without environment/business-impact context can misprioritize or produce false confidence just as easily as absent humans can miss things — the fix isn't "trust blindly," it's "automate discovery + enrichment, keep human judgment for ambiguous/high-impact exceptions," which is exactly what the DoD's "documented, time-boxed exception process with a named owner" line is trying to operationalize.

**One open structural risk not yet resolved in the ticket**

The changelog flags — and explicitly declines to resolve — whether FitFile is in scope for **NHS DSPT/DTAC/Cyber Essentials Plus** as an IT supplier. That's a compliance-exposure question sitting adjacent to this technical epic, and the ticket itself notes it needs validation against actual data-processing agreements, not inferred from infrastructure naming. Worth surfacing to whoever owns those agreements alongside this problem definition, since a credible "we cannot verify our own security posture" statement has direct bearing on that certification conversation.