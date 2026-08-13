---
created: 2026-02-22T17:07:12+00:00
last_verified: 2026-02-22
modified: 2026-08-13T10:53:56+00:00
permalink: llmeon/30-library/ops/playbook-ff-deployment-auth0-tenant-mismatch
severity: p1
tags: [auth0, crashloopbackoff, deployment, init, playbook, vault]
target_service: fitconnect
title: playbook_ff_deployment_auth0_tenant_mismatch
trigger: ffcloud / fitconnect CrashLoopBackOff during new environment deployment with
  Auth0 M2M
---

## Playbook: FFNode Auth0 Tenant Parity Failure

### ⚠️ Symptoms

> When to use this: New deployments of HIE / FFNode (or any application demanding Auth0 M2M initialization) are completely failing. The deployment is stuck in `Init:CrashLoopBackOff` or reporting downstream errors like `Tenant with id does not exist`.

- `ffcloud-service` stuck in `Init:CrashLoopBackOff`
- `fitconnect-ftc` in `CrashLoopBackOff`
- Auth0 token errors (401 → later 403)
- Secrets appear present but services still fail to start

---

### 🧠 Mental Model / Architecture Dependency

Startup order is strictly serial. If the init-container fails, nothing else boots:

`Vault → Kubernetes Secret → ffcloud init → Tenant seeded in Mongo → fitconnect starts`

If `ffcloud` cannot authenticate with Auth0:

- Init fails ❌
- Tenant never created ❌
- `fitconnect` cannot find tenant ❌
- Whole deployment appears broken ❌

This is not a Kubernetes failure—it is an identity configuration mismatch. Do not debug ingress, networking, or TLS until the init-container payload is verified.

---

### Phase 0: Context Establishment

1. Check Pod State for Init Crashes
   _Identify precisely which container in the pod is currently looping._
   ![[cmd_kubectl_get_pods#1. The Command]]

---

### Phase 1: Diagnosis

_Prove the specific failure mode (401/403 Authorisation) and trace the credential injection from Vault._

1. Inspect Ffcloud Init Logs (Most Important Signal)
   _Look for `POST https://fitfile-prod.eu.auth0.com/oauth/token status: 403 Forbidden`._
   _This indicates an Auth0 mismatch—NOT a Kubernetes networking issue._
   ![[cmd_kubectl_get_init_container_logs#1. The Command]]

2. Confirm Secrets Rendered by Vault
   _Does the Kubernetes secret structurally exist? Are the values populated?_
   ![[cmd_kubectl_decode_secret_json_key#1. The Command]]

3. Validate VaultStaticSecret Mapping
   _Check template references. Which exact Vault path is VSO querying? (`admin/deployments/<deployment>/application`)_
   ![[cmd_kubectl_get_vaultstaticsecret#1. The Command]]

4. Verify Auth0 Endpoint Matches Credential Tenant
   _Bypass Kubernetes. Test the token request manually using the extracted Client ID/Secret. If a token generates for `fitfile-test.eu.auth0.com` but the init logs show a call to `fitfile-prod.eu.auth0.com`, you've proven the tenant mismatch._
   ![[cmd_curl_auth0_token_test#1. The Command]]

5. Check Rendered Application Config (What the Pods Actually Use)
   _Investigate the `fitconnect` ConfigMap to see the Helm-rendered `baseURL`._
   ![[cmd_kubectl_get_configmap_values#1. The Command]]

---

### Phase 2: Remediation

_Synchronize the identity state. The Helm values must match the Auth0 tenant that owns the Vault credentials._

1. Fix Deployment Values (.yaml or.cue)
   _Update your infrastructure-as-code repository to point Helm values to the correct `baseURL` and `managementApiAudience`._

   ```yaml
   global:
     oauth:
       baseURL: "https://fitfile-test.eu.auth0.com"
       managementApiAudience: "https://fitfile-test.eu.auth0.com/api/v2/"
   ```

   _Commit → Push → Sync ArgoCD._

---

### Phase 3: Final Verification

_Force the orchestrator to spin down failing pods and boot fresh ones leveraging the newly synced configuration map._

1. Restart Services After Fix
   ![[cmd_kubectl_rollout_restart_deployment#1. The Command]]

2. Verify Expected Healthy Behaviour
   - [ ] `ffcloud` init completes successfully.
   - [ ] Mongo tenant is visibly created (if observing logs).
   - [ ] `fitconnect` starts normally.
   - [ ] Pods reach `READY 1/1` state with zero loops.

---

### 🔐 Key Lesson

Vault does not validate identity context.

It will happily inject credentials that cannot possibly work with your configured Auth0 domain. Kubernetes then faithfully deploys a system that can never authenticate. Ensure Vault payloads match Helm environments.

---

## Related

- [[cmd_kubectl_get_init_container_logs]]
- [[cmd_curl_auth0_token_test]]
- [[SoT - FitFile Identity & Access Management (Auth0)]]
- [[Protocol - VSO Secret Management & Troubleshooting]]
