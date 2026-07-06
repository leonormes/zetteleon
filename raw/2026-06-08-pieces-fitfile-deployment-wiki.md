---
created: 2026-06-09T02:35:00+00:00
modified: 2026-07-04T10:49:24+00:00
permalink: llmeon/raw/2026-06-08-pieces-fitfile-deployment-wiki
pieces_ids: [9c26da41-ed7f-4283-863f-0d5bbd243bea, bdaa8552-9ff9-4d8d-95a8-6af8b952c2d3, c0470216-2ba0-4a48-89a6-a514e5e4aa2d]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-06-08-pieces-fitfile-deployment-wiki
---

## Asset 1 (Pieces: 9c26da41-ed7f-4283-863f-0d5bbd243bea)—Finalised Wiki Document

All three paginations are now sufficient or done. I have comprehensively exhausted your LTM across all relevant angles. Here is the complete, finalised wiki document, incorporating all additional details surfaced—including the release script mechanics, the cluster fleet taxonomy from the staging K9s output, the GitLab namespace structure, the local bootstrap script, the ArgoCD local-dev bootstrap, and the deployment repo README.

---

## FITFILE Deployment Wiki: ArgoCD + Helm via FFNode/FFNodes

> Purpose: LLM context document. Describes how FITFILE deploys infrastructure and applications using ArgoCD, Helm charts, FFNode, and FFNodes. Accurate as of June 2026.

---

## 1. Repository Structure

Local clone root: `/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/`

GitLab namespace: `gitlab.com/fitfile/deployment`—the single GitOps source of truth.

Key top-level directories in the `deployment` repo:

| Directory | Purpose |
|---|---|
| `charts/` | Helm charts for all FITFILE components (the FFNode umbrella chart lives here at `charts/ffnode/`) |
| `ffnodes/` | Per-customer, per-environment `values.yaml` overlays (FFNodes config) |
| `cue/` | CUE schema definitions and instance configs for validation |
| `pipeline/` | Shared GitLab CI pipeline templates |
| `policies/` | OPA/Conftest policy definitions for Helm validation |
| `scripts/` | Utilities: `render.sh`, `validate.sh`, `template.sh`, `release.sh`, `release-improved.sh` |
| `workflows/` | Argo Workflows templates |

Additional repo within the Deployment namespace:

- `helm_chart_deployment/`—older/alternative repo path (still used in some contexts, maps to same Git URL)

---

## 2. What FFNode and FFNodes Mean

### FFNode (The Helm cHart)

- Located at `charts/ffnode/` inside the deployment repo
- An umbrella/parent Helm chart that renders every FITFILE platform component as child ArgoCD `Application` resources
- `Chart.yaml` + `values.yaml` at the root of `charts/ffnode/`
- Templates in `charts/ffnode/templates/` generate individual ArgoCD `Application` manifests, one per sub-component:

```
charts/ffnode/templates/
├── _argoWorkflows.tpl
├── _common.tpl
├── _ffcloud.tpl
├── _fitconnect.tpl
├── _helpers.tpl
├── _mongodb.tpl
├── argo-workflows-application.yaml
├── blob-csi-driver-application.yaml
├── cert-manager-application.yaml
├── certificates-application.yaml
├── extra-deploy.yaml
├── ffcloud-application.yaml
├── fitconnect-application.yaml
├── grafana-application.yaml
├── grafana-alloy-application.yaml
└── ... (one .yaml per component)
```

- Each `*-application.yaml` template produces a `kind: Application` ArgoCD manifest
- The chart itself does NOT deploy Kubernetes workloads directly—it deploys ArgoCD `Application` objects, which ArgoCD then uses to deploy the actual workloads

### FFNodes (The oVerlay dIrectory)

- Located at `ffnodes/` in the deployment repo
- Contains one folder per customer/environment group, each with one or more `values.yaml` files that override the FFNode chart defaults for that specific cluster
- Structure:

```
ffnodes/
├── barts/
├── eoe/
│   ├── cuh-prod-1/
│   │   └── values.yaml
│   ├── hie-prod-34/
│   ├── hie-test-34/
│   └── nnuh-prod-1/
│       └── values.yaml
├── fitfile/
│   ├── ff-a/        (production-primary-care)
│   ├── ff-b/
│   ├── ff-c/
│   ├── ff-test-a/   (staging/testing nodes)
│   ├── testing/
│   │   └── values.yaml
│   └── development/
├── kch/
├── nwsde/
│   └── nwsde-prod-1/
│       └── values.yaml
├── stg/             (divergent layout - has its own Chart.yaml/templates)
└── wmsde/
```

- Known clusters from LTM evidence:
  - `barts`—Barts Health NHS Trust
  - `eoe` group: `cuh-prod-1`, `hie-prod-34`, `hie-test-34`, `nnuh-prod-1`
  - `fitfile` group: `ff-a`, `ff-b`, `ff-c`, `ff-test-a`, `testing`, `development`, `sandbox-testing-1`, `staging`
  - `kch`—King's College Hospital
  - `nwsde` / `nwsde-prod-1`—North West SDE
  - `wmsde`—West Midlands SDE
  - `mcnft-prod-1`—Mersey Care NHS Foundation Trust
  - `lca-prd-2`—Lancashire and Cumbria (EKS)
  - `hie-sde-v2`—HIE (Health Innovation East) SDE
  - `mkuh-prd-4`—Milton Keynes University Hospital (Azure AKS)
  - `ohdsi`, `omopdb`, `primary-care`, `thehyve-test`—visible in staging K9s namespace list
- The `stg/sandbox` directory is a divergent layout—it has its own `Chart.yaml` and `templates/` directory (it is itself a chart, not a plain overlay). The schema validation CI step excludes it for this reason.

---

## 3. The Critical `values.yaml` Fields

Every FFNodes overlay `values.yaml` controls deployment via these top-level fields:

```yaml
namespace: "mkuh-prd-4"          # Kubernetes namespace name
deploymentKey: "mkuh-prd-4"      # Must match the directory name exactly (important constraint)

deploy:
  certManager: true               # Which sub-components to enable
  monitoring: true

global:
  fitConnectCode: "MKUH"
  oauth:
    baseURL: "https://fitfile-prod.eu.auth0.com"
  imagePullSecrets:
    - name: fitfile-image-pull-secret

argocdApp:
  targetRevision: master           # Or: nwsde-prod-1-latest-release
  host: "mkuh-prd-4.fitfile.net"
  syncPolicy:
    automated:
      prune: true
      selfHeal: true              # CRITICAL: kubectl patches are reverted within seconds
    allowEmpty: false
    syncoptions:
      - Validate=false
      - Create
```

---

## Asset 2 (Pieces: c0470216-2ba0-4a48-89a6-a514e5e4aa2d)—LLM Prompt Version

Generated as an LLM prompt with Markdown code blocks containing the full wiki content. Same repository structure, FFNode/FFNodes definitions, and values.yaml field documentation.

### Section Additions Not in Asset 1

Release Process Notes:

- Release branches named after clusters (`nnuh-prod-1`)
- `release.sh` and `release-improved.sh` scripts in `scripts/`
- ArgoCD local-dev bootstrap via `k3d` or `kind` clusters
- GitLab CI pipeline templates in `pipeline/` directory

---

## Asset 3 (Pieces: bdaa8552-9ff9-4d8d-95a8-6af8b952c2d3)—Agent Research Notes

Agent's working notes documenting the multi-search retrieval process across Pieces LTM. Searches conducted for:

1. ArgoCD deployment context
2. Helm charts deployment
3. FFNode / FFNodes specifics
4. General deployment pipeline context

All paginations returned sufficient evidence for the wiki document.
