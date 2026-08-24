---
created: 2026-08-24T15:35:00+00:00
modified: 2026-08-24T16:50:00+00:00
permalink: llmeon/30-library/200-projects/pipeline-improvement-synthesis-plan
tags: [cicd, devops, pipeline, SDLC, vulnerability-management]
title: Pipeline Improvement Synthesis Plan
type: project
---

## Pipeline Improvement Synthesis Plan

### Overview

This document synthesizes the various streams of work, audits, and team discussions aimed at transforming the FITFILE CI/CD Pipeline. It aggregates findings from the team's Miro board sessions (Release Process + Vuln Management boards), the DORA-driven [[Pipeline_Improvement_Proposal]], the "Nightmare Pipeline" quality ethos, and the FTFL-865 Vulnerability Management epic — including the 2026-08-24 refinement call with Oliver Rushton, Pavlo Kotov and Weronika Jastrzebska.

The goal is to turn the pipeline into a "purifying gauntlet" — a strict falsification mechanism that acts as the single, automated, and secure path to production, while remaining highly performant and developer-friendly. As of 2026-08-24 the estate is at **detect-only maturity**: we have visibility into problems, no gate that stops them, no automated remediation loop, and — the sharper finding from this week's work — **no reliable way to know whether our controls are even running**.

---

### 1. The Core Philosophy & Goals

- **The "Nightmare" Gauntlet:** code entering the pipeline must be proven ready. The pipeline should aggressively test, lint, and validate to ensure only code of supreme quality reaches production ([[Nightmare pipeline]]).
- **A Falsification Mechanism, not just a build tool:** per [[Pipeline_Improvement_Proposal]], the pipeline's job is to try to prove a change is *unfit* for production. If it survives, we trust it. It must be the **only** automated route to production.
- **DORA Metrics as North Star:** Lead Time for Changes (<1 hour), Deployment Frequency (on-demand), Change Failure Rate (near zero), and MTTR (minutes).
- **Decoupling Deployment from Release:** continuous deployment of technical artefacts, gated for business release by feature flags — not by holding back a merge.
- **Evidence-based improvement (Toyota Kata):** establish baseline → form a hypothesis → run a scoped experiment → measure → adopt or discard. Applies equally to pipeline architecture and to security controls (see §3).
- **A control must prove it ran.** This week's vulnerability-management work surfaced a principle that generalises to the whole pipeline: *absence of an error is not evidence of health.* Every gate, job, and alert should emit a positive signal ("I ran, I covered N things, at time T"), not just silence when nothing goes wrong. See §3.2 for why this matters — it cost the team a fully re-opened epic this week.

---

### 2. Structural & Architectural Improvements

Source: [[fitfile_pipeline_notes]] (Miro: Release Process board) and [[Pipeline_Improvement_Proposal]].

#### A. Solving "Merge Skew" & Big Batches

- **The blocker:** developers wait for a full feature before merging → long-lived branches → conflicts and race conditions when several land at once, because the pipeline validated each in isolation against a now-stale trunk.
- **Trunk-Based Development:** commit to `main` at least daily. Relies on Feature Flags being in place first.
- **Feature Flags:** experimental toggles so incomplete work merges safely without reaching customers. Currently **not visible enough** in the Feature Branch stage — a named problem in the Miro session.
- **Merge Trains / Merged-Results Pipelines:** run CI against the *merged* result, not the source branch, to stop broken-trunk races. Directly addresses the Merge Train stage's own top complaint: **"concurrent pipelines cause race conditions."**

#### B. Pipeline Efficiency & Speed

- **DAG YAML Architecture:** replace rigid stages with `needs:`-based graphs for parallel execution and fail-fast feedback.
- **Build Caching:** dedicated GitLab runners — named as a Quick Win in the Miro session, and the direct fix for two independently-reported problems: no build cache at Merge Train *and* at Staging Release, plus the AMD64-only ACR rebuild bottleneck.
- **Test Parallelism:** parameterise integration tests to run concurrently — removes the single-pipeline-at-a-time bottleneck that the team flagged as a **root, critical problem** (alongside "pipelines are slow", "pipelines are flakey", "builds are slow").

