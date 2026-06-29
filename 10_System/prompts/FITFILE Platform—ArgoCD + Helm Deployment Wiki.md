---
created: 2026-06-08 09:13:34+00:00
modified: 2026-06-08 09:18:49+00:00
title: FITFILE Platform—ArgoCD + Helm Deployment Wiki
permalink: llmeon/10-system/prompts/fitfile-platform-argo-cd-helm-deployment-wiki
---

## FITFILE Platform—ArgoCD + Helm Deployment Wiki

_For LLM context. Reflects the system as of June 2026._

---

### §1—Repository Topology

| Repo | GitLab Path | Purpose |
|---|---|---|
| deployment | `gitlab.com/fitfile/deployment` | Central GitOps repo. All Helm charts + ArgoCD Application manifests. Single source of truth for in-cluster state. |
| helm_chart_deployment | Local clone: `/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment` | Same repo, local name used in shell context |
| Customer repos (per cluster) | `gitlab.com/fitfile/customers/eoe/mkuh-prd-4`, `…/nwsde/lca-infrastructure-prd`, etc. | Customer-specific `generated/values.yaml` fed to ArgoCD as `$values` source |
| central-services | `gitlab.com/fitfile/central-services` | Terraform for GitLab/Auth0/HCP Vault/Azure platform control-plane |
| TFC-Modules | `gitlab.com/fitfile/TFC-Modules/…` | Private Terraform registry modules: `terraform-azure-private-infrastructure`, `terraform-azure-aks-automation`, `terraform-azure-aks-backup`, `terraform-argo-argocd`, `terraform-autho-tenant`, `fitfile-version-manager` |

Top-level `deployment` repo structure:

```
charts/          # Helm charts for every FITFILE component
  ffnode/        # THE umbrella chart — deploys a complete FFNode
    Chart.yaml
    values.yaml  # Defaults (sparse — overrides come from ffnodes/)
    templates/
      _argoWorkflows.tpl   _common.tpl   _ffcloud.tpl
      _fitconnect.tpl      _helpers.tpl  _mongodb.tpl
      argo-workflows-application.yaml
      blob-csi-driver-application.yaml
      cert-manager-application.yaml
      certificates-application.yaml
      extra-deploy.yaml
      ffcloud-application.yaml
      fitconnect-application.yaml
      grafana-application.yaml
      grafana-alloy-application.yaml
      mongodb-application.yaml  postgresql-application.yaml
      mssql-application.yaml    minio-application.yaml
      spicedb-application.yaml  storybook-application.yaml
      workflows-api-application.yaml
      mutating-proxy-webhook-application.yaml
  argo/          # ArgoCD chart
  certs/         # cert-manager chart
  components/    # Shared sub-components (frontend, hutch, etc.)
  databases/     # MongoDB, PostgreSQL, MSSQL standalone charts
  integrations/  # thehyve (Hutch), etc.
  local-dev/     # argocd-apps-values.yaml for local dev bootstrap
cue/             # CUE schema: validates ffnodes values, generates configs
ffnodes/         # Per-cluster value overlays (the FFNodes)
pipeline/        # GitLab CI pipeline templates
  common-jobs.yml
  verification-pipelines.yml
  build-pipelines.yml
  staging-pipelines.yml
  release.gitlab-ci.yml
policies/        # OPA/Conftest + Kyverno policies
scripts/
  render.sh      # Templates a specific FFNode deployment for validation
  template.sh    # Check validity of deployed component config
  validate.sh    # Runs conftest + kubeconform + kube-score
  release.sh     # Interactive release: bumps version, creates Git tags
  release-improved.sh  # 617-line interactive release with glab CLI
release-tool/    # Go tooling for chart versioning
workflows/       # Argo Workflow templates
```

---

### §2—FFNode Vs FFNodes—Terminology

