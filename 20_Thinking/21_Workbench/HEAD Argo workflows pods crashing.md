---
captured: "2026-03-07T16:52:54+00:00 2026-03-07T16:52:54+00:00"
created: 2026-03-07T16:52:58+00:00
modified: 2026-03-14T11:10:45+00:00
source: "https://claude.ai/chat/0773aa0a-0948-48c8-98e0-f8c19fa826b0"
status: "processing"
tags: ["input"]
title: HEAD Argo workflows pods crashing
type: "head"
---

## Raw Output / Content

kubectl get pods -n argo NAME READY STATUS RESTARTS AGE argo-workflows-server-8d7fbdbc7-x9tdz 0/1 CrashLoopBackOff 17 (104s ago) 64m argo-workflows-workflow-controller-56bdc6f8f7-vz99t 0/1 CrashLoopBackOff 17 (89s ago) 64m

---

Both pods are in CrashLoopBackOff—they're starting, crashing, and Kubernetes keeps restarting them. Let's get the logs to find out _why_.

Immediate next action—run this:

The `--previous` flag grabs logs from the _last crashed instance_ (since the current one may not have produced output yet).

Then the same for the controller:

Paste both outputs here and I'll pinpoint the issue. The most common culprits for both pods crashing together are:

- Missing or misconfigured auth/SSO—bad OIDC config, unreachable Dex endpoint
- Database connectivity—can't reach Postgres/MySQL if you're using one for artifact/workflow persistence
- ConfigMap or Secret reference errors—a referenced Secret (like TLS certs or SSO client credentials) doesn't exist in the namespace
- RBAC / ServiceAccount issues—less common for CrashLoop, more typical for permission errors at runtime

The logs will tell us which one. Go grab them.

---

kubectl logs -n argo argo-workflows-server-8d7fbdbc7-x9tdz --previous {"time":"2026-03-03T11:21:23.727845318Z","level":"INFO","msg":"not enabling pprof debug endpoints"} {"time":"2026-03-03T11:21:23.729210313Z","level":"INFO","msg":"Starting Argo Server","authModes":\["client"\],"namespace":"argo","managedNamespace":"","ssoNamespace":"argo","baseHRef":"/","secure":true} {"time":"2026-03-03T11:21:23.729284542Z","level":"INFO","msg":"Generating Self Signed TLS Certificates for Secure Mode"} {"time":"2026-03-03T11:21:23.730282022Z","level":"INFO","msg":"SSO disabled"} {"time":"2026-03-03T11:21:23.753367731Z","level":"INFO","msg":"Starting Argo Server","buildDate":"2025-09-17T06:08:44Z","gitCommit":"41a9328efd150a3763590dab2379c403da4841ef","gitTag":"untagged","gitTreeState":"clean","goVersion":"go1.24.4","version":"untagged","instanceID":""} {"time":"2026-03-03T11:21:23.776481749Z","level":"ERROR","msg":"failed to connect to `user= database=argoworkflows`: 10.244.1.118:5432 (ff-lca-prd-2-postgresql-0.ff-lca-prd-2-postgresql-hl.lca-prd-2.svc.cluster.local): server error: FATAL: no PostgreSQL user name specified in startup packet (SQLSTATE 28000)"} ➜ terraform kubectl logs -n argo argo-workflows-workflow-controller-56bdc6f8f7-vz99t --previous time=2026-03-03T11:21:38.501Z level=INFO msg="index config" indexWorkflowSemaphoreKeys=true time=2026-03-03T11:21:38.501Z level=INFO msg="cron config" cronSyncPeriod=10s time=2026-03-03T11:21:38.501Z level=INFO msg="Memoization caches will be garbage-collected if they have not been hit after" gcAfterNotHitDuration=30s {"time":"2026-03-03T11:21:38.50127092Z","level":"INFO","msg":"not enabling pprof debug endpoints"} {"time":"2026-03-03T11:21:38.533868618Z","level":"INFO","msg":"Configuration","config":"artifactRepository: {}\\nexecutor:\\n imagePullPolicy: Always\\n name: \\"\\"\\n resources:\\n requests:\\n cpu: 100m\\n memory: 100Mi\\ninitialDelay: 0s\\nmetricsConfig:\\n enabled: true\\n path: /metrics\\n port: 9090\\n secure: false\\nnodeEvents:\\n enabled: true\\npersistence:\\n archive: true\\n postgresql:\\n database: argoworkflows\\n host: ff-lca-prd-2-postgresql-0.ff-lca-prd-2-postgresql-hl.lca-prd-2.svc.cluster.local\\n passwordSecret:\\n key: password\\n name: argo-postgres-config\\n port: 5432\\n ssl: true\\n sslMode: disable\\n tableName: argo\_workflows\\n userNameSecret:\\n key: username\\n name: argo-postgres-config\\npodSpecLogStrategy: {}\\nsso:\\n clientId:\\n key: \\"\\"\\n clientSecret:\\n key: \\"\\"\\n issuer: \\"\\"\\n redirectUrl: \\"\\"\\n sessionExpiry: 0s\\ntelemetryConfig:\\n enabled: true\\n path: /telemetry\\n port: 8081\\n secure: false\\nworkflowEvents:\\n enabled: true\\n"} {"time":"2026-03-03T11:21:38.533890427Z","level":"INFO","msg":"Persistence configuration enabled"} {"time":"2026-03-03T11:21:38.592891995Z","level":"ERROR","msg":"Failed to update config","error":"failed to connect to `user= database=argoworkflows`: 10.244.1.118:5432 (ff-lca-prd-2-postgresql-0.ff-lca-prd-2-postgresql-hl.lca-prd-2.svc.cluster.local): server error: FATAL: no PostgreSQL user name specified in startup packet (SQLSTATE 28000)"}

---

Got it. The error is crystal clear:

