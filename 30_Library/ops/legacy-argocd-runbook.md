---
created: 2025-12-04T12:02:41Z
last_reviewed: null
modified: 2026-03-14T11:10:10+00:00
status: deprecated
tags: [state/thinking]
title: legacy-argocd-runbook
type: head
updated: null
---

> [!CAUTION] DEPRECATED
> This runbook has been modularized into atomic commands.
> Please use: [[pb-argocd-sync-failure-triage]]

## ArgoCD Debugging Runbook (kubectl-only)

### Overview

This runbook covers debugging ArgoCD applications using only `kubectl` commands (no ArgoCD CLI required). Use this when applications show `Unknown` sync status or fail to sync from Git repositories.

---

### 1. Check Application Status

#### View All Applications

```sh
kubectl get applications -n argocd
```

Expected Output:

```sh
NAME             SYNC STATUS   HEALTH STATUS
app-name         Synced        Healthy
```

Status Values:

- `Synced`: Git matches cluster state
- `OutOfSync`: Git differs from cluster (needs sync)
- `Unknown`: ArgoCD cannot determine sync state (authentication or config issue)

---

#### Describe Specific Application

```sh
kubectl describe application <app-name> -n argocd
```

Look For:

- `Status.Sync.Status`: Current sync state
- `Status.Health`: Application health
- `Events`: Recent sync operations and errors
- `Operation State.Message`: Detailed error messages

---

#### Watch Application Status Live

```sh
kubectl get applications -n argocd -w
```

Use When: Monitoring active sync operations

---

### 2. Diagnose ArgoCD Server Issues

#### Check ArgoCD Server Pod Status

```sh
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-server
```

Expected: `STATUS: Running`, `READY: 1/1`

---

#### View ArgoCD Server Logs

```sh
kubectl logs -n argocd deployment/argocd-server --tail=100
```

Look For:

- Authentication errors
- Configuration parsing errors
- Resource limit issues (OOMKilled)

---

#### Check ArgoCD Server Events

```sh
kubectl get events -n argocd --sort-by='.lastTimestamp' | grep argocd-server
```

Look For:

- Crashloop patterns
- Readiness probe failures
- Secret rotation triggers

---

### 3. Diagnose Application Controller Issues

#### Check Application Controller Status

```sh
kubectl get statefulset -n argocd
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-application-controller
```

Note: In ArgoCD v2.5+, the application controller is a StatefulSet, not a Deployment.

---

#### View Application Controller Logs

```sh
kubectl logs -n argocd statefulset/argocd-application-controller --tail=100
```

Look For:

- `authentication required`: Git credentials missing/invalid
- `Failed to load target state`: Cannot fetch from Git
- `Skipping auto-sync: application status is Unknown`: Sync state unknown

---

#### Filter Logs for Specific Application

```sh
kubectl logs -n argocd statefulset/argocd-application-controller --tail=200 | grep -E "application-name|authentication|Access denied"
```

---

#### Watch Controller Logs Live

```sh
kubectl logs -n argocd statefulset/argocd-application-controller --tail=50 -f
```

---

### 4. Investigate Git Repository Credentials

#### List All Repository Secrets

```sh
kubectl get secrets -n argocd -l argocd.argoproj.io/secret-type=repository
```

---

#### Inspect Repository Secret Contents

```sh
kubectl get secret <secret-name> -n argocd -o yaml
```

Required Fields:

- `data.url`: Repository URL (base64-encoded)
- `data.username`: Git username or token username
- `data.password`: Git password or token
- `data.type`: Should be `git`

---

#### Decode Secret Fields

```sh
# Decode URL
kubectl get secret <secret-name> -n argocd -o jsonpath='{.data.url}' | base64 -d

# Decode username
kubectl get secret <secret-name> -n argocd -o jsonpath='{.data.username}' | base64 -d

# Check password length (don't print actual password)
kubectl get secret <secret-name> -n argocd -o jsonpath='{.data.password}' | base64 -d | wc -c
```

Expected: Password length > 0 (e.g., 28 characters for a token)

