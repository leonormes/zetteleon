---
created: 2026-05-14T13:32:12+00:00
modified: 2026-05-15T07:54:48+00:00
title: pieces_copilot_message_export_may_14_2026_2_32pm
---

## TASK: Comprehensive CI/CD Pipeline Audit & Documentation

You are a senior platform engineer tasked with producing a complete, accurate documentation of how this organisation's GitLab CI/CD pipelines are wired together to perform delivery and deployment. Use ALL code analysis tools available to you—file reading, directory traversal, grep/search, AST analysis, and any others—before drawing any conclusions.

---

### ORGANISATION CONTEXT

Company: FITFILE (FITFILE Group Limited)

GitLab Group: `gitlab.com/fitfile`

GitLab Namespace structure (confirmed):

gitlab.com/fitfile/

```
├── apps/
│   └── InsightFILE          # Main application repo — has .gitlab-ci.yml
├── Application/
│   └── data-and-analytics   # Data/OMOP pipeline repo
├── Deployment/
│   ├── helm_chart_deployment  # GitOps Helm deployment repo — has .gitlab-ci.yml AND staging.gitlab-ci.yml
│   └── Clusters/
│       ├── eoe/
│       │   ├── Production/   # Customer cluster repos (e.g. hie-sde-v2, CUH-DP, NNUH-DP, mkuh-prd-4)
│       │   └── Test/
│       ├── FITFILE/
│       │   └── (Non-Production, Production, sandbox)
│       └── nwsde/
│           ├── lca-infrastructure-prd
│           └── mcnft-prod-1
├── Customers/
│   ├── eoe/
│   └── nwsde/
├── TFC-Modules/              # Terraform Cloud module repos
│   ├── fitfile-version-manager
│   ├── terraform-argo-argocd
│   ├── terraform-auth0-tenant
│   ├── terraform-azure-private-infrastructure
│   ├── terraform-azure-aks-automation
│   ├── terraform-azure-aks-backup
│   └── ...
└── central-services          # Platform control plane — Terraform for GitLab/Auth0/HCP/Azure/Grafana
```

Local clone root (confirmed): `/Volumes/DAL/Fitfile/gitlab/FITFILE/`

---

### KNOWN TECHNOLOGY STACK

These tools are in use—your analysis must confirm and expand on exactly how each is configured:

| Layer | Technology |
|---|---|
| CI/CD Engine | GitLab CI (`.gitlab-ci.yml`, `staging.gitlab-ci.yml`) |
| Container Registry | Azure Container Registry (`fitfileregistry.azurecr.io`) |
| IaC | Terraform (run via HCP Terraform Cloud, org: `FITFILE-Platforms`) |
| Infrastructure | Azure AKS (multiple clusters per customer) |
| GitOps | ArgoCD (manages in-cluster Helm releases) |
| Helm | Custom `helm_chart_deployment` repo + `fitfile-version-manager` for centralised chart versioning |
| Secrets | HashiCorp Vault (HCP) → Vault Secrets Operator (VSO) in cluster |
| Auth | Auth0 (tenant managed via Terraform) |
| Manifest Generation | CUE lang (`cue export`) from Terraform outputs → Helm values |
| DNS | Cloudflare |
| Observability | Grafana Cloud |
| GitLab Auth (Vault) | JWT/OIDC via `gitlab.com/fitfile` group |
| Renovate | Dependency updates via `renovate.json` |

---

### INVESTIGATION SCOPE

Work through the following areas in order, using ALL available tools for each. Do not skip sections.

---

#### 1. GitLab CI Pipeline Configuration

For every `.gitlab-ci.yml` and `staging.gitlab-ci.yml` found in the repo tree:

1. Read the full file contents.
2. Document:
   - Stages (in order)
   - Jobs per stage—name, `image`, `script`, `rules`/`only`/`except` trigger conditions
   - Variables—which are defined inline vs referenced from GitLab CI/CD settings
   - Artifacts—what is produced and passed between jobs
   - Cache configuration
   - Include directives (child pipelines, templates)
   - Trigger jobs (cross-project pipeline triggers)
   - Environment targets (staging, production, etc.)
   - When conditions (manual, on-push, merge-to-main, scheduled)

Key files to find and read:

- `helm_chart_deployment/.gitlab-ci.yml`
- `helm_chart_deployment/staging.gitlab-ci.yml`
- `apps/InsightFILE/.gitlab-ci.yml` (if present)
- Any `.gitlab-ci.yml` in `Deployment/Clusters/`
- Any included YAML templates referenced via `include:`