> `failed to connect to ` user= database=argoworkflows\`\`

The username is empty. Both pods are trying to connect to PostgreSQL but the credential lookup is failing silently, resulting in a blank user.

The root cause is in the persistence config—it references a Secret called `argo-postgres-config` with keys `username` and `password`, but either:

1. The Secret doesn't exist in the `argo` namespace
2. The Secret exists but the key names don't match (`username` / `password`)
3. The Secret exists with the right keys but the values are empty

Immediate next action—run this:

This will show you the base64-encoded keys present in the secret (without decoding the actual password in your terminal). If it errors with `NotFound`, that's your answer.

If the secret _does_ exist, decode the username to check it's not blank:

Paste what you get and we'll fix it in one step.

---

kubectl get secret argo-postgres-config -n argo -o jsonpath='{.data}' {"\_raw":"eyJkYXRhIjp7InBvc3RncmVzcWxfcGFzc3dvcmQiOiJ5QUd5d1AxSzJzQ0txU1ZEcWxlZjJHY3EiLCJwb3N0Z3Jlc3FsX3VzZXJuYW1lIjoicG9zdGdyZXMifSwibWV0YWRhdGEiOnsiY3JlYXRlZF90aW1lIjoiMjAyNi0wMS0yN1QxMzozNjoxNC4wMDM4ODk5OTVaIiwiY3VzdG9tX21ldGFkYXRhIjpudWxsLCJkZWxldGlvbl90aW1lIjoiIiwiZGVzdHJveWVkIjpmYWxzZSwidmVyc2lvbiI6M319","password":"","username":""}% ➜ terraform kubectl get secret argo-postgres-config -n argo -o jsonpath='{.data.username}' | base64 -d; echo ➜ terraform kubectl get secret argo-postgres-config -n argo -o jsonpath='{.data}' | base64 -d; echo base64: invalid input

---

There's the problem. Classic Vault Secrets Operator (VSO) key mismatch.

What's happening: VSO is syncing from HCP Vault, but it's dumping everything into a single `_raw` key with the full Vault JSON payload. The actual credentials live _inside_ that blob:

- `postgresql_username` → `postgres`
- `postgresql_password` → `[[REDACTED]]`

Meanwhile, Argo's config expects top-level keys called `username` and `password`—which are empty.

The fix is in your VaultStaticSecret (or VaultDynamicSecret) CR. You need to add a `destination.transformation` to extract and remap those keys.

Step 1—find the VSO CR:

If nothing comes back, try:

Step 2—once you have the name, inspect it:

Paste that output here. What we're looking for is the `destination` block—we'll need to add something like this:

This tells VSO: "Don't just dump the raw blob—extract the individual fields into the keys Argo actually expects."

Go grab the CR definition and we'll write the exact patch.

---

kubectl get vaultstaticsecrets -n argo NAME AGE argo-postgres-config 66m ➜ terraform kubectl get vaultdynamicsecrets -n argo NAME AGE fitfile-image-pull-secret 7d ➜ terraform kubectl get vaultstaticsecret argo-postgres-config -n argo -o yaml apiVersion: secrets.hashicorp.com/v1beta1 kind: VaultStaticSecret metadata: annotations: argocd.argoproj.io/tracking-id: argo-workflows:secrets.hashicorp.com/VaultStaticSecret:argo/argo-postgres-config kubectl.kubernetes.io/last-applied-configuration: | {"apiVersion":"secrets.hashicorp.com/v1beta1","kind":"VaultStaticSecret","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"argo-workflows:secrets.hashicorp.com/VaultStaticSecret:argo/argo-postgres-config"},"name":"argo-postgres-config","namespace":"argo"},"spec":{"destination":{"create":true,"name":"argo-postgres-config","transformation":{"excludes":\[".\*"\],"templates":{"password":{"text":"{{ get.Secrets \\"password\\" }}"},"username":{"text":"{{ get.Secrets \\"username\\" }}"}}}},"hmacSecretData":true,"mount":"secrets","namespace":"admin/deployments/lca-prd-2","path":"argo-workflows","refreshAfter":null,"rolloutRestartTargets":\[\],"type":"kv-v2","vaultAuthRef":"default"}} creationTimestamp: "2026-03-03T10:18:57Z" finalizers: - vaultstaticsecret.secrets.hashicorp.com/finalizer generation: 5 name: argo-postgres-config namespace: argo resourceVersion: "7984522" uid: fc7b227c-abd1-47be-976f-bbf64b9c94bd spec: destination: create: true name: argo-postgres-config overwrite: true transformation: excludes: -.\* templates: password: text: '{{ get.Secrets "password" }}' username: text: '{{ get.Secrets "username" }}' hmacSecretData: true mount: secrets namespace: admin/deployments/lca-prd-2 path: argo-workflows rolloutRestartTargets: \[\] type: kv-v2 vaultAuthRef: default status: lastGeneration: 5 secretMAC: O+N9mPsikQjV1gcbNs+cJgdMFAYkIJTYDyjvT0fRSYU=

---

Spotted it. The templates are looking for keys called `password` and `username`, but the Vault secret stores them as `postgresql_password` and `postgresql_username`. Simple key name mismatch.

The fix—update the two template references:

Find the `templates` block and change it from:

To:

Save and exit. VSO will re-reconcile and populate the `username` and `password` keys in the Kubernetes Secret with the actual values.

However—since this is managed by ArgoCD (I can see the tracking annotation), editing in-cluster will get reverted. The proper fix is in whatever source repo defines this manifest. So:

1. Quick test now—do the `kubectl edit` above to confirm it fixes the crash
2. Permanent fix—update the Helm values or kustomize overlay in your Git repo where this VaultStaticSecret is defined, then let ArgoCD sync it

After the edit, verify the secret populated correctly:

That should now return `postgres`. The pods will likely self-recover on the next CrashLoop restart cycle (within ~5 minutes given 17 restarts), or you can force it:

Give it a go and let me know what comes back.

---

I have a values.yaml that had those password: text: '{{ get.Secrets "password" }}' username: text: '{{ get.Secrets "username" }}' in and I have correct and pushed them. How do I force argocd and vso to pick up those changes

---

Two steps—ArgoCD first, then VSO.

Step 1—Force ArgoCD to sync the new manifest:

If you don't have the ArgoCD CLI handy, you can do it with kubectl:

Verify the VaultStaticSecret has the updated templates:

You should see `postgresql_password` and `postgresql_username` in the output.

Step 2—Force VSO to re-reconcile the secret:

The quickest way is to bump the generation by touching an annotation:

Then confirm the secret is now populated:

Should return `postgres`.

Step 3—Bounce the Argo pods:

Run those in order and paste back anything unexpected.

---

kubectl get secret argo-postgres-config -n argo -o jsonpath='{.data.username}' | base64 -d; echo ➜ terraform kubectl annotate application argo-workflows -n argocd argocd.argoproj.io/refresh=hard --overwrite application.argoproj.io/argo-workflows annotated ➜ terraform kubectl get vaultstaticsecret argo-postgres-config -n argo -o jsonpath='{.spec.destination.transformation.templates}'; echo {"password":{"text":"{{ get.Secrets \\"password\\" }}"},"username":{"text":"{{ get.Secrets \\"username\\" }}"}}

---

ArgoCD hasn't synced yet—the templates still show the old keys. The `refresh=hard` annotation just tells ArgoCD to re-read the repo, but it won't apply changes if auto-sync isn't enabled or if it's waiting for a sync window.

Force the actual sync:

This will tell us if auto-sync is on. Either way, force it explicitly:

If you don't have the CLI authenticated, use kubectl directly:

After that, check the templates again:

Once you see `postgresql_password` / `postgresql_username` in the output, we're good to proceed with the VSO re-reconcile and pod bounce.

---

kubectl get vaultstaticsecret argo-postgres-config -n argo -o jsonpath='{.spec.destination.transformation.templates}'; echo {"password":{"text":"{{ get.Secrets \\"password\\" }}"},"username":{"text":"{{ get.Secrets \\"username\\" }}"}} ➜ terraform kubectl get application argo-workflows -n argocd -o jsonpath='{.spec.syncPolicy}'; echo {"automated":{"prune":true,"selfHeal":true},"retry":{"backoff":{"duration":"5s","factor":2,"maxDuration":"3m"},"limit":5},"syncOptions":\["Validate=false","PrunePropagationPolicy=foreground","PruneLast=true","CreateNamespace=true"\]} ➜ terraform kubectl patch application argo-workflows -n argocd --type merge -p '{"operation":{"initiatedBy":{"username":"admin"},"sync":{"revision":"HEAD","syncStrategy":{"hook":{}}}}}' ➜ terraform kubectl get vaultstaticsecret argo-postgres-config -n argo -o jsonpath='{.spec.destination.transformation.templates}'; echo {"password":{"text":"{{ get.Secrets \\"password\\" }}"},"username":{"text":"{{ get.Secrets \\"username\\" }}"}} ➜ terraform kubectl get vaultstaticsecret argo-postgres-config -n argo -o jsonpath='{.spec.destination.transformation.templates}'; echo ➜ terraform kubectl patch application argo-workflows -n argocd --type merge -p '{"operation":{"initiatedBy":{"username":"admin"},"sync":{"revision":"HEAD","syncStrategy":{"hook":{}}}}}' application.argoproj.io/argo-workflows patched ➜ terraform kubectl get vaultstaticsecret argo-postgres-config -n argo -o jsonpath='{.spec.destination.transformation.templates}'; echo {"password":{"text":"{{ get.Secrets \\"password\\" }}"},"username":{"text":"{{ get.Secrets \\"username\\" }}"}}

---

ArgoCD is auto-syncing with selfHeal but still not picking up the change. Let's figure out why. Either it hasn't fetched the latest commit, or the rendered manifest doesn't look different to what ArgoCD expects.

Step 1—Check what revision ArgoCD is synced to:

Step 2—Check if ArgoCD sees it as out-of-sync:

Step 3—Force a repo cache refresh and check what ArgoCD would render:

If you don't have the CLI, force the repo cache bust:

Then check the sync status again:

Also—worth confirming the commit actually landed in the branch ArgoCD is tracking:

Check that matches the branch you pushed to. Paste what comes back from these and we'll narrow it down.

---

kubectl get application argo-workflows -n argocd -o jsonpath='{.status.sync.revision}'; echo ➜ terraform kubectl get application argo-workflows -n argocd -o jsonpath='{.status.sync.status}'; echo Unknown ➜ terraform kubectl annotate application argo-workflows -n argocd argocd.argoproj.io/refresh=hard --overwrite application.argoproj.io/argo-workflows annotated ➜ terraform kubectl get application argo-workflows -n argocd -o jsonpath='{.status.sync.status}'; echo kubectl get application argo-workflows -n argocd -o jsonpath='{.status.operationState.message}'; echo Unknown ComparisonError: Failed to load target state: failed to generate manifest for source 1 of 1: rpc error: code = Unknown desc = unable to get tags: failed to get tags: GET "": GET " [https://fitfileregistry.azurecr.io/oauth2/token?scope=repository%3Ahelm%2Fargo-workflows%3Ametadata\_read%2Cpull&service=fitfileregistry.azurecr.io](https://fitfileregistry.azurecr.io/oauth2/token?scope=repository%3Ahelm%2Fargo-workflows%3Ametadata_read%2Cpull&service=fitfileregistry.azurecr.io) ": response status code 401: unauthorized: Invalid clientid or client secret. ➜ terraform kubectl get application argo-workflows -n argocd -o jsonpath='{.spec.source.targetRevision}'; echo 0.45.\* ➜ terraform

---

There's the blocker—ArgoCD can't reach your Helm chart at all. The sync status is `Unknown` because it's failing before it even gets to comparing manifests:

> `unauthorized: Invalid clientid or client secret` against `fitfileregistry.azurecr.io`

ArgoCD's credentials for your ACR Helm registry are expired or wrong. This is why your push hasn't taken effect—ArgoCD can't pull the chart to render anything.

Step 1—Check how the repo is configured:

Step 2—Inspect the repo secret (without leaking the password):

Step 3—Check if this is also a VSO-managed secret:

The fix will depend on how these ACR credentials are managed—if it's a service principal, the client secret may have expired. If it's VSO-managed, we may have a similar template key mismatch to the one we just fixed.

Paste the output and we'll sort the credential issue, which will unblock the sync, which will deploy your VSO fix, which will fix Argo Workflows. One domino at a time.

---

kubectl get application argo-workflows -n argocd -o jsonpath='{.spec.source.targetRevision}'; echo 0.45.\* ➜ terraform kubectl get secrets -n argocd -l argocd.argoproj.io/secret-type=repository | grep -i fitfile argocd-repo-fitfile-deployment-repo Opaque 5 6d18h ➜ terraform kubectl get secrets -n argocd -l argocd.argoproj.io/secret-type=repository -o jsonpath='{range.items\[\*\]}{.metadata.name}{"\\t"}{.data.url}{"\\n"}{end}' | while read name url; do echo "$name -> $(echo $url | base64 -d)"; done argocd-acr-pull-secret -> fitfileregistry.azurecr.io argocd-group-creds -> [https://gitlab.com/fitfile](https://gitlab.com/fitfile) argocd-repo-creds-acr -> [https://fitfileregistry.azurecr.io](https://fitfileregistry.azurecr.io/) argocd-repo-fitfile-deployment-repo -> [https://gitlab.com/fitfile/deployment.git](https://gitlab.com/fitfile/deployment.git) argocd-values-repo-creds -> [https://gitlab.com/fitfile/customers/nwsde/lca-infrastructure-prd.git](https://gitlab.com/fitfile/customers/nwsde/lca-infrastructure-prd.git) ➜ terraform kubectl get vaultstaticsecrets -n argocd kubectl get vaultdynamicsecrets -n argocd NAME AGE argocd-group-creds 7d argocd-repo-fitfile-deployment-repo 6d20h argocd-secret 7d argocd-values-repo-creds 21h NAME AGE argocd-pull 7d23h argocd-repo-creds-acr 7d fitfile-image-pull-secret 7d

---

The ACR credentials come from a VaultDynamicSecret—`argocd-repo-creds-acr`. Dynamic secrets rotate, so this has likely either failed to renew or has the same kind of template key mismatch.

Step 1—Check the VDS status:

This will show us the spec (what keys it's mapping), the status (whether the lease is valid), and any error conditions.

Paste that and we'll see if it's a renewal failure, an expired lease, or another template mismatch.

---

kubectl get vaultdynamicsecret argocd-repo-creds-acr -n argocd -o yaml apiVersion: secrets.hashicorp.com/v1beta1 kind: VaultDynamicSecret metadata: annotations: force-sync: "1771940526" creationTimestamp: "2026-02-24T10:39:48Z" finalizers: - vaultdynamicsecret.secrets.hashicorp.com/finalizer generation: 1 name: argocd-repo-creds-acr namespace: argocd resourceVersion: "7955411" uid: c6d4f8d1-6179-4df1-94f2-6f58b9150794 spec: destination: create: true labels: argocd.argoproj.io/secret-type: repository name: argocd-repo-creds-acr overwrite: false transformation: templates: name: text: ACR password: text: '{{.Secrets.client\_secret }}' type: text: helm url: text: [https://fitfileregistry.azurecr.io](https://fitfileregistry.azurecr.io/) username: text: '{{.Secrets.client\_id }}' mount: central namespace: admin path: azure/creds/acr-pull renewalPercent: 67 vaultAuthRef: default status: lastGeneration: 1 lastRenewalTime: 1772530844 lastRuntimePodUID: c4139000-d320-4066-bef4-1b06bb21f088 secretLease: duration: 43200 id: azure/creds/acr-pull/BjL467wSUGu9mQ5FeJ3LIGKQ.jPL3k renewable: true requestID: 5ce79969-51f9-bec3-4d60-eb20668e7f3b staticCredsMetaData: lastVaultRotation: 0 rotationPeriod: 0 ttl: 0 vaultClientMeta: cacheKey: jwt-9667eb11d744f303be35db id: 48323a6389b18ad357a6a63c0781ddf5b40635c156c83a2d35cb1404535719f6

---

The VDS spec and lease look healthy—templates are correct, lease was recently renewed. But one thing jumps out: `overwrite: false`.

This means if the Kubernetes secret already existed (e.g. created manually or by a previous deployment) before VSO took ownership, VSO won't update it with fresh credentials on renewal. The lease renews in Vault but the rotated creds never make it into the actual Secret.

Step 1—Verify the secret has actual credentials:

If that returns an actual client ID (a UUID), the creds are there but may be stale from an earlier lease. If it's empty, same key mismatch problem as before.

Step 2—Fix the overwrite and force a refresh:

Then force VSO to re-reconcile:

Step 3—Verify the secret updated:

Once that returns a valid client ID, ArgoCD should be able to pull the chart, sync your updated values, fix the Argo Workflows VaultStaticSecret, and the pods will come up. The full domino chain.

Paste what you get back.

---

kubectl get secret argocd-repo-creds-acr -n argocd -o jsonpath='{.data.username}' | base64 -d; echo 1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a ➜ terraform kubectl patch vaultdynamicsecret argocd-repo-creds-acr -n argocd --type merge -p '{"spec":{"destination":{"overwrite":true}}}' vaultdynamicsecret.secrets.hashicorp.com/argocd-repo-creds-acr patched ➜ terraform kubectl annotate vaultdynamicsecret argocd-repo-creds-acr -n argocd force-sync=$(date +%s) --overwrite vaultdynamicsecret.secrets.hashicorp.com/argocd-repo-creds-acr annotated ➜ terraform kubectl get secret argocd-repo-creds-acr -n argocd -o jsonpath='{.data.username}' | base64 -d; echo 1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a

---

The client ID is there and looks like a valid UUID, so the secret isn't empty—the credentials are just invalid in Azure. The `overwrite: false` meant VSO was renewing the Vault lease but never writing fresh credentials to the K8s secret. The creds in there are likely from the initial creation 7 days ago and have since been rotated in Vault without the secret being updated.

Now that overwrite is `true`, we need VSO to actually generate a new lease (not just renew the stale one).

Step 1—Delete the lease to force a brand new credential issuance:

Then reapply it (ArgoCD should recreate it since it manages the argocd namespace, or if it's defined elsewhere):

Actually—safer approach. Rather than deleting, force a new lease by bumping the generation:

Wait a few seconds, then check if the client ID changed (indicating fresh creds):

Step 2—If the client ID hasn't changed, test if the current creds are actually valid:

Just to confirm there _is_ a password. Then test the auth directly:

This will tell us if the SP credentials are genuinely expired in Azure or if there's a different ACR auth issue. Paste what you get.

---

kubectl delete vaultdynamicsecret argocd-repo-creds-acr -n argocd vaultdynamicsecret.secrets.hashicorp.com "argocd-repo-creds-acr" deleted from argocd namespace ➜ terraform kubectl get application -n argocd -o name | xargs -I{} kubectl get {} -n argocd -o jsonpath='{.spec.source.path}{"\\n"}' ➜ terraform kubectl get secret argocd-repo-creds-acr -n argocd -o jsonpath='{.data.password}' | base64 -d | head -c 8; echo "…" Error from server (NotFound): secrets "argocd-repo-creds-acr" not found… ➜ terraform kubectl patch vaultdynamicsecret argocd-repo-creds-acr -n argocd --type merge -p '{"spec":{"renewalPercent":66}}' Error from server (NotFound): vaultdynamicsecrets.secrets.hashicorp.com "argocd-repo-creds-acr" not found

---

Right—the VDS is gone, and nothing recreated it. The ArgoCD app paths came back empty, which means this resource isn't managed by ArgoCD—it was likely applied manually or via Terraform.

We have the full spec from earlier. Let's recreate it with `overwrite: true` this time.

Run this:

Then verify it got a fresh lease and wrote credentials:

If the username comes back as a UUID, force ArgoCD to retry:

Then check if the sync error has cleared:

Paste it all back and we'll see if the dominos are falling.

---

sleep 10 && kubectl get vaultdynamicsecret argocd-repo-creds-acr -n argocd -o jsonpath='{.status.secretLease.id}'; echo azure/creds/acr-pull/jd7RED5GswdFsqKAyzfF3bzc.jPL3k ➜ terraform kubectl get secret argocd-repo-creds-acr -n argocd -o jsonpath='{.data.username}' | base64 -d; echo 1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a ➜ terraform kubectl annotate application argo-workflows -n argocd argocd.argoproj.io/refresh=hard --overwrite application.argoproj.io/argo-workflows annotated ➜ terraform kubectl get application argo-workflows -n argocd -o jsonpath='{.status.sync.status}'; echo kubectl get application argo-workflows -n argocd -o jsonpath='{.status.operationState.message}'; echo Unknown ComparisonError: Failed to load target state: failed to generate manifest for source 1 of 1: rpc error: code = Unknown desc = unable to get tags: failed to get tags: GET "": GET " [https://fitfileregistry.azurecr.io/oauth2/token?scope=repository%3Ahelm%2Fargo-workflows%3Ametadata\_read%2Cpull&service=fitfileregistry.azurecr.io](https://fitfileregistry.azurecr.io/oauth2/token?scope=repository%3Ahelm%2Fargo-workflows%3Ametadata_read%2Cpull&service=fitfileregistry.azurecr.io) ": response status code 401: unauthorized: Invalid clientid or client secret.

---

Same error, same client ID even with a brand new lease. This means the service principal itself is the problem—Vault is generating credentials for an SP that Azure is rejecting. Either the SP was deleted/disabled in Entra ID, or the Vault Azure secrets engine's own root config is broken.

Step 1—Test the fresh credentials directly:

If that returns `401`, the SP is genuinely broken in Azure.

Step 2—Check if the SP still exists in Entra ID:

Step 3—Check the Vault Azure engine's role config (if you have Vault CLI access):

or check what role the path uses:

The issue is upstream of Kubernetes now—something is wrong at the Azure/Vault layer. The most likely cause: someone rotated the root SP credentials in the Vault Azure engine, or the `acr-pull` role's SP was deleted or had its permissions revoked in Entra ID.

Let me know what access you have (az CLI, Vault CLI, Azure Portal) and what comes back from these, and we'll trace it to the source.

---

az ad sp show --id 1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a --query '{displayName:displayName, enabled:accountEnabled}' -o table DisplayName Enabled ------------------ --------- HCP Vault ACR Pull True

---

The SP exists and is active, so it's not deleted. The problem is likely one of two things:

1. The SP doesn't have the right role assignment on the ACR (e.g. `AcrPull` was removed)
2. Azure AD propagation delay—Vault just rotated the client secret and Azure hasn't caught up yet (can take 1-2 minutes)

Step 1—Check ACR role assignments:

Step 2—Test the actual credentials from the secret:

This directly tests whether the credentials Vault generated are valid in Azure. If this fails with `AADSTS7000215` or similar, Vault is issuing credentials that Azure doesn't recognise—likely because Vault rotated the secret on the app registration but something went wrong.

Step 3—If the az login works, test ACR specifically:

This will tell us exactly where the chain breaks—is it the credentials themselves, or the ACR permission? Paste the output.

---

I have an azure secret engine in vault with app id d973ad67-bc08-4ba9-91fd-bbeb8fe80d17. This is for vault to access azure. Then there is the identity to get a pull secret. I am using vso. Explain the logic flow of getting the creds. and how we can investigate each component

---

Good call stepping back. Here's the full chain, component by component.

## The Credential Flow

Component 1—Vault Azure Secrets Engine Root Config App ID: `d973ad67-bc08-4ba9-91fd-bbeb8fe80d17`

This is Vault's own service principal—its "root account" for talking to Azure. Vault uses this SP to authenticate to Microsoft Graph / Azure AD, so it can manage other SPs on your behalf. It needs `Application.ReadWrite.All` or equivalent permissions.

Investigate:

This shows the tenant ID, subscription, and client ID Vault is using. If the root SP's own secret has expired, _all_ dynamic credential generation fails silently—Vault may return stale or invalid creds.

Check its credentials haven't expired:

Look at the `EndDateTime` column. If all credentials are past expiry, this is your root cause—Vault can't authenticate to Azure at all.

Component 2—Vault Role Definition This is the role at `central/azure/roles/acr-pull` (or whatever the role is named) that defines _what_ Vault creates when someone requests `central/azure/creds/acr-pull`.

There are two modes:

- Dynamic SP mode—Vault creates a brand new SP each time, assigns it roles, and deletes it when the lease expires
- Static SP mode—Vault rotates the credentials on a pre-existing SP (your `1c2d5c6f…` SP)

Given that you're getting the same client ID across lease renewals, you're in static SP mode—the role is pinned to the `HCP Vault ACR Pull` SP.

Investigate:

This shows the application\_object\_id or SP reference, plus any Azure role assignments Vault should apply.

Component 3—The Target SP App ID: `1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a` (`HCP Vault ACR Pull`)

This is the SP that actually authenticates to ACR. When Vault issues a lease, it generates a new client secret on this SP via the Graph API (using the root SP from Component 1). The new secret is returned to the caller.

Investigate:

Check the SP's current credentials:

If you see dozens of credentials here, Vault has been creating them but possibly not cleaning up. More importantly, check if recent ones were created in the last few minutes (matching your new lease).

Check its ACR role assignment:

You need `AcrPull` scoped to the `fitfileregistry` ACR.

Component 4—VSO (VaultDynamicSecret) This is where we are now. VSO calls `central/azure/creds/acr-pull`, gets back a `client_id` and `client_secret`, and writes them into the K8s secret via the transformation templates.

Investigate:

Look for any error conditions or failed renewal states.

Component 5—ArgoCD Reads the K8s secret labelled `argocd.argoproj.io/secret-type: repository` and uses `username` / `password` to authenticate to `https://fitfileregistry.azurecr.io` as a Helm OCI registry.

