---
created: 2026-08-27T10:30:00+00:00
modified: 2026-08-27T10:30:00+00:00
permalink: llmeon/30-library/200-projects/fitfile-audit-security-findings-and-remediation
project_category: refined_deployment
project_name: Pipeline
project_status: active
date: 2026-08-27
related_tickets: [FTFL-973, FTFL-974, FTFL-975, FTFL-976, FTFL-951, FTFL-1015, FTFL-512]
tags: [audit, ci-cd, remediation, security, supply-chain, maturity]
title: FITFILE Audit - Security Findings and Remediation
type: audit
---

## Security Findings & Remediation

Section of [[FITFILE Delivery Pipeline Audit 2026-08-27]]. Verified live 2026-08-27.

**16 open findings · 3 resolved.** Severity reflects reachability, not theoretical impact. Each finding records status against the previous audit where one exists.

---

### S-01 · Critical · New

**Every group-level CI secret is unprotected, giving any branch push a path to cluster-admin**

All ten group-level CI/CD variables on the `fitfile` group are `protected: false` with `environment_scope: "*"`. Protected variables are exposed only to protected branches and tags; unprotected ones are exposed to **every branch in every one of the 140 projects**, including a brand-new feature branch. Masking prevents a verbatim echo into logs but is trivially defeated by re-encoding.

```
glab api groups/fitfile/variables

ACR_SERVICE_PRINCIPLE        protected=false  masked=true
ACR_SERVICE_PRINCIPLE_PASS   protected=false  masked=true
ARGOCD_STAGING_PASSWORD      protected=false  masked=true
ARGOCD_STAGING_USERNAME      protected=false  masked=false
AZ_CLIENT_ID                 protected=false  masked=true
AZ_CLIENT_SECRET             protected=false  masked=true
DOCKER_HUB_DEPLOY_TOKEN      protected=false  masked=true
GCR_PASSWORD                 protected=false  masked=true
GCR_USERNAME                 protected=false  masked=false
RUNTIME_ACCESS_TOKEN         protected=false  masked=true
```

**The reachable chain, every link verified:**

1. **Push any branch to any project.** No approval is required anywhere (S-02), and unprotected variables are exposed to all branches.
2. **Read `AZ_CLIENT_SECRET` and `ACR_SERVICE_PRINCIPLE_PASS`.** A one-line job in the attacker's own `.gitlab-ci.yml` reads both from the environment.
3. **Obtain cluster-admin on AKS.** `staging.gitlab-ci.yml` shows the exact call: `az login --service-principal -u $AZ_CLIENT_ID -p $AZ_CLIENT_SECRET` then `az aks get-credentials … --admin`, which bypasses Azure AD RBAC entirely.
4. **Push a malicious image both clusters will pull.** `acr-service-principal` holds **AcrPush on FITFILEPublic** — the registry serving `argoproj/argocd:v3.5.1` to production and staging. Overwriting that tag compromises the GitOps controller on both.

Step 4 is the sharpest edge: the credential used for routine image builds can publish to the registry that supplies the cluster's own control plane, and that registry additionally permits anonymous pull.

---

### S-02 · Critical · FTFL-975 not done

**Merges to auto-deployed branches require neither a passing pipeline nor a reviewer**

Every project examined requires **zero approvals**. Approval rules exist but are all configured `approvals_required: 0`. Three of five projects, including InsightFILE and the GitOps `deployment` repo, also have `only_allow_merge_if_pipeline_succeeds: false`.

```
glab api projects/…/approvals + /approval_rules

InsightFILE         approvals_before_merge=0   RULE Engineers: required=0    pipeline_gate=false
deployment          approvals_before_merge=0   RULE All Members: required=0  pipeline_gate=false
ude-cli             approvals_before_merge=0   RULE Engineers: required=0    pipeline_gate=true
data-and-analytics  approvals_before_merge=0   RULE team: required=0         pipeline_gate=false
central-services    —                                                        pipeline_gate=true
```

