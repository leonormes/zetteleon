---
conformant: true
created: 2026-08-27T18:42:19+01:00
modified: 2026-08-28T17:40:20+00:00
permalink: llmeon/30-library/200-projects/2026-08-27-fitfile-helm-chart-acr-publishing-audit
project_category: refined_deployment
project_name: Refined Deployment
project_status: active
tags: [acr, argocd, deployment, fitfile, ftfl-1008, gitops, helm, oci, supply-chain]
title: 2026-08-27-fitfile-helm-chart-acr-publishing-audit
---

## FITFILE—Helm Chart Publishing & Versioning to ACR (FTFL-1008)

Scope: `fitfile/deployment` repo, both FitFile-run AKS clusters, and the customer root-Application definitions under `Deployment/Clusters`.

Date: 2026-08-27. All cluster and registry operations read-only; no secret value was read.

Parent audit: [[FITFILE Delivery Pipeline Audit 2026-08-27]] · [[FITFILE Audit - ACR and Identity]] · [[FITFILE Audit - AKS and ArgoCD Topology]] · [[FITFILE Audit - Security Findings and Remediation]]

> Provenance. This note was authored by an agent into `30_Library/`, which `AGENTS.md` §6 forbids. Written under explicit per-run human authorisation on 2026-08-27, routed here (not to the Workbench) because [[SoT - HEAD Note Contract (The Workbench)]] §1.2 sends finished engineering analysis to `200_Projects/`. The single unresolved decision was split out to a HEAD note rather than left here as an open-questions section, per contract §4.

> Open threads: [[HEAD - Should ffnode ship to ACR as one umbrella chart or as versioned leaf charts?]]

---

### 1. The Ticket's Premise Is Half Right

FTFL-1008 reads as a quick win: "charts are not currently built or versioned in ACR." The _mechanism_ genuinely is easy, because it already exists and is in production use. What is not easy is that `ffnode` is not the artefact—it is a pointer file.

`charts/ffnode` is an app-of-apps. It renders ~15 ArgoCD `Application` objects. Eight already resolve from ACR. Eleven resolve their own chart from git at sync time:

```yaml
repoURL: https://gitlab.com/fitfile/deployment.git
path: charts/components/ffcloud-service
targetRevision: {{ .Values.argocdApp.targetRevision }}
```

Publishing `ffnode-1.2.3` to ACR today versions the wrapper and not the payload. The version number moves; the deployed content does not correlate with it. That fails the ticket's acceptance criteria 3 (pipeline run ↔ artefact mapping) and 4 (reliable rollback) while appearing to pass—the same shape as the four inert controls catalogued in the parent audit's maturity section.

---

### 2. Evidence—The ACR OCI Path Is Already Live

This is the load-bearing finding for effort estimation. Every piece of the ArgoCD-side plumbing exists:

| Component | State | Evidence |
|---|---|---|
| ACR OCI Helm repo registered | Working | Secret `argocd-acr-pull-secret`—`url: fitfileregistry.azurecr.io`, `type: helm`, `enableOCI: true` |
| AppProject allows the registry | Yes | `AppProject/fitfile` `sourceRepos: [https://gitlab.com/fitfile/deployment.git, fitfileregistry.azurecr.io]`—on staging, prod-1 _and_ the customer template |
| Applications consuming OCI charts | 8, all Synced/Healthy | `helm/mongodb`, `helm/postgresql`, `helm/minio`, `helm/cert-manager`, `helm/argo-workflows`, `helm/prometheus-operator-crds`, `helm/k8s-monitoring` |
| Charts consuming OCI dependencies | 5 | `charts/spicedb`, `charts/hutch`, `charts/integrations/{thehyve,thehyve-v2,ohdsi}` → `repository: oci://fitfileregistry.azurecr.io/helm` |
| Push tooling | Exists | `scripts/old_import_chart_to_acr.sh`—`helm package` → `helm push … oci://$ACR.azurecr.io/helm` |
| Version bumping | Automated | Renovate; the `bugfix/mongodb-19.x`, `bugfix/argo-cd-10.x` branches |

Correction to the parent audit. S-13 states charts are pinned with floating ranges as a general practice. Measured on staging, seven of eight OCI Applications pin exact versions (`19.1.29`, `v1.21.1`, `15.5.15`, `14.7.8-patched`, `8.0.1`, `4.1.6`, `18.1.13`). Only `argo-workflows` at `2.0.*` floats. The floating-version problem is one chart, not a habit.

