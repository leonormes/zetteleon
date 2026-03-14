---
created: 2026-03-14T10:29:53+00:00
modified: 2026-03-14T11:10:50+00:00
title: secret-management
---

## Secret Management: Current State & Improvement Plan

### 1. Current Architecture Overview

The stack uses Vault Secrets Operator (VSO) with HCP Vault to sync secrets from Vault KV into Kubernetes Secrets, deployed via ArgoCD app-of-apps.

```
HCP Vault (HCP Cloud)
  └── Namespace: admin/deployments/{deploymentKey}
        └── KV v2 Mount: secrets/
              ├── {applicationVaultPath}   (e.g. ff-a-application, dev)
              ├── cloudflare
              ├── monitoring
              ├── spicedb
              ├── argo-workflows
              └── mesh

ArgoCD (app-of-apps)
  └── ffnode umbrella chart → 26 ArgoCD Applications (sync waves -5 → +5)
        └── Each Application embeds VaultStaticSecret CRDs via extraDeploy

VSO (in-cluster)
  └── Watches VaultStaticSecret CRDs
        └── Syncs → Kubernetes Secrets (auto-created, drift-detected)

Pods
  └── Mount K8s Secrets as volumes (/secrets/) or env vars
```

---

### 2. Authentication

Method: AppRole

CRD: `VaultAuth` (name: `default`, or `mesh` for mesh integration)

Auth path: `auth/approle`

Vault namespace: `admin/deployments/{deploymentKey}`

Node-specific `deploymentKey` controls which Vault namespace is used (e.g. `prod-1`, `dev`).

---

### 3. How a Secret Gets from Vault to a Pod

#### Step 1—Define in `values.yaml`

Each component has a `vaultSecrets` array in `values.yaml`:

```yaml
fitconnect:
  vaultSecrets:
    - secretName: "fitconnect"
      vaultPath: '{{ include "applicationVaultPath" . }}'   # templated
      refreshAfter: 5m
      rolloutRestartTargets:
        - kind: Deployment
          name: '{{ printf "%s-fitconnect-ftc" .Release.Name }}'
      secretTransformation:
        excludes: [.*]          # drop all raw Vault fields
        templates:
          mongodb:
            text: 'mongodb://{{get .Secrets "mongodb_username"}}:{{get .Secrets "mongodb_password"}}@...'
          postgresql.json:
            text: '{"password":"{{get .Secrets "postgresql_password"}}"}'
```

#### Step 2—Helm Renders `VaultStaticSecret` CRDs

`renderValuesWithVaultSecretInExtraDeploy` in `_helpers.tpl` processes the `vaultSecrets` array and appends `VaultStaticSecret` CRD objects to the `extraDeploy` list. These are rendered inline into the ArgoCD Application's `values:` block.

#### Step 3—ArgoCD Syncs the Application

The child Application's Helm chart sees the CRDs in `extraDeploy` and creates them in the target namespace. ArgoCD respects sync waves so secrets are available before pods start.

#### Step 4—VSO Syncs the Secret

VSO watches `VaultStaticSecret` CRDs, fetches the Vault path, applies `secretTransformation` templates, and creates/updates a `kubernetes.io/v1 Secret` in the same namespace. `hmacSecretData: true` enables drift detection.

#### Step 5—Pod Consumes the Secret

```yaml
volumes:
  - name: fitconnect-secrets
    secret:
      secretName: fitconnect   # matches VaultStaticSecret.spec.destination.name
volumeMounts:
  - name: fitconnect-secrets
    mountPath: /secrets
    readOnly: true
```

Pod reads `/secrets/postgresql.json`, `/secrets/mongodb`, etc.

---

### 4. Secret Inventory by Component

