---
type: playbook
target_service: argocd
incident_type: auth_failure
tags: #playbook #argocd #oci #acr
---

# Playbook: Debugging ArgoCD Helm OCI Auth (401 Unauthorized)

## 🧭 Trigger Condition
- ArgoCD fails to generate manifests for OCI-based Helm charts.
- Error: `helm dependency build failed... 401: unauthorized (cached)`.

---

## 🧱 Execution Flow

### Phase 1: Local Credential Validation
1. Check if the Service Principal secret has expired:
   ![[cmd-az-check-sp-expiry#⚡ Action]]

2. Verify login and pull ability from a local CLI to isolate registry issues:
   ![[cmd-helm-oci-pull-test#⚡ Action]]

### Phase 2: Configuration Integrity
1. Ensure the ArgoCD Project permits OCI sources:
   ![[cmd-k8s-patch-appproject-source#⚡ Action]]

2. **Check for "Zsh Artifacts":** Run `cat -e` on any secret file to ensure no trailing `%` or `~` were accidentally included in passwords.

### Phase 3: The "Nuclear" Cache Flush
*If credentials are verified but ArgoCD still reports 401, the cache is stale.*

1. Flush Redis, the Controller, and the Repo Server:
   ![[cmd-argocd-flush-cache#⚡ Action]]

2. Trigger a hard refresh on the failing application:
   ![[cmd-k8s-refresh-argocd-app#⚡ Action]]

---

## 🧠 End State
Success = 
- Application transitions to `Synced`.
- No `401 Unauthorized` conditions remain in the status.

---

## 🛡️ Prevention Checklist
- [ ] Use `ForceHttpBasicAuth: "true"` in Vault templates for OCI.
- [ ] Always use wildcard `oci://<REGISTRY>/*` in AppProject whitelisting.
- [ ] Ensure Service Principal has `AcrPull` role.