---

## Where to Start

The most likely failure point given the symptoms (valid SP, fresh lease, but 401) is Component 1—the root SP. If `d973ad67` 's credentials have expired in Azure, Vault can't call the Graph API to create a new client secret on `1c2d5c6f`. Vault may still return _something_ from the lease, but the password will be stale or invalid.

Run this first:

Then:

These two outputs will tell us where the chain is broken. Paste them both.

---

ault read admin/central/azure/creds/acr-pull No value found at admin/central/azure/creds/acr-pull …/mkuh-prod-3 on  main on ⛵ fitfile-cloud-staging-aks-cluster () on ☁️ Shared Services on 🅰 (eu-west-2) at 11:46:11 ❯ vault read central/azure/creds/acr-pull Key Value --- ----- lease\_id azure/creds/acr-pull/f80cAn1CL1mW4ihC97Mt5FSU.jPL3k lease\_duration 12h lease\_renewable true client\_id 1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a client\_secret [[REDACTED]] …/mkuh-prod-3 on  main on ⛵ fitfile-cloud-staging-aks-cluster () on ☁️ Shared Services on 🅰 (eu-west-2) at 11:46:16 ❯ vault read central/config/root No value found at central/config/root

---

Vault is generating creds successfully. Now let's test if that fresh secret actually works against Azure.

