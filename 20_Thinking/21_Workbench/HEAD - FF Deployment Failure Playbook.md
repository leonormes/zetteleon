---
created: 2025-12-04T12:02:41Z
last_reviewed: null
modified: 2026-02-12T13:02:03+00:00
status: processing
tags: [state/thinking]
title: HEAD - FF Deployment Failure Playbook
type: head
updated: null
---

Issue: ffcloud / fitconnect CrashLoopBackOff during new environment deployment

Last Updated: 2026-02-12

Applies To: HIE / FFNode deployments using Vault Secrets Operator + Auth0 M2M authentication

---

## 🔎 Summary

New deployments may fail with:

- ffcloud-service stuck in Init:CrashLoopBackOff
- fitconnect-ftc in CrashLoopBackOff
- Auth0 token errors (401 → later 403)
- Errors referencing Tenant not found
- Secrets appear present but services still fail to start

Root Cause:

Deployment was configured to use Auth0 PROD endpoints while Vault supplied TEST tenant credentials.

This tenant mismatch caused Auth0 to reject token requests, preventing ffcloud initialization, which in turn prevented tenant seeding required by fitconnect.

---

## 🧠 Architecture Dependency (Why This Breaks Everything)

Startup order is critical:

```
Vault → Kubernetes Secret → ffcloud init → Tenant seeded in Mongo → fitconnect starts
```

If ffcloud cannot authenticate with Auth0:

- Init fails ❌
- Tenant never created ❌
- fitconnect cannot find tenant ❌
- Whole deployment appears broken ❌

This is not a Kubernetes failure—it is an identity configuration mismatch.

---

## 🚨 Symptoms

|Component|Symptom|Meaning|
|---|---|---|
|ffcloud init|AuthTokenDecodeError|Cannot authenticate to Auth0|
|Auth0 response|401 Unauthorized|Secret missing / wrong|
|Auth0 response|403 Forbidden|Correct secret, wrong tenant / audience|
|fitconnect|Tenant with id "<client_id>" does not exist|ffcloud never seeded tenant|
|Pods|Restarting endlessly|Init dependency failing|

---

## 🔍 Investigation Steps (Run in Order)

---

### 1️⃣ Check Pod State

```sh
kubectl get pods -n <namespace>
```

Look for:

- Init:CrashLoopBackOff
- Error
- Repeated restarts

---

### 2️⃣ Inspect Ffcloud Init Logs (Most Important Signal)

```sh
kubectl logs -n <ns> <ffcloud-pod> -c <init-container>
kubectl logs -n <ns> <ffcloud-pod> -c <init-container> --previous
```

Example failure:

```sh
POST https://fitfile-prod.eu.auth0.com/oauth/token
status: 403 Forbidden
```

➡️ Indicates Auth0 mismatch—NOT Kubernetes issue.

---

### 3️⃣ Confirm Secrets Rendered by Vault

```sh
kubectl get secret ffcloud -n <ns> \
  -o jsonpath='{.data.auth\.json}' | base64 -d; echo
```

Verify values exist:

```sh
clientId
clientSecret
audience
```

If empty → Vault template problem.

If populated → move to Auth0 validation.

---

### 4️⃣ Validate VaultStaticSecret Mapping

```sh
kubectl get vaultstaticsecrets -n <ns>
kubectl get vaultstaticsecret ffcloud -n <ns> -o yaml
```

Check template references:

```json
{{ get .Secrets "auth0_client_id" }}
{{ get .Secrets "auth0_client_secret" }}
```

Ensure keys exist in Vault path:

```sh
admin/deployments/<deployment>/application
```

---

### 5️⃣ Verify Auth0 Endpoint Matches Credential Tenant

Manually test token request using Vault credentials:

```sh
curl --request POST \
  --url https://<tenant>.auth0.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{
    "client_id":"XXX",
    "client_secret":"XXX",
    "audience":"https://<tenant>.auth0.com/api/v2/",
    "grant_type":"client_credentials"
  }'
```

If this only works against test tenant, but app calls prod, you found the issue.

---

### 6️⃣ Check Rendered Application Config (What the Pods Actually Use)

```sh
kubectl get configmap -n <ns> <fitconnect-config> -o yaml
```

Look for:

```sh
"baseURL": "https://fitfile-prod.eu.auth0.com"
"managementApiAudience": "https://fitfile-prod.eu.auth0.com/api/v2/"
```

Mismatch between:

- ConfigMap → PROD
- Vault Secret → TEST

This causes the 403.

---

## 🛠 Root Cause

Configuration Drift Between Three Systems:

|System|Value|
|---|---|
|Vault|TEST Auth0 credentials|
|Helm Values|PROD Auth0 URLs|
|Application|Uses Helm-rendered URLs|
|Auth0|Rejects cross-tenant token exchange|

Auth0 correctly rejects the request because client IDs are tenant-scoped.

---

## ✅ Resolution

Update Helm values to match the tenant where the credentials live.

### Fix in Deployment Values

```yaml
global:
  oauth:
    baseURL: "https://fitfile-test.eu.auth0.com"
    managementApiAudience: "https://fitfile-test.eu.auth0.com/api/v2/"
```

Commit → ArgoCD sync → redeploy.

---

### Restart Services After Fix

```sh
kubectl rollout restart deployment <ffcloud> -n <ns>
kubectl rollout restart deployment <fitconnect> -n <ns>
```

---

## ✔️ Expected Healthy Behaviour

After fix:

|Step|Result|
|---|---|
|ffcloud init|Completes successfully|
|Mongo|Tenant created|
|fitconnect|Starts normally|
|Pods|READY 1/1|
|No more CrashLoops|Stable deployment|

---

## ⚠️ Common Misdiagnoses

Do NOT waste time checking:

- Kubernetes networking
- Mongo connectivity
- Vault authentication
- TLS / ingress
- Container image bugs

If you see Auth0 401/403 during init, it is almost always tenant mismatch or M2M authorization.

---

## 🧩 Why Fitconnect Error Is Misleading

```sh
Tenant with id "<client_id>" does not exist
```

This is a downstream failure:

- ffcloud should create that tenant.
- It never ran successfully.

Fix ffcloud → fitconnect fixes itself.

---

## 🧭 Preventative Checklist for Future Deployments

Before deploying any new environment:

✔ Confirm which Auth0 tenant is intended (test/prod)

✔ Ensure Vault secrets belong to that tenant

✔ Ensure Helm values reference same tenant URLs

✔ Validate curl token request manually

✔ Never mix TEST credentials with PROD endpoints

---

## 🔐 Key Lesson

Vault does not validate identity context.

It will happily inject credentials that cannot possibly work with your configured Auth0 domain.

Kubernetes then faithfully deploys a system that can never authenticate.

---

## 📚 Quick Diagnostic Command Bundle

Use this block next time:

```sh
kubectl get pods -n <ns>
kubectl logs -n <ns> <ffcloud-pod> -c <init>
kubectl get secret ffcloud -n <ns> \
  -o jsonpath='{.data.auth\.json}' | base64 -d; echo
kubectl get configmap -n <ns> <fitconnect-config> -o yaml \
  | grep auth0 -n
# Test credentials directly
curl https://<tenant>.auth0.com/oauth/token ...
```

If tenant mismatch appears → stop debugging Kubernetes.

---

Owner: Platform Engineering

Category: Identity / Environment Parity Issue

Severity: High (deployment-blocking, non-obvious)

If you'd like, I can also produce a shortened "on-call quick reference" version for responders.