---

#### View All Secret Fields (Sanitised)

```sh
kubectl get secret <secret-name> -n argocd -o jsonpath='{.data}' | jq
```

---

### 5. Fix Vault-Managed Repository Secrets

#### Check VaultStaticSecret Configuration

```sh
kubectl get vaultstaticsecret <secret-name> -n argocd -o yaml
```

Verify:

- `spec.mount`: Correct Vault mount path
- `spec.path`: Correct Vault secret path
- `spec.destination.name`: Matches ArgoCD repository secret name
- `spec.destination.transformation.templates`: Maps Vault fields to ArgoCD secret fields

---

#### View VaultStaticSecret Spec Only

```sh
kubectl get vaultstaticsecret <secret-name> -n argocd -o jsonpath='{.spec}' | jq
```

---

#### Force Vault Secret Rotation

```sh
kubectl annotate vaultstaticsecret <secret-name> -n argocd secrets.hashicorp.com/vault-force-rotation="$(date +%s)" --overwrite
```

Why: Forces immediate re-fetch from Vault, bypassing normal refresh interval

---

#### Watch for Secret Rotation Events

```sh
kubectl get events -n argocd --sort-by='.lastTimestamp' -w | grep SecretRotated
```

Expected: New `SecretRotated` event within 30-60 seconds

---

#### Restart Vault Secrets Operator (If Rotation Fails)

```sh
kubectl get pods -n vault-secrets-operator-system
kubectl delete pod -n vault-secrets-operator-system -l app.kubernetes.io/name=vault-secrets-operator
```

---

### 6. Force Application Sync

#### Trigger Manual Sync (Latest Revision)

```sh
kubectl patch application <app-name> -n argocd --type merge -p '{"operation": {"initiatedBy": {"username": "manual"}, "sync": {"revision": "HEAD"}}}'
```

---

#### Trigger Manual Sync (Specific Branch)

```sh
kubectl patch application <app-name> -n argocd --type merge -p '{"operation": {"initiatedBy": {"username": "manual"}, "sync": {"revision": "branch-name"}}}'
```

---

#### Force Sync All Applications

```sh
for app in $(kubectl get applications -n argocd -o jsonpath='{.items[*].metadata.name}'); do
  kubectl patch application $app -n argocd --type merge -p '{"operation": {"initiatedBy": {"username": "manual"}, "sync": {"revision": "HEAD"}}}'
done
```

---

#### Force Sync Multiple Specific Applications

```sh
for app in app1 app2 app3; do
  kubectl patch application $app -n argocd --type merge -p '{"operation": {"initiatedBy": {"username": "manual"}, "sync": {"revision": "HEAD"}}}'
done
```

---

### 7. Monitor Deployment Progress

#### Watch Pods in Target Namespace

```sh
kubectl get pods -n <target-namespace> -w
```

---

#### Watch Specific Deployment Rollout

```sh
kubectl rollout status deployment/<deployment-name> -n <target-namespace>
```

---

#### Stream Pod Logs

```sh
kubectl logs -f deployment/<deployment-name> -n <target-namespace>
```

---

#### Check Recent Events in Namespace

```sh
kubectl get events -n <target-namespace> --sort-by='.lastTimestamp'
```

Look For:

- Pod scheduling failures
- Image pull errors
- CrashLoopBackOff reasons

---

### 8. Restart ArgoCD Components

#### Restart ArgoCD Server

```sh
kubectl rollout restart deployment/argocd-server -n argocd
kubectl rollout status deployment/argocd-server -n argocd
```

---

#### Restart Application Controller

```sh
kubectl rollout restart statefulset/argocd-application-controller -n argocd
kubectl rollout status statefulset/argocd-application-controller -n argocd
```

---

### 9. Troubleshooting Cheat Sheet

#### Problem: Applications Show "Unknown" Sync Status

Diagnostic Commands:

