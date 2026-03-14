---
captured: "2026-02-16T09:38:15+00:00 2026-02-16T09:38:15+00:00"
created: 2026-02-16T09:38:20+00:00
modified: 2026-02-27T09:19:55+00:00
source: "https://chatgpt.com/c/698d94e7-8b44-838f-a453-242fd665f004"
status: "processing"
tags: ["input", 1, 2, 5, failure, success]
title: HEAD Kubectl Debugging Commands
type: "head"
---

## Raw Output / Content

give me the kubectl commands to debug kubectl get pods -n hie-test-34 NAME READY STATUS RESTARTS AGE hie-test-34-ffcloud-service-5bd9f95cf9-z4mz5 0/3 Init:CrashLoopBackOff 179 (14s ago) 15h hie-test-34-ffcloud-service-6767db44c7-64fbb 0/3 Init:CrashLoopBackOff 196 (2m6s ago) 16h hie-test-34-fitconnect-ftc-5f59c5686-qx6fz 0/1 CrashLoopBackOff 195 (4m9s ago) 16h hie-test-34-fitconnect-ftc-6f7d9dc8b4-5chrz 0/1 CrashLoopBackOff 178 (112s ago) 15h hie-test-34-minio-6b9779bb4b-gnsb8 1/1 Running 0 16h hie-test-34-minio-provisioning-88sn8 0/1 Completed 0 16h hie-test-34-mongodb-b17ef-0 2/2 Running 0 16h hie-test-34-mongodb-b17ef-arbiter-0 1/1 Running 0 16h hie-test-34-postgresql-0 1/1 Running 0 16h workflows-api-5bd448f79-78szp 1/1 Running 0 16h

---

You've got two different failure modes here:

- `Init:CrashLoopBackOff` → an init container is failing before the app even starts
- `CrashLoopBackOff` → main container starts, then dies repeatedly

You debug these slightly differently.

---

## 1️⃣ Start With a Wide View (Events Tell You A Lot)

Look for:

- image pull errors
- secret/config mount failures
- DNS / connection errors
- permission denied
- OOMKilled

---

## 2️⃣ Describe One of the Failing Pods (This Is Critical)

Pick one pod from each type.

### For the Init Failure

### For the Crashing App

Scroll to the bottom—the `Events:` section usually contains the real cause.

---

## 3️⃣ Find Which Container Is Actually Failing

List containers (including init containers):

This tells you which container name to target with logs.

---

## 4️⃣ Get Logs From the Init Container (Most People Miss This)

Because this is an Init crash, you must specify the init container:

If it's looping fast, get the _previous_ crash:

👉 `--previous` is essential for CrashLoop debugging.

---

## 5️⃣ Now Debug the Normal CrashLoop Container

First get container names:

Then:

---

## 6️⃣ If Logs Are Empty → It's Dying Before Logging

Check exit code:

Common meanings:

| Exit Code | Meaning |
| --- | --- |
| 137 | OOMKilled |
| 1 | App error |
| 126 | Permission denied |
| 127 | Entrypoint missing |
| 139 | Segfault (bad native lib) |

---

## 7️⃣ Check Environment / Secrets (VERY Common Cause)

Init containers often fail due to missing config:

Then verify referenced secrets/configmaps exist:

---

## 8️⃣ Check If It's Waiting On Mongo / Postgres (You Have Both Running)

These stacks often include a migration init container that waits for DB readiness and fails.

Test connectivity manually by launching a debug shell in the namespace:

Then inside:

If DNS fails → it's a service naming issue.

If connect fails → readiness / auth issue.

---

## 9️⃣ See the Actual Init Script (This Is Often the Root Cause)

Dump the pod spec:

Look at:

These scripts frequently contain:

- migrations
- bucket creation (MinIO)
- schema validation
- vault pulls
- broken wait loops

---

## 🔎 10️⃣ If You Suspect a Bad Deployment Rollout

Check what changed:

Rollback fast if needed:

---

## 🧠 Based on Your Stack, Most Likely Causes

Given:

- Mongo ✅
- Postgres ✅
- MinIO ✅
- Provisioning job completed ✅

Your failures are _very likely_:

- migration init container failing auth to DB
- wrong secret injected
- MinIO bucket already exists → script exits non-zero
- TLS/env mismatch between services

---

## If You Paste Back These 3 Things, I Can Pinpoint It

Run and share:

That will expose the real failure immediately.

---

kubectl get events -n hie-test-34 --sort-by=.metadata.creationTimestamp LAST SEEN TYPE REASON OBJECT MESSAGE 96s Normal SecretRotated vaultstaticsecret/s3-export-secret Secret synced 101s Normal SecretRotated vaultstaticsecret/workflows-secrets Secret synced 2m52s Normal Pulled pod/hie-test-34-ffcloud-service-6767db44c7-64fbb Container image "fitfileregistry.azurecr.io/ffcloud-service:1.0.752" already present on machine 4m56s Normal Pulled pod/hie-test-34-fitconnect-ftc-5f59c5686-qx6fz Container image "fitfileregistry.azurecr.io/fitconnect-service:1.0.694" already present on machine 14s Warning BackOff pod/hie-test-34-ffcloud-service-6767db44c7-64fbb Back-off restarting failed container hie-test-34-ffcloud-service-init-db in pod hie-test-34-ffcloud-service-6767db44c7-64fbb\_hie-test-34(051c929a-dc9d-4cbc-a6bf-c4f9c4853946) 14s Warning BackOff pod/hie-test-34-fitconnect-ftc-5f59c5686-qx6fz Back-off restarting failed container hie-test-34-fitconnect-ftc in pod hie-test-34-fitconnect-ftc-5f59c5686-qx6fz\_hie-test-34(5afa8e47-8915-4471-9218-41794f6e1bbb) 60s Normal Pulled pod/hie-test-34-ffcloud-service-5bd9f95cf9-z4mz5 Container image "fitfileregistry.azurecr.io/ffcloud-service:1.0.752" already present on machine 2m5s Warning BackOff pod/hie-test-34-ffcloud-service-5bd9f95cf9-z4mz5 Back-off restarting failed container hie-test-34-ffcloud-service-init-db in pod hie-test-34-ffcloud-service-5bd9f95cf9-z4mz5\_hie-test-34(0efda23e-2a86-48b6-bb27-48669affc32c) 2m39s Normal Pulled pod/hie-test-34-fitconnect-ftc-6f7d9dc8b4-5chrz Container image "fitfileregistry.azurecr.io/fitconnect-service:1.0.694" already present on machine 37s Warning BackOff pod/hie-test-34-fitconnect-ftc-6f7d9dc8b4-5chrz Back-off restarting failed container hie-test-34-fitconnect-ftc in pod hie-test-34-fitconnect-ftc-6f7d9dc8b4-5chrz\_hie-test-34(1bc208cd-1f3e-45ce-8d77-64f7a5e34811) 37m Normal Created pod/hie-test-34-ffcloud-service-5bd9f95cf9-z4mz5 Created container: hie-test-34-ffcloud-service-init-db 30m Normal Created pod/hie-test-34-fitconnect-ftc-5f59c5686-qx6fz Created container: hie-test-34-fitconnect-ftc awsadmin@ip-10-66-2-4:~/terraform$ kubectl describe pod hie-test-34-ffcloud-service-5bd9f95cf9-z4mz5 -n hie-test-34 Name: hie-test-34-ffcloud-service-5bd9f95cf9-z4mz5 Namespace: hie-test-34 Priority: 0 Service Account: default Node: ip-10-66-5-187.eu-west-2.compute.internal/10.66.5.187 Start Time: Wed, 11 Feb 2026 17:50:55 +0000 Labels: app=hie-test-34-ffcloud-service pod-template-hash=5bd9f95cf9 Annotations: vso.secrets.hashicorp.com/restartedAt: 2026-02-11T17:50:54Z Status: Pending IP: 10.66.5.68 IPs: IP: 10.66.5.68 Controlled By: ReplicaSet/hie-test-34-ffcloud-service-5bd9f95cf9 Init Containers: hie-test-34-ffcloud-service-init-db: Container ID: containerd://6803365c41810b7cd613ca0047944de4b65ce94f8e3a78141d667606642573f1 Image: fitfileregistry.azurecr.io/ffcloud-service:1.0.752 Image ID: fitfileregistry.azurecr.io/ffcloud-service@sha256:d949bfe3fc61cc5f28cefd8f8c0cc0e3c4c83ce50c4da3de19540499ef09be51 Port: <none> Host Port: <none> Command: /bin/ash Args: -c set -e; set -o pipefail; yarn db:migrate:remote:up; yarn run init; State: Waiting Reason: CrashLoopBackOff Last State: Terminated Reason: Error Exit Code: 1 Started: Thu, 12 Feb 2026 08:52:18 +0000 Finished: Thu, 12 Feb 2026 08:52:21 +0000 Ready: False Restart Count: 179 Environment: NODE\_ENV: production FITFILE\_ENV: production TENANT\_SIGNING\_PUBLIC\_KEY: <set to the key 'public.crt' in secret 'fitfile-rsa-private-key'> Optional: true LOAD\_DEFINITION\_PATH: /config/load\_definition.json Mounts: /config from config (ro) /secrets from ffcloud-secrets (ro) /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-spk8m (ro) Containers: hie-test-34-ffcloud-service: Container ID: Image: fitfileregistry.azurecr.io/ffcloud-service:1.0.752 Image ID: Port: 4000/TCP (http) Host Port: 0/TCP (http) State: Waiting Reason: PodInitializing Ready: False Restart Count: 0 Requests: cpu: 100m Liveness: http-get http://:4000/ffcloud/readyz%3FhealthServiceName=FitConnectHostsHealthService&healthServiceName=MongoDBConnectionHealthService&healthServiceName=Auth0PingHealthService&healthServiceName=SpiceDbSchemaConnectionHealthService delay=15s timeout=12s period=15s success=1 failure=3 Readiness: http-get http://:4000/ffcloud/readyz%3FhealthServiceName=FitConnectHostsHealthService&healthServiceName=MongoDBConnectionHealthService&healthServiceName=Auth0PingHealthService&healthServiceName=SpiceDbSchemaConnectionHealthService delay=15s timeout=12s period=15s success=1 failure=3 Environment: NODE\_ENV: production FITFILE\_ENV: production LOAD\_DEFINITION\_PATH: /config/load\_definition.json Mounts: /config from config (ro) /secrets from ffcloud-secrets (ro) /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-spk8m (ro) hie-test-34-ffcloud-service-cli: Container ID: Image: fitfileregistry.azurecr.io/ffcloud-cli:1.0.49 Image ID: Port: <none> Host Port: <none> State: Waiting Reason: PodInitializing Ready: False Restart Count: 0 Environment: NODE\_ENV: production FITFILE\_ENV: production Mounts: /config from cli-config (ro) /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-spk8m (ro) scheduler: Container ID: Image: fitfileregistry.azurecr.io/scheduler-service:1.0.319 Image ID: Port: 4001/TCP Host Port: 0/TCP State: Waiting Reason: PodInitializing Ready: False Restart Count: 0 Environment: NODE\_ENV: production FITFILE\_ENV: production Mounts: /config from scheduler-config (ro) /secrets from ffcloud-secrets (ro) /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-spk8m (ro) Conditions: Type Status PodReadyToStartContainers True Initialized False Ready False ContainersReady False PodScheduled True Volumes: ffcloud-secrets: Type: Secret (a volume populated by a Secret) SecretName: ffcloud Optional: false config: Type: Projected (a volume that contains injected data from multiple sources) ConfigMapName: hie-test-34-ffcloud-service-config-018d3159a4f3949ddce5def71d09 Optional: false ConfigMapName: ffcloud-load-definition Optional: false cli-config: Type: Projected (a volume that contains injected data from multiple sources) ConfigMapName: hie-test-34-ffcloud-service-cli-config-ec35c472fc0b3d71b957ddc0 Optional: false scheduler-config: Type: Projected (a volume that contains injected data from multiple sources) ConfigMapName: hie-test-34-ffcloud-service-scheduler-config-678212ccf453f519d0 Optional: false kube-api-access-spk8m: Type: Projected (a volume that contains injected data from multiple sources) TokenExpirationSeconds: 3607 ConfigMapName: kube-root-ca.crt Optional: false DownwardAPI: true QoS Class: Burstable Node-Selectors: <none> Tolerations: node.kubernetes.io/not-ready:NoExecute op=Exists for 300s node.kubernetes.io/unreachable:NoExecute op=Exists for 300s Events: Type Reason Age From Message ---- ------ ---- ---- ------- Normal Created 37m (x173 over 15h) kubelet Created container: hie-test-34-ffcloud-service-init-db Warning BackOff 2m17s (x4094 over 15h) kubelet Back-off restarting failed container hie-test-34-ffcloud-service-init-db in pod hie-test-34-ffcloud-service-5bd9f95cf9-z4mz5\_hie-test-34(0efda23e-2a86-48b6-bb27-48669affc32c) Normal Pulled 72s (x180 over 15h) kubelet Container image "fitfileregistry.azurecr.io/ffcloud-service:1.0.752" already present on machine awsadmin@ip-10-66-2-4:~/terraform$ kubectl describe pod hie-test-34-fitconnect-ftc-5f59c5686-qx6fz -n hie-test-34 Name: hie-test-34-fitconnect-ftc-5f59c5686-qx6fz Namespace: hie-test-34 Priority: 0 Service Account: default Node: ip-10-66-5-187.eu-west-2.compute.internal/10.66.5.187 Start Time: Wed, 11 Feb 2026 16:22:16 +0000 Labels: app=hie-test-34-fitconnect-ftc pod-template-hash=5f59c5686 Annotations: <none> Status: Running IP: 10.66.5.206 IPs: IP: 10.66.5.206 Controlled By: ReplicaSet/hie-test-34-fitconnect-ftc-5f59c5686 Init Containers: hie-test-34-fitconnect-ftc-init: Container ID: containerd://c23d2008d54abbcad3db59791f1ade8b9e7f2e1352773f87e8598901d7671872 Image: fitfileregistry.azurecr.io/fitconnect-service:1.0.694 Image ID: fitfileregistry.azurecr.io/fitconnect-service@sha256:03ee98701cc69dad05431091b92f681effc72e19056fc805e36d46b6e262656f Port: <none> Host Port: <none> Command: yarn db:migrate:remote:up State: Terminated Reason: Completed Exit Code: 0 Started: Wed, 11 Feb 2026 16:22:36 +0000 Finished: Wed, 11 Feb 2026 16:22:39 +0000 Ready: True Restart Count: 0 Environment: NODE\_ENV: production FITFILE\_ENV: production LOAD\_DEFINITION\_PATH: /config/load\_definition.json Mounts: /config from config (ro) /secrets from fitconnect-secrets (ro) /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-2jswm (ro) Containers: hie-test-34-fitconnect-ftc: Container ID: containerd://525c251c8e02c83cdf916522dda94c2b6e78e048979d7f0ed6d25d43180f6eed Image: fitfileregistry.azurecr.io/fitconnect-service:1.0.694 Image ID: fitfileregistry.azurecr.io/fitconnect-service@sha256:03ee98701cc69dad05431091b92f681effc72e19056fc805e36d46b6e262656f Port: 4000/TCP (http) Host Port: 0/TCP (http) Command: node --require./instrumentation.js server.js State: Terminated Reason: Error Exit Code: 1 Started: Thu, 12 Feb 2026 08:53:31 +0000 Finished: Thu, 12 Feb 2026 08:53:35 +0000 Last State: Terminated Reason: Error Exit Code: 1 Started: Thu, 12 Feb 2026 08:48:22 +0000 Finished: Thu, 12 Feb 2026 08:48:26 +0000 Ready: False Restart Count: 196 Requests: cpu: 100m Liveness: http-get http://:4000/fitconnect/readyz%3FhealthServiceName=TenantDocumentHealthService&healthServiceName=SpiceDbSchemaConnectionHealthService&healthServiceName=MongoDBConnectionHealthService&healthServiceName=PostgresDBConnectionHealthService&healthServiceName=MinioS3ConnectionHealthService&healthServiceName=WorkflowsAPIConnectionHealthService&healthServiceName=Auth0PingHealthService delay=15s timeout=12s period=15s success=1 failure=3 Readiness: http-get http://:4000/fitconnect/readyz%3FhealthServiceName=TenantDocumentHealthService&healthServiceName=SpiceDbSchemaConnectionHealthService&healthServiceName=MongoDBConnectionHealthService&healthServiceName=PostgresDBConnectionHealthService&healthServiceName=MinioS3ConnectionHealthService&healthServiceName=WorkflowsAPIConnectionHealthService&healthServiceName=Auth0PingHealthService delay=15s timeout=12s period=15s success=1 failure=3 Environment: NODE\_ENV: production FITFILE\_ENV: production LOAD\_DEFINITION\_PATH: /config/load\_definition.json Mounts: /config from config (ro) /secrets from fitconnect-secrets (ro) /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-2jswm (ro) Conditions: Type Status PodReadyToStartContainers True Initialized True Ready False ContainersReady False PodScheduled True Volumes: fitconnect-secrets: Type: Secret (a volume populated by a Secret) SecretName: fitconnect Optional: false config: Type: Projected (a volume that contains injected data from multiple sources) ConfigMapName: hie-test-34-fitconnect-ftc-config-ce7e43b5d512c3d01a5cafdd2586b Optional: false ConfigMapName: fitconnect-load-definition Optional: false kube-api-access-2jswm: Type: Projected (a volume that contains injected data from multiple sources) TokenExpirationSeconds: 3607 ConfigMapName: kube-root-ca.crt Optional: false DownwardAPI: true QoS Class: Burstable Node-Selectors: <none> Tolerations: node.kubernetes.io/not-ready:NoExecute op=Exists for 300s node.kubernetes.io/unreachable:NoExecute op=Exists for 300s Events: Type Reason Age From Message ---- ------ ---- ---- ------- Normal Created 31m (x191 over 16h) kubelet Created container: hie-test-34-fitconnect-ftc Warning BackOff 37s (x4604 over 16h) kubelet Back-off restarting failed container hie-test-34-fitconnect-ftc in pod hie-test-34-fitconnect-ftc-5f59c5686-qx6fz\_hie-test-34(5afa8e47-8915-4471-9218-41794f6e1bbb) Normal Pulled 10s (x197 over 16h) kubelet Container image "fitfileregistry.azurecr.io/fitconnect-service:1.0.694" already present on machine awsadmin@ip-10-66-2-4:~/terraform$ kubectl get pod hie-test-34-ffcloud-service-5bd9f95cf9-z4mz5 \\ -n hie-test-34 \\ -o jsonpath='{.spec.initContainers\[\*\].name}{"\\n"}{.spec.containers\[\*\].name}{"\\n"}' hie-test-34-ffcloud-service-init-db hie-test-34-ffcloud-service hie-test-34-ffcloud-service-cli scheduler awsadmin@ip-10-66-2-4:~/terraform$ kubectl logs hie-test-34-ffcloud-service-5bd9f95cf9-z4mz5 \\ -c <INIT\_CONTAINER\_NAME> \\ -n hie-test-34 -bash: INIT\_CONTAINER\_NAME: No such file or directory awsadmin@ip-10-66-2-4:~/terraform$ kubectl logs hie-test-34-ffcloud-service-5bd9f95cf9-z4mz5 -c hie-test-34-ffcloud-service-init-db -n hie-test-34 yarn run v1.22.22 $ node db-migrations/nosql/migration-runner.js up {"name":"MongoMigrationManager","hostname":"hie-test-34-ffcloud-service-5bd9f95cf9-z4mz5","pid":28,"level":20,"msg":"Checking migrations for ffcloud","time":"2026-02-12T08:52:19.878Z","v":0} - Migrations up ⚠ No migrations found Done in 1.49s. yarn run v1.22.22 $ yarn node scripts/init.js {"name":"ffcloud","hostname":"hie-test-34-ffcloud-service-5bd9f95cf9-z4mz5","pid":71,"level":30,"event":"Mongo Client Instantiated","msg":"","time":"2026-02-12T08:52:21.557Z","src":{"file":"/app/infra/repositories/MongoClientSingleton.js","line":20,"func":"getInstance"},"v":0} {"name":"ffcloud","hostname":"hie-test-34-ffcloud-service-5bd9f95cf9-z4mz5","pid":71,"level":30,"msg":"EventMediator: Starting up","time":"2026-02-12T08:52:21.656Z","src":{"file":"/app/infra/mediator/mongodb/MongoDBChangeStreamEventMediator.js","line":121},"v":0,"correlationId":"a51c5eed-f314-4baf-a58b-ac35f78543cf","userId":{"userId":"auth0|61f3e4d81a44500069ebc39d"}} {"name":"ffcloud","hostname":"hie-test-34-ffcloud-service-5bd9f95cf9-z4mz5","pid":71,"level":30,"msg":"EventMediator: Starting watch on Events change stream","time":"2026-02-12T08:52:21.669Z","src":{"file":"/app/infra/mediator/mongodb/MongoDBChangeStreamEventMediator.js","line":135},"v":0,"correlationId":"a51c5eed-f314-4baf-a58b-ac35f78543cf","userId":{"userId":"auth0|61f3e4d81a44500069ebc39d"}} {"name":"ffcloud","hostname":"hie-test-34-ffcloud-service-5bd9f95cf9-z4mz5","pid":71,"level":30,"msg":"EventMediator: Change stream ready","time":"2026-02-12T08:52:21.673Z","src":{"file":"/app/infra/mediator/mongodb/MongoDBChangeStreamEventMediator.js","line":153},"v":0,"correlationId":"a51c5eed-f314-4baf-a58b-ac35f78543cf","userId":{"userId":"auth0|61f3e4d81a44500069ebc39d"}} AuthTokenDecodeError: Unable to get Auth0 access token at getAuthHeader (/app/node\_modules/@fitfile/service-common/dist/infra/clients/auth0.js:92:19) at process.processTicksAndRejections (node:internal/process/task\_queues:105:5) at async Object.getUsersInfo (/app/node\_modules/@fitfile/service-common/dist/infra/clients/auth0.js:96:29) { \[cause\]: AxiosError: Request failed with status code 401 at settle (/app/node\_modules/axios/dist/node/axios.cjs:2097:12) at IncomingMessage.handleStreamEnd (/app/node\_modules/axios/dist/node/axios.cjs:3305:11) at IncomingMessage.emit (node:events:536:35) at endReadableNT (node:internal/streams/readable:1698:12) at process.processTicksAndRejections (node:internal/process/task\_queues:90:21) at Axios.request (/app/node\_modules/axios/dist/node/axios.cjs:4483:41) at process.processTicksAndRejections (node:internal/process/task\_queues:105:5) at async getAuthHeader (/app/node\_modules/@fitfile/service-common/dist/infra/clients/auth0.js:81:26) at async Object.getUsersInfo (/app/node\_modules/@fitfile/service-common/dist/infra/clients/auth0.js:96:29) { code: 'ERR\_BAD\_REQUEST', config: { transitional: \[Object\], adapter: \[AsyncFunction: adapter\], transformRequest: \[Array\], transformResponse: \[Array\], timeout: 0, xsrfCookieName: 'XSRF-TOKEN', xsrfHeaderName: 'X-XSRF-TOKEN', maxContentLength: -1, maxBodyLength: -1, env: \[Object\], validateStatus: \[Function: validateStatus\], headers: \[Object \[AxiosHeaders\]\], caching: \[Object\], method: 'post', url: 'https://fitfile-prod.eu.auth0.com/oauth/token', data: '{"client\_id":"","client\_secret":"","audience":"https://fitfile-prod.eu.auth0.com/api/v2/","grant\_type":"client\_credentials"}', allowAbsoluteUrls: true }, request: ClientRequest { \_events: \[Object: null prototype\], \_eventsCount: 7, \_maxListeners: undefined, outputData: \[\], outputSize: 0, writable: true, destroyed: true, \_last: false, chunkedEncoding: false, shouldKeepAlive: true, maxRequestsOnConnectionReached: false, \_defaultKeepAlive: true, useChunkedEncodingByDefault: true, sendDate: false, \_removedConnection: false, \_removedContLen: false, \_removedTE: false, strictContentLength: false, \_contentLength: '124', \_hasBody: true, \_trailer: '', finished: true, \_headerSent: true, \_closed: true, \_header: 'POST /oauth/token HTTP/1.1\\r\\n' + 'Accept: application/json, text/plain, \*/\*\\r\\n' + 'Content-Type: application/json\\r\\n' + 'x-correlation-id: a51c5eed-f314-4baf-a58b-ac35f78543cf\\r\\n' + 'User-Agent: axios/1.12.2\\r\\n' + 'Content-Length: 124\\r\\n' + 'Accept-Encoding: gzip, compress, deflate, br\\r\\n' + 'Host: fitfile-prod.eu.auth0.com\\r\\n' + 'Connection: keep-alive\\r\\n' + '\\r\\n', \_keepAliveTimeout: 0, \_onPendingData: \[Function: nop\], agent: \[Agent\], socketPath: undefined, method: 'POST', maxHeaderSize: undefined, insecureHTTPParser: undefined, joinDuplicateHeaders: undefined, path: '/oauth/token', \_ended: true, res: \[IncomingMessage\], aborted: false, timeoutCb: null, upgradeOrConnect: false, parser: null, maxHeadersCount: null, reusedSocket: false, host: 'fitfile-prod.eu.auth0.com', protocol: 'https:', \_redirectable: \[Writable\], \[Symbol(shapeMode)\]: false, \[Symbol(kCapture)\]: false, \[Symbol(kBytesWritten)\]: 0, \[Symbol(kNeedDrain)\]: false, \[Symbol(corked)\]: 0, \[Symbol(kChunkedBuffer)\]: \[\], \[Symbol(kChunkedLength)\]: 0, \[Symbol(kSocket)\]: \[TLSSocket\], \[Symbol(kOutHeaders)\]: \[Object: null prototype\], \[Symbol(errored)\]: null, \[Symbol(kHighWaterMark)\]: 65536, \[Symbol(kRejectNonStandardBodyWrites)\]: false, \[Symbol(kUniqueHeaders)\]: null }, response: { status: 401, statusText: 'Unauthorized', headers: \[Object \[AxiosHeaders\]\], config: \[Object\], request: \[ClientRequest\], data: \[Object\] }, status: 401 } } error Command failed. Exit code: 1 Command: /usr/local/bin/node Arguments: scripts/init.js Directory: /app Output: info Visit <https://yarnpkg.com/en/docs/cli/node> for documentation about this command. error Command failed with exit code 1. info Visit <https://yarnpkg.com/en/docs/cli/run> for documentation about this command. awsadmin@ip-10-66-2-4:~/terraform$ kubectl get pod hie-test-34-fitconnect-ftc-5f59c5686-qx6fz \\ -n hie-test-34 \\ -o jsonpath='{.spec.containers\[\*\].name}' hie-test-34-fitconnect-ftcawsadmin@kubectl get secrets -n hie-test-34get secrets -n hie-test-34 kubectl get configmaps -n hie-test-34 NAME TYPE DATA AGE ffcloud Opaque 7 16h fitconnect Opaque 7 16h fitfile-image-pull-secret kubernetes.io/dockerconfigjson 2 18h fitfile-rsa-private-key Opaque 3 16h minio Opaque 3 16h mongodb Opaque 3 16h postgresql Opaque 2 16h role-secrets Opaque 2 21h s3-export-secret Opaque 5 16h ude-secret Opaque 2 16h workflows-secrets Opaque 7 16h NAME DATA AGE artifact-repositories 1 16h ffcloud-load-definition 1 16h fitconnect-load-definition 1 16h hie-test-34-ffcloud-service-cli-config-ec35c472fc0b3d71b957ddc0 1 16h hie-test-34-ffcloud-service-config-018d3159a4f3949ddce5def71d09 1 16h hie-test-34-ffcloud-service-scheduler-config-678212ccf453f519d0 1 16h hie-test-34-fitconnect-ftc-config-ce7e43b5d512c3d01a5cafdd2586b 1 16h hie-test-34-minio-provisioning 1 16h hie-test-34-mongodb-b17ef-common-scripts 3 16h hie-test-34-mongodb-b17ef-scripts 2 16h hie-test-34-postgresql-init-scripts 1 16h kube-root-ca.crt 1 22h load-data-cli-load-definition 1 16h load-data-config 1 16h submit-mesh-request-load-definition 1 16h ude-scripts 1 16h

---

Nice, you've already got the smoking gun.

### ✅ Root Cause (from the Init Container logs)

Your `ffcloud-service` init container is failing here:

- `AuthTokenDecodeError: Unable to get Auth0 access token`
- Auth0 `/oauth/token` returns 401 Unauthorized
- The request body shows empty `client_id` and `client_secret`:

So the init script (`yarn run init`) is trying to talk to Auth0 using client credentials that are missing or not being read from secrets. Until that succeeds, the whole pod stays stuck in `Init:CrashLoopBackOff`.

Fitconnect is also crashing and likely for the same "missing Auth0 credentials" reason (but we still need its logs to confirm).

---

## The Exact Kubectl Commands You Need next

### 1) Confirm the Ffcloud Init Container is Reading Env Vars / Secrets

Dump the init container env + mounts from the live spec:

You're looking for env like `AUTH0_CLIENT_ID`, `AUTH0_CLIENT_SECRET`, domain, audience, etc—either as `env:` entries or mounted files under `/secrets`.

---

### 2) Inspect What's Actually inside the Mounted Secrets Directory

Because the pod never gets past init, use an ephemeral debug container attached to the same pod (best way to see the volumes):

Then inside:

If `/secrets` is empty or missing the expected filenames/keys, that's your issue.

