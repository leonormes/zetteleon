---
captured: "2026-03-07T16:52:37+00:00 2026-03-07T16:52:37+00:00"
created: 2026-03-07T16:52:39+00:00
modified: 2026-03-14T11:10:44+00:00
source: "https://claude.ai/chat/cdf6fe08-6bfa-403e-9053-fc292d78b2d4"
status: "processing"
tags: ["input"]
title: HEAD Debugging ArgoCD application sync and pod errors
type: "head"
---

## Raw Output / Content

help me debug a config error causing this kubectl get applications -n argocd NAME SYNC STATUS HEALTH STATUS argo-workflows Synced Healthy blob-csi-driver Synced Healthy cert-manager Synced Healthy ff-lca-prd-2 OutOfSync Degraded ff-lca-prd-2-minio Synced Healthy ff-lca-prd-2-mongodb-b17ef Synced Healthy ff-lca-prd-2-postgresql Synced Healthy ff-lca-prd-2-workflow-templates Synced Healthy grafana-k8s-monitoring Synced Healthy prometheus-operator-crds Synced Healthy spicedb Synced Degraded ➜ terraform kubectl delete pod -l app=spicedb -n spicedb pod "spicedb-55b56bb9b4-tjcxh" deleted from spicedb namespace ➜ terraform kubectl get pods -n spicedb NAME READY STATUS RESTARTS AGE spicedb-55b56bb9b4-sbx4m 0/1 Error 1 (3s ago) 7s spicedb-postgresql-0 1/1 Running 0 40m

---

Right, two issues showing here—let's triage them separately. The SpiceDB pod crash is the one you've just poked, so let's start there since you've got momentum.

## SpiceDB—Pod In Error State

The pod restarted and immediately errored again, so this isn't a transient blip. Most common culprits for SpiceDB:

1. Can't connect to its PostgreSQL backend (connection string, credentials, or network policy)
2. Schema migration failure (datastore migration not run or version mismatch)
3. Bad secret / missing env var (especially if Vault Secrets Operator recently rotated or failed to sync a credential)

Given your recent VSO auth chain issues on this exact cluster, credential sync is high on my suspicion list.

### Immediate next action—grab the Pod Logs

(`--previous` because the container already errored once, so the current instance may not have useful output yet. If it errors again quickly, drop `--previous`.)

Then also check whether the secret SpiceDB mounts actually has data:

Paste what comes back and we'll pinpoint the root cause before touching anything else.

---

## ff-lca-prd-2—OutOfSync + Degraded

We'll tackle this second. Once you've grabbed the SpiceDB logs, I'll walk you through pulling the ArgoCD diff for that app to see exactly what's drifted. One thing at a time.

---

kubectl get secret -n spicedb | grep spicedb spicedb Opaque 5 47m ➜ terraform kubectl get secret spicedb -n spicedb -o jsonpath='{.data}' | jq 'keys' \["\_raw", "datastore-connection-uri", "postgres-password", "postgres-username", "preshared-key" \] In vault the secrets are === spicedb === \["postgresql\_password", "postgresql\_username", "spicedb\_preshared\_key" \]

---

Got it. The error is unambiguous:

> `"a preshared key must be provided to authenticate API requests"`

The secret exists and has a `preshared-key` key—so either the value is empty/blank, or the Deployment is referencing the wrong key name when mounting it as an env var or argument.

## Step 1—Check if the Value is Actually Populated

If that returns `0`, the VSO synced the key name but the value is empty—meaning the Vault → K8s mapping is broken.

## Step 2—Check what the Pod Actually Consumes

While that runs, also grab how the Deployment references the secret:

We need to confirm the env var or CLI flag name matches the secret key exactly. SpiceDB expects `--grpc-preshared-key` as a flag or `SPICEDB_GRPC_PRESHARED_KEY` as an env var—if the Deployment references a key name that doesn't match `preshared-key` in the secret, it'll silently get nothing.

## What I Suspect

The Vault field is `spicedb_preshared_key`. The K8s secret key is `preshared-key`. That mapping happens in your `VaultStaticSecret` (or `VaultDynamicSecret`) CR. If the transformation template has a mismatch, or if the VSO credential chain we fixed previously is still partially broken for this specific secret, the value lands empty.

Paste both outputs and we'll know exactly which of these it is.

---

kubectl get deployment spicedb -n spicedb -o yaml | grep -A5 -i preshared {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"spicedb:apps/Deployment:spicedb/spicedb"},"labels":{"app.kubernetes.io/name":"spicedb"},"name":"spicedb","namespace":"spicedb"},"spec":{"progressDeadlineSeconds":600,"replicas":1,"selector":{"matchLabels":{"app":"spicedb"}},"strategy":{"rollingUpdate":{"maxSurge":"25%","maxUnavailable":"25%"},"type":"RollingUpdate"},"template":{"metadata":{"annotations":{},"labels":{"app":"spicedb"}},"spec":{"containers":\[{"args":\["if \[-f /secrets/spicedb \]; then\\n source /secrets/spicedb;\\nelse\\n echo \\"No secrets file to source\\";\\nfi;\\nspicedb serve;\\n"\],"command":\["sh","-c"\],"env":\[{"name":"SPICEDB\_DATASTORE\_CONN\_URI","valueFrom":{"secretKeyRef":{"key":"datastore-connection-uri","name":"spicedb"}}},{"name":"SPICEDB\_GRPC\_PRESHARED\_KEY","valueFrom":{"secretKeyRef":{"key":"preshared-key","name":"spicedb"}}},{"name":"SPICEDB\_DATASTORE\_ENGINE","value":"postgres"},{"name":"SPICEDB\_LOG\_LEVEL","value":"debug"},{"name":"SPICEDB\_HTTP\_ENABLED","value":"true"},{"name":"SPICEDB\_GRPC\_SHUTDOWN\_GRACE\_PERIOD","value":"1s"}\],"image":"fitfileregistry.azurecr.io/authzed/spicedb:v1.34.0-debug","imagePullPolicy":"Always","name":"spicedb","ports":\[{"containerPort":50051,"name":"grpc","protocol":"TCP"},{"containerPort":8443,"name":"http","protocol":"TCP"},{"containerPort":50053,"name":"dispatch","protocol":"TCP"},{"containerPort":9090,"name":"prometheus","protocol":"TCP"}\],"readinessProbe":{"exec":{"command":\["grpc\_health\_probe","-v","-addr=localhost:50051"\]},"failureThreshold":5,"periodSeconds":10,"successThreshold":1,"timeoutSeconds":5},"resources":{"requests":{"cpu":"100m","memory":"256Mi"}}}\],"dnsPolicy":"ClusterFirst","imagePullSecrets":\[{"name":"fitfile-image-pull-secret"}\],"initContainers":\[{"args":\["if \[-f /secrets/spicedb \]; then\\n cat /secrets/spicedb;\\n source /secrets/spicedb;\\nelse\\n echo \\"No secrets file to source\\";\\nfi;\\nspicedb migrate head \\\\\\n --datastore-engine $SPICEDB\_DATASTORE\_ENGINE \\\\\\n --datastore-conn-uri $SPICEDB\_DATASTORE\_CONN\_URI;\\n"\],"command":\["sh","-c"\],"env":\[{"name":"SPICEDB\_DATASTORE\_CONN\_URI","valueFrom":{"secretKeyRef":{"key":"datastore-connection-uri","name":"spicedb"}}},{"name":"SPICEDB\_GRPC\_PRESHARED\_KEY","valueFrom":{"secretKeyRef":{"key":"preshared-key","name":"spicedb"}}},{"name":"SPICEDB\_DATASTORE\_ENGINE","value":"postgres"},{"name":"SPICEDB\_LOG\_LEVEL","value":"debug"}\],"image":"fitfileregistry.azurecr.io/authzed/spicedb:v1.34.0-debug","name":"spicedb-init"}\],"restartPolicy":"Always","serviceAccountName":"spicedb","terminationGracePeriodSeconds":30}}}} creationTimestamp: "2026-03-03T13:41:33Z" generation: 1 labels: app.kubernetes.io/name: spicedb name: spicedb -- - name: SPICEDB\_GRPC\_PRESHARED\_KEY valueFrom: secretKeyRef: key: preshared-key name: spicedb - name: SPICEDB\_DATASTORE\_ENGINE value: postgres - name: SPICEDB\_LOG\_LEVEL value: debug -- - name: SPICEDB\_GRPC\_PRESHARED\_KEY valueFrom: secretKeyRef: key: preshared-key name: spicedb - name: SPICEDB\_DATASTORE\_ENGINE value: postgres - name: SPICEDB\_LOG\_LEVEL value: debug

---

Good—the wiring is correct. The Deployment reads `preshared-key` from the `spicedb` secret into `SPICEDB_GRPC_PRESHARED_KEY`. No naming mismatch.

That leaves one suspect: the value itself is empty. Did you run the Step 1 check?

If it returns `0`, the VSO synced the key but not the value. At that point we need to look at the `VaultStaticSecret` CR to check the field mapping between Vault's `spicedb_preshared_key` and the K8s secret's `preshared-key`.

---

---

Confirmed—the key exists but the value is empty. The VSO created the secret structure but didn't populate that field. Let's find out why.

## Next action—inspect the VaultStaticSecret CR

We're looking for two things:

1. The `destination.transformation` or `spec.destination.create` mapping—does it correctly map Vault's `spicedb_preshared_key` → K8s `preshared-key`?
2. The `status` block—any error conditions from VSO's last reconciliation attempt (auth failures, field-not-found, etc.)

If your setup uses a template/transformation block, a common gotcha is that Vault field names with underscores (`spicedb_preshared_key`) need to match exactly what the template references—a typo or case difference silently produces an empty value rather than an error.

---

