---
created: 2026-08-27T10:30:00+00:00
modified: 2026-08-27T10:30:00+00:00
permalink: llmeon/30-library/200-projects/fitfile-audit-repo-and-pipeline-inventory
project_category: refined_deployment
project_name: Pipeline
project_status: active
date: 2026-08-27
tags: [audit, ci-cd, gitlab, infrastructure/azure, security]
title: FITFILE Audit - Repo and Pipeline Inventory
type: audit
---

## Repo & Pipeline Inventory

Section of [[FITFILE Delivery Pipeline Audit 2026-08-27]]. Verified live 2026-08-27.

**140 projects** exist under the `fitfile` group; **33** have local clones. Of the 140, **40** sit under `fitfile/archive/` and are dormant. The active delivery surface is far smaller than the project count suggests.

---

### 1. Application repositories

| Repo | Default | CI trigger | Deploy target | ACR image path |
|---|---|---|---|---|
| `apps/InsightFILE` | `development` | MR event; push to `development` | Child `release` pipeline → bumps `fitfile/deployment` → ArgoCD | `fitfileregistry.azurecr.io/{ffcloud-service, fitconnect-service, scheduler-service, frontend, storybook, sftp-loader, emis-processing, default-exit-handler, medcat-annotation, set-intersection-estimator, dps/workflows-api, mockrest, mutating-proxy-webhook, nhs-pet, s3-fitfile-cli}` |
| `ude-cli` | `development` | MR event; push to default | Release job → version bump | `fitfileregistry.azurecr.io/ude-cli` |
| `data-and-analytics` | `development` | MR event; merge train; push to default | Release job → version bump | `fitfileregistry.azurecr.io/dps/queue-listener` (+ per-package builds) |
| `workflows-api` | `master` | MR event; merge train; push to default | Release job → version bump | `fitfileregistry.azurecr.io/dps/workflows-api` |
| `deployment` | `master` | Any CI event (`if: $CI`) | ArgoCD sync via `testing-argocd.fitfile.net`; source of truth for all clusters | — (GitOps repo) |
| `central-services` | `master` | Pipeline-gated merge | 7 TFC workspaces (auth0, grafana, vault, cloudflare, entra) | — |

Sources: each repo's `.gitlab-ci.yml`, `deployment/pipeline/build-job.yaml` and `build.sh`, cross-checked against `glab api projects/…`.

---

### 2. How a build actually authenticates

All four application repos share one credential pair. The identical line appears in each `build.sh`:

```bash
docker login fitfileregistry.azurecr.io \
  --username "${ACR_SERVICE_PRINCIPLE}" --password "${ACR_SERVICE_PRINCIPLE_PASS}"
```

Consequences covered in [[FITFILE Audit - ACR and Identity]]: the credential expires 2026-10-18, and its expiry breaks every image build across the estate simultaneously.

InsightFILE additionally pushes build cache to the registry with `--cache-to type=registry,mode=max`, publishing intermediate layers.

---

### 3. Build and scan coverage

None of the four repos runs a container scan or secret detection before publishing.

| Repo | SAST | Secret detection | Container scan | SonarQube | Docker image pin |
|---|---|---|---|---|---|
| `InsightFILE` | None | None | None | Yes | `docker:latest` |
| `ude-cli` | None | None | None | None | `docker:latest` |
| `data-and-analytics` | Yes | None | None | None | `docker:29` |
| `workflows-api` | None | None | None | Yes | `docker:24` |

Vulnerability detection happens only **after** deployment, via Trivy Operator in-cluster. Nothing blocks a vulnerable image from reaching a cluster.

Python runtime drift is also present in `data-and-analytics` (3.10.9, 3.11, 3.13 across packages) and `workflows-api` (`python:3.10-buster`; Debian buster is past LTS).

---

### 4. Self-documented coverage blind spot

InsightFILE's `.gitlab-ci.yml` carries a `mr_pipeline_guard` job whose own comment is unusually candid:

> Every other job in this pipeline is gated on `changes:`, so a change that touches no matched path produces zero jobs… The whole of `apps/tasks/*` except `s3-fitfile-cli` is in that blind spot… Renovate MRs against `nhs-pet` merged with no pipeline whatsoever.
>
> This job passing means the pipeline exists — it does NOT mean the change was tested.

Tracked as FTFL-877. Note the same comment asserts *"With 'Pipelines must succeed' now enabled on this project…"* — **that assertion is stale**; the gate is off. See S-02 in [[FITFILE Audit - Security Findings and Remediation]].

Also disabled: `resource_group: deployment-repo` on the release job is commented out ("Temporarily removing"), removing race-condition protection when multiple pipelines version the deployment repo concurrently.

---

### 5. Clones without remotes, remotes without clones

- **112 remote projects have no local clone** — expected, not itself a problem.
- `Deployment/TFC-Modules/platform-defaults` points at a GitLab project that **no longer exists** (renamed to `terraform-fitfile-platform-defaults`). A stale clone that will silently fail to fetch.
- `Deployment/new-helm/fitfile-platform` and `…/customer-nhs-trust-b` are git repos with **no remote at all** — local-only Helm chart work, no backup, no review path.
- `Deployment/Clusters` — **5,149 files, not under version control**, including every `customer.yaml` defining production customer network ranges, node pools and backup scope.
- `Application/git-auto-package-versioner/test/deployment` → `https://my-fake-repo.com`. Benign: a test fixture.

---

### 6. Runner fleet

All runners available to the group are **GitLab SaaS shared/instance runners** — `saas-linux-*`, `saas-macos-*`, `saas-windows-*`, and the `shared-gitlab-org` dind pool. No self-hosted group runner was found, correcting a prior assumption of `docker+machine` executors.

One stale `project_type` runner (`3149836`) remains registered to InsightFILE.

This matters because group secrets — including the AKS `--admin` credentials — flow to GitLab-managed shared infrastructure, and because SaaS runner egress IPs are not stable, which constrains the ACR network-allowlist remediation.

---

### Related

- [[FITFILE Delivery Pipeline Audit 2026-08-27]] — hub
- [[FITFILE Audit - ACR and Identity]] · [[FITFILE Audit - Security Findings and Remediation]]
- [[FTFL-512_CICD_Incident_Report]] · [[Improve CICD Pipeline]] · [[GitLab CI integration]]