#### C. Testing & Reliability

- **API tests are flakey** and have **low coverage**, alongside Data Pipeline integration tests — named directly in the Merge Train stage.
- **No resource limits on integration test pods** — a likely contributor to the flakiness; test pods competing for cluster resources produce non-deterministic failures that get misread as code defects.
- **No way to pass image version to tests** — tests currently rely on the ArgoCD sync rather than an explicit version, which weakens the mapping between "this pipeline run" and "this artefact under test."
- **Write more tests on the pipeline itself** — a Quick Win from the Miro session; the pipeline's own YAML/scripts are currently untested code running in production.

#### D. Environment & Deployment Management

- **Ephemeral Environments** per branch, to raise testing confidence before merge.
- **Configuration as Code:** move customer-specific config into its own repositories so config-only changes don't require a full release — directly fixes the Customer Release stage's **"config changes require a new release"** problem.
- **Publishing Charts to ACR** with proper versioning — charts are currently not built/versioned there at all.
- **ACR push secret expiry breaks the pipeline** and requires manual intervention — a known Staging Release failure mode with no automated renewal.

#### E. Rollback & MTTR

- **No rollback procedure when a migration is involved** — flagged as a Production Release problem and the single biggest risk to the MTTR DORA metric. A pipeline with fast deploys but no rollback path for stateful changes cannot hit "minutes to restore service."
- **Per-environment config drift:** each environment differs slightly, making the blast-radius of any upgrade hard to assess consistently — compounds rollback risk.
- **No inbound connectivity to private clusters without a bastion** — slows incident response by design; worth weighing against the security benefit when scoping MTTR work.

#### F. Visibility & Process

- **Three disparate ways to deploy** (infra / platform / application) — no single mental model for "how does code get to prod."
- **No SBOM, no release notes** — both are prerequisites for two things this document cares about: supply-chain attestation (§3) and being able to answer "what actually changed" during an incident.
- **Manual, per-customer tagging** with no overview of client state — a scaling risk as customer count grows.
- **Single-owner review gates** drag down Lead Time (per [[Pipeline_Improvement_Proposal]]) — worth pairing with the trunk-based/small-batch work in §2A rather than solving in isolation.

---

### 3. Security & Vulnerability Management — FTFL-865

