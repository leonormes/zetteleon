---
type: playbook
target_service: argocd
trigger: "ArgoCD Application Sync Failed with 401 Unauthorized against Helm Registry"
severity: p2
status: active
last_verified: 2026-02-22
tags: [playbook, argocd, vso, oci, registry, auth, failure]
---

# Playbook: ArgoCD VSO OCI Registry Authentication Failure

## ⚠️ Symptoms

> **When to use this:** ArgoCD applications show `Unknown` sync status with a `ComparisonError` mentioning `helm registry login` failures, `401 unauthorized`, or `Invalid clientid or client secret` against an OCI Helm registry — and your registry credentials are managed by HashiCorp Vault Secrets Operator (VSO) dynamic secrets.

- ArgoCD Application sync status: `Unknown`
- ArgoCD Application health status: `Healthy` (previously deployed resources still running)
- Condition type: `ComparisonError`

---

## 🧠 Mental Model / Architecture

Before debugging, it is critical to understand that there are **two separate credential paths** for an OCI container registry in a Kubernetes + ArgoCD + VSO setup:

| Credential Path | Consumer | Used For | K8s Secret Type |
|---|---|---|---|
| Image Pull Secret | kubelet | Pulling container images at pod scheduling time | `kubernetes.io/dockerconfigjson` |
| ArgoCD Repository Secret | ArgoCD repo-server | `helm registry login` to fetch OCI Helm charts | `Opaque` with ArgoCD labels |

Both may be sourced from the **same Vault dynamic secrets engine** (e.g. `azure/creds/acr-pull`) but are written to **different K8s Secrets** by **different VaultDynamicSecret CRs**. Fixing one does not fix the other.

Additionally, ArgoCD has **two types** of repository credential secrets:
- `repo-creds` (Template match, takes priority)
- `repository` (Exact match)

A stale `repo-creds` secret will silently override a valid `repository` secret.

---

## Phase 0: Context Establishment

1. **Get an overview of failing applications**
   ![[cmd_argocd_get_app#1. The Command]]

---

## Phase 1: Diagnosis

*Identify the exact drift/failure symptom and trace back down the credential chain to find the problem secret.*

1. **Get Operation State Message**
   ![[cmd_kubectl_argocd_get_app_operation_state#1. The Command]]

2. **Confirm Helm Source and Registry URL**
   ![[cmd_kubectl_argocd_get_app_source#1. The Command]]

3. **Find All Secrets Claiming this Registry URL**
   ![[cmd_kubectl_argocd_find_repo_secrets#1. The Command]]
   ![[cmd_kubectl_argocd_find_repo_creds#1. The Command]]
   ![[cmd_kubectl_find_image_pull_secrets#1. The Command]]

4. **Verify if Credentials in ArgoCD Secret match the valid Image Pull Secret**
   *If the passwords differ, the ArgoCD repo secret holds stale credentials.*
   ![[cmd_kubectl_argocd_get_secret_creds#1. The Command]]
   ![[cmd_kubectl_get_image_pull_secret_creds#1. The Command]]

5. **Examine the VaultDynamicSecret Spec (VSO status)**
   *The `overwrite` property is critical. If `false`, VSO will not overwrite existing secrets and breaks dynamic lease rotation.*
   ![[cmd_kubectl_get_vso_cr_details#1. The Command]]

---

## Phase 2: Remediation

*Fix the VSO configuration, purge stale secrets, and force system caches to drop memory structures referencing dead tokens.*

> [!DANGER] Destructive Action
> Deleting non-VSO managed `repo-creds` or `repository` secrets permanently removes manual configurations. Only delete manual secrets if you have verified they are overriding VSO intentionally.

1. **Delete Stale Application Secrets**
   *VSO will recreate dynamic secrets automatically within seconds once they are deleted.*
   ![[cmd_kubectl_recreate_vso_secret#1. The Command]]

2. **Patch all affected VaultDynamicSecrets to use `overwrite: true`**
   *IMPORTANT: You must eventually push this change into parameterised code (Helm, Terraform).*
   ![[cmd_kubectl_patch_vso_overwrite#1. The Command]]

3. **Restart Repo-Server to Flush In-Process Cache**
   *ArgoCD repo-server caches registry credentials. A fresh K8s Secret doesn't instantly reload the cache.*
   ![[cmd_kubectl_restart_argocd_repo_server#1. The Command]]

---

## Phase 3: Final Verification

*Force ArgoCD to synchronize and check if the Reflector mirror architecture is stable.*

1. **Force Hard Refresh on Errored Applications**
   ![[cmd_kubectl_bulk_hard_refresh_argocd_apps#1. The Command]]

2. **Verify Reflector Replicas (If using emberstack reflector on the image-pull side)**
   ![[cmd_kubectl_verify_reflector_sync#1. The Command]]

---

## Post-Incident Checklist

- [ ] All ArgoCD repo/repo-creds secrets for the registry are VSO-managed (no manual secrets)
- [ ] All relevant `VaultDynamicSecret` CRs have `overwrite: true`
- [ ] The `overwrite: true` change is committed to Git source manifests (not just `kubectl patch`)
- [ ] No `repo-creds` secrets silently overriding `repository` secrets for the same URL
- [ ] Repo-server restarted and all affected applications show `Synced`
- [ ] Reflector-mirrored copies of image pull secrets are up to date
