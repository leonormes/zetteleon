---
created: 2026-02-17T15:31:52+00:00
modified: 2026-02-17T15:33:29+00:00
title: argocd-oci-helm-dependency-runbook
---

## ArgoCD OCI Helm Dependency Troubleshooting Runbook

### Overview

This runbook covers troubleshooting ArgoCD Applications that fail to resolve OCI Helm chart dependencies from a private registry (e.g. Azure Container Registry). The typical symptom is a `ComparisonError` during manifest generation when ArgoCD runs `helm dependency build` for a Git-sourced Application whose `Chart.yaml` declares OCI sub-dependencies.

---

### Error Signatures

| Stage | Error Message Pattern |
|---|---|
| Project restriction | `helm repos <registry> are not permitted in project '<project>'` |
| Cached project error | `Manifest generation error (cached): … are not permitted in project` |
| Authentication failure | `response status code 401: unauthorized: authentication required` |
| Missing dependencies | `found in Chart.yaml, but missing in charts/ directory: <chart>, <chart>` |

---

### Variables

Replace these placeholders throughout:

| Placeholder | Description | Example |
|---|---|---|
| `<REGISTRY>` | OCI registry hostname | `myregistry.azurecr.io` |
| `<REGISTRY_PATH>` | Registry + path | `myregistry.azurecr.io/helm` |
| `<APP_NAME>` | ArgoCD Application name | `thehyve` |
| `<PROJECT_NAME>` | ArgoCD AppProject name | `my-project` |
| `<NAMESPACE>` | ArgoCD namespace | `argocd` |
| `<GIT_REPO>` | Git repository URL | `https://gitlab.com/org/deployment.git` |
| `<CHART_PATH>` | Path to chart in repo | `charts/integrations/myapp` |
| `<BRANCH>` | Git branch / target revision | `main` |
| `<VSO_NAMESPACE>` | Vault Secrets Operator namespace | `vault-secrets-operator-system` |

---

### Phase 1: Diagnose the Error

#### 1.1 Describe the Application

```bash
kubectl describe application <APP_NAME> -n <NAMESPACE>
```

Key fields to check:

- `Status.Conditions[].Message`—the actual error
- `Status.Conditions[].Type`—should be `ComparisonError`
- `Spec.Project`—which AppProject governs this Application
- `Spec.Source.Path`—the chart path in Git

#### 1.2 Inspect the Chart Dependencies

```bash
cat <CHART_PATH>/Chart.yaml | grep -A 5 'dependencies'
```

Note whether dependencies use the `oci://` scheme or bare registry URLs.

#### 1.3 Check for Pre-Built Dependencies

```bash
ls -la <CHART_PATH>/charts/
```

If `.tgz` files are present, `helm dependency build` is skipped entirely. If the directory is empty or missing, ArgoCD must resolve dependencies at runtime.

---

### Phase 2: Fix AppProject sourceRepos

#### 2.1 Check Current sourceRepos

```bash
kubectl get appproject <PROJECT_NAME> -n <NAMESPACE> -o yaml | grep -A 20 'sourceRepos'
```

#### 2.2 Add Missing Registry Sources

ArgoCD does inconsistent URL matching between `oci://` and bare URLs. Add both variants:

```bash
# Add OCI-scheme variant
kubectl patch appproject <PROJECT_NAME> -n <NAMESPACE> --type='json' \
  -p='[{"op": "add", "path": "/spec/sourceRepos/-", "value": "oci://<REGISTRY_PATH>"}]'

# Add bare variant
kubectl patch appproject <PROJECT_NAME> -n <NAMESPACE> --type='json' \
  -p='[{"op": "add", "path": "/spec/sourceRepos/-", "value": "<REGISTRY_PATH>"}]'
```

Alternatively, use a wildcard to avoid this entirely:

```bash
kubectl patch appproject <PROJECT_NAME> -n <NAMESPACE> --type='json' \
  -p='[{"op": "add", "path": "/spec/sourceRepos/-", "value": "<REGISTRY>/*"}]'
```

#### 2.3 Clear Cached Errors

ArgoCD caches manifest generation results. After fixing sourceRepos, bust the cache:

```bash
# Option A: Restart the repo-server
kubectl rollout restart deployment argocd-repo-server -n <NAMESPACE>

# Option B: If ArgoCD CLI is available
argocd cache clear
```

Then force a hard refresh:

```bash
kubectl annotate application <APP_NAME> -n <NAMESPACE> argocd.argoproj.io/refresh=hard --overwrite
```

---

### Phase 3: Fix Registry Authentication (401 Errors)

#### 3.1 Inspect the Repository Secret

```bash
kubectl get secrets -n <NAMESPACE> -l argocd.argoproj.io/secret-type=repository -o yaml
```

Key fields in the secret:

- `url`—must match how ArgoCD resolves the registry
- `username` / `password`—the credentials
- `type`—should be `helm`
- `enableOCI`—should be `true`

#### 3.2 Decode and Test Credentials

```bash
PASS=$(kubectl get secret <SECRET_NAME> -n <NAMESPACE> -o jsonpath='{.data.password}' | base64 -d)
USER=$(kubectl get secret <SECRET_NAME> -n <NAMESPACE> -o jsonpath='{.data.username}' | base64 -d)

echo "$PASS" | helm registry login <REGISTRY> --username "$USER" --password-stdin
```

#### 3.3 Test Credentials from Inside the Repo-Server Pod

```bash
POD=$(kubectl get pod -n <NAMESPACE> -l app.kubernetes.io/name=argocd-repo-server -o jsonpath='{.items[0].metadata.name}')

kubectl exec -n <NAMESPACE> $POD -c repo-server -- \
  sh -c "echo '<PASSWORD>' | helm registry login <REGISTRY> --username '<USERNAME>' --password-stdin"
```

#### 3.4 Compare URL Field Against Working Cluster

```bash
# On BOTH clusters
kubectl get secret <SECRET_NAME> -n <NAMESPACE> -o jsonpath='{.data.url}' | base64 -d && echo
```

ArgoCD matches the repository secret's `url` field against the dependency URL. Mismatches cause silent auth failures.

---

### Phase 4: Fix Vault Dynamic Secret Issues

If credentials are managed by HashiCorp Vault Secrets Operator (VSO):

#### 4.1 Check VaultDynamicSecret Status

```bash
kubectl get vaultdynamicsecret <VDS_NAME> -n <NAMESPACE> -o yaml | grep -A 30 'status'
```

Look for:

- `secretLease.renewable`—should be `true`
- `lastRenewalTime`—should be recent
- Any error conditions

#### 4.2 Force Credential Regeneration

Delete the secret so VSO recreates it with a fresh Vault lease:

```bash
kubectl delete secret <SECRET_NAME> -n <NAMESPACE>
```

Watch it come back:

```bash
kubectl get secret -n <NAMESPACE> -w | grep <SECRET_NAME>
```

#### 4.3 Restart VSO if Needed

```bash
kubectl rollout restart deployment vault-secrets-operator-controller-manager -n <VSO_NAMESPACE>
```

> Warning: After VSO regenerates the secret, restart the repo-server immediately before VSO rotates again, or the repo-server may start with stale credentials.

---

### Phase 5: Fix OCI Sub-Dependency Credential Passthrough

This is the most common root cause for Git-sourced Applications with OCI Helm dependencies.

#### The Problem

ArgoCD uses `repository` secrets for direct Application sources (e.g. an Application pointing at an OCI chart). However, when a Git-sourced Application's chart has OCI sub-dependencies in `Chart.yaml`, ArgoCD may not pass the repository secret credentials through to `helm dependency build`.

#### 5.1 Verify the Problem

```bash
# Check repo-creds (credential templates)
kubectl get secrets -n <NAMESPACE> -l argocd.argoproj.io/secret-type=repo-creds -o yaml
```

If the result is an empty list, there are no credential templates—this is likely the issue.

#### 5.2 Create a Repo-creds Credential Template

Unlike `repository` secrets, `repo-creds` act as wildcard credential templates that ArgoCD applies to any matching URL, including during sub-dependency resolution.

```bash
PASS=$(kubectl get secret <REPOSITORY_SECRET_NAME> -n <NAMESPACE> -o jsonpath='{.data.password}' | base64 -d)
USER=$(kubectl get secret <REPOSITORY_SECRET_NAME> -n <NAMESPACE> -o jsonpath='{.data.username}' | base64 -d)

cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: argocd-oci-repo-creds
  namespace: <NAMESPACE>
  labels:
    argocd.argoproj.io/secret-type: repo-creds
type: Opaque
stringData:
  url: "<REGISTRY>"
  username: "${USER}"
  password: "${PASS}"
  type: "helm"
  enableOCI: "true"
  ForceHttpBasicAuth: "true"
EOF
```

