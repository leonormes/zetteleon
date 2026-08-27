---
created: 2026-08-27T10:30:00+00:00
modified: 2026-08-27T10:30:00+00:00
permalink: llmeon/30-library/200-projects/fitfile-delivery-pipeline-audit-2026-08-27
project_category: refined_deployment
project_name: Pipeline
project_status: active
classification: Platform / DevOps audit — read-only
date: 2026-08-27
related_tickets: [FTFL-973, FTFL-974, FTFL-975, FTFL-976, FTFL-951, FTFL-1015, FTFL-512, FTFL-877, FTFL-940]
sources: Live API verification — az 2.89.1, glab 1.114.0, kubectl (3 AKS contexts), HCP Terraform API
status: Findings consolidated
tags: [audit, ci-cd, gitops, infrastructure/azure, kubernetes, security, terraform, typed-edge]
title: FITFILE Delivery Pipeline Audit 2026-08-27
type: audit
---

## FITFILE Delivery Pipeline Audit — 2026-08-27

End-to-end review of source control, CI, container registry, infrastructure-as-code and GitOps deployment. Every figure re-verified live on 2026-08-27; nothing carried forward unverified from prior sessions.

**Scope:** GitLab · ACR · Terraform Cloud · AKS · ArgoCD
**Method:** Live API, read-only. No FitFile system modified, no secret value read.
**Result:** 16 open findings · 3 resolved

---

### Section notes

| Note | Covers |
|---|---|
| [[FITFILE Audit - Repo and Pipeline Inventory]] | 140 projects, CI triggers, ACR image paths, scan coverage |
| [[FITFILE Audit - Terraform and IaC State]] | 54 TFC workspaces, module inventory, failed applies |
| [[FITFILE Audit - ACR and Identity]] | Two registries, service principals, rotation status, orphaned RBAC |
| [[FITFILE Audit - AKS and ArgoCD Topology]] | 8 clusters, 71 ArgoCD apps, parity gap, customer tenants |
| [[FITFILE Audit - Security Findings and Remediation]] | 16 findings with evidence, maturity assessment, remediation plan |

---

### 1. Headline

The platform is more capable than its controls. Delivery works — 140 projects, 54 Terraform workspaces, eight clusters and a functioning GitOps loop — but the gates that should stand between a developer's keyboard and an NHS production cluster are largely absent or inert.

The most consequential finding is not any single misconfiguration but a **reachable chain**: every group-level CI secret is unprotected, so any push to any branch in any of the 140 projects can read the credentials that grant cluster-admin on AKS and push rights to the registry both production clusters pull from. Set out in full as S-01 in [[FITFILE Audit - Security Findings and Remediation]].

Three items from the previous audit have genuinely been fixed, and one — the token-in-logs leak — was closed the day before this audit ran.

---

### 2. Status of tracked tickets

| Ticket | Item | Verdict |
|---|---|---|
| FTFL-976 | Protect `ARGOCD_STAGING_*` variables | **Not done** — still unprotected, username unmasked |
| FTFL-975 | Enable "pipelines must succeed" | **Not done** on InsightFILE, deployment, data-and-analytics |
| FTFL-973 | ACR JWT in job logs | **Code fixed** 2026-08-26 — logs not purged, credential not rotated |
| FTFL-974 | Rotate ACR SP credentials | **Partial** — rotated 2026-04-21, but expires **2026-10-18** |
| FTFL-951 / FTFL-1015 | Renovate ACR access | **Incomplete** — SP exists, holds zero role assignments |
| — | CI job token scoping | **Confirmed good** |
| — | Forward deployment | **Confirmed good** |

---

### 3. Corrections to prior briefing context

Ten previously held facts did not survive verification. Several are load-bearing.