Step 1—Test the credentials Vault just gave you:

Step 2—If that works, test ACR specifically:

Step 3—Now compare: is this the same secret that's in the K8s secret?

If the K8s secret has a _different_ (older) password than what Vault just returned, then VSO wrote the secret once with `overwrite: false` and never updated it despite lease renewals. Recreating the VDS with `overwrite: true` should have fixed that, but the secret may have been created before the patch took effect.

If they differ, the quick fix:

This forces VSO to recreate the secret from scratch with fresh credentials. Then nudge ArgoCD:

Let's see if the credentials are valid first—paste the az login output.

---

az acr login --name fitfileregistry --username "1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a" --password "[[REDACTED]]" Login Succeeded …/mkuh-prod-3 on  main on ⛵ fitfile-cloud-staging-aks-cluster () on ☁️ Shared Services on 🅰 (eu-west-2) at 11:50:44 ❯ az login --service-principal -u "1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a" -p "[[REDACTED]]" --tenant $(az account show --query tenantId -o tsv) --allow-no-subscriptions \[{ "cloudName": "AzureCloud", "homeTenantId": "45e73aa3-1ee9-47c0-ba25-54eda9da021a", "id": "a085dd04-19aa-4d2b-9a35-e438097d84fc", "isDefault": true, "managedByTenants": \[\], "name": "Shared Services", "state": "Enabled", "tenantId": "45e73aa3-1ee9-47c0-ba25-54eda9da021a", "user": { "name": "1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a", "type": "servicePrincipal" } } \] …/mkuh-prod-3 on  main on ⛵ fitfile-cloud-staging-aks-cluster () on ☁️ Shared Services on 🅰 (eu-west-2) at 11:50:57 ❯ az acr login --name fitfileregistry --username "1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a" --password "[[REDACTED]]" Login Succeeded

---

Credentials are valid. The problem is confirmed—the K8s secret has a stale password from the original lease. Let's force the refresh:

Step 1—Delete the stale secret so VSO recreates it:

Step 2—Force VSO to write fresh creds:

Step 3—Verify the new password matches:

Compare that against the working password from your Vault read. They should match (or at least be a recent credential that works).

Step 4—Kick ArgoCD:

We should finally see `Synced` or `OutOfSync` instead of `Unknown`. Go for it.

---

