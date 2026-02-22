---
type: playbook
target_service: argocd
trigger: "ComparisonError during manifest generation for Helm charts with OCI sub-dependencies"
severity: p2
status: active
last_verified: 2026-02-22
tags: [playbook, argocd, helm, oci, dependencies, auth, troubleshooting]
---

# Playbook: ArgoCD OCI Helm Dependency Troubleshooting

## ⚠️ Symptoms

> **When to use this:** Troubleshooting ArgoCD Applications that fail to resolve OCI Helm chart dependencies from a private registry (e.g. Azure Container Registry). The typical symptom is a `ComparisonError` during manifest generation when ArgoCD runs `helm dependency build` for a Git-sourced Application whose `Chart.yaml` declares OCI sub-dependencies.

### Common Error Signatures
- **Project restriction:** `helm repos <registry> are not permitted in project '<project>'`
- **Cached project error:** `Manifest generation error (cached): … are not permitted in project`
- **Authentication failure:** `response status code 401: unauthorized: authentication required`
- **Missing dependencies:** `found in Chart.yaml, but missing in charts/ directory: <chart>, <chart>`

---

## Phase 0: Context Establishment

1. **Describe the Failing Application**
   *Identify the error details, the target chart path, and the ruling AppProject name.*
   ![[cmd_kubectl_argocd_describe_application#1. The Command]]

2. **Verify Chart Dependencies**
   *Check if `Chart.yaml` actually declares `oci://` endpoints.*
   ![[cmd_cat_helm_chart_dependencies#1. The Command]]

3. **Check for Pre-Built Dependencies**
   *If `.tgz` files are stored in git, auth isn't the problem.*
   ![[cmd_ls_helm_chart_prebuilt_dependencies#1. The Command]]

---

## Phase 1: Diagnosis

*Identify whether the blocker is structural (AppProject RBAC), network (egress/DNS), or pure authentication (stale Vault credential).*

1. **Check if OCI Registry is Permitted by AppProject**
   ![[cmd_kubectl_argocd_get_appproject_sourcerepos#1. The Command]]

2. **Test Credentials Locally First**
   *Isolate Kubernetes config by proving the credentials still work.*
   ![[cmd_helm_registry_login#1. The Command]]

3. **Test Credentials from inside the Repo-Server Pod**
   *Isolate network boundaries by proving Helm works from inside ArgoCD.*
   ![[cmd_kubectl_argocd_exec_helm_registry_login#1. The Command]]

4. **Investigate Repo-Server Config and Helm Config.json**
   *Verify injected credentials actually reach the helm subprocess environment inside the repo-server.*
   ![[cmd_kubectl_argocd_exec_cat_helm_registry_config#1. The Command]]
   ![[cmd_kubectl_argocd_logs_repo_server#1. The Command]]

---

## Phase 2: Remediation

*Correct the misconfiguration, forcibly purge stale credentials, and establish wildcard overrides for Helm sub-dependencies if necessary.*

1. **Patch AppProject if the Registry is Blocked**
   ![[cmd_kubectl_argocd_patch_appproject_sourcerepos#1. The Command]]

2. **Force Vault Secrets Operator to Rotate Stale Credentials**
   *(Skip if VSO is not managing your registry credentials).*
   ![[cmd_kubectl_recreate_vso_secret#1. The Command]]

3. **Create the `repo-creds` Credential Template**
   > [!IMPORTANT] Sub-dependency Issue Root Cause
   > ArgoCD uses `repository` secrets for direct Application sources (e.g., an App pointing at an OCI chart). However, for *Git-sourced* apps whose chart has OCI sub-dependencies natively, ArgoCD fails to pass the specific repository credentials through to `helm dependency build`. `repo-creds` templates fix this by applying to ANY matching URL prefix.
   ![[cmd_kubectl_argocd_create_repo_creds_template#1. The Command]]

4. **Restart Repo-Server to Flush In-Process Cache**
   *ArgoCD repo-server caches registry credentials. A fresh K8s Secret doesn't instantly reload the cache.*
   ![[cmd_kubectl_restart_argocd_repo_server#1. The Command]]

---

## Phase 3: Final Verification

*Force ArgoCD to re-evaluate the dependency build against the un-cached network.*

1. **Hard Refresh the Application**
   ![[cmd_argocd_refresh_app#1. The Command]]

2. **Watch the Reconcile Status**
   *Observe the `Status.Conditions` clear and transition to `Synced`.*
   ![[cmd_kubectl_argocd_describe_application#1. The Command]]

---

## Long-Term Fixes Overview

| Approach | Pros | Cons |
|---|---|---|
| Commit chart tarballs to Git | Eliminates runtime dependency resolution entirely | Bloats repo, manual update burden |
| Use `repo-creds` templates | Works with dynamic secrets, covers all sub-deps | Extra secret to manage, credential rotation complexity |
| Wildcard `sourceRepos` | Avoids URL matching headaches | Slightly weaker security boundary |
| Declarative AppProject management | Prevents manual drift | Requires GitOps for ArgoCD config itself |