| Term | Meaning |
|---|---|
| FFNode (`charts/ffnode`) | The Helm chart. Umbrella chart that renders ArgoCD `Application` CRDs for every service in a customer cluster. |
| FFNodes (`ffnodes/`) | The directory of per-cluster value overlay files. Each subdirectory is a customer/environment group (e.g., `fitfile/`, `barts/`, `eoe/`, `nwsde/`, `kch/`, `wmsde/`, `stg/`), each containing further subdirectories per cluster. |

Values overlay structure:

```
ffnodes/
  fitfile/
    testing/
      values.yaml          # testing cluster overlay
    staging/
      values.yaml
    ff-test-a/
      values.yaml
      hutch_values.yaml    # optional Hutch/Relay config
  barts/
    values.yaml
  eoe/
    cuh-prod-1/values.yaml
    hie-prod-34/values.yaml
    nnuh-prod-1/values.yaml
  nwsde/
    nwsde-prod-1/values.yaml
  kch/
    values.yaml
  wmsde/
    values.yaml
  stg/          # divergent layout — has its own Chart.yaml/templates/
  empty-values.yaml  # canonical blank template
```

A real `values.yaml` overlay looks like:

```yaml
namespace: nwsde-prod-1
deploymentKey: nwsde-prod-1
deploy:
  certManager: true
argocdApp:
  targetRevision: nwsde-prod-1-latest-release
  host: "nwsde-prod-1.fitfile.net"
argoworkflows:
  server:
    authModes: [client]
  sso:
    enabled: false
global:
  fitConnectCode: "North West SDE"
  oauth:
    baseURL: "https://fitfile-prod.eu.auth0.com"
    managementApiAudience: "https://fitfile-prod.eu.auth0.com/api/v2/"
```

Key `values.yaml` top-level sections:

| Key | Purpose |
|---|---|
| `namespace` | Kubernetes namespace for all workloads |
| `deploymentKey` | Must match the directory name; used as label/naming prefix |
| `deploy.*` | Feature flags: `certManager`, `monitoring`, `fitconnect`, `persistence`, `proxy`, etc. |
| `argocdApp.targetRevision` | The mutable Git tag ArgoCD tracks (e.g., `mkuh-prod-latest-release`) |
| `argocdApp.host` | Cluster ingress hostname |
| `argocdApp.globalIgnoreDifferences` | `ignoreDifferences` passed to all child ArgoCD apps |
| `argocdApp.syncPolicy` | Default: `automated: {prune: true, selfHeal: true}` |
| `global.imagePullSecrets` | ACR pull secret (usually `fitfile-image-pull-secret`) |
| `global.fitConnectCode` | Human name for the cluster (e.g., "North West SDE") |
| `global.oauth.*` | Auth0 endpoints |
| `grafanaAlloy.*` | Grafana Alloy (k8s-monitoring) chart config |
| `mongodb.*` / `postgresql.*` | Database config including `vaultSecrets` |
| `argoWorkflows.*` / `workflowsApi.*` | Argo Workflows config |
| `vaultSecrets` | List of `VaultStaticSecret` definitions (component-level) |

---

### §3—ArgoCD Application Architecture

#### App-of-Apps Pattern

```
ArgoCD (argocd namespace)
└── ff-{deploymentKey}         ← Root Application (app-of-apps)
    ├── ff-{dk}-cert-manager   ← from charts/certs/ (sync wave -4)
    ├── ff-{dk}-certificates   ← (sync wave -3)
    ├── ff-{dk}-argo-workflows ← (sync wave -2)
    ├── ff-{dk}-ffcloud-service← (sync wave 3)
    ├── ff-{dk}-fitconnect     ← (sync wave 3)
    ├── ff-{dk}-frontend       ← (sync wave 4)
    ├── ff-{dk}-mongodb-{hash} ← (sync wave 2)
    ├── ff-{dk}-postgresql     ← (sync wave 2)
    ├── ff-{dk}-minio          ← (sync wave 2)
    ├── ff-{dk}-spicedb        ← (sync wave 2)
    ├── ff-{dk}-grafana-k8s-monitoring ← (sync wave -4)
    └── ... (blob-csi-driver, mutating-proxy-webhook, etc.)
```