**Last known:** FTFL-975 open — "enable pipelines must succeed"
**Now:** Still disabled on InsightFILE, deployment and data-and-analytics. Enabled only on ude-cli and central-services.

Two independent corroborations. First, InsightFILE's own `.gitlab-ci.yml` contains a `mr_pipeline_guard` job whose comment states *"With 'Pipelines must succeed' now enabled on this project…"* — **that comment is stale**; the gate it describes is off, so the workaround guards a gate that does not exist. Second, [[FTFL-512_CICD_Incident_Report]] records an 8h47m outage caused by a chart change *"solo-merged by a single engineer with no reviewer"* where *"the merge button is gated on neither CI nor review."*

---

### S-03 · Critical · FTFL-976 not done

**ArgoCD staging credentials remain unprotected and partly unmasked**

`ARGOCD_STAGING_PASSWORD` is `protected=false`; `ARGOCD_STAGING_USERNAME` is both unprotected and `masked=false`. These reach the ArgoCD instance at `testing-argocd.fitfile.net`, which controls sync for every staging namespace.

**Last known:** FTFL-976 open — "protect ARGOCD_STAGING_* variables"
**Now:** Unchanged. Both still unprotected; username still unmasked.

---

### S-04 · High · FTFL-973 code fixed

**ACR token leak fixed in code, but the exposed logs were never purged**

The leak was real and recent. Job `16068637438` (`get_staging_images`, 2026-08-24) printed a 1,037-character JWT to its log. Root cause was a bare `echo $token` in `get_staging_images.sh`, which requested scope `repository:*:*`.

```
git log — deployment/pipeline/common/get_staging_images.sh
cb16fb281  2026-08-26  FTFL-973: Remove token echo log leak in get_staging_images.sh
   -echo $token

Live JWT-pattern scan of job traces (values never read)
job 16068637438  2026-08-24T13:18Z  JWT-in-log=1   <- still retrievable 2026-08-27
job 16121359511  2026-08-26T14:02Z  JWT-in-log=1   <- still retrievable
job 16124287079  2026-08-26T15:50Z  JWT-in-log=0
job 16125169965  2026-08-26T16:29Z  JWT-in-log=0
```

**Last known:** Live JWT observed in job 16068637438; rotation + log redaction required
**Now:** Code fixed 2026-08-26 (took effect between 14:02 and 15:50). **Logs not purged** — two traces still return a token today. **Credential not rotated** — the underlying secret still dates from 2026-04-21.

The leaked artefact was a short-lived ACR access token rather than the SP password, so the direct window has closed. Outstanding work is deleting the two job logs and rotating the source credential, which is due before 2026-10-18 in any case (S-07).

---

### S-05 · High · New

**Registry hardening controls are off, and the network allowlist is inert**

Admin user — a static, shared, non-attributable credential — is enabled on **both** registries. `FITFILEPublic` additionally permits **anonymous pull**. On `Fitfileregistry`, content trust, quarantine, retention and soft-delete are all disabled, and the IP allowlist sits under `defaultAction: "Allow"`, making it decorative.

Detail in [[FITFILE Audit - ACR and Identity]]. That the CI credential holds AcrPush on the anonymous-pull registry (S-01 step 4) is what elevates this from hygiene to exposure.

---

### S-06 · High · New

**Production Terraform state sits unencrypted on a local volume**

**49** `.tfstate` files exist under the local repo root, including for production customer environments. Terraform state stores provider attributes in plaintext.

The `fitfile-bootstrap` state is the concerning one — 72K, 23 resources, holding Vault and GitLab bootstrap material with `client_secret`, `encryption_key` and `import_url_password` attribute keys present. Only attribute *names* were enumerated; no values read.

These sit in `Deployment/Clusters`, which is **not a git repository**, so there is no `.gitignore` protecting them and no record of who has copied them. Full listing in [[FITFILE Audit - Terraform and IaC State]].

---

### S-07 · High · FTFL-974 partial

**The single shared registry credential expires on 2026-10-18**

All four application repos authenticate to ACR with the same `ACR_SERVICE_PRINCIPLE` / `ACR_SERVICE_PRINCIPLE_PASS` pair. The active secret runs 2026-04-21 → **2026-10-18**. When it lapses, every image build across the estate fails at once, with no staged fallback.

**Unresolved:** `acr-service-principal` holds only *Reader* on `Fitfileregistry`, which cannot authorise a push — yet pushes succeed. Most likely `ACR_SERVICE_PRINCIPLE` holds the **registry admin username** rather than the SP's app ID. Inference from behaviour, not confirmation — the variable is masked.

---

### S-08 · High · FTFL-951 / FTFL-1015 incomplete

**The Renovate service principal was created but never granted any permission**

`sp-renovate-acr-pull` was created 2026-08-26 with a two-year secret but holds **no role assignment in any subscription**. It cannot pull from private ACR. The work is half-landed: the identity exists, the grant does not. The two-year secret lifetime should also be shortened when the grant is added.

---

### S-09 · High · New

**The GitOps repository permits force-push to master**

`fitfile/deployment` — the repository ArgoCD treats as source of truth for every cluster — has `allow_force_push: true` on `master`. History on the branch that defines production can be rewritten, defeating reconstruction of what was deployed when.

```
glab api projects/fitfile%2Fdeployment/protected_branches

BRANCH master:  push=Ollie Rushton, gapv-deployment-access-token
                merge=Maintainers, Developers + Maintainers
                force_push=true   code_owner_approval=true
BRANCH staging: push=Ollie Rushton  merge=Ollie Rushton
                force_push=false  code_owner_approval=false
```

The same output shows a **single named individual** as the only push and merge path on `staging`, and one of two on `master` — a concentration risk independent of the force-push setting.

---

### S-10 · Medium · New

**Vulnerability scanning is absent on the testing cluster and stale in production**

The testing cluster has Trivy CRDs and 27 VulnerabilityReports dated **November 2024** — 21 months old — with **no running workload** in `trivy-system`. The operator was removed and its reports left behind, so a dashboard reading these shows reassuring, meaningless data.

Production runs trivy-operator `0.25.0` against staging's `0.33.0`, and lacks the EPSS/KEV exporter and VEX cache proxy staging has — production has the weakest prioritisation signal of the three. Detail in [[FITFILE Audit - AKS and ArgoCD Topology]].

---

### S-11 · Medium · Re-measured

**Live vulnerability counts**

Measured 2026-08-27T10:25Z. Previously circulated figures (741 Critical / 1233 High / 2320) do not match current state and should be retired. Full table in [[FITFILE Audit - AKS and ArgoCD Topology]].

Staging: 203 Critical / 1,544 High across 102 reports. Production: 189 Critical / 1,563 High across 64 reports. Config audit: 0 Critical on both.

`argoproj/argocd:v3.5.1` carries 2 Critical / 22 High; `dexidp/dex:v2.45.1` carries **5 Critical / 43 High**. SBOM export works: 340 SBOMReports staging, 148 production, 30 stale on testing.

---

### S-12 · Medium · New

**Short-lived tokens are baked into image build arguments**

Three of four repos pass `CI_JOB_TOKEN` as a Docker `--build-arg`. Build arguments persist in image metadata and are readable with `docker history` by anyone who can pull the image — which, for anything mirrored to `FITFILEPublic`, is anyone.

```
InsightFILE  build.sh:  --build-arg GIT_AUTH_TOKEN="${CI_JOB_TOKEN}"
data-and-analytics:      --build-arg AUTH_TOKEN="${CI_JOB_TOKEN}"
workflows-api:           --build-arg AUTH_TOKEN="${CI_JOB_TOKEN}"
```

InsightFILE also pushes build cache with `--cache-to type=registry,mode=max`, publishing intermediate layers and widening the same exposure. Job tokens are short-lived, which caps impact, but the pattern should move to BuildKit secret mounts.

---

### S-13 · Medium · New

**Deployed state is not reproducible from any revision**