| K8s Secret Name | Vault Path | Component(s) | Injection Method |
|---|---|---|---|
| `mongodb` | `{appVaultPath}` | mongodb StatefulSet | env var (existingSecret) |
| `postgresql` | `{appVaultPath}` | postgresql StatefulSet | env var (existingSecret) |
| `fitconnect` | `{appVaultPath}` | fitconnect Deployment | volume `/secrets/` |
| `ffcloud` | `{appVaultPath}` | ffcloud-service Deployment | volume `/secrets/` |
| `workflows-secrets` | `{appVaultPath}` | workflow-templates (Argo steps) | volume `/secrets/` |
| `argo-postgres-config` | `argo-workflows` | Argo Workflows | env var (secretKeyRef) |
| `argo-server-sso` | `argo-workflows` | Argo Workflows server | env var |
| `spicedb` | `{appVaultPath}` | SpiceDB | env var (existingSecret) |
| `monitoring` | `monitoring` | grafana-k8s-monitoring | Helm values |
| `cloudflare-issuer-api-token` | `cloudflare` | cert-manager ClusterIssuer | volume |
| `mesh-secrets` | `mesh` | fitconnect optout | volume `/secrets/` |
| `fitfile-rsa-private-key` | `{appVaultPath}` | fitconnect | volume |
| `mutating-proxy-webhook-tls` | `{appVaultPath}` | mutating-proxy-webhook | volume |
| `pg-web` | `{appVaultPath}` | external DB client | env var |

---

### 5. Presets (Shorthand Patterns)

`_helpers.tpl` supports `preset:` to avoid repeating standard transformation templates:

| Preset | Generates keys |
|---|---|
| `mongodb` | `mongodb-replica-set-key`, `mongodb-root-password` |
| `postgresql` | `postgres-password` |
| `auth0` | `client-id`, `client-secret` |

Usage:

```yaml
vaultSecrets:
  - secretName: "mongodb"
    vaultPath: '{{ include "applicationVaultPath" . }}'
    preset: mongodb
```

---

### 6. Node-Specific Overrides

Nodes add extra secrets via `extraVaultSecrets` in their `values.yaml`:

```yaml
# ffnodes/fitfile/ff-a/values.yaml
extraVaultSecrets:
  - secretName: "sleuth-secret"
    vaultPath: "ff-a-application"
    secretTransformation:
      excludes: [.*]
      templates:
        apiKey:
          text: '{{get .Secrets "sleuth_api_key"}}'
```

The `renderValuesWithVaultSecretInExtraDeploy` helper merges `vaultSecrets` + `extraVaultSecrets` before generating CRDs.

---

### 7. Known Issues & Anti-Patterns

#### 7a. KCH Hardcoded Secrets (Critical)

`ffnodes/kch/prod/templates/vault-replacement-secrets.yaml` contains base64-encoded credentials committed to git:

```yaml
# TODO: Remove once KCH can connect to Vault!
data:
  mongodb.json: eyJwYXNzd29yZCI6...   # base64 plaintext credentials
```

Risk: Credentials in git history. Any repo access = credential access.

#### 7b. No Local Dev Workflow

There is no documented way for a developer to:

- Run the stack locally without Vault connectivity
- Test secret transformation templates before pushing
- Verify that a new Vault key name is correctly mapped

#### 7c. Multi-Step Secret Addition Process

Adding a new secret requires coordinating changes across:

1. Vault (write the key manually)
2. `values.yaml` (add `secretTransformation` template entry)
3. Component chart (add volume mount or env var reference)
4. Node `values.yaml` if node-specific

There is no single source of truth or automated validation that all four are in sync.

#### 7d. Template Escaping Complexity

The double-escaping required for VSO templates within Helm templates is hard to read and error-prone:

```yaml
# This is what you have to write to produce: {{get .Secrets "key"}}
text: '{{"{{`{{get .Secrets \"key\"}}`}}"}}'
# vs the simpler form that works in most templates:
text: '{{get .Secrets "key"}}'
```

The `secretTransformationDisableTpl` flag exists to bypass Helm templating but is not consistently documented.

#### 7e. Inconsistent Refresh Intervals

Some secrets have `refreshAfter: 5m`, others have `null`. There is no documented policy.

---

### 8. Improvement Plan

#### Phase 1—Immediate (Security & Hygiene)

P1.1—Rotate and remove KCH hardcoded secrets

- Assume credentials in `vault-replacement-secrets.yaml` are compromised
- Rotate all credentials referenced in that file
- Migrate KCH to VSO: deploy a `VaultAuth` AppRole into KCH cluster or use Vault agent injector as an intermediate step if network access to HCP is not possible from KCH
- Delete `vault-replacement-secrets.yaml` and purge from git history with `git filter-branch` or `bfg`

P1.2—Enforce `refreshAfter` policy

- Define a standard: `5m` for app secrets, `1h` for rarely-rotating infra secrets (TLS, monitoring)
- Add the field to every `VaultStaticSecret` entry

---

#### Phase 2—Developer Experience

P2.1—Secret Registry (single source of truth)

Create `docs/secret-registry.yaml` that lists every Vault key, its K8s secret destination, and which components consume it:

```yaml
# docs/secret-registry.yaml
secrets:
  - vaultKey: mongodb_password
    vaultPath: "{applicationVaultPath}"
    description: MongoDB root password
    consumedBy:
      - k8sSecret: mongodb
        k8sKey: mongodb-root-password
        component: mongodb
        injectionMethod: existingSecret
      - k8sSecret: fitconnect
        k8sKey: mongodb          # embedded in connection string
        component: fitconnect
        injectionMethod: volumeMount
```

This is documentation only—it does not replace `values.yaml`. Use it as a checklist when adding secrets.

P2.2—Debugging scripts

Add `scripts/secret-debug.sh`:

```bash
#!/usr/bin/env bash
# Usage: ./scripts/secret-debug.sh <namespace> [secret-name]
# Shows all VaultStaticSecrets and their sync status in a namespace

NS=${1:?Usage: secret-debug.sh <namespace> [secret-name]}
SECRET=${2:-}

echo "=== VaultStaticSecrets in $NS ==="
kubectl get vaultstaticsecret -n "$NS" -o custom-columns=\
'NAME:.metadata.name,READY:.status.conditions[0].status,REASON:.status.conditions[0].reason,LAST-SYNC:.status.lastGeneration'

if [[ -n "$SECRET" ]]; then
  echo ""
  echo "=== VaultStaticSecret detail: $SECRET ==="
  kubectl get vaultstaticsecret "$SECRET" -n "$NS" -o yaml

  echo ""
  echo "=== Resulting K8s Secret keys: $SECRET ==="
  kubectl get secret "$SECRET" -n "$NS" -o jsonpath='{.data}' | jq 'keys'
fi
```

Add `scripts/vault-sync-status.sh`:

```bash
#!/usr/bin/env bash
# Shows all VaultStaticSecrets that are NOT in a Ready state
kubectl get vaultstaticsecret -A -o json | \
  jq -r '.items[] | select(.status.conditions[]?.status != "True") |
    "\(.metadata.namespace)/\(.metadata.name): \(.status.conditions[]?.reason // "Unknown")"'
```

P2.3—Local development values override

Create `ffnodes/local/values.yaml` with VSO disabled and static K8s secrets for development:

```yaml
# ffnodes/local/values.yaml
# Use this file to override values for local development (kind/k3d)
# Run: helm template ffnode charts/ffnode -f ffnodes/local/values.yaml | kubectl apply -f -

deploymentKey: local
namespace: local

global:
  vault:
    enabled: false   # Disables VSO CRD generation in renderValuesWithVaultSecretInExtraDeploy

# For each component, provide the existingSecret name and create the K8s secret manually
# or via a local-secrets.yaml (gitignored)
```

Pair this with a `Makefile` target:

```makefile
local-secrets:
	@echo "Creating local development secrets..."
	kubectl create secret generic mongodb \
	  --from-literal=mongodb-root-password=localpassword \
	  --from-literal=mongodb-replica-set-key=localkey \
	  --dry-run=client -o yaml | kubectl apply -f -
	# ... repeat for other secrets
```

P2.4—Preset expansion

Extend the `preset` system in `_helpers.tpl` to cover the most common full-component patterns, reducing repeated transformation boilerplate:

```yaml
# Instead of 8-line transformation block:
vaultSecrets:
  - secretName: "fitconnect"
    vaultPath: '{{ include "applicationVaultPath" . }}'
    preset: fitconnect-full   # generates mongodb, postgresql.json, spicedb.json, auth.json, s3-*