#### Root Application Spec (multi-source, the Defining pattern)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ff-mkuh-prd-4
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "-2"
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  destination:
    namespace: argocd
    server: https://kubernetes.default.svc
  ignoreDifferences:
    - group: apps
      jsonPointers: [/spec/replicas]
      kind: Deployment
  sources:
    # Source 1: The chart itself (ffnode umbrella chart)
    - path: charts/ffnode
      repoURL: https://gitlab.com/fitfile/deployment.git
      targetRevision: mkuh-prod-latest-release   # ← mutable tag
      helm:
        valueFiles:
          - $values/generated/values.yaml        # ← from source 2
    # Source 2: Customer values repo ($values ref)
    - ref: values
      repoURL: https://gitlab.com/fitfile/customers/eoe/mkuh-prd-4.git
      targetRevision: main
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - Validate=false
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
```

Critical: `selfHeal: true` means all changes MUST go through GitOps source—`kubectl patch` commands are reverted within minutes.

#### Child Application Example (grafana)

```yaml
{{- if eq .Values.deploy.monitoring true }}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: grafana-k8s-monitoring
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "-4"
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  ignoreDifferences: {{ toYaml .Values.argocdApp.globalIgnoreDifferences | nindent 4 }}
  destination:
    namespace: monitoring
    server: https://kubernetes.default.svc
  source:
    chart: helm/k8s-monitoring
    repoURL: "fitfileregistry.azurecr.io"   # OCI chart from ACR
    targetRevision: {{ default "4.1.4" (.Values.grafanaAlloy.chart).targetRevision }}
    helm:
      releaseName: grafana-alloy-k8s-monitoring
      values: |-
        {{- toYaml .Values.grafanaAlloy | nindent 8 }}
  project: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
{{- end }}
```

#### OCI Charts (ACR)

Helm charts are published to `fitfileregistry.azurecr.io/helm/…` via the CI pipeline. ArgoCD pulls them using OCI protocol:

```yaml
repoURL: "fitfileregistry.azurecr.io"
chart: helm/k8s-monitoring
targetRevision: 4.1.3
```

ACR credentials are injected via a `VaultDynamicSecret` that populates `argocd-acr-pull-secret` in the `argocd` namespace.

---

### §4—The Release Process

#### Standard Flow (`release.sh` / `release-improved.sh`)

The `release-improved.sh` script (617 lines, uses `glab` CLI):

1. Developer merges feature branch into `master`
2. Runs `./release.sh` or `./release-improved.sh` from the repo root
3. Script prompts for/determines version bump (semver)
4. Creates two Git tags:
   - Immutable: `v{major}.{minor}.{patch}` (e.g., `v1.8.67`)
   - Mutable per-cluster: `{deploymentKey}-latest-release` (e.g., `mkuh-prod-latest-release`, `nwsde-prod-1-latest-release`, `sandbox-testing-1-latest-release`)
5. Pushes both tags to `gitlab.com/fitfile/deployment`
6. ArgoCD (watching the mutable tag) detects the tag move → auto-syncs

Tag naming convention examples (from LTM):

- `latest-release`—general/testing
- `sandbox-testing-1-latest-release`
- `mkuh-prod-latest-release`
- `nwsde-prod-1-latest-release`
- `nnuh-prod-1-latest-release`
- `cuh-prod-1-latest-release`
- `eoe-latest-release`
- `v1.8.65`, `v1.8.66`, `v1.8.67`—immutable semver tags

GitLab branch naming policy enforced via pre-receive hook:

```
(renovate/|feature/|bugfix/|hotfix/|task/|master|development|staging).*
```

Commit message convention for releases:

```
[RELEASE] The following charts have been updated: <chart-list>
```

---

### §5—Vault Secrets Integration

#### Architecture

```
HashiCorp Vault (HCP Cloud)
  └── Namespace: admin/deployments/{deploymentKey}/
      └── KV path: secrets/data/{component}
              ↓
      VaultStaticSecret CRD (in Kubernetes)
              ↓
      Vault Secrets Operator (VSO)
              ↓
      Kubernetes Secret (Pod-mountable)