(If your cluster doesn't allow `kubectl debug`, use the "copy the secret to stdout" commands below.)

---

### 3) Verify the Secret Keys Exist (names + Keys, without Printing values)

This shows which keys are in the `ffcloud` secret:

And same for fitconnect:

If you don't have `jq`:

You're checking: are there keys that correspond to Auth0 creds at all?

---

### 4) Check how the Secret is Being Consumed (envFrom Vs Volume files)

Search the pod spec for `ffcloud-secrets` usage:

And look for `envFrom:` or `valueFrom:`:

This tells you whether the app expects:

- env vars (secretKeyRef / envFrom), or
- files in `/secrets` (volume mount)

Right now the logs imply it _thinks_ it has creds but they're empty—classic "wrong key name" or "wrong file path" mismatch.

---

## Now Confirm Fitconnect's Crash Reason (very Likely Same problem)

### 5) Get Fitconnect Logs (previous crash)

If it's the same Auth0 401 / empty creds, you can fix both by correcting the secret injection once.

---

## What to Fix (once You Confirm with the Commands above)

You'll almost certainly find one of these:

- Auth0 secret keys exist but don't match what the container expects (e.g. `AUTH0_CLIENTID` vs `AUTH0_CLIENT_ID`)
- Secret is mounted, but the code expects env vars (or vice versa)
- You're hitting prod Auth0 (`fitfile-prod.eu.auth0.com`) from a test namespace and the secret contains non-prod creds (or empty placeholders)

---

## Fast "sanity check" Commands (minimal)

If you want the quickest path:

If you paste the `describe secret ffcloud` (just the Keys: section) and the `fitconnect --previous` logs, I'll tell you exactly which key/path mapping is wrong.

---

kubectl describe secret ffcloud -n hie-test-34 kubectl logs -n hie-test-34 hie-test-34-fitconnect-ftc-5f59c5686-qx6fz --previous kubectl get pod hie-test-34-ffcloud-service-5bd9f95cf9-z4mz5 -n hie-test-34 -o yaml | egrep -n "AUTH0|client|secret|audience|domain|envFrom|secretKeyRef" Name: ffcloud Namespace: hie-test-34 Labels: app.kubernetes.io/component=secret-sync app.kubernetes.io/managed-by=hashicorp-vso app.kubernetes.io/name=vault-secrets-operator secrets.hashicorp.com/vso-ownerRefUID=6c288162-f074-4c6e-beae-864241a3024e Annotations: <none> Type: Opaque Data ==== \_raw: 4856 bytes auth.json: 49 bytes cli-auth.json: 145 bytes mongodb: 149 bytes mongodb.json: 47 bytes postgresql.json: 49 bytes spicedb.json: 31 bytes Defaulted container "hie-test-34-fitconnect-ftc" out of: hie-test-34-fitconnect-ftc, hie-test-34-fitconnect-ftc-init (init) {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-5f59c5686-qx6fz","pid":1,"level":30,"event":"application\_start","msg":"Initialising FITConnect application","time":"2026-02-12T08:58:43.166Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-5f59c5686-qx6fz","pid":1,"level":30,"event":"Mongo Client Instantiated","msg":"","time":"2026-02-12T08:58:43.185Z","v":0} (node:1) \[DEP0040\] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead. (Use `node --trace-deprecation …` to show where the warning was created) {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-5f59c5686-qx6fz","pid":1,"level":30,"msg":"Setting default connections","time":"2026-02-12T08:58:43.261Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-5f59c5686-qx6fz","pid":1,"level":50,"err":{"message":"\[\\n {\\n \\"code\\": \\"invalid\_union\\",\\n \\"errors\\": \[\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"PostgreSQL\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"PostgreSQL\\\\\\"\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"databaseName\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"MSSQL\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"MSSQL\\\\\\"\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"databaseName\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n}\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"MySQL\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"MySQL\\\\\\"\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"databaseName\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"ElasticSearch\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"ElasticSearch\\\\\\"\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"FITConnect\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"FITConnect\\\\\\"\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"endpoint\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"tenantId\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"audience\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected stringto have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"Project\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"Project\\\\\\"\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"FileUpload\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"FileUpload\\\\\\"\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"path\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n },\\n {\\n \\"expected\\": \\"number\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"version\\"\\n \],\\n \\"message\\": \\"Invalid input: expected number, received undefined\\"\\n },\\n {\\n \\"expected\\": \\"array\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"datasets\\"\\n \],\\n \\"message\\": \\"Invalid input: expected array, received undefined\\"\\n }\\n \]\\n \],\\n \\"path\\": \[\],\\n \\"message\\": \\"Invalid input\\"\\n }\\n\]","name":"ZodError","stack":"ZodError: \[\\n {\\n \\"code\\": \\"invalid\_union\\",\\n \\"errors\\": \[\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"PostgreSQL\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"PostgreSQL\\\\\\"\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"databaseName\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"MSSQL\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"MSSQL\\\\\\"\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"databaseName\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"MySQL\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"MySQL\\\\\\"\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"databaseName\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"ElasticSearch\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"ElasticSearch\\\\\\"\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"FITConnect\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"FITConnect\\\\\\"\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"endpoint\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"tenantId\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"audience\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"Project\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"Project\\\\\\"\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"FileUpload\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"FileUpload\\\\\\"\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"path\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n },\\n {\\n \\"expected\\": \\"number\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"version\\"\\n \],\\n \\"message\\": \\"Invalid input: expected number, received undefined\\"\\n },\\n {\\n \\"expected\\": \\"array\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"datasets\\"\\n \],\\n \\"message\\": \\"Invalid input: expected array, received undefined\\"\\n }\\n \]\\n \],\\n \\"path\\": \[\],\\n \\"message\\": \\"Invalid input\\"\\n }\\n\]\\n at DataSourceFactory.create (/app/domain/dataSource/dataSources/DataSourceFactory.js:19:45)\\n at DataSourceRepo.seedDefaultConnections (/app/infra/repositories/datasource/DataSourceRepo.js:121:74)\\n at Object.defaultBuildInfrastructure \[as buildInfrastructure\] (/app/infra/index.js:22:35)\\n at process.processTicksAndRejections (node:internal/process/task\_queues:105:5)\\n at async KoaApp.init (/app/KoaApp.js:30:31)\\n at async /app/server.js:18:5"},"msg":"\[\\n {\\n \\"code\\": \\"invalid\_union\\",\\n \\"errors\\": \[\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"PostgreSQL\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"PostgreSQL\\\\\\"\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"databaseName\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"MSSQL\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"MSSQL\\\\\\"\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"databaseName\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"MySQL\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"MySQL\\\\\\"\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"databaseName\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"ElasticSearch\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"ElasticSearch\\\\\\"\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"FITConnect\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"FITConnect\\\\\\"\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"endpoint\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"tenantId\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"audience\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"Project\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"Project\\\\\\"\\"\\n }\\n \],\\n \[\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"creatorId\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"origin\\": \\"string\\",\\n \\"code\\": \\"too\_small\\",\\n \\"minimum\\": 1,\\n \\"inclusive\\": true,\\n \\"path\\": \[\\n \\"lastUpdatedById\\"\\n \],\\n \\"message\\": \\"Too small: expected string to have >=1 characters\\"\\n },\\n {\\n \\"code\\": \\"invalid\_value\\",\\n \\"values\\": \[\\n \\"FileUpload\\"\\n \],\\n \\"path\\": \[\\n \\"type\\"\\n \],\\n \\"message\\": \\"Invalid input: expected \\\\\\"FileUpload\\\\\\"\\"\\n },\\n {\\n \\"expected\\": \\"string\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"path\\"\\n \],\\n \\"message\\": \\"Invalid input: expected string, received undefined\\"\\n },\\n {\\n \\"expected\\": \\"number\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"version\\"\\n \],\\n \\"message\\": \\"Invalid input: expected number, received undefined\\"\\n },\\n {\\n \\"expected\\": \\"array\\",\\n \\"code\\": \\"invalid\_type\\",\\n \\"path\\": \[\\n \\"datasets\\"\\n \],\\n \\"message\\": \\"Invalid input: expected array, received undefined\\"\\n }\\n \]\\n \],\\n \\"path\\": \[\],\\n \\"message\\": \\"Invalid input\\"\\n }\\n\]","time":"2026-02-12T08:58:43.272Z","v":0} /app/domain/dataSource/dataSources/DataSourceFactory.js:23 throw new Error(`DataSourceFactory: Unable to create DataSource from connection with id (${connectionDetails.connectionId}). Connection document is invalid.`, { cause: e }); ^ Error: DataSourceFactory: Unable to create DataSource from connection with id (19b4d43f-a264-429d-864c-9fb32ef750b5). Connection document is invalid. at DataSourceFactory.create (/app/domain/dataSource/dataSources/DataSourceFactory.js:23:19) at DataSourceRepo.seedDefaultConnections (/app/infra/repositories/datasource/DataSourceRepo.js:121:74)… 3 lines matching cause stack trace… at async /app/server.js:18:5 { \[cause\]: ZodError: \[{ "code": "invalid\_union", "errors": \[\[{ "origin": "string", "code": "too\_small", "minimum": 1, "inclusive": true, "path": \["creatorId" \], "message": "Too small: expected string to have >=1 characters" }, { "origin": "string", "code": "too\_small", "minimum": 1, "inclusive": true, "path": \["lastUpdatedById" \], "message": "Too small: expected string to have >=1 characters" }, { "code": "invalid\_value", "values": \["PostgreSQL" \], "path": \["type" \], "message": "Invalid input: expected \\"PostgreSQL\\"" }, { "expected": "string", "code": "invalid\_type", "path": \["databaseName" \], "message": "Invalid input: expected string, received undefined" } \], \[{ "origin": "string", "code": "too\_small", "minimum": 1, "inclusive": true, "path": \["creatorId" \], "message": "Too small: expected string to have >=1 characters" }, { "origin": "string", "code": "too\_small", "minimum": 1, "inclusive": true, "path": \["lastUpdatedById" \], "message": "Too small: expected string to have >=1 characters" }, { "code": "invalid\_value", "values": \["MSSQL" \], "path": \["type" \], "message": "Invalid input: expected \\"MSSQL\\"" }, { "expected": "string", "code": "invalid\_type", "path": \["databaseName" \], "message": "Invalid input: expected string, received undefined" } \], \[{ "origin": "string", "code": "too\_small", "minimum": 1, "inclusive": true, "path": \["creatorId" \], "message": "Too small: expected string to have >=1 characters" }, { "origin": "string", "code": "too\_small", "minimum": 1, "inclusive": true, "path": \["lastUpdatedById" \], "message": "Too small: expected string to have >=1 characters" }, { "code": "invalid\_value", "values": \["MySQL" \], "path": \["type" \], "message": "Invalid input: expected \\"MySQL\\"" }, { "expected": "string", "code": "invalid\_type", "path": \["databaseName" \], "message": "Invalid input: expected string, received undefined" } \], \[{ "origin": "string", "code": "too\_small", "minimum": 1, "inclusive": true, "path": \["creatorId" \], "message": "Too small: expected string to have >=1 characters" }, { "origin": "string", "code": "too\_small", "minimum": 1, "inclusive": true, "path": \["lastUpdatedById" \], "message": "Too small: expected string to have >=1 characters" }, { "code": "invalid\_value", "values": \["ElasticSearch" \], "path": \["type" \], "message": "Invalid input: expected \\"ElasticSearch\\"" } \], \[{ "origin": "string", "code": "too\_small", "minimum": 1, "inclusive": true, "path": \["creatorId" \], "message": "Too small: expected string to have >=1 characters" }, { "origin": "string", "code": "too\_small", "minimum": 1, "inclusive": true, "path": \["lastUpdatedById" \], "message": "Too small: expected string to have >=1 characters" } \], \[{ "origin": "string", "code": "too\_small", "minimum": 1, "inclusive": true, "path": \["creatorId" \], "message": "Too small: expected string to have >=1 characters" }, { "origin": "string", "code": "too\_small", "minimum": 1, "inclusive": true, "path": \["lastUpdatedById" \], "message": "Too small: expected string to have >=1 characters" }, { "code": "invalid\_value", "values": \["FITConnect" \], "path": \["type" \], "message": "Invalid input: expected \\"FITConnect\\"" }, { "expected": "string", "code": "invalid\_type", "path": \["endpoint" \], "message": "Invalid input: expected string, received undefined" }, { "expected": "string", "code": "invalid\_type", "path": \["tenantId" \], "message": "Invalid input: expected string, received undefined" }, { "expected": "string", "code": "invalid\_type", "path": \["audience" \], "message": "Invalid input: expected string, received undefined" } \], \[{ "origin": "string", "code": "too\_small", "minimum": 1, "inclusive": true, "path": \["creatorId" \], "message": "Too small: expected string to have >=1 characters" }, { "origin": "string", "code": "too\_small", "minimum": 1, "inclusive": true, "path": \["lastUpdatedById" \], "message": "Too small: expected string to have >=1 characters" }, { "code": "invalid\_value", "values": \["Project" \], "path": \["type" \], "message": "Invalid input: expected \\"Project\\"" } \], \[{ "origin": "string", "code": "too\_small", "minimum": 1, "inclusive": true, "path": \["creatorId" \], "message": "Too small: expected string to have >=1 characters" }, { "origin": "string", "code": "too\_small", "minimum": 1, "inclusive": true, "path": \["lastUpdatedById" \], "message": "Too small: expected string to have >=1 characters" }, { "code": "invalid\_value", "values": \["FileUpload" \], "path": \["type" \], "message": "Invalid input: expected \\"FileUpload\\"" }, { "expected": "string", "code": "invalid\_type", "path": \["path" \], "message": "Invalid input: expected string, received undefined" }, { "expected": "number", "code": "invalid\_type", "path": \["version" \], "message": "Invalid input: expected number, received undefined" }, { "expected": "array", "code": "invalid\_type", "path": \["datasets" \], "message": "Invalid input: expected array, received undefined" } \] \], "path": \[\], "message": "Invalid input" } \] at DataSourceFactory.create (/app/domain/dataSource/dataSources/DataSourceFactory.js:19:45) at DataSourceRepo.seedDefaultConnections (/app/infra/repositories/datasource/DataSourceRepo.js:121:74) at Object.defaultBuildInfrastructure \[as buildInfrastructure\] (/app/infra/index.js:22:35) at process.processTicksAndRejections (node:internal/process/task\_queues:105:5) at async KoaApp.init (/app/KoaApp.js:30:31) at async /app/server.js:18:5 } Node.js v22.13.1 5: vso.secrets.hashicorp.com/restartedAt: "2026-02-11T17:50:54Z" 65: - mountPath: /secrets 66: name: ffcloud-secrets 71: - mountPath: /var/run/secrets/kubernetes.io/serviceaccount 89: - mountPath: /var/run/secrets/kubernetes.io/serviceaccount 107: - mountPath: /secrets 108: name: ffcloud-secrets 113: - mountPath: /var/run/secrets/kubernetes.io/serviceaccount 131: - name: fitfile-image-pull-secret 149: secretKeyRef: 162: - mountPath: /secrets 163: name: ffcloud-secrets 168: - mountPath: /var/run/secrets/kubernetes.io/serviceaccount 190: - name: ffcloud-secrets 191: secret: 193: secretName: ffcloud 274: - mountPath: /secrets 275: name: ffcloud-secrets 282: - mountPath: /var/run/secrets/kubernetes.io/serviceaccount 301: - mountPath: /var/run/secrets/kubernetes.io/serviceaccount 316: - mountPath: /secrets 317: name: ffcloud-secrets 324: - mountPath: /var/run/secrets/kubernetes.io/serviceaccount 383: - mountPath: /secrets 384: name: ffcloud-secrets 391: - mountPath: /var/run/secrets/kubernetes.io/serviceaccount

---

Cool, this is now very clear: you've got two separate config problems.

## A) Ffcloud-service Init Crash: Auth0 Client Creds Are Missing

From your init logs earlier, the Auth0 token request had:

- `client_id: ""`
- `client_secret: ""`
- 401 from `https://fitfile-prod.eu.auth0.com/oauth/token`

And your `ffcloud` secret contains no obvious Auth0 keys, only:

- `auth.json` (49 bytes)
- `cli-auth.json`
- db config jsons (`mongodb.json`, `postgresql.json`, `spicedb.json`)
- `_raw`

So the container is probably expecting Auth0 creds either:

1. as env vars (`AUTH0_CLIENT_ID`, `AUTH0_CLIENT_SECRET`, etc.), but they're not set, or
2. in `/secrets/auth.json`, but that file is either missing fields / wrong structure / wrong path the code reads.

### Commands to Prove Which it is (and to See what the Pod is Actually getting)

#### 1) List the Secret Files as Mounted in the Pod (fast check)

Because you already mount `/secrets`, verify the filenames in the volume:

^^ that won't help because it's minio. You need a pod that mounts the `ffcloud` secret—but ffcloud pods are stuck in init so normal `exec` won't work.

Use kubectl debug on the stuck pod to inspect mounted files:

Then inside:

(If `cat` reveals sensitive info, just confirm whether `client_id` / `client_secret` are present and non-empty.)

#### 2) See if Any Env Vars Are Being Set from Secrets (likely not)

Right now your grep output shows mounts and one `secretKeyRef` somewhere, but not the matching lines.

Do this instead:

Search in that output for:

- `env:`
- `envFrom:`
- `secretKeyRef:`
- `AUTH0`

If there are no env vars, the code must be reading `/secrets/auth.json` (or `_raw`) and it's missing values.

#### 3) Confirm the Mounted Key-to-filename Mapping (super Common gotcha)

K8s secret key names become filenames. Your secret keys are `auth.json`, `cli-auth.json`, etc.

So these files should exist:

- `/secrets/auth.json`
- `/secrets/cli-auth.json`
- `/secrets/mongodb.json`
- `/secrets/postgresql.json`
- `/secrets/spicedb.json`

If the code expects `/secrets/auth0.json` or `/secrets/auth`, it will silently fail and fall back to empty strings.

---

## B) Fitconnect Crash: Invalid "connection document" (not Auth0)

Your fitconnect logs show a Zod schema validation failure while seeding default connections:

Key errors include missing/empty fields like:

- `creatorId` empty
- `lastUpdatedById` empty
- `databaseName` undefined
- and for FITConnect connection: `endpoint`, `tenantId`, `audience` are undefined

So fitconnect is reading some "default connections" config/document (likely from Mongo, or from a JSON config in `/config` or `/secrets`) and it's incomplete.

### Commands to Debug Fitconnect Config Source

#### 1) Dump the Fitconnect Configmap Contents

This is usually the easiest win:

Also:

Look for anything like:

- default connections
- seed data
- connection templates
- tenant config

#### 2) Inspect the Mounted /config and /secrets inside a Running Container (fitconnect Starts then Dies, but You Can Still Often Exec Briefly; if Not, Use debug)

Try:

If it restarts too fast and `exec` fails, use debug:

Then:

#### 3) Identify where that "connectionId" Document Lives (Mongo Vs file)

Because the error references a UUID connectionId, it smells like Mongo document.

Check which Mongo DB it's using from `/secrets/mongodb.json` (in fitconnect secret):

Then (if you can port-forward mongo and have creds) you can query the connection doc by ID—but we can avoid that until we see the configmaps and the secret file layout.

---

## What I'd Do next (minimal Steps, Highest signal)

### 1) Confirm Ffcloud Auth File Actually Has Client Creds

### 2) Dump the Fitconnect Configmap (this Likely Fixes the ZodError)

If you paste:

- the contents (or at least relevant sections) of `auth.json` (redact secrets), and
- that fitconnect configmap yaml

…I'll tell you exactly what key/path is wrong for Auth0 and which missing fields are causing the fitconnect seed failure.

---

the secrets are in hvp vault /v1/admin/deployments/hie-test-34/secrets/data/application with "cli\_auth0\_client\_secret" and "cli\_auth0\_client\_id" that vso should be getting

---

Got it—then the problem is 100% in the VSO → Kubernetes Secret mapping, not "Auth0 is down".

Your container is clearly trying to call Auth0 with empty `client_id` / `client_secret`, and your `ffcloud` k8s secret currently only has `auth.json` / `cli-auth.json` etc. That means VSO is either:

1. not fetching those Vault keys at all, or
2. fetching them but writing them under different key names / into `_raw`, or
3. fetching from the wrong path / wrong namespace / wrong auth, or
4. your app expects `auth.json` but VSO is providing `cli_auth0_client_id` and `cli_auth0_client_secret` (names mismatch).

Here are the kubectl commands that will tell you exactly which.

---

## 1) Find the VaultStaticSecret / VaultSecret Resource Backing Ffcloud

VSO stamped labels show it's managed by hashicorp-vso. List the CRs in the namespace:

If your cluster uses different CRD names, search by "vault":

---

## 2) Describe the VaultStaticSecret that Owns Ffcloud

(You have ownerRefUID on the k8s secret, but the easiest is just to find the CR with `destination.name: ffcloud`.)

Then find the one that writes `ffcloud`, and describe it:

What you're looking for in that output:

- the Vault path (should match `/v1/admin/deployments/hie-test-34/secrets/data/application` _or_ the VSO-equivalent logical path)
- any key selection / templates
- sync status / errors (auth denied, missing key, bad template, etc.)

---

## 3) Check what VSO Actually Synced (Kubernetes Secret Key names)

Right now `ffcloud` has:

- `auth.json` (49 bytes) ← suspiciously small
- `cli-auth.json` (145 bytes)
- plus DB jsons

No `cli_auth0_client_id` / `cli_auth0_client_secret`.

Let's confirm whether those strings exist anywhere in the secret (often they're in `_raw`):

Then search for the keys:

If that grep returns nothing, VSO isn't pulling them at all.

If it _does_ return them, you need to template them into `auth.json` / env vars.

---

## 4) Prove what the App Expects (file-based Vs env-based)

From your earlier logs, the payload was built as:

That suggests the code read config successfully enough to know the domain and audience, but got blank creds.

So it's probably reading a JSON file (like `/secrets/auth.json` or `/secrets/cli-auth.json`) and mapping fields.

Check what's inside those files in the k8s secret (don't paste secrets; just inspect locally):

You'll likely see the domain/audience set but `client_id` / `client_secret` missing.

---

## 5) The Actual Fix Pattern (what VSO Should Be doing)

Since Vault has keys named:

- `cli_auth0_client_id`
- `cli_auth0_client_secret`

…but the pod is consuming `/secrets/cli-auth.json` (or `/secrets/auth.json`), you need VSO to template a JSON file using those Vault fields.

Depending on your VSO version/config, this is typically one of:

- templated secret data (generate `cli-auth.json` from vault fields)
- direct key mapping (write `cli_auth0_client_id` as a secret key and change app to read it as env var)
- both (write both file + discrete keys)

---

## 6) Quick "smoking gun" Confirmation for You

Run this and tell me whether it prints anything:

- If nothing: VSO isn't fetching the Auth0 fields from that Vault path.
- If something: VSO is fetching them, but not materializing them into the keys the app reads (`auth.json` / `cli-auth.json`).

---

## Why auth.json Size (49 bytes) Matters

A 49-byte JSON is usually something like `{}` or `{"x":"y"}`—it's _way_ too small to contain Auth0 domain + audience + id + secret. So the file VSO is generating is almost certainly incomplete.

---

If you paste the `vaultstaticsecret -o yaml` for the one that writes `ffcloud` (redact tokens), I can point to the exact stanza that needs changing (path, key mapping, or template).

---

kubectl get vaultstaticsecrets -n hie-test-34 kubectl get vaultsecrets -n hie-test-34 kubectl get vaultauth -n hie-test-34 NAME AGE ffcloud 16h fitconnect 16h fitfile-rsa-private-key 16h minio 16h mongodb 16h postgresql 16h s3-export-secret 16h ude-secret 16h workflows-secrets 16h error: the server doesn't have a resource type "vaultsecrets" NAME AGE default 19h awsadmin@ip-10-66-2-4:~/terraform$ kubectl api-resources | grep -i vault hcpvaultsecretsapps secrets.hashicorp.com/v1beta1 true HCPVaultSecretsApp vaultauthglobals secrets.hashicorp.com/v1beta1 true VaultAuthGlobal vaultauths secrets.hashicorp.com/v1beta1 true VaultAuth vaultconnections secrets.hashicorp.com/v1beta1 true VaultConnection vaultdynamicsecrets secrets.hashicorp.com/v1beta1 true VaultDynamicSecret vaultpkisecrets secrets.hashicorp.com/v1beta1 true VaultPKISecret vaultstaticsecrets secrets.hashicorp.com/v1beta1 true VaultStaticSecret awsadmin@ip-10-66-2-4:~/terraform$ kubectl get vaultstaticsecrets -n hie-test-34 -o yaml | less awsadmin@ip-10-66-2-4:~/terraform$ kubectl get vaultstaticsecrets -n hie-test-34 -o yaml | less awsadmin@ip-10-66-2-4:~/terraform$ kubectl get vaultstaticsecrets -n hie-test-34 -o yaml apiVersion: v1 items: - apiVersion: secrets.hashicorp.com/v1beta1 kind: VaultStaticSecret metadata: annotations: argocd.argoproj.io/tracking-id: hie-test-34-ffcloud-service:secrets.hashicorp.com/VaultStaticSecret:hie-test-34/ffcloud kubectl.kubernetes.io/last-applied-configuration: | {"apiVersion":"secrets.hashicorp.com/v1beta1","kind":"VaultStaticSecret","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"hie-test-34-ffcloud-service:secrets.hashicorp.com/VaultStaticSecret:hie-test-34/ffcloud"},"name":"ffcloud","namespace":"hie-test-34"},"spec":{"destination":{"create":true,"name":"ffcloud","transformation":{"excludes":\[".\*"\],"templates":{"auth.json":{"text":"{\\"clientId\\":\\"{{ get.Secrets \\"auth0\_client\_id\\" }}\\",\\"clientSecret\\":\\"{{ get.Secrets \\"auth0\_client\_secret\\" }}\\", \\"audience\\": \\"{{ get.Secrets \\"auth0\_audience\\" }}\\"}"},"cli-auth.json":{"text":"{\\"clientId\\":\\"{{ get.Secrets \\"cli\_auth0\_client\_id\\" }}\\",\\"clientSecret\\":\\"{{ get.Secrets \\"cli\_auth0\_client\_secret\\" }}\\", \\"audience\\": \\"{{ get.Secrets \\"auth0\_audience\\" }}\\"}"},"mongodb":{"text":"mongodb://{{get.Secrets \\"mongodb\_username\\"}}:{{get.Secrets \\"mongodb\_password\\"}}@hie-test-34-mongodb-b17ef-0.hie-test-34-mongodb-b17ef-headless.hie-test-34.svc.cluster.local:27017/admin?replicaSet=rs0"},"mongodb.json":{"text":"{\\"password\\":\\"{{ get.Secrets \\"mongodb\_password\\" }}\\",\\"username\\":\\"{{ get.Secrets \\"mongodb\_username\\" }}\\"}"},"postgresql.json":{"text":"{\\"password\\":\\"{{get.Secrets \\"postgresql\_password\\"}}\\",\\"username\\":\\"{{get.Secrets \\"postgresql\_username\\"}}\\"}"},"spicedb.json":{"text":"{\\"preSharedKey\\":\\"{{ get.Secrets \\"spicedb\_pre\_shared\_key\\"}}\\"}"}}}},"hmacSecretData":true,"mount":"secrets","namespace":"admin/deployments/hie-test-34","path":"application","refreshAfter":"5m","rolloutRestartTargets":\[{"kind":"Deployment","name":"hie-test-34-ffcloud-service"}\],"type":"kv-v2","vaultAuthRef":"default"}} creationTimestamp: "2026-02-11T16:22:16Z" finalizers: - vaultstaticsecret.secrets.hashicorp.com/finalizer generation: 1 name: ffcloud namespace: hie-test-34 resourceVersion: "548614" uid: 6c288162-f074-4c6e-beae-864241a3024e spec: destination: create: true name: ffcloud overwrite: false transformation: excludes: -.\* templates: auth.json: text: '{"clientId":"{{ get.Secrets "auth0\_client\_id" }}","clientSecret":"{{ get.Secrets "auth0\_client\_secret" }}", "audience": "{{ get.Secrets "auth0\_audience" }}"}' cli-auth.json: text: '{"clientId":"{{ get.Secrets "cli\_auth0\_client\_id" }}","clientSecret":"{{ get.Secrets "cli\_auth0\_client\_secret" }}", "audience": "{{ get.Secrets "auth0\_audience" }}"}' mongodb: text: mongodb://{{get.Secrets "mongodb\_username"}}:{{get.Secrets "mongodb\_password"}}@hie-test-34-mongodb-b17ef-0.hie-test-34-mongodb-b17ef-headless.hie-test-34.svc.cluster.local:27017/admin?replicaSet=rs0 mongodb.json: text: '{"password":"{{ get.Secrets "mongodb\_password" }}","username":"{{ get.Secrets "mongodb\_username" }}"}' postgresql.json: text: '{"password":"{{get.Secrets "postgresql\_password"}}","username":"{{get.Secrets "postgresql\_username"}}"}' spicedb.json: text: '{"preSharedKey":"{{ get.Secrets "spicedb\_pre\_shared\_key"}}"}' hmacSecretData: true mount: secrets namespace: admin/deployments/hie-test-34 path: application refreshAfter: 5m rolloutRestartTargets: - kind: Deployment name: hie-test-34-ffcloud-service type: kv-v2 vaultAuthRef: default status: lastGeneration: 1 secretMAC: eNA7f6cTcGwqZeOSpEjyjb/adhf1utyDCxvqhLwW8uw= - apiVersion: secrets.hashicorp.com/v1beta1 kind: VaultStaticSecret metadata: annotations: argocd.argoproj.io/tracking-id: hie-test-34-fitconnect:secrets.hashicorp.com/VaultStaticSecret:hie-test-34/fitconnect kubectl.kubernetes.io/last-applied-configuration: | {"apiVersion":"secrets.hashicorp.com/v1beta1","kind":"VaultStaticSecret","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"hie-test-34-fitconnect:secrets.hashicorp.com/VaultStaticSecret:hie-test-34/fitconnect"},"name":"fitconnect","namespace":"hie-test-34"},"spec":{"destination":{"create":true,"name":"fitconnect","transformation":{"excludes":\[".\*"\],"templates":{"auth.json":{"text":"{\\"clientId\\":\\"{{ get.Secrets \\"auth0\_client\_id\\" }}\\",\\"clientSecret\\":\\"{{ get.Secrets \\"auth0\_client\_secret\\" }}\\", \\"audience\\": \\"{{ get.Secrets \\"auth0\_audience\\" }}\\"}"},"mongodb":{"text":"mongodb://{{get.Secrets \\"mongodb\_username\\"}}:{{get.Secrets \\"mongodb\_password\\"}}@hie-test-34-mongodb-b17ef-0.hie-test-34-mongodb-b17ef-headless.hie-test-34.svc.cluster.local:27017/admin?replicaSet=rs0"},"postgresql.json":{"text":"{\\"password\\":\\"{{get.Secrets \\"postgresql\_password\\"}}\\",\\"username\\":\\"{{get.Secrets \\"postgresql\_username\\"}}\\"}"},"s3-access-key":{"text":"{{ get.Secrets \\"s3\_access\_key\_id\\" }}"},"s3-secret-key":{"text":"{{ get.Secrets \\"s3\_secret\_access\_key\\" }}"},"spicedb.json":{"text":"{\\"preSharedKey\\":\\"{{ get.Secrets \\"spicedb\_pre\_shared\_key\\"}}\\"}"}}}},"hmacSecretData":true,"mount":"secrets","namespace":"admin/deployments/hie-test-34","path":"application","refreshAfter":"5m","rolloutRestartTargets":\[{"kind":"Deployment","name":"hie-test-34-fitconnect-ftc"}\],"type":"kv-v2","vaultAuthRef":"default"}} creationTimestamp: "2026-02-11T16:22:16Z" finalizers: - vaultstaticsecret.secrets.hashicorp.com/finalizer generation: 1 name: fitconnect namespace: hie-test-34 resourceVersion: "549087" uid: 99f95816-ab7c-43bd-85d0-98f907206400 spec: destination: create: true name: fitconnect overwrite: false transformation: excludes: -.\* templates: auth.json: text: '{"clientId":"{{ get.Secrets "auth0\_client\_id" }}","clientSecret":"{{ get.Secrets "auth0\_client\_secret" }}", "audience": "{{ get.Secrets "auth0\_audience" }}"}' mongodb: text: mongodb://{{get.Secrets "mongodb\_username"}}:{{get.Secrets "mongodb\_password"}}@hie-test-34-mongodb-b17ef-0.hie-test-34-mongodb-b17ef-headless.hie-test-34.svc.cluster.local:27017/admin?replicaSet=rs0 postgresql.json: text: '{"password":"{{get.Secrets "postgresql\_password"}}","username":"{{get.Secrets "postgresql\_username"}}"}' s3-access-key: text: '{{ get.Secrets "s3\_access\_key\_id" }}' s3-secret-key: text: '{{ get.Secrets "s3\_secret\_access\_key" }}' spicedb.json: text: '{"preSharedKey":"{{ get.Secrets "spicedb\_pre\_shared\_key"}}"}' hmacSecretData: true mount: secrets namespace: admin/deployments/hie-test-34 path: application refreshAfter: 5m rolloutRestartTargets: - kind: Deployment name: hie-test-34-fitconnect-ftc type: kv-v2 vaultAuthRef: default status: lastGeneration: 1 secretMAC: nR6kIcJx1Uoj+ezh/fpPlfyTELXL6CsnPMSH+xi+LEs= - apiVersion: secrets.hashicorp.com/v1beta1 kind: VaultStaticSecret metadata: annotations: argocd.argoproj.io/tracking-id: hie-test-34-workflow-templates:secrets.hashicorp.com/VaultStaticSecret:hie-test-34/fitfile-rsa-private-key kubectl.kubernetes.io/last-applied-configuration: | {"apiVersion":"secrets.hashicorp.com/v1beta1","kind":"VaultStaticSecret","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"hie-test-34-workflow-templates:secrets.hashicorp.com/VaultStaticSecret:hie-test-34/fitfile-rsa-private-key"},"name":"fitfile-rsa-private-key","namespace":"hie-test-34"},"spec":{"destination":{"create":true,"name":"fitfile-rsa-private-key","transformation":{"excludes":\[".\*"\],"templates":{"pkcs8.key":{"text":"{{get.Secrets \\"fitfile\_tenant\_pkcs8.key\\"}}"},"public.crt":{"text":"{{get.Secrets \\"fitfile\_tenant\_public.crt\\"}}"}}}},"hmacSecretData":true,"mount":"secrets","namespace":"admin/deployments/hie-test-34","path":"application","refreshAfter":null,"rolloutRestartTargets":\[\],"type":"kv-v2","vaultAuthRef":"default"}} creationTimestamp: "2026-02-11T16:21:16Z" finalizers: - vaultstaticsecret.secrets.hashicorp.com/finalizer generation: 3 name: fitfile-rsa-private-key namespace: hie-test-34 resourceVersion: "548038" uid: 7672d22d-7d3a-4032-9f6b-2f778ebaa08a spec: destination: create: true name: fitfile-rsa-private-key overwrite: false transformation: excludes: -.\* templates: pkcs8.key: text: '{{get.Secrets "fitfile\_tenant\_pkcs8.key"}}' public.crt: text: '{{get.Secrets "fitfile\_tenant\_public.crt"}}' hmacSecretData: true mount: secrets namespace: admin/deployments/hie-test-34 path: application rolloutRestartTargets: \[\] type: kv-v2 vaultAuthRef: default status: lastGeneration: 3 secretMAC: 6IeSKGO6mlIbYFXG93ZbVF4Lj6Lev0TcnVhCXPJH3Ow= - apiVersion: secrets.hashicorp.com/v1beta1 kind: VaultStaticSecret metadata: annotations: argocd.argoproj.io/tracking-id: hie-test-34-minio:secrets.hashicorp.com/VaultStaticSecret:hie-test-34/minio kubectl.kubernetes.io/last-applied-configuration: | {"apiVersion":"secrets.hashicorp.com/v1beta1","kind":"VaultStaticSecret","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"hie-test-34-minio:secrets.hashicorp.com/VaultStaticSecret:hie-test-34/minio"},"name":"minio","namespace":"hie-test-34"},"spec":{"destination":{"create":true,"name":"minio","transformation":{"excludes":\[".\*"\],"templates":{"root-password":{"text":"{{get.Secrets \\"s3\_secret\_access\_key\\"}}"},"root-user":{"text":"{{get.Secrets \\"s3\_access\_key\_id\\"}}"}}}},"hmacSecretData":true,"mount":"secrets","namespace":"admin/deployments/hie-test-34","path":"application","refreshAfter":null,"rolloutRestartTargets":\[\],"type":"kv-v2","vaultAuthRef":"default"}} creationTimestamp: "2026-02-11T16:20:36Z" finalizers: - vaultstaticsecret.secrets.hashicorp.com/finalizer generation: 3 name: minio namespace: hie-test-34 resourceVersion: "547893" uid: 5bd84f72-2ff8-44e8-b168-e9684231e458 spec: destination: create: true name: minio overwrite: false transformation: excludes: -.\* templates: root-password: text: '{{get.Secrets "s3\_secret\_access\_key"}}' root-user: text: '{{get.Secrets "s3\_access\_key\_id"}}' hmacSecretData: true mount: secrets namespace: admin/deployments/hie-test-34 path: application rolloutRestartTargets: \[\] type: kv-v2 vaultAuthRef: default status: lastGeneration: 3 secretMAC: woExbmorjlRybPXY7aQ8BHfDkOr5xAOCA2AcA6yzJRQ= - apiVersion: secrets.hashicorp.com/v1beta1 kind: VaultStaticSecret metadata: annotations: argocd.argoproj.io/tracking-id: hie-test-34-mongodb-b17ef:secrets.hashicorp.com/VaultStaticSecret:hie-test-34/mongodb kubectl.kubernetes.io/last-applied-configuration: | {"apiVersion":"secrets.hashicorp.com/v1beta1","kind":"VaultStaticSecret","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"hie-test-34-mongodb-b17ef:secrets.hashicorp.com/VaultStaticSecret:hie-test-34/mongodb"},"name":"mongodb","namespace":"hie-test-34"},"spec":{"destination":{"create":true,"name":"mongodb","transformation":{"excludes":\[".\*"\],"templates":{"mongodb-replica-set-key":{"text":"{{get.Secrets \\"mongodb\_replica\_set\_key\\"}}"},"mongodb-root-password":{"text":"{{get.Secrets \\"mongodb\_password\\"}}"}}}},"hmacSecretData":true,"mount":"secrets","namespace":"admin/deployments/hie-test-34","path":"application","refreshAfter":null,"rolloutRestartTargets":\[\],"type":"kv-v2","vaultAuthRef":"default"}} creationTimestamp: "2026-02-11T16:20:34Z" finalizers: - vaultstaticsecret.secrets.hashicorp.com/finalizer generation: 3 name: mongodb namespace: hie-test-34 resourceVersion: "548009" uid: c3781ff1-07c3-4952-b40e-2ac43a0a964e spec: destination: create: true name: mongodb overwrite: false transformation: excludes: -.\* templates: mongodb-replica-set-key: text: '{{get.Secrets "mongodb\_replica\_set\_key"}}' mongodb-root-password: text: '{{get.Secrets "mongodb\_password"}}' hmacSecretData: true mount: secrets namespace: admin/deployments/hie-test-34 path: application rolloutRestartTargets: \[\] type: kv-v2 vaultAuthRef: default status: lastGeneration: 3 secretMAC: Lyw8AgOl/qY9tWkbGDBCQb9qxmEMDH9z3C7sbs0rtHo= - apiVersion: secrets.hashicorp.com/v1beta1 kind: VaultStaticSecret metadata: annotations: argocd.argoproj.io/tracking-id: hie-test-34-postgresql:secrets.hashicorp.com/VaultStaticSecret:hie-test-34/postgresql kubectl.kubernetes.io/last-applied-configuration: | {"apiVersion":"secrets.hashicorp.com/v1beta1","kind":"VaultStaticSecret","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"hie-test-34-postgresql:secrets.hashicorp.com/VaultStaticSecret:hie-test-34/postgresql"},"name":"postgresql","namespace":"hie-test-34"},"spec":{"destination":{"create":true,"name":"postgresql","transformation":{"excludes":\[".\*"\],"templates":{"postgres-password":{"text":"{{get.Secrets \\"postgresql\_password\\"}}"}}}},"hmacSecretData":true,"mount":"secrets","namespace":"admin/deployments/hie-test-34","path":"application","refreshAfter":null,"rolloutRestartTargets":\[\],"type":"kv-v2","vaultAuthRef":"default"}} creationTimestamp: "2026-02-11T16:19:31Z" finalizers: - vaultstaticsecret.secrets.hashicorp.com/finalizer generation: 3 name: postgresql namespace: hie-test-34 resourceVersion: "547825" uid: b5f39284-6daa-44f0-b598-ac6437355763 spec: destination: create: true name: postgresql overwrite: false transformation: excludes: -.\* templates: postgres-password: text: '{{get.Secrets "postgresql\_password"}}' hmacSecretData: true mount: secrets namespace: admin/deployments/hie-test-34 path: application rolloutRestartTargets: \[\] type: kv-v2 vaultAuthRef: default status: lastGeneration: 3 secretMAC: cQyCwv5Ax/tSmHyga8mSbak8uOZl/OcdT6tzudEPp88= - apiVersion: secrets.hashicorp.com/v1beta1 kind: VaultStaticSecret metadata: annotations: argocd.argoproj.io/tracking-id: hie-test-34-workflow-templates:secrets.hashicorp.com/VaultStaticSecret:hie-test-34/s3-export-secret kubectl.kubernetes.io/last-applied-configuration: | {"apiVersion":"secrets.hashicorp.com/v1beta1","kind":"VaultStaticSecret","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"hie-test-34-workflow-templates:secrets.hashicorp.com/VaultStaticSecret:hie-test-34/s3-export-secret"},"name":"s3-export-secret","namespace":"hie-test-34"},"spec":{"destination":{"create":true,"name":"s3-export-secret","transformation":{"excludeRaw":true,"excludes":\[".\*"\],"templates":{"s3\_access\_key\_id":{"text":"{{get.Secrets \\"hie\_s3\_export\_access\_key\_id\\"}}"},"s3\_endpoint":{"text":"{{get.Secrets \\"hie\_s3\_export\_endpoint\\"}}"},"s3\_region":{"text":"{{get.Secrets \\"hie\_s3\_export\_aws\_region\\"}}"},"s3\_role\_arn":{"text":"{{get.Secrets \\"hie\_s3\_export\_role\_arn\\"}}"},"s3\_secret\_access\_key":{"text":"{{get.Secrets \\"hie\_s3\_export\_secret\_access\_key\\"}}"}}}},"hmacSecretData":true,"mount":"secrets","namespace":"admin/deployments/hie-test-34","path":"application","refreshAfter":null,"rolloutRestartTargets":\[\],"type":"kv-v2","vaultAuthRef":"default"}} creationTimestamp: "2026-02-11T16:21:16Z" finalizers: - vaultstaticsecret.secrets.hashicorp.com/finalizer generation: 3 name: s3-export-secret namespace: hie-test-34 resourceVersion: "521077" uid: 495cbcff-fd5d-42ff-b8c1-01ad6e4b4e93 spec: destination: create: true name: s3-export-secret overwrite: false transformation: excludeRaw: true excludes: -.\* templates: s3\_access\_key\_id: text: '{{get.Secrets "hie\_s3\_export\_access\_key\_id"}}' s3\_endpoint: text: '{{get.Secrets "hie\_s3\_export\_endpoint"}}' s3\_region: text: '{{get.Secrets "hie\_s3\_export\_aws\_region"}}' s3\_role\_arn: text: '{{get.Secrets "hie\_s3\_export\_role\_arn"}}' s3\_secret\_access\_key: text: '{{get.Secrets "hie\_s3\_export\_secret\_access\_key"}}' hmacSecretData: true mount: secrets namespace: admin/deployments/hie-test-34 path: application rolloutRestartTargets: \[\] type: kv-v2 vaultAuthRef: default status: lastGeneration: 3 secretMAC: yecLChFsFdHb1xVlfK2fQLjIRd+3OzEzYAeA8dZQpQA= - apiVersion: secrets.hashicorp.com/v1beta1 kind: VaultStaticSecret metadata: annotations: argocd.argoproj.io/tracking-id: hie-test-34-workflow-templates:secrets.hashicorp.com/VaultStaticSecret:hie-test-34/ude-secret kubectl.kubernetes.io/last-applied-configuration: | {"apiVersion":"secrets.hashicorp.com/v1beta1","kind":"VaultStaticSecret","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"hie-test-34-workflow-templates:secrets.hashicorp.com/VaultStaticSecret:hie-test-34/ude-secret"},"name":"ude-secret","namespace":"hie-test-34"},"spec":{"destination":{"create":true,"name":"ude-secret","transformation":{"excludes":\[".\*"\],"templates":{"udeKey":{"text":"{{get.Secrets \\"ude\_key\\"}}"}}}},"hmacSecretData":true,"mount":"secrets","namespace":"admin/deployments/hie-test-34","path":"application","refreshAfter":null,"rolloutRestartTargets":\[\],"type":"kv-v2","vaultAuthRef":"default"}} creationTimestamp: "2026-02-11T16:21:16Z" finalizers: - vaultstaticsecret.secrets.hashicorp.com/finalizer generation: 3 name: ude-secret namespace: hie-test-34 resourceVersion: "547869" uid: f661032f-5a82-443e-924b-174c75783696 spec: destination: create: true name: ude-secret overwrite: false transformation: excludes: -.\* templates: udeKey: text: '{{get.Secrets "ude\_key"}}' hmacSecretData: true mount: secrets namespace: admin/deployments/hie-test-34 path: application rolloutRestartTargets: \[\] type: kv-v2 vaultAuthRef: default status: lastGeneration: 3 secretMAC: 2t7y4xTQjfcKH+3MChPwbAON2fSl7M1puYHcvCgxBus= - apiVersion: secrets.hashicorp.com/v1beta1 kind: VaultStaticSecret metadata: annotations: argocd.argoproj.io/tracking-id: hie-test-34-workflow-templates:secrets.hashicorp.com/VaultStaticSecret:hie-test-34/workflows-secrets kubectl.kubernetes.io/last-applied-configuration: | {"apiVersion":"secrets.hashicorp.com/v1beta1","kind":"VaultStaticSecret","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"hie-test-34-workflow-templates:secrets.hashicorp.com/VaultStaticSecret:hie-test-34/workflows-secrets"},"name":"workflows-secrets","namespace":"hie-test-34"},"spec":{"destination":{"create":true,"name":"workflows-secrets","transformation":{"excludes":\[".\*"\],"templates":{"mongodb\_connection\_string":{"text":"mongodb://{{get.Secrets \\"mongodb\_username\\"}}:{{get.Secrets \\"mongodb\_password\\"}}@hie-test-34-mongodb-b17ef-0.hie-test-34-mongodb-b17ef-headless.hie-test-34.svc.cluster.local:27017/admin?replicaSet=rs0"},"oauth\_client\_id":{"text":"{{get.Secrets \\"auth0\_client\_id\\"}}"},"oauth\_client\_secret":{"text":"{{get.Secrets \\"auth0\_client\_secret\\"}}"},"s3\_access\_key\_id":{"text":"{{get.Secrets \\"s3\_access\_key\_id\\"}}"},"s3\_secret\_access\_key":{"text":"{{get.Secrets \\"s3\_secret\_access\_key\\"}}"},"spicedb.json":{"text":"{\\"preSharedKey\\":\\"{{ get.Secrets \\"spicedb\_pre\_shared\_key\\"}}\\"}"}}}},"hmacSecretData":true,"mount":"secrets","namespace":"admin/deployments/hie-test-34","path":"application","refreshAfter":null,"rolloutRestartTargets":\[\],"type":"kv-v2","vaultAuthRef":"default"}} creationTimestamp: "2026-02-11T16:21:16Z" finalizers: - vaultstaticsecret.secrets.hashicorp.com/finalizer generation: 3 name: workflows-secrets namespace: hie-test-34 resourceVersion: "548084" uid: f0d85c3e-b95e-4f68-a3f7-e8f233aecd3c spec: destination: create: true name: workflows-secrets overwrite: false transformation: excludes: -.\* templates: mongodb\_connection\_string: text: mongodb://{{get.Secrets "mongodb\_username"}}:{{get.Secrets "mongodb\_password"}}@hie-test-34-mongodb-b17ef-0.hie-test-34-mongodb-b17ef-headless.hie-test-34.svc.cluster.local:27017/admin?replicaSet=rs0 oauth\_client\_id: text: '{{get.Secrets "auth0\_client\_id"}}' oauth\_client\_secret: text: '{{get.Secrets "auth0\_client\_secret"}}' s3\_access\_key\_id: text: '{{get.Secrets "s3\_access\_key\_id"}}' s3\_secret\_access\_key: text: '{{get.Secrets "s3\_secret\_access\_key"}}' spicedb.json: text: '{"preSharedKey":"{{ get.Secrets "spicedb\_pre\_shared\_key"}}"}' hmacSecretData: true mount: secrets namespace: admin/deployments/hie-test-34 path: application rolloutRestartTargets: \[\] type: kv-v2 vaultAuthRef: default status: lastGeneration: 3 secretMAC: 7EqFKP3OsufMmYViZeSYHptBZYcRYxOzF+pipI2eOjE= kind: List metadata: resourceVersion: ""

