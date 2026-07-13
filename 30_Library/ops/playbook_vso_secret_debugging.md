---
created: 2026-02-21T15:07:26+00:00
modified: 2026-07-13T08:53:02+00:00
permalink: llmeon/30-library/ops/playbook-vso-secret-debugging
service: vso
severity: p2
tags: [playbook, secrets, troubleshooting, vso]
title: playbook_vso_secret_debugging
trigger: VSO-managed Secret is stale, misconfigured, or causing 401/403 errors
---

## Playbook: VSO Managed Secret Debugging

### Mental Model

VSO acts as a bridge. If the bridge is broken, we must determine if the failure is at the Vault source (auth/lease), the VSO logic (CR config), or the Kubernetes destination (drift/overwrite).

---

### Phase 1: Identify Origin

_Determine what owns this secret and where it lives in Vault._

1. Identify the managing controller and CR:
   ![[cmd_kubectl_get_secret_origin]]
2. Map the metadata to the Vault source:
   ![[kb_vso_metadata_identifiers]]

---

### Phase 2: Inspect Controller State

_Check if VSO is healthy and has a valid lease._

1. Inspect the Custom Resource spec and status:
   ![[cmd_kubectl_get_vso_cr_details]]
2. Decision:
   - If `status` shows error → Check Vault connectivity or RBAC.
   - If `status` is healthy but data is failing → Go to Phase 3.

---

### Phase 3: Inspect Secret Data

_Verify what is actually in the cluster._

1. Decode the secret data:
   ![[cmd_kubectl_decode_secret_data]]
2. Compare the decoded identity (e.g., Client ID) with what is expected in Vault.

---

### Phase 4: Remediation (The Force Sync)

_Recover from drift or stale credentials._

1. Enable overwrite to prevent future blocks:
   ![[cmd_kubectl_patch_vso_overwrite]]
2. Nuclear option: Delete the secret to force recreation:
   ![[cmd_kubectl_recreate_vso_secret]]

> [!DANGER] Caution
> Deleting a secret used by a running pod may cause service interruption until the secret is recreated and the pod is restarted.

---

### Phase 5: Verification

1. Confirm Reflector has synchronized mirrors:
   ![[cmd_kubectl_verify_reflector_sync]]
2. Re-test downstream service authentication.

---

### 🧠 End State

Success =

- Secret is recreated with fresh credentials.
- `spec.destination.overwrite` is set to `true`.
- Downstream services accept the credentials.