---

#### 2. Docker Build & Publish Pipeline

1. Find all `Dockerfile*` files in the repos.
2. For each, document:
   - Base image
   - Build stages (multi-stage builds)
   - What is installed / what binary/artifact is produced
3. Find all `docker build`, `docker push`, `docker tag` commands in CI scripts, Makefiles, and shell scripts.
4. Identify which images are pushed to `fitfileregistry.azurecr.io` and under what tags/naming conventions.
5. Document ACR authentication method used in pipelines (service principal via `ACR_SERVICE_PRINCIPLE` + `ACR_SERVICE_PRINCIPLE_PASS` CI variables—confirm).
6. Find the `publish_worker_image_acr.sh` script in `data-and-analytics` and document its logic.

---

#### 3. Helm Chart Deployment Pipeline

The `helm_chart_deployment` repo is the central GitOps delivery mechanism.

1. Read and document the full directory structure:
   - `charts/`—what charts are managed, `Chart.yaml`, `values.yaml`
   - `cue/`—CUE schemas and value generation logic
   - `ffnodes/`—per-customer/cluster node definitions
   - `pipeline/`—any pipeline-specific config
   - `policies/`—OPA/Kyverno policies
   - `release-tool/`—what is `release.sh`, `release-improved.sh`?
   - `workflows/`—Argo Workflows definitions
   - `scripts/`—helper scripts (what does each do?)
   - `Makefile`—document every target

2. Trace the delivery flow:
   - How does a chart version change flow from `fitfile-version-manager` → `helm_chart_deployment` → ArgoCD → cluster?
   - What triggers a Helm release update (push to main, manual, Renovate PR)?
   - How does ArgoCD sync—polling interval, webhook, ApplicationSet?

3. Read the `renovate.json` and document what Renovate is managing.

---

#### 4. Terraform / Infrastructure Provisioning Pipeline

1. For each customer cluster repo in `Deployment/Clusters/` (read a representative sample—e.g., `mkuh-prd-4`, `hie-sde-v2`, `lca-infrastructure-prd`), document:
   - `locals.tf`—what customer-specific config is defined
   - `main.tf`—which TFC modules are called and with what parameters
   - `generators.tf`—what `infra_facts` outputs are produced for downstream CUE/Helm
   - `versions.tf`—Terraform version and provider versions
   - `workspace_vars.tf`—TFC workspace variable configuration
   - The Makefile targets (especially `make generate-values`, `make validate-cue`, `make bootstrap`)

2. Document the data flow:

   ```
   config/customer.yaml → locals.tf → main.tf (TFC module) → Terraform apply
       → terraform output infra_facts → JSON
       → cue export -t "infra=$JSON" → generated/values.yaml
       → ArgoCD reads values.yaml → Helm release
   ```

3. For `central-services`, document:
   - What GitLab resources it manages (projects, CI variables, protected branches, deploy tokens)
   - What Azure resources it provisions
   - What HCP Vault resources it manages
   - What Auth0 tenant config it drives

4. Identify how TFC workspaces are triggered—VCS-driven from GitLab, or API-triggered from CI?

---

#### 5. Secrets Management Flow

1. Find all `VaultSecret` / `VaultStaticSecret` CRD definitions in Helm chart values and `cue/` configs.
2. Document the full secret injection chain:

   ```
   HCP Vault (cloud) → Vault Secrets Operator (in-cluster K8s)
       → VaultSecret CRD → Kubernetes Secret → Pod env var / mounted file
   ```

3. Find the GitLab JWT auth configuration for Vault (how CI pipelines authenticate to Vault).
4. Read any `vault_secret_dispatch.cue` or equivalent and document how secrets are routed to the correct namespace/app.
5. Document the `ACR_SERVICE_PRINCIPLE`, `ARGOCD_STAGING_PASSWORD/USERNAME`, and any other critical CI variables used across pipelines.

---

#### 6. ArgoCD Configuration

1. Find all ArgoCD `Application` and `ApplicationSet` manifests.
2. For each, document:
   - `repoURL` and `targetRevision` (which repo/branch ArgoCD watches)
   - `path` (which directory in the repo)
   - `destination` (which cluster + namespace)
   - `syncPolicy` (automated? manual? prune? selfHeal?)
   - `helm.valueFiles` (which values files are used)
3. Find the ArgoCD Vault plugin or external secrets plugin configuration if present.
4. Identify how ArgoCD is bootstrapped per cluster—is it managed by Terraform or by the `terraform-argo-argocd` module?