It has a previous misspelled version kubectl get vaultstaticsecret -n spicedb -o yaml apiVersion: v1 items: - apiVersion: secrets.hashicorp.com/v1beta1 kind: VaultStaticSecret metadata: annotations: argocd.argoproj.io/tracking-id: spicedb:secrets.hashicorp.com/VaultStaticSecret:spicedb/spicedb kubectl.kubernetes.io/last-applied-configuration: | {"apiVersion":"secrets.hashicorp.com/v1beta1","kind":"VaultStaticSecret","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"spicedb:secrets.hashicorp.com/VaultStaticSecret:spicedb/spicedb"},"name":"spicedb","namespace":"spicedb"},"spec":{"destination":{"create":true,"name":"spicedb","transformation":{"excludes":\[".\*"\],"templates":{"datastore-connection-uri":{"text":"postgres://{{ get.Secrets \\"postgresql\_username\\" }}:{{ get.Secrets \\"postgresql\_password\\" }}@spicedb-postgresql:5432/spicedb?sslmode=prefer"},"postgres-password":{"text":"{{ get.Secrets \\"postgresql\_password\\" }}"},"postgres-username":{"text":"{{ get.Secrets \\"postgresql\_username\\" }}"},"preshared-key":{"text":"{{ get.Secrets \\"spicedb\_pre\_shared\_key\\" }}"}}}},"hmacSecretData":true,"mount":"secrets","namespace":"admin/deployments/lca-prd-2","path":"spicedb","refreshAfter":null,"rolloutRestartTargets":\[\],"type":"kv-v2","vaultAuthRef":"default"}} creationTimestamp: "2026-03-03T13:41:33Z" finalizers: - vaultstaticsecret.secrets.hashicorp.com/finalizer generation: 5 name: spicedb namespace: spicedb resourceVersion: "8099394" uid: 67f01866-7360-4ed3-aad5-c95dea548303 spec: destination: create: true name: spicedb overwrite: false transformation: excludes: -.\* templates: datastore-connection-uri: text: postgres://{{ get.Secrets "postgresql\_username" }}:{{ get.Secrets "postgresql\_password" }}@spicedb-postgresql:5432/spicedb?sslmode=prefer postgres-password: text: '{{ get.Secrets "postgresql\_password" }}' postgres-username: text: '{{ get.Secrets "postgresql\_username" }}' preshared-key: text: '{{ get.Secrets "spicedb\_pre\_shared\_key" }}' hmacSecretData: true mount: secrets namespace: admin/deployments/lca-prd-2 path: spicedb rolloutRestartTargets: \[\] type: kv-v2 vaultAuthRef: default status: lastGeneration: 5 secretMAC: txIpY9STfVHpSP08E9t072AYatGWwopqZjHHXYiCSWo= kind: List metadata: resourceVersion: "" See text: '{{ get.Secrets "spicedb\_pre\_shared\_key" }}' has pre\_share rather than preshared. I changed that in the values file that argocd is reading

---

Spot on. The template references `spicedb_pre_shared_key` but Vault has `spicedb_preshared_key`. The `get.Secrets` call silently returns an empty string on a miss—no error, just nothing. Classic.

You've fixed the values file, so now you need ArgoCD to push that change through. Since `ff-lca-prd-2` is already showing OutOfSync, ArgoCD may have already detected the diff.

## Next action—sync the SpiceDB App

If you don't have the ArgoCD CLI handy, you can do it via kubectl:

Then watch it come back:

Once the `VaultStaticSecret` is updated, VSO will re-reconcile, populate the `preshared-key` value, and the next pod restart should pick it up. If the pod doesn't automatically restart after the secret updates, check whether `rolloutRestartTargets` is empty (it is—we saw `[]`). That means VSO won't auto-restart the Deployment when the secret changes. In that case, you'll need to bounce it manually:

Let me know once the sync lands and we'll verify the value is populated, then move on to the `ff-lca-prd-2` OutOfSync/Degraded issue.

---

kubectl patch application spicedb -n argocd --type merge -p '{"operation":{"initiatedBy":{"username":"leon"},"sync":{"force":true}}}' Warning: unknown field "operation.sync.force" application.argoproj.io/spicedb patched

---

That warning suggests the patch was accepted but the `force` field may not have triggered a proper sync. Let's verify—check if ArgoCD actually started an operation:

If it doesn't show `Running` or `Succeeded`, the sync didn't fire. In that case, the most reliable route without the ArgoCD CLI is:

Or if that's also fiddly, just use the ArgoCD UI to hit Sync on the spicedb app—no shame in clicking a button when the kubectl patching gets awkward.

Once the sync has actually landed, the verification chain is:

1. Confirm the VaultStaticSecret template updated:

Should now show `{{ get.Secrets "spicedb_preshared_key" }}`

1. Confirm the secret value is populated:

Should be > 0

1. Bounce the pods (since `rolloutRestartTargets` is empty):
2. Watch it come healthy:

Let me know where you get to.

---

kubectl rollout restart deployment/spicedb -n spicedb deployment.apps/spicedb restarted ➜ terraform kubectl get pods -n spicedb -w NAME READY STATUS RESTARTS AGE spicedb-55b56bb9b4-sbx4m 0/1 CrashLoopBackOff 6 (37s ago) 6m42s spicedb-7cf8bf8bb-fqk8m 0/1 Error 0 5s spicedb-postgresql-0 1/1 Running 0 46m spicedb-7cf8bf8bb-fqk8m 0/1 Error 1 (2s ago) 6s spicedb-7cf8bf8bb-fqk8m 0/1 CrashLoopBackOff 1 (6s ago) 11s ^C% ➜ terraform kubectl get application spicedb -n argocd -o jsonpath='{.status.operationState.phase}' Succeeded% ➜ terraform kubectl get vaultstaticsecret spicedb -n spicedb -o jsonpath='{.spec.destination.transformation.templates.preshared-key.text}' {{ get.Secrets "spicedb\_pre\_shared\_key" }}%

---

The sync succeeded but the template still has the old typo—`spicedb_pre_shared_key`. Your values file change hasn't made it through yet. Most likely cause:

1. The change isn't committed and pushed—ArgoCD synced HEAD but your fix isn't in the repo yet
2. ArgoCD is pointing at a different branch or path than where you made the edit

## Immediate check—is Your Fix Committed?

If the file is still uncommitted or unpushed, that's the whole story—ArgoCD faithfully synced the old version.

If it is pushed, then check which revision ArgoCD actually synced:

Compare that commit hash against your fix commit. If they don't match, ArgoCD may be targeting a different branch or hasn't picked up the latest yet.

---

here is the file copied from gitlab

---

The values file in Git is already correct—`spicedb_preshared_key` under the `spicedb:` section. So the fix is committed. The problem is you synced the wrong ArgoCD app.

This is an app-of-apps pattern. The `spicedb` ArgoCD application is a child app whose manifest (including the VaultStaticSecret) is rendered by the parent `ff-lca-prd-2` application using these values. Syncing the `spicedb` child just re-applies whatever the parent last generated.

## You Need to Sync the Parent

Or hit Sync on `ff-lca-prd-2` in the ArgoCD UI—that one's already showing OutOfSync, which is likely _because_ of this very fix sitting in Git waiting to be applied.

Once that syncs, verify the chain:

This should also clear the `ff-lca-prd-2` OutOfSync/Degraded status, since the drift was likely caused by this pending change.

---

Althought that is commit 924d644267ea70839a067d2260e69768980e1e7f kubectl get application spicedb -n argocd -o jsonpath='{.status.sync.revision}' 24fcdf3163575ab5a2c89fff1d09a1ac97969983%

---

Exactly—ArgoCD is still rendering from an older commit. The fix exists in Git but the parent app hasn't synced it through yet. Sync the parent:

Then confirm the child picked up the new commit:

Should now show `924d644…`. Once it does, run the verification chain from before.

---

kubectl patch application ff-lca-prd-2 -n argocd --type merge -p '{"operation":{"initiatedBy":{"username":"leon"},"sync":{"revision":"HEAD"}}}' application.argoproj.io/ff-lca-prd-2 patched ➜ terraform kubectl get application spicedb -n argocd -o jsonpath='{.status.sync.revision}' 24fcdf3163575ab5a2c89fff1d09a1ac97969983%

---

Hasn't picked it up yet. Check if the parent sync actually fired:

If it shows `Succeeded` but the revision hasn't changed, the patch may have been a no-op (ArgoCD can be finicky with operation patches). If it shows `Running`, just give it a moment and re-check.

If it's not running, the most reliable fallback—hit Sync on `ff-lca-prd-2` in the ArgoCD UI. The kubectl patch approach for triggering syncs is honestly unreliable without the ArgoCD CLI. No point wrestling with it when the button is right there.

---

kubectl get application spicedb -n argocd -o jsonpath='{.status.sync.revision}' 24fcdf3163575ab5a2c89fff1d09a1ac97969983% ➜ terraform kubectl patch application ff-lca-prd-2 -n argocd --type merge -p '{"operation":{"initiatedBy":{"username":"leon"},"sync":{"revision":"HEAD"}}}' application.argoproj.io/ff-lca-prd-2 patched ➜ terraform kubectl get application spicedb -n argocd -o jsonpath='{.status.sync.revision}' 24fcdf3163575ab5a2c89fff1d09a1ac97969983% ➜ terraform kubectl get application ff-lca-prd-2 -n argocd -o jsonpath='{.status.operationState.phase}' Running% ➜ terraform kubectl get application ff-lca-prd-2 -n argocd -o jsonpath='{.status.operationState.phase}' Running%

---

Good—it's actually running this time. The parent app has a lot of child apps to reconcile so give it a minute. Poll it:

Once the parent phase flips to `Succeeded`, check if the spicedb revision changed to `924d644…`. If it has, run the verification chain:

---

it is stuck running. It is taking a long time

---

Let's see what's blocking it:

And check if any child apps are stuck:

If nothing obvious there, check the sync operation details:

Paste what comes back—it'll tell us whether it's waiting on a hook, stuck on a health check (likely the already-crashlooping SpiceDB pod), or something else entirely.

---

outputs

---

Good news in there—the spicedb Application was `configured` (not `unchanged`), and the revision `924d644…` is in the sync result. The change has been pushed through. The parent is just stuck waiting for SpiceDB to report Healthy, which it can't do while the pod is crashlooping.

Let's check if the fix actually landed:

If that now shows `spicedb_preshared_key` (not `spicedb_pre_shared_key`), then check the secret value:

If > 0, bounce the pods:

Once SpiceDB comes up healthy, the parent sync will unblock itself and complete automatically.

---

kubectl get vaultstaticsecret spicedb -n spicedb -o jsonpath='{.spec.destination.transformation.templates.preshared-key.text}' {{ get.Secrets "spicedb\_preshared\_key" }}% ➜ terraform kubectl get secret spicedb -n spicedb -o jsonpath='{.data.preshared-key}' | base64 -d | wc -c 32 ➜ terraform kubectl rollout restart deployment/spicedb -n spicedb deployment.apps/spicedb restarted

---

Template fixed, secret populated with 32 bytes. Now watch it come up:

Once you see `1/1 Running`, the parent sync should unblock and complete on its own. Check with:

Both `spicedb` and `ff-lca-prd-2` should flip to Healthy.

---

kubectl get pods -n spicedb -w NAME READY STATUS RESTARTS AGE spicedb-7cf8bf8bb-fqk8m 1/1 Terminating 5 (5m47s ago) 7m18s spicedb-dc5f4cd8b-f42j8 1/1 Running 0 27s spicedb-postgresql-0 1/1 Running 0 54m ^C% ➜ terraform kubectl get applications -n argocd NAME SYNC STATUS HEALTH STATUS argo-workflows Synced Healthy blob-csi-driver Synced Healthy cert-manager Synced Healthy ff-lca-prd-2 OutOfSync Progressing ff-lca-prd-2-minio Synced Healthy ff-lca-prd-2-mongodb-b17ef Synced Healthy ff-lca-prd-2-postgresql Synced Healthy ff-lca-prd-2-workflow-templates Synced Healthy grafana-k8s-monitoring Synced Healthy prometheus-operator-crds Synced Healthy spicedb OutOfSync Healthy ➜ terraform

---

SpiceDB is Healthy—that's the big win. The parent is `Progressing` which means it's still finishing the sync wave. Give it a minute and re-check:

If `spicedb` stays `OutOfSync` after the parent completes, it just needs its own sync now that its spec was updated:

Once everything settles, you should see both `ff-lca-prd-2` and `spicedb` as Synced/Healthy.

Recap of what happened: The VaultStaticSecret template had `spicedb_pre_shared_key` (typo) instead of `spicedb_preshared_key` (the actual Vault field). VSO silently returned an empty string, SpiceDB got no preshared key, and crashed. The fix was in Git but needed the parent app synced to propagate to the child.

---

kubectl patch application spicedb -n argocd --type merge -p '{"operation":{"initiatedBy":{"username":"leon"},"sync":{"revision":"HEAD"}}}' application.argoproj.io/spicedb patched ➜ terraform kubectl get applications -n argocd NAME SYNC STATUS HEALTH STATUS argo-workflows Synced Healthy blob-csi-driver Synced Healthy cert-manager Synced Healthy ff-lca-prd-2 OutOfSync Progressing ff-lca-prd-2-minio Synced Healthy ff-lca-prd-2-mongodb-b17ef Synced Healthy ff-lca-prd-2-postgresql Synced Healthy ff-lca-prd-2-workflow-templates Synced Healthy grafana-k8s-monitoring Synced Healthy prometheus-operator-crds Synced Healthy spicedb OutOfSync Healthy ➜ terraform kubectl get applications -n argocd NAME SYNC STATUS HEALTH STATUS argo-workflows Synced Healthy blob-csi-driver Synced Healthy cert-manager Synced Healthy ff-lca-prd-2 OutOfSync Progressing ff-lca-prd-2-minio Synced Healthy ff-lca-prd-2-mongodb-b17ef Synced Healthy ff-lca-prd-2-postgresql Synced Healthy ff-lca-prd-2-workflow-templates Synced Healthy grafana-k8s-monitoring Synced Healthy prometheus-operator-crds Synced Healthy spicedb OutOfSync Healthy

---

Still stuck. Let's see what's keeping both OutOfSync:

And check what spicedb thinks is out of sync:

The parent might still be waiting on remaining child apps to deploy (the values file has `fitconnect`, `ffcloud`, `frontend` etc. enabled). Check if any new apps appeared or if anything else is unhealthy:

---

kubectl get application ff-lca-prd-2 -n argocd -o jsonpath='{.status.operationState.message}' waiting for healthy state of argoproj.io/Application/spicedb% ➜ terraform kubectl get application spicedb -n argocd -o jsonpath='{.status.conditions}' | jq. ➜ terraform kubectl get applications -n argocd --sort-by='.metadata.name' NAME SYNC STATUS HEALTH STATUS argo-workflows Synced Healthy blob-csi-driver Synced Healthy cert-manager Synced Healthy ff-lca-prd-2 OutOfSync Progressing ff-lca-prd-2-minio Synced Healthy ff-lca-prd-2-mongodb-b17ef Synced Healthy ff-lca-prd-2-postgresql Synced Healthy ff-lca-prd-2-workflow-templates Synced Healthy grafana-k8s-monitoring Synced Healthy prometheus-operator-crds Synced Healthy spicedb OutOfSync Healthy

---

The parent sees spicedb as not fully reconciled because it's still `OutOfSync`—even though it's Healthy. Let's see what spicedb thinks is drifting:

This will show which specific resources within the spicedb app are out of sync. Likely the VaultStaticSecret or Deployment still has a diff from the old sync vs the new spec.

---

kubectl get application spicedb -n argocd -o jsonpath='{.status.resources}' | jq '.\[\] | select(.status!= "Synced")' { "group": "apps", "kind": "Deployment", "name": "spicedb", "namespace": "spicedb", "status": "OutOfSync", "version": "v1" }

---

The Deployment is drifting—most likely because `kubectl rollout restart` added a `restartedAt` annotation that doesn't exist in the Git-defined spec. Let's confirm:

To clear this, sync spicedb with force to overwrite the live state:

Or honestly—just use the ArgoCD UI, click Sync on `spicedb`, tick "Replace" or "Force". The kubectl patching for sync operations has been fighting us all session.

Once spicedb flips to `Synced`, the parent should unblock and complete.

---

kubectl get application spicedb -n argocd -o jsonpath='{.status.operationState.syncResult.resources}' | jq '.\[\] | select(.kind == "Deployment")' { "group": "apps", "hookPhase": "Running", "images": \["fitfileregistry.azurecr.io/authzed/spicedb:v1.34.0-debug" \], "kind": "Deployment", "message": "deployment.apps/spicedb unchanged", "name": "spicedb", "namespace": "spicedb", "status": "Synced", "syncPhase": "Sync", "version": "v1" } ➜ terraform kubectl patch application spicedb -n argocd --type merge -p '{"operation":{"initiatedBy":{"username":"leon"},"sync":{"syncStrategy":{"apply":{"force":true}}}}}' application.argoproj.io/spicedb patched

---

Check if that kicked off:

And then watch both:

If it's still stuck after a minute, the ArgoCD UI is the path of least resistance here—click Sync on `spicedb`, enable "Force", and let it reconcile. We've burned enough time wrestling with kubectl patches for ArgoCD operations.

---

kubectl get application spicedb -n argocd -o jsonpath='{.status.operationState.syncResult.resources}' | jq '.\[\] | select(.kind == "Deployment")' { "group": "apps", "hookPhase": "Running", "images": \["fitfileregistry.azurecr.io/authzed/spicedb:v1.34.0-debug" \], "kind": "Deployment", "message": "deployment.apps/spicedb unchanged", "name": "spicedb", "namespace": "spicedb", "status": "Synced", "syncPhase": "Sync", "version": "v1" } ➜ terraform kubectl patch application spicedb -n argocd --type merge -p '{"operation":{"initiatedBy":{"username":"leon"},"sync":{"syncStrategy":{"apply":{"force":true}}}}}' application.argoproj.io/spicedb patched

---

We're going in circles with the kubectl patches. Let's break the deadlock. The parent started its sync _before_ SpiceDB was healthy, and it's stuck on that old wait. We need to terminate the stuck operation first:

If that doesn't take (ArgoCD can protect operation state), use the UI:

1. Open `ff-lca-prd-2` in ArgoCD UI
2. Click Terminate on the running operation
3. Then Sync `spicedb` with Force enabled
4. Then Sync `ff-lca-prd-2`

The core issue is the parent's sync operation is waiting on a health check that predates our fix. Terminating it and re-syncing cleanly should resolve the whole chain. SpiceDB itself is running and healthy—this is purely an ArgoCD bookkeeping problem now.

---

i don't have access to the Argocd UI

---

Right. Let's try the ArgoCD CLI—it handles sync operations much more reliably than kubectl patches:

If not installed:

Then authenticate (since you're already kubectl-authenticated to the cluster):

Once logged in, terminate the stuck operation and re-sync cleanly:

Alternatively, if you'd rather not install the CLI—we can remove the drift directly. The OutOfSync is caused by the `restartedAt` annotation from `rollout restart`. Remove it:

That should make the live Deployment match Git again, flipping spicedb to `Synced`, which unblocks the parent.

---

kubectl get applications -n argocd NAME SYNC STATUS HEALTH STATUS argo-workflows Synced Healthy blob-csi-driver Synced Healthy cert-manager Synced Healthy ff-lca-prd-2 OutOfSync Progressing ff-lca-prd-2-ffcloud-service Synced Progressing ff-lca-prd-2-fitconnect Synced Progressing ff-lca-prd-2-minio Synced Healthy ff-lca-prd-2-mongodb-b17ef Synced Healthy ff-lca-prd-2-postgresql Synced Healthy ff-lca-prd-2-workflow-templates Synced Healthy ff-lca-prd-2-workflows-api Synced Healthy grafana-k8s-monitoring Synced Healthy prometheus-operator-crds Synced Healthy spicedb Synced Healthy ➜ terraform kubectl get pods -n ff-lca-prd-2 No resources found in ff-lca-prd-2 namespace. ➜ terraform kubectl get pods -n lca-prd-2 NAME READY STATUS RESTARTS AGE ff-lca-prd-2-ffcloud-service-74948dcd45-9rhtv 0/3 Init:CrashLoopBackOff 2 (23s ago) 60s ff-lca-prd-2-fitconnect-ftc-5cbf7f8ddd-5klzb 0/1 Init:CrashLoopBackOff 2 (17s ago) 60s ff-lca-prd-2-minio-6c9b4586f4-94nfs 1/1 Running 0 128m ff-lca-prd-2-minio-provisioning-ftxtt 0/1 Completed 4 129m ff-lca-prd-2-mongodb-b17ef-0 2/2 Running 7 (140m ago) 149m ff-lca-prd-2-mongodb-b17ef-arbiter-0 1/1 Running 0 133m ff-lca-prd-2-postgresql-0 1/1 Running 0 5h24m workflows-api-6df47dfd8f-5hl4p 1/1 Running 0 75s

---

SpiceDB is done—Synced and Healthy. The parent sync unblocked and has now deployed the remaining apps. Two pods are crashlooping in init containers. Let's see what's failing:

And for ffcloud:

Given the pattern we just fixed, I'd wager these are also VSO-related—empty secret values for MongoDB or Auth0 credentials. Let's see the logs first.

---

kubectl logs ff-lca-prd-2-fitconnect-ftc-5cbf7f8ddd-5klzb -n lca-prd-2 --init-containers --previous 2>/dev/null || kubectl logs ff-lca-prd-2-fitconnect-ftc-5cbf7f8ddd-5klzb -n lca-prd-2 -c $(kubectl get pod ff-lca-prd-2-fitconnect-ftc-5cbf7f8ddd-5klzb -n lca-prd-2 -o jsonpath='{.spec.initContainers\[0\].name}') yarn run v1.22.22 $ yarn node db-migrations/nosql/migration-runner.js up /app/node\_modules/@fitfile/service-common/dist/config/loader.js:48 throw result.error; ^ ServiceError: Unable to parse json config file (/secrets/postgresql.json) at readConfig (/app/node\_modules/@fitfile/service-common/dist/config/loader.js:22:15) at loadConfig (/app/node\_modules/@fitfile/service-common/dist/config/loader.js:30:24)… 12 lines matching cause stack trace… at Object.<anonymous> (/app/config/index.js:17:14) at Module.\_compile (node:internal/modules/cjs/loader:1562:14) { status: 500, originalError: SyntaxError: Expected ',' or '}' after property value in JSON at position 30 (line 1 column 31) at JSON.parse (<anonymous>) at readConfig (/app/node\_modules/@fitfile/service-common/dist/config/loader.js:19:21) at loadConfig (/app/node\_modules/@fitfile/service-common/dist/config/loader.js:30:24) at /app/node\_modules/@fitfile/service-common/dist/config/loader.js:45:47 at Array.reduce (<anonymous>) at loadAllConfig (/app/node\_modules/@fitfile/service-common/dist/config/loader.js:40:37) at Object.<anonymous> (/app/config/config-loader.js:68:53) at Module.\_compile (node:internal/modules/cjs/loader:1562:14) at Object..js (node:internal/modules/cjs/loader:1699:10) at Module.load (node:internal/modules/cjs/loader:1313:32) at Function.\_load (node:internal/modules/cjs/loader:1123:12) at TracingChannel.traceSync (node:diagnostics\_channel:322:14) at wrapModuleLoad (node:internal/modules/cjs/loader:217:24) at Module.require (node:internal/modules/cjs/loader:1335:12) at require (node:internal/modules/helpers:136:16) at Object.<anonymous> (/app/config/index.js:17:14), \[cause\]: SyntaxError: Expected ',' or '}' after property value in JSON at position 30 (line 1 column 31) at JSON.parse (<anonymous>) at readConfig (/app/node\_modules/@fitfile/service-common/dist/config/loader.js:19:21) at loadConfig (/app/node\_modules/@fitfile/service-common/dist/config/loader.js:30:24) at /app/node\_modules/@fitfile/service-common/dist/config/loader.js:45:47 at Array.reduce (<anonymous>) at loadAllConfig (/app/node\_modules/@fitfile/service-common/dist/config/loader.js:40:37) at Object.<anonymous> (/app/config/config-loader.js:68:53) at Module.\_compile (node:internal/modules/cjs/loader:1562:14) at Object..js (node:internal/modules/cjs/loader:1699:10) at Module.load (node:internal/modules/cjs/loader:1313:32) at Function.\_load (node:internal/modules/cjs/loader:1123:12) at TracingChannel.traceSync (node:diagnostics\_channel:322:14) at wrapModuleLoad (node:internal/modules/cjs/loader:217:24) at Module.require (node:internal/modules/cjs/loader:1335:12) at require (node:internal/modules/helpers:136:16) at Object.<anonymous> (/app/config/index.js:17:14) } Node.js v22.13.1 error Command failed. Exit code: 1 Command: /usr/local/bin/node Arguments: db-migrations/nosql/migration-runner.js up Directory: /app Output: info Visit [https://yarnpkg.com/en/docs/cli/node](https://yarnpkg.com/en/docs/cli/node) for documentation about this command. error Command failed with exit code 1. info Visit [https://yarnpkg.com/en/docs/cli/run](https://yarnpkg.com/en/docs/cli/run) for documentation about this command.

---

JSON parse error in `postgresql.json` at position 30 (column 31). The PostgreSQL password almost certainly contains a character that breaks JSON—like a `"`, `\`, or `}`.

Let's see the actual rendered value:

If the password contains an unescaped `"` or `\`, the rendered JSON breaks. This is a known pain point with VSO templates—there's no built-in JSON escaping function.

---

kubectl get secret fitconnect -n lca-prd-2 -o jsonpath='{.data.postgresql\\.json}' | base64 -d {"password":"{{ get.Secrets "postgresql\_password" }}","username":"{{ get.Secrets "postgresql\_username" }}"}%

---

The template hasn't been rendered—that's the raw Go template string sitting in the secret, not actual credentials. VSO received the template but couldn't substitute the values from Vault. Either VSO hasn't reconciled it yet, or it can't authenticate/fetch from Vault for this secret.

Check the VaultStaticSecret status:

Or more broadly—check if any of the lca-prd-2 secrets have the same problem:

And check VSO's ability to reach Vault from this namespace:

This is likely the same auth chain issue affecting all the newly-created VaultStaticSecrets in the `lca-prd-2` namespace—SpiceDB worked because it had its own namespace where VSO was already reconciling. The `lca-prd-2` namespace probably doesn't have a working `VaultAuth` or `VaultConnection` yet.

---

kubectl get vaultstaticsecret -n lca-prd-2 -o yaml | grep -A 20 'name: fitconnect' | grep -A 15 'status:' ➜ terraform kubectl get vaultstaticsecret -n lca-prd-2 NAME AGE ffcloud 3m55s fitconnect 3m55s fitfile-rsa-private-key 124m minio 151m mongodb 151m postgresql 21h s3-export-secret 124m ude-secret 124m workflows-secrets 124m ➜ terraform kubectl get vaultauth -n lca-prd-2 kubectl get vaultconnection -n lca-prd-2 NAME AGE default 7d5h No resources found in lca-prd-2 namespace.

---

No `VaultConnection` in `lca-prd-2`—that's likely the problem. VSO needs both a `VaultAuth` and a `VaultConnection` to reach Vault. Let's confirm by comparing with the spicedb namespace where things work:

And check the VaultAuth in lca-prd-2 to see if it references a connection:

Also check the status of the fitconnect VaultStaticSecret directly:

That status block should tell us exactly what VSO is complaining about—likely something like "VaultConnection not found".

---

kubectl get vaultconnection -n spicedb No resources found in spicedb namespace. ➜ terraform kubectl get vaultauth default -n lca-prd-2 -o yaml apiVersion: secrets.hashicorp.com/v1beta1 kind: VaultAuth metadata: annotations: kubectl.kubernetes.io/last-applied-configuration: | {"apiVersion":"secrets.hashicorp.com/v1beta1","kind":"VaultAuth","metadata":{"name":"default","namespace":"lca-prd-2"},"spec":{"jwt":{"audiences":\[" [https://uksouth.oic.prod-aks.azure.com/dbb3517b-09e6-4a76-9aa9-d7d72b1073e7/102b5853-a8d1-4ced-9d5e-d72787b21dfa/"\],"role":"lca-prd-2","serviceAccount":"default"},"method":"jwt","mount":"jwt-lca-prd-2","namespace":"admin"}}](https://uksouth.oic.prod-aks.azure.com/dbb3517b-09e6-4a76-9aa9-d7d72b1073e7/102b5853-a8d1-4ced-9d5e-d72787b21dfa/%22],%22role%22:%22lca-prd-2%22,%22serviceAccount%22:%22default%22%7D,%22method%22:%22jwt%22,%22mount%22:%22jwt-lca-prd-2%22,%22namespace%22:%22admin%22%7D%7D) creationTimestamp: "2026-02-24T09:56:59Z" finalizers: - vaultauth.secrets.hashicorp.com/finalizer generation: 1 name: default namespace: lca-prd-2 resourceVersion: "3478279" uid: b2c65c17-b57b-4086-b753-a4756987071b spec: jwt: audiences: - [https://uksouth.oic.prod-aks.azure.com/dbb3517b-09e6-4a76-9aa9-d7d72b1073e7/102b5853-a8d1-4ced-9d5e-d72787b21dfa/](https://uksouth.oic.prod-aks.azure.com/dbb3517b-09e6-4a76-9aa9-d7d72b1073e7/102b5853-a8d1-4ced-9d5e-d72787b21dfa/) role: lca-prd-2 serviceAccount: default tokenExpirationSeconds: 600 method: jwt mount: jwt-lca-prd-2 namespace: admin status: specHash: 65952ddbbe4f683d18d1befde91c1237a9f8973fd9488d1f4b230e682cc4ab37 valid: true ➜ terraform kubectl get vaultstaticsecret fitconnect -n lca-prd-2 -o jsonpath='{.status}' | jq. { "lastGeneration": 1, "secretMAC": "cYfoppPq0FSkmXC5oSd3PmIj4gUpSMc3xdphuVc7eTk=" }

---

Interesting—VaultAuth is valid, no VaultConnection in either namespace (so both use the operator's default), and VSO reports no errors on fitconnect. Yet the secret has raw template strings. Let's see the full fitconnect VaultStaticSecret spec:

Something is off with how the transformation templates are being applied—VSO thinks it reconciled successfully (it has a `secretMAC`) but didn't evaluate the Go templates. I want to see whether the `transformation` vs `secretTransformation` field is set correctly in the rendered CR.

---

kubectl get vaultstaticsecret fitconnect -n lca-prd-2 -o yaml apiVersion: secrets.hashicorp.com/v1beta1 kind: VaultStaticSecret metadata: annotations: argocd.argoproj.io/tracking-id: ff-lca-prd-2-fitconnect:secrets.hashicorp.com/VaultStaticSecret:lca-prd-2/fitconnect kubectl.kubernetes.io/last-applied-configuration: | {"apiVersion":"secrets.hashicorp.com/v1beta1","kind":"VaultStaticSecret","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"ff-lca-prd-2-fitconnect:secrets.hashicorp.com/VaultStaticSecret:lca-prd-2/fitconnect"},"name":"fitconnect","namespace":"lca-prd-2"},"spec":{"destination":{"create":true,"name":"fitconnect","transformation":{"excludes":\[".\*"\],"templates":{"auth.json":{"text":"{\\"clientId\\":\\"{{ \\"{{\\" }} get.Secrets \\"auth0\_client\_id\\" {{ \\"}}\\" }}\\",\\"clientSecret\\":\\"{{ \\"{{\\" }} get.Secrets \\"auth0\_client\_secret\\" {{ \\"}}\\" }}\\", \\"audience\\": \\"{{ \\"{{\\" }} get.Secrets \\"auth0\_audience\\" {{ \\"}}\\" }}\\"}"},"mongodb":{"text":"mongodb://{{ \\"{{\\" }} get.Secrets \\"mongodb\_username\\" {{ \\"}}\\" }}:{{ \\"{{\\" }} get.Secrets \\"mongodb\_password\\" {{ \\"}}\\" }}@ff-lca-prd-2-mongodb-b17ef-0.ff-lca-prd-2-mongodb-b17ef-headless.lca-prd-2.svc.cluster.local:27017/admin?replicaSet=rs0"},"postgresql.json":{"text":"{\\"password\\":\\"{{ \\"{{\\" }} get.Secrets \\"postgresql\_password\\" {{ \\"}}\\" }}\\",\\"username\\":\\"{{ \\"{{\\" }} get.Secrets \\"postgresql\_username\\" {{ \\"}}\\" }}\\"}"},"s3-access-key":{"text":"{{ \\"{{\\" }} get.Secrets \\"s3\_access\_key\_id\\" {{ \\"}}\\" }}"},"s3-secret-key":{"text":"{{ \\"{{\\" }} get.Secrets \\"s3\_secret\_access\_key\\" {{ \\"}}\\" }}"},"spicedb.json":{"text":"{\\"preSharedKey\\":\\"{{ \\"{{\\" }} get.Secrets \\"spicedb\_preshared\_key\\" {{ \\"}}\\" }}\\"}"}}}},"hmacSecretData":true,"mount":"secrets","namespace":"admin/deployments/lca-prd-2","path":"application","refreshAfter":"5m","rolloutRestartTargets":\[{"kind":"Deployment","name":"ff-lca-prd-2-fitconnect-ftc"}\],"type":"kv-v2","vaultAuthRef":"default"}} creationTimestamp: "2026-03-03T15:41:43Z" finalizers: - vaultstaticsecret.secrets.hashicorp.com/finalizer generation: 1 name: fitconnect namespace: lca-prd-2 resourceVersion: "8133193" uid: 873973c8-4125-43db-b508-2052f7e505e1 spec: destination: create: true name: fitconnect overwrite: false transformation: excludes: -.\* templates: auth.json: text: '{"clientId":"{{ "{{" }} get.Secrets "auth0\_client\_id" {{ "}}" }}","clientSecret":"{{ "{{" }} get.Secrets "auth0\_client\_secret" {{ "}}" }}", "audience": "{{ "{{" }} get.Secrets "auth0\_audience" {{ "}}" }}"}' mongodb: text: mongodb://{{ "{{" }} get.Secrets "mongodb\_username" {{ "}}" }}:{{ "{{" }} get.Secrets "mongodb\_password" {{ "}}" }}@ff-lca-prd-2-mongodb-b17ef-0.ff-lca-prd-2-mongodb-b17ef-headless.lca-prd-2.svc.cluster.local:27017/admin?replicaSet=rs0 postgresql.json: text: '{"password":"{{ "{{" }} get.Secrets "postgresql\_password" {{ "}}" }}","username":"{{ "{{" }} get.Secrets "postgresql\_username" {{ "}}" }}"}' s3-access-key: text: '{{ "{{" }} get.Secrets "s3\_access\_key\_id" {{ "}}" }}' s3-secret-key: text: '{{ "{{" }} get.Secrets "s3\_secret\_access\_key" {{ "}}" }}' spicedb.json: text: '{"preSharedKey":"{{ "{{" }} get.Secrets "spicedb\_preshared\_key" {{ "}}" }}"}' hmacSecretData: true mount: secrets namespace: admin/deployments/lca-prd-2 path: application refreshAfter: 5m rolloutRestartTargets: - kind: Deployment name: ff-lca-prd-2-fitconnect-ftc type: kv-v2 vaultAuthRef: default status: lastGeneration: 1 secretMAC: cYfoppPq0FSkmXC5oSd3PmIj4gUpSMc3xdphuVc7eTk=

---

Found it. Compare the templates in the rendered CRs.

SpiceDB (working):

Fitconnect (broken):

The `{{ "{{" }}` idiom in Go templates outputs a literal `{{`. So VSO evaluates the fitconnect template and produces the string `{{ get.Secrets "postgresql_password" }}` as text—it never actually looks up the value. That's why you see raw template strings in the secret.

## Why This Difference Exists

In your values file, the spicedb section uses single-level escaping:

But fitconnect/ffcloud/frontend all use double-level escaping:

The double-escaping pattern is designed to survive two rounds of Go template evaluation. It would be correct if the Helm chart itself was evaluating the template text before writing it into the CR. But the rendered CR shows it's being passed through verbatim into `spec.destination.transformation`—so only VSO evaluates it (one round), and the extra escaping breaks it.

## Key Question before Fixing

Did the Helm chart (`charts/ffnode`) recently change how it renders `vaultSecrets` → `VaultStaticSecret`? The spicedb subchart appears to handle it differently from the fitconnect/ffcloud subcharts. Check if there was a recent change to the chart templates that switched from `spec.secretTransformation` to `spec.destination.transformation`, because that would explain why the double-escaping pattern previously worked but now doesn't.

---

no changes. I have been fixing the same error mulitple times.

---

Right, so it's a systemic escaping issue across your values file. The pattern is clear:

SpiceDB (works)—single-level escaping:

→ VSO receives `{{ get.Secrets "spicedb_preshared_key" }}` → evaluates → actual value

Everything else (broken)—double-level escaping:

→ VSO receives `{{ "{{" }} get.Secrets "…" {{ "}}" }}` → evaluates → literal string `{{ get.Secrets "…" }}`

The fix is to convert every affected template to match the spicedb pattern. For simple values, it's straightforward. For the JSON templates, wrap the whole string in a single backtick block:

Before:

After:

This affects fitconnect, ffcloud, frontend, workflowTemplates, argoWorkflows, certManager, minio, mongodb, postgresql, and grafana sections—basically everything except spicedb.

### Immediate next Action

Do you want me to generate the corrected values file so you can diff it against yours? That'll be faster than hunting each one manually.

---

here is my values file

---

All 0 remaining—every double-escaped pattern is fixed. Let me verify the critical lines look right:

---

I don't think that would work. We have multiple layers of templating. Helm \_helper files and tmplts and so on. That is why it was like it is.

---

You're right, I jumped ahead. If the Helm chart templates use `tpl` to evaluate the values, the double escaping would be needed to survive both Helm's evaluation and VSO's evaluation. SpiceDB's subchart must handle it differently.

The problem then isn't the escaping pattern—it's where the rendered CR ends up putting the templates. Let me check something. In the fitconnect CR we inspected, the templates landed under `spec.destination.transformation`. But in your values file, you're specifying `secretTransformation` (a top-level spec field, not nested under destination).

Can you show me the chart template that renders VaultStaticSecrets for fitconnect? Something like:

I want to see whether the chart is mapping `secretTransformation` → `spec.destination.transformation` or `spec.secretTransformation`, because those are two different fields in VSO and they handle template evaluation differently. If a recent chart change moved it from one to the other without adjusting the escaping, that would explain everything—the double escaping was correct for `spec.secretTransformation` (which evaluates twice) but breaks under `spec.destination.transformation` (which evaluates once).

---

find charts/ffnode -name '\*.tpl' -o -name '\*.yaml' | xargs grep -l 'secretTransformation\\|VaultStaticSecret' | head -10 charts/ffnode/templates/\_argoWorkflows.tpl charts/ffnode/templates/\_helpers.tpl charts/ffnode/values.yaml

---

Let's see how the chart renders VaultStaticSecrets:

And:

Also check if there's a shared helper that builds the VSS spec:

I need to see whether the chart maps `secretTransformation` into `spec.secretTransformation` (two rounds of evaluation—double escaping correct) or `spec.destination.transformation` (one round—double escaping breaks). That's the root cause.

---

find charts/ffnode -name '\*.tpl' -o -name '\*.yaml' | xargs grep -l 'secretTransformation\\|VaultStaticSecret' | head -10 charts/ffnode/templates/\_argoWorkflows.tpl charts/ffnode/templates/\_helpers.tpl charts/ffnode/values.yaml charts/ffnode/templates/\_argoWorkflows.tpl charts/ffnode/templates/\_helpers.tpl charts/ffnode/values.yaml zsh: permission denied: charts/ffnode/templates/\_argoWorkflows.tpl zsh: permission denied: charts/ffnode/templates/\_helpers.tpl zsh: permission denied: charts/ffnode/values.yaml …/helm\_chart\_deployment on  master $ on ⛵ fitfile-cloud-staging-aks-cluster () on ☁️ Shared Services on 🅰 (eu-west-2) at 16:13:53 ❯ cat charts/ffnode/templates/\_argoWorkflows.tpl | grep -A 30 -i 'vaultstaticsecret\\|secretTransformation\\|transformation' secretTransformationDisableTpl: true secretTransformation: excludes: -.\* templates: password: text: '{{"{{ `{{get.Secrets \"postgresql_password\"}}` }}"}}' username: text: '{{"{{ `{{get.Secrets \"postgresql_username\"}}` }}"}}' - secretName: "argo-server-sso" vaultPath: "argo-workflows" secretTransformationDisableTpl: true secretTransformation: excludes: -.\* templates: client-id: text: '{{"{{ `{{get.Secrets \"argo_sso_client_id\"}}` }}"}}' client-secret: text: '{{"{{ `{{get.Secrets \"argo_sso_client_secret\"}}` }}"}}' {{- end -}} {{- end -}} {{/\* Grabs the argo workflows host from a single value in the root values.Values.argoWorkflows.host \*/}} {{- define "argoWorkflowsHost" -}} {{ default "argocd.com".Values.argoWorkflows.host }} {{- end -}} {{- define "argoWorkflowsRedirectUrl" -}} {{- if.Values.argoWorkflows.redirectUrl -}} {{.Values.argoWorkflows.redirectUrl}} {{- else -}} {{printf " [https://%s/oauth2/callback](https://%s/oauth2/callback) ".Values.argoWorkflows.host}} {{- end -}} {{- end -}} # What needs to be configured with argo workflows? # - Host URL # -

---

That's revealing. The argoWorkflows template has `secretTransformationDisableTpl: true` and uses yet another escaping pattern. Now I need to see the main helper that renders VaultStaticSecrets for the other subcharts:

This will show us whether `tpl` is called on the transformation block and whether it writes to `spec.secretTransformation` or `spec.destination.transformation`. That's the key to understanding the correct escaping level.

---

Now I can see the full picture. Here's the critical section:

go

```
{{- if hasKey $config "secretTransformationDisableTpl"}}
transformation: {{ $config.secretTransformation | toYaml | nindent 6}}
{{- else }}
transformation: {{ tpl ($config.secretTransformation | toYaml) $ | nindent 6}}
{{- end }}
\`\`\`

There are exactly two layers of evaluation for your secrets (not three):

### Layer 1: Helm \`tpl\` call
Your values.yaml is loaded as data (not a template). The \`tpl\` function then evaluates it once.

### Layer 2: VSO evaluates the rendered CR

Let me trace both patterns through:

SpiceDB (works):
\`\`\`
Values:  {{ \`{{ get .Secrets "spicedb_preshared_key" }}\` }}
         ↓ tpl evaluates: backtick = raw string, outputs its content
CR:      {{ get .Secrets "spicedb_preshared_key" }}
         ↓ VSO evaluates: looks up the secret
Result:  actual_password_value ✓
\`\`\`

Fitconnect (broken):
\`\`\`
Values:  {{ \`{{ "{{" }} get .Secrets "postgresql_password" {{ "}}" }}\` }}
         ↓ tpl evaluates: backtick = raw string, outputs its content
CR:      {{ "{{" }} get .Secrets "postgresql_password" {{ "}}" }}
         ↓ VSO evaluates: {{ "{{" }} outputs literal "{{"
Result:  {{ get .Secrets "postgresql_password" }}  ← literal text, never looked up ✗
```

The backtick already protects the content from `tpl`. Everything inside the backtick goes directly to VSO. So inside the backtick, you need valid VSO template syntax—not another layer of escaping.

My fix is correct. The file I generated replaces every `{{ "{{" }} get.Secrets "key" {{ "}}" }}` with `{{ get.Secrets "key" }}` inside the backtick blocks. The `tpl` + VSO two-layer chain is fully handled.

The preset patterns in `_helpers.tpl` (like `'{{"{{` {{get.Secrets…}} `}}"}}'`) are different—they're hardcoded in the template itself (not values), so they go through Helm template rendering directly (not `tpl`), and they use double-wrapping to survive that single Helm pass.

Want to review the corrected file I generated and push it?

---

I have pushed those changes to the vaules file. How do I force argocd and vso to pick them up? I do not have argocd cli so give me the kubectl commands

---

First, terminate the stuck parent operation by patching its status:

If it's still `Running`, force-clear it:

Then trigger the fresh sync:

Once the child apps update, force VSO to re-reconcile the secrets by deleting the existing ones (VSO will recreate them with the corrected templates):

Then verify:

That should now show actual credentials instead of raw template strings. If it does, the pods should self-heal via their restart loops.

---

sleep 30 kubectl get secret fitconnect -n lca-prd-2 -o jsonpath='{.data.postgresql\\.json}' | base64 -d {"password":"{{ get.Secrets "postgresql\_password" }}","username":"{{ get.Secrets "postgresql\_username" }}"}%

---

The CR hasn't been updated yet. Let's verify:

If that still shows the double-escaped version, the parent sync didn't push the new commit through. Check:

What's the commit hash of your new push?

---

kubectl get vaultstaticsecret fitconnect -n lca-prd-2 -o jsonpath='{.spec.destination.transformation.templates.postgresql\\.json.text}' {"password":"{{ "{{" }} get.Secrets "postgresql\_password" {{ "}}" }}","username":"{{ "{{" }} get.Secrets "postgresql\_username" {{ "}}" }}"}% ➜ terraform kubectl get application ff-lca-prd-2 -n argocd -o jsonpath='{.status.operationState.phase}' kubectl get application ff-lca-prd-2 -n argocd -o jsonpath='{.status.sync.revision}' Error%

---

The sync errored. Let's see why:

And check if ArgoCD even sees the new commit:

Also—what does the app status look like now?

---

It looks like the templating kubectl get application ff-lca-prd-2 -n argocd -o jsonpath='{.status.operationState.message}' ComparisonError: Failed to load target state: failed to generate manifest for source 1 of 2: rpc error: code = Unknown desc = failed to execute helm template command: failed to get command args to log: `helm template. --name-template ff-lca-prd-2 --namespace argocd --kube-version 1.34 --values <path to cached source>/generated/values.yaml <api versions removed> --include-crds` failed exit status 1: Error: template: ffnode/templates/workflow-templates-application.yaml:25:4: executing "ffnode/templates/workflow-templates-application.yaml" at <include "renderValuesWithVaultSecretInExtraDeploy" (list. $values)>: error calling include: template: ffnode/templates/\_helpers.tpl:135:33: executing "renderValuesWithVaultSecretInExtraDeploy" at <include "generateVaultDynamicSecrets" (list $root $item)>: error calling include: template: ffnode/templates/\_helpers.tpl:80:23: executing "generateVaultDynamicSecrets" at <tpl ($config.secretTransformation | toYaml) $>: error calling tpl: error during tpl function execution for "excludeRaw: true\\nexcludes:\\n-.\*\\ntemplates:\\n s3\_access\_key\_id:\\n text: '{{ get.Secrets \\"s3\_access\_key\_id\\" }}'\\n s3\_endpoint:\\n text: '{{ get.Secrets \\"s3\_endpoint\\" }}'\\n s3\_region:\\n text: '{{ get.Secrets \\"s3\_region\\" }}'\\n s3\_role\_arn:\\n text: '{{ get.Secrets \\"s3\_role\_arn\\" }}'\\n s3\_secret\_access\_key:\\n text: '{{ get.Secrets \\"s3\_secret\_access\_key\\" }}'": template: gotpl:6:18: executing "gotpl" at <.Secrets>: wrong type for value; expected map\[string\]interface {}; got interface {} Use --debug flag to render out invalid YAML% ➜ terraform kubectl get application ff-lca-prd-2 -n argocd -o jsonpath='{.status.sync.status}' kubectl get application ff-lca-prd-2 -n argocd -o jsonpath='{.status.sync.comparedTo}' | jq. Unknown{ "destination": { "namespace": "argocd", "server": " [https://kubernetes.default.svc](<https://kubernetes.default.svc/>) " }, "sources": \[{ "helm": { "valueFiles": \["$values/generated/values.yaml" \] }, "path": "charts/ffnode", "repoURL": " [https://gitlab.com/fitfile/deployment.git](https://gitlab.com/fitfile/deployment.git) ", "targetRevision": "lcrca-prod-latest-release" }, { "ref": "values", "repoURL": " [https://gitlab.com/fitfile/customers/nwsde/lca-infrastructure-prd.git](https://gitlab.com/fitfile/customers/nwsde/lca-infrastructure-prd.git) ", "targetRevision": "main" } \] } ➜ terraform kubectl get applications -n argocd NAME SYNC STATUS HEALTH STATUS argo-workflows Synced Healthy blob-csi-driver Synced Healthy cert-manager Synced Healthy ff-lca-prd-2 Unknown Degraded ff-lca-prd-2-ffcloud-service Synced Progressing ff-lca-prd-2-fitconnect Synced Progressing ff-lca-prd-2-minio Synced Healthy ff-lca-prd-2-mongodb-b17ef Synced Healthy ff-lca-prd-2-postgresql Synced Healthy ff-lca-prd-2-workflow-templates Synced Healthy ff-lca-prd-2-workflows-api Synced Healthy grafana-k8s-monitoring Synced Healthy prometheus-operator-crds Synced Healthy spicedb Synced Healthy

---

Right, I was wrong to apply a blanket fix. The error reveals the problem—`extraVaultSecrets` goes through `tpl` twice in the chart:

1. `renderValuesWithVaultSecretInExtraDeploy` `tpl` 's everything except `vaultSecrets` (but `extraVaultSecrets` is NOT excluded)
2. `generateVaultDynamicSecrets` calls `tpl` on `secretTransformation` again

So `extraVaultSecrets` needs the double escaping to survive two `tpl` passes. Regular `vaultSecrets` entries only get `tpl` 'd once, so they need single escaping.

My fix was correct for `vaultSecrets` but broke `extraVaultSecrets`. Only one section is affected—the `workflowTemplates.extraVaultSecrets` block (the s3-export-secret).

Let me fix the file:

---

\# Step 7: Check secrets are populated sleep 30 kubectl get secret fitconnect -n lca-prd-2 -o jsonpath='{.data.postgresql\\.json}' | base64 -d {"password":"{{ get.Secrets "postgresql\_password" }}","username":"{{ get.Secrets "postgresql\_username" }}"}%

---

Still raw templates. Let's verify the CR actually updated:

If that now shows `{{ get.Secrets "postgresql_password" }}` (single-escaped, no `"{{" }}`), then VSO received it correctly but hasn't re-reconciled. Force it:

If the CR still shows the old double-escaped version, the sync didn't update it. In that case check:

---

kubectl get vaultstaticsecret fitconnect -n lca-prd-2 -o jsonpath='{.spec.destination.transformation.templates.postgresql\\.json.text}' {"password":"{{ "{{" }} get.Secrets "postgresql\_password" {{ "}}" }}","username":"{{ "{{" }} get.Secrets "postgresql\_username" {{ "}}" }}"}% ➜ terraform # Delete the secret to force VSO to recreate kubectl delete secret fitconnect -n lca-prd-2 # Check VSO logs for errors kubectl logs deployment/vault-secrets-operator-controller-manager -n vault-secrets-operator-system --tail=30 | grep -i 'fitconnect\\|error\\|fail' secret "fitconnect" deleted from lca-prd-2 namespace ➜ terraform kubectl get application ff-lca-prd-2-fitconnect -n argocd -o jsonpath='{.status.sync.status}' Synced%

---

The CR hasn't been updated—the parent sync failed earlier (the `extraVaultSecrets` error) before it could update the fitconnect child app. The child says "Synced" but against the old spec.

You need to sync the parent again now that the corrected file (with `extraVaultSecrets` reverted) is pushed:

Then watch for the parent to succeed:

Once the parent completes successfully, then check if the fitconnect CR updated:

---

\# Check parent status first kubectl get application ff-lca-prd-2 -n argocd -o jsonpath='{.status.operationState.phase}' Failed% # Trigger fresh sync kubectl annotate application ff-lca-prd-2 -n argocd argocd.argoproj.io/refresh=hard --overwrite sleep 5 kubectl patch application ff-lca-prd-2 -n argocd --type merge -p '{"operation":{"initiatedBy":{"username":"leon"},"sync":{"revision":"HEAD"}}}' application.argoproj.io/ff-lca-prd-2 annotated application.argoproj.io/ff-lca-prd-2 patched ➜ terraform watch -n 5 'kubectl get application ff-lca-prd-2 -n argocd -o jsonpath="{.status.operationState.phase}" && echo "" && kubectl get application ff-lca-prd-2 -n argocd -o jsonpath="{.status.operationState.message}"'

---

What's it showing? If it flips to `Succeeded`, check the CR immediately:

If it fails again with the same template error, it means the corrected file hasn't been pushed yet—confirm with:

---

kubectl get vaultstaticsecret fitconnect -n lca-prd-2 -o jsonpath='{.spec.destination.transformation.templates.postgresql\\.json.text}' {"password":"{{ "{{" }} get.Secrets "postgresql\_password" {{ "}}" }}","username":"{{ "{{" }} get.Secrets "postgresql\_username" {{ "}}" }}"}% ➜ terraform kubectl get application ff-lca-prd-2 -n argocd -o jsonpath='{.status.operationState.message}' one or more synchronization tasks completed unsuccessfully%

---

The parent completed but something failed. Let's find out what failed and whether the fitconnect child even got updated:

The fitconnect VaultStaticSecret is rendered by the child app `ff-lca-prd-2-fitconnect`, not directly by the parent. Even if the parent synced, the child needs to re-sync with the new values. Check if the child is OutOfSync:

---

\# What failed? kubectl get application ff-lca-prd-2 -n argocd -o jsonpath='{.status.operationState.syncResult.resources}' | jq '.\[\] | select(.hookPhase!= "Succeeded")' # Did the fitconnect child app get a new spec? kubectl get application ff-lca-prd-2-fitconnect -n argocd -o jsonpath='{.status.sync.revision}' # What's your latest commit hash? { "group": "argoproj.io", "hookPhase": "Failed", "kind": "Application", "message": "Failed to load target state: failed to generate manifest for source 1 of 1: rpc error: code = Unknown desc = failed to execute helm template command: failed to get command args to log: `helm template. --name-template cert-manager --namespace cert-manager --kube-version 1.34 --values /tmp/e76c9151-9e9a-4151-a67d-5e5eea315ad3 <api versions removed> --include-crds` failed exit status 1: Error: template: cert-manager/templates/extras-objects.yaml:3:3: executing \\"cert-manager/templates/extras-objects.yaml\\" at <tpl. $>: error calling tpl: error during tpl function execution for \\"apiVersion: secrets.hashicorp.com/v1beta1\\\\nkind: VaultStaticSecret\\\\nmetadata:\\\\n name: cloudflare-issuer-api-token\\\\nspec:\\\\n destination:\\\\n create: true\\\\n name: cloudflare-issuer-api-token\\\\n transformation:\\\\n excludes:\\\\n -.\*\\\\n templates:\\\\n api-token:\\\\n text: '{{ get.Secrets \\\\\\"api-token\\\\\\" }}'\\\\n hmacSecretData: true\\\\n mount: secrets\\\\n namespace: admin/deployments/lca-prd-2\\\\n path: cloudflare\\\\n refreshAfter: null\\\\n rolloutRestartTargets: \[\]\\\\n type: kv-v2\\\\n vaultAuthRef: default\\": template: gotpl:14:24: executing \\"gotpl\\" at <.Secrets>: wrong type for value; expected map\[string\]interface {}; got interface {}\\n\\nUse --debug flag to render out invalid YAML", "name": "cert-manager", "namespace": "argocd", "status": "Synced", "syncPhase": "Sync", "version": "v1alpha1" } 24fcdf3163575ab5a2c89fff1d09a1ac97969983% kubectl get application ff-lca-prd-2-fitconnect -n argocd -o jsonpath='{.status.sync.status}' kubectl get application ff-lca-prd-2-fitconnect -n argocd -o jsonpath='{.status.resources}' | jq '.\[\] | select(.status!= "Synced")' Synced%

---

Two problems visible:

1. cert-manager failed—its VaultStaticSecret is rendered through cert-manager's own `extras-objects.yaml` which calls `tpl` again. So it needs double escaping, same as `extraVaultSecrets`.
2. fitconnect never got updated—the parent sync failed on cert-manager before reaching the other child apps. Revision is still the old one.

We need to revert cert-manager's `api-token` back to double escaping too. Same root cause—additional `tpl` pass in the subchart.

---

kubectl patch application ff-lca-prd-2 -n argocd --type merge -p '{"operation":{"initiatedBy":{"username":"leon"},"sync":{"revision":"HEAD"}}}' application.argoproj.io/ff-lca-prd-2 patched ➜ terraform kubectl get secret fitconnect -n lca-prd-2 -o jsonpath='{.data.postgresql\\.json}' | base64 -d {"password":"{{ get.Secrets "postgresql\_password" }}","username":"{{ get.Secrets "postgresql\_username" }}"}%

---

Too early—the sync needs time. Check the progress:

Wait for `Succeeded`, then check if the child CR updated:

If the CR updates but the secret doesn't, delete the secret to force VSO to recreate it:

---

kubectl get vaultstaticsecret fitconnect -n lca-prd-2 -o jsonpath='{.spec.destination.transformation.templates.postgresql\\.json.text}' {"password":"{{ get.Secrets "postgresql\_password" }}","username":"{{ get.Secrets "postgresql\_username" }}"}% ➜ terraform kubectl delete secret fitconnect -n lca-prd-2 sleep 15 kubectl get secret fitconnect -n lca-prd-2 -o jsonpath='{.data.postgresql\\.json}' | base64 -d secret "fitconnect" deleted from lca-prd-2 namespace

---

The CR is updated—that's the single-escaped version now. What did the final command output? After the `sleep 15`, did `base64 -d` show actual credentials or still the template string?

If the secret hasn't been recreated yet:

If it exists, check the value:

If it doesn't exist yet, VSO may need a nudge:

---

kubectl get secret fitconnect -n lca-prd-2 -o jsonpath='{.data.postgresql\\.json}' | base64 -d {"password":"yAG…..","username":"postgres"}%

---

That's real credentials. The fix works.

Check if the pods are recovering:

And the overall app status:

---

kubectl get pods -n lca-prd-2 NAME READY STATUS RESTARTS AGE ff-lca-prd-2-ffcloud-service-6567b68b99-5vs78 0/3 Init:CrashLoopBackOff 4 (65s ago) 2m43s ff-lca-prd-2-ffcloud-service-86f4578f7-vxx6n 0/3 Init:CrashLoopBackOff 7 (4m1s ago) 15m ff-lca-prd-2-fitconnect-ftc-5b7c54c575-dxgf7 0/1 CrashLoopBackOff 4 (24s ago) 2m8s ff-lca-prd-2-fitconnect-ftc-5d97d498f4-xdjsf 0/1 CrashLoopBackOff 4 (44s ago) 2m43s ff-lca-prd-2-minio-6c9b4586f4-94nfs 1/1 Running 0 6h5m ff-lca-prd-2-minio-provisioning-ftxtt 0/1 Completed 4 6h6m ff-lca-prd-2-mongodb-b17ef-0 2/2 Running 7 (6h17m ago) 6h25m ff-lca-prd-2-mongodb-b17ef-arbiter-0 1/1 Running 0 6h9m ff-lca-prd-2-postgresql-0 1/1 Running 0 9h workflows-api-6df47dfd8f-5hl4p 1/1 Running 0 3h57m

---

Pods are still crashlooping from before the fix. New replicas were created but may have started before the secret was recreated. Check the latest fitconnect logs:

If it's the same JSON parse error, the pod picked up the old secret. Force a fresh rollout:

Then watch:

---

kubectl get pods -n lca-prd-2 NAME READY STATUS RESTARTS AGE ff-lca-prd-2-ffcloud-service-6567b68b99-5vs78 0/3 Init:CrashLoopBackOff 5 (57s ago) 4m7s ff-lca-prd-2-ffcloud-service-769bd96cd8-b8j5h 0/3 Init:Error 2 (25s ago) 32s ff-lca-prd-2-fitconnect-ftc-555b9c5d4f-vvcdn 0/1 Running 2 (17s ago) 32s ff-lca-prd-2-fitconnect-ftc-5b7c54c575-dxgf7 0/1 CrashLoopBackOff 5 (15s ago) 3m32s ff-lca-prd-2-minio-6c9b4586f4-94nfs 1/1 Running 0 6h6m ff-lca-prd-2-minio-provisioning-ftxtt 0/1 Completed 4 6h7m ff-lca-prd-2-mongodb-b17ef-0 2/2 Running 7 (6h18m ago) 6h27m ff-lca-prd-2-mongodb-b17ef-arbiter-0 1/1 Running 0 6h11m ff-lca-prd-2-postgresql-0 1/1 Running 0 9h workflows-api-6df47dfd8f-5hl4p 1/1 Running 0 3h59m

---

Fitconnect's new pod is Running—promising. ffcloud's new pod is erroring in init. Check it:

And verify the ffcloud secret is also populated:

---

kubectl logs ff-lca-prd-2-ffcloud-service-769bd96cd8-b8j5h -n lca-prd-2 -c $(kubectl get pod ff-lca-prd-2-ffcloud-service-769bd96cd8-b8j5h -n lca-prd-2 -o jsonpath='{.spec.initContainers\[0\].name}') yarn run v1.22.22 $ node db-migrations/nosql/migration-runner.js up {"name":"MongoMigrationManager","hostname":"ff-lca-prd-2-ffcloud-service-769bd96cd8-b8j5h","pid":28,"level":20,"msg":"Checking migrations for ffcloud","time":"2026-03-03T19:41:11.286Z","v":0} - Migrations up - Applying migration SetSpicedbSchema\_20250725183221 ✖ Error executing migration SetSpicedbSchema\_20250725183221 ✖ Error executing migrations ExecuteMigrationError: Error: 16 UNAUTHENTICATED: missing preshared key at up (/app/node\_modules/mongo-migrate-ts/dist/lib/commands/up.js:47:23) at process.processTicksAndRejections (node:internal/process/task\_queues:105:5) at async Command.<anonymous> (/app/node\_modules/mongo-migrate-ts/dist/lib/cli.js:52:17) error Command failed with exit code 1. info Visit [https://yarnpkg.com/en/docs/cli/run](https://yarnpkg.com/en/docs/cli/run) for documentation about this command. ➜ terraform kubectl get secret ffcloud -n lca-prd-2 -o jsonpath='{.data.postgresql\\.json}' | base64 -d {"password":"yAGK…ef2Gcq","username":"postgres"}%

---

PostgreSQL credentials are fine. The error is SpiceDB authentication—the migration can't connect to SpiceDB. Check the spicedb.json secret:

If it shows the actual preshared key, then the migration might be looking for it in a different location or env var. If it's empty or raw template, that's the problem.

---

---

Empty value. The template is correct but the Vault path doesn't contain `spicedb_preshared_key`. The ffcloud VaultStaticSecret reads from `applicationVaultPath` (likely `application`), but the spicedb preshared key is stored at the `spicedb` Vault path.

Check what keys exist at the application path:

And check if fitconnect has the same issue:

This is likely a Vault data issue—`spicedb_preshared_key` needs to be added to the application secret in Vault at `secrets/admin/deployments/lca-prd-2/application`, or the template needs to pull from a different path. Was this key previously in the application Vault path, or is this a new deployment?

---

kubectl get secret ffcloud -n lca-prd-2 -o jsonpath='{.data}' | jq 'keys' \["\_raw", "auth.json", "cli-auth.json", "mongodb", "mongodb.json", "postgresql.json", "spicedb.json" \] kubectl get secret fitconnect -n lca-prd-2 -o jsonpath='{.data.spicedb\\.json}' | base64 -d {"preSharedKey":""}%

---

Both empty. The `spicedb_preshared_key` doesn't exist at the `application` path in Vault—it only exists at the `spicedb` path. You need to add it to your Vault secret at `secrets/admin/deployments/lca-prd-2/application`:

Then add the spicedb preshared key to it:

Once it's in Vault, VSO will pick it up on its next refresh cycle (5m for fitconnect/ffcloud). To speed it up:

Is this a brand new deployment, or was `spicedb_preshared_key` previously at the `application` path?

---

it is there == application === \["auth0\_audience", "auth0\_client\_id", "auth0\_client\_secret", "cli\_auth\_client\_id", "cli\_auth\_client\_secret", "fitfile\_tenant\_pkcs8\_key", "fitfile\_tenant\_public\_crt", "grafana\_admin\_password", "loki\_password", "mongodb\_password", "mongodb\_replica\_set\_key", "mongodb\_username", "postgresql\_password", "postgresql\_username", "prometheus\_password", "s3\_access\_key\_id", "s3\_secret\_access\_key", "spicedb\_pre\_shared\_key", "tempo\_password", "ude\_key", "vm\_admin\_password" \] === argo-workflows === \["postgresql\_password", "postgresql\_username" \] === argocd === \["admin\_password", "gitlab\_deploy\_token\_password", "gitlab\_deploy\_token\_username", "gitlab\_values\_access\_token", "gitlab\_values\_access\_username", "server\_secret\_key", "unhashed\_admin\_password" \] === atlas === No value found at secrets/data/atlas === hutch === No value found at secrets/data/hutch === hutch-prod === No value found at secrets/data/hutch-prod === monitoring === \["loki\_password", "loki\_username", "prometheus\_password", "prometheus\_username", "tempo\_password", "tempo\_username" \] === spicedb === \["postgresql\_password", "postgresql\_username", "spicedb\_preshared\_key" \] === thehyve === No value found at secrets/data/thehyve \_\_wezterm\_user\_vars\_precmd:2: command not found: id

---

Same typo, different location. Look at the Vault keys:

- `application` path:`spicedb_pre_shared_key`
- `spicedb` path:`spicedb_preshared_key`
- Templates reference:`spicedb_preshared_key`

The `application` secret has the underscore variant (`pre_shared`) while the templates expect `preshared`. You need to fix it in Vault:

Then optionally clean up the old key, or leave it for now. Once patched, force the refresh:

This is the same `pre_shared` vs `preshared` naming inconsistency that caused the original SpiceDB issue. Worth standardising across all Vault paths once things are stable.

---

kubectl get pods -n lca-prd-2 NAME READY STATUS RESTARTS AGE ff-lca-prd-2-ffcloud-service-665767b7c5-z8vjc 3/3 Running 0 5m8s ff-lca-prd-2-fitconnect-ftc-7667689d49-spsqr 1/1 Running 0 5m8s ff-lca-prd-2-minio-6c9b4586f4-94nfs 1/1 Running 0 6h19m ff-lca-prd-2-minio-provisioning-ftxtt 0/1 Completed 4 6h20m ff-lca-prd-2-mongodb-b17ef-0 2/2 Running 7 (6h31m ago) 6h40m ff-lca-prd-2-mongodb-b17ef-arbiter-0 1/1 Running 0 6h24m ff-lca-prd-2-postgresql-0 1/1 Running 0 9h workflows-api-6df47dfd8f-5hl4p 1/1 Running 0 4h12m ➜ terraform kubectl get applications -n argocd NAME SYNC STATUS HEALTH STATUS argo-workflows Synced Healthy blob-csi-driver Synced Healthy cert-manager Synced Healthy ff-lca-prd-2 OutOfSync Healthy ff-lca-prd-2-ffcloud-service Synced Healthy ff-lca-prd-2-fitconnect Synced Healthy ff-lca-prd-2-minio Synced Healthy ff-lca-prd-2-mongodb-b17ef Synced Healthy ff-lca-prd-2-postgresql Synced Healthy ff-lca-prd-2-workflow-templates Synced Healthy ff-lca-prd-2-workflows-api Synced Healthy grafana-k8s-monitoring Synced Healthy prometheus-operator-crds Synced Healthy spicedb Synced Healthy

---

Everything is up and running. All pods healthy, all child apps Synced/Healthy.

The parent `ff-lca-prd-2` showing `OutOfSync` is likely just the `rollout restart` annotation drift again. One final sync should clear it:

### Summary of what We Fixed Today

1. SpiceDB crash—VaultStaticSecret template had `spicedb_pre_shared_key` (typo), Vault field was `spicedb_preshared_key`. Fixed in values file.
2. Fitconnect/ffcloud/frontend crash—Double-escaped VSO templates (`{{ "{{" }} get.Secrets … {{ "}}" }}`) were passing through `tpl` only once, so VSO received literal template strings instead of evaluating them. Fixed to single escaping for these three subcharts only (other subcharts go through two `tpl` passes and need double escaping).
3. Empty spicedb preshared key in fitconnect/ffcloud—The `application` Vault path had the key as `spicedb_pre_shared_key` while templates referenced `spicedb_preshared_key`. Fixed in Vault.

### Recommendation for when Things Are Calm

Standardise the naming across all Vault paths—`spicedb_pre_shared_key` in `application` vs `spicedb_preshared_key` in `spicedb` is a landmine. Pick one and update both Vault and all templates to match.

---

kubectl get pods -n lca-prd-2 NAME READY STATUS RESTARTS AGE ff-lca-prd-2-ffcloud-service-665767b7c5-z8vjc 3/3 Running 0 6m9s ff-lca-prd-2-fitconnect-ftc-7667689d49-spsqr 1/1 Running 0 6m9s ff-lca-prd-2-frontend-frontend-866b86d869-tgq85 0/1 ErrImagePull 0 11s ff-lca-prd-2-minio-6c9b4586f4-94nfs 1/1 Running 0 6h21m ff-lca-prd-2-minio-provisioning-ftxtt 0/1 Completed 4 6h21m ff-lca-prd-2-mongodb-b17ef-0 2/2 Running 7 (6h32m ago) 6h41m ff-lca-prd-2-mongodb-b17ef-arbiter-0 1/1 Running 0 6h25m ff-lca-prd-2-postgresql-0 1/1 Running 0 9h workflows-api-6df47dfd8f-5hl4p 1/1 Running 0 4h13m

---

---

kubectl describe pod ff-lca-prd-2-frontend-frontend-866b86d869-tgq85 -n lca-prd-2 | grep -A 5 'Events\\|image\\|Failed\\|Error' Events: Type Reason Age From Message ---- ------ ---- ---- ------- Normal Scheduled 37s default-scheduler Successfully assigned lca-prd-2/ff-lca-prd-2-frontend-frontend-866b86d869-tgq85 to aks-system-38063810-vmss000001 Normal Pulling 25s (x2 over 37s) kubelet Pulling image "fitfileregistry.azurecr.io/frontend:0.1.618" Warning Failed 25s (x2 over 37s) kubelet Failed to pull image "fitfileregistry.azurecr.io/frontend:0.1.618": failed to pull and unpack image "fitfileregistry.azurecr.io/frontend:0.1.618": failed to resolve reference "fitfileregistry.azurecr.io/frontend:0.1.618": failed to authorize: failed to fetch anonymous token: unexpected status from GET request to [https://fitfileregistry.azurecr.io/oauth2/token?scope=repository%3Afrontend%3Apull&service=fitfileregistry.azurecr.io](https://fitfileregistry.azurecr.io/oauth2/token?scope=repository%3Afrontend%3Apull&service=fitfileregistry.azurecr.io): 401 Unauthorized Warning Failed 25s (x2 over 37s) kubelet Error: ErrImagePull Normal BackOff 10s (x2 over 36s) kubelet Back-off pulling image "fitfileregistry.azurecr.io/frontend:0.1.618" Warning Failed 10s (x2 over 36s) kubelet Error: ImagePullBackOff

---

401 Unauthorized—the image pull secret isn't working for this pod. Check if it exists in the namespace:

And verify the pod is referencing it:

The other pods (fitconnect, ffcloud) are pulling from the same registry and working, so either the frontend deployment is missing the `imagePullSecrets` reference, or the secret doesn't exist yet in the namespace.

---

No `imagePullSecrets` on the pod at all. The secret exists but the frontend Deployment isn't referencing it. Your values file has it set:

But the rendered pod has no `imagePullSecrets`. Check the Deployment directly:

If that's empty, the frontend subchart might expect `imagePullSecrets` under `global` rather than at the subchart level. The fix may already be present via `global.imagePullSecrets` in your values, but the frontend chart might not read from there.

Quick fix to unblock right now—patch the deployment directly:

Then investigate why the chart isn't passing it through—this is likely a separate chart templating issue to fix in the Helm chart itself.

---

kubectl get deployment ff-lca-prd-2-frontend-frontend -n lca-prd-2 -o jsonpath='{.spec.template.spec.imagePullSecrets}' ➜ terraform kubectl get deployment ff-lca-prd-2-frontend-frontend -n lca-prd-2 -o jsonpath='{.spec.template.spec}' {"containers":\[{"args":\["if \[-f /secrets/config \]; then\\n source /secrets/config;\\nelse\\n echo \\"No secrets file to source\\";\\nfi;\\nnode server.js;\\n"\],"command":\["sh","-c"\],"env":\[{"name":"RESULT\_DETAILS\_LIMIT","value":"10000"},{"name":"INACTIVITY\_TIME\_PERIOD","value":"900000"},{"name":"FITFILE\_ENV","value":"production"},{"name":"GRAPHQL\_API\_URL","valueFrom":{"configMapKeyRef":{"key":"graphqlApiUrl","name":"ff-lca-prd-2-frontend-frontend-app-config-24cd4f3bf0ddefc10a237"}}},{"name":"TENANT\_NAME","valueFrom":{"configMapKeyRef":{"key":"tenantName","name":"ff-lca-prd-2-frontend-frontend-app-config-24cd4f3bf0ddefc10a237"}}},{"name":"NEXTAUTH\_SECRET","valueFrom":{"configMapKeyRef":{"key":"nextAuthSecret","name":"ff-lca-prd-2-frontend-frontend-app-config-24cd4f3bf0ddefc10a237"}}},{"name":"NEXTAUTH\_URL","value":" [https://lca-prd-2.privatelink.fitfile.net/fitfile/api/auth"},{"name":"REST\_API\_URL","valueFrom":{"configMapKeyRef":{"key":"restApiUrl","name":"ff-lca-prd-2-frontend-frontend-app-config-24cd4f3bf0ddefc10a237"}}},{"name":"ATLAS\_BASE\_URL","valueFrom":{"configMapKeyRef":{"key":"atlasApiUrl","name":"ff-lca-prd-2-frontend-frontend-app-config-24cd4f3bf0ddefc10a237","optional":true}}},{"name":"AUTH0\_ISSUER","valueFrom":{"configMapKeyRef":{"key":"oauthBaseURL","name":"ff-lca-prd-2-frontend-frontend-app-config-24cd4f3bf0ddefc10a237"}}},{"name":"AUTH0\_AUDIENCE","valueFrom":{"configMapKeyRef":{"key":"oauthAudience","name":"ff-lca-prd-2-frontend-frontend-app-config-24cd4f3bf0ddefc10a237"}}},{"name":"LOG\_LEVEL","value":"info"},{"name":"FEATURE\_UPDATE\_QUERY\_PLAN","value":"true"},{"name":"FEATURE\_CREATE\_QUERY\_PLAN","value":"true"},{"name":"FEATURE\_DELETE\_QUERY\_PLAN","value":"true"},{"name":"FEATURE\_QUICK\_PROJECT\_CREATION","value":"true"},{"name":"FEATURE\_CUSTOM\_PROJECT\_NAME","value":"true"},{"name":"FEATURE\_CREATE\_CUSTOM\_TRANSFORMATIONS","value":"true"},{"name":"FEATURE\_PII\_DETECTION\_OPERATION","value":"false"},{"name":"FEATURE\_JIRA\_HELPDESK\_WIDGET","value":"false"},{"name":"FEATURE\_NHS\_PET\_AND\_PRIVACY\_TREATMENT\_QUERY\_PLAN","value":"false"},{"name":"FEATURE\_RAW\_USER\_INPUTS","value":"true"},{"name":"FEATURE\_OMOP\_DATA\_EXTRACT","value":"false"}\],"image":"fitfileregistry.azurecr.io/frontend:0.1.618","imagePullPolicy":"Always","livenessProbe":{"failureThreshold":3,"initialDelaySeconds":30,"periodSeconds":15,"successThreshold":1,"tcpSocket":{"port":4000},"timeoutSeconds":1},"name":"ff-lca-prd-2-frontend-frontend","ports":\[{"containerPort":4000,"name":"http","protocol":"TCP"}\],"readinessProbe":{"failureThreshold":3,"initialDelaySeconds":15,"periodSeconds":15,"successThreshold":1,"tcpSocket":{"port":4000},"timeoutSeconds":1},"resources":{"requests":{"cpu":"100m"}},"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File","volumeMounts":\[{"mountPath":"/secrets","name":"frontend-secrets","readOnly":true}\]}\],"dnsPolicy":"ClusterFirst","restartPolicy":"Always","schedulerName":"default-scheduler","securityContext":{},"terminationGracePeriodSeconds":30,"volumes":\[{"name":"frontend-secrets","secret":{"defaultMode":420,"secretName":"frontend"}}\]}%](https://lca-prd-2.privatelink.fitfile.net/fitfile/api/auth%22%7D,%7B%22name%22:%22REST_API_URL%22,%22valueFrom%22:%7B%22configMapKeyRef%22:%7B%22key%22:%22restApiUrl%22,%22name%22:%22ff-lca-prd-2-frontend-frontend-app-config-24cd4f3bf0ddefc10a237%22%7D%7D%7D,%7B%22name%22:%22ATLAS_BASE_URL%22,%22valueFrom%22:%7B%22configMapKeyRef%22:%7B%22key%22:%22atlasApiUrl%22,%22name%22:%22ff-lca-prd-2-frontend-frontend-app-config-24cd4f3bf0ddefc10a237%22,%22optional%22:true%7D%7D%7D,%7B%22name%22:%22AUTH0_ISSUER%22,%22valueFrom%22:%7B%22configMapKeyRef%22:%7B%22key%22:%22oauthBaseURL%22,%22name%22:%22ff-lca-prd-2-frontend-frontend-app-config-24cd4f3bf0ddefc10a237%22%7D%7D%7D,%7B%22name%22:%22AUTH0_AUDIENCE%22,%22valueFrom%22:%7B%22configMapKeyRef%22:%7B%22key%22:%22oauthAudience%22,%22name%22:%22ff-lca-prd-2-frontend-frontend-app-config-24cd4f3bf0ddefc10a237%22%7D%7D%7D,%7B%22name%22:%22LOG_LEVEL%22,%22value%22:%22info%22%7D,%7B%22name%22:%22FEATURE_UPDATE_QUERY_PLAN%22,%22value%22:%22true%22%7D,%7B%22name%22:%22FEATURE_CREATE_QUERY_PLAN%22,%22value%22:%22true%22%7D,%7B%22name%22:%22FEATURE_DELETE_QUERY_PLAN%22,%22value%22:%22true%22%7D,%7B%22name%22:%22FEATURE_QUICK_PROJECT_CREATION%22,%22value%22:%22true%22%7D,%7B%22name%22:%22FEATURE_CUSTOM_PROJECT_NAME%22,%22value%22:%22true%22%7D,%7B%22name%22:%22FEATURE_CREATE_CUSTOM_TRANSFORMATIONS%22,%22value%22:%22true%22%7D,%7B%22name%22:%22FEATURE_PII_DETECTION_OPERATION%22,%22value%22:%22false%22%7D,%7B%22name%22:%22FEATURE_JIRA_HELPDESK_WIDGET%22,%22value%22:%22false%22%7D,%7B%22name%22:%22FEATURE_NHS_PET_AND_PRIVACY_TREATMENT_QUERY_PLAN%22,%22value%22:%22false%22%7D,%7B%22name%22:%22FEATURE_RAW_USER_INPUTS%22,%22value%22:%22true%22%7D,%7B%22name%22:%22FEATURE_OMOP_DATA_EXTRACT%22,%22value%22:%22false%22%7D],%22image%22:%22fitfileregistry.azurecr.io/frontend:0.1.618%22,%22imagePullPolicy%22:%22Always%22,%22livenessProbe%22:%7B%22failureThreshold%22:3,%22initialDelaySeconds%22:30,%22periodSeconds%22:15,%22successThreshold%22:1,%22tcpSocket%22:%7B%22port%22:4000%7D,%22timeoutSeconds%22:1%7D,%22name%22:%22ff-lca-prd-2-frontend-frontend%22,%22ports%22:[%7B%22containerPort%22:4000,%22name%22:%22http%22,%22protocol%22:%22TCP%22%7D],%22readinessProbe%22:%7B%22failureThreshold%22:3,%22initialDelaySeconds%22:15,%22periodSeconds%22:15,%22successThreshold%22:1,%22tcpSocket%22:%7B%22port%22:4000%7D,%22timeoutSeconds%22:1%7D,%22resources%22:%7B%22requests%22:%7B%22cpu%22:%22100m%22%7D%7D,%22terminationMessagePath%22:%22/dev/termination-log%22,%22terminationMessagePolicy%22:%22File%22,%22volumeMounts%22:[%7B%22mountPath%22:%22/secrets%22,%22name%22:%22frontend-secrets%22,%22readOnly%22:true%7D]%7D],%22dnsPolicy%22:%22ClusterFirst%22,%22restartPolicy%22:%22Always%22,%22schedulerName%22:%22default-scheduler%22,%22securityContext%22:%7B%7D,%22terminationGracePeriodSeconds%22:30,%22volumes%22:[%7B%22name%22:%22frontend-secrets%22,%22secret%22:%7B%22defaultMode%22:420,%22secretName%22:%22frontend%22%7D%7D]%7D%)

---

Confirmed—no `imagePullSecrets` in the Deployment at all. Patch it now to unblock:

Then watch:

This is a separate chart issue—the frontend subchart isn't picking up `imagePullSecrets` from your values. That's a fix for the Helm chart itself, not the values file. We can investigate the frontend chart template once the deployment is stable. For now the patch will get it running.

---

kubectl get applications -n argocd NAME SYNC STATUS HEALTH STATUS argo-workflows Synced Healthy blob-csi-driver Synced Healthy cert-manager Synced Healthy certificates Synced Progressing ff-lca-prd-2 OutOfSync Progressing ff-lca-prd-2-ffcloud-service Synced Healthy ff-lca-prd-2-fitconnect Synced Healthy ff-lca-prd-2-frontend Synced Healthy ff-lca-prd-2-minio Synced Healthy ff-lca-prd-2-mongodb-b17ef Synced Healthy ff-lca-prd-2-postgresql Synced Healthy ff-lca-prd-2-workflow-templates Synced Healthy ff-lca-prd-2-workflows-api Synced Healthy grafana-k8s-monitoring Synced Healthy prometheus-operator-crds Synced Healthy spicedb Synced Healthy

---

Looking good. All the core apps are Synced/Healthy. `certificates` is still Progressing—that's likely Let's Encrypt issuing the TLS cert, which can take a minute or two.

Once that completes, the parent should settle. You're essentially up and running now.

### Final State

- SpiceDB—Healthy
- Fitconnect—Healthy
- FFCloud—Healthy
- Frontend—Healthy
- Workflows API—Healthy
- All supporting services—Healthy

### Outstanding Items for Follow-up

1. Frontend `imagePullSecrets`—the kubectl patch will drift on next sync. The frontend subchart needs fixing to read from `imagePullSecrets` in values.
2. Vault naming inconsistency—standardise `spicedb_pre_shared_key` vs `spicedb_preshared_key` across all Vault paths.
3. Parent OutOfSync—will likely clear once certificates finishes. If not, one more sync should do it.

Solid session—you untangled a lot today.

---

kubectl get certificates -n lca-prd-2 NAME READY SECRET AGE fitfile-lca False fitfile-lca-tls 3m28s

---

Not ready. Check why:

And check the certificate request:

Likely either the ClusterIssuer/Issuer isn't set up yet, or the DNS-01 challenge is pending—which could be tied to the Cloudflare API token secret we saw earlier (that one uses double escaping via cert-manager's `extras-objects.yaml`). If the token is empty, the ACME challenge can't complete.

---

kubectl describe certificate fitfile-lca -n lca-prd-2 | grep -A 10 'Events\\|Conditions\\|Status' Status: Conditions: Last Transition Time: 2026-03-03T19:57:17Z Message: Issuing certificate as Secret does not exist Observed Generation: 1 Reason: DoesNotExist Status: False Type: Ready Last Transition Time: 2026-03-03T19:57:18Z Message: Issuing certificate as Secret does not exist Observed Generation: 1 Reason: DoesNotExist Status: True Type: Issuing Next Private Key Secret Name: fitfile-lca-wkdz4 Events: Type Reason Age From Message ---- ------ ---- ---- ------- Normal Issuing 4m1s cert-manager-certificates-trigger Issuing certificate as Secret does not exist Normal Generated 4m1s cert-manager-certificates-key-manager Stored new private key in temporary Secret resource "fitfile-lca-wkdz4" Normal Requested 4m1s cert-manager-certificates-request-manager Created new CertificateRequest resource "fitfile-lca-1" kubectl get certificaterequest -n lca-prd-2 kubectl get challenges -n lca-prd-2 NAME APPROVED DENIED READY ISSUER REQUESTER AGE fitfile-lca-1 True False letsencrypt-prod system:serviceaccount:cert-manager:cert-manager 4m23s NAME STATE DOMAIN AGE fitfile-lca-1-3793982414-760861233 pending lca-prd-2.privatelink.fitfile.net 4m16s

---

Challenge is pending. Let's check if the Cloudflare API token is populated:

And check the challenge details:

If the API token is empty (0 bytes), it's the same VSO issue—cert-manager's `extras-objects.yaml` adds a `tpl` pass, so it needs double escaping (which we preserved). But the token may still not have synced.

---

kubectl get secret cloudflare-issuer-api-token -n cert-manager -o jsonpath='{.data.api-token}' | base64 -d | wc -c 0 ➜ terraform kubectl describe challenge fitfile-lca-1-3793982414-760861233 -n lca-prd-2 Name: fitfile-lca-1-3793982414-760861233 Namespace: lca-prd-2 Labels: <none> Annotations: <none> API Version: acme.cert-manager.io/v1 Kind: Challenge Metadata: Creation Timestamp: 2026-03-03T19:57:25Z Finalizers: acme.cert-manager.io/finalizer Generation: 1 Owner References: API Version: acme.cert-manager.io/v1 Block Owner Deletion: true Controller: true Kind: Order Name: fitfile-lca-1-3793982414 UID: a77cc833-2d27-49c9-892c-2c1464bd14e5 Resource Version: 8260434 UID: 04a73d5e-5354-4fa0-b3c7-b13d238ed428 Spec: Authorization URL: [https://acme-v02.api.letsencrypt.org/acme/authz/3113620302/667571402322](https://acme-v02.api.letsencrypt.org/acme/authz/3113620302/667571402322) Dns Name: lca-prd-2.privatelink.fitfile.net Issuer Ref: Kind: ClusterIssuer Name: letsencrypt-prod Key: UxspenclGA2rawq00tjDV7hdljTbE2Ixl3avC\_0O76g Solver: dns01: Cloudflare: API Token Secret Ref: Key: api-token Name: cloudflare-issuer-api-token Token: AZWbdIeJTuHN-5s5viS9-zGc9ZDn7AhJEDsSLn3PwPU Type: DNS-01 URL: [https://acme-v02.api.letsencrypt.org/acme/chall/3113620302/667571402322/f5tuOw](https://acme-v02.api.letsencrypt.org/acme/chall/3113620302/667571402322/f5tuOw) Wildcard: false Status: Presented: false Processing: true Reason: error instantiating cloudflare challenge solver: no Cloudflare credential has been given (can be either an API key or an API token) State: pending Events: Type Reason Age From Message ---- ------ ---- ---- ------- Normal Started 4m59s cert-manager-challenges Challenge scheduled for processing Warning PresentError 2m28s (x6 over 4m53s) cert-manager-challenges Error presenting challenge: error instantiating cloudflare challenge solver: no Cloudflare credential has been given (can be either an API key or an API token)

---

Empty Cloudflare token—same VSO pattern. Let's check the VaultStaticSecret in cert-manager's namespace:

And check if VSO can auth from the cert-manager namespace:

The cert-manager VaultStaticSecret is created via `extras-objects.yaml` with `tpl`, so the double escaping should produce valid VSO templates. But if there's no VaultAuth in cert-manager's namespace, VSO can't reach Vault to fetch the value.

---

kubectl get vaultstaticsecret -n cert-manager kubectl get vaultstaticsecret cloudflare-issuer-api-token -n cert-manager -o yaml NAME AGE cloudflare-issuer-api-token 26h apiVersion: secrets.hashicorp.com/v1beta1 kind: VaultStaticSecret metadata: annotations: argocd.argoproj.io/tracking-id: cert-manager:secrets.hashicorp.com/VaultStaticSecret:cert-manager/cloudflare-issuer-api-token kubectl.kubernetes.io/last-applied-configuration: | {"apiVersion":"secrets.hashicorp.com/v1beta1","kind":"VaultStaticSecret","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"cert-manager:secrets.hashicorp.com/VaultStaticSecret:cert-manager/cloudflare-issuer-api-token"},"name":"cloudflare-issuer-api-token","namespace":"cert-manager"},"spec":{"destination":{"create":true,"name":"cloudflare-issuer-api-token","transformation":{"excludes":\[".\*"\],"templates":{"api-token":{"text":"{{ get.Secrets \\"api-token\\" }}"}}}},"hmacSecretData":true,"mount":"secrets","namespace":"admin/deployments/lca-prd-2","path":"cloudflare","refreshAfter":null,"rolloutRestartTargets":\[\],"type":"kv-v2","vaultAuthRef":"default"}} creationTimestamp: "2026-03-02T17:33:33Z" finalizers: - vaultstaticsecret.secrets.hashicorp.com/finalizer generation: 3 name: cloudflare-issuer-api-token namespace: cert-manager resourceVersion: "7526346" uid: 365b83cf-f498-405f-8f0f-e2129a9f86e2 spec: destination: create: true name: cloudflare-issuer-api-token overwrite: false transformation: excludes: -.\* templates: api-token: text: '{{ get.Secrets "api-token" }}' hmacSecretData: true mount: secrets namespace: admin/deployments/lca-prd-2 path: cloudflare rolloutRestartTargets: \[\] type: kv-v2 vaultAuthRef: default status: lastGeneration: 3 secretMAC: 9MBxXL8AR5xOMi1p669wUAttYUB0wgp6vWy6Nb3nnUI= ➜ terraform kubectl get vaultauth -n cert-manager NAME AGE default 7d10h

---

The CR looks correct—valid VSO template, VaultAuth exists, secretMAC is set. But the value is empty. Check what keys actually exist at the cloudflare Vault path:

The template references `api-token` (with a hyphen). If the Vault key is `api_token` (underscore) or something else, VSO silently returns empty—same pattern as the `spicedb_pre_shared_key` issue.

---

vault kv get -namespace=admin/deployments/lca-prd-2 secrets/cloudflare ===== Secret Path ===== secrets/data/cloudflare ======= Metadata ======= Key Value --- ----- created\_time 2026-03-02T17:59:13.459358872Z custom\_metadata <nil> deletion\_time n/a destroyed false version 1 ====== Data ====== Key Value --- ----- api\_token \_kqbKU8j2KkRDP7D9Gl-hT2Yx

---

Same story. Vault has `api_token` (underscore), template references `api-token` (hyphen).

Two options—fix in Vault or fix in the values file. Vault is quicker:

Then force VSO to pick it up:

Once the token is populated, cert-manager should retry the challenge automatically. Watch it:

You're collecting a nice list of naming mismatches to standardise once this deployment is stable.

---

kubectl delete secret cloudflare-issuer-api-token -n cert-manager sleep 15 kubectl get secret cloudflare-issuer-api-token -n cert-manager -o jsonpath='{.data.api-token}' | base64 -d | wc -c secret "cloudflare-issuer-api-token" deleted from cert-manager namespace 25 ➜ terraform kubectl get challenges -n lca-prd-2 -w NAME STATE DOMAIN AGE fitfile-lca-1-3793982414-760861233 pending lca-prd-2.privatelink.fitfile.net 8m9s

---

Token populated. The challenge may take a minute or two for cert-manager to retry and for DNS propagation. Give it a few minutes, then check:

While we wait—here's your naming mismatch hit list to clean up when things are stable:

Both caused silent empty values from VSO with no errors logged.

---

kubectl get certificates -n lca-prd-2 kubectl get applications -n argocd NAME READY SECRET AGE fitfile-lca False fitfile-lca-tls 9m14s NAME SYNC STATUS HEALTH STATUS argo-workflows Synced Healthy blob-csi-driver Synced Healthy cert-manager Synced Healthy certificates Synced Progressing ff-lca-prd-2 OutOfSync Progressing ff-lca-prd-2-ffcloud-service Synced Healthy ff-lca-prd-2-fitconnect Synced Healthy ff-lca-prd-2-frontend Synced Healthy ff-lca-prd-2-minio Synced Healthy ff-lca-prd-2-mongodb-b17ef Synced Healthy ff-lca-prd-2-postgresql Synced Healthy ff-lca-prd-2-workflow-templates Synced Healthy ff-lca-prd-2-workflows-api Synced Healthy grafana-k8s-monitoring Synced Healthy prometheus-operator-crds Synced Healthy spicedb Synced Healthy

---

Still pending. Check if the challenge is progressing now with the token:

DNS-01 challenges can take a few minutes for propagation. If the events still show the "no Cloudflare credential" error, cert-manager may need a restart to pick up the new secret:

---

kubectl describe challenge fitfile-lca-1-3793982414-760861233 -n lca-prd-2 | tail -15 Processing: true Reason: while attempting to find Zones for domain \_acme-challenge.lca-prd-2.privatelink.fitfile.net. while querying the Cloudflare API for GET "/zones?name=\_acme-challenge.lca-prd-2.privatelink.fitfile.net" Error: 6003: Invalid request headers<- 6111: Invalid format for Authorization header State: pending Events: Type Reason Age From Message ---- ------ ---- ---- ------- Normal Started 10m cert-manager-challenges Challenge scheduled for processing Warning PresentError 5m1s (x7 over 10m) cert-manager-challenges Error presenting challenge: error instantiating cloudflare challenge solver: no Cloudflare credential has been given (can be either an API key or an API token) Warning PresentError 11s cert-manager-challenges Error presenting challenge: while attempting to find Zones for domain \_acme-challenge.lca-prd-2.privatelink.fitfile.net. while querying the Cloudflare API for GET "/zones?name=\_acme-challenge.lca-prd-2.privatelink.fitfile.net": Get " [https://api.cloudflare.com/client/v4/zones?name=\_acme-challenge.lca-prd-2.privatelink.fitfile.net](https://api.cloudflare.com/client/v4/zones?name=_acme-challenge.lca-prd-2.privatelink.fitfile.net) ": context canceled Warning PresentError 2s cert-manager-challenges Error presenting challenge: while attempting to find Zones for domain \_acme-challenge.lca-prd-2.privatelink.fitfile.net. while querying the Cloudflare API for GET "/zones?name=\_acme-challenge.lca-prd-2.privatelink.fitfile.net" Error: 6003: Invalid request headers<- 6111: Invalid format for Authorization header ➜ terraform kubectl describe challenge fitfile-lca-1-3793982414-760861233 -n lca-prd-2 | tail -15 Processing: true Reason: while attempting to find Zones for domain \_acme-challenge.lca-prd-2.privatelink.fitfile.net. while querying the Cloudflare API for GET "/zones?name=\_acme-challenge.lca-prd-2.privatelink.fitfile.net" Error: 6003: Invalid request headers<- 6111: Invalid format for Authorization header State: pending Events: Type Reason Age From Message ---- ------ ---- ---- ------- Normal Started 10m cert-manager-challenges Challenge scheduled for processing Warning PresentError 5m5s (x7 over 10m) cert-manager-challenges Error presenting challenge: error instantiating cloudflare challenge solver: no Cloudflare credential has been given (can be either an API key or an API token) Warning PresentError 15s cert-manager-challenges Error presenting challenge: while attempting to find Zones for domain \_acme-challenge.lca-prd-2.privatelink.fitfile.net. while querying the Cloudflare API for GET "/zones?name=\_acme-challenge.lca-prd-2.privatelink.fitfile.net": Get " [https://api.cloudflare.com/client/v4/zones?name=\_acme-challenge.lca-prd-2.privatelink.fitfile.net](https://api.cloudflare.com/client/v4/zones?name=_acme-challenge.lca-prd-2.privatelink.fitfile.net) ": context canceled Warning PresentError 2s (x2 over 6s) cert-manager-challenges Error presenting challenge: while attempting to find Zones for domain \_acme-challenge.lca-prd-2.privatelink.fitfile.net. while querying the Cloudflare API for GET "/zones?name=\_acme-challenge.lca-prd-2.privatelink.fitfile.net" Error: 6003: Invalid request headers<- 6111: Invalid format for Authorization header

---

Progress—it's now using the token (no more "no credential" error), but Cloudflare is rejecting it with "Invalid format for Authorization header". Let's check the actual token value:

The value from Vault was `_kqbKU8j2KkRDP7D9Gl-hT2Yx`—that's only 25 characters and starts with an underscore. Cloudflare API tokens are typically 40 characters. This looks truncated or wrong.

Is this the correct Cloudflare API token? Can you verify it in the Cloudflare dashboard, or check if a valid token exists elsewhere in your setup—perhaps another deployment's Vault path has the correct one?

---

you were correct. I have now updated it

---

Force the refresh:

Then restart cert-manager to clear the cached bad token:

Watch the challenge:

---

kubectl get challenges -n lca-prd-2 -w NAME STATE DOMAIN AGE fitfile-lca-1-3793982414-760861233 pending lca-prd-2.privatelink.fitfile.net 14m ^C% ➜ terraform kubectl describe challenge fitfile-lca-1-3793982414-760861233 -n lca-prd-2 | tail -15 Presented: true Processing: true Reason: Waiting for DNS-01 challenge propagation: Could not determine authoritative nameservers for "\_acme-challenge.lca-prd-2.privatelink.fitfile.net." State: pending Events: Type Reason Age From Message ---- ------ ---- ---- ------- Normal Started 16m cert-manager-challenges Challenge scheduled for processing Warning PresentError 11m (x7 over 16m) cert-manager-challenges Error presenting challenge: error instantiating cloudflare challenge solver: no Cloudflare credential has been given (can be either an API key or an API token) Warning PresentError 6m25s cert-manager-challenges Error presenting challenge: while attempting to find Zones for domain \_acme-challenge.lca-prd-2.privatelink.fitfile.net. while querying the Cloudflare API for GET "/zones?name=\_acme-challenge.lca-prd-2.privatelink.fitfile.net": Get " [https://api.cloudflare.com/client/v4/zones?name=\_acme-challenge.lca-prd-2.privatelink.fitfile.net](https://api.cloudflare.com/client/v4/zones?name=_acme-challenge.lca-prd-2.privatelink.fitfile.net) ": context canceled Warning PresentError 3m55s (x5 over 6m16s) cert-manager-challenges Error presenting challenge: while attempting to find Zones for domain \_acme-challenge.lca-prd-2.privatelink.fitfile.net. while querying the Cloudflare API for GET "/zones?name=\_acme-challenge.lca-prd-2.privatelink.fitfile.net" Error: 6003: Invalid request headers<- 6111: Invalid format for Authorization header Normal Presented 3m14s cert-manager-challenges Presented challenge using DNS-01 challenge mechanism

---

Good progress—the challenge was presented successfully (the TXT record is now in Cloudflare). It's just waiting for DNS propagation. The "Could not determine authoritative nameservers" message is common with `privatelink` subdomains since they have non-standard NS delegation.

This can take a few minutes. Give it 2-3 minutes and check:

If it stays stuck on the nameserver resolution, cert-manager may need recursive nameserver configuration to resolve it. You can check if other deployments use custom DNS settings for cert-manager:

Look for `--dns01-recursive-nameservers`—if it's not set, adding `--dns01-recursive-nameservers=1.1.1.1:53` can help with privatelink domains.

---

kubectl get deployment cert-manager -n cert-manager -o jsonpath='{.spec.template.spec.containers\[0\].args}' | tr ',' '\\n' \["--v=2" "--cluster-resource-namespace=$(POD\_NAMESPACE)" "--leader-election-namespace=kube-system" "--acme-http01-solver-image=fitfileregistry.azurecr.io/jetstack/cert-manager-acmesolver:v1.18.2" "--max-concurrent-challenges=60"\]%

---

No recursive nameservers set. That's why it can't resolve the privatelink domain. Patch it:

This tells cert-manager to use Cloudflare/Google public DNS instead of trying to find authoritative nameservers for the privatelink domain. The pod will restart automatically. Then watch:

Once the challenge completes, the certificate should flip to Ready and the whole stack settles.

---

it is now Normal Presented 9m50s cert-manager-challenges Presented challenge using DNS-01 challenge mechanism

---

Still waiting on propagation. Check the current state:

Also verify the TXT record actually exists:

If the TXT record is there, cert-manager should validate it shortly. If it's not resolving, the zone setup in Cloudflare may need checking—the `privatelink.fitfile.net` subdomain may not be delegated to Cloudflare.

---

nslookup -type=TXT \_acme-challenge.lca-prd-2.privatelink.fitfile.net 1.1.1.1 Server: 1.1.1.1 Address: 1.1.1.1#53 Non-authoritative answer: \_acme-challenge.lca-prd-2.privatelink.fitfile.net text = "UxspenclGA2rawq00tjDV7hdljTbE2Ixl3avC\_0O76g" Authoritative answers can be found from: ➜ terraform kubectl describe challenge fitfile-lca-1-3793982414-760861233 -n lca-prd-2 | tail -15 Presented: true Processing: true Reason: Waiting for DNS-01 challenge propagation: Could not determine authoritative nameservers for "\_acme-challenge.lca-prd-2.privatelink.fitfile.net." State: pending Events: Type Reason Age From Message ---- ------ ---- ---- ------- Normal Started 23m cert-manager-challenges Challenge scheduled for processing Warning PresentError 18m (x7 over 23m) cert-manager-challenges Error presenting challenge: error instantiating cloudflare challenge solver: no Cloudflare credential has been given (can be either an API key or an API token) Warning PresentError 13m cert-manager-challenges Error presenting challenge: while attempting to find Zones for domain \_acme-challenge.lca-prd-2.privatelink.fitfile.net. while querying the Cloudflare API for GET "/zones?name=\_acme-challenge.lca-prd-2.privatelink.fitfile.net": Get " [https://api.cloudflare.com/client/v4/zones?name=\_acme-challenge.lca-prd-2.privatelink.fitfile.net](https://api.cloudflare.com/client/v4/zones?name=_acme-challenge.lca-prd-2.privatelink.fitfile.net) ": context canceled Warning PresentError 11m (x5 over 13m) cert-manager-challenges Error presenting challenge: while attempting to find Zones for domain \_acme-challenge.lca-prd-2.privatelink.fitfile.net. while querying the Cloudflare API for GET "/zones?name=\_acme-challenge.lca-prd-2.privatelink.fitfile.net" Error: 6003: Invalid request headers<- 6111: Invalid format for Authorization header Normal Presented 10m cert-manager-challenges Presented challenge using DNS-01 challenge mechanism

---

The TXT record is live, but cert-manager is still trying to find authoritative nameservers instead of using the recursive ones we patched. Check if the patch took effect:

If the args are there, the pod may not have restarted yet:

If the pod is old (pre-patch), force it:

After the restart, the existing challenge may need to be retried. Delete it to force cert-manager to create a fresh one:

Then watch:

---

Events: Type Reason Age From Message ---- ------ ---- ---- ------- Normal Started 103s cert-manager-challenges Challenge scheduled for processing Normal Presented 94s cert-manager-challenges Presented challenge using DNS-01 challenge mechanism ➜ terraform kubectl get deployment cert-manager -n cert-manager -o jsonpath='{.spec.template.spec.containers\[0\].args}' | tr ',' '\\n' | grep recursive ➜ terraform

---

The patch didn't stick. Apply it again:

Verify it took:

If it shows the args, wait for the pod to restart and then delete the challenge to force a fresh attempt:

---

we are using argocd. is that resetting the confog as soon as we patch it?

---

Exactly. ArgoCD sees the drift and reverts it. The fix needs to go through the values file. In your values you have:

You need to add the extra args here. The cert-manager Helm chart accepts them under `extraArgs`:

Commit and push that, then sync the parent. This is also the same reason the frontend `imagePullSecrets` patch won't persist—that also needs to go through the chart/values properly.

However, if you want to unblock right now without waiting for a full commit/sync cycle, you can temporarily disable auto-sync on cert-manager to stop ArgoCD reverting the patch:

Then re-enable auto-sync after you've pushed the values file fix.

---

like this?

---

That looks right. Push it and sync. Meanwhile, unblock it now so you're not waiting:

Once the cert issues, push the values file change and re-sync to make it permanent.

---

ive pushed the changes to the vaules. how do we force sync and check the changes are picked up then get a new challenge going

---

Once the parent shows `Succeeded`:

---

\# 4. Verify the args landed kubectl get deployment cert-manager -n cert-manager -o jsonpath='{.spec.template.spec.containers\[0\].args}' | tr ',' '\\n' | grep recursive # 5. Delete stale challenges to force fresh attempt kubectl delete challenge -n lca-prd-2 --all # 6. Watch it kubectl get challenges -n lca-prd-2 -w "--dns01-recursive-nameservers=1.1.1.1:53 "--dns01-recursive-nameservers-only" challenge.acme.cert-manager.io "fitfile-lca-1-3793982414-760861233" deleted from lca-prd-2 namespace NAME STATE DOMAIN AGE fitfile-lca-1-3793982414-760861233 lca-prd-2.privatelink.fitfile.net 0s fitfile-lca-1-3793982414-760861233 lca-prd-2.privatelink.fitfile.net 0s fitfile-lca-1-3793982414-760861233 lca-prd-2.privatelink.fitfile.net 0s fitfile-lca-1-3793982414-760861233 valid lca-prd-2.privatelink.fitfile.net 0s fitfile-lca-1-3793982414-760861233 valid lca-prd-2.privatelink.fitfile.net 0s fitfile-lca-1-3793982414-760861233 valid lca-prd-2.privatelink.fitfile.net 1s fitfile-lca-1-3793982414-760861233 valid lca-prd-2.privatelink.fitfile.net 1s ^C%

---

---

kubectl get certificates -n lca-prd-2 kubectl get applications -n argocd NAME READY SECRET AGE fitfile-lca True fitfile-lca-tls 39m NAME SYNC STATUS HEALTH STATUS argo-workflows Synced Healthy blob-csi-driver Synced Healthy cert-manager Synced Healthy certificates Synced Healthy ff-lca-prd-2 OutOfSync Healthy ff-lca-prd-2-ffcloud-service Synced Healthy ff-lca-prd-2-fitconnect Synced Healthy ff-lca-prd-2-frontend Synced Healthy ff-lca-prd-2-minio Synced Healthy ff-lca-prd-2-mongodb-b17ef Synced Healthy ff-lca-prd-2-postgresql Synced Healthy ff-lca-prd-2-workflow-templates Synced Healthy ff-lca-prd-2-workflows-api Synced Healthy grafana-k8s-monitoring Synced Healthy prometheus-operator-crds Synced Healthy spicedb Synced Healthy

---

Everything Healthy, certificate Ready. The parent `OutOfSync` is just the frontend `imagePullSecrets` drift from the kubectl patch earlier. That's cosmetic for now.

One last sync should clear it, but it'll revert the frontend patch. To make it permanent, add `imagePullSecrets` support to the frontend chart—but that's a separate task for another day.

### What We Fixed Today

### Still Outstanding

1. Frontend `imagePullSecrets`—needs fixing in the Helm chart so it persists through syncs
2. Vault naming standardisation—`pre_shared` vs `preshared`, `api_token` vs `api-token`
3. Parent OutOfSync—will clear once the frontend chart fix is in place

Solid work getting through all of that.

---

i now what to check the frontend. we need to use curl. how do i find the hostnames and urls that are configured

---

And for the full details:

From your values file, the expected URLs are:

- Frontend:`https://lca-prd-2.privatelink.fitfile.net/fitfile`
- Fitconnect:`https://lca-prd-2.privatelink.fitfile.net/fitconnect`
- FFCloud:`https://lca-prd-2.privatelink.fitfile.net/ffcloud`

Since it's a privatelink domain, you'll need to curl from within the cluster or a machine that can resolve it:

If it doesn't resolve from your machine, curl from inside the cluster:

---

we also need to validate the certs

---

Frontend is up—HTTP 200 with full FITFILE HTML. The TLS info from the curl output already shows:

- Subject:`CN=lca-prd-2.privatelink.fitfile.net`
- Issuer: Let's Encrypt R12
- Valid: Mar 3 2026 → Jun 1 2026
- Protocol: TLSv1.3 / TLS\_AES\_256\_GCM\_SHA384

The `unable to get local issuer certificate` warning is just the local machine missing the Let's Encrypt R12 intermediate—not a real problem. Validate the full chain properly:

And check from the browser's perspective with openssl:

Also verify the other endpoints respond:

The cert looks clean. The whole stack is live.

---

curl -v [https://lca-prd-2.privatelink.fitfile.net/fitfile](https://lca-prd-2.privatelink.fitfile.net/fitfile) 2>&1 | grep -E 'subject:|issuer:|expire|verify' \* TLSv1.3 (IN), TLS handshake, CERT verify (15): \* subject: CN=lca-prd-2.privatelink.fitfile.net \* expire date: Jun 1 19:35:10 2026 GMT \* issuer: C=US; O=Let's Encrypt; CN=R12 \* SSL certificate verify ok. ➜ terraform openssl s\_client -connect lca-prd-2.privatelink.fitfile.net:443 -servername lca-prd-2.privatelink.fitfile.net </dev/null 2>/dev/null | openssl x509 -noout -text | grep -E 'Issuer:|Subject:|Not Before|Not After|DNS:' Issuer: C = US, O = Let's Encrypt, CN = R12 Not Before: Mar 3 19:35:11 2026 GMT Not After: Jun 1 19:35:10 2026 GMT Subject: CN = lca-prd-2.privatelink.fitfile.net DNS:lca-prd-2.privatelink.fitfile.net ➜ terraform curl -sk -o /dev/null -w '%{http\_code}' [https://lca-prd-2.privatelink.fitfile.net/fitconnect](https://lca-prd-2.privatelink.fitfile.net/fitconnect) curl -sk -o /dev/null -w '%{http\_code}' [https://lca-prd-2.privatelink.fitfile.net/ffcloud](https://lca-prd-2.privatelink.fitfile.net/ffcloud) 200200%

---

All green. Certificate validates cleanly, all three endpoints returning 200. The `lca-prd-2` deployment is live.

### Cleanup To-do when You Have a Quiet Moment

1. Frontend `imagePullSecrets`—kubectl patch will revert on next sync. Needs a chart fix.
2. Vault naming—standardise `spicedb_pre_shared_key` → `spicedb_preshared_key` in the `application` path, and `api_token` → `api-token` in `cloudflare`.
3. Parent OutOfSync—one final sync after the frontend chart fix should clear it completely.

Well fought, Leon. That was a proper session.