Epic: [FTFL-865](https://fitfile.atlassian.net/browse/FTFL-865) (In Progress, High, due 31 Aug 2026). Sources: [[FTFL-865 Problem Definition — Secure or Not Looking]], [[FTFL-865 Vulnerability Management — Refinement Brief 2026-08-24]], [[Vulnerability Management Implementation Plan (FTFL-865)]], [[Vulnerability Management Audit - Trivy, VEX, Renovate (Round 1)]].

#### 3.1 The reframed problem

> **We cannot tell the difference between "we are secure" and "we are not looking."**

The issue isn't the size of the backlog (7,399 findings as of 2026-08-24). It's that **every safety mechanism we own can fail silently** — several currently are — and a control that reports success while doing nothing is worse than no control: it consumes attention *and* manufactures false confidence. This is an **epistemics problem**, not a capacity problem, and epistemics problems get *worse* when you throw manual effort at them, because you accumulate confidence that was never earned.

**The exhibit — nine mechanisms found silently failing in two weeks, none raising an alarm:**

| What it reported | What was actually true |
|---|---|
| Dashboard showing full severity counts | Scan jobs erroring continuously — 3,132 failures across six working days |
| Tier 0 gate "scan jobs green for 72h" passed | The check window spanned a weekend when the cluster was off — it could only ever return zero |
| No alerts firing | The alert sits in `NoData` when healthy — indistinguishable from the log pipeline being broken |
| Terraform apply succeeded | The running pod served the old config for ~1.5h; a ConfigMap change restarts nothing |
| Export CronJob "deployed and healthy" | Scheduled at 02:17 on a cluster that sleeps at night — had never fired once |
| Merge requests "passing CI" | `ude-cli` MRs created no pipeline at all — a Rust `rsa` **security** update merged with zero tests |
| Renovate "configured" against our private registry | `DOCKER_REGISTRY_PASSWORD` was never set — it has never once authenticated |
| Trivy "scanning our images clean" | Third-party-repo packages are skipped by design — they don't show as Unknown, they don't appear at all |
| Gates/dashboards keyed on Critical/High | 51% of findings carry no CVSS score, so they're invisible to every control we've designed |

**The operating rule this implies:** every check must emit a positive signal — "I ran, I covered N workloads, here is when" — never merely an absence of errors. This single rule would have caught all nine failures above.

#### 3.2 Live baseline (2026-08-24, ~10:45 UTC, staging cluster)

| Severity | Count | 14 Aug baseline | Change |
|---|---:|---:|---:|
| Critical | 195 | 213 | −18 (−8%) |
| High | 1,487 | 1,731 | −244 (−14%) |
| Medium | 1,496 | 1,774 | −278 |
| Low | 424 | 544 | −120 |
| **Unknown** | **3,797** | 3,779 | **+18 (flat)** |
| **Total** | **7,399** | 8,041 | −642 (−8%) |

Two facts worth carrying into any planning conversation:

1. **Ten days of the whole team's remediation effort moved Critical by 18 findings.** 1,682 findings sit at High or above — there is no plausible headcount at which manual triage closes that gap.
2. **`Unknown` is 51% of the estate — larger than Critical+High+Medium+Low combined.** NIST stopped universally scoring CVEs in April 2026, so for most of this bucket a severity is *never coming*. Every gate and SLA in the epic is currently keyed on CVSS tiers, meaning it is silently undefined for over half the findings. [FTFL-954](https://fitfile.atlassian.net/browse/FTFL-954) (characterise the Unknown bucket) is the cheapest way to de-risk everything downstream.

**Active regression (found 2026-08-24, not yet root-caused):** [FTFL-938](https://fitfile.atlassian.net/browse/FTFL-938) — the VEX-metadata `EOF` failure killing scan jobs — was closed Done on 17 Aug but has recurred every working day since (~3,100 log lines, 285 today alone). It was closed on a weekend-window Loki query that could only ever return zero, because the staging cluster is off Fri 20:00–Mon 06:00. **Do not re-apply a fourth patch** — the epic's own instruction is that recurrence means the working theory is incomplete and needs reopening properly.

#### 3.3 Payoff-ordered plan

From [[Vulnerability Management Implementation Plan (FTFL-865)]], calibrated against real effort (FTFL-855's estimate was off by a day plus an incident — treat all effort bands as approximate).

**Tier 0 — Restore the skeleton (nothing below works without it)**

| # | Action | Ticket | Effort |
|---|---|---|---|
| 0.1 | Fix the VEX metadata EOF failure killing scan jobs | [FTFL-938](https://fitfile.atlassian.net/browse/FTFL-938) (reopened) | 0.5–2 d |
| 0.2 | Fix `TrivyImageScanFailed` alert to match real log output | [FTFL-939](https://fitfile.atlassian.net/browse/FTFL-939) | 2 h |
| 0.3 | Durable report retention beyond 24h TTL | [FTFL-893](https://fitfile.atlassian.net/browse/FTFL-893) | 2–4 d |
| 0.4 | Validation CI on `vex-repository` (single point of failure for every scan job) | [FTFL-940](https://fitfile.atlassian.net/browse/FTFL-940) | 1 d |

**Gate:** scan jobs green for 72h *measured on a live-cluster window, not a weekend*, plus coverage stable at ~90 workloads, before Tier 1 starts.

**Tier 1 — Highest payoff per unit effort**

| # | Action | Ticket | Why |
|---|---|---|---|
| 1.1 | CI scan gate, **report-only first** (`--exit-code 0`, JSON artefact) | [FTFL-856](https://fitfile.atlassian.net/browse/FTFL-856) | Zero CI scanning exists estate-wide; report-only ships into an uncleared backlog without breaking every pipeline, and produces the durable inventory other tickets need |
| 1.2 | EPSS + CISA KEV prioritisation | [FTFL-947](https://fitfile.atlassian.net/browse/FTFL-947) | Best noise-reduction available; cuts an actionable list by an order of magnitude with no per-CVE human analysis |
| 1.3 | Confirm CI actually runs on every repo in scope | [FTFL-891](https://fitfile.atlassian.net/browse/FTFL-891) | A gate is decoration on a repo whose MRs create no pipeline (true of `ude-cli` until 13 Aug) |
| 1.4 | Renovate `vulnerabilityAlerts` nesting fix | [FTFL-894](https://fitfile.atlassian.net/browse/FTFL-894) | Root-level `packageRules` can't constrain security updates — Renovate's `force` object overrides them |
| 1.5 | Transitive dependency overrides | [FTFL-895](https://fitfile.atlassian.net/browse/FTFL-895) | Hard prerequisite before 1.1 goes blocking, or transitive-only findings become unfixable build failures |
| 1.6 | Fix dashboard's 3 dead metric rows + threshold calibration | [FTFL-941](https://fitfile.atlassian.net/browse/FTFL-941) | `configaudits`/`rbacassessments`/`exposedsecrets` show zero series despite chart defaults being on |
| 1.7 | Metric-based alerts (new Critical, coverage drop, staleness) | [FTFL-942](https://fitfile.atlassian.net/browse/FTFL-942) | Nothing currently alerts on the vulnerabilities themselves, only on log strings |

**Tier 2 — Structural, higher effort, still worth it**

| # | Action | Ticket | Notes |
|---|---|---|---|
| 2.1 | **Base-image minimisation** (distroless/Chainguard) | [FTFL-863](https://fitfile.atlassian.net/browse/FTFL-863) | Ranked *above* the source report's own Tier 3 — it's the only lever that reduces the CVE count rather than reclassifying it (>80% reduction observed). Pilot on `ff-test-a` (102 Criticals) or `ohdsi` (60) |
| 2.2 | Flip the CI gate to blocking | FTFL-856 (part 2) | Only once the inventory is clear enough not to go permanently red; needs 1.2 + 1.5 landed |
| 2.3 | Severity-tier recording rules | [FTFL-860](https://fitfile.atlassian.net/browse/FTFL-860) | Keep `metricsVulnIdEnabled` on; do before multi-cluster rollout (9,547 series → 30k+) |
| 2.4 | GitOps for security tooling + Helm-values drift lockdown | [FTFL-858](https://fitfile.atlassian.net/browse/FTFL-858), [FTFL-862](https://fitfile.atlassian.net/browse/FTFL-862) | Real fix is *who has write access outside GitOps*, not a values-file tool |
| 2.5 | Extend trivy-operator to testing, then production | [FTFL-945](https://fitfile.atlassian.net/browse/FTFL-945) | Production is currently entirely unscanned |
| 2.6 | Cosign image signing + attestation in CI | [FTFL-861](https://fitfile.atlassian.net/browse/FTFL-861) | Genuinely useful; sequence after Tier 1 — signing images whose contents we can't yet reason about is backwards |
| 2.7 | Automated remediation loop (Trivy findings → Renovate/issue) | [FTFL-857](https://fitfile.atlassian.net/browse/FTFL-857) | Needs 0.3 and 1.5 first, or it generates unactionable tickets |

**Tier 3 — Deferred / re-scoped / explicitly rejected**

| Idea | Verdict |
|---|---|
| Gatekeeper phased enforcement ([FTFL-859](https://fitfile.atlassian.net/browse/FTFL-859)) | Re-scope first — it's Azure Policy for AKS, not standalone Gatekeeper; hand-written ConstraintTemplates get reconciled away |
| OWASP Dependency-Track | Defer — needs CI-generated SBOMs we don't yet produce |
| Policy Reporter UI | Skip — duplicates the Grafana dashboard once §1.6 lands |
| Grype as second scanner ([FTFL-864](https://fitfile.atlassian.net/browse/FTFL-864)) | Defer — can't reliably operate the one scanner we have yet |
| Snyk / Wiz / JFrog Xray | No — cost/weight not justified at current team size |
| `additionalVulnerabilityReportFields` | Defer to whatever consumes it — grows etcd objects with no current reader |
| SLSA L3 / Ratify / in-toto provenance | Far future — realistic ambition is SLSA 2–3; we're not at 1 |
| `.trivyignore.yaml` with `expired_at` | Adopt opportunistically alongside 1.1 — cheaper than VEX for local, time-boxed suppressions |

#### 3.4 Refinement call outcome — 2026-08-24, 13:00

Attendees: Leon Ormes, Oliver Rushton, Pavlo Kotov, Weronika Jastrzebska.

- **Moved into this sprint (Selected for Development):** FTFL-858, FTFL-857, FTFL-956 (priority Medium → High), FTFL-864 (Lowest → Medium), FTFL-863, FTFL-893.
- **New tickets raised, parented to FTFL-865:** FTFL-966 (reachability spike), FTFL-967 (upstream-won't-fix suppression policy), FTFL-968 (compliance scope owner), FTFL-969 (trivy-system footprint / cost).
- **FTFL-938 reopened** in the call; **FTFL-942 promoted off Low** given the "no signal read as health" pattern has now cost a full week three separate times (Terraform apply, CronJob, this alert).
- **FTFL-863 (distroless/Chainguard)** explicitly agreed as an *opportunistic, scoped pilot* rather than a full migration — effort: opportunistic; impact: improves detection coverage on highest-risk images without the operational overhead of a fleet-wide second scanner. (Sourced against "Trivy vs Grype 2026 Buyer Comparison" and "Container Security Scanning in 2026.")

#### 3.5 The compliance driver — flag it, don't solve it

Unresolved: **is FitFile in scope for NHS DSPT / DTAC / Cyber Essentials Plus** as an IT supplier? This is a question for whoever holds the data-processing agreements, not something platform work resolves — but it reorders the whole quarter if the answer is yes:

- **CE+ (from April 2026):** mandates a 14-day remediation window for anything CVSS ≥7.0. We have 1,682 findings at that level today — manual triage cannot clear that inside 14 days by any means. Promotes FTFL-895, FTFL-863, FTFL-857 from "worth doing" to load-bearing.
- **DSPT:** requires a *written* vulnerability-management policy with an exception-approval workflow — a document, not automation. We currently have automation and no document.
- **DTAC:** requires an annual external penetration test showing nothing at CVSS ≥7.0 — nothing in this plan provides that.

**Action:** name an owner for the scope question before it silently gates the rest of the platform work.

---

### 4. Best-Practice Alignment

Mapping the above against recognised frameworks, so gaps are named against an external standard rather than internal opinion.

| Framework | What it asks for | Where we stand |
|---|---|---|
| **DORA / *Accelerate*** (Forsgren, Humble, Kim) | Trunk-based dev, CI, deployment automation, loosely-coupled architecture, monitoring & observability, as the drivers of the four keys | Baseline not yet instrumented (§1); trunk-based dev blocked on feature flags (§2A); monitoring exists but has proven it can lie (§3.1) |
| **Continuous Delivery** (Humble & Farley) | The deployment pipeline is the *only* route to production, and its job is to falsify releasability | Three disparate deploy paths currently exist (§2F) — violates the "only route" principle directly |
| **OWASP DevSecOps Maturity Model** | Security shifts left through the pipeline stages, not bolted on at the end | Zero CI scanning estate-wide today (§3.3, Tier 1); this document's own plan is the shift-left move |
| **NIST SSDF / SLSA** (supply-chain integrity) | Provenance, signed artefacts, SBOM, verified builds | No SBOM generated in CI (§2F); Cosign signing scoped but deliberately sequenced after detection is trustworthy (§3.3, 2.6); realistic target is SLSA 1→2, not L3 |
| **Toyota Improvement Kata** | Hypothesis-driven, measured experiments over top-down mandates | Explicitly adopted in [[Pipeline_Improvement_Proposal]] §3; the FTFL-865 reframing (§3.1) is this pattern applied to security |
| **Dead-man's-switch / positive-signal monitoring** (SRE practice) | A healthy system announces itself; the alarm is silence *changing*, not the default state | Directly the gap found this week (§3.1) — `NoData` currently means both "healthy" and "broken" |

---

### 5. Prioritised Roadmap

Sequenced by dependency and payoff, merging the pipeline structural work with the FTFL-865 tiers. Effort bands are approximate.

1. **Now — Tier 0 (security skeleton):** reopen FTFL-938 properly (root cause, not a fourth patch), fix the alert that should have caught it (FTFL-939), durable retention (FTFL-893), VEX repo validation CI (FTFL-940). *Nothing in vulnerability management is trustworthy until this gates green on a live-cluster window.*
2. **Now — parallel, independent of Tier 0:** instrument DORA baseline metrics; characterise the Unknown vulnerability bucket (FTFL-954/955) against the already-banked archive — no cluster access needed, de-risks everything downstream.
3. **Next — pipeline quick wins:** dedicated GitLab runners for build cache; parameterise integration tests for parallelism; publish charts to ACR with versioning; move customer config to its own repos.
4. **Next — Tier 1 security:** audit CI coverage across all repos (FTFL-891) *before* flipping any gate; ship the CI scan gate report-only (FTFL-856, `--exit-code 0`); EPSS/KEV prioritisation (FTFL-947, after Unknown is characterised); fix Renovate's `vulnerabilityAlerts` nesting (FTFL-894).
5. **Next — one trunk-based-dev experiment:** pick one upcoming feature, add a feature flag, and measure Lead Time / Change Failure Rate against baseline for two weeks (Kata-style, per §1 and §4).
6. **Later — Tier 2 security + structural pipeline work:** distroless pilot on highest-CVE service (FTFL-863); flip the CI gate to blocking once inventory is clear (FTFL-856 part 2); Cosign signing (FTFL-861); merge trains; ephemeral environments; GitOps lockdown for security tooling.
7. **Ongoing:** name an owner for the NHS DSPT/DTAC/CE+ scope question — its answer changes the priority order of steps 4 and 6 materially, so don't let it sit unowned.
8. **Ongoing:** build a rollback procedure for migration-bearing releases — currently the single largest MTTR risk and not yet on any tier above.

---

### 6. Open Threads

Carried forward from source notes — none of these are established yet, and none should be silently assumed either way:

- Root cause of the FTFL-938 EOF regression — not yet found; the local infra repo clone was behind master at time of investigation.
- Does trivy-operator support `--epss`/`--kev` natively, or is EPSS/KEV CLI-only? Determines whether FTFL-947 rides on the operator or on the CI gate (FTFL-856).
- Why do `trivy_resource_configaudits` / `trivy_role_rbacassessments` / `trivy_image_exposedsecrets` show zero series despite chart defaults enabling them — likely the same root cause as the scan-job failures, but unverified.
- What does Kubescape actually cover, and does it overlap trivy-operator enough to retire one?
- NHS DSPT/DTAC/CE+ applicability — owner not yet named (§3.5).

---

### Related

- [[Pipeline Best Practices Research Prompt]] — deep-research prompt built from this document, for sourcing external best-practice recommendations
- [[fitfile_pipeline_notes]] — Miro Release Process board, raw notes
- [[Pipeline_Improvement_Proposal]] — DORA-driven proposal and Kata methodology
- [[Nightmare pipeline]] — quality ethos
- [[FTFL-865 Problem Definition — Secure or Not Looking]] — the epistemics argument
- [[FTFL-865 Vulnerability Management — Refinement Brief 2026-08-24]] — ROI ranking and call outcome
- [[Vulnerability Management Implementation Plan (FTFL-865)]] — payoff-ordered tickets
- [[Vulnerability Management Audit - Trivy, VEX, Renovate (Round 1)]] — current-state audit
- Epic: [FTFL-865](https://fitfile.atlassian.net/browse/FTFL-865)