---

Perfect—your VSO template is already trying to read the right keys:

…but in the _actual_ Kubernetes `Secret/ffcloud` you showed earlier, `cli-auth.json` exists yet the app is still sending:

That narrows it to one of these (in order of likelihood):

1. The keys in Vault are not present at that KV-v2 path (or different names/case), so `get.Secrets "cli_auth0_client_id"` renders empty.
2. Your app expects `client_id` / `client_secret`, but your generated JSON uses camelCase `clientId` / `clientSecret`. (This would result in "empty" even though the secret is present.)
3. The app is reading auth.json (not cli-auth.json), and _those_ fields (`auth0_client_id`, `auth0_client_secret`) are missing/empty for this deployment.

We can prove which in 60 seconds with 2 commands.

---

## 1) Print the Rendered JSON Files from the Kubernetes Secret (safe-ish)

These will show whether VSO templating produced empty fields and whether the field names match what the app reads.

### What to Look for

- Are `clientId` / `clientSecret` empty strings?
- Do you see `clientId` vs `client_id` mismatch?

---

## 2) Check whether the Vault Data Actually Contains Those Keys (via \_raw)

Because `ffcloud` includes `_raw`, this is the quickest "did Vault have the key?" check:

### Interpret the Result

- If grep finds nothing → Vault response didn't include those keys at that path (wrong name or wrong secret location).
- If grep shows the keys exist → templating or app parsing is the issue (likely camelCase vs snake\_case).

---

## Likely Fix You Can Apply Immediately

## Fix Option A (very likely): Change JSON Keys to what the Code Expects

Your Node code (and the Auth0 request body you saw) uses `client_id` / `client_secret` (snake\_case).

But your templates generate `clientId` / `clientSecret` (camelCase).

So update templates in the `VaultStaticSecret/ffcloud` to:

That change alone would turn "empty creds" into real creds even if Vault is correct.

## Fix Option B: App is Reading the Wrong File

If `cli-auth.json` is populated but `auth.json` is empty, and the init script uses non-cli creds, then you need Vault keys for:

- `auth0_client_id`
- `auth0_client_secret`

(or point the init script to use the cli ones).

---

## Separate: Fitconnect Crash is NOT Auth0 (it's Invalid Seed data)

Your VSO `fitconnect` secret doesn't include any `cli-auth.json` (only `auth.json`, db, s3 keys). That's fine.

But your fitconnect crash is a Zod validation on a "connection document" with missing fields like `endpoint`, `tenantId`, `audience`, `databaseName`. That's coming from seed/default connection config (configmap or Mongo). We can tackle that next, but the ffcloud init must be fixed first because it's blocking multiple pods.

---

## Do These now and Paste the Output

Just these two:

If they show `clientId/clientSecret`, I'll give you the exact `kubectl patch` to update the VaultStaticSecret template in-place (no guessing).

---

kubectl get secret ffcloud -n hie-test-34 -o jsonpath='{.data.auth\\.json}' | base64 -d; echo kubectl get secret ffcloud -n hie-test-34 -o jsonpath='{.data.cli-auth\\.json}' | base64 -d; echo {"clientId":"","clientSecret":"", "audience": ""} {"clientId":"CzWFSi0mEbLJVG3vLaLVQtQnfw'''","clientSecret":"slhvkIoi3Ae3-GVnODClCTcZQzLIeXP\_bhxn2Tyl35Fy9Dn…", "audience": ""} I redacted the actual secret values for safty

---

Yep—that explains _everything_.

### What We now Know

- `cli-auth.json` has `clientId` + `clientSecret` ✅ (so VSO is pulling `cli_auth0_client_*` correctly)
- `auth.json` has empty `clientId/clientSecret/audience` ❌ (so `auth0_client_id`, `auth0_client_secret`, `auth0_audience` are missing/empty at that Vault path)
- Your ffcloud init script is calling Auth0 with empty creds → it's almost certainly using auth.json (or the non-cli keys), not `cli-auth.json`
- Also: both JSON files use camelCase (`clientId`) but your failing request body earlier used snake\_case (`client_id`). That could be a second mismatch depending on how the app parses it.

So you have two fixes:

1. Populate the non-cli Auth0 keys in Vault (`auth0_client_id`, `auth0_client_secret`, `auth0_audience`)
	_or_ change the template to use the cli keys for `auth.json` too.
2. Ensure the JSON key names match what the code expects (`client_id` / `client_secret` vs `clientId` / `clientSecret`).

Given your logs literally show the outgoing JSON has `client_id` / `client_secret`, I'd fix the templates to output snake\_case to be safe.

---

## Fix Option (fastest, Works immediately): Make auth.json Use the Cli Keys + snake\_case

### Patch the VaultStaticSecret Ffcloud Templates

Run this (it only changes the two template strings):

### Then Force a Refresh (wait One Sync Interval or just Restart rollout)

VSO refreshes every 5m, but you already have rolloutRestartTargets set; easiest is restart the deployment once the secret updates:

### Verify the Secret now Has the Right Shape (and audience)

You want to see non-empty `client_id`, `client_secret`, and (ideally) `audience`.

---

## Fix the Missing Audience (you Currently Have "")

Both templates are pulling `auth0_audience`, but it's coming out empty. That means either:

- the key in Vault is named differently (common: `auth0_audience_ffcloud`, `auth0_api_audience`, etc), or
- it's missing in that path.

### Quick Check: is the Audience Present Anywhere in \_raw?

- If nothing → Vault doesn't have `auth0_audience` there; you must add it or change the key name in the template.
- If it exists → template key name mismatch or it's nested.

If you know the correct Vault key name, patch just the audience line in the templates similarly.

---

## After Ffcloud is Fixed, Your Fitconnect Issue Remains (different problem)

fitconnect is crashing because it's seeding/reading an invalid "connection document" (missing endpoint/tenantId/audience/databaseName). That's not Auth0—it's bad seed config (likely in Mongo or configmap). Once ffcloud is up, we can tackle that with:

---

### If You want the Safest Long-term Fix instead

Rather than reusing cli creds, populate in Vault:

- `auth0_client_id`
- `auth0_client_secret`
- `auth0_audience`

…so `auth.json` is "service creds" and `cli-auth.json` is "cli creds". But the patch above will get you unstuck now.

If you run the patch + restart and paste the new `auth.json`, we'll know immediately if the init container will pass.

---

I deployed via terraform on the jumpbox cat main.tf ############# # Variables # ############# variable "vault\_address" { description = "The address of the Hashicorp Vault instance" type = string } variable "tls\_certificate\_secret\_name" { description = "The name of the Kubernetes secret containing TLS certificates for the ingress controller" type = string default = "hie-prod-34-tls-cert" } variable "enable\_default\_tls" { description = "Whether to enable default TLS certificate for the ingress controller" type = bool default = true } variable "deployment\_repo\_values\_file\_path" { description = "The path in the FITFILE GitLab deployment repo to the helm value overrides file for this specific deployment." type = string } variable "argocd\_host" { description = "The host for the argocd ingress object" type = string } variable "deployment\_key" { description = "The deployment key chosen for this particular deployment" type = string } variable "vault\_auth\_backend" { description = "The name of the auth backend mount to use for approle authentication" type = string default = "approle" } variable "approles" { description = "The hashicorp Vault approle secrets for this deployment" type = map(object({ secret\_id = string role\_id = string })) sensitive = true validation { condition = contains(keys(var.approles), "argocd") && contains(keys(var.approles), "application") && contains(keys(var.approles), "spicedb") && contains(keys(var.approles), "monitoring") error\_message = "The approles must provide keys for `argocd`, `application`, `monitoring` and `spicedb` " } } variable "aks\_cluster\_host" { description = "The host address of the aks cluster" } variable "aks\_cluster\_ca\_certificate" { description = "The ca certificate of the aks cluster" sensitive = true } variable "ingress\_controller\_ip\_address" { description = "The ip address for the nginx ingress controller to bind to. This should have been chosen in the infrastructure. The default value is 10.0.1.10" } ################### # TLS Certificate # ################### # Create VaultDynamicSecret to request TLS certificate from PKI resource "kubectl\_manifest" "tls\_certificate\_vault\_secret" { count = var.enable\_default\_tls? 1: 0 yaml\_body = yamlencode({ apiVersion = "secrets.hashicorp.com/v1beta1" kind = "VaultDynamicSecret" metadata = { name = "tls-certificate" namespace = "cert-manager" labels = { managedBy = "terraform" } } spec = { mount = "pki\_int\_${var.deployment\_key}" path = "issue/${var.deployment\_key}-server" destination = { name = "${var.deployment\_key}-tls-cert" create = true type = "kubernetes.io/tls" transformation = { templates = { "tls.crt" = { text = "{{.Secrets.certificate }}" } "tls.key" = { text = "{{.Secrets.private\_key }}" } } } annotations = { "reflector.v1.k8s.emberstack.com/reflection-allowed" = "true" "reflector.v1.k8s.emberstack.com/reflection-auto-enabled" = "true" "reflector.v1.k8s.emberstack.com/reflection-auto-namespaces" = "ingress-nginx" } } vaultAuthRef = "vault-issuer" renewalPercent = 67 params = { common\_name = "${var.deployment\_key}.fitfile.net" ttl = "2160h" } } }) depends\_on = \[module.platform\] } ########## # Locals # ########## locals { # This may not be used for a private cluster argocd\_host = var.argocd\_host argocd\_applications = \[{ name = "ff-${lower(var.deployment\_key)}" target\_revision = "eoe-test-release" source = { release\_name = lower(var.deployment\_key) type = "helm" value\_files = \[var.deployment\_repo\_values\_file\_path\] } }\] vault\_namespace = "deployments/${var.deployment\_key}" app\_role\_secrets\_map = tomap({ "argocd" = { namespace = "argocd" secret\_name = "role-secrets" role\_id = var.approles\["argocd"\].role\_id secret\_id = var.approles\["argocd"\].secret\_id vault\_namespace = local.vault\_namespace vault\_backend = var.vault\_auth\_backend vault\_auth\_name = "default" } "application" = { namespace = lower(var.deployment\_key) secret\_name = "role-secrets" role\_id = var.approles\["application"\].role\_id secret\_id = var.approles\["application"\].secret\_id vault\_namespace = local.vault\_namespace vault\_backend = var.vault\_auth\_backend vault\_auth\_name = "default" } "spicedb" = { namespace = "spicedb" secret\_name = "role-secrets" role\_id = var.approles\["spicedb"\].role\_id secret\_id = var.approles\["spicedb"\].secret\_id vault\_namespace = local.vault\_namespace vault\_backend = var.vault\_auth\_backend vault\_auth\_name = "default" } "argoWorkflows" = { namespace = "argo" secret\_name = "role-secrets" role\_id = var.approles\["argo-workflows"\].role\_id secret\_id = var.approles\["argo-workflows"\].secret\_id vault\_namespace = local.vault\_namespace vault\_backend = var.vault\_auth\_backend vault\_auth\_name = "default" } "monitoring" = { namespace = "monitoring" secret\_name = "role-secrets" role\_id = var.approles\["monitoring"\].role\_id secret\_id = var.approles\["monitoring"\].secret\_id vault\_namespace = local.vault\_namespace vault\_backend = var.vault\_auth\_backend vault\_auth\_name = "default" } }) } ############# # Providers # ############# terraform { required\_providers { kubernetes = { source = "hashicorp/kubernetes" } helm = { source = "hashicorp/helm" version = "3.0.2" } kubectl = { source = "app.terraform.io/FITFILE-Platforms/kubectl" } } } provider "helm" { kubernetes = { host = var.aks\_cluster\_host exec = { api\_version = "client.authentication.k8s.io/v1beta1" args = \["--region", "eu-west-2", "eks", "get-token", "--cluster-name", "eoe-test-codisc"\] command = "aws" } cluster\_ca\_certificate = base64decode(var.aks\_cluster\_ca\_certificate) } } provider "kubernetes" { host = var.aks\_cluster\_host exec { api\_version = "client.authentication.k8s.io/v1beta1" args = \["--region", "eu-west-2", "eks", "get-token", "--cluster-name", "eoe-test-codisc"\] command = "aws" } cluster\_ca\_certificate = base64decode(var.aks\_cluster\_ca\_certificate) } # Needed to deploy CRD objects before the CRDs are deployed # This article explains it very nicely: <https://medium.com/@danieljimgarcia/dont-use-the-terraform-kubernetes-manifest-resource-6c7ff4fe629a> provider "kubectl" { host = var.aks\_cluster\_host exec { api\_version = "client.authentication.k8s.io/v1beta1" args = \["--region", "eu-west-2", "eks", "get-token", "--cluster-name", "eoe-test-codisc"\] command = "aws" } cluster\_ca\_certificate = base64decode(var.aks\_cluster\_ca\_certificate) load\_config\_file = false } data "terraform\_remote\_state" "versions" { backend = "remote" config = { organization = "FITFILE-Platforms" workspaces = { name = "global-version-manager" } } } ################### # Platform Module # ################### module "platform" { source = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm" version = "2.2.10" # Pass provider configurations from root module providers = { kubernetes = kubernetes helm = helm kubectl = kubectl } helm\_repository\_url = "oci://fitfilepublic.azurecr.io" ingress\_nginx\_chart\_version = data.terraform\_remote\_state.versions.outputs.ingress\_nginx\_chart\_version argocd\_chart\_version = data.terraform\_remote\_state.versions.outputs.argocd\_chart\_version # argocd\_apps\_chart\_version = data.terraform\_remote\_state.versions.outputs.argocd\_apps\_chart\_version argocd\_apps\_chart\_version = "2.0.2" vault\_operator\_chart\_version = data.terraform\_remote\_state.versions.outputs.vault\_operator\_chart\_version reflector\_chart\_version = data.terraform\_remote\_state.versions.outputs.reflector\_chart\_version cluster\_autoscaler\_chart\_version = data.terraform\_remote\_state.versions.outputs.cluster\_autoscaler\_chart\_version ingress\_ip\_address = var.ingress\_controller\_ip\_address ingress\_load\_balancer\_type = "internal" ingress\_host\_network = true ingress\_nginx\_controller\_kind = "DaemonSet" vault\_address = var.vault\_address argocd\_host = local.argocd\_host argocd\_applications = local.argocd\_applications app\_role\_secrets\_map = local.app\_role\_secrets\_map cloud\_provider = "AWS" use\_image\_pull\_secret = true cluster\_name = "eoe-test-codisc" cluster\_autoscaler\_iam\_role\_arn = "arn:aws:iam::135808916559:role/eoe-test-codisc-eks-cluster-autoscaler-role" argocd\_sso = { enabled = false } } resource "kubectl\_manifest" "argocd\_git\_creds" { yaml\_body = yamlencode({ apiVersion = "secrets.hashicorp.com/v1beta1" kind = "VaultStaticSecret" metadata = { name = "argocd-repo-git-creds" namespace = "argocd" } spec = { type = "kv-v2" vaultAuthRef = "default" mount = "secrets" path = "argocd" destination = { name = "argocd-repo-fitfile-deployment-repo" create = true labels = { "argocd.argoproj.io/secret-type" = "repository" } transformation = { templates = { username = { text = "{{.Secrets.gitlab\_deploy\_token\_username }}" } password = { text = "{{.Secrets.gitlab\_deploy\_token\_password }}" } type = { text = "git" } url = { text = "https://gitlab.com/fitfile/deployment.git" } } } } refreshAfter = "1h" } }) }

---

Thanks—the Terraform is basically fine for "wiring", but it explains _why_ you're seeing empty fields:

### What's Actually Happening

- Your `VaultStaticSecret` is reading from Vault KV-v2 at:
	- `mount: secrets`
	- `namespace: admin/deployments/hie-test-34`
	- `path: application`
- In that Vault location, you have cli keys:
	- `cli_auth0_client_id`
	- `cli_auth0_client_secret`

…and those _are_ coming through (since `cli-auth.json` is populated).

But your template also expects non-cli keys:

- `auth0_client_id`
- `auth0_client_secret`
- `auth0_audience`

Those are missing in that same Vault secret (and `auth0_audience` is missing too—hence empty audience in both JSONs).

So the question isn't Terraform at this point—it's: do you intend to store service creds as `auth0_client_*` and audience as `auth0_audience` at that Vault path, or do you want the app to use the cli creds?

Either way, you can fix it immediately at the K8s/VSO layer.

---

## ✅ Fastest "get it Running now" Fix (Kubernetes side)

## Patch Ffcloud VaultStaticSecret so auth.json Uses the Cli Creds

This makes the init container stop calling Auth0 with empty creds.

Two important improvements there:

- switch to snake\_case (`client_id`, `client_secret`) to match what your code was sending
- make `auth.json` use the populated cli keys

Then restart:

Verify:

---

## ✅ Correct "proper" Fix (Vault Side, what Terraform/VSO expects)

If you _don't_ want to reuse cli creds for the service, then you should add these keys to the Vault secret at:

`secrets (kv-v2) / admin/deployments/hie-test-34 / application`

- `auth0_client_id`
- `auth0_client_secret`
- `auth0_audience`

Once those exist, your existing templates will render correctly without the patch above.

You can confirm what's missing right now without exposing values:

---

## One More Terraform Observation (important but not the Root cause)

In your Terraform `locals` you set:

…but your actual `VaultStaticSecret` objects are using:

That implies the helm chart/module is intentionally using the `admin/` prefix (or you have multiple Vault namespaces in play). Since `cli-auth.json` is being populated, auth is working—but it's easy for the values to be in a different Vault namespace/path than you think.

If you intended the secrets to live under `deployments/hie-test-34` (without `admin/`), then you'll see exactly this kind of "some keys exist, some are empty" depending on where they were written.

---

## What I'd Do next (in order)

1. Patch VSS templates (K8s) to get ffcloud out of init crash (above).
2. Fix `auth0_audience` in Vault (or patch template to use the correct key name).
3. Then tackle fitconnect's seeded connection document validation error (separate issue).

If you tell me what the correct Vault key name is for audience (or whether it's meant to be blank), I'll give you the exact one-line patch to fix audience too.

---

kubectl patch vaultstaticsecret ffcloud -n hie-test-34 --type='json' -p='\[{"op":"replace","path":"/spec/destination/transformation/templates/auth.json/text", "value":"{\\"client\_id\\":\\"{{ get.Secrets \\\\\\"cli\_auth0\_client\_id\\\\\\" }}\\",\\"client\_secret\\":\\"{{ get.Secrets \\\\\\"cli\_auth0\_client\_secret\\\\\\" }}\\",\\"audience\\":\\"{{ get.Secrets \\\\\\"auth0\_audience\\\\\\" }}\\"}"}, {"op":"replace","path":"/spec/destination/transformation/templates/cli-auth.json/text", "value":"{\\"client\_id\\":\\"{{ get.Secrets \\\\\\"cli\_auth0\_client\_id\\\\\\" }}\\",\\"client\_secret\\":\\"{{ get.Secrets \\\\\\"cli\_auth0\_client\_secret\\\\\\" }}\\",\\"audience\\":\\"{{ get.Secrets \\\\\\"auth0\_audience\\\\\\" }}\\"}"} \]' vaultstaticsecret.secrets.hashicorp.com/ffcloud patched awsadmin@ip-10-66-2-4:~/terraform$ kubectl rollout restart deployment hie-test-34-ffcloud-service -n hie-test-34 deployment.apps/hie-test-34-ffcloud-service restarted awsadmin@ip-10-66-2-4:~/terraform$ kubectl get secret ffcloud -n hie-test-34 -o jsonpath='{.data.auth\\.json}' | base64 -d; echo {"clientId":"","clientSecret":"", "audience": ""}

---

That output is expected right now, and it tells us the patch didn't take effect in the _rendered Secret_ yet—not that the patch failed.

There are two likely reasons:

1. VSO hasn't re-synced the secret since you patched the `VaultStaticSecret` (it's on a 5-minute refresh), and rollout restart doesn't force the operator to regenerate the Secret.
2. Even after resync, your `Secret/ffcloud` may still show the old JSON because destination.overwrite is `false` in the VaultStaticSecret. That means "don't update existing keys", which would leave the old `auth.json` content in place forever.

You can confirm 2 immediately: in your YAML, I can see:

That is the blocker.

---

## ✅ Fix: Allow the Operator to Overwrite the Existing Secret Data

Patch `overwrite` to `true`:

Now force a reconcile by deleting the generated Secret (it will be recreated by VSO with the new templates):

Then watch for it to come back:

Once it's recreated, re-check:

You should now see the new JSON (with `client_id` / `client_secret`).

---

## Important: You Restarted the Deployment before the Secret Changed

After the secret updates, restart the deployment again:

Then watch the init container logs:

(or if it's still running, without `--previous`)

---

## One More Thing: Your auth.json Output Still Shows clientId/clientSecret

That confirms you're still reading the old `auth.json` content (pre-patch). After the overwrite+recreate, it should become `client_id/client_secret` if our template update applied.

If after recreate it _still_ shows camelCase, then we're patching the wrong object (e.g., ArgoCD is immediately reconciling it back), which we can detect by:

That should print the new snake\_case template.

---

### Do These 3 Commands in order and Paste Outputs

That will get you to the new rendered secret.

---

kubectl get vaultstaticsecret ffcloud -n hie-test-34 -o jsonpath='{.spec.destination.transformation.templates.auth\\.json.text}'; echo {"clientId":"{{ get.Secrets "auth0\_client\_id" }}","clientSecret":"{{ get.Secrets "auth0\_client\_secret" }}", "audience": "{{ get.Secrets "auth0\_audience" }}"}

---

Great catch—this proves what's happening:

✅ Your patch _applied_, but ArgoCD immediately reconciled the `VaultStaticSecret` back to the original template (camelCase + non-cli keys). That's why the spec still shows:

- `auth0_client_id/auth0_client_secret` (empty in Vault)
- `clientId/clientSecret` (camelCase)
	…and why your Secret never changes.

So you have two separate blockers:

1. GitOps drift: you must fix it in the source-of-truth (Terraform/Helm values / Argo app), or Argo will revert any manual patch.
2. Even if you fix the template, `destination.overwrite: false` can prevent updates to existing Secret keys.

Let's do the shortest "get it stable" path.

---

## 1) Confirm Argo is the Reconciler (and See the Owning app)

This will show the Argo labels/annotations and the managing Argo Application:

Look for:

- `argocd.argoproj.io/tracking-id`
- any `app.kubernetes.io/managed-by: argocd`

You already have `argocd.argoproj.io/tracking-id` so yes, Argo owns it.

---

## 2) The Correct Fix: Update the chart/value File that Generates This VSS

Because Argo is deploying `ff-${deployment_key}` from the deployment repo values file you pass in:

So the fix belongs in that values file (or whatever template in the chart produces the `VaultStaticSecret ffcloud`).

### What to Change in Git

Change the `ffcloud` VaultStaticSecret templates to:

- use cli keys for auth.json (or ensure auth0\_client\_\* exist)
- use snake\_case to match Node's Auth0 request payload
- set overwrite true (optional but recommended)

#### Recommended Template (service Uses Cli Creds as workaround)

If you want the "proper" version, keep `auth0_client_*` but then you must add those keys in Vault.

Also set:

so updates actually propagate.

---

## 3) If You Need an Immediate One-off Fix (without Fighting Argo)

You can do it, but you must _either_ pause Argo sync or accept it'll be reverted.

### Option A: Temporarily Disable Argo Auto-sync for that App (best Tactical move)

Find the Argo Application in namespace `argocd`:

Then patch it to disable automated sync (names vary; this is the general idea):

Now your `kubectl patch vaultstaticsecret …` will stick.

### Option B: Patch Again, but Expect it to Revert

Not great, but if you just want to prove it works, you can patch and immediately restart pods before Argo flips it back.

---

## 4) Once the VSS Template is Correct, You Still Must Handle Overwrite

Because `overwrite: false` stops the Secret content updating.

So in Git (or temporarily via patch) set:

Then either wait for refresh or force regeneration by deleting the Secret:

---

## Minimal Command Sequence to Prove the Full Flow (after You Fix Git or Disable sync)

1. Verify VSS spec shows the new template:
2. Ensure overwrite is true:
3. Regenerate the secret:
4. Verify rendered secret:
5. Restart deployment:

---

## The One Thing I Need from You to point at the Exact File to Edit

What is `var.deployment_repo_values_file_path` for this deployment? (Just the path, not secrets.)

But even without that: the fix is definitely "change the VaultStaticSecret ffcloud template in the Git-managed manifest", because Argo is overwriting you.

---

### # Hyve FFNode Chart Values # ############################### Namespace: Hie-test-34 deploymentKey: Hie-test-34 Host: "app.eoe-test-codisc.privatelink.fitfile.net" argocdApp: targetRevision: "eoe-test-release" Global: fitConnectCode: "EOE SDE CODISC" Oauth: baseURL: "https://fitfile-prod.eu.auth0.com" managementApiAudience: "https://fitfile-prod.eu.auth0.com/api/v2/" Mongodb: targetRevision: "16.5.\*" replicaCount: 1 Minio: Persistence: Size: 64Gi Postgresql: Primary: Persistence: Size: 64Gi argoWorkflows: Server: authModes: \[client\] Sso: Enabled: False workflowTemplates: extraVaultSecrets: - secretName: s3-export-secret vaultPath: "application" secretTransformation: excludeRaw: True Excludes: -.\* Templates: s3\_access\_key\_id: Text: '{{"{{ `{{get.Secrets \"hie_s3_export_access_key_id\"}}` }}"}}' s3\_secret\_access\_key: Text: '{{"{{ `{{get.Secrets \"hie_s3_export_secret_access_key\"}}` }}"}}' s3\_region: Text: '{{"{{ `{{get.Secrets \"hie_s3_export_aws_region\"}}` }}"}}' s3\_endpoint: Text: '{{"{{ `{{get.Secrets \"hie_s3_export_endpoint\"}}` }}"}}' s3\_role\_arn: Text: '{{"{{ `{{get.Secrets \"hie_s3_export_role_arn\"}}` }}"}}' Global: nodeSelector: Agentpool: Null eks.amazonaws.com/nodegroup: WorkflowsNodeGroup Tolerations: - Key: "workflows" Operator: "Equal" Value: "true" Effect: "NoSchedule" Fitconnect: Fitconnect: appConfig: featureFlags: exportToS3: True omopAndExportToS3: True Tls: Spec: - Hosts: - app.eoe-test-codisc.privatelink.fitfile.net secretName: Fitfile-eoe-tls Ingress: Hosts: - Hostname: "app.eoe-test-codisc.privatelink.fitfile.net" Path: "/fitconnect" pathType: Prefix Ffcloud: appConfig: availableServiceAccountIds: \["r0rfJBjPvbXBq3AnOOCgx7M6feJCKVYt"\] # Ollie defaultOrganisationAdminUserId: "auth0|61f3e4d81a44500069ebc39d" fitConnectHosts: - fitConnectCode: "EOE SDE CODISC" fitConnectUri: http://hie-test-34-fitconnect-ftc/fitconnect coordinatorUri: http://hie-test-34-ffcloud-service/ffcloud cryptoUri: "" Tls: Spec: - Hosts: - app.eoe-test-codisc.privatelink.fitfile.net secretName: Fitfile-eoe-tls Ingress: Hosts: - Hostname: "app.eoe-test-codisc.privatelink.fitfile.net" Path: "/ffcloud" pathType: Prefix workflowsApi: workflow\_node\_selector: eks.amazonaws.com/nodegroup: WorkflowsNodeGroup # Unsets the Default Node Selector Agentpool: Null workflow\_tolerations: - Key: "workflows" Operator: "Equal" Value: "true" Effect: "NoSchedule" Frontend: Features: FEATURE\_UPDATE\_QUERY\_PLAN: "true" FEATURE\_CREATE\_QUERY\_PLAN: "true" FEATURE\_DELETE\_QUERY\_PLAN: "true" FEATURE\_QUICK\_PROJECT\_CREATION: "true" FEATURE\_CUSTOM\_PROJECT\_NAME: "true" FEATURE\_CREATE\_CUSTOM\_TRANSFORMATIONS: "true" Tls: existingSecret: Fitfile-eoe-tls Env: - Name: RESULT\_DETAILS\_LIMIT Value: "10000" - Name: INACTIVITY\_TIME\_PERIOD Value: "900000" certManager: Webhook: # Must Be Host Networking in AWS EKS hostNetwork: True securePort: 10260 Certs: Certificates: - Name: Fitfile-eoe Namespace: Hie-test-34 dnsNames: \["app.eoe-test-codisc.privatelink.fitfile.net"\] secretName: Fitfile-eoe-tls - Name: Ohdsi-eoe Namespace: Ohdsi dnsNames: \["ohdsi.eoe-test-codisc.privatelink.fitfile.net"\] secretName: Ohdsi-eoe-tls defaultCertificateConfig: issuerRef: Name: "vault-issuer" Issuer: Amce: Enabled: False Vault: Enabled: True Namespace: admin/deployments/hie-test-34 Path: pki\_int\_hie-test-34/sign/cert-manager roleId: "f5152031-e2ea-f1e1-e2cf-fd8ee0a6296a"

---

Nice—this values file tells us exactly why your manual patch keeps reverting: the VaultStaticSecret is generated by the Hyve FFNode chart, and Argo is applying it from this repo.

So the fix is: change the chart/templates (or the values the chart uses) so the rendered `VaultStaticSecret ffcloud` uses the right keys + overwrite. Your values file _doesn't currently expose a knob_ for the ffcloud secret template, so you have two practical routes:

---

## Route 1 (cleanest): Put the Missing Keys into Vault

Your chart's rendered VSS expects:

- `auth0_client_id`
- `auth0_client_secret`
- `auth0_audience`

…and uses those to generate `auth.json`. Right now Vault only has the cli\_ keys.

If you add those three keys to Vault at:

- KV-v2 mount: `secrets`
- Vault namespace: `admin/deployments/hie-test-34`
- Secret path: `application`

…then no chart change is required and everything will work with GitOps as-is.

This is the best long-term approach if `auth.json` is meant to represent "service creds" (not cli creds).

---

## Route 2 (fast Workaround, GitOps-safe): Change the Chart Template Output

If you _want_ the service to use the cli creds (or you don't want to add new Vault keys), then you need the chart-rendered VSS for ffcloud updated to:

1. read `cli_auth0_client_id` / `cli_auth0_client_secret` for `auth.json`, and
2. use snake\_case JSON keys (`client_id`, `client_secret`) to match your Node/Auth0 client code, and
3. set `destination.overwrite: true` (or delete+recreate secret on change).

### What to Change in the Chart Template (this is the Exact Desired Rendered spec)

For `VaultStaticSecret ffcloud`:

You'll also want to ensure `auth0_audience` exists in Vault (it's currently empty too).

---

## Your Values File Hints at the Audience Key name Mismatch

In values you've got:

But your VSS template is reading `auth0_audience` from Vault, which is empty.

So either:

- add `auth0_audience` to Vault (recommended), OR
- change the template to use `global.oauth.managementApiAudience` as the audience for the CLI token (if that's what you want), OR
- have separate audiences for management API vs your API.

Given the request body you saw used `audience: "https://fitfile-prod.eu.auth0.com/api/v2/"`, your `managementApiAudience` value is exactly that—so you could eliminate the Vault dependency for audience entirely.

---

## What I'd Do Next, Minimal Effort

## Step 1: Decide "Vault fix" Vs "chart fix"

- If you can edit Vault: add `auth0_client_id`, `auth0_client_secret`, `auth0_audience` → fastest overall, no Git/Argo changes.
- If you can't: you must edit the chart template (or add a values override feature) because Argo will revert kubectl patches.

## Step 2: Validate whether the Chart Supports "extraVaultSecrets" for Ffcloud

Your chart already supports:

If it also supports something like `ffcloud.extraVaultSecrets` / `extraVaultSecrets` at top level, you could inject a second secret without changing the chart. But I can't assume it does.

We can quickly confirm by searching rendered manifests from Argo:

and/or pull the manifest from Argo (if argocd cli exists). If not, simplest is: update chart.

---

## Tactical "get Me Unblocked now" (even with Argo)

If you want it working _immediately_ and you can tolerate an out-of-band fix:

1. Add the missing Vault keys (`auth0_client_id`, `auth0_client_secret`, `auth0_audience`) at that path.
2. Then restart deployment:

No Argo fights, no template changes.

---

## Quick Confirmation Question (only One, because it Determines the Correct fix)

Do you have permission to write those three keys into Vault at `admin/deployments/hie-test-34/application`?

- If yes → do Vault fix, you're done.
- If no → I'll tell you exactly where in the chart/template to edit and what values override pattern to add so future deployments don't break.

---

kubectl rollout restart deployment hie-test-34-ffcloud-service -n hie-test-34 deployment.apps/hie-test-34-ffcloud-service restarted awsadmin@ip-10-66-2-4:~/terraform$ kubectl get pods -n hie-test-34 NAME READY STATUS RESTARTS AGE hie-test-34-ffcloud-service-67645976cc-2xh56 0/3 Init:0/1 0 2s hie-test-34-ffcloud-service-6c69644b49-nclcz 0/3 Init:0/1 3 (28s ago) 52s hie-test-34-fitconnect-ftc-5b4c975dcf-bb7m6 0/1 CrashLoopBackOff 1 (3s ago) 17s hie-test-34-fitconnect-ftc-6f7d9dc8b4-5chrz 0/1 CrashLoopBackOff 187 (2m33s ago) 15h hie-test-34-minio-6b9779bb4b-gnsb8 1/1 Running 0 17h hie-test-34-minio-provisioning-88sn8 0/1 Completed 0 17h hie-test-34-mongodb-b17ef-0 2/2 Running 0 17h hie-test-34-mongodb-b17ef-arbiter-0 1/1 Running 0 17h hie-test-34-postgresql-0 1/1 Running 0 17h workflows-api-5bd448f79-78szp 1/1 Running 0 17h awsadmin@ip-10-66-2-4:~/terraform$ kubectl get pods -n hie-test-34 NAME READY STATUS RESTARTS AGE hie-test-34-ffcloud-service-67645976cc-2xh56 0/3 Init:Error 2 (20s ago) 29s hie-test-34-ffcloud-service-6c69644b49-nclcz 0/3 Init:CrashLoopBackOff 3 (25s ago) 79s hie-test-34-fitconnect-ftc-5b4c975dcf-bb7m6 0/1 Error 2 (30s ago) 44s hie-test-34-fitconnect-ftc-6f7d9dc8b4-5chrz 0/1 CrashLoopBackOff 187 (3m ago) 15h hie-test-34-minio-6b9779bb4b-gnsb8 1/1 Running 0 17h hie-test-34-minio-provisioning-88sn8 0/1 Completed 0 17h hie-test-34-mongodb-b17ef-0 2/2 Running 0 17h hie-test-34-mongodb-b17ef-arbiter-0 1/1 Running 0 17h hie-test-34-postgresql-0 1/1 Running 0 17h workflows-api-5bd448f79-78szp 1/1 Running 0 17h

---

Yep—this is consistent with Argo having reverted your VSS template: the new ffcloud pods are still dying in the init container.

Now you want the next kubectl commands that will tell you exactly _why_ the new init containers failed (it'll almost certainly still be Auth0 401 with empty creds / audience).

## 1) Grab Init Container Logs from the New Pods

Do both current and previous (because it's CrashLooping):

## 2) Confirm what auth.json Looks like Right now (post-restart)

This tells us whether Argo reverted (it will):

If `auth.json` is still empty, the init script will keep failing.

## 3) Get the Events for just Those Pods (quick signal)

---

## Fitconnect: Grab Its Logs (it's now "Error", not just CrashLoop)

For the new one:

(From earlier, fitconnect is failing seed validation; likely still happening.)

---

## The Fix You Need (and why Restarts Won't help)

Until Git/Vault is corrected, ffcloud will never pass init.

You have two stable ways forward:

### Option A: Add Missing Keys in Vault (no Git change)

Add these into Vault at `admin/deployments/hie-test-34/application`:

- `auth0_client_id`
- `auth0_client_secret`
- `auth0_audience`

This will make the _existing_ chart template render a valid `auth.json`.

### Option B: Change Chart Template (Git change)

Update the ffcloud VaultStaticSecret template so `auth.json` uses the `cli_` keys (or outputs env vars / snake\_case).

---

If you paste the init-db logs from one of the new ffcloud pods, I'll tell you exactly which of the above is required (and whether the audience being empty is now the immediate blocker).

---

Done in 1.46s. yarn run v1.22.22 $ yarn node scripts/init.js {"name":"ffcloud","hostname":"hie-test-34-ffcloud-service-6c69644b49-nclcz","pid":71,"level":30,"event":"Mongo Client Instantiated","msg":"","time":"2026-02-12T09:40:32.591Z","src":{"file":"/app/infra/repositories/MongoClientSingleton.js","line":20,"func":"getInstance"},"v":0} {"name":"ffcloud","hostname":"hie-test-34-ffcloud-service-6c69644b49-nclcz","pid":71,"level":30,"msg":"EventMediator: Starting up","time":"2026-02-12T09:40:32.684Z","src":{"file":"/app/infra/mediator/mongodb/MongoDBChangeStreamEventMediator.js","line":121},"v":0,"correlationId":"f88e55ec-506d-47c3-9978-85cfeb392cc5","userId":{"userId":"auth0|61f3e4d81a44500069ebc39d"}} {"name":"ffcloud","hostname":"hie-test-34-ffcloud-service-6c69644b49-nclcz","pid":71,"level":30,"msg":"EventMediator: Starting watch on Events change stream","time":"2026-02-12T09:40:32.695Z","src":{"file":"/app/infra/mediator/mongodb/MongoDBChangeStreamEventMediator.js","line":135},"v":0,"correlationId":"f88e55ec-506d-47c3-9978-85cfeb392cc5","userId":{"userId":"auth0|61f3e4d81a44500069ebc39d"}} {"name":"ffcloud","hostname":"hie-test-34-ffcloud-service-6c69644b49-nclcz","pid":71,"level":30,"msg":"EventMediator: Change stream ready","time":"2026-02-12T09:40:32.700Z","src":{"file":"/app/infra/mediator/mongodb/MongoDBChangeStreamEventMediator.js","line":153},"v":0,"correlationId":"f88e55ec-506d-47c3-9978-85cfeb392cc5","userId":{"userId":"auth0|61f3e4d81a44500069ebc39d"}} AuthTokenDecodeError: Unable to get Auth0 access token at getAuthHeader (/app/node\_modules/@fitfile/service-common/dist/infra/clients/auth0.js:92:19) at process.processTicksAndRejections (node:internal/process/task\_queues:105:5) at async Object.getUsersInfo (/app/node\_modules/@fitfile/service-common/dist/infra/clients/auth0.js:96:29) { \[cause\]: AxiosError: Request failed with status code 403 at settle (/app/node\_modules/axios/dist/node/axios.cjs:2097:12) at IncomingMessage.handleStreamEnd (/app/node\_modules/axios/dist/node/axios.cjs:3305:11) at IncomingMessage.emit (node:events:536:35) at endReadableNT (node:internal/streams/readable:1698:12) at process.processTicksAndRejections (node:internal/process/task\_queues:90:21) at Axios.request (/app/node\_modules/axios/dist/node/axios.cjs:4483:41) at process.processTicksAndRejections (node:internal/process/task\_queues:105:5) at async getAuthHeader (/app/node\_modules/@fitfile/service-common/dist/infra/clients/auth0.js:81:26) at async Object.getUsersInfo (/app/node\_modules/@fitfile/service-common/dist/infra/clients/auth0.js:96:29) { code: 'ERR\_BAD\_REQUEST', config: { transitional: \[Object\], adapter: \[AsyncFunction: adapter\], transformRequest: \[Array\], transformResponse: \[Array\], timeout: 0, xsrfCookieName: 'XSRF-TOKEN', xsrfHeaderName: 'X-XSRF-TOKEN', maxContentLength: -1, maxBodyLength: -1, env: \[Object\], validateStatus: \[Function: validateStatus\], headers: \[Object \[AxiosHeaders\]\], caching: \[Object\], method: 'post', url: 'https://fitfile-prod.eu.auth0.com/oauth/token', data: '{"client\_id":"CzWFSi0mEbLJVG3vLaLVQtQnfwog0TBt","client\_secret":"slhvkIoi3Ae3-GVnODClCTcZQzLIeXP\_bhxn2Tyl35Fy9DnQ6qaCK9FvsX\_WMzQ2","audience":"https://fitfile-prod.eu.auth0.com/api/v2/","grant\_type":"client\_credentials"}', allowAbsoluteUrls: true }, request: ClientRequest { \_events: \[Object: null prototype\], \_eventsCount: 7, \_maxListeners: undefined, outputData: \[\], outputSize: 0, writable: true, destroyed: true, \_last: false, chunkedEncoding: false, shouldKeepAlive: true, maxRequestsOnConnectionReached: false, \_defaultKeepAlive: true, useChunkedEncodingByDefault: true, sendDate: false, \_removedConnection: false, \_removedContLen: false, \_removedTE: false, strictContentLength: false, \_contentLength: '220', \_hasBody: true, \_trailer: '', finished: true, \_headerSent: true, \_closed: true, \_header: 'POST /oauth/token HTTP/1.1\\r\\n' + 'Accept: application/json, text/plain, \*/\*\\r\\n' + 'Content-Type: application/json\\r\\n' + 'x-correlation-id: f88e55ec-506d-47c3-9978-85cfeb392cc5\\r\\n' + 'User-Agent: axios/1.12.2\\r\\n' + 'Content-Length: 220\\r\\n' + 'Accept-Encoding: gzip, compress, deflate, br\\r\\n' + 'Host: fitfile-prod.eu.auth0.com\\r\\n' + 'Connection: keep-alive\\r\\n' + '\\r\\n', \_keepAliveTimeout: 0, \_onPendingData: \[Function: nop\], agent: \[Agent\], socketPath: undefined, method: 'POST', maxHeaderSize: undefined, insecureHTTPParser: undefined, joinDuplicateHeaders: undefined, path: '/oauth/token', \_ended: true, res: \[IncomingMessage\], aborted: false, timeoutCb: null, upgradeOrConnect: false, parser: null, maxHeadersCount: null, reusedSocket: false, host: 'fitfile-prod.eu.auth0.com', protocol: 'https:', \_redirectable: \[Writable\], \[Symbol(shapeMode)\]: false, \[Symbol(kCapture)\]: false, \[Symbol(kBytesWritten)\]: 0, \[Symbol(kNeedDrain)\]: false, \[Symbol(corked)\]: 0, \[Symbol(kChunkedBuffer)\]: \[\], \[Symbol(kChunkedLength)\]: 0, \[Symbol(kSocket)\]: \[TLSSocket\], \[Symbol(kOutHeaders)\]: \[Object: null prototype\], \[Symbol(errored)\]: null, \[Symbol(kHighWaterMark)\]: 65536, \[Symbol(kRejectNonStandardBodyWrites)\]: false, \[Symbol(kUniqueHeaders)\]: null }, response: { status: 403, statusText: 'Forbidden', headers: \[Object \[AxiosHeaders\]\], config: \[Object\], request: \[ClientRequest\], data: \[Object\] }, status: 403 } } error Command failed. Exit code: 1 Command: /usr/local/bin/node Arguments: scripts/init.js Directory: /app Output: info Visit <https://yarnpkg.com/en/docs/cli/node> for documentation about this command. error Command failed with exit code 1. info Visit <https://yarnpkg.com/en/docs/cli/run> for documentation about this command. awsadmin@ip-10-66-2-4:~/terraform$ kubectl get secret ffcloud -n hie-test-34 -o jsonpath='{.data.auth\\.json}' | base64 -d; echo kubectl get secret ffcloud -n hie-test-34 -o jsonpath='{.data.cli-auth\\.json}' | base64 -d; echo {"clientId":"CzWFSi0mEbLJVG3vLaLVQtQnfwog0TBt","clientSecret":"slhvkIoi3Ae3-GVnODClCTcZQzLIeXP\_bhxn2Tyl35Fy9DnQ6qaCK9FvsX\_WMzQ2", "audience": "https://fitfile-prod.eu.auth0.com/api/v2/"} {"clientId":"CzWFSi0mEbLJVG3vLaLVQtQnfwog0TBt","clientSecret":"slhvkIoi3Ae3-GVnODClCTcZQzLIeXP\_bhxn2Tyl35Fy9DnQ6qaCK9FvsX\_WMzQ2", "audience": "https://fitfile-prod.eu.auth0.com/api/v2/"} awsadmin@ip-10-66-2-4:~/terraform$ kubectl describe pod -n hie-test-34 hie-test-34-ffcloud-service-67645976cc-2xh56 | sed -n '/Events:/,$p' kubectl describe pod -n hie-test-34 hie-test-34-ffcloud-service-6c69644b49-nclcz | sed -n '/Events:/,$p' Events: Type Reason Age From Message ---- ------ ---- ---- ------- Normal Scheduled 2m36s default-scheduler Successfully assigned hie-test-34/hie-test-34-ffcloud-service-67645976cc-2xh56 to ip-10-66-5-187.eu-west-2.compute.internal Normal Pulled 58s (x5 over 2m36s) kubelet Container image "fitfileregistry.azurecr.io/ffcloud-service:1.0.752" already present on machine Normal Created 58s (x5 over 2m36s) kubelet Created container: hie-test-34-ffcloud-service-init-db Normal Started 58s (x5 over 2m35s) kubelet Started container hie-test-34-ffcloud-service-init-db Warning BackOff 2s (x11 over 2m26s) kubelet Back-off restarting failed container hie-test-34-ffcloud-service-init-db in pod hie-test-34-ffcloud-service-67645976cc-2xh56\_hie-test-34(ebeb9934-484c-4d3f-84e2-bbae4d36b31b) Events: Type Reason Age From Message ---- ------ ---- ---- ------- Normal Scheduled 3m27s default-scheduler Successfully assigned hie-test-34/hie-test-34-ffcloud-service-6c69644b49-nclcz to ip-10-66-5-187.eu-west-2.compute.internal Normal Pulled 16s (x6 over 3m27s) kubelet Container image "fitfileregistry.azurecr.io/ffcloud-service:1.0.752" already present on machine Normal Created 16s (x6 over 3m27s) kubelet Created container: hie-test-34-ffcloud-service-init-db Normal Started 16s (x6 over 3m27s) kubelet Started container hie-test-34-ffcloud-service-init-db Warning BackOff 1s (x15 over 3m19s) kubelet Back-off restarting failed container hie-test-34-ffcloud-service-init-db in pod hie-test-34-ffcloud-service-6c69644b49-nclcz\_hie-test-34(17bed0a3-fdec-4248-a691-b5c1b7434206) awsadmin@ip-10-66-2-4:~/terraform$ kubectl logs -n hie-test-34 hie-test-34-fitconnect-ftc-5b4c975dcf-bb7m6 --previous kubectl logs -n hie-test-34 hie-test-34-fitconnect-ftc-5b4c975dcf-bb7m6 Defaulted container "hie-test-34-fitconnect-ftc" out of: hie-test-34-fitconnect-ftc, hie-test-34-fitconnect-ftc-init (init) {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-5b4c975dcf-bb7m6","pid":1,"level":30,"event":"application\_start","msg":"Initialising FITConnect application","time":"2026-02-12T09:41:25.664Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-5b4c975dcf-bb7m6","pid":1,"level":30,"event":"Mongo Client Instantiated","msg":"","time":"2026-02-12T09:41:25.684Z","v":0} (node:1) \[DEP0040\] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead. (Use `node --trace-deprecation …` to show where the warning was created) {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-5b4c975dcf-bb7m6","pid":1,"level":30,"msg":"Setting default connections","time":"2026-02-12T09:41:25.773Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-5b4c975dcf-bb7m6","pid":1,"level":30,"datasourceId":"19b4d43f-a264-429d-864c-9fb32ef750b5","msg":"Adding datasource to this tennant","time":"2026-02-12T09:41:25.800Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-5b4c975dcf-bb7m6","pid":1,"level":30,"datasourceId":"bdacecd7-b8fa-4be6-b75e-19b2934fb52f","msg":"Adding datasource to this tennant","time":"2026-02-12T09:41:25.838Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-5b4c975dcf-bb7m6","pid":1,"level":30,"datasourceId":"0e6c333c-0fd2-f3f1-4ef0-b61acb62e1a8","msg":"Adding datasource to this tennant","time":"2026-02-12T09:41:25.921Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-5b4c975dcf-bb7m6","pid":1,"level":30,"msg":"Default connections set","time":"2026-02-12T09:41:25.927Z","v":0} /app/infra/repositories/TenantRepo.js:52 throw new errors\_1.NotFound(`Tenant with id "${id.toValue()}" does not exist`); ^ NotFound: Tenant with id "CzWFSi0mEbLJVG3vLaLVQtQnfwog0TBt" does not exist at TenantRepo.findById (/app/infra/repositories/TenantRepo.js:52:19) at process.processTicksAndRejections (node:internal/process/task\_queues:105:5) at async LoadTenantSettingsUseCase.execute (/app/services/tenant/LoadTenantSettingsUseCase.js:13:24) at async Object.defaultBuildInfrastructure \[as buildInfrastructure\] (/app/infra/index.js:26:5) at async KoaApp.init (/app/KoaApp.js:30:31) at async /app/server.js:18:5 { status: 404 } Node.js v22.13.1 Defaulted container "hie-test-34-fitconnect-ftc" out of: hie-test-34-fitconnect-ftc, hie-test-34-fitconnect-ftc-init (init) {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-5b4c975dcf-bb7m6","pid":1,"level":30,"event":"application\_start","msg":"Initialising FITConnect application","time":"2026-02-12T09:41:25.664Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-5b4c975dcf-bb7m6","pid":1,"level":30,"event":"Mongo Client Instantiated","msg":"","time":"2026-02-12T09:41:25.684Z","v":0} (node:1) \[DEP0040\] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead. (Use `node --trace-deprecation …` to show where the warning was created) {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-5b4c975dcf-bb7m6","pid":1,"level":30,"msg":"Setting default connections","time":"2026-02-12T09:41:25.773Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-5b4c975dcf-bb7m6","pid":1,"level":30,"datasourceId":"19b4d43f-a264-429d-864c-9fb32ef750b5","msg":"Adding datasource to this tennant","time":"2026-02-12T09:41:25.800Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-5b4c975dcf-bb7m6","pid":1,"level":30,"datasourceId":"bdacecd7-b8fa-4be6-b75e-19b2934fb52f","msg":"Adding datasource to this tennant","time":"2026-02-12T09:41:25.838Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-5b4c975dcf-bb7m6","pid":1,"level":30,"datasourceId":"0e6c333c-0fd2-f3f1-4ef0-b61acb62e1a8","msg":"Adding datasource to this tennant","time":"2026-02-12T09:41:25.921Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-5b4c975dcf-bb7m6","pid":1,"level":30,"msg":"Default connections set","time":"2026-02-12T09:41:25.927Z","v":0} /app/infra/repositories/TenantRepo.js:52 throw new errors\_1.NotFound(`Tenant with id "${id.toValue()}" does not exist`); ^ NotFound: Tenant with id "CzWFSi0mEbLJVG3vLaLVQtQnfwog0TBt" does not exist at TenantRepo.findById (/app/infra/repositories/TenantRepo.js:52:19) at process.processTicksAndRejections (node:internal/process/task\_queues:105:5) at async LoadTenantSettingsUseCase.execute (/app/services/tenant/LoadTenantSettingsUseCase.js:13:24) at async Object.defaultBuildInfrastructure \[as buildInfrastructure\] (/app/infra/index.js:26:5) at async KoaApp.init (/app/KoaApp.js:30:31) at async /app/server.js:18:5 { status: 404 } Node.js v22.13.1

---

Good—you've moved forward. Now the failures are different and that's progress.

## 1) Ffcloud Init Failure: Auth0 Token Call now Has Creds, but Returns 403 Forbidden

Key line:

- POST `https://fitfile-prod.eu.auth0.com/oauth/token`
- `grant_type=client_credentials`
- `audience=https://fitfile-prod.eu.auth0.com/api/v2/`
- status 403

That usually means the client is valid, but not allowed to request that audience (or the app is not authorized for the Management API / missing proper grants/scopes). This is no longer "missing secret"; it's Auth0 configuration.

### What to Do next (kubectl + what to Ask the Auth0 Side to check)

#### A) Confirm Ffcloud is Using the Right Audience

Right now it is requesting the Management API audience (`/api/v2/`). If your init script only needs user lookup, that might be correct _only if_ this client is authorized for Mgmt API.

If this environment should be using a different audience (e.g. your own API identifier), it must change.

Since your values file has:

…this is likely intentional.

#### B) Get the Exact Error from Auth0 (it's in Response body)

Axios logged `data: [Object]` but not the contents. Grab it by re-running with more output is hard, but you can sometimes get it by turning on debug env; not possible here.

Instead: capture the response body from the init container logs with `--previous` (sometimes it prints the JSON error). Try:

If Auth0 returns something like:

- `access_denied`
- `unauthorized_client`
- `invalid_target`
	…that will tell you exactly what's wrong.

#### C) Auth0-side Fix (most likely)

Whoever manages Auth0 needs to ensure that this client (`client_id = CzWF…`) is:

- a Machine-to-Machine Application, and
- authorized to access Auth0 Management API, and
- granted the required scopes (at minimum often `read:users`, sometimes more depending on what `getUsersInfo` does).

In Auth0 UI this is typically under:

- Applications → (your M2M app) → APIs → Auth0 Management API → Authorized + scopes

If you don't want ffcloud init to depend on Mgmt API at all, the code needs changing (not kubectl).

### Meanwhile, Keep the Cluster from Thrashing

If you want to stop the loop while Auth0 is fixed:

(and scale back later)

---

## 2) Fitconnect Crash: it Can't Find a Tenant with Id = the Auth0 client\_id

This is super telling:

That ID is the same as your Auth0 client\_id. So fitconnect is using the Auth0 client\_id as a tenant identifier (or it's mis-reading tenant id from auth config).

This is almost certainly because the service expects something like:

- `tenantId` in config / secret
	…but it's pulling the wrong field (clientId).

### What to Check (kubectl)

#### A) Inspect Fitconnect Secret auth.json

If it contains only clientId/clientSecret/audience, then the app has no tenant id and is falling back to client\_id (bad default).

#### B) Inspect Fitconnect Configmap for Tenant Id Setting

Dump the configmap:

Search in it:

You're looking for something like `tenantId`, `TENANT_ID`, `FITFILE_TENANT_ID`, etc.

#### C) If Tenant is Meant to Be Seeded in Mongo, Check whether Ffcloud Init is Responsible for Creating it

Given ffcloud init is failing, it might be the component that creates the tenant record in Mongo. That would explain why fitconnect can't find the tenant.

So: fixing ffcloud init (Auth0 403) might unlock fitconnect if ffcloud init seeds the tenant.

---

## What to Do next in order

1. Fix Auth0 403 for the M2M client (`CzWF…`) against the Management API audience.
	- That's outside Kubernetes; it's Auth0 grants/scopes/authorized API access.
2. Once ffcloud init succeeds, re-test fitconnect:
	- If fitconnect still fails, then you need to provide an explicit tenant id (or seed tenant).

---

## Quick Commands to Run now

These will confirm the dependency chain:

### 1) Does Fitconnect Have a Tenant Id Configured Anywhere?

### 2) Does Ffcloud Init Error Include an Auth0 Error String?

If you paste those two outputs (redact secrets), I'll tell you whether fitconnect is blocked purely because ffcloud init hasn't created the tenant, or because fitconnect config is wrong.

---

kubectl logs -n hie-test-34 hie-test-34-ffcloud-service-6c69644b49-nclcz -c hie-test-34-ffcloud-service-init-db --previous | tail -n 80 shouldKeepAlive: true, maxRequestsOnConnectionReached: false, \_defaultKeepAlive: true, useChunkedEncodingByDefault: true, sendDate: false, \_removedConnection: false, \_removedContLen: false, \_removedTE: false, strictContentLength: false, \_contentLength: '220', \_hasBody: true, \_trailer: '', finished: true, \_headerSent: true, \_closed: true, \_header: 'POST /oauth/token HTTP/1.1\\r\\n' + 'Accept: application/json, text/plain, \*/\*\\r\\n' + 'Content-Type: application/json\\r\\n' + 'x-correlation-id: c77ce137-1c59-49da-ab7d-0335fd83893c\\r\\n' + 'User-Agent: axios/1.12.2\\r\\n' + 'Content-Length: 220\\r\\n' + 'Accept-Encoding: gzip, compress, deflate, br\\r\\n' + 'Host: fitfile-prod.eu.auth0.com\\r\\n' + 'Connection: keep-alive\\r\\n' + '\\r\\n', \_keepAliveTimeout: 0, \_onPendingData: \[Function: nop\], agent: \[Agent\], socketPath: undefined, method: 'POST', maxHeaderSize: undefined, insecureHTTPParser: undefined, joinDuplicateHeaders: undefined, path: '/oauth/token', \_ended: true, res: \[IncomingMessage\], aborted: false, timeoutCb: null, upgradeOrConnect: false, parser: null, maxHeadersCount: null, reusedSocket: false, host: 'fitfile-prod.eu.auth0.com', protocol: 'https:', \_redirectable: \[Writable\], \[Symbol(shapeMode)\]: false, \[Symbol(kCapture)\]: false, \[Symbol(kBytesWritten)\]: 0, \[Symbol(kNeedDrain)\]: false, \[Symbol(corked)\]: 0, \[Symbol(kChunkedBuffer)\]: \[\], \[Symbol(kChunkedLength)\]: 0, \[Symbol(kSocket)\]: \[TLSSocket\], \[Symbol(kOutHeaders)\]: \[Object: null prototype\], \[Symbol(errored)\]: null, \[Symbol(kHighWaterMark)\]: 65536, \[Symbol(kRejectNonStandardBodyWrites)\]: false, \[Symbol(kUniqueHeaders)\]: null }, response: { status: 403, statusText: 'Forbidden', headers: \[Object \[AxiosHeaders\]\], config: \[Object\], request: \[ClientRequest\], data: \[Object\] }, status: 403 } } error Command failed. Exit code: 1 Command: /usr/local/bin/node Arguments: scripts/init.js Directory: /app Output: info Visit <https://yarnpkg.com/en/docs/cli/node> for documentation about this command. error Command failed with exit code 1. info Visit <https://yarnpkg.com/en/docs/cli/run> for documentation about this command. kubectl get secret fitconnect -n hie-test-34 -o jsonpath='{.data.auth\\.json}' | base64 -d; echo {"clientId":"CzWFSi0mEbLJVG3vLaLVQtQnfwog0TBt","clientSecret":"slhvkIoi3Ae3-GVnODClCTcZQzLIeXP\_bhxn2Tyl35Fy9DnQ6qaCK9FvsX\_WMzQ2", "audience": "https://fitfile-prod.eu.auth0.com/api/v2/"} awsadmin@ip-10-66-2-4:~/terraform$ kubectl get configmap -n hie-test-34 hie-test-34-fitconnect-ftc-config-ce7e43b5d512c3d01a5cafdd2586b -o yaml apiVersion: v1 data: config.json: | { "allowedOrigin": ".\*\\\\.fitfile.net", "auditDbName": "audit", "auth": { "baseURL": "https://fitfile-prod.eu.auth0.com", "managementApiAudience": "https://fitfile-prod.eu.auth0.com/api/v2/" }, "basePath": "/fitconnect", "dbName": "fitconnect", "eventDbName": "events", "featureFlags": { "exportToS3": true, "omopAndExportToS3": true }, "ffCloudDbName": "ffcloud", "ffCloudHosts": \[\], "ffcloudGraphQLUri": "https://app.eoe-test-codisc.privatelink.fitfile.net/ffcloud/graphql", "fileUpload": { "chunkSize": 1000, "inferenceLimit": 5000, "keepUploads": false, "maxSize": 100000000, "path": "" }, "fileUploadSqlDb": { "host": "hie-test-34-postgresql-0.hie-test-34-postgresql-hl.hie-test-34.svc.cluster.local", "id": "0e6c333c-0fd2-f3f1-4ef0-b61acb62e1a8", "name": "fitconnect" }, "fitConnectCode": "EOE SDE CODISC", "healthWindow": 168, "logLevel": "info", "optout": { "enabled": false }, "port": 4000, "s3": { "endpoint": "http://hie-test-34-minio.hie-test-34.svc.cluster.local:9000" }, "schemaDbName": "schemas", "skipQuerySchemaValidation": false, "spicedb": { "insecure": true, "uri": "spicedb.spicedb:50051" }, "tenant": { "baseUrl": "http://hie-test-34-fitconnect-ftc/fitconnect", "name": "Default" }, "workflows": { "workflowsApiBaseUrl": "http://workflows-api" } } immutable: true kind: ConfigMap metadata: annotations: argocd.argoproj.io/tracking-id: hie-test-34-fitconnect:/ConfigMap:hie-test-34/hie-test-34-fitconnect-ftc-config-ce7e43b5d512c3d01a5cafdd2586b kubectl.kubernetes.io/last-applied-configuration: | {"apiVersion":"v1","data":{"config.json":"{\\n \\"allowedOrigin\\": \\".\*\\\\\\\\.fitfile.net\\",\\n \\"auditDbName\\": \\"audit\\",\\n \\"auth\\": {\\n \\"baseURL\\": \\"<https://fitfile-prod.eu.auth0.com>\\",\\n \\"managementApiAudience\\": \\"<https://fitfile-prod.eu.auth0.com/api/v2/>\\"\\n },\\n \\"basePath\\": \\"/fitconnect\\",\\n \\"dbName\\": \\"fitconnect\\",\\n \\"eventDbName\\": \\"events\\",\\n \\"featureFlags\\": {\\n \\"exportToS3\\": true,\\n \\"omopAndExportToS3\\": true\\n },\\n \\"ffCloudDbName\\": \\"ffcloud\\",\\n \\"ffCloudHosts\\": \[\],\\n \\"ffcloudGraphQLUri\\": \\"<https://app.eoe-test-codisc.privatelink.fitfile.net/ffcloud/graphql>\\",\\n \\"fileUpload\\": {\\n \\"chunkSize\\": 1000,\\n \\"inferenceLimit\\": 5000,\\n \\"keepUploads\\": false,\\n \\"maxSize\\": 100000000,\\n \\"path\\": \\"\\"\\n },\\n \\"fileUploadSqlDb\\": {\\n \\"host\\": \\"hie-test-34-postgresql-0.hie-test-34-postgresql-hl.hie-test-34.svc.cluster.local\\",\\n \\"id\\": \\"0e6c333c-0fd2-f3f1-4ef0-b61acb62e1a8\\",\\n \\"name\\": \\"fitconnect\\"\\n },\\n \\"fitConnectCode\\": \\"EOE SDE CODISC\\",\\n \\"healthWindow\\": 168,\\n \\"logLevel\\": \\"info\\",\\n \\"optout\\": {\\n \\"enabled\\": false\\n },\\n \\"port\\": 4000,\\n \\"s3\\": {\\n \\"endpoint\\": \\"<http://hie-test-34-minio.hie-test-34.svc.cluster.local:9000>\\"\\n },\\n \\"schemaDbName\\": \\"schemas\\",\\n \\"skipQuerySchemaValidation\\": false,\\n \\"spicedb\\": {\\n \\"insecure\\": true,\\n \\"uri\\": \\"spicedb.spicedb:50051\\"\\n },\\n \\"tenant\\": {\\n \\"baseUrl\\": \\"http://hie-test-34-fitconnect-ftc/fitconnect\\",\\n \\"name\\": \\"Default\\"\\n },\\n \\"workflows\\": {\\n \\"workflowsApiBaseUrl\\": \\"http://workflows-api\\"\\n }\\n}\\n"},"immutable":true,"kind":"ConfigMap","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"hie-test-34-fitconnect:/ConfigMap:hie-test-34/hie-test-34-fitconnect-ftc-config-ce7e43b5d512c3d01a5cafdd2586b"},"name":"hie-test-34-fitconnect-ftc-config-ce7e43b5d512c3d01a5cafdd2586b","namespace":"hie-test-34"}} creationTimestamp: "2026-02-11T16:22:16Z" name: hie-test-34-fitconnect-ftc-config-ce7e43b5d512c3d01a5cafdd2586b namespace: hie-test-34 resourceVersion: "521538" uid: fd18c39f-b210-44bc-99f2-891e11c1124f

---

Nice, we've got enough to call it:

## Ffcloud: 403 on /oauth/token means Auth0 is Rejecting This M2M Client for the Management API

You're now sending a _valid_ client\_id/secret and the correct Management API audience (`https://fitfile-prod.eu.auth0.com/api/v2/`), but Auth0 returns 403 Forbidden.

That's almost always one of:

- the client is not authorized for the "Auth0 Management API" (M2M app not toggled on for that API), or
- it's authorized but has no scopes (or the wrong grant), or
- the client is for a different tenant / connection / environment than `fitfile-prod.eu`.

### What to Ask / Check in Auth0 (actionable)

In Auth0 dashboard:

1. Applications → (the M2M app with client id `CzWF…`)
2. APIs tab → find Auth0 Management API
3. Ensure it's Authorized and grant scopes (minimum usually `read:users`; whatever your init needs).

If you have Auth0 Management API access via UI/terraform, this is the fix. Kubernetes can't "kubectl" its way around a 403 from Auth0.

### Optional: Keep the Cluster from Thrashing while Auth0 is Fixed

---

## Fitconnect: It's Using the Auth0 client\_id as the Tenant Id, and that Tenant Doesn't Exist

Your fitconnect secret `auth.json` is:

Your fitconnect configmap has `tenant.name` and `tenant.baseUrl`, but no tenant id. So the service tries to load tenant settings and ends up using `clientId` as the tenant identifier → then:

> Tenant with id "CzWF…" does not exist

This strongly suggests tenant creation/seeding hasn't happened (and it might be done by ffcloud init—which is currently blocked by Auth0 403).

### Likely Dependency Chain

ffcloud init needs Auth0 Mgmt API to look up/create initial users/tenant metadata → it fails → tenant record never created in Mongo → fitconnect can't find tenant → it fails.

So: fix Auth0 403 first, then re-run.

---

## Best next Kubectl Checks (to Confirm Tenant Missing in Mongo)

## 1) See Which Mongo DB/URI Fitconnect is Using (from secret)

Your fitconnect secret doesn't include mongodb.json (only `mongodb` connection string key in the VSS template). List keys:

If it has a `mongodb` key, print it (it's a URI; redact password):

## 2) Query Mongo for Tenants (quick & dirty)

If your mongodb pod has `mongosh`, you can exec and query. Try:

Then check the fitconnect DB for tenants (db name is `fitconnect` from configmap):

If there's a `tenants` collection:

(If auth is enabled on Mongo you'll need creds; those are in your `mongodb.json` in the `ffcloud` secret.)

---

## What You Should Change in Vault Secrets (based on what We see)

Right now you're using cli creds to call the Auth0 Management API. That's probably not what you intended. You likely need a dedicated M2M client that's authorized for Mgmt API.

So either:

- update Vault keys `auth0_client_id/auth0_client_secret` to a proper M2M that has Mgmt API scopes, and keep cli keys separate, or
- authorize the existing cli client `CzWF…` for Mgmt API (quick fix, but arguably wrong separation of concerns).

---

## TL;DR Next Actions

1. Fix Auth0: authorize client `CzWF…` to call Management API (audience `/api/v2/`) with needed scopes → ffcloud init will pass.
2. Recreate/restart ffcloud → it should seed tenant.
3. Restart fitconnect → tenant lookup should succeed.

If you can run the Mongo queries above and paste whether `tenants` exists / is empty, we can confirm the dependency chain completely.

---

---

Yep—that's the root cause.

Your pods are calling:

- `https://fitfile-prod.eu.auth0.com/oauth/token`
- audience `https://fitfile-prod.eu.auth0.com/api/v2/`

…but your client belongs to the test tenant:

- `https://fitfile-test.eu.auth0.com/oauth/token`
- audience `https://fitfile-test.eu.auth0.com/api/v2/`

So Auth0 is correctly rejecting it (403) when you hit the prod tenant with a test client (or when the audience/issuer doesn't match).

## What to Change

You need the baseURL and managementApiAudience to point at `fitfile-test.eu.auth0.com` (or you need prod credentials that match prod).

Right now your values file hardcodes prod:

and your configmap for fitconnect is also prod:

### Fix in Git (recommended, since Argo Manages it)

Update those two values to `fitfile-test`:

Then let Argo sync (or you sync it), and restart the deployments:

## Immediate Tactical Fix (if You Can't Wait for Git/Argo)

Patch the ConfigMap (but note: yours is `immutable: true`, so you can't patch it—you must change the chart values and redeploy).

You _can_ confirm ffcloud uses the same config source by grepping its configmap:

I expect you'll see `fitfile-prod` in there too.

## After You Flip to Fitfile-test

- ffcloud init should be able to obtain a token (no more 403)
- it can then seed whatever tenant/user data is needed
- fitconnect's "Tenant … does not exist" should likely resolve after ffcloud init succeeds (or at least change to a more informative next error)

If you paste the ffcloud configmap grep output above, I'll tell you exactly which rendered object is driving ffcloud's Auth0 URL (so you update the right values once).

---

create a wiki page about this bug and the root cause. list the commands used and why. I want it as a playbook for other deployments that might have these symptoms so I can check these things quicker next time

---

Writing

---

## FF Deployment Failure Playbook

Issue:`ffcloud` / `fitconnect` CrashLoopBackOff during new environment deployment

Last Updated: 2026-02-12

Applies To: HIE / FFNode deployments using Vault Secrets Operator + Auth0 M2M authentication

---

## 🔎 Summary

New deployments may fail with:

- `ffcloud-service` stuck in `Init:CrashLoopBackOff`
- `fitconnect-ftc` in `CrashLoopBackOff`
- Auth0 token errors (`401` → later `403`)
- Errors referencing Tenant not found
- Secrets appear present but services still fail to start

Root Cause:

Deployment was configured to use Auth0 PROD endpoints while Vault supplied TEST tenant credentials.

This tenant mismatch caused Auth0 to reject token requests, preventing `ffcloud` initialization, which in turn prevented tenant seeding required by `fitconnect`.

---

## 🧠 Architecture Dependency (Why This Breaks Everything)

Startup order is critical:

```markdown
Vault → Kubernetes Secret → ffcloud init → Tenant seeded in Mongo → fitconnect starts
```

If `ffcloud` cannot authenticate with Auth0:

- Init fails ❌
- Tenant never created ❌
- `fitconnect` cannot find tenant ❌
- Whole deployment appears broken ❌

This is not a Kubernetes failure—it is an identity configuration mismatch.

---

## 🚨 Symptoms

| Component | Symptom | Meaning |
| --- | --- | --- |
| ffcloud init | `AuthTokenDecodeError` | Cannot authenticate to Auth0 |
| Auth0 response | `401 Unauthorized` | Secret missing / wrong |
| Auth0 response | `403 Forbidden` | Correct secret, wrong tenant / audience |
| fitconnect | `Tenant with id "<client_id>" does not exist` | ffcloud never seeded tenant |
| Pods | Restarting endlessly | Init dependency failing |

---

## 🔍 Investigation Steps (Run in Order)

---

### 1️⃣ Check Pod State

```markdown
kubectl get pods -n <namespace>
```

Look for:

- `Init:CrashLoopBackOff`
- `Error`
- Repeated restarts

---

### 2️⃣ Inspect Ffcloud Init Logs (Most Important Signal)

```markdown
kubectl logs -n <ns> <ffcloud-pod> -c <init-container>
kubectl logs -n <ns> <ffcloud-pod> -c <init-container> --previous
```

Example failure:

```markdown
POST https://fitfile-prod.eu.auth0.com/oauth/token
status: 403 Forbidden
```

➡️ Indicates Auth0 mismatch—NOT Kubernetes issue.

---

### 3️⃣ Confirm Secrets Rendered by Vault

```markdown
kubectl get secret ffcloud -n <ns> \
  -o jsonpath='{.data.auth\.json}' | base64 -d; echo
```

Verify values exist:

```markdown
clientId
clientSecret
audience
```

If empty → Vault template problem.

If populated → move to Auth0 validation.

---

### 4️⃣ Validate VaultStaticSecret Mapping

```markdown
kubectl get vaultstaticsecrets -n <ns>
kubectl get vaultstaticsecret ffcloud -n <ns> -o yaml
```

Check template references:

```markdown
{{ get .Secrets "auth0_client_id" }}
{{ get .Secrets "auth0_client_secret" }}
```

Ensure keys exist in Vault path:

```markdown
admin/deployments/<deployment>/application
```

---

### 5️⃣ Verify Auth0 Endpoint Matches Credential Tenant

Manually test token request using Vault credentials:

```markdown
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

```markdown
kubectl get configmap -n <ns> <fitconnect-config> -o yaml
```

Look for:

```markdown
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

| System | Value |
| --- | --- |
| Vault | TEST Auth0 credentials |
| Helm Values | PROD Auth0 URLs |
| Application | Uses Helm-rendered URLs |
| Auth0 | Rejects cross-tenant token exchange |

Auth0 correctly rejects the request because client IDs are tenant-scoped.

---

## ✅ Resolution

Update Helm values to match the tenant where the credentials live.

### Fix in Deployment Values

```markdown
global:
  oauth:
    baseURL: "https://fitfile-test.eu.auth0.com"
    managementApiAudience: "https://fitfile-test.eu.auth0.com/api/v2/"
```

Commit → ArgoCD sync → redeploy.

---

### Restart Services After Fix

```markdown
kubectl rollout restart deployment <ffcloud> -n <ns>
kubectl rollout restart deployment <fitconnect> -n <ns>
```

---

## ✔️ Expected Healthy Behaviour

After fix:

| Step | Result |
| --- | --- |
| ffcloud init | Completes successfully |
| Mongo | Tenant created |
| fitconnect | Starts normally |
| Pods | `READY 1/1` |
| No more CrashLoops | Stable deployment |

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

```markdown
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

```markdown
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

---

now the pods say running but the arogcd says outOfSync kubectl get applications -n argocd NAME SYNC STATUS HEALTH STATUS argo-workflows Synced Healthy cert-manager Synced Healthy ff-hie-test-34 OutOfSync Degraded grafana-k8s-monitoring Synced Healthy hie-test-34-ffcloud-service Synced Healthy hie-test-34-fitconnect OutOfSync Healthy hie-test-34-minio Synced Healthy hie-test-34-mongodb-b17ef Synced Healthy hie-test-34-postgresql Synced Healthy hie-test-34-workflow-templates Synced Healthy hie-test-34-workflows-api Synced Healthy prometheus-operator-crds Synced Healthy spicedb Synced Healthy awsadmin@ip-10-66-2-4:~/terraform$ kubectl get pods -n hie-test-34 NAME READY STATUS RESTARTS AGE hie-test-34-ffcloud-service-86b45f4c8c-sqg8x 3/3 Running 1 (12m ago) 13m hie-test-34-fitconnect-ftc-845b98ddd7-bkvxh 1/1 Running 0 3m36s hie-test-34-minio-6b9779bb4b-gnsb8 1/1 Running 0 20h hie-test-34-minio-provisioning-88sn8 0/1 Completed 0 20h hie-test-34-mongodb-b17ef-0 2/2 Running 0 12m hie-test-34-mongodb-b17ef-arbiter-0 1/1 Running 0 20h hie-test-34-postgresql-0 1/1 Running 0 20h workflows-api-5bd448f79-78szp 1/1 Running 0 20h

---

Pods running ✅ means the _runtime_ state is healthy now. Argo OutOfSync just means "what's in the cluster differs from what Git says should be there." That's totally expected if you hot-fixed anything (kubectl patch, edited secrets in Vault, manual restarts, etc.).

Here's the fastest way to see _exactly what_ is OutOfSync and decide whether to sync, revert, or make Git match reality.

## 1) See the Exact Diff Argo is Complaining about (kubectl-only)

Start with the two OutOfSync apps:

Often the `status.operationState.message` or `status.conditions[]` tells you "resource X differs".

If you want a more direct "which resources are OutOfSync" list:

Look for lines where `sync=OutOfSync`.

## 2) For Each OutOfSync Resource, Diff it Locally

Pick the specific resource(s) Argo flags and run:

Then compare against the desired manifest from git (depends on how you deploy; if you don't have argocd CLI, simplest is to re-render helm locally from the same chart + values file, or just trust Argo and sync).

## 3) Decide the Right Action

### If Your Fix Was "real" and Should Persist

Make Git match reality (update the deployment repo values file / chart) and let Argo sync cleanly.

This is the right choice if you changed:

- Auth0 baseURL / audience values
- Vault secret keys / templates
- anything that should be the permanent config for this environment

### If Your Fix Was a Temporary Emergency Patch

Let Argo sync and revert to Git (but you might re-break the deployment).

### If It's just "noise" (common)

Argo can show OutOfSync due to things like:

- `kubectl rollout restart` (changes pod template annotation)
- auto-generated fields (`status`, `resourceVersion`)
- operators adding annotations/labels
- immutable configmaps being recreated with a new hash name

In that case, you can either:

- Sync to re-apply desired state, or
- add ignoreDifferences rules in the Argo app (best if it keeps happening)

## 4) Quick Likely Causes in Your Specific case

Given your earlier debugging path, the common drift sources are:

- You changed secrets in Vault (now rendered content differs from what Argo expects)
- You patched a `VaultStaticSecret` / destination secret (or changed overwrite behaviour)
- You changed Auth0 URLs somewhere (values/configmap) but didn't commit it to the deployment repo
- `ff-hie-test-34` is Degraded even though pods are Running—that often means:
	- an Argo Hook/Job failed,
	- or an init Job/Workflow template resource is failing,
	- or Argo thinks a required resource is missing

## 5) One Command to Reveal why Ff-hie-test-34 is Degraded

Do the same for fitconnect:

## 6) If You just want to "make Argo green" Safely

Don't blindly sync `ff-hie-test-34` until you know what it wants to revert.

But you _can_ sync the fitconnect app if it's OutOfSync but Healthy:

(That forces a refresh; actual sync normally done via Argo UI/CLI. With kubectl alone you can't "sync" unless you patch the app spec to include automated sync, but I wouldn't do that without seeing the diff.)

---

### Paste These Two Outputs and I'll Tell You Exactly what Changed

(That will pinpoint which resource is OutOfSync/Degraded and what Argo is unhappy about.)

---

kubectl get pods -n hie-test-34 NAME READY STATUS RESTARTS AGE hie-test-34-ffcloud-service-86b45f4c8c-sqg8x 3/3 Running 1 (12m ago) 13m hie-test-34-fitconnect-ftc-845b98ddd7-bkvxh 1/1 Running 0 3m36s hie-test-34-minio-6b9779bb4b-gnsb8 1/1 Running 0 20h hie-test-34-minio-provisioning-88sn8 0/1 Completed 0 20h hie-test-34-mongodb-b17ef-0 2/2 Running 0 12m hie-test-34-mongodb-b17ef-arbiter-0 1/1 Running 0 20h hie-test-34-postgresql-0 1/1 Running 0 20h workflows-api-5bd448f79-78szp 1/1 Running 0 20h awsadmin@ip-10-66-2-4:~/terraform$ kubectl logs hie-test-34-fitconnect-ftc-845b98ddd7-bkvxh -n hie-test-34 Defaulted container "hie-test-34-fitconnect-ftc" out of: hie-test-34-fitconnect-ftc, hie-test-34-fitconnect-ftc-init (init) {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-845b98ddd7-bkvxh","pid":1,"level":30,"event":"application\_start","msg":"Initialising FITConnect application","time":"2026-02-12T13:01:33.668Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-845b98ddd7-bkvxh","pid":1,"level":30,"event":"Mongo Client Instantiated","msg":"","time":"2026-02-12T13:01:33.684Z","v":0} (node:1) \[DEP0040\] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead. (Use `node --trace-deprecation …` to show where the warning was created) {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-845b98ddd7-bkvxh","pid":1,"level":30,"msg":"Setting default connections","time":"2026-02-12T13:01:33.751Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-845b98ddd7-bkvxh","pid":1,"level":30,"datasourceId":"19b4d43f-a264-429d-864c-9fb32ef750b5","msg":"Adding datasource to this tennant","time":"2026-02-12T13:01:33.782Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-845b98ddd7-bkvxh","pid":1,"level":30,"datasourceId":"bdacecd7-b8fa-4be6-b75e-19b2934fb52f","msg":"Adding datasource to this tennant","time":"2026-02-12T13:01:33.821Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-845b98ddd7-bkvxh","pid":1,"level":30,"datasourceId":"0e6c333c-0fd2-f3f1-4ef0-b61acb62e1a8","msg":"Adding datasource to this tennant","time":"2026-02-12T13:01:33.827Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-845b98ddd7-bkvxh","pid":1,"level":30,"msg":"Default connections set","time":"2026-02-12T13:01:33.833Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-845b98ddd7-bkvxh","pid":1,"level":30,"event":"Cron Scheduler Instantiated","msg":"","time":"2026-02-12T13:01:33.850Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-845b98ddd7-bkvxh","pid":1,"level":30,"event":"started\_mediator","msg":"Started FITConnect mediator","time":"2026-02-12T13:01:33.908Z","v":0} {"name":"fitconnect","hostname":"hie-test-34-fitconnect-ftc-845b98ddd7-bkvxh","pid":1,"level":30,"cron":"0 \* \* \* \*","taskName":"data\_source\_sync\_all","singleton":true,"msg":"Registering scheduled task","time":"2026-02-12T13:01:33.909Z","v":0} {"name":"Fitconnect","hostname":"hie-test-34-fitconnect-ftc-845b98ddd7-bkvxh","pid":1,"level":30,"event":"Server Lifecycle","port":4000,"host":"0.0.0.0","env":"production","msg":"FITConnect Server Accepting Connections","time":"2026-02-12T13:01:33.923Z","v":0} awsadmin@ip-10-66-2-4:~/terraform$ kubectl get application -n argocd hie-test-34-fitconnect -o jsonpath='{range.status.resources\[\*\]}{.kind}{" "}{.namespace}{" "}{.name}{" sync="}{.status}{" health="}{.health.status}{"\\n"}{end}' ConfigMap hie-test-34 fitconnect-load-definition sync=Synced health= ConfigMap hie-test-34 hie-test-34-fitconnect-ftc-config-3ad7d286319b68f329e68a5b45f8d sync=Synced health= ConfigMap hie-test-34 hie-test-34-fitconnect-ftc-config-ce7e43b5d512c3d01a5cafdd2586b sync=OutOfSync health= Service hie-test-34 hie-test-34-fitconnect-ftc sync=Synced health= Deployment hie-test-34 hie-test-34-fitconnect-ftc sync=Synced health= Ingress hie-test-34 hie-test-34-fitconnect-ftc-ingress sync=Synced health= VaultStaticSecret hie-test-34 fitconnect sync=Synced health= awsadmin@ip-10-66-2-4:~/terraform$ kubectl get application -n argocd ff-hie-test-34 -o jsonpath='{range.status.conditions\[\*\]}{.type}{" "}{.reason}{" "}{.message}{"\\n"}{end}' SyncError Failed sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9: one or more synchronization tasks completed unsuccessfully (retried 5 times). awsadmin@ip-10-66-2-4:~/terraform$ kubectl get application -n argocd hie-test-34-fitconnect -o jsonpath='{range.status.conditions\[\*\]}{.type}{" "}{.reason}{" "}{.message}{"\\n"}{end}' SyncError Failed sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9: one or more synchronization tasks completed unsuccessfully (retried 5 times). awsadmin@ip-10-66-2-4:~/terraform$ kubectl annotate application -n argocd hie-test-34-fitconnect argocd.argoproj.io/refresh=hard --overwrite application.argoproj.io/hie-test-34-fitconnect annotated awsadmin@ip-10-66-2-4:~/terraform$ kubectl get application -n argocd ff-hie-test-34 -o jsonpath='{range.status.resources\[\*\]}{.kind}{" "}{.namespace}{" "}{.name}{" sync="}{.status}{" health="}{.health.status}{"\\n"}{end}' kubectl get application -n argocd ff-hie-test-34 -o jsonpath='{range.status.conditions\[\*\]}{.type}{" "}{.reason}{" "}{.message}{"\\n"}{end}' Application argocd argo-workflows sync=Synced health= Application argocd cert-manager sync=Synced health= Application argocd certificates sync=OutOfSync health= Application argocd grafana-k8s-monitoring sync=Synced health= Application argocd hie-test-34-ffcloud-service sync=Synced health= Application argocd hie-test-34-fitconnect sync=Synced health= Application argocd hie-test-34-frontend sync=OutOfSync health= Application argocd hie-test-34-minio sync=Synced health= Application argocd hie-test-34-mongodb-b17ef sync=Synced health= Application argocd hie-test-34-postgresql sync=Synced health= Application argocd hie-test-34-workflow-templates sync=Synced health= Application argocd hie-test-34-workflows-api sync=Synced health= Application argocd prometheus-operator-crds sync=Synced health= Application argocd spicedb sync=Synced health= SyncError Failed sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9: one or more synchronization tasks completed unsuccessfully (retried 5 times).

---

Nice, this is very readable now.

### What's Actually Going on

1. `hie-test-34-fitconnect` OutOfSync is just one old ConfigMap
	You've got two fitconnect configmaps:
- `…-config-3ad7d…` ✅ Synced
- `…-config-ce7e…` ❌ OutOfSync

That old `ce7e…` one is the immutable configmap from before you fixed Auth0. It's hanging around, and Argo is trying (and failing) to reconcile it.

This is usually safe to delete if it's not referenced by anything anymore.

1. `ff-hie-test-34` Degraded is because Argo thinks some child apps/resources failed sync
	Your `ff-hie-test-34` app is an "app-of-apps" (it lists Application resources like `hie-test-34-frontend`, `certificates`, etc.). It's showing OutOfSync for:
- `certificates` (Application) OutOfSync
- `hie-test-34-frontend` (Application) OutOfSync

So even though the core pods are running, the parent app is still unhappy because some child apps aren't synced (and earlier it retried and gave up).

---

## Fix Fitconnect OutOfSync (clean up the Stale Immutable ConfigMap)

### 1) Prove Nothing References the Old Configmap

Check if any deployment references it:

If that `ce7e…` name is NOT referenced, it's orphaned.

### 2) Delete the Stale Configmap

### 3) Refresh Argo

That should make `hie-test-34-fitconnect` go Synced.

---

## Fix the Parent App Ff-hie-test-34 Degraded (focus on the Child apps)

You already saw which child apps are OutOfSync:

- `certificates`
- `hie-test-34-frontend`

### 1) Get Exactly what Resources Are OutOfSync inside Each Child App

Run:

### 2) And Grab the Failure Reason (usually Tells You Exactly what Apply failed)

Common causes:

- immutable object changed (ConfigMap/Secret) → Argo can't patch it
- resource already exists with different owner/labels
- CRD mismatch
- certificate resource failing admission

### 3) After Fixing Those, Refresh the Parent

---

## Why Argo Says "Failed Sync Attempt … Retried 5 times"

That's almost always "apply failed" rather than a drift-only OutOfSync. The conditions you posted confirm it.

Deleting orphaned immutable configmaps is the 1 fix when you see:

- old hashed configmap OutOfSync
- new hashed configmap Synced
- deployment is healthy/running

---

## Quick "make it green" Checklist

1. Delete unused immutable old configmaps/secrets that Argo can't mutate.
2. Refresh child apps (`certificates`, `frontend`) and resolve their specific sync errors.
3. Refresh parent (`ff-hie-test-34`).

---

If you paste the outputs from the two child apps (`certificates` + `hie-test-34-frontend`) resource lists + conditions, I'll tell you the exact remediation (it's usually one stale immutable thing or a cert object with changed spec).

---

create a playbook wiki page with the commands for rereshing various argocd resources for when debugging

---

Writing

---

## Argo CD Refresh & Debug Playbook (kubectl-first)

Purpose: Quick commands to refresh Argo CD Applications and identify why they are `OutOfSync`, `Degraded`, or stuck on failed sync attempts—using only `kubectl` (no argocd CLI required).

Scope: Clusters where Argo CD is installed in `argocd` namespace and Applications are CRs (`application.argoproj.io`).

---

## 0) Quick Mental Model

Argo evaluates an Application by:

1. Reading desired state (Git/Helm/Kustomize)
2. Comparing to live state in the cluster
3. Reporting:
- `sync.status`: `Synced | OutOfSync | Unknown`
- `health.status`: `Healthy | Degraded | Progressing | Missing | Unknown`
- conditions explaining failures (e.g., `SyncError`, `ComparisonError`)

A "Refresh" tells Argo to re-run comparison right now.

---

## 1) List Applications + Current Status

```markdown
kubectl get applications -n argocd
```

If you want a concise table-like view with sync/health:

```markdown
kubectl get applications -n argocd \
  -o custom-columns=NAME:.metadata.name,SYNC:.status.sync.status,HEALTH:.status.health.status \
  --no-headers
```

---

## 2) Force Argo to Refresh an Application

### Soft Refresh (often enough)

```markdown
kubectl annotate application -n argocd <app-name> argocd.argoproj.io/refresh=normal --overwrite
```

### Hard Refresh (best when Debugging drift)

```markdown
kubectl annotate application -n argocd <app-name> argocd.argoproj.io/refresh=hard --overwrite
```

Why:

- `normal` refreshes the app status and comparison.
- `hard` forces a deeper refresh (use when Argo seems stale).

---

## 3) Show Exactly what Resources Are OutOfSync

This prints every tracked resource and its per-resource sync/health:

```markdown
kubectl get application -n argocd <app-name> \
  -o jsonpath='{range .status.resources[*]}{.kind}{" "}{.namespace}{" "}{.name}{"  sync="}{.status}{"  health="}{.health.status}{"\n"}{end}'
```

Why:

When an app is OutOfSync, this tells you which specific resources are causing it.

---

## 4) Show Application Conditions (why Sync Failed / degraded)

```markdown
kubectl get application -n argocd <app-name> \
  -o jsonpath='{range .status.conditions[*]}{.type}{"  "}{.reason}{"  "}{.message}{"\n"}{end}'
```

Why:

This is where you'll see messages like:

- `SyncError Failed sync attempt …`
- `ComparisonError …`
- admission webhook failures
- immutable field errors
- missing resources / RBAC issues

---

## 5) Show Last Operation State (most Useful for "Failed Sync attempt")

```markdown
kubectl get application -n argocd <app-name> -o yaml | \
  sed -n '/operationState:/,/^status:/p'
```

If you want only the message:

```markdown
kubectl get application -n argocd <app-name> \
  -o jsonpath='{.status.operationState.message}{"\n"}'
```

Why:

`operationState` often includes the clearest "what failed to apply and why".

---

## 6) Quickly Identify "app-of-apps" (parent Apps Managing Child apps)

If the resources list contains many `Application argocd <child-app>`, then it's a parent app.

List child apps tracked by a parent:

```markdown
kubectl get application -n argocd <parent-app> \
  -o jsonpath='{range .status.resources[?(@.kind=="Application")]}{.name}{"  sync="}{.status}{"  health="}{.health.status}{"\n"}{end}'
```

Why:

Parent apps can be `Degraded` even when workloads run, because a _child app_ is OutOfSync or failed sync.

---

## 7) Refresh Everything in a "deployment bundle" (common workflow)

Example: if `<parent-app>` is an app-of-apps:

```markdown
# Refresh parent
kubectl annotate application -n argocd <parent-app> argocd.argoproj.io/refresh=hard --overwrite

# Refresh all child apps listed by the parent (manual loop)
kubectl get application -n argocd <parent-app> \
  -o jsonpath='{range .status.resources[?(@.kind=="Application")]}{.name}{"\n"}{end}'
```

Then refresh each child:

```markdown
kubectl annotate application -n argocd <child-app> argocd.argoproj.io/refresh=hard --overwrite
```

Why:

Parent status may not clear until children re-compare cleanly.

---

## 8) Common "OutOfSync but Pods Are running" Causes + what to Check

### A) Immutable ConfigMap/Secret Rotated / Replaced

Symptoms:

- old hashed ConfigMap shows `OutOfSync`
- new hashed ConfigMap shows `Synced`
- workload is healthy

Find what's OutOfSync (Section 3), then verify it's referenced:

```markdown
kubectl get deploy -n <ns> <deploy> -o yaml | grep -n '<old-configmap-name>\|configMap'
```

If not referenced, it's orphaned and safe to delete:

```markdown
kubectl delete configmap -n <ns> <old-configmap-name>
kubectl annotate application -n argocd <app> argocd.argoproj.io/refresh=hard --overwrite
```

### B) Operator-managed Resources Mutate Live State

Examples: cert-manager, external-secrets, vault-secrets-operator, etc.

Argo can show drift due to auto-added annotations/labels.

Check the exact drifted resource from Section 3 and decide:

- allow drift (ignoreDifferences), or
- make Git match operator behaviour, or
- accept Argo re-apply.

---

## 9) Quick "what's different?" Checks (live Resource introspection)

Once you know the drifting resource from Section 3:

```markdown
kubectl get <kind> -n <ns> <name> -o yaml
```

Useful focused greps:

```markdown
kubectl get <kind> -n <ns> <name> -o yaml | egrep -n 'annotations:|labels:|image:|env:|configMapRef:|secretRef:'
```

Why:

This helps identify whether drift is a real config change or just metadata noise.

---

## 10) Optional: Server-side "force re-evaluation" via Restart (workload-level)

This doesn't change Argo sync status, but can help when you fixed a secret/config and need pods to pick it up:

```markdown
kubectl rollout restart deployment -n <ns> <deployment-name>
```

---

## 11) Copy/paste "Debug Bundle" Template

Replace `<app>` and run:

```markdown
# 1) Refresh app
kubectl annotate application -n argocd <app> argocd.argoproj.io/refresh=hard --overwrite

# 2) List resources and their sync/health
kubectl get application -n argocd <app> \
  -o jsonpath='{range .status.resources[*]}{.kind}{" "}{.namespace}{" "}{.name}{"  sync="}{.status}{"  health="}{.health.status}{"\n"}{end}'

# 3) Show conditions (why)
kubectl get application -n argocd <app> \
  -o jsonpath='{range .status.conditions[*]}{.type}{"  "}{.reason}{"  "}{.message}{"\n"}{end}'

# 4) Show last operation message (if sync attempts failed)
kubectl get application -n argocd <app> \
  -o jsonpath='{.status.operationState.message}{"\n"}'
```

---

## Notes / Guardrails

- A refresh does not "sync". It only re-checks desired vs live.
- If Argo says it retried sync 5 times and failed, there is usually an apply error (immutable field, webhook rejection, RBAC, missing CRD).
- For app-of-apps, always inspect child apps—the parent reflects their state.

---

Owner: Platform Engineering

Category: Operational Playbooks → GitOps / Argo CD

Keywords: argocd refresh, outofsync, degraded, syncerror, kubectl-only

---

kubectl get applications -n argocd \\ -o custom-columns=NAME:.metadata.name,SYNC:.status.sync.status,HEALTH:.status.health.status \\ --no-headers argo-workflows Synced Healthy cert-manager Synced Healthy ff-hie-test-34 OutOfSync Healthy grafana-k8s-monitoring Synced Healthy hie-test-34-ffcloud-service Synced Healthy hie-test-34-fitconnect Synced Healthy hie-test-34-minio Synced Healthy hie-test-34-mongodb-b17ef Synced Healthy hie-test-34-postgresql Synced Healthy hie-test-34-workflow-templates Synced Healthy hie-test-34-workflows-api Synced Healthy prometheus-operator-crds Synced Healthy spicedb Synced Healthy awsadmin@ip-10-66-2-4:~/terraform$ kubectl get application -n argocd ff-hie-test-34 \\ -o jsonpath='{range.status.resources\[\*\]}{.kind}{" "}{.namespace}{" "}{.name}{" sync="}{.status}{" health="}{.health.status}{"\\n"}{end}' Application argocd argo-workflows sync=Synced health= Application argocd cert-manager sync=Synced health= Application argocd certificates sync=OutOfSync health= Application argocd grafana-k8s-monitoring sync=Synced health= Application argocd hie-test-34-ffcloud-service sync=Synced health= Application argocd hie-test-34-fitconnect sync=Synced health= Application argocd hie-test-34-frontend sync=OutOfSync health= Application argocd hie-test-34-minio sync=Synced health= Application argocd hie-test-34-mongodb-b17ef sync=Synced health= Application argocd hie-test-34-postgresql sync=Synced health= Application argocd hie-test-34-workflow-templates sync=Synced health= Application argocd hie-test-34-workflows-api sync=Synced health= Application argocd prometheus-operator-crds sync=Synced health= Application argocd spicedb sync=Synced health=

---

You've basically proven the pattern: `ff-hie-test-34` is an app-of-apps, and it's only OutOfSync because two child apps are OutOfSync:

- `certificates`
- `hie-test-34-frontend`

Everything else is Synced + Healthy, so the fix is entirely inside those two apps.

## Do This next (copy/paste)

### 1) Refresh the Two Child Apps

### 2) Find what Resources inside Each Child App Are OutOfSync

### 3) Get the Sync Error Message for Each (this Tells You why it Won't sync)

### 4) After You Resolve Those, Refresh the Parent

---

## What You're Likely to See (based on how Your Deployment Has behaved)

The most common reasons those two child apps stay OutOfSync while the cluster is healthy:

### Certificates OutOfSync

Usually one of:

- cert-manager mutating Certificate resources (extra annotations/status fields) → Argo drift
- issuer/secret name changed vs what exists
- immutable field changed (rare for Certificate, more common for Secret)

### hie-test-34-frontend OutOfSync

Usually:

- configmap/secret hash rotation (old immutable resource still exists)
- deployment env/ingress differs because of manual change or operator mutation

---

## The Shortest Path to the Answer

Run steps 2 + 3 and paste outputs for both apps. From that I can tell you:

- if it's safe to delete an orphaned immutable ConfigMap/Secret,
- if it needs a Git change,
- or if it's an "ignoreDifferences" situation.

Right now we only know _which_ child apps are OutOfSync—not _why_.

---

kubectl get pods -n hie-test-34 NAME READY STATUS RESTARTS AGE hie-test-34-ffcloud-service-86b45f4c8c-sqg8x 3/3 Running 1 (23m ago) 24m hie-test-34-fitconnect-ftc-845b98ddd7-bkvxh 1/1 Running 0 14m hie-test-34-minio-6b9779bb4b-gnsb8 1/1 Running 0 20h hie-test-34-minio-provisioning-88sn8 0/1 Completed 0 20h hie-test-34-mongodb-b17ef-0 2/2 Running 0 23m hie-test-34-mongodb-b17ef-arbiter-0 1/1 Running 0 20h hie-test-34-postgresql-0 1/1 Running 0 20h workflows-api-5bd448f79-78szp 1/1 Running 0 20h awsadmin@ip-10-66-2-4:~/terraform$ kubectl annotate application -n argocd certificates argocd.argoproj.io/refresh=hard --overwrite kubectl annotate application -n argocd hie-test-34-frontend argocd.argoproj.io/refresh=hard --overwrite Error from server (NotFound): applications.argoproj.io "certificates" not found Error from server (NotFound): applications.argoproj.io "hie-test-34-frontend" not found awsadmin@ip-10-66-2-4:~/terraform$ kubectl get application -n argocd certificates \\ -o jsonpath='{range.status.resources\[\*\]}{.kind}{" "}{.namespace}{" "}{.name}{" sync="}{.status}{" health="}{.health.status}{"\\n"}{end}' kubectl get application -n argocd hie-test-34-frontend \\ -o jsonpath='{range.status.resources\[\*\]}{.kind}{" "}{.namespace}{" "}{.name}{" sync="}{.status}{" health="}{.health.status}{"\\n"}{end}' Error from server (NotFound): applications.argoproj.io "certificates" not found Error from server (NotFound): applications.argoproj.io "hie-test-34-frontend" not found awsadmin@ip-10-66-2-4:~/terraform$ kubectl get application -n argocd certificates \\ -o jsonpath='{range.status.conditions\[\*\]}{.type}{" "}{.reason}{" "}{.message}{"\\n"}{end}' kubectl get application -n argocd hie-test-34-frontend \\ -o jsonpath='{range.status.conditions\[\*\]}{.type}{" "}{.reason}{" "}{.message}{"\\n"}{end}' Error from server (NotFound): applications.argoproj.io "certificates" not found Error from server (NotFound): applications.argoproj.io "hie-test-34-frontend" not found

---

Ah—that output is the giveaway: those child "applications" shown under `ff-hie-test-34` are _not_ actually named `certificates` / `hie-test-34-frontend` as Application CRs in the `argocd` namespace (or they're in a different namespace, or Argo is tracking them as resources from a different project/cluster and the names don't exist locally).

So we need to refresh/debug them _the way Argo can see them_: via the parent app's resource list and then discover the _real_ app names that exist.

## 1) List the Real Application Names that Exist

Run:

Then grep for likely matches:

Why: Sometimes the child app is named `hie-test-34-certificates` or `certificates-hie-test-34`, etc. The parent's `.status.resources[].name` can also be stale/mismatched if the child app got renamed.

## 2) Pull Full Details of the Parent's "Application resources"

Your parent says it has resources:

- `Application argocd certificates`
- `Application argocd hie-test-34-frontend`

Let's confirm Argo is literally reporting those names:

If that prints `argocd certificates` and `argocd hie-test-34-frontend` but `kubectl get application …` can't find them, then one of these is true:

### Possibility A—The Applications Exist but in a Different Namespace

Check all namespaces:

If they show up elsewhere, refresh using that namespace.

### Possibility B—They Were Deleted, and the Parent Status is Stale

Force refresh of the parent:

Then re-check the parent's resources list:

### Possibility C—You're Looking in the Wrong Argo Namespace

You ran `kubectl get applications -n argocd` and it worked, so likely correct—but confirm the parent app's namespace too:

## 3) Fastest way to Get Unstuck: Find the Real "certificates" App name

Run this and paste the output:

If nothing matches, run across all namespaces:

## 4) If They Truly Don't Exist, Fix the Parent App (it's Referencing Missing apps)

If the apps were deleted/renamed, the parent app-of-apps chart/manifests in Git still reference them. That will keep `ff-hie-test-34` OutOfSync forever.

Confirm by checking the parent's conditions:

If it mentions missing resources / failed sync tasks, that's consistent.

---

### Quick Note on Your Earlier "refresh commands"

My earlier `kubectl annotate application … certificates` approach is correct _if_ those Application CRs exist. Here they don't, so we just need to identify their actual Application names (or namespaces), or confirm they're missing and update the parent app-of-apps config.

---

If you paste the output of these two commands, I'll tell you exactly which path it is and what to do next:

---

kubectl get applications -A | egrep -i 'certificates|hie-test-34-frontend' kubectl get application -n argocd ff-hie-test-34 -o jsonpath='{range.status.resources\[?(@.kind=="Application")\]}{.namespace}{" "}{.name}{" sync="}{.status}{"\\n"}{end}' argocd argo-workflows sync=Synced argocd cert-manager sync=Synced argocd certificates sync=OutOfSync argocd grafana-k8s-monitoring sync=Synced argocd hie-test-34-ffcloud-service sync=Synced argocd hie-test-34-fitconnect sync=Synced argocd hie-test-34-frontend sync=OutOfSync argocd hie-test-34-minio sync=Synced argocd hie-test-34-mongodb-b17ef sync=Synced argocd hie-test-34-postgresql sync=Synced argocd hie-test-34-workflow-templates sync=Synced argocd hie-test-34-workflows-api sync=Synced argocd prometheus-operator-crds sync=Synced argocd spicedb sync=Synced awsadmin@ip-10-66-2-4:~/terraform$

---

Got it—and this is now consistent:

- Parent `ff-hie-test-34` claims it manages child apps named `certificates` and `hie-test-34-frontend`.
- `kubectl get applications -A | egrep …` returned nothing, meaning those Application CRs do not exist anywhere.
- Yet Argo's parent status still lists them as resources and marks them OutOfSync.

That usually means the parent app's desired manifests still include Application objects named `certificates` and `hie-test-34-frontend`, but those resources were never created (or were deleted), and Argo is failing to apply them (likely why you saw "Failed sync attempt … retried 5 times" earlier).

### The Most Likely Reason Kubectl Get Application Certificates Says NotFound

Kubernetes plural for the CR is `applications` but you _can_ fetch a single resource as `application` normally. However your earlier `kubectl get application …` calls failed. That can happen if:

- your kubectl alias doesn't include the CRD shortname, or
- the CRD is only registered as `applications.argoproj.io` (plural) in your setup/cluster tooling.

So: use the plural form explicitly.

## 1) Confirm They Truly Do not Exist (using Plural explicitly)

If these still return NotFound, they're genuinely missing.

## 2) Prove whether the Parent "wants" to Create Them

Check the parent spec source (repo/path/revision) so we know where to look in Git:

And check whether the parent has automated sync disabled (common):

## 3) Pull the Actual Sync Error Message (this Will Tell You why Those Child Apps Aren't Being created)

If it says something like:

- `permission denied` / RBAC
- `namespace not permitted`
- `resource not permitted in project`
- `InvalidSpecError`
- `Failed to load target state`
	…then we know exactly what blocks creation.

## 4) Quick Remediation Paths (pick the One that Matches the message)

### A) The Child Apps Were Deleted Accidentally

If Git still defines them, the correct action is: sync the parent from Argo UI/CLI.

With kubectl-only you can't "sync" directly, but you _can_ detect if auto-sync is off and temporarily enable it (then disable later):

Then refresh:

(If your org doesn't allow auto-sync, don't do this; use Argo UI "Sync" instead.)

### B) The Parent App no Longer Should Manage These

If the deployment no longer includes frontend/certificates, update the app-of-apps chart/manifests in Git to remove those two Application objects. That will make `ff-hie-test-34` go Synced.

### C) Project Restrictions Prevent Creating Application Objects

Argo Projects can restrict:

- which namespaces are allowed destinations
- which source repos/paths are allowed
- which kinds can be created (yes, including `Application`)

If the condition mentions "not permitted in project", inspect the project:

Then fix the project rules or move those child apps to an allowed project.

---

## The next 3 Commands I'd Run (highest signal)

Copy/paste these and paste back the outputs:

- If the first two are NotFound → they truly aren't there, and the third will say why sync didn't create them.
- If the first two _do_ exist → then your earlier `kubectl get application` was just the singular/plural mismatch and we can refresh them normally.

Either way, we'll get you to "Synced".

---

kubectl get application -n argocd ff-hie-test-34 -o jsonpath='{range.status.resources\[?(@.kind=="Application")\]}{.namespace}{" "}{.name}{" sync="}{.status}{"\\n"}{end}' argocd argo-workflows sync=Synced argocd cert-manager sync=Synced argocd certificates sync=OutOfSync argocd grafana-k8s-monitoring sync=Synced argocd hie-test-34-ffcloud-service sync=Synced argocd hie-test-34-fitconnect sync=Synced argocd hie-test-34-frontend sync=OutOfSync argocd hie-test-34-minio sync=Synced argocd hie-test-34-mongodb-b17ef sync=Synced argocd hie-test-34-postgresql sync=Synced argocd hie-test-34-workflow-templates sync=Synced argocd hie-test-34-workflows-api sync=Synced argocd prometheus-operator-crds sync=Synced argocd spicedb sync=Synced awsadmin@ip-10-66-2-4:~/terraform$ kubectl get applications.argoproj.io -n argocd certificates -o yaml | sed -n '1,120p' kubectl get applications.argoproj.io -n argocd hie-test-34-frontend -o yaml | sed -n '1,120p' kubectl get applications.argoproj.io -n argocd ff-hie-test-34 -o jsonpath='{range.status.conditions\[\*\]}{.type}{" "}{.reason}{" "}{.message}{"\\n"}{end}' Error from server (NotFound): applications.argoproj.io "certificates" not found Error from server (NotFound): applications.argoproj.io "hie-test-34-frontend" not found SyncError Failed sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9: one or more synchronization tasks completed unsuccessfully (retried 5 times). awsadmin@ip-10-66-2-4:~/terraform$ kubectl get pods -n hie-test-34 NAME READY STATUS RESTARTS AGE hie-test-34-ffcloud-service-777c7b959b-x4dn4 3/3 Running 0 13m hie-test-34-fitconnect-ftc-fffdf4c6c-dgfp9 1/1 Running 0 12m hie-test-34-minio-6b9779bb4b-gnsb8 1/1 Running 0 21h hie-test-34-minio-provisioning-88sn8 0/1 Completed 0 21h hie-test-34-mongodb-b17ef-0 2/2 Running 0 44m hie-test-34-mongodb-b17ef-arbiter-0 1/1 Running 0 21h hie-test-34-postgresql-0 1/1 Running 0 21h workflows-api-5bd448f79-78szp 1/1 Running 0 21h awsadmin@ip-10-66-2-4:~/terraform$ kubectl get applications -n argocd NAME SYNC STATUS HEALTH STATUS argo-workflows Synced Healthy cert-manager Synced Healthy ff-hie-test-34 OutOfSync Healthy grafana-k8s-monitoring Synced Healthy hie-test-34-ffcloud-service Synced Healthy hie-test-34-fitconnect Synced Healthy hie-test-34-minio Synced Healthy hie-test-34-mongodb-b17ef Synced Healthy hie-test-34-postgresql Synced Healthy hie-test-34-workflow-templates Synced Healthy hie-test-34-workflows-api Synced Healthy prometheus-operator-crds Synced Healthy spicedb Synced Healthy

---

Perfect—now we know for sure:

- `ff-hie-test-34` expects two child `Application` resources: `certificates` and `hie-test-34-frontend`
- Those `Application` CRs do not exist in the cluster (`NotFound`)
- Parent has a `SyncError` with "retried 5 times" → Argo tried to create/apply them and failed

So the only remaining question is: why did Argo fail to create those two Application objects?

The fastest way to answer that is to inspect the parent's operationState (it contains per-resource apply errors).

## 1) Get the Exact Failure from operationState (this Will name the Resource + error)

If that's too long/noisy, pull the message and the sync results:

Why: This will say something like:

- "application is invalid: spec.destination.namespace … not permitted"
- "permission denied"
- "error when creating … already exists"
- "resource not permitted in project"
- "unknown field …"
	…etc.

## 2) Most Common Root Causes (so You Can Act Immediately once You See the message)

### A) Argo Project Disallows Creating Application Resources

If the error mentions "not permitted in project", check which project the parent uses and what it allows:

Fix: allow `applications.argoproj.io` creation, destinations, and sources for that project.

### B) Argo RBAC Doesn't Allow it to Create Applications

If the error mentions RBAC/forbidden, inspect Argo's controller permissions (clusterrolebindings, etc.). (Usually a platform change.)

### C) The Child App Manifests Are Invalid (bad repo/path/destination)

If it mentions `InvalidSpecError` / `spec.source` / `repoURL` etc, then Git content for those two apps is wrong.

---

## 3) "Make It green" Options once We Know the Error

### Option 1 (recommended): Fix Git/app-of-apps so Argo Can Create the Child Apps

This makes the sync clean and durable.

### Option 2: Remove Those Two Child Apps from the App-of-apps

If you no longer deploy frontend/certificates via this parent.

### Option 3 (temporary): Manually Create the Missing Applications

Only if Argo is failing due to project restrictions/templating and you need it running now (but you'll still want Git fixed).

---

## 4) Why Everything Runs but Parent is OutOfSync

Because the workloads are managed by other apps and are healthy; the parent is only failing on two missing child Application CRs. Until Argo can create (or stop wanting to create) them, `ff-hie-test-34` will remain OutOfSync.

---

### Paste This Output and I'll Tell You the Exact Fix

Run:

That single command usually contains the smoking gun.

---

kubectl get application -n argocd ff-hie-test-34 -o yaml | sed -n '/operationState:/,/^ sync:/p' operationState: finishedAt: "2026-02-12T12:18:57Z" message: one or more synchronization tasks completed unsuccessfully (retried 5 times). operation: initiatedBy: automated: true retry: limit: 5 sync: prune: true revision: d4ee068bd666f1213627d4f27791b86f870842e9 phase: Failed retryCount: 5 startedAt: "2026-02-12T11:37:05Z" syncResult: resources: - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/prometheus-operator-crds unchanged name: prometheus-operator-crds namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/cert-manager unchanged name: cert-manager namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/grafana-k8s-monitoring unchanged name: grafana-k8s-monitoring namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/hie-test-34-postgresql unchanged name: hie-test-34-postgresql namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/argo-workflows unchanged name: argo-workflows namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/hie-test-34-minio unchanged name: hie-test-34-minio namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/hie-test-34-mongodb-b17ef unchanged name: hie-test-34-mongodb-b17ef namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/spicedb unchanged name: spicedb namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/hie-test-34-workflow-templates unchanged name: hie-test-34-workflow-templates namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/hie-test-34-workflows-api unchanged name: hie-test-34-workflows-api namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Failed kind: Application message: 'Failed sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9: one or more synchronization tasks completed unsuccessfully (retried 5 times).' name: hie-test-34-fitconnect namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/hie-test-34-ffcloud-service unchanged name: hie-test-34-ffcloud-service namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 revision: d4ee068bd666f1213627d4f27791b86f870842e9 source: helm: releaseName: hie-test-34 valueFiles: - /ffnodes/eoe/hie-test-34/values.yaml path: charts/ffnode repoURL: <https://gitlab.com/fitfile/deployment.git> targetRevision: eoe-test-release reconciledAt: "2026-02-12T13:36:53Z" resourceHealthSource: appTree resources: - group: argoproj.io kind: Application name: argo-workflows namespace: argocd status: Synced syncWave: -2 version: v1alpha1 - group: argoproj.io kind: Application name: cert-manager namespace: argocd status: Synced syncWave: -5 version: v1alpha1 - group: argoproj.io kind: Application name: certificates namespace: argocd status: OutOfSync syncWave: 5 version: v1alpha1 - group: argoproj.io kind: Application name: grafana-k8s-monitoring namespace: argocd status: Synced syncWave: -4 version: v1alpha1 - group: argoproj.io kind: Application name: hie-test-34-ffcloud-service namespace: argocd status: Synced syncWave: 3 version: v1alpha1 - group: argoproj.io kind: Application name: hie-test-34-fitconnect namespace: argocd status: Synced syncWave: 3 version: v1alpha1 - group: argoproj.io kind: Application name: hie-test-34-frontend namespace: argocd status: OutOfSync syncWave: 4 version: v1alpha1 - group: argoproj.io kind: Application name: hie-test-34-minio namespace: argocd status: Synced version: v1alpha1 - group: argoproj.io kind: Application name: hie-test-34-mongodb-b17ef namespace: argocd status: Synced version: v1alpha1 - group: argoproj.io kind: Application name: hie-test-34-postgresql namespace: argocd status: Synced syncWave: -3 version: v1alpha1 - group: argoproj.io kind: Application name: hie-test-34-workflow-templates namespace: argocd status: Synced syncWave: 1 version: v1alpha1 - group: argoproj.io kind: Application name: hie-test-34-workflows-api namespace: argocd status: Synced syncWave: 2 version: v1alpha1 - group: argoproj.io kind: Application name: prometheus-operator-crds namespace: argocd status: Synced syncWave: -5 version: v1alpha1 - group: argoproj.io kind: Application name: spicedb namespace: argocd status: Synced syncWave: 1 version: v1alpha1 sourceHydrator: {} sourceType: Helm summary: {} sync: awsadmin@ip-10-66-2-4:~/terraform$ kubectl get application -n argocd ff-hie-test-34 -o jsonpath='{.status.operationState.message}{"\\n"}' kubectl get application -n argocd ff-hie-test-34 -o jsonpath='{range.status.operationState.syncResult.resources\[\*\]}{.kind}{" "}{.namespace}{" "}{.name}{" status="}{.status}{" message="}{.message}{"\\n"}{end}' one or more synchronization tasks completed unsuccessfully (retried 5 times). Application argocd prometheus-operator-crds status=Synced message=application.argoproj.io/prometheus-operator-crds unchanged Application argocd cert-manager status=Synced message=application.argoproj.io/cert-manager unchanged Application argocd grafana-k8s-monitoring status=Synced message=application.argoproj.io/grafana-k8s-monitoring unchanged Application argocd hie-test-34-postgresql status=Synced message=application.argoproj.io/hie-test-34-postgresql unchanged Application argocd argo-workflows status=Synced message=application.argoproj.io/argo-workflows unchanged Application argocd hie-test-34-minio status=Synced message=application.argoproj.io/hie-test-34-minio unchanged Application argocd hie-test-34-mongodb-b17ef status=Synced message=application.argoproj.io/hie-test-34-mongodb-b17ef unchanged Application argocd spicedb status=Synced message=application.argoproj.io/spicedb unchanged Application argocd hie-test-34-workflow-templates status=Synced message=application.argoproj.io/hie-test-34-workflow-templates unchanged Application argocd hie-test-34-workflows-api status=Synced message=application.argoproj.io/hie-test-34-workflows-api unchanged Application argocd hie-test-34-fitconnect status=Synced message=Failed sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9: one or more synchronization tasks completed unsuccessfully (retried 5 times). Application argocd hie-test-34-ffcloud-service status=Synced message=application.argoproj.io/hie-test-34-ffcloud-service unchanged

---

Nice—this output tells us something subtle but important:

- The last sync operation failed, but `syncResult` does not list `certificates` or `hie-test-34-frontend` at all.
- Instead, the failure is "attributed" to `hie-test-34-fitconnect` in `syncResult`, even though `hie-test-34-fitconnect` is currently Synced/Healthy.
- Meanwhile, the _app tree_ (`status.resources`) still shows `certificates` and `hie-test-34-frontend` as OutOfSync—but they don't exist as Application CRs.

This is classic "app-of-apps drift + stale/partial operation result": Argo is stuck reporting a failed operation from earlier, while current tree reconciliation still thinks two expected children exist.

### What's Almost Certainly Happening

The Helm chart `charts/ffnode` for `ff-hie-test-34` is rendering `Application` manifests for:

- `certificates`
- `hie-test-34-frontend`

…but for some reason Argo is not actually applying them (or they're being pruned immediately / blocked by a policy), and Argo's UI/tree continues to show them as desired but missing.

We need to answer: Are those two Applications in the desired manifests (rendered output), and if so why aren't they being created?

Since we don't have `argocd` CLI here, we'll do it with Kubernetes + git facts.

---

## 1) Prove whether the Parent Still Wants Those Apps (rendered Desired state)

The easiest Kubernetes-only check: look at the parent Application's source path and values file (you already have it), then check whether the chart should create those apps based on values.

You already showed values contain `certs:` and `frontend:` sections—so likely yes.

But let's confirm via the live manifest stored by Argo. Argo stores the last-applied/desired manifest in `.status` in some cases, but not always. Better: pull the Helm parameters and see if the parent has toggles for those apps.

If no parameters, that's fine—then the chart likely always includes those child apps when `certs` / `frontend` blocks exist.

---

## 2) Find the Real Reason They Aren't Being Created: Check Argo Controller Logs

When Argo can't create an `Application`, it logs an explicit error (RBAC, project restrictions, invalid spec, etc).

Find the application-controller pod and tail logs around your reconcile time (`reconciledAt: 2026-02-12T13:36:53Z`):

If controller is a StatefulSet instead of deploy:

Why: this will usually show the exact Kubernetes API error that never made it into `operationState.syncResult` (because the sync was retried/aborted/short-circuited).

---

## 3) Check Argo Project Policy (very Common Blocker for app-of-apps)

If the project doesn't allow creating Application resources, Argo will refuse.

Get the project used by the parent:

Then dump that project:

What to look for:

- `spec.sourceRepos` includes your repo
- `spec.destinations` includes `argocd` namespace / cluster
- `spec.clusterResourceWhitelist` / `namespaceResourceWhitelist` includes `argoproj.io/Application` if restricted

If Application isn't permitted, that explains _exactly_ why those child apps never exist.

---

## 4) Why Kubectl Get Applications -A | egrep… Printed Nothing Earlier

Because that command only searched for literal strings `certificates|hie-test-34-frontend` and returned nothing—which is consistent with them not existing. Good.

But now: Argo says they're desired. So we need to either:

1. Allow Argo to create them (policy/RBAC/project), or
2. Stop the parent chart from rendering them (values/Git fix).

---

## 5) "Make It Green now" Options (Kubernetes-only)

### Option A (safe, reversible): Disable Auto-sync Retries Stuck State, then Hard Refresh

Sometimes Argo gets stuck showing old OutOfSync children after failures. A hard refresh can clear the tree view once the desired state no longer contains those resources (or after policy fix).

(You already did similar; do again after the policy fix.)

### Option B (only if You Confirm the Chart Should NOT Deploy these): Prune the Phantom Children by Removing Them from Git

If your deployment shouldn't have frontend/certificates as child apps, remove/disable them in `/ffnodes/eoe/hie-test-34/values.yaml` (or whatever values are used) and sync again. That will make the parent stop expecting them.

### Option C (temporary): Manually Create the Missing Applications

If policies allow but something else prevents creation, you can create `Application` resources yourself, but that's usually fighting GitOps unless you commit it back.

---

## The Single Command that Will Likely Settle it Immediately

Run this and paste the output:

And then:

If `argoproj.io` + `Application` isn't whitelisted (in a locked-down project), that's your root cause: the parent can manage existing child apps but cannot create new ones like `certificates` / `hie-test-34-frontend`.

If it _is_ allowed, then the controller logs (step 2) will show the next-most-likely reason (invalid child spec, destination namespace not allowed, etc.).

---

kubectl get application -n argocd ff-hie-test-34 -o jsonpath='{.spec.source.helm.parameters}{"\\n"}' kubectl get application -n argocd ff-hie-test-34 -o jsonpath='{.spec.source.helm.valueFiles}{"\\n"}' \["/ffnodes/eoe/hie-test-34/values.yaml"\] awsadmin@ip-10-66-2-4:~/terraform$ kubectl -n argocd get pods -l app.kubernetes.io/name=argocd-application-controller kubectl -n argocd logs deploy/argocd-application-controller --since=3h | egrep -i 'ff-hie-test-34|certificates|hie-test-34-frontend|permission|forbidden|InvalidSpec|appproject|denied|sync' NAME READY STATUS RESTARTS AGE argocd-application-controller-0 1/1 Running 0 23h error: error from server (NotFound): deployments.apps "argocd-application-controller" not found in namespace "argocd" awsadmin@ip-10-66-2-4:~/terraform$ kubectl -n argocd logs sts/argocd-application-controller --since=3h | egrep -i 'ff-hie-test-34|certificates|hie-test-34-frontend|permission|forbidden|InvalidSpec|appproject|denied|sync' {"app-namespace":"argocd","application":"hie-test-34-workflows-api","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:15:35Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-workflows-api","auto\_sync\_ms":0,"compare\_app\_state\_ms":26,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":11,"git\_ms":13,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":18,"persist\_app\_status\_ms":18,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":2,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:15:35Z","time\_ms":48} {"app-namespace":"argocd","application":"cert-manager","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:15:35Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"cert-manager","auto\_sync\_ms":0,"compare\_app\_state\_ms":334,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"cert-manager","dest-server":"https://kubernetes.default.svc","diff\_ms":297,"git\_ms":25,"health\_ms":9,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":2,"patch\_ms":32,"persist\_app\_status\_ms":34,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":66,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:15:35Z","time\_ms":438} {"app-namespace":"argocd","application":"hie-test-34-fitconnect","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:15:43Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-fitconnect","auto\_sync\_ms":0,"compare\_app\_state\_ms":50,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":39,"git\_ms":8,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":22,"persist\_app\_status\_ms":22,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":2,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:15:43Z","time\_ms":77} {"app-namespace":"argocd","application":"hie-test-34-postgresql","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:15:44Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-postgresql","auto\_sync\_ms":0,"compare\_app\_state\_ms":29,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":21,"git\_ms":6,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":16,"persist\_app\_status\_ms":17,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":3,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:15:44Z","time\_ms":51} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:15:52Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":204,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":79,"git\_ms":117,"health\_ms":5,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":34,"persist\_app\_status\_ms":35,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":13,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:15:52Z","time\_ms":254} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (comparison expired, requesting refresh. reconciledAt: 2026-02-12 13:09:32 +0000 UTC, expiry: 3m0s), level (2)","project":"fitfile","time":"2026-02-12T13:15:55Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:15:55Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":298,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:15:55Z","time\_ms":299} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:15:56Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:15:56Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:15:56Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":344,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":35,"git\_ms":299,"health\_ms":8,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":16,"persist\_app\_status\_ms":17,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":27,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:15:56Z","time\_ms":391} {"app-namespace":"argocd","application":"hie-test-34-workflow-templates","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:16:06Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-workflow-templates","auto\_sync\_ms":0,"compare\_app\_state\_ms":221,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":184,"git\_ms":22,"health\_ms":0,"level":"info","live\_ms":12,"msg":"Reconciliation completed","normalize\_application\_ms":3,"patch\_ms":37,"persist\_app\_status\_ms":39,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":39,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:16:06Z","time\_ms":305} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:16:26Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":101,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":77,"git\_ms":9,"health\_ms":12,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":2,"patch\_ms":30,"persist\_app\_status\_ms":30,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":25,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:16:26Z","time\_ms":160} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:16:27Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":99,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":81,"git\_ms":9,"health\_ms":6,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":0,"persist\_app\_status\_ms":0,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:16:27Z","time\_ms":114} {"app-namespace":"argocd","application":"hie-test-34-ffcloud-service","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:18:26Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-ffcloud-service","auto\_sync\_ms":0,"compare\_app\_state\_ms":44,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":30,"git\_ms":12,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":2,"patch\_ms":26,"persist\_app\_status\_ms":27,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":3,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:18:26Z","time\_ms":78} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:18:32Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":95,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":78,"git\_ms":10,"health\_ms":5,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":26,"persist\_app\_status\_ms":27,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":14,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:18:32Z","time\_ms":139} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:18:32Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":96,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":79,"git\_ms":10,"health\_ms":5,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":0,"persist\_app\_status\_ms":0,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":14,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:18:32Z","time\_ms":112} {"app-namespace":"argocd","application":"hie-test-34-minio","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:18:45Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-minio","auto\_sync\_ms":0,"compare\_app\_state\_ms":31,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":23,"git\_ms":6,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":20,"persist\_app\_status\_ms":20,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:18:45Z","time\_ms":65} {"app-namespace":"argocd","application":"spicedb","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:18:52Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"spicedb","auto\_sync\_ms":0,"compare\_app\_state\_ms":43,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"spicedb","dest-server":"https://kubernetes.default.svc","diff\_ms":31,"git\_ms":9,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":30,"persist\_app\_status\_ms":30,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":4,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:18:52Z","time\_ms":79} {"app-namespace":"argocd","application":"cert-manager","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:18:52Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"cert-manager","auto\_sync\_ms":0,"compare\_app\_state\_ms":332,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"cert-manager","dest-server":"https://kubernetes.default.svc","diff\_ms":293,"git\_ms":25,"health\_ms":10,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":35,"persist\_app\_status\_ms":36,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":59,"setop\_ms":0,"settings\_ms":0,"sync\_ms":1,"time":"2026-02-12T13:18:52Z","time\_ms":430} {"app-namespace":"argocd","application":"hie-test-34-fitconnect","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:18:54Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-fitconnect","auto\_sync\_ms":0,"compare\_app\_state\_ms":25,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":15,"git\_ms":9,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":20,"persist\_app\_status\_ms":20,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":2,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:18:54Z","time\_ms":50} {"app-namespace":"argocd","application":"hie-test-34-mongodb-b17ef","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:18:56Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-mongodb-b17ef","auto\_sync\_ms":0,"compare\_app\_state\_ms":133,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":43,"git\_ms":87,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":19,"persist\_app\_status\_ms":19,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":6,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:18:56Z","time\_ms":161} {"app-namespace":"argocd","application":"hie-test-34-postgresql","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:19:02Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-postgresql","auto\_sync\_ms":0,"compare\_app\_state\_ms":28,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":21,"git\_ms":5,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":26,"persist\_app\_status\_ms":26,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":3,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:19:02Z","time\_ms":60} {"app-namespace":"argocd","application":"prometheus-operator-crds","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:19:09Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"prometheus-operator-crds","auto\_sync\_ms":0,"compare\_app\_state\_ms":398,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"","dest-server":"https://kubernetes.default.svc","diff\_ms":313,"git\_ms":64,"health\_ms":18,"level":"info","live\_ms":2,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":18,"persist\_app\_status\_ms":19,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":117,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:19:09Z","time\_ms":536} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:19:12Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":104,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":90,"git\_ms":10,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":23,"persist\_app\_status\_ms":24,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":11,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:19:12Z","time\_ms":141} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:19:40Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":106,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":92,"git\_ms":11,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":25,"persist\_app\_status\_ms":25,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":11,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:19:40Z","time\_ms":145} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:19:41Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":156,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":139,"git\_ms":12,"health\_ms":1,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":0,"persist\_app\_status\_ms":0,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":11,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:19:41Z","time\_ms":170} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:21:15Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":117,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":100,"git\_ms":11,"health\_ms":3,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":2,"patch\_ms":22,"persist\_app\_status\_ms":22,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":18,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:21:15Z","time\_ms":160} {"app-namespace":"argocd","application":"hie-test-34-workflows-api","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:21:18Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-workflows-api","auto\_sync\_ms":0,"compare\_app\_state\_ms":320,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":9,"git\_ms":310,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":24,"persist\_app\_status\_ms":24,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":1,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:21:18Z","time\_ms":348} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:21:19Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":110,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":94,"git\_ms":11,"health\_ms":1,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":58,"persist\_app\_status\_ms":58,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":13,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:21:19Z","time\_ms":183} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:21:24Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":107,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":91,"git\_ms":12,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":27,"persist\_app\_status\_ms":29,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":31,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:21:24Z","time\_ms":169} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (comparison expired, requesting refresh. reconciledAt: 2026-02-12 13:15:55 +0000 UTC, expiry: 3m0s), level (2)","project":"fitfile","time":"2026-02-12T13:21:25Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:21:25Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":11,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:21:25Z","time\_ms":11} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:21:25Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:21:25Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:21:25Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":56,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":36,"git\_ms":11,"health\_ms":6,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":16,"persist\_app\_status\_ms":16,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":23,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:21:25Z","time\_ms":96} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:21:30Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":198,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":87,"git\_ms":103,"health\_ms":6,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":28,"persist\_app\_status\_ms":29,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":15,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:21:30Z","time\_ms":245} {"app-namespace":"argocd","application":"hie-test-34-ffcloud-service","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:21:34Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-ffcloud-service","auto\_sync\_ms":0,"compare\_app\_state\_ms":33,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":20,"git\_ms":10,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":28,"persist\_app\_status\_ms":29,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":3,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:21:34Z","time\_ms":67} {"app-namespace":"argocd","application":"cert-manager","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:21:53Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"cert-manager","auto\_sync\_ms":0,"compare\_app\_state\_ms":345,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"cert-manager","dest-server":"https://kubernetes.default.svc","diff\_ms":297,"git\_ms":25,"health\_ms":19,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":2,"patch\_ms":34,"persist\_app\_status\_ms":35,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":62,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:21:53Z","time\_ms":446} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:21:57Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":95,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":79,"git\_ms":10,"health\_ms":5,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":30,"persist\_app\_status\_ms":31,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":14,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:21:57Z","time\_ms":143} {"app-namespace":"argocd","application":"spicedb","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:22:02Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"spicedb","auto\_sync\_ms":0,"compare\_app\_state\_ms":64,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"spicedb","dest-server":"https://kubernetes.default.svc","diff\_ms":51,"git\_ms":10,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":15,"persist\_app\_status\_ms":16,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":5,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:22:02Z","time\_ms":86} {"app-namespace":"argocd","application":"hie-test-34-workflow-templates","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:22:12Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-workflow-templates","auto\_sync\_ms":18,"compare\_app\_state\_ms":202,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":174,"git\_ms":23,"health\_ms":0,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":3,"patch\_ms":61,"persist\_app\_status\_ms":66,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":38,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:22:12Z","time\_ms":330} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:22:13Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":107,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":88,"git\_ms":9,"health\_ms":7,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":22,"persist\_app\_status\_ms":23,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":18,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:22:13Z","time\_ms":151} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:22:14Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":104,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":90,"git\_ms":11,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":20,"persist\_app\_status\_ms":20,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:22:14Z","time\_ms":139} {"app-namespace":"argocd","application":"hie-test-34-postgresql","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:22:33Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-postgresql","auto\_sync\_ms":0,"compare\_app\_state\_ms":30,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":22,"git\_ms":6,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":62,"persist\_app\_status\_ms":63,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":7,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:22:33Z","time\_ms":102} {"app-namespace":"argocd","application":"hie-test-34-mongodb-b17ef","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:22:53Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-mongodb-b17ef","auto\_sync\_ms":0,"compare\_app\_state\_ms":519,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":43,"git\_ms":473,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":34,"persist\_app\_status\_ms":34,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":11,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:22:53Z","time\_ms":566} {"app-namespace":"argocd","application":"hie-test-34-minio","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:22:57Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-minio","auto\_sync\_ms":0,"compare\_app\_state\_ms":31,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":23,"git\_ms":6,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":18,"persist\_app\_status\_ms":19,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":7,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:22:57Z","time\_ms":59} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:23:01Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":173,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":158,"git\_ms":12,"health\_ms":1,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":40,"persist\_app\_status\_ms":40,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:23:01Z","time\_ms":228} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:23:02Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":119,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":98,"git\_ms":17,"health\_ms":1,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":0,"persist\_app\_status\_ms":0,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:23:02Z","time\_ms":134} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:23:10Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":109,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":81,"git\_ms":9,"health\_ms":16,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":2,"patch\_ms":24,"persist\_app\_status\_ms":24,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":20,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:23:10Z","time\_ms":157} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:23:10Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":98,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":81,"git\_ms":9,"health\_ms":5,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":0,"persist\_app\_status\_ms":0,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:23:10Z","time\_ms":113} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:24:13Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":124,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":106,"git\_ms":9,"health\_ms":6,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":23,"persist\_app\_status\_ms":24,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":13,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:24:13Z","time\_ms":164} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:24:13Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":105,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":90,"git\_ms":11,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":34,"persist\_app\_status\_ms":35,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":11,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:24:13Z","time\_ms":153} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:24:13Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":114,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":98,"git\_ms":10,"health\_ms":3,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":2,"patch\_ms":0,"persist\_app\_status\_ms":0,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":21,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:24:13Z","time\_ms":139} {"app-namespace":"argocd","application":"hie-test-34-ffcloud-service","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:24:15Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-ffcloud-service","auto\_sync\_ms":0,"compare\_app\_state\_ms":22,"comparison-level":1,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":13,"git\_ms":6,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":36,"persist\_app\_status\_ms":65,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":5,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:24:15Z","time\_ms":94} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (controller refresh requested), level (1)","project":"fitfile","time":"2026-02-12T13:24:16Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:24:16Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":10,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:24:16Z","time\_ms":11} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:24:16Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:24:16Z"} {"application":"ff-hie-test-34","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","level":"info","msg":"Updated health status: Healthy -\\u003e Progressing","reason":"ResourceUpdated","time":"2026-02-12T13:24:16Z","type":"Normal"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:24:16Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":56,"comparison-level":1,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":36,"git\_ms":11,"health\_ms":6,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":20,"persist\_app\_status\_ms":27,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":26,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:24:16Z","time\_ms":110} {"app-namespace":"argocd","application":"hie-test-34-fitconnect","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:24:19Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-fitconnect","auto\_sync\_ms":0,"compare\_app\_state\_ms":262,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":14,"git\_ms":245,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":34,"persist\_app\_status\_ms":34,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":3,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:24:19Z","time\_ms":301} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:24:22Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":210,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":183,"git\_ms":16,"health\_ms":6,"level":"info","live\_ms":2,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":24,"persist\_app\_status\_ms":25,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":13,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:24:22Z","time\_ms":250} {"app-namespace":"argocd","application":"prometheus-operator-crds","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:24:32Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"prometheus-operator-crds","auto\_sync\_ms":0,"compare\_app\_state\_ms":411,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"","dest-server":"https://kubernetes.default.svc","diff\_ms":316,"git\_ms":73,"health\_ms":17,"level":"info","live\_ms":2,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":19,"persist\_app\_status\_ms":20,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":93,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:24:32Z","time\_ms":525} {"app-namespace":"argocd","application":"hie-test-34-ffcloud-service","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:24:39Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-ffcloud-service","auto\_sync\_ms":0,"compare\_app\_state\_ms":37,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":26,"git\_ms":9,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":81,"persist\_app\_status\_ms":81,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":6,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:24:39Z","time\_ms":126} {"app-namespace":"argocd","application":"hie-test-34-ffcloud-service","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:24:40Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-ffcloud-service","auto\_sync\_ms":0,"compare\_app\_state\_ms":21,"comparison-level":1,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":13,"git\_ms":6,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":49,"persist\_app\_status\_ms":58,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":6,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:24:40Z","time\_ms":87} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (comparison expired, requesting refresh. reconciledAt: 2026-02-12 13:21:25 +0000 UTC, expiry: 3m0s), level (2)","project":"fitfile","time":"2026-02-12T13:24:40Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:24:40Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":14,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:24:40Z","time\_ms":14} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:24:40Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:24:40Z"} {"application":"ff-hie-test-34","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","level":"info","msg":"Updated health status: Progressing -\\u003e Healthy","reason":"ResourceUpdated","time":"2026-02-12T13:24:40Z","type":"Normal"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:24:40Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":58,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":36,"git\_ms":14,"health\_ms":6,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":28,"persist\_app\_status\_ms":44,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":30,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:24:40Z","time\_ms":134} {"app-namespace":"argocd","application":"hie-test-34-workflows-api","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:24:52Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-workflows-api","auto\_sync\_ms":0,"compare\_app\_state\_ms":18,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":8,"git\_ms":8,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":20,"persist\_app\_status\_ms":21,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":2,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:24:52Z","time\_ms":42} {"app-namespace":"argocd","application":"cert-manager","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:24:59Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"cert-manager","auto\_sync\_ms":0,"compare\_app\_state\_ms":335,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"cert-manager","dest-server":"https://kubernetes.default.svc","diff\_ms":295,"git\_ms":30,"health\_ms":7,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":28,"persist\_app\_status\_ms":30,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":54,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:24:59Z","time\_ms":422} {"app-namespace":"argocd","application":"hie-test-34-fitconnect","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:25:10Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-fitconnect","auto\_sync\_ms":0,"compare\_app\_state\_ms":21,"comparison-level":1,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":9,"git\_ms":6,"health\_ms":0,"level":"info","live\_ms":5,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":17,"persist\_app\_status\_ms":30,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":14,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:25:10Z","time\_ms":66} {"app-namespace":"argocd","application":"hie-test-34-fitconnect","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:25:10Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-fitconnect","auto\_sync\_ms":0,"compare\_app\_state\_ms":9,"comparison-level":1,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":0,"git\_ms":7,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":0,"persist\_app\_status\_ms":0,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":2,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:25:10Z","time\_ms":13} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (controller refresh requested), level (1)","project":"fitfile","time":"2026-02-12T13:25:10Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:25:10Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":7,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:25:10Z","time\_ms":7} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:25:10Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:25:10Z"} {"application":"ff-hie-test-34","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","level":"info","msg":"Updated health status: Healthy -\\u003e Progressing","reason":"ResourceUpdated","time":"2026-02-12T13:25:10Z","type":"Normal"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:25:10Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":26,"comparison-level":1,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":10,"git\_ms":7,"health\_ms":6,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":17,"persist\_app\_status\_ms":24,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":23,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:25:10Z","time\_ms":75} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:25:18Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":1340,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":93,"git\_ms":1239,"health\_ms":5,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":30,"persist\_app\_status\_ms":31,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":13,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:25:18Z","time\_ms":1387} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:25:18Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":151,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":131,"git\_ms":12,"health\_ms":5,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":21,"persist\_app\_status\_ms":22,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:25:18Z","time\_ms":188} {"app-namespace":"argocd","application":"hie-test-34-fitconnect","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:25:32Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-fitconnect","auto\_sync\_ms":0,"compare\_app\_state\_ms":15,"comparison-level":1,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":8,"git\_ms":6,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":35,"persist\_app\_status\_ms":46,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":5,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:25:32Z","time\_ms":68} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (controller refresh requested), level (1)","project":"fitfile","time":"2026-02-12T13:25:32Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:25:32Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":7,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:25:32Z","time\_ms":7} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:25:32Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:25:32Z"} {"application":"ff-hie-test-34","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","level":"info","msg":"Updated health status: Progressing -\\u003e Healthy","reason":"ResourceUpdated","time":"2026-02-12T13:25:32Z","type":"Normal"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:25:32Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":23,"comparison-level":1,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":7,"git\_ms":8,"health\_ms":5,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":23,"persist\_app\_status\_ms":30,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":22,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:25:32Z","time\_ms":77} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:25:43Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":114,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":84,"git\_ms":11,"health\_ms":15,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":2,"patch\_ms":30,"persist\_app\_status\_ms":31,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":22,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:25:43Z","time\_ms":171} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:25:43Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":107,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":85,"git\_ms":10,"health\_ms":9,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":26,"persist\_app\_status\_ms":26,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:25:43Z","time\_ms":148} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:26:20Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":94,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":77,"git\_ms":9,"health\_ms":5,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":22,"persist\_app\_status\_ms":23,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":36,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:26:20Z","time\_ms":156} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:26:36Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":108,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":83,"git\_ms":16,"health\_ms":5,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":23,"persist\_app\_status\_ms":23,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":15,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:26:36Z","time\_ms":149} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:27:09Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":97,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":80,"git\_ms":10,"health\_ms":4,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":23,"persist\_app\_status\_ms":24,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:27:09Z","time\_ms":135} {"app-namespace":"argocd","application":"spicedb","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:27:16Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"spicedb","auto\_sync\_ms":0,"compare\_app\_state\_ms":74,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"spicedb","dest-server":"https://kubernetes.default.svc","diff\_ms":60,"git\_ms":9,"health\_ms":1,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":33,"persist\_app\_status\_ms":33,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":8,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:27:16Z","time\_ms":117} {"app-namespace":"argocd","application":"hie-test-34-postgresql","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:27:22Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-postgresql","auto\_sync\_ms":0,"compare\_app\_state\_ms":29,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":21,"git\_ms":5,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":26,"persist\_app\_status\_ms":27,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":3,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:27:22Z","time\_ms":61} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:27:27Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":104,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":90,"git\_ms":11,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":30,"persist\_app\_status\_ms":31,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:27:27Z","time\_ms":149} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:27:42Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":120,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":103,"git\_ms":10,"health\_ms":5,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":27,"persist\_app\_status\_ms":27,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:27:42Z","time\_ms":162} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:27:42Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":98,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":81,"git\_ms":9,"health\_ms":5,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":0,"persist\_app\_status\_ms":0,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":13,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:27:42Z","time\_ms":113} {"app-namespace":"argocd","application":"hie-test-34-mongodb-b17ef","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:27:46Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-mongodb-b17ef","auto\_sync\_ms":0,"compare\_app\_state\_ms":169,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":42,"git\_ms":124,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":24,"persist\_app\_status\_ms":24,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":5,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:27:46Z","time\_ms":200} {"app-namespace":"argocd","application":"prometheus-operator-crds","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:27:57Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"prometheus-operator-crds","auto\_sync\_ms":0,"compare\_app\_state\_ms":406,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"","dest-server":"https://kubernetes.default.svc","diff\_ms":308,"git\_ms":68,"health\_ms":16,"level":"info","live\_ms":12,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":16,"persist\_app\_status\_ms":16,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":123,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:27:57Z","time\_ms":547} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:28:01Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":110,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":93,"git\_ms":13,"health\_ms":1,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":42,"persist\_app\_status\_ms":43,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":11,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:28:01Z","time\_ms":167} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:28:01Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":170,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":151,"git\_ms":16,"health\_ms":1,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":0,"persist\_app\_status\_ms":0,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":14,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:28:01Z","time\_ms":187} {"app-namespace":"argocd","application":"hie-test-34-fitconnect","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:28:02Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-fitconnect","auto\_sync\_ms":0,"compare\_app\_state\_ms":468,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":15,"git\_ms":452,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":25,"persist\_app\_status\_ms":26,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":2,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:28:02Z","time\_ms":498} {"app-namespace":"argocd","application":"hie-test-34-minio","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:28:11Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-minio","auto\_sync\_ms":0,"compare\_app\_state\_ms":49,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":38,"git\_ms":8,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":19,"persist\_app\_status\_ms":20,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":8,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:28:11Z","time\_ms":81} {"app-namespace":"argocd","application":"hie-test-34-workflow-templates","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:28:11Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-workflow-templates","auto\_sync\_ms":0,"compare\_app\_state\_ms":279,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":244,"git\_ms":27,"health\_ms":0,"level":"info","live\_ms":5,"msg":"Reconciliation completed","normalize\_application\_ms":3,"patch\_ms":49,"persist\_app\_status\_ms":51,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":79,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:28:11Z","time\_ms":414} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:30:20Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":210,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":81,"git\_ms":121,"health\_ms":5,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":27,"persist\_app\_status\_ms":28,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":16,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:30:20Z","time\_ms":255} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:30:21Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":135,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":115,"git\_ms":11,"health\_ms":5,"level":"info","live\_ms":3,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":0,"persist\_app\_status\_ms":1,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":13,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:30:21Z","time\_ms":151} {"app-namespace":"argocd","application":"cert-manager","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:30:26Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"cert-manager","auto\_sync\_ms":0,"compare\_app\_state\_ms":363,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"cert-manager","dest-server":"https://kubernetes.default.svc","diff\_ms":320,"git\_ms":33,"health\_ms":6,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":29,"persist\_app\_status\_ms":32,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":88,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:30:26Z","time\_ms":486} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:30:33Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":110,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":96,"git\_ms":11,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":29,"persist\_app\_status\_ms":30,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":11,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:30:33Z","time\_ms":154} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:30:53Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":105,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":90,"git\_ms":11,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":26,"persist\_app\_status\_ms":26,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:30:53Z","time\_ms":145} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:30:54Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":136,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":121,"git\_ms":11,"health\_ms":1,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":0,"persist\_app\_status\_ms":0,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":11,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:30:54Z","time\_ms":151} {"app-namespace":"argocd","application":"hie-test-34-ffcloud-service","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:30:54Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-ffcloud-service","auto\_sync\_ms":0,"compare\_app\_state\_ms":31,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":20,"git\_ms":9,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":31,"persist\_app\_status\_ms":32,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":4,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:30:54Z","time\_ms":69} {"app-namespace":"argocd","application":"hie-test-34-workflows-api","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:30:54Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-workflows-api","auto\_sync\_ms":0,"compare\_app\_state\_ms":17,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":8,"git\_ms":8,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":23,"persist\_app\_status\_ms":24,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":2,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:30:54Z","time\_ms":45} {"app-namespace":"argocd","application":"spicedb","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:31:04Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"spicedb","auto\_sync\_ms":0,"compare\_app\_state\_ms":289,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"spicedb","dest-server":"https://kubernetes.default.svc","diff\_ms":31,"git\_ms":255,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":28,"persist\_app\_status\_ms":28,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":4,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:31:04Z","time\_ms":323} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (comparison expired, requesting refresh. reconciledAt: 2026-02-12 13:24:40 +0000 UTC, expiry: 3m0s), level (2)","project":"fitfile","time":"2026-02-12T13:31:05Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:31:05Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":14,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:31:05Z","time\_ms":14} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:31:05Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:31:05Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:31:05Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":57,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":35,"git\_ms":15,"health\_ms":5,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":18,"persist\_app\_status\_ms":18,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":55,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:31:05Z","time\_ms":132} {"app-namespace":"argocd","application":"hie-test-34-postgresql","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:33:19Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-postgresql","auto\_sync\_ms":0,"compare\_app\_state\_ms":29,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":21,"git\_ms":6,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":31,"persist\_app\_status\_ms":31,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":4,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:33:19Z","time\_ms":66} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:33:28Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":106,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":91,"git\_ms":12,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":22,"persist\_app\_status\_ms":23,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":29,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:33:28Z","time\_ms":161} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:33:28Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":149,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":134,"git\_ms":12,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":0,"persist\_app\_status\_ms":0,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":11,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:33:28Z","time\_ms":163} {"app-namespace":"argocd","application":"prometheus-operator-crds","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:33:32Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"prometheus-operator-crds","auto\_sync\_ms":0,"compare\_app\_state\_ms":406,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"","dest-server":"https://kubernetes.default.svc","diff\_ms":322,"git\_ms":64,"health\_ms":16,"level":"info","live\_ms":2,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":22,"persist\_app\_status\_ms":22,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":106,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:33:32Z","time\_ms":535} {"app-namespace":"argocd","application":"hie-test-34-workflow-templates","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:33:55Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-workflow-templates","auto\_sync\_ms":0,"compare\_app\_state\_ms":240,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":174,"git\_ms":61,"health\_ms":0,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":2,"patch\_ms":43,"persist\_app\_status\_ms":46,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":39,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:33:56Z","time\_ms":328} {"app-namespace":"argocd","application":"hie-test-34-fitconnect","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:33:56Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-fitconnect","auto\_sync\_ms":0,"compare\_app\_state\_ms":27,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":16,"git\_ms":9,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":21,"persist\_app\_status\_ms":22,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":5,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:33:56Z","time\_ms":55} {"app-namespace":"argocd","application":"hie-test-34-ffcloud-service","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:33:59Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-ffcloud-service","auto\_sync\_ms":0,"compare\_app\_state\_ms":38,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":26,"git\_ms":10,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":2,"patch\_ms":24,"persist\_app\_status\_ms":26,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":9,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:33:59Z","time\_ms":77} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:34:01Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":389,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":102,"git\_ms":279,"health\_ms":5,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":30,"persist\_app\_status\_ms":31,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":14,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:34:01Z","time\_ms":437} {"app-namespace":"argocd","application":"hie-test-34-minio","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:34:01Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-minio","auto\_sync\_ms":0,"compare\_app\_state\_ms":34,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":24,"git\_ms":8,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":26,"persist\_app\_status\_ms":27,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":4,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:34:01Z","time\_ms":67} {"app-namespace":"argocd","application":"hie-test-34-mongodb-b17ef","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:34:05Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-mongodb-b17ef","auto\_sync\_ms":0,"compare\_app\_state\_ms":172,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":44,"git\_ms":124,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":20,"persist\_app\_status\_ms":20,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":6,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:34:05Z","time\_ms":200} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:34:34Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":125,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":106,"git\_ms":12,"health\_ms":5,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":29,"persist\_app\_status\_ms":29,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:34:34Z","time\_ms":169} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:35:19Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":97,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":79,"git\_ms":10,"health\_ms":5,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":31,"persist\_app\_status\_ms":32,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":13,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:35:19Z","time\_ms":144} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:36:13Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":99,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":77,"git\_ms":9,"health\_ms":11,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":2,"patch\_ms":35,"persist\_app\_status\_ms":36,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":27,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:36:13Z","time\_ms":166} {"app-namespace":"argocd","application":"hie-test-34-workflows-api","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:36:23Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-workflows-api","auto\_sync\_ms":0,"compare\_app\_state\_ms":250,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":9,"git\_ms":239,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":24,"persist\_app\_status\_ms":25,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":2,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:36:23Z","time\_ms":278} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:36:27Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":104,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":90,"git\_ms":11,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":26,"persist\_app\_status\_ms":27,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":11,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:36:27Z","time\_ms":145} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:36:27Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":105,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":91,"git\_ms":10,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":0,"persist\_app\_status\_ms":0,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:36:27Z","time\_ms":119} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:36:28Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":115,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":99,"git\_ms":9,"health\_ms":5,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":27,"persist\_app\_status\_ms":28,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:36:28Z","time\_ms":158} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:36:28Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":96,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":79,"git\_ms":10,"health\_ms":5,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":0,"persist\_app\_status\_ms":0,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:36:28Z","time\_ms":111} {"app-namespace":"argocd","application":"spicedb","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:36:29Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"spicedb","auto\_sync\_ms":0,"compare\_app\_state\_ms":43,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"spicedb","dest-server":"https://kubernetes.default.svc","diff\_ms":30,"git\_ms":10,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":24,"persist\_app\_status\_ms":24,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":4,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:36:29Z","time\_ms":73} {"app-namespace":"argocd","application":"cert-manager","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:36:32Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"cert-manager","auto\_sync\_ms":0,"compare\_app\_state\_ms":340,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"cert-manager","dest-server":"https://kubernetes.default.svc","diff\_ms":305,"git\_ms":25,"health\_ms":6,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":72,"persist\_app\_status\_ms":74,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":80,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:36:32Z","time\_ms":498} {"app-namespace":"argocd","application":"hie-test-34-postgresql","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:36:40Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-postgresql","auto\_sync\_ms":0,"compare\_app\_state\_ms":39,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":30,"git\_ms":6,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":30,"persist\_app\_status\_ms":30,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":4,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:36:40Z","time\_ms":75} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (comparison expired, requesting refresh. reconciledAt: 2026-02-12 13:31:05 +0000 UTC, expiry: 3m0s), level (2)","project":"fitfile","time":"2026-02-12T13:36:53Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:36:53Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":11,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:36:53Z","time\_ms":11} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:36:54Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:36:54Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:36:54Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":56,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":37,"git\_ms":12,"health\_ms":5,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":24,"persist\_app\_status\_ms":25,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":22,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:36:54Z","time\_ms":105} {"app-namespace":"argocd","application":"hie-test-34-fitconnect","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:36:59Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-fitconnect","auto\_sync\_ms":0,"compare\_app\_state\_ms":31,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":18,"git\_ms":12,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":34,"persist\_app\_status\_ms":35,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":2,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:36:59Z","time\_ms":70} {"app-namespace":"argocd","application":"hie-test-34-workflow-templates","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:37:00Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-workflow-templates","auto\_sync\_ms":0,"compare\_app\_state\_ms":223,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":195,"git\_ms":23,"health\_ms":0,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":2,"patch\_ms":61,"persist\_app\_status\_ms":63,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":36,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:37:00Z","time\_ms":326} {"app-namespace":"argocd","application":"hie-test-34-ffcloud-service","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:37:06Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-ffcloud-service","auto\_sync\_ms":0,"compare\_app\_state\_ms":34,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":20,"git\_ms":13,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":28,"persist\_app\_status\_ms":29,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":4,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:37:06Z","time\_ms":71} {"app-namespace":"argocd","application":"prometheus-operator-crds","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:37:12Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"prometheus-operator-crds","auto\_sync\_ms":0,"compare\_app\_state\_ms":413,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"","dest-server":"https://kubernetes.default.svc","diff\_ms":329,"git\_ms":64,"health\_ms":17,"level":"info","live\_ms":2,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":13,"persist\_app\_status\_ms":14,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":120,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:37:12Z","time\_ms":549} {"app-namespace":"argocd","application":"hie-test-34-minio","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:39:14Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-minio","auto\_sync\_ms":0,"compare\_app\_state\_ms":32,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":24,"git\_ms":6,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":27,"persist\_app\_status\_ms":27,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":4,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:39:14Z","time\_ms":66} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:39:37Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":640,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":78,"git\_ms":552,"health\_ms":7,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":41,"persist\_app\_status\_ms":42,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":16,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:39:37Z","time\_ms":699} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:39:37Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":126,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":108,"git\_ms":10,"health\_ms":5,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":0,"persist\_app\_status\_ms":0,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:39:37Z","time\_ms":141} {"app-namespace":"argocd","application":"hie-test-34-mongodb-b17ef","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:40:01Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-mongodb-b17ef","auto\_sync\_ms":0,"compare\_app\_state\_ms":252,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":61,"git\_ms":188,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":39,"persist\_app\_status\_ms":39,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":6,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:40:01Z","time\_ms":300} {"app-namespace":"argocd","application":"spicedb","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:40:05Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"spicedb","auto\_sync\_ms":0,"compare\_app\_state\_ms":299,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"spicedb","dest-server":"https://kubernetes.default.svc","diff\_ms":31,"git\_ms":265,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":37,"persist\_app\_status\_ms":37,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":4,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:40:05Z","time\_ms":343} {"app-namespace":"argocd","application":"hie-test-34-fitconnect","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:40:05Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-fitconnect","auto\_sync\_ms":0,"compare\_app\_state\_ms":26,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":16,"git\_ms":8,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":26,"persist\_app\_status\_ms":27,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":2,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:40:05Z","time\_ms":57} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:40:06Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":143,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":127,"git\_ms":12,"health\_ms":2,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":26,"persist\_app\_status\_ms":26,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":16,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:40:06Z","time\_ms":188} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:40:06Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":112,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":98,"git\_ms":10,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":0,"persist\_app\_status\_ms":0,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:40:06Z","time\_ms":126} {"app-namespace":"argocd","application":"hie-test-34-workflows-api","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:40:11Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-workflows-api","auto\_sync\_ms":0,"compare\_app\_state\_ms":18,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":8,"git\_ms":8,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":28,"persist\_app\_status\_ms":28,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":1,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:40:11Z","time\_ms":49} {"app-namespace":"argocd","application":"hie-test-34-minio","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:42:15Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-minio","auto\_sync\_ms":0,"compare\_app\_state\_ms":31,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":23,"git\_ms":6,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":25,"persist\_app\_status\_ms":25,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":4,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:42:15Z","time\_ms":63} {"app-namespace":"argocd","application":"hie-test-34-workflow-templates","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:42:21Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-workflow-templates","auto\_sync\_ms":0,"compare\_app\_state\_ms":242,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":209,"git\_ms":28,"health\_ms":1,"level":"info","live\_ms":2,"msg":"Reconciliation completed","normalize\_application\_ms":3,"patch\_ms":162,"persist\_app\_status\_ms":164,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":39,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:42:21Z","time\_ms":450} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:42:23Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":111,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":97,"git\_ms":10,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":61,"persist\_app\_status\_ms":63,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":19,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:42:23Z","time\_ms":196} {"app-namespace":"argocd","application":"hie-test-34-ffcloud-service","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"fitfile","time":"2026-02-12T13:42:24Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-ffcloud-service","auto\_sync\_ms":0,"compare\_app\_state\_ms":31,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":21,"git\_ms":8,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":29,"persist\_app\_status\_ms":30,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":3,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:42:24Z","time\_ms":67} {"app-namespace":"argocd","application":"hie-test-34-postgresql","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:42:33Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"hie-test-34-postgresql","auto\_sync\_ms":0,"compare\_app\_state\_ms":29,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"hie-test-34","dest-server":"https://kubernetes.default.svc","diff\_ms":21,"git\_ms":6,"health\_ms":0,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":20,"persist\_app\_status\_ms":20,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":3,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:42:33Z","time\_ms":54} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:42:36Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":94,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":78,"git\_ms":9,"health\_ms":5,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":140,"persist\_app\_status\_ms":141,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":23,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:42:36Z","time\_ms":261} {"app-namespace":"argocd","application":"argo-workflows","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:42:36Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"argo-workflows","auto\_sync\_ms":0,"compare\_app\_state\_ms":122,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argo","dest-server":"https://kubernetes.default.svc","diff\_ms":104,"git\_ms":10,"health\_ms":5,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":0,"persist\_app\_status\_ms":0,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":12,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:42:36Z","time\_ms":137} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:42:38Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":105,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":91,"git\_ms":10,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":47,"persist\_app\_status\_ms":48,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":11,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:42:38Z","time\_ms":166} {"app-namespace":"argocd","application":"grafana-k8s-monitoring","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:42:38Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"grafana-k8s-monitoring","auto\_sync\_ms":0,"compare\_app\_state\_ms":107,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"monitoring","dest-server":"https://kubernetes.default.svc","diff\_ms":93,"git\_ms":10,"health\_ms":1,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":0,"persist\_app\_status\_ms":1,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":17,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:42:38Z","time\_ms":126} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (comparison expired, requesting refresh. reconciledAt: 2026-02-12 13:36:53 +0000 UTC, expiry: 3m0s), level (2)","project":"fitfile","time":"2026-02-12T13:42:43Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:42:43Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":10,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:42:43Z","time\_ms":10} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:42:43Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:42:43Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:42:43Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":53,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":35,"git\_ms":10,"health\_ms":6,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":19,"persist\_app\_status\_ms":19,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":23,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:42:43Z","time\_ms":97} {"app-namespace":"argocd","application":"cert-manager","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:42:44Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"cert-manager","auto\_sync\_ms":0,"compare\_app\_state\_ms":341,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"cert-manager","dest-server":"https://kubernetes.default.svc","diff\_ms":301,"git\_ms":30,"health\_ms":7,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":73,"persist\_app\_status\_ms":74,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":61,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:42:44Z","time\_ms":480} {"app-namespace":"argocd","application":"prometheus-operator-crds","level":"info","msg":"Skipping auto-sync: application status is Synced","project":"default","time":"2026-02-12T13:42:49Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"prometheus-operator-crds","auto\_sync\_ms":0,"compare\_app\_state\_ms":396,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"","dest-server":"https://kubernetes.default.svc","diff\_ms":316,"git\_ms":61,"health\_ms":16,"level":"info","live\_ms":2,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":28,"persist\_app\_status\_ms":29,"process\_finalizers\_ms":0,"project":"default","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":106,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:42:49Z","time\_ms":532} awsadmin@ip-10-66-2-4:~/terraform$ kubectl annotate application -n argocd ff-hie-test-34 argocd.argoproj.io/refresh=hard --overwrite application.argoproj.io/ff-hie-test-34 annotated

---

Perfect—this narrows it a lot.

### What We Learned from Your Outputs

1. `ff-hie-test-34` has no helm parameters, only a values file:
- `["/ffnodes/eoe/hie-test-34/values.yaml"]`

So whether `certificates` and `hie-test-34-frontend` are rendered is driven entirely by that values.yaml + chart logic.

1. You're logging the controller correctly (it's a StatefulSet, not a Deployment). ✅
2. The controller logs show this key line repeatedly:

> `Skipping auto-sync: failed previous sync attempt to d4ee068…`

That explains why it stays OutOfSync forever: Argo CD will not auto-sync again after a failed sync attempt, until you intervene (manual sync / clear the failure / change revision / reset operation). Your hard refresh updates the comparison, but it doesn't "retry sync".

1. We still haven't seen the actual _reason_ for the failed sync in the controller logs you grepped. Your grep pattern is missing the most common "why" strings (and it didn't include `frontend` / `certificates` lines either). The logs you pasted are mostly reconciliation timing lines, not sync errors.

---

## The Most Likely Root Cause (based on symptoms)

- The parent app (`ff-hie-test-34`) desires child `Application` resources (`certificates`, `hie-test-34-frontend`), but those Application CRs do not exist when you try `kubectl get application -n argocd certificates`.
- That leaves the parent OutOfSync (missing desired resources).
- A previous sync attempt failed (maybe during the Auth0 issue earlier, or during child creation), and now auto-sync is suppressed until you manually resync.

We need one concrete thing now:

✅ Find the exact sync failure reason (it'll be in the `ff-hie-test-34` Application status, events, or controller logs without the restrictive grep).

---

## Do This next (commands only)

### 1) Pull the Parent App's syncResult Details (often Contains the First failing resource)

You posted a version earlier that didn't include `certificates` / `frontend`—but run it again now after the refresh. If they appear with a failure message, we've got it.

### 2) Get Recent Kubernetes Events for the Parent App

This is _hugely_ useful because Argo emits Events when it can't create/update a resource.

### 3) Widen the Controller Log search (remove the Tight grep)

Right now your grep filters out most errors. Instead:

If that's too noisy, we can tighten it after we see the real error phrase.

### 4) Confirm the Argo Project Restrictions (still My 1 Suspect for "child Apps Never created")

If the project is locked down and doesn't allow `argoproj.io/Application`, Argo will refuse to create `certificates` + `frontend` Applications, leaving the parent OutOfSync forever.

---

## How to "unstick" Auto-sync once the Issue is Fixed

Once you fix the underlying problem (policy, invalid child spec, etc.), you need to trigger an actual sync, not just refresh.

### If You Have Argocd CLI

### If You Don't Have Argocd CLI

You can trigger a sync via the Application "operation" field by patching, but that's messy. The clean Kubernetes-only approach is typically:

- use the Argo UI "Sync" button, or
- install/use `argocd` CLI.

(Refresh ≠ Sync; refresh just re-compares.)

---

## Quick Sanity Check: Are You Sure Those Child Apps Should Exist?

Because your `kubectl get applications -n argocd` list does not include `certificates` or `hie-test-34-frontend` at all. That means either:

- the chart is trying to create them but failing, or
- the chart used to create them (hence Argo remembers them as desired) but the rendered manifests no longer include them, and Argo's app tree is stale (less likely, given it consistently lists them).

The controller log line `GetRepoObjs stats` indicates it _is_ pulling manifests each time, so stale desire is less likely.

---

If you run (1) and (2) above, we'll have the exact "why" in plain text and can close this out cleanly (and it'll slot nicely into the playbook you're building).

---

kubectl get application -n argocd ff-hie-test-34 -o jsonpath='{range.status.operationState.syncResult.resources\[\*\]}{.kind}{" "}{.namespace}{" "}{.name}{" hookPhase="}{.hookPhase}{" status="}{.status}{" message="}{.message}{"\\n"}{end}' Application argocd prometheus-operator-crds hookPhase=Succeeded status=Synced message=application.argoproj.io/prometheus-operator-crds unchanged Application argocd cert-manager hookPhase=Succeeded status=Synced message=application.argoproj.io/cert-manager unchanged Application argocd grafana-k8s-monitoring hookPhase=Succeeded status=Synced message=application.argoproj.io/grafana-k8s-monitoring unchanged Application argocd hie-test-34-postgresql hookPhase=Succeeded status=Synced message=application.argoproj.io/hie-test-34-postgresql unchanged Application argocd argo-workflows hookPhase=Succeeded status=Synced message=application.argoproj.io/argo-workflows unchanged Application argocd hie-test-34-minio hookPhase=Succeeded status=Synced message=application.argoproj.io/hie-test-34-minio unchanged Application argocd hie-test-34-mongodb-b17ef hookPhase=Succeeded status=Synced message=application.argoproj.io/hie-test-34-mongodb-b17ef unchanged Application argocd spicedb hookPhase=Succeeded status=Synced message=application.argoproj.io/spicedb unchanged Application argocd hie-test-34-workflow-templates hookPhase=Succeeded status=Synced message=application.argoproj.io/hie-test-34-workflow-templates unchanged Application argocd hie-test-34-workflows-api hookPhase=Succeeded status=Synced message=application.argoproj.io/hie-test-34-workflows-api unchanged Application argocd hie-test-34-fitconnect hookPhase=Failed status=Synced message=Failed sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9: one or more synchronization tasks completed unsuccessfully (retried 5 times). Application argocd hie-test-34-ffcloud-service hookPhase=Succeeded status=Synced message=application.argoproj.io/hie-test-34-ffcloud-service unchanged awsadmin@ip-10-66-2-4:~/terraform$ kubectl -n argocd get events --sort-by=.lastTimestamp | tail -n 80 | egrep -i 'ff-hie-test-34|certificates|frontend|Denied|forbidden|Invalid|sync|error' 37m Normal ResourceUpdated application/ff-hie-test-34 Updated health status: Degraded -> Healthy 37m Normal ResourceUpdated application/hie-test-34-fitconnect Updated sync status: OutOfSync -> Synced 21m Normal ResourceUpdated application/ff-hie-test-34 Updated health status: Healthy -> Progressing 20m Normal ResourceUpdated application/ff-hie-test-34 Updated health status: Progressing -> Healthy 20m Normal ResourceUpdated application/ff-hie-test-34 Updated health status: Healthy -> Progressing 20m Normal ResourceUpdated application/ff-hie-test-34 Updated health status: Progressing -> Healthy awsadmin@ip-10-66-2-4:~/terraform$ kubectl -n argocd logs sts/argocd-application-controller --since=6h | egrep -i 'ff-hie-test-34|sync failed|operation|cannot|forbidden|denied|invalid|error|permission|appproject|rbac' {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (comparison expired, requesting refresh. reconciledAt: 2026-02-12 13:09:32 +0000 UTC, expiry: 3m0s), level (2)","project":"fitfile","time":"2026-02-12T13:15:55Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:15:55Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":298,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:15:55Z","time\_ms":299} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:15:56Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:15:56Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:15:56Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":344,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":35,"git\_ms":299,"health\_ms":8,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":1,"patch\_ms":16,"persist\_app\_status\_ms":17,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":27,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:15:56Z","time\_ms":391} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (comparison expired, requesting refresh. reconciledAt: 2026-02-12 13:15:55 +0000 UTC, expiry: 3m0s), level (2)","project":"fitfile","time":"2026-02-12T13:21:25Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:21:25Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":11,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:21:25Z","time\_ms":11} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:21:25Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:21:25Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:21:25Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":56,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":36,"git\_ms":11,"health\_ms":6,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":16,"persist\_app\_status\_ms":16,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":23,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:21:25Z","time\_ms":96} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (controller refresh requested), level (1)","project":"fitfile","time":"2026-02-12T13:24:16Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:24:16Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":10,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:24:16Z","time\_ms":11} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:24:16Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:24:16Z"} {"application":"ff-hie-test-34","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","level":"info","msg":"Updated health status: Healthy -\\u003e Progressing","reason":"ResourceUpdated","time":"2026-02-12T13:24:16Z","type":"Normal"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:24:16Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":56,"comparison-level":1,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":36,"git\_ms":11,"health\_ms":6,"level":"info","live\_ms":1,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":20,"persist\_app\_status\_ms":27,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":26,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:24:16Z","time\_ms":110} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (comparison expired, requesting refresh. reconciledAt: 2026-02-12 13:21:25 +0000 UTC, expiry: 3m0s), level (2)","project":"fitfile","time":"2026-02-12T13:24:40Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:24:40Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":14,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:24:40Z","time\_ms":14} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:24:40Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:24:40Z"} {"application":"ff-hie-test-34","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","level":"info","msg":"Updated health status: Progressing -\\u003e Healthy","reason":"ResourceUpdated","time":"2026-02-12T13:24:40Z","type":"Normal"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:24:40Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":58,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":36,"git\_ms":14,"health\_ms":6,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":28,"persist\_app\_status\_ms":44,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":30,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:24:40Z","time\_ms":134} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (controller refresh requested), level (1)","project":"fitfile","time":"2026-02-12T13:25:10Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:25:10Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":7,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:25:10Z","time\_ms":7} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:25:10Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:25:10Z"} {"application":"ff-hie-test-34","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","level":"info","msg":"Updated health status: Healthy -\\u003e Progressing","reason":"ResourceUpdated","time":"2026-02-12T13:25:10Z","type":"Normal"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:25:10Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":26,"comparison-level":1,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":10,"git\_ms":7,"health\_ms":6,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":17,"persist\_app\_status\_ms":24,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":23,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:25:10Z","time\_ms":75} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (controller refresh requested), level (1)","project":"fitfile","time":"2026-02-12T13:25:32Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:25:32Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":7,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:25:32Z","time\_ms":7} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:25:32Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:25:32Z"} {"application":"ff-hie-test-34","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","level":"info","msg":"Updated health status: Progressing -\\u003e Healthy","reason":"ResourceUpdated","time":"2026-02-12T13:25:32Z","type":"Normal"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:25:32Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":23,"comparison-level":1,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":7,"git\_ms":8,"health\_ms":5,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":23,"persist\_app\_status\_ms":30,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":22,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:25:32Z","time\_ms":77} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (comparison expired, requesting refresh. reconciledAt: 2026-02-12 13:24:40 +0000 UTC, expiry: 3m0s), level (2)","project":"fitfile","time":"2026-02-12T13:31:05Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:31:05Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":14,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:31:05Z","time\_ms":14} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:31:05Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:31:05Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:31:05Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":57,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":35,"git\_ms":15,"health\_ms":5,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":18,"persist\_app\_status\_ms":18,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":55,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:31:05Z","time\_ms":132} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (comparison expired, requesting refresh. reconciledAt: 2026-02-12 13:31:05 +0000 UTC, expiry: 3m0s), level (2)","project":"fitfile","time":"2026-02-12T13:36:53Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:36:53Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":11,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:36:53Z","time\_ms":11} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:36:54Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:36:54Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:36:54Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":56,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":37,"git\_ms":12,"health\_ms":5,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":24,"persist\_app\_status\_ms":25,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":22,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:36:54Z","time\_ms":105} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (comparison expired, requesting refresh. reconciledAt: 2026-02-12 13:36:53 +0000 UTC, expiry: 3m0s), level (2)","project":"fitfile","time":"2026-02-12T13:42:43Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:42:43Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":10,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:42:43Z","time\_ms":10} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:42:43Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:42:43Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:42:43Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":53,"comparison-level":2,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":35,"git\_ms":10,"health\_ms":6,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":19,"persist\_app\_status\_ms":19,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":23,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:42:43Z","time\_ms":97} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Refreshing app status (hard refresh requested), level (3)","project":"fitfile","time":"2026-02-12T13:44:07Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Comparing app state (cluster: <https://kubernetes.default.svc>, namespace: argocd)","project":"fitfile","time":"2026-02-12T13:44:07Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","build\_options\_ms":0,"level":"info","manifests\_ms":420,"msg":"GetRepoObjs stats","plugins\_ms":0,"project":"fitfile","repo\_ms":0,"time":"2026-02-12T13:44:07Z","time\_ms":420} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Executing compare of syncResult.Revision and commitSha because manifest changed: d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:44:07Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"warning","msg":"Skipping auto-sync: failed previous sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9","project":"fitfile","time":"2026-02-12T13:44:07Z"} {"app-namespace":"argocd","application":"ff-hie-test-34","level":"info","msg":"Update successful","project":"fitfile","time":"2026-02-12T13:44:07Z"} {"app-namespace":"argocd","app\_status\_update\_ms":0,"application":"ff-hie-test-34","auto\_sync\_ms":0,"compare\_app\_state\_ms":463,"comparison-level":3,"comparison\_with\_nothing\_ms":0,"dedup\_ms":0,"dest-name":"","dest-namespace":"argocd","dest-server":"https://kubernetes.default.svc","diff\_ms":35,"git\_ms":420,"health\_ms":6,"level":"info","live\_ms":0,"msg":"Reconciliation completed","normalize\_application\_ms":0,"patch\_ms":49,"persist\_app\_status\_ms":50,"process\_finalizers\_ms":0,"project":"fitfile","refresh\_app\_conditions\_ms":0,"set\_app\_managed\_resources\_ms":22,"setop\_ms":0,"settings\_ms":0,"sync\_ms":0,"time":"2026-02-12T13:44:07Z","time\_ms":537} awsadmin@ip-10-66-2-4:~/terraform$ kubectl get application -n argocd ff-hie-test-34 -o jsonpath='{.spec.project}{"\\n"}' PROJ=$(kubectl get application -n argocd ff-hie-test-34 -o jsonpath='{.spec.project}') kubectl get appproject -n argocd "$PROJ" -o yaml | egrep -n 'namespaceResourceWhitelist|clusterResourceWhitelist|destinations|sourceRepos|roles|policies|applications|argoproj' fitfile 1:apiVersion: argoproj.io/v1alpha1 9: - resources-finalizer.argocd.argoproj.io 18: clusterResourceWhitelist: 27: description: The main project for all fitfile applications 28: destinations: 31: sourceRepos:

---

Nice—this is now _very_ clear.

### What Your Latest Output Proves

- The parent sync attempt failed because of `hie-test-34-fitconnect`, and only that.
- Everything else in that operationState syncResult is "unchanged".
- Your `events` output shows no "forbidden/denied/invalid" messages (so this is not obviously AppProject/RBAC blocking at the Kubernetes API level).
- The controller logs you grabbed still don't show the underlying error—only "Skipping auto-sync: failed previous sync attempt …".

So the "root cause" is inside the child application `hie-test-34-fitconnect` (or one of _its_ resources), not the parent.

Also: your `egrep -n` on the AppProject shows only that those sections exist; we still need the actual contents of `clusterResourceWhitelist`, `destinations`, `sourceRepos` because those determine whether Argo can manage what fitconnect needs.

---

## Next Move: Interrogate the Child App Directly

### 1) Show why hie-test-34-fitconnect Last Sync Failed

This usually reveals the _actual_ Kubernetes object that failed (Deployment/Job/Ingress/Secret/etc) and the _actual_ error string (immutable field, invalid patch, forbidden, webhook denial, etc).

### 2) List Which Resources Are OutOfSync/Degraded in Fitconnect (current state)

If anything prints, that's your culprit set.

### 3) Pull the Child App's Conditions (often Contains the "money" error)

