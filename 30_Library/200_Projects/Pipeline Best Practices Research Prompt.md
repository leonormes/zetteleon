---
created: 2026-08-24T17:00:00+00:00
modified: 2026-08-24T15:48:28+00:00
permalink: llmeon/30-library/200-projects/pipeline-best-practices-research-prompt
title: Pipeline Best Practices Research Prompt
type: note
tags: [cicd, devops, pipeline, vulnerability-management, research-prompt]
---

# Research Brief: Building a Best-Practice CI/CD Pipeline for FitFile

## Who you're advising

FitFile is a small platform engineering team (single-digit reviewers, one release
manager) running a GitLab-based CI/CD pipeline for a set of application and data
services on AKS, deployed via ArgoCD and Terraform Cloud. Among the workloads is
an OHDSI-based health data pipeline, which puts FitFile in scope (unconfirmed) for
UK NHS supplier security frameworks — DSPT, DTAC, and Cyber Essentials Plus. Treat
this as a real engineering organisation, not a greenfield exercise: every
recommendation needs to work for a team this size, not just a FAANG-scale org.

## Current state (verified, not aspirational)

**Pipeline architecture today:**
- Stage-by-stage GitLab pipeline (not a DAG); Local Dev → Feature Branch → Merge
  Train → Staging Release → Production Release → Customer Release.
- No trunk-based development — long-lived feature branches are the norm, causing
  "merge skew": branches conflict/break when finally merged because they were
  tested in isolation against a now-stale trunk.
- Feature flags exist but aren't consistently used or visible.
- One concurrent pipeline at a time; no build cache anywhere; all ACR builds are
  AMD64-only, forcing rebuilds; frontend-only pipeline takes ~19 minutes.
- API and data-pipeline integration tests are flaky, low coverage, run without
  resource limits on their pods, and can't be pointed at a specific image version
  (tests rely on the ArgoCD sync state instead).
- Three disparate ways to deploy (infra / platform / application) with no unified
  model.
- No SBOM, no release notes, no rollback procedure for migration-bearing
  production releases.
- Single-owner PR approval gate is a queueing bottleneck.
- Per-customer deployment is manually tagged with no fleet-wide visibility;
  customer-specific config changes currently require a full release.

**Security / vulnerability management today (the sharper finding):**
- Zero CI-stage vulnerability scanning anywhere in the estate — detection only
  happens post-deploy, in-cluster, via trivy-operator.
- 7,399 open findings (195 Critical, 1,487 High, 1,496 Medium, 424 Low, 3,797
  Unknown/unscored). Ten engineer-days of manual remediation moved Critical by 18
  findings — manual triage provably does not converge against this volume.
- 51% of findings carry no CVSS score at all (NIST stopped universal CVE scoring
  in April 2026) and every planned gate/SLA is currently keyed on CVSS tiers —
  meaning it's undefined behaviour for over half the backlog.
- Renovate has never successfully authenticated to the private registry
  (credential was never set), so no FitFile-built image has ever had automated
  dependency remediation.
- A recurring, still-unexplained scan-job failure (VEX metadata parse error) was
  marked "fixed" against a 72-hour health check that spanned a weekend when the
  cluster is powered off — the check could only ever return a false positive.
- Nine separate control-failure incidents were found by hand in the last two
  weeks (a Terraform apply that "succeeded" without restarting the affected pod;
  a CronJob scheduled for a time the cluster is asleep; an alert that reads
  identically whether the system is healthy or the monitoring pipeline itself is
  broken; a merge request that ran zero tests because GitLab doesn't set
  `$CI_COMMIT_BRANCH` on MR pipelines; etc.). None of the nine tripped any alert.
  The working principle this produced: **every control must emit a positive
  "I ran, over N things, at time T" signal — absence of an error is not evidence
  of health.**
- Gatekeeper is deployed as Azure Policy for AKS, not a standalone install, which
  invalidates most generic "add a ConstraintTemplate" admission-control guidance.

## What I already have — don't re-derive this

I already have an internal synthesis document covering: a payoff-ordered
implementation plan (Tier 0 "restore the detection skeleton" → Tier 1 CI scan
gate + EPSS/KEV prioritisation → Tier 2 base-image minimisation, Cosign signing,
GitOps lockdown → Tier 3 deferred items like Dependency-Track and SLSA L3), a
DORA-metrics baseline goal, and a rough mapping to *Accelerate*, *Continuous
Delivery*, the OWASP DevSecOps Maturity Model, NIST SSDF/SLSA, and Toyota Kata.
I don't need you to re-explain what DORA's four keys are or summarise these
frameworks in the abstract — I need you to **apply them to this specific
situation** and tell me what I'm getting wrong, missing, or under-weighting.