| Item | As briefed | Verified 2026-08-27 |
|---|---|---|
| Tenant ID | `45e73a3-1ee9-…` | `45e73aa3-1ee9-47c0-ba25-54eda9da021a` |
| Subscription `a085dd04` | Named "Testing" | Named **"Shared Services"**; Testing is `7bbc8ae5` |
| Registries | One, possibly two | **Two distinct** — Fitfileregistry (Premium) + FITFILEPublic (Standard) |
| Subscriptions | One referenced | **Seven**, incl. separate Prod / Non-Prod / Identity |
| Clusters | Staging only | **Eight** AKS clusters (4 stopped) |
| Runners | Mix of SaaS + self-hosted `docker+machine` | **All GitLab SaaS shared**; no self-hosted group runner |
| TFC workspace `ff-demo-dbs` | Exists | **Does not exist** in FITFILE-Platforms |
| ArgoCD version | v3.4.4, multiple Criticals | **v3.5.1** — upgraded; still 2 Critical / 22 High |
| Config-audit counts | 741 Crit / 1233 High / 2320 | **0 Crit / 357 High / 2240** (staging) |
| Obsidian vault | `~/Documents/LMeon` | That path is a **stale divergent copy**; live vault is `/Volumes/DAL/Zettelkasten/LLMeon` |

#### Questions now answered

- **Are `Fitfileregistry` and `fitfilepublic` the same registry?** No. Two registries, same resource group. `FITFILEPublic` has **anonymous pull enabled** and serves third-party mirrors — including the ArgoCD image both clusters run.
- **Is `ffcloud` inside the InsightFILE monorepo?** Yes. `ffcloud-service` and `ffcloud` build from `apps/` paths in InsightFILE; there is no separate `fitfile/apps/ffcloud` project.
- **Are `argocli` and `argocdsync` one image renamed?** Two distinct Docker Hub images. `fitfile/argocdsync:latest` runs the ArgoCD sync script; `fitfile/argocli:alpine` runs the Argo Workflows CLI for integration tests.
- **Why both AWS and Azure modules?** Azure is the delivery platform for all customer and FitFile-run environments. AWS appears only in sandbox/experimental workspaces — no production AWS workload found. The AWS modules are exploratory, not a second production estate.

---

### 4. The recurring pattern

Four separate mechanisms in this estate look like controls and enforce nothing:

1. The ACR IP allowlist sits under `defaultAction: "Allow"` — inert.
2. Approval rules exist on every project but require **0** approvers.
3. InsightFILE's `mr_pipeline_guard` job defends a merge gate that is switched off — its own comment says the gate is enabled, and that comment is stale.
4. The testing cluster holds 27 Trivy reports from November 2024 with no scanner running.

Each would pass a checklist asking *"is it configured?"* and fail one asking *"what does it reject?"* Remediation should verify enforcement, not presence.

---

### 5. Method and limitations

All figures obtained live on 2026-08-27 via `az` 2.89.1, `glab` 1.114.0, `kubectl` against three AKS contexts, and the HCP Terraform API. All operations read-only. **No secret value was read at any point** — credential findings rest on metadata (expiry dates, role assignments, protection flags) and on pattern-matching leaked tokens without recording them. Counts marked "live" carry their capture timestamp and will drift.

**Largest gap:** the customer-tenant clusters (NNUH-DP, LCA-DP, MCNFT, mkuh-prd-4) run in customer-owned Azure tenants that no credential in this environment reaches. That is where NHS patient data actually lives, and it is unassessed. Full gap list in [[FITFILE Audit - Security Findings and Remediation]].

---

### Related

- [[FTFL-512_CICD_Incident_Report]] — independently reached the same conclusions on merge gating and `targetRevision: master`
- [[cicd_minimal_permissions]] — documents the intended standard; none of it is currently implemented
- [[FTFL-799_Unified_Customer_Cloud_Permissions]] — customer-facing permissions model
- [[Improve CICD Pipeline]] · [[Pipeline_Improvement_Proposal]] · [[Integrate Security into the Workflow (Shift Left)]]
- [[FITFILE Value Stream Report - 2026-06-20]] · [[FITFILE]]