---

## Also: Actually Dump the Fitfile AppProject Rules (we Can't Infer from just the headings)

Run these _without grep_ so we see the values:

If that's too big, at least:

Why: fitconnect might be trying to create some CRD type (e.g., `Certificate`, `ExternalSecret`, `IngressRoute`, etc.) that isn't whitelisted for the project, which can cause sync failures that don't always show up in your parent's syncResult.

---

## One More Quick Check: is Parent only "failed" because it Tried to Sync the Child Application and that Child Was Already in Bad State?

This is consistent with your output:

- Parent lists `Application argocd hie-test-34-fitconnect … hookPhase=Failed … status=Synced`
	- i.e., the _Application object itself_ exists and is "Synced" as a manifest,
	- but Argo marks the hookPhase failed because the child's sync operation failed.

So: fix child sync failure → then manually sync parent (or re-enable auto-sync).

---

### If You Paste the Outputs from the Three hie-test-34-fitconnect Commands Above, We'll Know the Exact failing Resource and the Exact Kubernetes Error String, and I Can Tell You the Precise Fix (immutable Fields, RBAC, Webhook Denial, Missing Namespace, Invalid Spec, etc.)

---

kubectl get application -n argocd hie-test-34-fitconnect -o jsonpath='{.status.operationState.phase}{"\\n"}{.status.operationState.message}{"\\n"}' kubectl get application -n argocd hie-test-34-fitconnect -o jsonpath='{range.status.operationState.syncResult.resources\[\*\]}{.kind}{" "}{.namespace}{" "}{.name}{" status="}{.status}{" message="}{.message}{"\\n"}{end}' Failed one or more synchronization tasks completed unsuccessfully (retried 5 times). ConfigMap hie-test-34 fitconnect-load-definition status=Synced message=configmap/fitconnect-load-definition unchanged ConfigMap hie-test-34 hie-test-34-fitconnect-ftc-config-3ad7d286319b68f329e68a5b45f8d status=Synced message=configmap/hie-test-34-fitconnect-ftc-config-3ad7d286319b68f329e68a5b45f8d unchanged Service hie-test-34 hie-test-34-fitconnect-ftc status=Synced message=service/hie-test-34-fitconnect-ftc unchanged Deployment hie-test-34 hie-test-34-fitconnect-ftc status=Synced message=Deployment "hie-test-34-fitconnect-ftc" exceeded its progress deadline Ingress hie-test-34 hie-test-34-fitconnect-ftc-ingress status=Synced message=ingress.networking.k8s.io/hie-test-34-fitconnect-ftc-ingress unchanged VaultStaticSecret hie-test-34 fitconnect status=Synced message=vaultstaticsecret.secrets.hashicorp.com/fitconnect unchanged awsadmin@ip-10-66-2-4:~/terraform$ kubectl get application -n argocd hie-test-34-fitconnect -o jsonpath='{range.status.resources\[\*\]}{.kind}{" "}{.namespace}{" "}{.name}{" sync="}{.status}{" health="}{.health.status}{"\\n"}{end}' | egrep -v 'sync=Synced health=Healthy' ConfigMap hie-test-34 fitconnect-load-definition sync=Synced health= ConfigMap hie-test-34 hie-test-34-fitconnect-ftc-config-3ad7d286319b68f329e68a5b45f8d sync=Synced health= Service hie-test-34 hie-test-34-fitconnect-ftc sync=Synced health= Deployment hie-test-34 hie-test-34-fitconnect-ftc sync=Synced health= Ingress hie-test-34 hie-test-34-fitconnect-ftc-ingress sync=Synced health= VaultStaticSecret hie-test-34 fitconnect sync=Synced health= awsadmin@ip-10-66-2-4:~/terraform$ kubectl get appproject -n argocd fitfile -o yaml apiVersion: argoproj.io/v1alpha1 kind: AppProject metadata: annotations: meta.helm.sh/release-name: fitfile-project meta.helm.sh/release-namespace: argocd creationTimestamp: "2026-02-11T13:25:34Z" finalizers: - resources-finalizer.argocd.argoproj.io generation: 1 labels: app.kubernetes.io/managed-by: Helm name: fitfile namespace: argocd resourceVersion: "466590" uid: dd5b9795-cea1-45d1-9715-b9a4cd72c253 spec: clusterResourceWhitelist: - group: '\*' kind: ClusterIssuer - group: '\*' kind: PriorityClass - group: admissionregistration.k8s.io kind: MutatingWebhookConfiguration - group: admissionregistration.k8s.io kind: ValidatingWebhookConfiguration description: The main project for all fitfile applications destinations: - namespace: '\*' server: <https://kubernetes.default.svc> sourceRepos: - <https://gitlab.com/fitfile/deployment.git>