kubectl get secret argocd-repo-creds-acr -n argocd -o jsonpath='{.data.password}' | base64 -d; echo [[REDACTED]] ➜ terraform kubectl get application argo-workflows -n argocd -o jsonpath='{.status.sync.status}'; echo kubectl get application argo-workflows -n argocd -o jsonpath='{.status.operationState.message}'; echo Unknown ComparisonError: Failed to load target state: failed to generate manifest for source 1 of 1: rpc error: code = Unknown desc = unable to get tags: failed to get tags: GET "": GET " [https://fitfileregistry.azurecr.io/oauth2/token?scope=repository%3Ahelm%2Fargo-workflows%3Ametadata\_read%2Cpull&service=fitfileregistry.azurecr.io](https://fitfileregistry.azurecr.io/oauth2/token?scope=repository%3Ahelm%2Fargo-workflows%3Ametadata_read%2Cpull&service=fitfileregistry.azurecr.io) ": response status code 401: unauthorized: Invalid clientid or client secret. ➜ terraform kubectl get secret argocd-repo-creds-acr -n argocd -o jsonpath='{.data.password}' | base64 -d; echo [[REDACTED]] ➜ terraform kubectl delete secret argocd-repo-creds-acr -n argocd kubectl annotate vaultdynamicsecret argocd-repo-creds-acr -n argocd force-sync=$(date +%s) --overwrite secret "argocd-repo-creds-acr" deleted from argocd namespace vaultdynamicsecret.secrets.hashicorp.com/argocd-repo-creds-acr annotated ➜ terraform sleep 10 && kubectl annotate application argo-workflows -n argocd argocd.argoproj.io/refresh=hard --overwrite kubectl get application argo-workflows -n argocd -o jsonpath='{.status.sync.status}'; echo application.argoproj.io/argo-workflows annotated Unknown ➜ terraform kubectl get secret argocd-repo-creds-acr -n argocd -o jsonpath='{.data.password}' | base64 -d; echo 5kP8Q~p9Q\_xq.vg5djR7rD~DnrxBlQ~1doSzeawR ➜ terraform kubectl annotate application argo-workflows -n argocd argocd.argoproj.io/refresh=hard --overwrite sleep 5 && kubectl get application argo-workflows -n argocd -o jsonpath='{.status.sync.status}'; echo application.argoproj.io/argo-workflows annotated Unknown

---

Fresh creds are being written each time (password keeps changing) but ArgoCD still 401s. ArgoCD's repo-server caches repository credentials in memory—it doesn't watch for secret changes. It loaded the stale password at startup and is still using it.

Restart the repo-server to force it to re-read the secret:

Then refresh the app:

This should be the one.

---

kubectl get secret argocd-acr-pull-secret -n argocd -o jsonpath='{.metadata.labels}'; echo kubectl get secret argocd-acr-pull-secret -n argocd -o jsonpath='{.data.username}' | base64 -d; echo kubectl get secret argocd-acr-pull-secret -n argocd -o jsonpath='{.data.password}' | base64 -d | head -c 8; echo "…" {"app.kubernetes.io/component":"secret-sync","app.kubernetes.io/instance":"argocd","app.kubernetes.io/managed-by":"hashicorp-vso","app.kubernetes.io/name":"vault-secrets-operator","app.kubernetes.io/part-of":"argocd","argocd.argoproj.io/secret-type":"repository","secrets.hashicorp.com/vso-ownerRefUID":"85877fbd-b0f5-4e94-9464-3bd726d22d51"} 1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a 6ud8Q~CV… ➜ terraform kubectl get vaultdynamicsecret argocd-pull -n argocd -o yaml apiVersion: secrets.hashicorp.com/v1beta1 kind: VaultDynamicSecret metadata: annotations: force-sync: "1772451100" kubectl.kubernetes.io/last-applied-configuration: | {"apiVersion":"secrets.hashicorp.com/v1beta1","kind":"VaultDynamicSecret","metadata":{"name":"argocd-pull","namespace":"argocd"},"spec":{"destination":{"create":true,"labels":{"app.kubernetes.io/instance":"argocd","app.kubernetes.io/part-of":"argocd","argocd.argoproj.io/secret-type":"repository"},"name":"argocd-acr-pull-secret","transformation":{"excludes":\[".\*"\],"templates":{"ForceHttpBasicAuth":{"text":"true"},"enableOCI":{"text":"true"},"name":{"text":"fitfileregistry"},"password":{"text":"{{get.Secrets \\"client\_secret\\"}}"},"type":{"text":"helm"},"url":{"text":"fitfileregistry.azurecr.io"},"username":{"text":"{{get.Secrets \\"client\_id\\"}}"}}}},"mount":"azure","namespace":"admin/central","path":"creds/acr-pull","vaultAuthRef":"default"}} creationTimestamp: "2026-02-23T11:49:49Z" finalizers: - vaultdynamicsecret.secrets.hashicorp.com/finalizer generation: 1 name: argocd-pull namespace: argocd resourceVersion: "7834204" uid: 85877fbd-b0f5-4e94-9464-3bd726d22d51 spec: destination: create: true labels: app.kubernetes.io/instance: argocd app.kubernetes.io/part-of: argocd argocd.argoproj.io/secret-type: repository name: argocd-acr-pull-secret overwrite: false transformation: excludes: -.\* templates: ForceHttpBasicAuth: text: "true" enableOCI: text: "true" name: text: fitfileregistry password: text: '{{get.Secrets "client\_secret"}}' type: text: helm url: text: fitfileregistry.azurecr.io username: text: '{{get.Secrets "client\_id"}}' mount: azure namespace: admin/central path: creds/acr-pull renewalPercent: 67 vaultAuthRef: default status: lastGeneration: 1 lastRenewalTime: 1772514864 lastRuntimePodUID: c4139000-d320-4066-bef4-1b06bb21f088 secretLease: duration: 43200 id: azure/creds/acr-pull/4UWrY5Fv8gPQ2A4Q7LqpyMNX.jPL3k renewable: true requestID: d17a65d7-a8aa-3962-8304-76018125a436 staticCredsMetaData: lastVaultRotation: 0 rotationPeriod: 0 ttl: 0 vaultClientMeta: cacheKey: jwt-9667eb11d744f303be35db-admin/central id: 48323a6389b18ad357a6a63c0781ddf5b40635c156c83a2d35cb1404535719f6

---

There are two ACR credential secrets, and ArgoCD is likely using the _other_ one. Look at the differences:

| VDS | Secret Name | URL | Has `enableOCI` |
| --- | --- | --- | --- |
| `argocd-repo-creds-acr` (the one we fixed) | `argocd-repo-creds-acr` | `https://fitfileregistry.azurecr.io` | No |
| `argocd-pull` (this one) | `argocd-acr-pull-secret` | `fitfileregistry.azurecr.io` | Yes |

The `argocd-pull` VDS has `enableOCI: true` and `ForceHttpBasicAuth: true`—this is the one ArgoCD uses for Helm OCI pulls. And it has the same problem: `overwrite: false`, so the password is stale.

Same fix. Delete the stale secret, patch the VDS, force resync:

Wait for the secret to repopulate, then restart the repo-server so it picks up the fresh creds:

Then check:

This should be the actual fix—we were patching the wrong secret all along.

---

sleep 10 && kubectl get secret argocd-acr-pull-secret -n argocd -o jsonpath='{.data.password}' | base64 -d | head -c 8; echo "…" kubectl rollout restart deployment argocd-repo-server -n argocd kubectl rollout status deployment argocd-repo-server -n argocd --timeout=60s ImE8Q~rb… deployment.apps/argocd-repo-server restarted Waiting for deployment spec update to be observed… Waiting for deployment "argocd-repo-server" rollout to finish: 0 out of 1 new replicas have been updated… Waiting for deployment "argocd-repo-server" rollout to finish: 1 old replicas are pending termination… Waiting for deployment "argocd-repo-server" rollout to finish: 1 old replicas are pending termination… deployment "argocd-repo-server" successfully rolled out ➜ terraform kubectl annotate application argo-workflows -n argocd argocd.argoproj.io/refresh=hard --overwrite sleep 10 && kubectl get application argo-workflows -n argocd -o jsonpath='{.status.sync.status}'; echo application.argoproj.io/argo-workflows annotated Synced ➜ terraform kubectl get app -n argocd NAME SYNC STATUS HEALTH STATUS argo-workflows Synced Degraded blob-csi-driver Synced Healthy cert-manager Synced Healthy ff-lca-prd-2 OutOfSync Degraded ff-lca-prd-2-postgresql Synced Healthy grafana-k8s-monitoring Synced Healthy prometheus-operator-crds Synced Healthy

---

`Synced`! ArgoCD is pulling from ACR again. It's `Degraded` because the Argo Workflows pods are still crashing from the postgres issue. Let's check if the sync deployed your VaultStaticSecret fix:

If that now shows `postgresql_username` / `postgresql_password`, verify the secret populated:

Should return `postgres`. Then bounce the pods:

We're on the last domino.

---

kubectl get pods -n argo NAME READY STATUS RESTARTS AGE argo-workflows-server-8d7fbdbc7-fn2pv 0/1 ImagePullBackOff 0 21s argo-workflows-workflow-controller-56bdc6f8f7-fqhsc 0/1 ImagePullBackOff 0 21s

---

Different problem now—`ImagePullBackOff` means the _nodes_ can't pull the container images from ACR. This is a separate credential from the Helm chart pull. Let's check:

And check what imagePullSecret the pods are using:

Also check what image it's trying to pull:

There was a VaultDynamicSecret called `fitfile-image-pull-secret` in both the `argo` and `argocd` namespaces from earlier. Same `overwrite: false` pattern likely applies:

Paste the outputs and we'll apply the same fix—patch overwrite, delete stale secret, force resync.

