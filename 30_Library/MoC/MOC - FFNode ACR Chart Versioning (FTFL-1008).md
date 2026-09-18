---
aliases: [FFNode ACR MOC, ffnode umbrella vs leaf charts, Helm Chart Versioning MOC]
created: 2026-09-17T00:00:00+00:00
modified: 2026-09-17T14:32:58+00:00
permalink: llmeon/30-library/mo-c/moc-ffnode-acr-chart-versioning-ftfl-1008
tags: [acr, argocd, deployment, fitfile, ftfl-1008, helm, moc]
title: MOC - FFNode ACR Chart Versioning (FTFL-1008)
type: map
---

## MOC - FFNode ACR Chart Versioning

> [!abstract] What this consolidates
> Everything current on one question: does `ffnode` ship to ACR as a single umbrella chart, or do its leaf charts publish and version independently? Driven by FTFL-1008 ("Helm charts are not published or versioned in ACR"), unpacked into a real architectural choice by the 2026-08-27 audit.

> Open threads: [[HEAD - Should ffnode ship to ACR as one umbrella chart or as versioned leaf charts?]]

---

### 1. The Open Decision

- [[HEAD - Should ffnode ship to ACR as one umbrella chart or as versioned leaf charts?]]—the live question. Status: `open` as of 2026-09-16.
- Current lean (both the HEAD note and the audit's recommendation converge): leaf charts, kept as an app-of-apps. Convert each child from a git path to a pinned ACR OCI reference; publish `ffnode` itself the same way, last, once children are pinned. Rejected: collapsing into a true umbrella chart with `dependencies:`/`Chart.lock`—it would remove per-component Applications (sync waves, per-app health, per-app rollback) and make every sync all-or-nothing, which is not a trade worth making at the team's current level-2 change-control maturity.
- What would settle it for good: convert one non-prod node to pinned OCI leaf charts and actually perform a rollback under time pressure—see the HEAD note's `## What Would Settle It`.

### 2. Evidence Base (Vault)

- [[2026-08-27-fitfile-helm-chart-acr-publishing-audit]]—the detailed investigation this decision sits on top of: ACR OCI path already live (8 Applications, exact-pinned), `ffnode` is a wrapper not the payload, chart versions frozen while mutable git refs carry the actual changes, four of six customer environments already run ArgoCD multi-source (chart/config split half-built), six broken chart references found.
- [[FITFILE Delivery Pipeline Audit 2026-08-27]]—parent audit; FTFL-1008 sits under epic FTFL-1000 (Pipeline Performance & Reliability).
- [[FITFILE Audit - ACR and Identity]]—two registries not one, the push-path/service-principal privilege question, credential rotation status.
- [[FITFILE Audit - AKS and ArgoCD Topology]]—cluster inventory, ArgoCD Application counts, "nothing is pinned to an immutable revision."
- [[FITFILE Audit - Security Findings and Remediation]]—S-07 (ACR credential expiry), S-13 (no immutable pinning), S-16 (config outside version control)—the findings this decision is meant to close.
- [[HEAD - The Release Candidate Object]]—the immutability / artefact-vs-config-separation properties the umbrella-vs-leaf choice is judged against (umbrella makes them true at node level; leaf only per component).

### 3. Delivery Tracking (Jira)

- [FTFL-1008](https://fitfile.atlassian.net/browse/FTFL-1008)—Publish and version Helm charts to ACR. Selected for Development, actively in progress. Per the 2026-09-11 comment: Phases 0–2 merged (push access confirmed via [!954](https://gitlab.com/fitfile/deployment/-/merge_requests/954), `ffcloud-service:1.0.123` published, `git-auto-package-versioner` updated to bump `Chart.yaml` versions, opt-in/inert by default); Phase 3 (source-from-ACR wiring) is a draft MR ([!955](https://gitlab.com/fitfile/deployment/-/merge_requests/955)); mechanism proven end-to-end on a throwaway Application. `sandbox-testing-1` identified as the correct first real pilot node (staging is shared with InsightFILE's merge-train tests, so unsafe).
- [FTFL-974](https://fitfile.atlassian.net/browse/FTFL-974)—ACR credential rotation. Correction found mid-work: ACR auth is already OIDC/workload-identity—FTFL-974/981 are Done, no rotation needed; the original audit's "credential expires 2026-10-18" blocker did not materialise.
- Related findings from the parent audit: FTFL-975, FTFL-976, FTFL-1015, FTFL-951, FTFL-973, FTFL-877, FTFL-940.
- [FTFL-512](https://fitfile.atlassian.net/browse/FTFL-512)—the CI/CD incident (chart change solo-merged, 8h47m outage) that motivates separating config change from version change.

### 4. Background & Tooling (Confluence)

- [ACR Assets](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2361262084)—inventory of what's already published to ACR (`helm/argocd-apps`, `helm/calico-cloud`, etc).
- [FITFILE ACR Image imports](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2109702152) / [ArgoCD Deployment](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2131230723) / [ingress-nginx](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2131427347)—the `import_chart_to_acr.sh` pattern already proven for third-party charts (mongodb, postgresql, argo-cd, ingress-nginx); the leaf-chart route reuses this exact mechanism for first-party charts.
- [RFC: Transition from Bitnami Helm Charts to an Alternative Source](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2296381442)—why ACR became the target registry in the first place.
- [FITFILE CI/CD Pipeline — Design Document & Improvement Plan](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2865528839)—where `helm lint`/`helm template` for `charts/ffnode` sits in the pipeline's validate stage.

### 5. Explicitly Out of Scope

- The "FFNode Stress Testing" Confluence series (capacity/scalability discovery, Design Documents v1–v4, Proposal & Business Case, Technical Design & Test Specification) is a separate FFNode workstream—performance testing, not chart packaging/versioning. Surfaced by search on "ffnode" but not part of this decision.
- "FFNode Access Control" / "FFNode: Access Control Design" (2022)—access-control architecture for FFNode deployments, unrelated to how charts are versioned or published.

---