---

#### 7. Application Pipeline (InsightFILE / data-and-analytics)

1. For `apps/InsightFILE`:
   - Read `.gitlab-ci.yml`—document all stages and jobs
   - Document build jobs: what services are built (`ffcloud-service`, `fitconnect`, etc.)
   - Document test jobs: what test suite is run
   - Document publish jobs: where do images land in ACR
   - Confirm the ACR auth flow (uses `ACR_SERVICE_PRINCIPLE` + Azure AD app `39cf7fc7-babb-445e-b5ad-b377f9eb3bab`)

2. For `data-and-analytics` (OMOP pipeline):
   - Document `scripts/azure_batch/`—all scripts and their roles
   - Document `Dockerfile.worker-prebaked`—what is baked in
   - Document the full Azure Batch job submission flow (`run_prebaked_e2e.sh` → Azure Batch → worker tasks)
   - Document how the built Docker image is published to ACR via `publish_worker_image_acr.sh`

---

#### 8. Environments & Promotion Flow

Document the full promotion path from code change to production:

1. Development / Feature branch → merge request pipeline → what runs?
2. `development` branch → validation pipeline → what runs?
3. `main`/`master` branch → what runs? Does it auto-deploy to staging?
4. Staging → what is the environment? Which cluster? What's the ArgoCD Application name?
5. Production → manual trigger? CAB approval? What gate exists?
6. How do customer deployments differ from the FITFILE-internal staging deployment?

---

#### 9. Version Management

1. Read `fitfile-version-manager` repo—document what output variables it exposes (e.g., `platform_module_version`, `vault_operator_chart_version`, `ingress_nginx_chart_version`, etc.)
2. Explain how a platform-wide version bump propagates:
   - Who updates `fitfile-version-manager`?
   - How do cluster repos pick up the new version?
   - Is it via Renovate, manual PR, or a CI-triggered update?

---

#### 10. CI/CD Variable Inventory

Produce a table of all CI/CD variables you can identify from:

- `.gitlab-ci.yml` files (inline `variables:` blocks)
- Shell scripts (referenced env vars)
- Terraform `workspace_vars.tf` files
- Any `cicd_minimal_permissions.md` or documentation files

| Variable Name | Scope (Group/Project) | Purpose | Sensitive? |
|---|---|---|---|
| `ACR_SERVICE_PRINCIPLE` | FITFILE Group | Azure ACR auth client ID | Yes |
| `ACR_SERVICE_PRINCIPLE_PASS` | FITFILE Group | Azure ACR auth client secret | Yes |
| `ARGOCD_STAGING_PASSWORD` | FITFILE Group | ArgoCD staging login | Yes |
| `ARGOCD_STAGING_USERNAME` | FITFILE Group | ArgoCD staging login | Yes |
| _(find all others)_ | | | |

---

### OUTPUT FORMAT

Produce a structured Markdown document with the following top-level sections:

```
# FITFILE GitLab CI/CD — Comprehensive Pipeline Documentation

## Executive Summary
(2-3 paragraphs: what the pipelines do, the overall architecture, key technologies)

## Repository Map
(Table: repo name | GitLab URL | Purpose | Has .gitlab-ci.yml?)

## 1. GitLab CI Pipeline Configurations
## 2. Docker Build & Image Publishing
## 3. Helm Chart Deployment Pipeline
## 4. Terraform / Infrastructure Provisioning
## 5. Secrets Management Flow
## 6. ArgoCD Configuration
## 7. Application Pipelines (InsightFILE, data-and-analytics)
## 8. Environment & Promotion Flow
## 9. Version Management
## 10. CI/CD Variable Inventory

## Architecture Diagram (Mermaid)
(A flowchart showing the full end-to-end delivery pipeline)

## Open Questions / Gaps Found
(Anything you could not find or confirm — be explicit about what's missing)
```

---

### CONSTRAINTS

- Do not hallucinate. If a file does not exist or you cannot find something, say so explicitly in the "Open Questions / Gaps Found" section.
- Read actual file contents. Do not infer from filenames alone—open and read every relevant file.
- Be exhaustive on `.gitlab-ci.yml` files. These are the primary CI/CD config files; document every job and stage.
- Follow cross-references. If a CI file has `include:` directives, read those too.
- Check for pipeline triggers. Look for `trigger:` keywords that kick off downstream pipelines.
- Cite file paths. Every claim must reference the file path it comes from.