---

Perfect—now we have the _real_ failure:

> `Deployment "hie-test-34-fitconnect-ftc" exceeded its progress deadline`

That's not an ArgoCD/AppProject/RBAC issue. Your AppProject allows `destinations: *` and has broad enough whitelist for what you're doing, and Argo successfully applied everything ("Synced"). Kubernetes just never got the Deployment to become "Available" within `progressDeadlineSeconds`.

So you're in Kubernetes rollout debugging territory: pods aren't becoming Ready (crashloop, failing probes, image pull, pending scheduling, init container stuck, secret missing, etc.).

---

## Fastest Path to the Root Cause (copy/paste)

### 1) See Exactly what Kubernetes Thinks is Wrong with the Deployment

Scroll to:

- Conditions
- Events at the bottom (usually the smoking gun)

### 2) See Pod State + why They're not Ready

Then for the _newest_ pod (or any not Running/Ready):

Check:

- `Events:` (image pull errors, probe failures, forbidden, mount errors)
- `Containers:` state (Waiting/Terminated reasons)

### 3) If Pods Are Running but not Ready: Check Probe Failures and Logs

---

## "Exceeded Progress deadline" Usually means One of These 6 Things

### A) CrashLoopBackOff

Symptoms: pod restarts, `--previous` logs show app exits.