---

kubectl describe pod -n argo argo-workflows-server-8d7fbdbc7-fn2pv | grep -A5 "Events:" | tail -10 Events: Type Reason Age From Message ---- ------ ---- ---- ------- Normal Scheduled 41s default-scheduler Successfully assigned argo/argo-workflows-server-8d7fbdbc7-fn2pv to aks-system-38063810-vmss000001 Normal BackOff 14s (x2 over 39s) kubelet Back-off pulling image "fitfileregistry.azurecr.io/argoproj/argocli:v3.7.2" Warning Failed 14s (x2 over 39s) kubelet Error: ImagePullBackOff ➜ terraform kubectl get pod -n argo argo-workflows-server-8d7fbdbc7-fn2pv -o jsonpath='{.spec.imagePullSecrets}'; echo \[{"name":"fitfile-image-pull-secret"}\] ➜ terraform kubectl get pod -n argo argo-workflows-server-8d7fbdbc7-fn2pv -o jsonpath='{.spec.containers\[0\].image}'; echo fitfileregistry.azurecr.io/argoproj/argocli:v3.7.2 ➜ terraform kubectl get vaultdynamicsecret fitfile-image-pull-secret -n argo -o jsonpath='{.spec.destination.overwrite}'; echo true

---

Overwrite is already `true` on this one, so it's a different issue. Let's check the actual image pull secret:

If it's not a dockerconfigjson type, check what type it is:

And check the VDS spec to see how it's generating the secret:

The image pull secret needs to be type `kubernetes.io/dockerconfigjson` with a `.dockerconfigjson` key containing the auth blob. If VSO is writing it as an `Opaque` secret with `username` / `password` keys, kubelet won't understand it.

---

---

Same stale credential problem. Even though `overwrite: true` is set, the current password in the secret is from an old lease. Force a refresh:

Wait for it to repopulate, then verify the new creds work:

Then delete the pods so they retry the pull with fresh creds:

Also—this same problem will hit every namespace that has a `fitfile-image-pull-secret`. Worth checking how many are affected:

We may need to do a bulk fix across all of them.

---

kubectl delete secret fitfile-image-pull-secret -n argo kubectl annotate vaultdynamicsecret fitfile-image-pull-secret -n argo force-sync=$(date +%s) --overwrite secret "fitfile-image-pull-secret" deleted from argo namespace vaultdynamicsecret.secrets.hashicorp.com/fitfile-image-pull-secret annotated ➜ terraform sleep 10 && kubectl get secret fitfile-image-pull-secret -n argo -o jsonpath='{.data.\\.dockerconfigjson}' | base64 -d | jq -r '.auths | to\_entries\[0\].value.password' | head -c 8; echo "…" QBO8Q~vU… ➜ terraform kubectl delete pods -n argo -l app.kubernetes.io/part-of=argo-workflows pod "argo-workflows-server-8d7fbdbc7-fn2pv" deleted from argo namespace pod "argo-workflows-workflow-controller-56bdc6f8f7-fqhsc" deleted from argo namespace ➜ terraform kubectl get vaultdynamicsecrets -A | grep image-pull argo fitfile-image-pull-secret 7d1h argocd fitfile-image-pull-secret 7d1h cert-manager fitfile-image-pull-secret 7d1h ingress-nginx fitfile-image-pull-secret 7d1h lca-prd-2 fitfile-image-pull-secret 7d1h monitoring fitfile-image-pull-secret 7d1h spicedb fitfile-image-pull-secret 7d1h vault-secrets-operator-system fitfile-image-pull-secret 7d1h

---

Fresh creds written. Let's check if the Argo pods are pulling now:

Give it 30 seconds, then Ctrl+C. While we wait—let's fix all the other namespaces in one go:

Then check the Argo pods status:

And check the VaultStaticSecret fix landed too:

Paste back what you get—we need both the image pull _and_ the postgres creds working for the pods to go `Running`.

---

Before 'fixing' the other ns here is the argo result kubectl get pods -n argo -w NAME READY STATUS RESTARTS AGE argo-workflows-server-8d7fbdbc7-mz27s 0/1 CrashLoopBackOff 2 (22s ago) 38s argo-workflows-workflow-controller-56bdc6f8f7-42rps 0/1 CrashLoopBackOff 2 (23s ago) 38s argo-workflows-workflow-controller-56bdc6f8f7-42rps 0/1 Error 3 (25s ago) 40s argo-workflows-server-8d7fbdbc7-mz27s 0/1 Error 3 (31s ago) 47s argo-workflows-workflow-controller-56bdc6f8f7-42rps 0/1 CrashLoopBackOff 3 (11s ago) 51s

---

Images are pulling—we're past the ACR issue. Back to CrashLoopBackOff, which means we're back to the postgres problem. Let's check if ArgoCD actually deployed the template fix:

And check the secret:

Confirm with the logs:

---

kubectl get vaultstaticsecret argo-postgres-config -n argo -o jsonpath='{.spec.destination.transformation.templates}'; echo {"password":{"text":"{{ get.Secrets \\"password\\" }}"},"username":{"text":"{{ get.Secrets \\"username\\" }}"}} ➜ terraform kubectl get secret argo-postgres-config -n argo -o jsonpath='{.data.username}' | base64 -d; echo ➜ terraform kubectl logs -n argo argo-workflows-server-8d7fbdbc7-mz27s --previous 2>/dev/null | tail -5 {"time":"2026-03-03T12:06:56.34546219Z","level":"INFO","msg":"Starting Argo Server","ssoNamespace":"argo","baseHRef":"/","secure":true,"authModes":\["client"\],"namespace":"argo","managedNamespace":""} {"time":"2026-03-03T12:06:56.345482044Z","level":"INFO","msg":"Generating Self Signed TLS Certificates for Secure Mode"} {"time":"2026-03-03T12:06:56.345867961Z","level":"INFO","msg":"SSO disabled"} {"time":"2026-03-03T12:06:56.366253391Z","level":"INFO","msg":"Starting Argo Server","gitTag":"untagged","gitTreeState":"clean","goVersion":"go1.24.4","instanceID":"","version":"untagged","buildDate":"2025-09-17T06:08:44Z","gitCommit":"41a9328efd150a3763590dab2379c403da4841ef"} {"time":"2026-03-03T12:06:56.388960682Z","level":"ERROR","msg":"failed to connect to `user= database=argoworkflows`: 10.244.1.118:5432 (ff-lca-prd-2-postgresql-0.ff-lca-prd-2-postgresql-hl.lca-prd-2.svc.cluster.local): server error: FATAL: no PostgreSQL user name specified in startup packet (SQLSTATE 28000)"} ➜ terraform

---

ArgoCD synced but the templates still show the old keys. Your values.yaml change isn't making it into the rendered manifest. Let's see what ArgoCD is actually using:

If it uses multiple sources (Helm chart from ACR + values from Git):

Also—which repo did you push the values fix to, and which branch? Let's verify ArgoCD is pointing at the right place and that the rendered output includes your change:

Meanwhile, let's just fix it directly so the pods come up while we sort the GitOps side:

Then verify and bounce:

---

here are the results

---

Now I see the full picture. The values aren't coming from a Git repo—they're inline in the ArgoCD Application spec itself. That's why your values.yaml push never took effect. The VaultStaticSecret is defined under `extraObjects` with the old key names baked into the Application manifest.

The kubectl patch will work for now. Let's verify and get the pods up:

If that returns `postgres`, bounce the pods:

Note the Helm double-escaping: `{{ "{{" }} get.Secrets "postgresql_username" {{ "}}" }}`—keep that pattern.

But first, let's confirm the pods come up. Paste the username check result.

---

it returned nothing sleep 5 && kubectl get secret argo-postgres-config -n argo -o jsonpath='{.data.username}' | base64 -d; echo ➜ terraform

---

The VSS templates are updated but VSO hasn't re-reconciled. Force it:

If still empty, delete the secret so VSO recreates it from scratch:

---

I am still getting this error where the identiy in azure entral has 600 certs. What can I do to find the offending vso code

---

600 credentials on one SP—every VaultDynamicSecret lease renewal creates a new client secret on the SP, and they're never being cleaned up. Let's find every VDS that's generating creds against that path:

That shows every VDS hitting the `acr-pull` path. Each one is independently generating credentials on the same SP.

Also check for any hitting the broader azure mount:

This gives you the full picture—namespace, name, vault path, and overwrite status for every VDS in the cluster.

To see the actual credential pile-up on the SP:

And to see how many are already expired (safe to clean up):

The root problem is architectural—8 namespaces each with a VDS renewing every 67% of a 12h lease means roughly 8 new credentials every ~8 hours. Vault's Azure engine should be revoking old ones on renewal, but with `overwrite: false` the leases were silently failing and accumulating. The fix was setting `overwrite: true`, but the old creds are still piled up.

To purge the expired ones:

Paste the output from the first two commands and we'll see the full scope of the problem.

---