```

#### VaultAuth Bootstrap

Each cluster namespace has a default `VaultAuth` resource using Kubernetes service account JWT:

```yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultAuth
metadata:
  name: default
  namespace: {deploymentKey}
spec:
  method: kubernetes
  mount: kubernetes
  kubernetes:
    role: {deploymentKey}
    serviceAccount: default
  vaultConnectionRef: default
```

#### VaultStaticSecret Example (from `values.yaml`)

```yaml
argoWorkflows:
  vaultSecrets:
    - secretName: argo-postgres-config
      vaultPath: application
      secretTransformationDisableTpl: true
      secretTransformation:
        excludes: [".*"]
        templates:
          username:
            text: '{{`{{get .Secrets "postgresql_username"}}`}}'
          password:
            text: '{{`{{get .Secrets "postgresql_password"}}`}}'
```

This renders into:

```yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultStaticSecret
metadata:
  name: argo-postgres-config
  namespace: argo
spec:
  mount: secrets
  namespace: admin/deployments/lca-prd-2
  path: application
  type: kv-v2
  refreshAfter: 5m
  destination:
    create: true
    name: argo-postgres-config
    overwrite: false
  transformation:
    excludes: [".*"]
    templates:
      username:
        text: '{{get .Secrets "postgresql_username"}}'
      password:
        text: '{{get .Secrets "postgresql_password"}}'
```

#### ArgoCD Git Credentials via VSO

ArgoCD's repo credentials are also Vault-managed. A `VaultStaticSecret` named `argocd-group-creds` (in `argocd` namespace) templates the `argocd-repo-fitfile-deployment-repo` Kubernetes secret:

```yaml
# In Vault: admin/deployments/{dk}/secrets/argocd
# Keys: gitlab_deploy_token_username, gitlab_deploy_token_password,
#       gitlab_values_access_token, gitlab_values_access_username,
#       admin_password, server_secret_key
```

VSO syncs these on a 30-minute refresh cycle. If the secret goes stale, delete it and VSO recreates it:

```bash
kubectl delete secret argocd-repo-fitfile-deployment-repo -n argocd
# VSO auto-recreates within seconds
```

---

### §6—Bootstrap Sequence (New Cluster)

Mode A: Bootstrap (local Terraform, one-time)

```bash
# 1. Terraform provisions foundation
terraform apply  # Creates: AKS cluster, Vault namespace, GitLab repo,
                 # TFC workspace, ACR pull secret, initial deploy tokens

# 2. Install ArgoCD via Helm (from local script)
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm upgrade --install -n argocd --version "$ARGOCD_CHART_VERSION" \
  argocd argo/argo-cd -f "$DEPLOYMENT_DIR/charts/local-dev/argocd-values.yaml"

sleep 5

# 3. Install argocd-apps (the ApplicationSet that creates child apps)
helm upgrade --install -n argocd --version "$ARGOCD_APPS_CHART_VERSION" \
  argocd-apps argo/argocd-apps \
  -f "$DEPLOYMENT_DIR/charts/local-dev/argocd-apps-values.yaml"

# 4. Create ACR pull secrets in all required namespaces
for ns in default argo spicedb mesh-mailbox monitoring; do
  kubectl create secret docker-registry acr -n "$ns" \
    --docker-server=fitfileregistry.azurecr.io \
    --docker-username=Fitfileregistry \
    --docker-password="$ACR_SERVICE_PRINCIPLE_ACCESS_KEY"
done
```

Mode B: Steady-state (TFC handles infra, ArgoCD handles apps)

After bootstrap: