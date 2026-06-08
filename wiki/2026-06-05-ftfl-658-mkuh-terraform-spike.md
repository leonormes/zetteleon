---
created: 2026-06-05
modified: 2026-06-05
title: "FTFL-658: MKUH Terraform Failure Spike — Complete Investigation Report"
tags: [hermes, solution, terraform, mkuh, ftfl-658, spike]
source: openrouter/owl-alpha (gather + synthesis)
---

# FTFL-658: MKUH Terraform Failure Spike — Complete Investigation Report

- **Spike Period:** 27 May – 5 Jun 2026
- **Workspace:** `mkuh-prd-4` (HCP Terraform, org: FITFILE-Platforms)
- **Customer:** Milton Keynes University Hospital (MKUH)
- **Cluster:** `Clusters/eoe/Production/mkuh-prd-4/` — Azure AKS, UK South
- **Node pools:** system (D2s_v5), workflows (Spot D2s_v5)
- **VNet:** `10.104.189.128/26`

---

## 1. Executive Summary

MKUH Terraform runs in the `mkuh-prd-4` HCP Terraform workspace have been failing for over a month. The spike has identified one primary root cause and three categories of secondary issues contributing to persistent failure.

**Primary Root Cause (already fixed):** A missing `argocd_path` attribute in `generators/variables.tf` caused the `templatefile` function to fail when rendering `jumpbox.tftpl`. This was resolved in commit `FTFL-658` on 5 May 2026.

**Secondary Issues (remain open):** After the template fix, the plan succeeds but reveals significant infrastructure drift:

- **Auth0 configuration deleted out-of-band** — 6 Auth0 resources (client, resource server, credentials, grant, service account) are gone. Terraform will recreate them, generating new client IDs that will break anything hardcoding the old IDs.
- **AKS `workflows` node pool requires replace** — an immutable field (likely `vm_size`, `os_disk_size_gb`, or `node_labels`) changed, forcing a destroy-and-recreate of the pool. Workloads on this pool will be evicted.
- **Grafana Cloud policy token expired** — stale token that will be recreated on apply.
- **11 resources modified out-of-band** — AKS cluster, VNet, jumpbox VM, jumpbox NIC, jumpbox NSG, Vault KV secrets (monitoring, application, auth0, argocd), TFE workspace, and GitLab customer repo config were changed outside Terraform.
- **6 new TFE variables** credential bootstrapping (arm_*, gitlab_token) — verify correctness before apply.

**Risk Level: 🟡 Medium (with 🔴 High sub-risks)**
The plan shows 17 to add, 13 to change, 1 to destroy. No full resource group or cluster deletion.

---

## 2. Acceptance Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Root cause of Terraform failures documented | ✅ Complete |
| 2 | List of infra components to keep/change/remove agreed | ✅ Complete |
| 3 | Rollout plan reviewed and signed off by team | 🟡 Drafted — needs team review |
| 4 | Follow-up implementation ticket(s) created | 🟡 Drafted below |

---

## 3. Root Cause Analysis

### 3.1 Primary Root Cause — Template Referencing Undeclared Variable

**Error:**
```
Error: Call to function "templatefile" failed:
./templates/jumpbox.tftpl:101,36-48: Unsupported attribute;
This object does not have an attribute named "argocd_path".
```

**What happened:** The `generators/variables.tf` file was missing a variable declaration for `argocd_path`. The `jumpbox.tftpl` template referenced `${argocd_path}` at line 101 (column 36–48), but the variable was not defined in the Terraform configuration. This caused the `templatefile()` function to fail on every run.

**Fix applied 5 May 2026:** Added `argocd_path = string` to `generators/variables.tf` in commit `FTFL-658 Add 'argocd_path' to platform vault configuration`.

**How it was missed:** The variable was likely removed during a refactor of the vault/generator module and not re-added when it was referenced by the jumpbox template. No unit test or pre-apply validation caught the omission because `terraform validate` passes (it only checks syntax, not `templatefile` attribute resolution at plan time).

### 3.2 Secondary Issues — Deployment Drift Summary

| Category | Count | Details | Action |
|----------|-------|---------|--------|
| Deleted OOB | 9 | Auth0 (6): client, resource server, credentials, grant, service account + Grafana token + 2 local files | Terraform recreates them |
| Modified OOB | 11 | AKS cluster, VNet, jumpbox (VM/NIC/NSG), Vault KV secrets (4), TFE workspace, GitLab repo | Terraform reconciles |
| Replace | 1 | AKS `workflows` node pool — immutable field change | Destroy + recreate |
| Net New | 7 | `vault_kv_secret_v2.secrets["thehyve"]` + 6 TFE variables | Create (safe) |

### 3.3 Failure Timeline

| Date | Event | Status |
|------|-------|--------|
| ~April 2026 | `argocd_path` variable removed from `generators/variables.tf` during refactor | 🔴 Cause Introduced |
| ~April – 5 May 2026 | All MKUH Terraform runs fail with `templatefile` error | 🔴 Failure Period |
| 5 May 2026 | `argocd_path = string` added to variables.tf. Plan now runs cleanly. | ✅ Fixed |
| 5 May 2026 | Run shows 16 to add, 13 to change, 0 to destroy + warnings | ✅ Plan Succeeds |
| 5 May 2026 | Claude safety assessment performed — gates identified | 🟡 Assessment Done |
| Late May – 5 Jun 2026 | Run shows 17 to add, 13 to change, 1 to destroy (AKS workflows replace) | 🟡 Pending Apply |

---

## 4. Infrastructure Decisions — What to Keep, Change, Remove

### 4.1 ✅ Keep — No Changes Required

| Component | Rationale |
|-----------|-----------|
| AKS control plane | Stable, no drift detected on control plane config. VMSS-backed, Terraform-managed. |
| `system` node pool | No changes in plan. Runs system pods (coredns, metrics-server). Keep as-is. |
| VNet structure | `10.104.189.128/26` — reconfirmed in plan. Minor drift will be reconciled in-place. |
| Vault JWT backends | `jwt` and `jwt_admin` + roles — config drift is cosmetic, will be auto-reconciled. |
| ArgoCD Application manifests | Deployed separately via GitOps, not in Terraform scope. No changes needed. |
| TFE workspace configuration | Minor update in plan. Keep workspace, reconcile config. |

### 4.2 🔧 Change — Requires Modification or Reconciliation

| Component | Required Change | Risk |
|-----------|----------------|------|
| `generators/variables.tf` | Already applied. Ensure `argocd_path = string` remains. Add comment re: tftpl variable declarations. | ✅ Done |
| Vault KV secrets | 4 secrets (auth0, monitoring, application, argocd) drifted. Apply reconciles to desired state. Verify correct before apply. | 🟢 Low |
| Jumpbox NSG + NIC | Network config changed out-of-band. Apply re-reconcilies. Verify NSG rules not more permissive. | 🟢 Low |
| TFE workspace variables | 6 new `tfe_variable` resources (arm_* + gitlab_token). Verify credential values are correct. | 🟡 Medium |
| Auth0 TFE variables | `auth0_client_id` and `auth0_client_secret` will update because Auth0 resources are being recreated. | 🟡 Medium |
| Pre-apply validation | Add validation gate in CI/CD — `terraform check` block or Sentinel policy for templatefile resolution. | 🟡 Medium |

### 4.3 ❌ Remove / Recreate — Destructive Changes

| Component | Action | Impact | Recommendation |
|-----------|--------|--------|----------------|
| AKS `workflows` node pool | 🔴 REPLACE | High. All workloads on this pool evicted. Argo Workflows jobs killed mid-run. | Check for active workloads before apply. Drain gracefully. Consider if immutable field change is intentional. |
| Auth0 resources (6 items) | 🔴 RECREATE | Medium. Auth0 client and SA get new client IDs. Old IDs hardcoded anywhere will break. | Audit downstream for hardcoded IDs before apply. TFE variables auto-update, but external consumers won't. |
| Grafana Cloud access policy token | 🟡 RECREATE | Low. Token expired/deleted externally. Recreated with new value. | Verify new token propagates to consuming configs. |
| Local generator files (2) | 🟢 REGENERATE | Low. Files missing from TFC agent disk. Regenerated on apply. Normal. | No action needed. |

### 4.4 🆕 Net New — Will Be Created

| Resource | Purpose | Risk |
|----------|---------|------|
| `vault_kv_secret_v2.secrets["thehyve"]` | New KV secret for The Hyve / hutch-mkuh namespace provisioning | 🟢 Low |
| 6 TFE variables (arm_*, gitlab_token) | Credential bootstrapping into the TFE workspace for automated runs | 🟡 Medium |

---

## 5. Rollout Plan — Staged Implementation

**Goal:** Apply the Terraform plan to MKUH mkuh-prd-4 with zero disruption to live service.

### Risk Assessment

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Overall risk | 🟡 Medium | No full resource group or cluster deletion. Auth0 and node pool are the two high-value risks, both containable with pre-apply gates. |
| AKS node pool replace | 🔴 High | Workloads on `workflows` pool will be disrupted. Argo Workflows jobs could be killed mid-run. |
| Auth0 recreation | 🟡 Medium | New client IDs will break anything hardcoding old values. TFE variables auto-update, but external consumers must be identified. |
| Vault secrets update | 🟢 Low | Reconciling to desired state. Secrets exist — Terraform is correcting out-of-band changes. |
| New TFE variables | 🟡 Medium | arm_* and gitlab_token are credentials. Wrong values = pipeline failures. |
| Import viability | 🟢 None | Import removes 0 changes from this plan. Auth0 resources are actually gone; AKS node pool has immutable field change. |

### Phase 1 — Pre-apply Gates (🕐 1–2 days)

**Gate 1: Verify workloads on `workflows` node pool**
```bash
kubectl get pods -n <workflows-namespace> -o wide \
  --field-selector spec.nodeName=$(kubectl get nodes -l agentpool=workflows -o name)
```
- If active long-running Argo Workflows jobs exist → wait for completion or drain gracefully
- If no active workloads → proceed (node pool is likely Spot with taints preventing system pods)
- If the immutable field change is unintentional → consider reverting the config to avoid the replace entirely

**Gate 2: Audit Auth0 client ID hardcodes**
- Old client ID: `gTJ4gooBkk4rhs59ljPqWvroUbtyCiZM`
- Old SA client ID: `fTmHPJXG7jaUbX6Ti7etRor6ExcrMFUn`
- Search across: app configs, k8s secrets, Helm values, CI/CD variables, external service integrations
- Anything outside TFE variables will NOT be auto-updated and will break

### Phase 2 — Apply to Lower Environment (🕐 1 day)
- Test the plan on a non-production workspace first (`ffuh-prd-1` is closest)
- Use `terraform plan -target` on isolated resource groups to validate drift reconciliation
- Verify Auth0 recreation works as expected (new IDs generated, TFE variables updated)
- Verify node pool replace completes without cluster disruption

### Phase 3 — MKUH Production Apply (🕐 4h window)
**Staged apply sequence:**
1. Apply Vault secrets and TFE variables (low risk)
2. Apply jumpbox NSG/NIC drift reconciliation (low risk, reversible)
3. Apply Auth0 recreation — verify new client IDs appear in TFE variables immediately
4. Apply AKS `workflows` node pool replace — during a maintenance window
5. Apply remaining drift reconciliation (Vault JWT backends, TFE workspace, etc.)

### Phase 4 — Post-apply Verification (🕐 2h)
**Validation checklist:**
- [ ] `kubectl get nodes` — all nodes Ready, workflows pool recreated
- [ ] `kubectl get pods -A` — all system + customer pods running, no CrashLoopBackOff
- [ ] Auth0 — new client IDs in TFE variables, app login still works
- [ ] Vault — KV secrets readable, JWT auth still functional
- [ ] ArgoCD — apps synced, health status green
- [ ] Jumpbox — SSH connectivity via new NSG/NIC config
- [ ] Fresh `terraform plan` — should show zero changes (clean state)

### Phase 5 — Guardrails (🕐 0.5 day)
- Add Sentinel policy or `terraform check` block validating all `*.tftpl` template variable references have corresponding declarations
- Add pre-apply validation in GitLab CI that runs `terraform validate` + `terraform plan` on every MR
- Consider adding drift detection cron (weekly `terraform plan` with notification on changes)
- Document the `generators/variables.tf` convention in the repo README

---

## 6. Pre-apply Gates (from Safety Assessment)

### 🔴 Gate 1 — Node Pool Workloads
Run this command to check if anything is currently running on the `workflows` node pool:
```bash
kubectl get pods -n <your-workflows-namespace> -o wide
```
If any long-running Argo Workflows jobs are active, wait for them to finish or drain the node pool gracefully before applying. The `workflows` pool uses Spot VMs (D2s_v5) and is likely tainted to accept only batch workloads, but confirm.

### 🟡 Gate 2 — Auth0 Client ID Hardcodes
The Auth0 client and service account will be recreated with new IDs. Check every system that might have the old IDs hardcoded:
- Application configuration files
- Kubernetes secrets
- Helm values files
- CI/CD pipeline variables (outside TFE)
- External service integrations that authenticate via Auth0

**Old client ID:** `gTJ4gooBkk4rhs59ljPqWvroUbtyCiZM`
**Old SA client ID:** `fTmHPJXG7jaUbX6Ti7etRor6ExcrMFUn`

TFE variables for `auth0_client_id` and `auth0_client_secret` will be auto-updated — but anything outside Terraform's purview will not.

---

## 7. Detailed Risk Assessment

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Overall risk | 🟡 Medium | No full resource group or cluster deletion. Auth0 and node pool are containable with pre-apply gates. |
| AKS node pool replace | 🔴 High | Workloads on `workflows` pool disrupted. Argo Workflows jobs could be killed mid-run. |
| Auth0 recreation | 🟡 Medium | New client IDs break hardcoded values. TFE variables auto-update, external consumers don't. |
| Vault secrets update | 🟢 Low | Reconciling to desired state. Secrets exist. |
| New TFE variables | 🟡 Medium | arm_* and gitlab_token are credentials. Verify before apply. |
| Import viability | 🟢 None | Import removes 0 changes. Auth0 and Grafana resources are actually deleted. |

---

## 8. Follow-up Implementation Tickets

### Ticket 1: [IMPLEMENT] Apply MKUH Terraform Plan to mkuh-prd-4
- **Priority:** High | **Sprint:** Next
- **Description:** Execute the rollout plan (Phases 1–4) in the MKUH production workspace. Check the two pre-apply gates, apply in stages (Vault → Auth0 → node pool → drift reconciliation), and run full post-apply verification.
- **Depends on:** This spike report sign-off

### Ticket 2: [GUARDRAIL] Add template variable validation to Terraform CI/CD
- **Priority:** Medium | **Sprint:** Next + 1
- **Description:** Add a pre-apply validation step (Sentinel policy, `terraform check` block, or GitLab CI job) that verifies all variables referenced in `*.tftpl` template files have corresponding declarations in `generators/variables.tf`. Prevents recurrence of the root cause.

### Ticket 3: [AUDIT] Audit Auth0 consumer configurations across all TFC workspaces
- **Priority:** Medium | **Sprint:** Backlog
- **Description:** MKUH's Auth0 consumer was deleted out-of-band. Audit all Auth0 consumer configurations across all HCP Terraform workspaces to ensure no other customer environments have silently lost Auth0 resources.

### Ticket 4: [DRIFT] Investigate MKUH out-of-band changes
- **Priority:** Low | **Sprint:** Backlog
- **Description:** 11 resources in the MKUH workspace were modified outside Terraform. Investigate who/what made these changes and why. Add drift detection monitoring if needed.

---

## 9. Appendix — Terraform Import Commands (for Reference)

Even though import cannot fix the current plan (Auth0 resources are gone, AKS node pool has immutable field change), these commands are documented for future reference:

```bash
# Auth0 resource server
terraform import 'module.central_services.module.auth0_consumer[0].auth0_resource_server.api' '69b94ac13b1621df30c0dc3a'

# Auth0 main client
terraform import 'module.central_services.module.auth0_consumer[0].auth0_client.client' 'gTJ4gooBkk4rhs59ljPqWvroUbtyCiZM'

# Auth0 service account client
terraform import 'module.central_services.module.auth0_consumer[0].auth0_client.service_account["Milton Keynes University Hospital Service Account"]' 'fTmHPJXG7jaUbX6Ti7etRor6ExcrMFUn'

# Auth0 client credentials (main)
terraform import 'module.central_services.module.auth0_consumer[0].auth0_client_credentials.client_credentials' 'gTJ4gooBkk4rhs59ljPqWvroUbtyCiZM'

# Auth0 client credentials (service account)
terraform import 'module.central_services.module.auth0_consumer[0].auth0_client_credentials.service_account_credentials["Milton Keynes University Hospital Service Account"]' 'fTmHPJXG7jaUbX6Ti7etRor6ExcrMFUn'

# Auth0 client grant
terraform import 'module.central_services.module.auth0_consumer[0].auth0_client_grant.client_grant_self' 'cgr_uRc6hDLCdJMsKPLB'

# Grafana Cloud access policy token
terraform import 'module.central_services.grafana_cloud_access_policy_token.deployment[0]' 'prod-gb-south-0:25b3c970-1a1c-46ce-ab97-5479c7873d00'
```

> Note: Since this is a TFC-managed workspace, these would need to run as a TFC run with import, not locally — or via a Terraform `import` block in the config for a plan-time import.