kubectl get vaultdynamicsecrets -A -o jsonpath='{range.items\[\*\]}{.metadata.namespace}{"\\t"}{.metadata.name}{"\\t"}{.spec.mount}/{.spec.path}{"\\n"}{end}' | grep acr argo fitfile-image-pull-secret azure/creds/acr-pull argocd argocd-pull azure/creds/acr-pull argocd fitfile-image-pull-secret azure/creds/acr-pull cert-manager fitfile-image-pull-secret azure/creds/acr-pull ingress-nginx fitfile-image-pull-secret azure/creds/acr-pull lca-prd-2 fitfile-image-pull-secret azure/creds/acr-pull monitoring fitfile-image-pull-secret azure/creds/acr-pull spicedb fitfile-image-pull-secret azure/creds/acr-pull vault-secrets-operator-system fitfile-image-pull-secret azure/creds/acr-pull ➜ ~ kubectl get vaultdynamicsecrets -A -o jsonpath='{range.items\[\*\]}{.metadata.namespace}{"\\t"}{.metadata.name}{"\\t"}{.spec.mount}/{.spec.path}{"\\t"}{.spec.destination.overwrite}{"\\n"}{end}' argo fitfile-image-pull-secret azure/creds/acr-pull true argocd argocd-pull azure/creds/acr-pull true argocd fitfile-image-pull-secret azure/creds/acr-pull true cert-manager fitfile-image-pull-secret azure/creds/acr-pull true ingress-nginx fitfile-image-pull-secret azure/creds/acr-pull true lca-prd-2 fitfile-image-pull-secret azure/creds/acr-pull true monitoring fitfile-image-pull-secret azure/creds/acr-pull true spicedb fitfile-image-pull-secret azure/creds/acr-pull true vault-secrets-operator-system fitfile-image-pull-secret azure/creds/acr-pull true ➜ ~ az ad app credential list --id 1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a --query "length(@)" bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) Insufficient privileges to complete the operation.

---

Insufficient privileges to manage the SP's credentials from the Azure CLI. Let's attack it from the Vault side instead—Vault created those credentials, so it can revoke them.

Step 1—See how many active leases exist:

Step 2—Revoke all stale leases in bulk:

This tells Vault to revoke every lease under that path, which should trigger Vault to clean up the corresponding client secrets on the SP via the Graph API (using the root SP `d973ad67…`).

Step 3—Force all VDS resources to generate fresh single credentials:

Longer-term architectural note: You have 9 VDS resources each independently generating credentials on the same SP every ~8 hours. That's ~27 new client secrets per day. The better pattern is one of:

- Single VDS + shared secret: Generate the credential once and use `kubectl` secret mirroring (e.g. Reflector or ClusterSecretStore) to distribute it across namespaces
- AKS workload identity: Use managed identities instead of SP credentials for ACR pull—no secrets to manage at all. AKS natively supports this with `az aks update --attach-acr`

But first—run the Vault lease revoke and the secret refresh. Paste what comes back, and let's also get the postgres secret sorted so Argo actually starts.

---

vault list -format=json sys/leases/lookup/azure/creds/acr-pull | jq length Error listing sys/leases/lookup/azure/creds/acr-pull: Error making API request. URL: GET [https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/v1/sys/leases/lookup/azure/creds/acr-pull?list=true](https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/v1/sys/leases/lookup/azure/creds/acr-pull?list=true) Code: 403. Errors: \* 1 error occurred: \* permission denied

---

HCP Vault Cloud—you won't have `sys/leases` access. That needs an HCP org admin. Let's focus on what you _can_ do right now.

Immediate priority—get Argo running. The postgres secret is still empty. Let's check if the patch actually stuck after ArgoCD's selfHeal may have reverted it:

If selfHeal reverted it back to `"password"` / `"username"`, ArgoCD is overwriting your manual patch. In that case, temporarily disable selfHeal:

Then re-apply the fix:

For the 600 credentials problem, you need someone with either:

- HCP Vault admin access to run `vault lease revoke -prefix azure/creds/acr-pull`
- Azure AD Application Administrator role to run the credential purge via `az ad app credential delete`

Worth raising this as urgent—at some point Azure will hit a credential limit on the SP and _all_ image pulls across the cluster will fail.

Run the commands above and let's at least get Argo healthy.

---

I do have az access, it was logged in to the wrong tenant fitfile-cloud-staging-aks-cluster () on ☁️ Shared Services on 🅰 (eu-west-2) at 08:54:38 ❯ az ad app credential list --id 1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a --query "\[?endDateTime < '$(date -u +%Y-%m-%dT%H:%M:%SZ)'\] | length(@)" Z)'\] | length(@)")0 ~ on ⛵ fitfile-cloud-staging-aks-cluster () on ☁️ Shared Services on 🅰 (eu-west-2) at 08:54:42 ❯ az ad app credential list --id 1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a --query "\[?endDateTime < '$(date -u +%Y-%m-%dT%H:%M:%SZ)'\] | length(@)" Z)'\] | length(@)")0

---

The shell is mangling the nested quotes. Let's do it in two steps:

And total count:

To purge expired ones:

Also—while that runs, let's get Argo sorted. Did selfHeal revert the patch?

---

NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ) az ad app credential list --id 1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a -o json | jq --arg now "$NOW" '\[.\[\] | select(.endDateTime < $now)\] | length' Z) az ad app credential list --id 1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a -o json | jq --arg now "$NOW" '\[.\[\] | select(.endDateTime < $now)\] | length')0 ~ on ⛵ fitfile-cloud-staging-aks-cluster () on ☁️ Shared Services on 🅰 (eu-west-2) at 08:59:22 ❯ az ad app credential list --id 1c2d5c6f-0b22-459e-97d2-f86a0ba2c20a -o json | jq length 631

---

631 credentials. The date command is being mangled by your shell (looks like zsh). Let's keep it simple:

Then use that literal value:

To purge them, save the key IDs to a file first:

Then delete in a loop:

While that runs—check the Argo fix status:

---

but i already delete them just yesterday and they all came back!

---

Right—deleting credentials is pointless because 9 VDS resources are each creating new ones every ~8 hours. That's ~27 new credentials per day. You're bailing water while the tap is running.

The fix is to stop the flood at the source. You have two practical options:

Option A (Quick)—Keep one VDS, mirror the secret

Delete 8 of the 9 VDS resources so only one namespace generates credentials. Then use Kubernetes Reflector or similar to copy the secret to other namespaces:

Option B (Proper)—AKS managed identity ACR pull

No secrets at all. AKS authenticates to ACR natively:

This grants the AKS kubelet identity `AcrPull` on the registry. No secrets, no rotation, no VSO involvement. Every pod pulls images without `imagePullSecrets`.

Before you choose—which approach fits your constraints better? And let's also get Argo unstuck. Check if selfHeal reverted your postgres fix:

---

forget the argocd it is fixed. The cluster is in a customer tenant so doesn't have access to our acr via a normal inta tenant access. So we are using vault and vso

---

Cross-tenant makes sense—Option B is off the table. The solution is one VDS, replicate the secret.

The approach:

Keep a single VDS in one namespace (e.g. `argocd` or a shared namespace). Then use a secret replicator to copy it to all other namespaces. Two common options:

1\. Kubernetes Reflector (lightweight, annotation-based):

Then annotate the source secret to mirror automatically:

2\. Stakater Replicator—similar concept, different annotations.

Either way the steps are:

1. Pick one namespace to own the VDS (keep that single `fitfile-image-pull-secret` VDS)
2. Delete the other 8 VDS resources
3. Add mirror annotations to the source secret (via the VDS `destination.labels` or `destination.annotations`)
4. Replicator copies it to all target namespaces, stays in sync on updates

This takes you from 27 credential rotations/day to 3. One SP, one lease, one secret, many mirrors.

Worth exploring for your next infrastructure pass—want me to draft the full implementation plan as an Obsidian note?

---

these are the vso logs from our staging

---

There's a specific error in there for the `argocd-pull` VDS:

> `Failed to add client to the cache`… `error: invalid cacheKey for cloned client "approle-5ff224385401730273f855-admin/central"`

This is a VSO bug/limitation with namespace-scoped Vault clients. When `argocd-pull` uses `namespace: admin/central` but authenticates via an approle cached under a different namespace path, VSO can't clone the client into its cache. This means lease management for that VDS is broken—VSO can't properly renew or revoke leases, so old credentials pile up in Azure while new ones keep being created.

This also explains why `overwrite: false` was so destructive. VSO was silently failing to manage leases, creating new SP credentials on every reconciliation loop, but never writing them to the K8s secret _or_ revoking the old ones.

The count of 11 lifetimeWatcher instances starting on boot confirms the scale—each one is a separate Vault lease being tracked.

Immediate actions to stop the bleed:

1. Check if the same cache error affects the `fitfile-image-pull-secret` VDS resources across namespaces:
2. Check if any VDS resources use a different `spec.namespace` than their `vaultAuthRef` expects:
3. And check the VaultAuth `default` config to see what namespace it authenticates under:

The cache key mismatch is likely the root cause of the credential explosion. Paste these outputs and we'll see the full pattern.

---