No ArgoCD Application pins an immutable revision. Staging tracks `master`, production tracks the movable tag `latest-release`, one app tracks `HEAD`, and Helm sources use floating ranges `2.0.*` and `0.45.*`. Combined with force-push on `master` (S-09), no revision reliably reconstructs a past deployment. [[FTFL-512_CICD_Incident_Report]] reached the same conclusion independently.

This is not a two-environment problem. Every customer tenant runs its own ArgoCD instance, bootstrapped by Terraform, tracking the same `deployment.git` app-of-apps at a customer-specific tag (see [[FITFILE Audit - AKS and ArgoCD Topology]] §2) — equally mutable, and multiplying the coordination problem across every customer rather than just staging and production. There is no single place to see which customer is running which version of what.

---

### S-14 · Medium · New

**Half of Terraform workspaces float their CLI version; a fifth last failed**

27 of 54 workspaces set `terraform-version: "latest"`, so an upstream release can break an apply with no change on FitFile's side. Separately, 11 workspaces last errored and 20 have no VCS repo attached, meaning applies happen without a commit or review trail. Five hold 45–53 live resources with no recorded run at all.

Production customer environments are affected: `hie-prod-35` (144 resources) errored since 2026-07-30; `lca-prd-2` (73 resources) since 2026-04-13. Detail in [[FITFILE Audit - Terraform and IaC State]].

---

### S-15 · Medium · New

**Production API servers are public and trail non-production on version**

All three `fitfile-cloud-*` clusters, including production, expose public Kubernetes API servers (`enablePrivateCluster: false`). The newer `aks-ff-uks-gp-*` clusters are private, so the better pattern exists internally but has not been retrofitted. Production runs Kubernetes `1.35.7` against non-production's `1.36.3`.

---

### S-16 · Medium · New

**Deployment configuration and Helm charts live outside version control**