```

Add presets: `fitconnect-full`, `ffcloud-full`, `workflows-full`.

---

#### Phase 3—GitOps Hardening

P3.1—VaultAuth CRD as code

The `VaultAuth` CRDs (AppRole config) should be in git, not created manually. Create a chart or Helm template that generates them:

```yaml
# charts/ffnode/templates/vault-auth.yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultAuth
metadata:
  name: default
  namespace: {{ include "namespace" . }}
spec:
  method: appRole
  mount: auth/approle
  namespace: {{ printf "admin/deployments/%s" .Values.deploymentKey }}
  appRole:
    roleId: {{ .Values.global.vault.appRole.roleId }}  # non-sensitive, safe to store in git
    secretRef: vault-approle-secret-id                  # K8s secret with the actual secret-id
```

The `vault-approle-secret-id` K8s Secret is the only thing bootstrapped out-of-band (via cluster init or external-secrets bootstrap).

P3.2—CUE validation in CI

Expand `cue/schema/vault.cue` usage: add a CI step that validates all `vaultSecrets` blocks in `values.yaml` against the CUE schema before merge. This catches missing required fields, wrong key types, and invalid presets early.

```yaml
# .gitlab-ci.yml addition
validate-vault-schema:
  stage: validate
  script:
    - cue vet ./cue/... ./charts/ffnode/values.yaml
```

P3.3—ArgoCD ignore differences for VSO status fields

Add `ignoreDifferences` to all Applications for VSO status fields to prevent ArgoCD from showing false OutOfSync:

```yaml
ignoreDifferences:
  - group: secrets.hashicorp.com
    kind: VaultStaticSecret
    jsonPointers:
      - /status
      - /metadata/resourceVersion
```

P3.4—Secret rotation runbook

Document the rotation procedure in `docs/secret-rotation.md`:

1. Update secret value in HCP Vault
2. VSO picks up change within `refreshAfter` window (default 5m)
3. K8s Secret is updated automatically
4. Pods in `rolloutRestartTargets` are restarted automatically
5. Verify: `kubectl rollout status deployment/{name} -n {namespace}`
6. If manual rotation needed: `kubectl annotate vaultstaticsecret {name} force-sync=$(date +%s) -n {namespace}`

---

#### Phase 4—Observability

P4.1—VSO metrics in Grafana

VSO exposes Prometheus metrics. Add a Grafana dashboard panel:

- `vault_secrets_operator_vaultstaticsecret_status`—sync success/failure per secret
- `vault_secrets_operator_vaultstaticsecret_last_sync_timestamp`—staleness detection

Alert if any VaultStaticSecret has not synced within `2 * refreshAfter`.

P4.2—Audit log forwarding

Enable HCP Vault audit logging and forward to the observability stack (Loki) so secret access is traceable per deployment.

---

### 9. Decision Record: Why VSO over Vault Agent Injector

The legacy Vault Agent Injector pattern (still visible in some component annotations) is being phased out in favor of VSO because:

- VSO creates first-class K8s Secrets—standard tooling (kubectl, ArgoCD) can inspect them
- No sidecar container overhead per pod
- Drift detection via `hmacSecretData`
- Automatic pod restart via `rolloutRestartTargets`
- Declarative GitOps-friendly CRDs

Do not add new vault agent annotations. All new secrets should use VSO `VaultStaticSecret`.

---

### 10. Checklist: Adding a New Secret

```
[ ] 1. Write the key/value to HCP Vault at the correct path
        vault kv put secrets/{path} {key}={value}

[ ] 2. Add the key to secretTransformation.templates in values.yaml
        templates:
          {k8s-key-name}:
            text: '{{get .Secrets "{vault_key_name}"}}'

[ ] 3. Add the K8s secret key reference to the component chart values
        (volumeMount, secretKeyRef, or existingSecret)

[ ] 4. Add the secret to docs/secret-registry.yaml

[ ] 5. Test locally with global.vault.enabled=false + manual K8s secret

[ ] 6. Verify in staging: kubectl get vaultstaticsecret {name} -n {ns} -o yaml
        Check .status.conditions[0].status == "True"

[ ] 7. Verify pod has the secret:
        kubectl exec -it {pod} -- cat /secrets/{key-name}
```
