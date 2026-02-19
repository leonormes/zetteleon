---
created: 2025-12-04T12:02:41Z
last_reviewed: null
modified: 2026-02-11T17:05:47+00:00
status: processing
tags: [state/thinking]
title: Playbook - Troubleshooting ArgoCD & Vault Secret Synchronisation
type: head
---

## 1. Symptom: Application Sync Status is `Unknown`

Error Message: `failed to generate manifest… authentication required: HTTP Basic: Access denied`

### Cause

ArgoCD cannot pull the repository from GitLab. This typically occurs because the GitLab Deploy Token stored in Vault has expired or is invalid, or the Vault Secrets Operator has not successfully created the Kubernetes secret.

### Resolution Steps

1. Verify the Token: Manually test the credentials from the Kubernetes secret:

```sh
PASS=$(kubectl get secret argocd-repo-fitfile-deployment-repo -n argocd -o jsonpath='{.data.password}' | base64 -d)
git ls-remote https://argocd-test:${PASS}@gitlab.com/fitfile/deployment.git
unset PASS
```

1. Update Vault: If the test fails, generate a new Deploy Token in GitLab (Settings > Repository) and update the `gitlab_deploy_token_password` in HCP Vault.
2. Force Re-sync: Delete the existing Kubernetes secret to force VSO to pull the new data:

```sh
kubectl delete secret argocd-repo-fitfile-deployment-repo -n argocd
```

1. Clear ArgoCD Cache: Restart the repo-server to clear cached authentication failures:

```sh
kubectl rollout restart deployment argocd-repo-server -n argocd
```

1. Hard Refresh: Trigger a hard refresh on the ArgoCD application:

```sh
kubectl patch application <app-name> -n argocd --type merge -p '{"metadata":{"annotations":{"argocd.argoproj.io/refresh":"hard"}}}'
```

---

## 2. Symptom: Vault Operator Connection Failure

Error Message:

`VaultConnection.secrets.hashicorp.com "default" not found` or `cachingClientFactory` errors in VSO logs.

### Cause

The `VaultAuth` resource cannot find its associated `VaultConnection`, often due to a race condition during the initial Terraform apply where CRDs were not yet established.

### Resolution Steps

1. Explicit Reference: Ensure the `VaultAuth` manifest explicitly references the connection:

```yaml
spec:
  vaultConnectionRef: default
```

1. Operator Restart: If the connection exists but the error persists, restart the VSO controller to clear its internal cache:

```sh
kubectl rollout restart deployment vault-secrets-operator-controller-manager -n vault-secrets-operator-system
```

1. Double Apply: If running Terraform, a second `apply` is often required to allow the Kubernetes API to discover the new CRDs.

---

## 3. Symptom: `ImagePullBackOff` for ACR Images

Error Message:

`Failed to retrieve image pull secret (fitfile-image-pull-secret)`

### Cause

The `VaultDynamicSecret` responsible for generating Azure Container Registry (ACR) credentials has provided an expired token, or the secret was generated before the Vault connection was established.

### Resolution Steps

1. Refresh Dynamic Secret: Delete the `VaultDynamicSecret` in the `argocd` namespace to force a new ACR token generation:

```sh
kubectl delete vaultdynamicsecret fitfile-image-pull -n argocd
```

1. Verify Reflector: Ensure the `emberstack` reflector is synchronising the new secret to the application namespace:

```sh
kubectl get secret fitfile-image-pull-secret -n <app-namespace>
```

---

## Quick Health Check Commands

| Component      | Command                                                                                      |
| ------------------ | ------------------------------------------------------------------------------------------------ |
| Vault Auth     | `kubectl get vaultauth -A`                                                                       |
| Static Secrets | `kubectl get vaultstaticsecret -A`                                                               |
| ArgoCD Apps    | `kubectl get applications -n argocd`                                                             |
| VSO Logs       | `kubectl logs -n vault-secrets-operator-system -l app.kubernetes.io/name=vault-secrets-operator` |
| Repo Logs      | `kubectl logs -n argocd -l app.kubernetes.io/component=repo-server`                              |