`Deployment/Clusters` holds **5,149 files** with no git repository — including every `customer.yaml` defining production customer network ranges, node pools and backup scope, and (in NNUH-DP's case) a `deployment_key` field. `Deployment/new-helm/fitfile-platform` and `…/customer-nhs-trust-b` are git repos with no remote — local-only, unbacked, unreviewable.

---

## Resolved since the last audit

### R-01 · CI job token inbound scoping is correctly enforced

Confirmed active with tight allowlists — not merely enabled but correctly narrowed. The legacy `ci_job_token_scope_enabled` attribute is indeed no longer writable; the current `job_token_scope` API is the right surface.

```
InsightFILE  inbound=true  outbound=false  allowlist: [InsightFILE, deployment]
deployment   inbound=true  outbound=false  allowlist: [deployment]
ude-cli      inbound=true  outbound=false  allowlist: [ude-cli]
```

### R-02 · Forward deployment protection is enabled across all projects

`ci_forward_deployment_enabled: true` on every project checked, preventing outdated deployment jobs from running out of order.

### R-03 · ArgoCD upgraded from v3.4.4 to v3.5.1

Both clusters now run v3.5.1. The upgrade landed, though the image still carries 2 Critical CVEs and its bundled Dex carries 5 — the upgrade cadence needs to continue rather than be considered closed.

---

## Control maturity assessment

Levels: **1** ad hoc · **2** repeatable but unenforced · **3** defined and enforced · **4** measured · **5** optimising. Capability sits a level or two above enforcement almost everywhere.

| Control domain | Level | Basis |
|---|---|---|
| Secrets management | **1** | All group secrets unprotected and wildcard-scoped; one shared registry credential across four repos; tokens in build args; state files on local disk. |
| Artifact & registry integrity | **1** | Admin user on both registries; anonymous pull on the registry serving the GitOps controller; no signing, no quarantine, inert network allowlist. |
| Change control & review | **2** | Protected branches and code-owner rules exist, but zero required approvals everywhere and no pipeline gate on three of five projects. Force-push permitted on GitOps master. |
| Build & test | **2** | Mature path-filtered monorepo pipelines with merge trains and shared build scripts — but self-documented coverage blind spots (FTFL-877) and inconsistent Docker/Python pinning. |
| Infrastructure as code | **2** | Well-factored reusable modules and a real TFC estate, undermined by floating CLI versions, 37% of workspaces off-VCS, and 20% last-errored with no remediation loop. |
| GitOps deployment | **2** | ArgoCD deployed and healthy with automated sync, but no immutable pinning anywhere and a major-version parity gap between staging and production. |
| Identity & access | **2** | Workload identity and AcrPull scoping used correctly for kubelets, but 69% of registry role assignments orphaned, CI uses `--admin` cluster credentials, one SP has a two-year secret and no grant. |
| Vulnerability management | **3** | Strongest domain: Trivy Operator, SBOM generation, EPSS/KEV prioritisation, VEX repository with CI validation gate. Held back by no coverage on testing, stale operator in production, detection only after deployment. |
| Delivery observability | **2** | Grafana Cloud and Alloy deployed and healthy, but FTFL-512 records 7h40m of silent `Degraded` state with no alert — sync failure is not currently an alerting signal. |

### The recurring pattern

Four separate mechanisms look like controls and enforce nothing: the ACR IP allowlist under `defaultAction: Allow`; approval rules set to zero approvers; the `mr_pipeline_guard` job defending a merge gate that is switched off; and 27 stale Trivy reports on a cluster with no scanner. Each would pass a checklist asking *"is it configured?"* and fail one asking *"what does it reject?"*

**Remediation should verify enforcement, not presence.**

---

## Remediation plan

### Immediate — this week

| # | Action | Finding | Effort |
|---|---|---|---|
| 1 | Set `protected: true` on all ten group variables and narrow `environment_scope` from `*`. Mask `ARGOCD_STAGING_USERNAME` and `GCR_USERNAME`. Verify protected branches are correctly defined first, or pipelines will break. | S-01, S-03 | Low |
| 2 | Delete job logs `16068637438` and `16121359511`, then rotate `ACR_SERVICE_PRINCIPLE_PASS`. | S-04 | Low |
| 3 | Grant `sp-renovate-acr-pull` AcrPull on `Fitfileregistry` and reduce its secret lifetime from two years. | S-08 | Low |
| 4 | Set `allow_force_push: false` on `fitfile/deployment` master. | S-09 | Low |
| 5 | Diarise the 2026-10-18 ACR credential expiry as a change, with a rotation runbook. | S-07 | Low |

### Short term — this month

| # | Action | Finding | Effort |
|---|---|---|---|
| 6 | Enable `only_allow_merge_if_pipeline_succeeds` on InsightFILE, deployment and data-and-analytics; set approval rules to at least 1. Then correct the stale comment in InsightFILE's `mr_pipeline_guard`. | S-02 | Low |
| 7 | Set `networkRuleSet.defaultAction` to `Deny` on `Fitfileregistry` so the existing allowlist takes effect — validate runner egress IPs first, since GitLab SaaS runners lack stable addresses. Private endpoints are the durable answer. | S-05 | Medium |
| 8 | Replace admin-user auth with a scoped AcrPush service principal or workload identity; disable admin user on both registries once builds are migrated. | S-05, S-07 | Medium |
| 9 | Remove the 24 orphaned ACR role assignments so the access list becomes reviewable. | ACR | Low |
| 10 | Reinstate Trivy Operator on the testing cluster and delete the 27 stale 2024 reports. Upgrade production's operator to match staging's 0.33.0. | S-10 | Medium |
| 11 | Move the 49 local state files into TFC or a secured backend; add `*.tfstate` to ignore rules and bring `Deployment/Clusters` under version control. Treat `fitfile-bootstrap` material as exposed and rotate it. | S-06, S-16 | Medium |
| 12 | Replace `--build-arg` token passing with BuildKit `--secret` mounts across all three repos. | S-12 | Low |

### Structural — this quarter

| # | Action | Finding | Effort |
|---|---|---|---|
| 13 | Replace `az aks get-credentials --admin` in CI with a workload-identity federated credential scoped to a namespace-limited role — removing the strongest link in the S-01 chain. | S-01 | High |
| 14 | Pin every ArgoCD Application to an immutable revision (tag or SHA) and replace floating Helm ranges with exact versions. | S-13 | Medium |
| 15 | Close the staging/production parity gap — argo-workflows 0.45 vs 2.0 is the urgent one — and align Kubernetes versions so staging tests what production runs. | S-15 | High |
| 16 | Pin `terraform-version` on all 27 floating workspaces; triage the 11 errored workspaces, prioritising `hie-prod-35`, `lca-prd-2` and `fitfile-entra-id`; attach VCS repos to the 20 workspaces lacking them. | S-14 | High |
| 17 | Add container scanning and secret detection to all four application pipelines so vulnerable images are blocked before push, not detected after deployment. | Inventory | Medium |
| 18 | Migrate the three `fitfile-cloud-*` clusters to private API servers, matching the `aks-ff-uks-gp-*` pattern already in use. | S-15 | High |
| 19 | Alert on ArgoCD `Degraded` and `OutOfSync` state — the FTFL-512 incident ran 7h40m unnoticed. Adopt the ~5-line Rego policy that review recommends. | Observability | Medium |

---

## Open questions & gaps

### Could not be verified with available access

- **Customer-tenant clusters.** NNUH-DP, LCA-DP, MCNFT and mkuh-prd-4 run in customer-owned Azure tenants (`NNUHFT-SDE` sits under tenant `d2a06081-…`), each with its own ArgoCD instance bootstrapped by Terraform (see [[FITFILE Audit - AKS and ArgoCD Topology]] §2). No credential in this environment reaches those tenants, so per-customer sync status, tag drift, Trivy coverage and cluster posture are all unassessed. **This is the single largest gap** — it is where NHS patient data actually lives.
- **The value of `ACR_SERVICE_PRINCIPLE`.** Masked. The inference that it holds the registry admin username rests on `acr-service-principal` having only Reader on `Fitfileregistry` while pushes succeed. Someone with variable read access should confirm — it determines whether disabling admin user is a one-line change or a pipeline migration.
- **Whether the 24 orphaned principals were AKS kubelets or something else.** Deleted directory objects cannot be resolved retrospectively. Azure Activity Log retention may still cover some.
- **The five workspaces holding resources with no recorded run.** Whether state was migrated, pushed via API, or runs were pruned is not visible from the workspace API alone.
- **Grafana alerting rules.** The Grafana Cloud MCP connector is not authorised in this session, so alert coverage for ArgoCD sync failure was inferred from [[FTFL-512_CICD_Incident_Report]] rather than read directly.

### Worth a decision

- **The `cuh-prod-1` namespace on the staging cluster.** A production-named customer namespace on non-production infrastructure. Either the name is misleading or the placement is.
- **Naming that misleads.** `staging.gitlab-ci.yml` deploys to `Fitfile-cloud-testing-aks-cluster` and `testing-argocd.fitfile.net`. FTFL-512 cites the same confusion as contributing to an outage.
- **Two divergent Obsidian vault copies.** `~/Documents/LMeon` and `/Volumes/DAL/Zettelkasten/LLMeon` are separate directories on separate devices, two weeks apart. Runbooks read from the wrong one will be stale.
- **The documented standard is stricter than reality.** [[cicd_minimal_permissions]] specifies two required approvals, `reject_unsigned_commits`, `allow_force_push: false` and required `terraform/plan` + `security/scan` status checks. None is implemented, and the note is marked `archived`. Either adopt it or retire it — a documented standard nobody enforces is a liability in an assurance review.
- **A stale project-type runner** (`3149836`) remains registered to InsightFILE.

---

### Related

- [[FITFILE Delivery Pipeline Audit 2026-08-27]] — hub
- [[FITFILE Audit - Repo and Pipeline Inventory]] · [[FITFILE Audit - Terraform and IaC State]] · [[FITFILE Audit - ACR and Identity]] · [[FITFILE Audit - AKS and ArgoCD Topology]]
- [[FTFL-512_CICD_Incident_Report]] · [[cicd_minimal_permissions]] · [[Integrate Security into the Workflow (Shift Left)]]