kubectl logs -n vault-secrets-operator-system deployment/vault-secrets-operator-controller-manager 2>&1 | grep "Failed to add client" {"level":"error","ts":"2026-03-04T09:42:35Z","msg":"Failed to add client to the cache","controller":"vaultdynamicsecret","controllerGroup":"secrets.hashicorp.com","controllerKind":"VaultDynamicSecret","VaultDynamicSecret":{"name":"argocd-pull","namespace":"argocd"},"namespace":"argocd","name":"argocd-pull","reconcileID":"8e4182a3-fa43-47d7-8d5e-66502edb44f3","cacheKey":"approle-5ff224385401730273f855-admin/central","isClone":true,"error":"invalid cacheKey for cloned client \\"approle-5ff224385401730273f855-admin/central\\""} …/rust-chart-manager on  main ✘!? on ⛵ fitfile-cloud-staging-aks-cluster () on ☁️ Shared Services on 🅰 (eu-west-2) at 09:46:08 ❯ kubectl get vaultdynamicsecrets -A -o jsonpath='{range.items\[\*\]}{.metadata.namespace}/{.metadata.name}{"\\t"}mount={.spec.mount}{"\\t"}ns={.spec.namespace}{"\\n"}{end}' argocd/argocd-pull mount=azure ns=admin/central …/rust-chart-manager on  main ✘!? on ⛵ fitfile-cloud-staging-aks-cluster () on ☁️ Shared Services on 🅰 (eu-west-2) at 09:46:15 ❯ kubectl get vaultauth default -n vault-secrets-operator-system -o yaml Error from server (NotFound): vaultauths.secrets.hashicorp.com "default" not found

---

Only `argocd-pull` shows the cache error, and it's the only VDS on this cluster. The `default` VaultAuth isn't in the operator namespace. Let's find where it actually lives:

And check if there's a VaultAuthGlobal:

Also check the VaultConnection:

The cache key issue is specifically because `argocd-pull` uses `namespace: admin/central` (a Vault namespace), and VSO can't reconcile that with the approle auth it's using. We need to see how auth is configured to understand the mismatch.

---

kubectl get vaultauths -A NAMESPACE NAME HEALTHY READY AGE argo default True True 494d argocd default True True 494d cert-manager default True True 494d ff-test-a default True True 494d ff-test-a mesh True True 490d ff-test-a nhs-pet True True 160d ff-test-b default True True 494d ff-test-b nhs-pet True True 160d ff-test-c default True True 494d ff-test-c nhs-pet True True 160d monitoring default True True 494d ohdsi default True True 49d spicedb default True True 494d …/rust-chart-manager on  main ✘!? on ⛵ fitfile-cloud-staging-aks-cluster () on ☁️ Shared Services on 🅰 (eu-west-2) at 09:46:45 ❯ kubectl get vaultauthglobals -A -o yaml apiVersion: v1 items: \[\] kind: List metadata: resourceVersion: "" …/rust-chart-manager on  main ✘!? on ⛵ fitfile-cloud-staging-aks-cluster () on ☁️ Shared Services on 🅰 (eu-west-2) at 09:46:51 ❯ kubectl get vaultconnections -A NAMESPACE NAME HEALTHY READY AGE vault-secrets-operator-system default True True 494d

---

Good—VaultAuth is per-namespace, VaultConnection is global. Let's see the argocd VaultAuth to understand the cache key mismatch:

And the VaultConnection:

The cache error happens because `argocd-pull` authenticates via the argocd VaultAuth (which likely uses one Vault namespace), but then requests credentials from `mount=azure` in `namespace=admin/central` (a different Vault namespace). VSO tries to clone the authenticated client into the different namespace and fails.

---

kubectl get vaultauth default -n argocd -o yaml apiVersion: secrets.hashicorp.com/v1beta1 kind: VaultAuth metadata: annotations: kubectl.kubernetes.io/last-applied-configuration: | {"apiVersion":"secrets.hashicorp.com/v1beta1","kind":"VaultAuth","metadata":{"annotations":{},"labels":{"managedBy":"terraform"},"name":"default","namespace":"argocd"},"spec":{"appRole":{"roleId":"4f005403-4c24-34a4-fc1f-70d82e43882f","secretRef":"role-secrets"},"method":"appRole","mount":"approle","namespace":"admin/deployments/staging"}} creationTimestamp: "2024-10-25T13:11:04Z" finalizers: - vaultauth.secrets.hashicorp.com/finalizer generation: 1 labels: managedBy: terraform name: default namespace: argocd resourceVersion: "346826290" uid: 3afc9342-b249-4180-a078-88d5ce8fc169 spec: appRole: roleId: 4f005403-4c24-34a4-fc1f-70d82e43882f secretRef: role-secrets method: appRole mount: approle namespace: admin/deployments/staging status: conditions: - lastTransitionTime: "2026-03-04T09:42:35Z" message: VaultAuthHealthy observedGeneration: 1 reason: Healthy status: "True" type: Healthy - lastTransitionTime: "2026-03-04T09:42:35Z" message: VaultAuthReady observedGeneration: 1 reason: Ready status: "True" type: Ready specHash: fc2dc19a0686eee30e9d8dab36dbf48b617587574c55068126a832baa36bcf18 valid: true …/rust-chart-manager on  main ✘!? on ⛵ fitfile-cloud-staging-aks-cluster () on ☁️ Shared Services on 🅰 (eu-west-2) at 09:47:56 ❯ kubectl get vaultconnection default -n vault-secrets-operator-system -o yaml apiVersion: secrets.hashicorp.com/v1beta1 kind: VaultConnection metadata: annotations: meta.helm.sh/release-name: vault-secrets-operator meta.helm.sh/release-namespace: vault-secrets-operator-system creationTimestamp: "2024-10-25T13:07:39Z" finalizers: - vaultconnection.secrets.hashicorp.com/finalizer generation: 1 labels: app.kubernetes.io/component: controller-manager app.kubernetes.io/instance: vault-secrets-operator app.kubernetes.io/managed-by: Helm app.kubernetes.io/name: vault-secrets-operator app.kubernetes.io/version: 1.3.0 component: controller-manager control-plane: controller-manager helm.sh/chart: vault-secrets-operator-1.3.0 name: default namespace: vault-secrets-operator-system resourceVersion: "346826276" uid: 83a89b16-c36e-4e60-8094-75bf07dfaca6 spec: address: [https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/](https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/) skipTLSVerify: false status: conditions: - lastTransitionTime: "2026-03-04T09:42:35Z" message: Vault ping, address= [https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/](https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/) observedGeneration: 1 reason: Accepted status: "True" type: VaultPing - lastTransitionTime: "2026-03-04T09:42:35Z" message: Successfully validated resource, address= [https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/](https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/) observedGeneration: 1 reason: Accepted status: "True" type: ResourceValidation - lastTransitionTime: "2026-03-04T09:42:35Z" message: VaultConnectionHealthy observedGeneration: 1 reason: Healthy status: "True" type: Healthy - lastTransitionTime: "2026-03-04T09:42:35Z" message: VaultConnectionReady observedGeneration: 1 reason: Ready status: "True" type: Ready valid: true

---

There's the mismatch:

| Component | Vault Namespace |
| --- | --- |
| VaultAuth `default` in argocd | `admin/deployments/staging` |
| VDS `argocd-pull` | `admin/central` |

VSO authenticates to `admin/deployments/staging` via approle, gets a token scoped to that namespace, then tries to use it against `admin/central` (where the Azure secrets engine lives). VSO can't clone the client across Vault namespaces, so it fails with the cache key error.

Despite the error, VSO still _attempts_ the credential generation (which is why creds appear) but can't properly track the lease for renewal or revocation. So every reconciliation loop creates a new client secret on the SP without revoking the previous one. That's your 631 credentials.

The fix—create a dedicated VaultAuth for the `admin/central` namespace:

Then update the VDS to reference it:

But first—you need an approle in the `admin/central` Vault namespace. Check if one exists:

And check what roles exist in staging for comparison:

This will tell us whether you need to create a new approle or if there's one already available in `admin/central`. The same pattern will apply to the production cluster—the `argocd-pull` VDS on `lca-prd-2` likely has the identical mismatch.

---

how do we check what has creaet a lease

---

From the Vault side, you can inspect individual leases:

Use the lease ID from your earlier `vault read` output. This shows who created it—the accessor, entity ID, and creation time.

To see all active leases under the path:

If that's permission-denied on HCP, try from the Kubernetes side instead—check which VDS resources have active leases:

This shows every VDS, its current lease ID, and when it was last renewed. Any VDS with a lease against `azure/creds/acr-pull` is creating credentials on that SP.

To see the full picture of _how many_ leases each entity has created, if you have HCP admin access:

On this staging cluster there's only the one VDS (`argocd-pull`), but on `lca-prd-2` you had 9. Each one is independently creating leases and accumulating SP credentials because the namespace mismatch prevents proper lifecycle management.

---

here is across all cluster sending to grafana. Do you see any patterns

---

Claude's response could not be fully generated

---

Let me check where we left off in the transcript.
