---
title: FITFILE Deployment — ArgoCD + Helm
wiki_type: dossier
entity_kind: project
created: 2026-06-09T03:35:00+01:00
modified: 2026-06-15T10:00:00+01:00
tags: [wiki, dossier]
sources:
  - raw/2026-06-08-pieces-fitfile-deployment-wiki
---

## Summary

FITFILE deploys infrastructure and applications using ArgoCD, Helm charts via the FFNode umbrella chart, with per-customer/per-environment `values.yaml` overlays in the `ffnodes/` directory. The deployment repo at `gitlab.com/fitfile/deployment` serves as the single GitOps source of truth, spanning ~15+ clusters across NHS trusts and SDEs with a diverse fleet taxonomy (AKS, EKS, private clusters).

## Key Facts

- **Repository structure** — The deployment repo has seven key top-level directories: `charts/` (Helm charts including the FFNode umbrella chart at `charts/ffnode/`), `ffnodes/` (per-cluster `values.yaml` overlays), `cue/` (CUE schema validation), `pipeline/` (GitLab CI templates), `policies/` (OPA/Conftest policies), `scripts/` (utility scripts: `render.sh`, `validate.sh`, `release.sh`), and `workflows/` (Argo Workflows templates) — [[raw/2026-06-08-pieces-fitfile-deployment-wiki]] (Pieces: 9c26da41-ed7f-4283-863f-0d5bbd243bea)

- **FFNode (umbrella chart)** — Located at `charts/ffnode/`, it renders every FITFILE platform component as child ArgoCD `Application` resources. Each `*-application.yaml` template produces a `kind: Application` ArgoCD manifest. The chart deploys ArgoCD Application objects, not Kubernetes workloads directly — ArgoCD then deploys the actual workloads — [[raw/2026-06-08-pieces-fitfile-deployment-wiki]] (Pieces: 9c26da41-ed7f-4283-863f-0d5bbd243bea)

- **FFNodes (overlays)** — Per-cluster `values.yaml` files organized by customer/environment group. Structure: `ffnodes/{customer}/{cluster}/values.yaml`. Each overlay overrides the FFNode chart defaults for that specific cluster — [[raw/2026-06-08-pieces-fitfile-deployment-wiki]] (Pieces: 9c26da41-ed7f-4283-863f-0d5bbd243bea)

- **Cluster fleet taxonomy** — Known clusters include: `barts` (Barts Health NHS Trust), `eoe` group (`cuh-prod-1`, `hie-prod-34`, `hie-test-34`, `nnuh-prod-1`), `fitfile` group (`ff-a`/production-primary-care, `ff-b`, `ff-c`, `ff-test-a`/staging, `testing`, `development`, `sandbox-testing-1`), `kch` (King's College Hospital), `nwsde`/`nwsde-prod-1` (North West SDE), `wmsde` (West Midlands SDE), `mcnft-prod-1` (Mersey Care NHS FT), `lca-prd-2` (Lancashire and Cumbria/EKS), `hie-sde-v2` (Health Innovation East SDE), `mkuh-prd-4` (Milton Keynes University Hospital/AKS) — [[raw/2026-06-08-pieces-fitfile-deployment-wiki]] (Pieces: 9c26da41-ed7f-4283-863f-0d5bbd243bea)

- **Critical `values.yaml` fields** — Every overlay must specify: `namespace` (K8s namespace name), `deploymentKey` (must match directory name exactly), `deploy.*` (which sub-components to enable), `global.fitConnectCode`, `global.oauth.baseURL`, `global.imagePullSecrets`, and `argocdApp.targetRevision` (branch/tag), `host`, and `syncPolicy` (prune: true, selfHeal: true) — [[raw/2026-06-08-pieces-fitfile-deployment-wiki]] (Pieces: 9c26da41-ed7f-4283-863f-0d5bbd243bea)

- **Self-heal constraint** — ArgoCD sync policy has `selfHeal: true`, meaning kubectl patches are reverted within seconds. Any direct cluster modifications must be made through the values overlay, not via kubectl — [[raw/2026-06-08-pieces-fitfile-deployment-wiki]] (Pieces: 9c26da41-ed7f-4283-863f-0d5bbd243bea)

- **Divergent layouts** — The `stg/sandbox` directory has its own `Chart.yaml` and `templates/` directory, making it itself a chart rather than a plain overlay. The schema validation CI step excludes it — [[raw/2026-06-08-pieces-fitfile-deployment-wiki]] (Pieces: 9c26da41-ed7f-4283-863f-0d5bbd243bea)

- **Release process** — Release branches named after clusters (e.g. `nnuh-prod-1`). Scripts `release.sh` and `release-improved.sh` in `scripts/`. ArgoCD local-dev bootstrap via `k3d` or `kind` clusters. GitLab CI pipeline templates in `pipeline/` directory — [[raw/2026-06-08-pieces-fitfile-deployment-wiki]] (Pieces: c0470216-2ba0-4a48-89a6-a514e5e4aa2d)

## Connections

- [[wiki/projects/ffnode Helm Chart Review]] — Detailed review of the FFNode umbrella chart structure, dependencies, and CI pipelines
- [[cicd-tooling-validated]] — Incremental optimisation of the GitOps pipeline measured via Four Key Metrics
- [[wiki/projects/Grafana Alloy Monitoring — FTFL-638]] — Monitoring stack deployed via the FFNode chart and ArgoCD pipeline
- [[wiki/projects/Helm Chart Structured Metadata — Grafana Cloud Log Enrichment]] — Structured metadata experiment deploying through the ffnode chart
- [[GitLab CI integration]] — CD philosophy decision process providing governance framework for pipeline remediation

## Contradictions

None identified yet.

## Open Questions

- Are `ffnodes/stg/sandbox` and `ffnodes/stg/staging` the same cluster with both a divergent and conventional overlay path?
- Is the `helm_chart_deployment/` repo still actively used or deprecated in favour of the main deployment repo?
- What is the release cadence and how are release branches merged back to master?