#### 5.3 Restart and Verify

```bash
kubectl rollout restart deployment argocd-repo-server -n <NAMESPACE>
sleep 30
kubectl annotate application <APP_NAME> -n <NAMESPACE> argocd.argoproj.io/refresh=hard --overwrite
sleep 15
kubectl get application <APP_NAME> -n <NAMESPACE> -o jsonpath='{.status.conditions[0].message}' && echo
```

---

### Phase 6: Compare Clusters

When debugging against a known-working cluster, run these commands on both and diff:

#### 6.1 Repository Secrets

```bash
kubectl get secrets -n <NAMESPACE> -l argocd.argoproj.io/secret-type=repository -o yaml
```

#### 6.2 Repo Credential Templates

```bash
kubectl get secrets -n <NAMESPACE> -l argocd.argoproj.io/secret-type=repo-creds -o yaml
```

#### 6.3 Repo-Server Config

```bash
kubectl get deployment argocd-repo-server -n <NAMESPACE> -o yaml | grep -A 5 -i 'registry\|HELM_\|DOCKER'
kubectl get deployment argocd-repo-server -n <NAMESPACE> -o yaml | grep -A 10 'volumeMounts'
```

#### 6.4 ArgoCD ConfigMap

```bash
kubectl get configmap argocd-cm -n <NAMESPACE> -o yaml | grep -i 'helm\|oci'
```

#### 6.5 Repo-Server Logs

```bash
kubectl logs -n <NAMESPACE> -l app.kubernetes.io/name=argocd-repo-server --tail=50 | grep -i 'auth\|401\|login\|registry\|helm'
```

#### 6.6 Helm Registry Config Inside Pod

```bash
POD=$(kubectl get pod -n <NAMESPACE> -l app.kubernetes.io/name=argocd-repo-server -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n <NAMESPACE> $POD -c repo-server -- cat /helm-working-dir/registry/config.json 2>/dev/null
```

---

### Quick Reference: Full Recovery Sequence

When all else fails, this is the nuclear option—run in order:

```bash
# 1. Ensure sourceRepos has all URL variants
kubectl get appproject <PROJECT_NAME> -n <NAMESPACE> -o yaml | grep -A 20 'sourceRepos'

# 2. Force-regenerate Vault credentials
kubectl delete secret <REPOSITORY_SECRET_NAME> -n <NAMESPACE>
# Wait for VSO to recreate...
kubectl get secret -n <NAMESPACE> -w | grep <REPOSITORY_SECRET_NAME>

# 3. Create repo-creds template
PASS=$(kubectl get secret <REPOSITORY_SECRET_NAME> -n <NAMESPACE> -o jsonpath='{.data.password}' | base64 -d)
USER=$(kubectl get secret <REPOSITORY_SECRET_NAME> -n <NAMESPACE> -o jsonpath='{.data.username}' | base64 -d)

cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: argocd-oci-repo-creds
  namespace: <NAMESPACE>
  labels:
    argocd.argoproj.io/secret-type: repo-creds
type: Opaque
stringData:
  url: "<REGISTRY>"
  username: "${USER}"
  password: "${PASS}"
  type: "helm"
  enableOCI: "true"
  ForceHttpBasicAuth: "true"
EOF

# 4. Restart repo-server to pick up fresh creds
kubectl rollout restart deployment argocd-repo-server -n <NAMESPACE>
sleep 30

# 5. Hard refresh the application
kubectl annotate application <APP_NAME> -n <NAMESPACE> argocd.argoproj.io/refresh=hard --overwrite

# 6. Check result
kubectl get application <APP_NAME> -n <NAMESPACE> -o jsonpath='{.status.sync.status}' && echo
```

---

### Long-Term Fixes

| Approach | Pros | Cons |
|---|---|---|
| Commit chart tarballs to Git | Eliminates runtime dependency resolution entirely | Bloats repo, manual update burden |
| Use `repo-creds` templates | Works with dynamic secrets, covers all sub-deps | Extra secret to manage, credential rotation complexity |
| Wildcard `sourceRepos` | Avoids URL matching headaches | Slightly weaker security boundary |
| Declarative AppProject management | Prevents manual drift | Requires GitOps for ArgoCD config itself |

> Note on caching: ArgoCD aggressively caches manifest generation results and errors. Always restart `argocd-repo-server` and hard-refresh applications after making credential or project changes. The `(cached)` marker in error messages confirms a stale cache is being served.