Publishing first-party charts to ACR therefore needs no new credential, no AppProject change, and no ArgoCD reconfiguration.

---

### 3. Evidence—Versioning Is Entirely Carried by Mutable Git Refs

#### 3.1 Chart Versions Are Frozen

Every first-party `Chart.yaml` sits at its initial version. `charts/ffnode` is `1.0.0`. The only chart whose version moves is `charts/components/ffcloud-service` (`1.0.123`).

The `[RELEASE] The following charts have been updated: workflows/src: 1.0.43` commits are misleading—the diff bumps an image tag inside `values.yaml`, not a chart version. Nothing in the repo increments a `Chart.yaml`.

#### 3.2 The Revision Graph

| Ref                                                                                                             | Kind                                       | Resolves to           | Consumers                                                                     |
| --------------------------------------------------------------------------------------------------------------- | ------------------------------------------ | --------------------- | ----------------------------------------------------------------------------- |
| `master`                                                                                                        | branch                                     | moving                | ffnode chart default (`values.yaml`); 20 of 28 values-driven nodes inherit it |
| `latest-release`                                                                                                | tag, deleted and recreated by `release.sh` | 643af13a (2026-08-18) | ff-a/b/c, barts, prod-1 root apps                                             |
| `eoe-latest-release`, `eoe-test-release`, `nnuh-prod-1-…`, `cuh-prod-1-…`, `mkuh-prod-…`, `sandbox-testing-1-…` | moving tags                                | 643af13a              | per-customer nodes                                                            |
| `nwsde-prod-1-…`, `lcrca-prod-…`                                                                                | moving tags                                | d2a4e8f3 (2026-05-12) | nwsde, LCA                                                                    |
| `mcnft-prod-1-…`                                                                                                | moving tag                                 | d889999f (2026-03-02) | MCNFT                                                                         |
| `upgrade-release`                                                                                               | tag                                        | 9592076f—2023-04-05   | `ffnodes/kch/mn4`                                                             |
| `feature/FFAPP-3073-new-ffnode-chart-with-vault-secrets`                                                        | branch                                     | live                  | acr-test, wm-dev-1                                                            |

Two nodes track a feature branch. `kch/mn4` tracks a tag from April 2023 whose repo layout is a different architectural generation (`charts/crypto-service`, `charts/dps`, `charts/healthfile`, `charts/insightfile`—none exist on master), and its file on master was last edited 2026-05-29.

Because `release.sh` deletes and recreates `latest-release`, and force-push is permitted on `master` (parent audit S-09), "what was ff-a running last Tuesday" is currently unanswerable.

---

### 4. Evidence—Staging Validated Against the Live Cluster

Rendering `charts/ffnode` at `master` over the three ffnodes values files, plus the five root apps from the `fitfile-project` Helm release, reproduces 30 of the 32 live Applications on staging exactly. Zero rendered-but-not-live.

The two extras are both hand-created, outside any Helm release or tracking-id:

- `stress-testing-omop-vocab`—`charts/integrations/thehyve-v2` at `HEAD`, OutOfSync
- `omop-test-db`—OCI `helm/postgresql 18.1.13`, sync status `Unknown`

The app-of-apps model is therefore confirmed, not inferred.

#### 4.1 Root Applications Live outside the Repo

The root Applications are not defined in `fitfile/deployment`. They are installed by a Helm release `fitfile-project` in the `argocd` namespace using the upstream `argocd-apps` 1.4.1 chart. `charts/local-dev/argocd-apps-values.yaml` is the local-dev twin of that values file.

The on-disk source is `Deployment/Clusters/`, which is not a git repository (parent audit S-16).

`Clusters/FITFILE/Production/fitfile-production-infrastructure/production-cluster/resources/argocd-apps.yaml` is dated 23 July 2024 and binds `/ffnodes/fitfile/ff-a/ffnode_values.yaml`—a path that has never existed at `latest-release`. The live release (updated 2026-08-18) binds `values.yaml`. The untracked file an engineer would edit to change production does not describe production. The only accurate record is the Helm release inside the cluster.

#### 4.2 AppProject Coverage is a Minority

13 of 32 staging Applications run in `AppProject/fitfile` (tight `sourceRepos`, single destination). The other 19 run in `default`—`sourceRepos: *`, `destinations: */*`.

This is deliberate, not a bug: `charts/ffnode/values.yaml:116` sets `argocdApp.project: default`, no node overrides it, and six templates hardcode `default` while six hardcode `fitfile` with no discernible rule. Note the split does not track trust—both hand-created apps are in `fitfile`.