## What I want from you

Do deep research across the best available industry sources — books,
canonical papers, and high-quality practitioner content, e.g.:

- *Accelerate* (Forsgren, Humble, Kim) and the underlying DORA research /
  State of DevOps reports — especially the 24 capabilities model, not just the
  four keys
- *Continuous Delivery* (Humble & Farley) — deployment pipeline as the sole path
  to production, environment/config management, release vs. deployment
- *The DevOps Handbook* (Kim, Debois, Humble, Willis)
- *Site Reliability Engineering* and *The Site Reliability Workbook* (Google) —
  especially on monitoring philosophy, error budgets, and alerting design
- *Building Secure & Reliable Systems* (Google)
- *Team Topologies* (Skelton & Pais) — team-shape implications for a
  single-reviewer bottleneck and platform-vs-stream-aligned team boundaries
- Trunk-Based Development literature (trunkbaseddevelopment.com, Paul Hammant)
  and feature-flag practice guides (Pete Hodgson / Martin Fowler on feature
  toggles) for teams that haven't done this before
- SLSA framework documentation, in-toto, and sigstore/Cosign guidance, for
  realistic incremental supply-chain security (we're targeting SLSA 1→2, not 3)
- NIST SSDF and the OWASP DevSecOps Maturity Model, applied to a detect-only
  estate moving to shift-left
- EPSS and CISA KEV documentation/best practice for vulnerability
  prioritisation at scale, as an alternative to CVSS-only triage
- Toyota Kata (Rother) as applied to engineering process change, if you have
  good secondary sources on this in a software context

## Specific questions to answer

1. **Sequencing challenge.** Given a team this size can't do everything at once,
   what does the literature say should come first: fixing pipeline speed/
   reliability (merge trains, build cache, trunk-based dev), or fixing the
   security detection layer? Are these genuinely independent, or does one
   materially de-risk the other in a way I'm not seeing?
2. **The "control must prove it ran" principle.** Is this a recognised pattern
   (dead-man's-switch monitoring, synthetic checks, heartbeat monitoring) with
   established implementation guidance? What's the SRE-literature-grade way to
   design alerting so silence-as-health failure modes like the nine we found
   can't recur — and where does this pattern have known failure modes of its
   own (alert fatigue, false positive heartbeats)?
3. **Trunk-based dev without existing feature-flag discipline.** What's the
   realistic adoption path (per Fowler/Hodgson and *Accelerate*) for a team
   that has flags but doesn't consistently use them — what's the first
   experiment to run, and what commonly goes wrong in month one?
4. **CVSS-blind vulnerability triage.** With 51% of findings unscored, is
   EPSS+KEV-first triage (deprioritising raw CVSS) actually the industry-
   recommended approach at our scale, or is there a better-regarded alternative
   (e.g., reachability analysis, exploit-maturity scoring, risk-based
   frameworks like FAIR) we should be considering instead or in addition?
5. **Report-only gates.** Is shipping a CI security gate in `--exit-code 0`
   report-only mode before flipping it to blocking a widely-endorsed pattern,
   or does the literature warn this tends to never get flipped on? What
   conditions/triggers does good practice suggest for the flip?
6. **Rollback for migration-bearing releases.** What do *Continuous Delivery*
   and modern practice recommend for teams that can't yet do zero-downtime
   expand/contract migrations everywhere — is there a credible middle ground
   short of full blue/green + migration choreography?
7. **What am I not asking about?** Given everything above, what's a
   well-regarded practice (progressive delivery/canary releases, chaos
   engineering, policy-as-code, DORA's "loosely coupled architecture"
   capability, database change management, incident review practice, etc.)
   that this brief doesn't mention but that the sources above would flag as a
   gap?

## Output format

For each recommendation:
- **The recommendation**, stated concretely enough to turn into a ticket.
- **Source**, with enough specificity to go re-read the original (book +
  chapter/concept, not just an author name).
- **Why it applies here**, tying it to a specific fact from "Current state"
  above — not generic advice.
- **Where it might be wrong for us**, given our team size, stack, or the
  compliance uncertainty (NHS DSPT/DTAC/CE+ scope not yet confirmed).

Group recommendations into: **Do next (0–2 weeks)**, **Do this quarter**,
**Structural / long-horizon**. Flag anywhere your sources genuinely disagree
with each other (e.g., the internal report I already have found two of its own
source documents contradicting each other on whether to enable a metrics flag —
I want to know if that kind of tension shows up in canonical sources too, not
just internal ones).