```sh
# Check ArgoCD server health
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-server

# Check application controller logs
kubectl logs -n argocd statefulset/argocd-application-controller --tail=100 | grep -E "Unknown|authentication"

# Verify repository secret
kubectl get secret <repo-secret> -n argocd -o jsonpath='{.data.password}' | base64 -d | wc -c
```

Solution:

1. Fix empty credentials in repository secret
2. Force Vault secret rotation (if using Vault)
3. Restart application controller

---

#### Problem: "Authentication Required" or "Access Denied" Errors

Diagnostic Commands:

```sh
# Check application controller logs
kubectl logs -n argocd statefulset/argocd-application-controller --tail=200 | grep -i "authentication\|access denied"

# Verify Git credentials exist
kubectl get secret <repo-secret> -n argocd -o jsonpath='{.data}' | jq
```

Solution:

1. Populate Vault secret with correct Git token
2. Force VaultStaticSecret rotation
3. Verify credentials populated: `kubectl get secret <repo-secret> -n argocd -o jsonpath='{.data.password}' | base64 -d | wc -c`

---

#### Problem: VaultStaticSecret Not Populating Credentials

Diagnostic Commands:

```sh
# Check VaultStaticSecret configuration
kubectl get vaultstaticsecret <secret-name> -n argocd -o jsonpath='{.spec}' | jq

# Check Vault operator logs
kubectl logs -n vault-secrets-operator-system -l app.kubernetes.io/name=vault-secrets-operator --tail=100
```

Solution:

1. Verify `spec.mount` and `spec.path` point to correct Vault location
2. Ensure `spec.destination.transformation.templates` maps Vault fields correctly
3. Force rotation with annotation
4. Restart Vault operator if needed

---

### 10. Common VaultStaticSecret Transformation Template

Example for GitLab Token:

```yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultStaticSecret
metadata:
  name: argocd-repo-<repo-name>
  namespace: argocd
spec:
  mount: admin/central          # Your Vault mount
  path: gitlab                  # Your Vault path
  type: kv-v2
  refreshAfter: 3600s
  destination:
    name: argocd-repo-<repo-name>
    create: true
    labels:
      argocd.argoproj.io/secret-type: repository
    transformation:
      templates:
        username:
          text: "gitlab-ci-token"
        password:
          text: "{{ .Secrets.token }}"    # Maps Vault 'token' field
        type:
          text: "git"
        url:
          text: "https://gitlab.com/<org>/<repo>.git"
```

---

### 11. Quick Reference: Common Commands

```sh
# Check all applications
kubectl get applications -n argocd

# Describe application
kubectl describe application <app-name> -n argocd

# Check controller logs
kubectl logs -n argocd statefulset/argocd-application-controller --tail=100

# Force sync
kubectl patch application <app-name> -n argocd --type merge -p '{"operation": {"initiatedBy": {"username": "manual"}, "sync": {"revision": "HEAD"}}}'

# Check repository secret credentials
kubectl get secret <repo-secret> -n argocd -o jsonpath='{.data.password}' | base64 -d | wc -c

# Force Vault rotation
kubectl annotate vaultstaticsecret <secret-name> -n argocd secrets.hashicorp.com/vault-force-rotation="$(date +%s)" --overwrite

# Watch application status
kubectl get applications -n argocd -w

# Watch events
kubectl get events -n argocd --sort-by='.lastTimestamp' -w
```

---

### Appendix: Understanding Sync Status Values

|Status|Meaning|Action Required|
|---|---|---|
|`Synced`|Git matches cluster|None|
|`OutOfSync`|Git differs from cluster|Wait for auto-sync or force sync|
|`Unknown`|Cannot determine state|Debug authentication or config|
|`Progressing`|Sync in progress|Monitor progress|
|`Degraded`|Some resources unhealthy|Check pod/service health|

---

### Appendix: Understanding Health Status Values

| Status        | Meaning                         |
| ------------- | ------------------------------- |
| `Healthy`     | All resources running correctly |
| `Progressing` | Deployment/rollout in progress  |
| `Degraded`    | Some resources failing          |
| `Suspended`   | Application paused              |
| `Missing`     | Expected resources not found    |