- Fix: app config/env, DB connectivity, missing secret, bad command, etc.

### B) Readiness/Liveness Probe failing

Symptoms: pod Running but `READY 0/1`, events show `Readiness probe failed`.

- Fix: wrong path/port, app slow startup, needs longer `initialDelaySeconds`, needs correct scheme/host.

### C) ImagePullBackOff / ErrImagePull

Symptoms: pod stuck Pending, events show auth/not found.

- Fix: image tag wrong, registry creds missing, IRSA/ECR auth, etc.

### D) Pending Scheduling

Symptoms: `Pending`, events show insufficient CPU/memory, taints, node selector, PDB, etc.

- Fix: resources, tolerations, add capacity.

### E) Volume/secret/config Errors

Symptoms: `CreateContainerConfigError`, `MountVolume.SetUp failed`, missing secret/configmap.

- Fix: secret name mismatch, projected volumes, CSI issues.

### F) Waiting on External Secret (VaultStaticSecret)

You _do_ have a `VaultStaticSecret fitconnect` object. If that secret isn't actually materializing into a K8s Secret (or is incomplete), the pod can fail to start or crash.

Check:

---

## Quick Rollout Status Commands (nice and compact)

---

## Why Argo Shows "Synced" but Still "Failed"

Argo marks resource apply as "Synced" because the manifests were applied successfully, but it waits for health. A Deployment can be applied fine and still be Unhealthy/ProgressDeadlineExceeded, and that makes the sync operation fail.

---

## What I Need from You to Tell You the Exact Fix

Paste just these two outputs (they'll contain the precise reason):

If you also include the `describe pod <pod>` for a failing pod, I can usually point to the single line in Events and tell you exactly what to change (probe, image, secret, scheduling, etc.).

---

kubectl get application -n argocd hie-test-34-fitconnect -o jsonpath='{range.status.resources\[\*\]}{.kind}{" "}{.namespace}{" "}{.name}{" sync="}{.status}{" health="}{.health.status}{"\\n"}{end}' | egrep -v 'sync=Synced health=Healthy' ConfigMap hie-test-34 fitconnect-load-definition sync=Synced health= ConfigMap hie-test-34 hie-test-34-fitconnect-ftc-config-3ad7d286319b68f329e68a5b45f8d sync=Synced health= Service hie-test-34 hie-test-34-fitconnect-ftc sync=Synced health= Deployment hie-test-34 hie-test-34-fitconnect-ftc sync=Synced health= Ingress hie-test-34 hie-test-34-fitconnect-ftc-ingress sync=Synced health= VaultStaticSecret hie-test-34 fitconnect sync=Synced health= awsadmin@ip-10-66-2-4:~/terraform$ kubectl get appproject -n argocd fitfile -o yaml apiVersion: argoproj.io/v1alpha1 kind: AppProject metadata: annotations: meta.helm.sh/release-name: fitfile-project meta.helm.sh/release-namespace: argocd creationTimestamp: "2026-02-11T13:25:34Z" finalizers: - resources-finalizer.argocd.argoproj.io generation: 1 labels: app.kubernetes.io/managed-by: Helm name: fitfile namespace: argocd resourceVersion: "466590" uid: dd5b9795-cea1-45d1-9715-b9a4cd72c253 spec: clusterResourceWhitelist: - group: '\*' kind: ClusterIssuer - group: '\*' kind: PriorityClass - group: admissionregistration.k8s.io kind: MutatingWebhookConfiguration - group: admissionregistration.k8s.io kind: ValidatingWebhookConfiguration description: The main project for all fitfile applications destinations: - namespace: '\*' server: <https://kubernetes.default.svc> sourceRepos: - <https://gitlab.com/fitfile/deployment.git> awsadmin@ip-10-66-2-4:~/terraform$ kubectl -n hie-test-34 describe deploy hie-test-34-fitconnect-ftc Name: hie-test-34-fitconnect-ftc Namespace: hie-test-34 CreationTimestamp: Wed, 11 Feb 2026 16:22:16 +0000 Labels: <none> Annotations: argocd.argoproj.io/tracking-id: hie-test-34-fitconnect:apps/Deployment:hie-test-34/hie-test-34-fitconnect-ftc deployment.kubernetes.io/revision: 8 Selector: app=hie-test-34-fitconnect-ftc Replicas: 1 desired | 1 updated | 1 total | 1 available | 0 unavailable StrategyType: RollingUpdate MinReadySeconds: 0 RollingUpdateStrategy: 25% max unavailable, 25% max surge Pod Template: Labels: app=hie-test-34-fitconnect-ftc Annotations: kubectl.kubernetes.io/restartedAt: 2026-02-12T10:17:06Z vso.secrets.hashicorp.com/restartedAt: 2026-02-12T13:25:10Z Init Containers: hie-test-34-fitconnect-ftc-init: Image: fitfileregistry.azurecr.io/fitconnect-service:1.0.695 Port: <none> Host Port: <none> Command: yarn db:migrate:remote:up Environment: NODE\_ENV: production FITFILE\_ENV: production LOAD\_DEFINITION\_PATH: /config/load\_definition.json Mounts: /config from config (ro) /secrets from fitconnect-secrets (ro) Containers: hie-test-34-fitconnect-ftc: Image: fitfileregistry.azurecr.io/fitconnect-service:1.0.695 Port: 4000/TCP (http) Host Port: 0/TCP (http) Command: node --require./instrumentation.js server.js Requests: cpu: 100m Liveness: http-get http://:4000/fitconnect/readyz%3FhealthServiceName=TenantDocumentHealthService&healthServiceName=SpiceDbSchemaConnectionHealthService&healthServiceName=MongoDBConnectionHealthService&healthServiceName=PostgresDBConnectionHealthService&healthServiceName=MinioS3ConnectionHealthService&healthServiceName=WorkflowsAPIConnectionHealthService&healthServiceName=Auth0PingHealthService delay=15s timeout=12s period=15s success=1 failure=3 Readiness: http-get http://:4000/fitconnect/readyz%3FhealthServiceName=TenantDocumentHealthService&healthServiceName=SpiceDbSchemaConnectionHealthService&healthServiceName=MongoDBConnectionHealthService&healthServiceName=PostgresDBConnectionHealthService&healthServiceName=MinioS3ConnectionHealthService&healthServiceName=WorkflowsAPIConnectionHealthService&healthServiceName=Auth0PingHealthService delay=15s timeout=12s period=15s success=1 failure=3 Environment: NODE\_ENV: production FITFILE\_ENV: production LOAD\_DEFINITION\_PATH: /config/load\_definition.json Mounts: /config from config (ro) /secrets from fitconnect-secrets (ro) Volumes: fitconnect-secrets: Type: Secret (a volume populated by a Secret) SecretName: fitconnect Optional: false config: Type: Projected (a volume that contains injected data from multiple sources) ConfigMapName: hie-test-34-fitconnect-ftc-config-3ad7d286319b68f329e68a5b45f8d Optional: false ConfigMapName: fitconnect-load-definition Optional: false Node-Selectors: <none> Tolerations: <none> Conditions: Type Status Reason ---- ------ ------ Available True MinimumReplicasAvailable Progressing True NewReplicaSetAvailable OldReplicaSets: hie-test-34-fitconnect-ftc-845b98ddd7 (0/0 replicas created) NewReplicaSet: hie-test-34-fitconnect-ftc-fffdf4c6c (1/1 replicas created) Events: Type Reason Age From Message ---- ------ ---- ---- ------- Normal ScalingReplicaSet 46m deployment-controller Scaled down replica set hie-test-34-fitconnect-ftc-77b9d454f from 1 to 0 Normal ScalingReplicaSet 23m deployment-controller Scaled up replica set hie-test-34-fitconnect-ftc-fffdf4c6c from 0 to 1 Normal ScalingReplicaSet 23m deployment-controller Scaled down replica set hie-test-34-fitconnect-ftc-845b98ddd7 from 1 to 0 awsadmin@ip-10-66-2-4:~/terraform$ kubectl -n hie-test-34 get pods -l app.kubernetes.io/name=fitconnect-ftc -o wide # if that label doesn't match, use: kubectl -n hie-test-34 get pods | grep fitconnect No resources found in hie-test-34 namespace. hie-test-34-fitconnect-ftc-fffdf4c6c-dgfp9 1/1 Running 0 23m awsadmin@ip-10-66-2-4:~/terraform$ kubectl -n hie-test-34 describe pod hie-test-34-fitconnect-ftc-fffdf4c6c-dgfp9 Name: hie-test-34-fitconnect-ftc-fffdf4c6c-dgfp9 Namespace: hie-test-34 Priority: 0 Service Account: default Node: ip-10-66-5-187.eu-west-2.compute.internal/10.66.5.187 Start Time: Thu, 12 Feb 2026 13:25:10 +0000 Labels: app=hie-test-34-fitconnect-ftc pod-template-hash=fffdf4c6c Annotations: kubectl.kubernetes.io/restartedAt: 2026-02-12T10:17:06Z vso.secrets.hashicorp.com/restartedAt: 2026-02-12T13:25:10Z Status: Running IP: 10.66.4.101 IPs: IP: 10.66.4.101 Controlled By: ReplicaSet/hie-test-34-fitconnect-ftc-fffdf4c6c Init Containers: hie-test-34-fitconnect-ftc-init: Container ID: containerd://a58d50b2ff7385e1c7e5a37ece69f1c8666a8ece14714358482763500d2811ae Image: fitfileregistry.azurecr.io/fitconnect-service:1.0.695 Image ID: fitfileregistry.azurecr.io/fitconnect-service@sha256:1d7e38f7c216ba904d1658445c3bcb05101a7fda5df1f3a56e497159e71da343 Port: <none> Host Port: <none> Command: yarn db:migrate:remote:up State: Terminated Reason: Completed Exit Code: 0 Started: Thu, 12 Feb 2026 13:25:11 +0000 Finished: Thu, 12 Feb 2026 13:25:13 +0000 Ready: True Restart Count: 0 Environment: NODE\_ENV: production FITFILE\_ENV: production LOAD\_DEFINITION\_PATH: /config/load\_definition.json Mounts: /config from config (ro) /secrets from fitconnect-secrets (ro) /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-6bfnk (ro) Containers: hie-test-34-fitconnect-ftc: Container ID: containerd://7438b9597296e0b01032820f7f82694dbe62deb05ce386ba412fe245a5858d3f Image: fitfileregistry.azurecr.io/fitconnect-service:1.0.695 Image ID: fitfileregistry.azurecr.io/fitconnect-service@sha256:1d7e38f7c216ba904d1658445c3bcb05101a7fda5df1f3a56e497159e71da343 Port: 4000/TCP (http) Host Port: 0/TCP (http) Command: node --require./instrumentation.js server.js State: Running Started: Thu, 12 Feb 2026 13:25:14 +0000 Ready: True Restart Count: 0 Requests: cpu: 100m Liveness: http-get http://:4000/fitconnect/readyz%3FhealthServiceName=TenantDocumentHealthService&healthServiceName=SpiceDbSchemaConnectionHealthService&healthServiceName=MongoDBConnectionHealthService&healthServiceName=PostgresDBConnectionHealthService&healthServiceName=MinioS3ConnectionHealthService&healthServiceName=WorkflowsAPIConnectionHealthService&healthServiceName=Auth0PingHealthService delay=15s timeout=12s period=15s success=1 failure=3 Readiness: http-get http://:4000/fitconnect/readyz%3FhealthServiceName=TenantDocumentHealthService&healthServiceName=SpiceDbSchemaConnectionHealthService&healthServiceName=MongoDBConnectionHealthService&healthServiceName=PostgresDBConnectionHealthService&healthServiceName=MinioS3ConnectionHealthService&healthServiceName=WorkflowsAPIConnectionHealthService&healthServiceName=Auth0PingHealthService delay=15s timeout=12s period=15s success=1 failure=3 Environment: NODE\_ENV: production FITFILE\_ENV: production LOAD\_DEFINITION\_PATH: /config/load\_definition.json Mounts: /config from config (ro) /secrets from fitconnect-secrets (ro) /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-6bfnk (ro) Conditions: Type Status PodReadyToStartContainers True Initialized True Ready True ContainersReady True PodScheduled True Volumes: fitconnect-secrets: Type: Secret (a volume populated by a Secret) SecretName: fitconnect Optional: false config: Type: Projected (a volume that contains injected data from multiple sources) ConfigMapName: hie-test-34-fitconnect-ftc-config-3ad7d286319b68f329e68a5b45f8d Optional: false ConfigMapName: fitconnect-load-definition Optional: false kube-api-access-6bfnk: Type: Projected (a volume that contains injected data from multiple sources) TokenExpirationSeconds: 3607 ConfigMapName: kube-root-ca.crt Optional: false DownwardAPI: true QoS Class: Burstable Node-Selectors: <none> Tolerations: node.kubernetes.io/not-ready:NoExecute op=Exists for 300s node.kubernetes.io/unreachable:NoExecute op=Exists for 300s Events: Type Reason Age From Message ---- ------ ---- ---- ------- Normal Scheduled 24m default-scheduler Successfully assigned hie-test-34/hie-test-34-fitconnect-ftc-fffdf4c6c-dgfp9 to ip-10-66-5-187.eu-west-2.compute.internal Normal Pulled 24m kubelet Container image "fitfileregistry.azurecr.io/fitconnect-service:1.0.695" already present on machine Normal Created 24m kubelet Created container: hie-test-34-fitconnect-ftc-init Normal Started 24m kubelet Started container hie-test-34-fitconnect-ftc-init Normal Pulled 24m kubelet Container image "fitfileregistry.azurecr.io/fitconnect-service:1.0.695" already present on machine Normal Created 24m kubelet Created container: hie-test-34-fitconnect-ftc Normal Started 24m kubelet Started container hie-test-34-fitconnect-ftc

---

This is the key twist: Kubernetes is now fine. Your Deployment has `1 available | 0 unavailable`, pod is Ready=True, init container completed, no restarts, no failing events.

So the "exceeded its progress deadline" message you saw in Argo is stale (from the _previous_ ReplicaSet rollout), and ArgoCD is currently refusing to auto-sync because of that earlier failed operation:

- You already saw in the controller logs: `Skipping auto-sync: failed previous sync attempt …`
- Argo still has `.status.operationState.phase=Failed` for the _Application_, even though the live state is healthy.

### What to Do now (cleanly)

#### 1) Confirm the Live Rollout is Healthy (you Already Basically did)

#### 2) Check Argo's view of Health (it May Still Be "Progressing/Degraded" until refresh)

#### 3) Force Argo to Recompute Health and Clear the Stale "Failed operation"

Pick one:

Option A (best): terminate the stuck/failed operation

This clears the stored operationState so Argo stops treating the last sync as the "current" failed op.

Option B: hard refresh + then sync

Then manually sync (CLI/UI) if it doesn't reconcile automatically.

---

## Why Your Egrep -v 'sync=Synced health=Healthy' Shows Blank Health

You're grepping out only `health=Healthy`, but Argo is returning empty health for those objects:

That typically happens when:

- Argo hasn't computed health for those resources yet (cached/stale status),
- or you're on an Argo version / configuration where some kinds don't get health by default (ConfigMap/Service commonly show empty health),
- but Deployment should normally show Healthy/Progressing, so the blank strongly suggests Argo's resource health cache/status isn't updated.

A hard refresh (or clearing operationState) usually fixes that immediately.

---

## One More Thing to Check: Did You Look at the Right App?

Earlier you had:

- parent app: `ff-hie-test-34` showing child `hie-test-34-fitconnect` "hookPhase=Failed"
- and child app `hie-test-34-fitconnect` operationState "Failed"

Now K8s is healthy, so after the refresh/clear, both should go green.

Verify parent app health after refresh too:

---

## If You want the Exact Proof it Was a Previous Rollout Deadline

Pull Deployment "ReplicaSet history" and check when the ProgressDeadline was triggered:

---

If you run Option A (patch operationState to null) and then re-check `.status.operationState.phase`, I expect it will disappear or flip to Succeeded on the next reconcile, and autosync will resume.

---

kubectl get application -n argocd ff-hie-test-34 -o yaml | sed -n '/operationState:/,/^status:/p' operationState: finishedAt: "2026-02-12T12:18:57Z" message: one or more synchronization tasks completed unsuccessfully (retried 5 times). operation: initiatedBy: automated: true retry: limit: 5 sync: prune: true revision: d4ee068bd666f1213627d4f27791b86f870842e9 phase: Failed retryCount: 5 startedAt: "2026-02-12T11:37:05Z" syncResult: resources: - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/prometheus-operator-crds unchanged name: prometheus-operator-crds namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/cert-manager unchanged name: cert-manager namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/grafana-k8s-monitoring unchanged name: grafana-k8s-monitoring namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/hie-test-34-postgresql unchanged name: hie-test-34-postgresql namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/argo-workflows unchanged name: argo-workflows namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/hie-test-34-minio unchanged name: hie-test-34-minio namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/hie-test-34-mongodb-b17ef unchanged name: hie-test-34-mongodb-b17ef namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/spicedb unchanged name: spicedb namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/hie-test-34-workflow-templates unchanged name: hie-test-34-workflow-templates namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/hie-test-34-workflows-api unchanged name: hie-test-34-workflows-api namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Failed kind: Application message: 'Failed sync attempt to d4ee068bd666f1213627d4f27791b86f870842e9: one or more synchronization tasks completed unsuccessfully (retried 5 times).' name: hie-test-34-fitconnect namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 - group: argoproj.io hookPhase: Succeeded kind: Application message: application.argoproj.io/hie-test-34-ffcloud-service unchanged name: hie-test-34-ffcloud-service namespace: argocd status: Synced syncPhase: Sync version: v1alpha1 revision: d4ee068bd666f1213627d4f27791b86f870842e9 source: helm: releaseName: hie-test-34 valueFiles: - /ffnodes/eoe/hie-test-34/values.yaml path: charts/ffnode repoURL: <https://gitlab.com/fitfile/deployment.git> targetRevision: eoe-test-release reconciledAt: "2026-02-12T14:07:50Z" resourceHealthSource: appTree resources: - group: argoproj.io kind: Application name: argo-workflows namespace: argocd status: Synced syncWave: -2 version: v1alpha1 - group: argoproj.io kind: Application name: cert-manager namespace: argocd status: Synced syncWave: -5 version: v1alpha1 - group: argoproj.io kind: Application name: certificates namespace: argocd status: OutOfSync syncWave: 5 version: v1alpha1 - group: argoproj.io kind: Application name: grafana-k8s-monitoring namespace: argocd status: Synced syncWave: -4 version: v1alpha1 - group: argoproj.io kind: Application name: hie-test-34-ffcloud-service namespace: argocd status: Synced syncWave: 3 version: v1alpha1 - group: argoproj.io kind: Application name: hie-test-34-fitconnect namespace: argocd status: Synced syncWave: 3 version: v1alpha1 - group: argoproj.io kind: Application name: hie-test-34-frontend namespace: argocd status: OutOfSync syncWave: 4 version: v1alpha1 - group: argoproj.io kind: Application name: hie-test-34-minio namespace: argocd status: Synced version: v1alpha1 - group: argoproj.io kind: Application name: hie-test-34-mongodb-b17ef namespace: argocd status: Synced version: v1alpha1 - group: argoproj.io kind: Application name: hie-test-34-postgresql namespace: argocd status: Synced syncWave: -3 version: v1alpha1 - group: argoproj.io kind: Application name: hie-test-34-workflow-templates namespace: argocd status: Synced syncWave: 1 version: v1alpha1 - group: argoproj.io kind: Application name: hie-test-34-workflows-api namespace: argocd status: Synced syncWave: 2 version: v1alpha1 - group: argoproj.io kind: Application name: prometheus-operator-crds namespace: argocd status: Synced syncWave: -5 version: v1alpha1 - group: argoproj.io kind: Application name: spicedb namespace: argocd status: Synced syncWave: 1 version: v1alpha1 sourceHydrator: {} sourceType: Helm summary: {} sync: comparedTo: destination: namespace: argocd server: <https://kubernetes.default.svc> ignoreDifferences: - group: apps jsonPointers: - /spec/replicas kind: Deployment source: helm: releaseName: hie-test-34 valueFiles: - /ffnodes/eoe/hie-test-34/values.yaml path: charts/ffnode repoURL: <https://gitlab.com/fitfile/deployment.git> targetRevision: eoe-test-release revision: d4ee068bd666f1213627d4f27791b86f870842e9 status: OutOfSync

---

Nice—that YAML tells us exactly what's happening.

### What it means

- The parent app `ff-hie-test-34` has a recorded sync operation that ran from 11:37Z to 12:18Z and ended `phase: Failed` because the child app `hie-test-34-fitconnect` had `hookPhase: Failed` during that operation.
- Since then, Argo has continued to reconcile (`reconciledAt: 14:07:50Z`), but it has not started a new sync operation, because the previous automated one hit retryCount 5 / limit 5.
- Also, the parent app is still OutOfSync right now because at least these children are OutOfSync:
	- `certificates` (OutOfSync)
	- `hie-test-34-frontend` (OutOfSync)

So even if fitconnect is now healthy in the cluster, the parent won't "become succeeded" until a NEW sync operation runs and completes, and it won't auto-retry because it already exhausted retries.

---

## Fix: Start a New Sync Operation

### Option A (cleanest): Use ArgoCD CLI

You can also sync just the OutOfSync children first:

### Option B: Trigger Sync via Kubectl (no Argocd CLI)

ArgoCD Applications support an `.operation.sync` request. This will kick off a brand new sync:

If you want to re-sync fitconnect specifically:

(If your ArgoCD version requires it, add a revision, but usually it'll use the app's targetRevision.)

---

## After Triggering, Watch the New Operation Replace the Old Failure

If `certificates` / `frontend` remain OutOfSync, the parent will remain OutOfSync too—so those are worth checking next.

---

## Quick Sanity Checks for the Two OutOfSync Children

If you paste the output of those two (just the jsonpath lines above), I can tell you whether you're dealing with a harmless diff (e.g., auto-generated fields) or a real rollout/health issue.

---

kubectl get applications -n argocd NAME SYNC STATUS HEALTH STATUS argo-workflows Synced Healthy cert-manager Synced Healthy certificates OutOfSync Degraded ff-hie-test-34 Synced Degraded grafana-k8s-monitoring Synced Healthy hie-test-34-ffcloud-service Synced Healthy hie-test-34-fitconnect Synced Healthy hie-test-34-frontend Synced Healthy hie-test-34-minio Synced Healthy hie-test-34-mongodb-b17ef Synced Healthy hie-test-34-postgresql Synced Healthy hie-test-34-workflow-templates Synced Healthy hie-test-34-workflows-api Synced Healthy prometheus-operator-crds Synced Healthy spicedb Synced Healthy awsadmin@ip-10-66-2-4:~/terraform$ kubectl -n argocd get app certificates -o jsonpath='{.status.sync.status}{"\\n"}{.status.health.status}{"\\n"}{.status.operationState.message}{"\\n"}' kubectl -n argocd get app hie-test-34-frontend -o jsonpath='{.status.sync.status}{"\\n"}{.status.health.status}{"\\n"}{.status.operationState.message}{"\\n"}' OutOfSync Degraded one or more objects failed to apply, reason: namespaces "ohdsi" not found due to application controller sync timeout. Retrying attempt 5 at 2:17PM. Synced Healthy successfully synced (all tasks run)

---

Cool, this narrows it down to one thing:

- Everything is fine except `certificates`
- Parent `ff-hie-test-34` is Synced but Degraded because a child app is degraded.
- `certificates` is:
	- OutOfSync
	- Degraded
	- failing with: `namespaces "ohdsi" not found` and then timing out / retrying.

So ArgoCD is trying to apply at least one resource in the `ohdsi` namespace, but that namespace doesn't exist (or isn't allowed / isn't being created soon enough).

---

## The Likely Root Cause

One of these is true:

1. `certificates` contains resources with `metadata.namespace: ohdsi` but does not create the Namespace object.
2. It _does_ create the Namespace, but ArgoCD is trying to apply namespaced objects before the namespace exists (ordering / sync-wave / hook ordering).
3. Namespace creation is blocked by AppProject destinations or cluster RBAC (less likely here since other apps can create namespaces, but possible).

---

## Fastest way to Confirm what Argo is Trying to Apply

Run:

You'll see the exact resource(s) failing, and whether a `Namespace ohdsi` is even part of the app.

---

## Quick Fix Options

### Option A: Create the Namespace (unblocks immediately)

If it's genuinely expected to exist:

Then re-sync `certificates`:

### Option B: Make Argo Create it in the Certificates App (proper GitOps fix)

Add a `Namespace` manifest to the `certificates` app (same repo/path as the rest of its manifests):

Then ensure it applies _before_ the cert resources (see Option C).

### Option C: Enforce Ordering (when Namespace is in Git but Applied Too late)

If the namespace manifest already exists but ordering is wrong, add a sync-wave annotation so it applies first:

Put `-10` on the Namespace, and `0` (or default) on the cert resources.

### Option D: if the Namespace is Created by Another App

Then you need deterministic ordering between apps:

- Put the app that creates the namespace in an earlier syncWave than `certificates`, or
- Move the namespace creation into `certificates` so it's self-contained.

---

## Why the "application Controller Sync timeout" part Shows up

Argo retries apply, but since the namespace never appears, it eventually hits its per-sync timeout and reports the retry attempt (you're already at attempt 5 in the message).

---

If you paste the output of either:

- `kubectl -n argocd get app certificates -o yaml | sed -n '/operationState:/,/^  sync:/p'`
	or
- the `syncResult.resources[*]` jsonpath list

…I can tell you exactly which object(s) are trying to go into `ohdsi`, and whether the fix is "missing Namespace", "wrong ordering", or "wrong destination/permissions".