#### 4.3 The Degraded Signal is Unusable

All three root ffnode Applications report `Degraded` with an empty health message, while every child resource reports `Synced` and no health at all. Alerting on ArgoCD `Degraded` today would fire three permanent false positives. This must be fixed before the parent audit's remediation item 19 (alert on Degraded/OutOfSync) is worth implementing—and it likely explains why that alert was never added.

---

### 5. Evidence—The Customer Pattern, and Where It Is Ahead

Same `argocd-apps` chart, same `fitfile` AppProject with ACR already in `sourceRepos`, same `charts/ffnode` + `/ffnodes/<org>/<node>/values.yaml` binding. One format difference: customers use the chart's map form (`applications: {name: {…}}`), FitFile clusters use the list form—relevant to anyone writing a parser.

The significant finding is that four of six customer environments already use ArgoCD multi-source (`ff-test-1`, `mkuh-prd-4`, `LCA-DP`, `MCNFT`); `hie-sde-v2` and `hie-test-34` remain single-source. From `Clusters/eoe/Test/ff-test-1/templates/jumpbox.tftpl`:

```hcl
sources = [
  { repoURL = local.chart_repo_url,  path = app.chart_path, targetRevision = chart_target_revision,
    helm = { valueFiles = ["$values/${app.values_file_path}"] } },
  { repoURL = local.values_repo_url, targetRevision = values_target_revision, ref = "values" }
]
```

Chart and values already come from separate repos at separate revisions, and `chart_repo_url` is an overridable config value defaulting to the deployment repo. That is the chart/config split this analysis recommends—already built. For those four environments, pointing charts at ACR is a config change plus swapping `path` for `chart`. The work sits on the older single-source paths: staging, prod-1, `hie-sde-v2`, `hie-test-34`.

---

### 6. Defects Found

| # | Defect | Location | Status |
|---|---|---|---|
| 1 | `kch/prod` and `stg/sandbox` ApplicationSets resolve `charts/ffcloud-service`, `charts/fitconnect`, `charts/frontend` at `latest-release`, where those paths do not exist (they moved to `charts/components/`) | `ffnodes/kch/prod/templates/kch-prod-application-set.yaml:43`, `ffnodes/stg/sandbox/…:43` | 6 Applications that cannot sync |
| 2 | `mkuh-prd-4` points at `charts/thehyve`; the chart is `charts/integrations/thehyve`. Never updated when it moved | `Clusters/eoe/Production/mkuh-prd-4/locals.tf:293` | Customer production |
| 3 | `ff-test-1` pins `chart_target_revision: "ffuh-prod-latest-release"`—not a tag on origin | `Clusters/eoe/Test/ff-test-1/config/customer.yaml:27` | Ref does not resolve |
| 4 | `kch/mn4` tracks `upgrade-release` (2023-04-05), a different repo generation | `ffnodes/kch/mn4/templates/kch-mn4-application-set.yaml` | 12 unresolvable paths |
| 5 | No ApplicationSets are deployed on either FitFile cluster | live clusters | The three ApplicationSet node charts are not running here |
| 6 | Two Applications on staging created by hand, outside any release | `stress-testing-omop-vocab`, `omop-test-db` | Untracked config |

Defects 2 and 3 are read from `Clusters/`, which §4.1 proves can be stale. They are real as written; whether they are live needs customer-tenant access. As `mkuh-prod-latest-release` resolves to the current 643af13a, defect 2 is likely genuinely broken now.

---

### 7. Recommendation

Keep the app-of-apps. Convert each child from a git path to an ACR OCI reference—the shape mongodb and postgresql already use. Publish `ffnode` itself the same way and pin it per node.

```yaml
repoURL: "fitfileregistry.azurecr.io"
chart: helm/ffcloud-service
targetRevision: {{ .Values.ffcloud.chartVersion }}   # "1.4.2", not "master"
```

Rejected: collapsing `ffnode` into an umbrella chart with `dependencies:` and a `Chart.lock`. It gives a stronger single-artefact story and digest-level pinning, but costs per-component Applications—sync waves (annotated throughout the templates), per-app health, per-app rollback, the granularity a 39-app production estate is operated through. One sync becomes all-or-nothing. Not a trade worth making at level-2 change-control maturity.

Why the OCI-reference approach wins here specifically:

- It is not new. Proven in this repo, with working auth and working Renovate.
- It is incremental. One chart at a time; no branch that must land whole.
- It satisfies the ACs literally. A pipeline run maps to `helm/ffcloud-service:1.4.2`; rollback is editing one version string.
- It separates config change from version change. These are one event today—which is what produced the FTFL-512 outage (chart change solo-merged, 8h47m).
- It makes repo tidying safe. Once clusters resolve `oci://…/helm/x:1.2.3`, deleting a directory from `master` cannot change what runs. ACR pull telemetry then answers "is this used?" empirically.

#### 7.1 On the `ffnode` → `ffnodes/<customer>/values.yaml` Pattern

Keep it. The failure is not the pattern but that it is the _only_ axis: the file carries both per-customer configuration and, via `argocdApp.targetRevision`, which code version runs. Split them—config stays in git (reviewable, diffable); version selection becomes an explicit chart-version pin.

#### 7.2 On Per-app Charts

Already true—`charts/components/*`, `charts/spicedb`, `charts/workflows-api`, `charts/certs` are separate charts. What is missing is independent _versions_. Give each its own semver and OCI artefact. Do not split into separate git repositories: that trades one coordination problem for N and multiplies the places holding a shared ACR credential.

---

### 8. Sequencing and the Hard Constraint

The shared ACR credential expires 2026-10-18 (parent audit S-07). All four application repos authenticate with the same `ACR_SERVICE_PRINCIPLE` / `_PASS` pair. Any chart-push job builds on a credential with seven weeks left. FTFL-974 must land first.

Also unresolved and blocking a clean design: `acr-service-principal` holds only `Reader` on `Fitfileregistry`, yet pushes succeed—most likely because the variable holds the registry admin username. A chart-push job needs `AcrPush`. This determines whether disabling admin user is a one-line change or a pipeline migration.

Proposed order:

1. Rotate the ACR credential; resolve what `ACR_SERVICE_PRINCIPLE` actually holds.
2. Confirm and version-control the root Application definitions (§4.1)—they define production and are untracked and stale.
3. Publish one leaf chart (`ffcloud-service`) to ACR; convert one non-production node.
4. Prove rollback by version.
5. Roll forward chart by chart.
6. Publish `ffnode` last, once its children are pinned.
7. Fix the empty-message `Degraded` before adding sync alerting.

---

### 9. Tooling Produced

Both in `fitfile/deployment`, read-only, stdlib + git only:

- `scripts/chart_reference_sweep.py`—fixpoint walk over every git ref reachable from a `targetRevision`, collecting chart-path references at each. Anchors `path:` to a `repoURL:` source block (a bare `path:` is also an ingress path, a volume path, a vault path); expands `charts/{{serviceName}}` against the generator's own list; resolves each path against its own `targetRevision`, not the ref its manifest sits on; deduplicates the ten refs sharing commit 643af13a. Classifies each chart as live / frozen-only / unreferenced / subchart.
- `scripts/external-chart-references.txt`—the out-of-repo references from §4.1 and §5, with provenance and regeneration commands.

Current result: `15 refs reached · 20 live · 0 frozen-only · 4 unreferenced · 6 broken references on master`.

Note `frozen-only` is empty: there is currently no chart that can be deleted from `master` on the argument that an immutable tag retains its own copy. The four unreferenced are `charts/argo/cd` and the three ApplicationSet node charts.

---

### 10. Not Verified

- Customer-tenant clusters. NNUH-DP, LCA-DP, MCNFT and mkuh-prd-4 run in customer-owned Azure tenants. No credential here reaches them. Everything in §5 and defects 2–3 is read from `Clusters/`, which §4.1 proves can drift from reality by years.
- The value of `ACR_SERVICE_PRINCIPLE`. Masked; the admin-username inference rests on behaviour, not confirmation.
- Whether `kch/prod` is deployed anywhere. It resolves three non-existent paths and no ApplicationSet runs on FitFile clusters; its file on master was last touched 2024-02-15.

---

### Sources

- Live: `kubectl` against `fitfile-cloud-staging-aks-cluster` and `fitfile-cloud-prod-1-aks-cluster`; `helm get values fitfile-project -n argocd`; git plumbing over `fitfile/deployment`; `Deployment/Clusters` on disk.
- Jira: FTFL-1008 (parent epic FTFL-1000, Pipeline Performance & Reliability); related FTFL-974, FTFL-975, FTFL-976, FTFL-512.
- [[FITFILE Delivery Pipeline Audit 2026-08-27]]
- [[HEAD - The Release Candidate Object]]—the immutability and artefact/config-separation properties argued there are what §7 operationalises.
