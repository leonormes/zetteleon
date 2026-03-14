---
captured: "2026-03-07T16:50:10+00:00 2026-03-07T16:50:10+00:00"
created: 2026-03-07T16:50:12+00:00
modified: 2026-03-14T11:10:29+00:00
source: "https://gemini.google.com/app/4dc953c7aaccc2f1"
status: "processing"
tags: ["input"]
title: HEAD You said why is the parent app saying degraded  ku...
type: "head"
---

## Raw Output / Content

why is the parent app saying degraded

kubectl get applications -n argocd

NAME SYNC STATUS HEALTH STATUS

argo-workflows Unknown Healthy

cert-manager Synced Healthy

certificates Synced Healthy

ff-hie-prod-34 Synced Degraded

grafana-k8s-monitoring Synced Healthy

hie-prod-34-ffcloud-service Synced Healthy

hie-prod-34-fitconnect Synced Healthy

hie-prod-34-frontend Synced Healthy

hie-prod-34-minio Synced Healthy

hie-prod-34-mongodb-b17ef Unknown Healthy

hie-prod-34-postgresql Synced Healthy

hie-prod-34-workflow-templates Synced Healthy

hie-prod-34-workflows-api Synced Healthy

hutch Synced Healthy

hutch-prod Synced Healthy

ohdsi Synced Healthy

prometheus-operator-crds Synced Healthy

spicedb Synced Healthy

thehyve Synced Healthy

ip-10-65-2-8% kubectl describe application ff-hie-prod-34 -n argocd

Name: ff-hie-prod-34

Namespace: argocd

Labels: app.kubernetes.io/managed-by=Helm

Annotations: meta.helm.sh/release-name: fitfile-project

meta.helm.sh/release-namespace: argocd

API Version: argoproj.io/v1alpha1

Kind: Application

Metadata:

Creation Timestamp: 2025-05-07T14:53:36Z

Finalizers:

resources-finalizer.argocd.argoproj.io

Generation: 111263

Resource Version: 247031910

UID: 9b3da4ea-c4dd-4a86-9864-01d3ec140454

Spec:

Destination:

Namespace: argocd

Server: <https://kubernetes.default.svc>

Ignore Differences:

Group: apps

Json Pointers:

/spec/replicas

Kind: Deployment

Info:

Name: url

Value: <https://argoproj.github.io/>

Project: fitfile

Source:

Helm:

Release Name: hie-prod-34

Value Files:

/ffnodes/eoe/hie-prod-34/values.yaml

Path: charts/ffnode

Repo URL: <https://gitlab.com/fitfile/deployment.git>

Target Revision: eoe-latest-release

Sync Policy:

Automated:

Prune: true

Self Heal: true

Status:

Controller Namespace: argocd

Health:

Last Transition Time: 2026-02-18T15:10:18Z

Status: Degraded

History:

Deploy Started At: 2025-12-19T16:14:58Z

Deployed At: 2025-12-19T16:15:26Z

Id: 49

Initiated By:

Automated: true

Revision: 691fc36b11ee0d90e811170bfd1d71a8e344a933

Source:

Helm:

Release Name: hie-prod-34

Value Files:

/ffnodes/eoe/hie-prod-34/values.yaml

Path: charts/ffnode

Repo URL: <https://gitlab.com/fitfile/deployment.git>

Target Revision: eoe-latest-release

Deploy Started At: 2025-12-20T19:07:05Z

Deployed At: 2025-12-20T19:08:10Z

Id: 50

Initiated By:

Automated: true

Revision: 9274d69da35c2446d2048cd5414307e0cf7e65ec

Source:

Helm:

Release Name: hie-prod-34

Value Files:

/ffnodes/eoe/hie-prod-34/values.yaml

Path: charts/ffnode

Repo URL: <https://gitlab.com/fitfile/deployment.git>

Target Revision: eoe-latest-release

Deploy Started At: 2025-12-22T14:41:16Z

Deployed At: 2025-12-22T14:41:41Z

Id: 51

Initiated By:

Automated: true

Revision: da0ed0a37b016257b7765a78d8cf0c93a00605e2

Source:

Helm:

Release Name: hie-prod-34

Value Files:

/ffnodes/eoe/hie-prod-34/values.yaml

Path: charts/ffnode

Repo URL: <https://gitlab.com/fitfile/deployment.git>

Target Revision: eoe-latest-release

Deploy Started At: 2025-12-23T14:46:32Z

Deployed At: 2025-12-23T14:47:00Z

Id: 52

Initiated By:

Automated: true

Revision: 95453f1373c66be0a60e6c9ea1c8d7218f02a87c

Source:

Helm:

Release Name: hie-prod-34

Value Files:

/ffnodes/eoe/hie-prod-34/values.yaml

Path: charts/ffnode

Repo URL: <https://gitlab.com/fitfile/deployment.git>

Target Revision: eoe-latest-release

Deploy Started At: 2025-12-30T18:55:25Z

Deployed At: 2025-12-30T18:56:35Z

Id: 53

Initiated By:

Automated: true

Revision: 55f395c5b22e02febd2cda909c1f484a7cc8a44e

Source:

Helm:

Release Name: hie-prod-34

Value Files:

/ffnodes/eoe/hie-prod-34/values.yaml

Path: charts/ffnode

Repo URL: <https://gitlab.com/fitfile/deployment.git>

Target Revision: eoe-latest-release

Deploy Started At: 2026-01-22T11:17:26Z

Deployed At: 2026-01-22T11:18:54Z

Id: 54

Initiated By:

Automated: true

Revision: 262d08860788f9b5236876f73f1eedd0ba75780e

Source:

Helm:

Release Name: hie-prod-34

Value Files:

/ffnodes/eoe/hie-prod-34/values.yaml

Path: charts/ffnode

Repo URL: <https://gitlab.com/fitfile/deployment.git>

Target Revision: eoe-latest-release

Deploy Started At: 2026-01-26T10:44:18Z

Deployed At: 2026-01-26T10:45:10Z

Id: 55

Initiated By:

Automated: true

Revision: 7fcc3a77c57e698580c168e0aaabf45988ecdb12

Source:

Helm:

Release Name: hie-prod-34

Value Files:

/ffnodes/eoe/hie-prod-34/values.yaml

Path: charts/ffnode

Repo URL: <https://gitlab.com/fitfile/deployment.git>

Target Revision: eoe-latest-release

Deploy Started At: 2026-01-26T10:47:07Z

Deployed At: 2026-01-26T10:48:15Z

Id: 56

Initiated By:

Username: admin

Revision: 7fcc3a77c57e698580c168e0aaabf45988ecdb12

Source:

Helm:

Release Name: hie-prod-34

Value Files:

/ffnodes/eoe/hie-prod-34/values.yaml

Path: charts/ffnode

Repo URL: <https://gitlab.com/fitfile/deployment.git>

Target Revision: eoe-latest-release

Deploy Started At: 2026-02-04T12:09:56Z

Deployed At: 2026-02-04T12:10:23Z

Id: 57

Initiated By:

Automated: true

Revision: 8d035df2f18b8ee313e4bd60023bf7af1dbeef65

Source:

Helm:

Release Name: hie-prod-34

Value Files:

/ffnodes/eoe/hie-prod-34/values.yaml

Path: charts/ffnode

Repo URL: <https://gitlab.com/fitfile/deployment.git>

Target Revision: eoe-latest-release

Deploy Started At: 2026-02-05T16:33:32Z

Deployed At: 2026-02-05T16:33:56Z

Id: 58

Initiated By:

Automated: true

Revision: 872708deb2e0a7c709e4721421263e9bf8a3d503

Source:

Helm:

Release Name: hie-prod-34

Value Files:

/ffnodes/eoe/hie-prod-34/values.yaml

Path: charts/ffnode

Repo URL: <https://gitlab.com/fitfile/deployment.git>

Target Revision: eoe-latest-release

Operation State:

Finished At: 2026-02-05T16:33:57Z

Message: successfully synced (all tasks run)

Operation:

Initiated By:

Automated: true

Retry:

Limit: 5

Sync:

Auto Heal Attempts Count: 1

Prune: true

Resources:

Group: argoproj.io

Kind: Application

Name: certificates

Revision: 872708deb2e0a7c709e4721421263e9bf8a3d503

Phase: Succeeded

Started At: 2026-02-05T16:33:56Z

Sync Result:

Resources:

Group: argoproj.io

Hook Phase: Running

Kind: Application

Message: application.argoproj.io/certificates configured

Name: certificates

Namespace: argocd

Status: Synced

Sync Phase: Sync

Version: v1alpha1

Revision: 872708deb2e0a7c709e4721421263e9bf8a3d503

Source:

Helm:

Release Name: hie-prod-34

Value Files:

/ffnodes/eoe/hie-prod-34/values.yaml

Path: charts/ffnode

Repo URL: <https://gitlab.com/fitfile/deployment.git>

Target Revision: eoe-latest-release

Reconciled At: 2026-02-18T15:28:26Z

Resource Health Source: appTree

Resources:

Group: argoproj.io

Kind: Application

Name: argo-workflows

Namespace: argocd

Status: Synced

Sync Wave: -2

Version: v1alpha1

Group: argoproj.io

Kind: Application

Name: cert-manager

Namespace: argocd

Status: Synced

Sync Wave: -5

Version: v1alpha1

Group: argoproj.io

Kind: Application

Name: certificates

Namespace: argocd

Status: Synced

Sync Wave: 5

Version: v1alpha1

Group: argoproj.io

Kind: Application

Name: grafana-k8s-monitoring

Namespace: argocd

Status: Synced

Sync Wave: -4

Version: v1alpha1

Group: argoproj.io

Kind: Application

Name: hie-prod-34-ffcloud-service

Namespace: argocd

Status: Synced

Sync Wave: 3

Version: v1alpha1

Group: argoproj.io

Kind: Application

Name: hie-prod-34-fitconnect

Namespace: argocd

Status: Synced

Sync Wave: 3

Version: v1alpha1

Group: argoproj.io

Kind: Application

Name: hie-prod-34-frontend

Namespace: argocd

Status: Synced

Sync Wave: 4

Version: v1alpha1

Group: argoproj.io

Kind: Application

Name: hie-prod-34-minio

Namespace: argocd

Status: Synced

Version: v1alpha1

Group: argoproj.io

Kind: Application

Name: hie-prod-34-mongodb-b17ef

Namespace: argocd

Status: Synced

Version: v1alpha1

Group: argoproj.io

Kind: Application

Name: hie-prod-34-postgresql

Namespace: argocd

Status: Synced

Sync Wave: -3

Version: v1alpha1

Group: argoproj.io

Kind: Application

Name: hie-prod-34-workflow-templates

Namespace: argocd

Status: Synced

Sync Wave: 1

Version: v1alpha1

Group: argoproj.io

Kind: Application

Name: hie-prod-34-workflows-api

Namespace: argocd

Status: Synced

Sync Wave: 2

Version: v1alpha1

Group: argoproj.io

Kind: Application

Name: prometheus-operator-crds

Namespace: argocd

Status: Synced

Sync Wave: -5

Version: v1alpha1

Group: argoproj.io

Kind: Application

Name: spicedb

Namespace: argocd

Status: Synced

Sync Wave: 1

Version: v1alpha1

Source Hydrator:

Source Type: Helm

Summary:

Sync:

Compared To:

Destination:

Namespace: argocd

Server: <https://kubernetes.default.svc>

Ignore Differences:

Group: apps

Json Pointers:

/spec/replicas

Kind: Deployment

Source:

Helm:

Release Name: hie-prod-34

Value Files:

/ffnodes/eoe/hie-prod-34/values.yaml

Path: charts/ffnode

Repo URL: <https://gitlab.com/fitfile/deployment.git>

Target Revision: eoe-latest-release

Revision: 872708deb2e0a7c709e4721421263e9bf8a3d503

Status: Synced

Events:

Type Reason Age From Message

\---- ------ ---- ---- -------

Normal ResourceUpdated 18m argocd-application-controller Updated health status: Healthy -> Degraded

ip-10-65-2-8% kubectl get applications -n argocd

NAME SYNC STATUS HEALTH STATUS

argo-workflows Unknown Healthy

cert-manager Synced Healthy

certificates Synced Healthy

ff-hie-prod-34 Synced Degraded

grafana-k8s-monitoring Synced Healthy

hie-prod-34-ffcloud-service Synced Healthy

hie-prod-34-fitconnect Synced Healthy

hie-prod-34-frontend Synced Healthy

hie-prod-34-minio Synced Healthy

hie-prod-34-mongodb-b17ef Unknown Healthy

hie-prod-34-postgresql Synced Healthy

hie-prod-34-workflow-templates Synced Healthy

hie-prod-34-workflows-api Synced Healthy

hutch Synced Healthy

hutch-prod Synced Healthy

ohdsi Synced Healthy

prometheus-operator-crds Synced Healthy

spicedb Synced Healthy

thehyve Synced Healthy

---

Based on the output provided, your parent application `ff-hie-prod-34` is Degraded because of the status of its child applications, specifically the ones showing a `SYNC STATUS` of `Unknown`.

Here is the breakdown of why this is happening and how to fix it.

### 1\. The Root Cause: "Unknown" Child Apps

In an "App of Apps" pattern, the parent application's health is an aggregation of its children. Looking at your `kubectl get applications` list, two applications are in an unstable state:

| Application Name | Sync Status | Health Status |
| --- | --- | --- |
| argo-workflows | Unknown | Healthy |
| hie-prod-34-mongodb-b17ef | Unknown | Healthy |

Even though they show as "Healthy", the `Unknown` sync status indicates that the Argo CD controller has failed to generate the manifests for these apps (often due to a repository connection error, a timeout, or a Helm template error).

Because the parent application uses `Resource Health Source: appTree` (seen in your describe output), it detects that it cannot reliably verify the state of these children. Consequently, it marks the entire parent tree as Degraded to alert you that the state is not fully consistent.

### 2\. Contradiction in Output

You might notice a confusing detail in your `kubectl describe` output for the parent:

The parent's `Resources` list shows the _last known good state_ or the desired state it tried to apply. However, the `kubectl get` command reflects the _live_ state of the cluster, which confirms the children have drifted into an `Unknown` state. The parent detects this discrepancy in the live cluster and degrades itself.

### 3\. Immediate Next Steps

You need to investigate why `argo-workflows` and the MongoDB app are failing to sync.

Please run the following commands to find the specific error message (look for `Conditions` or `Events` at the bottom of the output):

and

Common fixes for "Unknown" status:

- Repo Connection: Check if the Git repository URL is correct and accessible from the Argo CD repo server.
- Helm Values: If these are Helm charts, check if a recent change to `values.yaml` introduced a syntax error.
- Timeout: If the chart is very large, you might need to increase the `timeout.reconciliation` setting in your Argo CD config map.

---

both had the same Status:

Conditions:

Last Transition Time: 2026-02-18T15:10:37Z

Message: Failed to load target state: failed to generate manifest for source 1 of 1: rpc error: code = Unknown desc = unable to get tags: failed to get tags: GET "https://fitfileregistry.azurecr.io/v2/helm/mongodb/tags/list": GET "<https://fitfileregistry.azurecr.io/oauth2/token?scope=repository%3Ahelm%2Fmongodb%3Ametadata>\_read%2Cpull&service=fitfileregistry.azurecr.io": response status code 401: unauthorized: Invalid clientid or client secret.

Type: ComparisonError

Controller Namespace: argocd

---

The error message `response status code 401: unauthorized: Invalid clientid or client secret` is the definitive "smoking gun".

The parent application is Degraded because its child applications (specifically the MongoDB and Argo Workflows ones) cannot download their Helm charts from your Azure Container Registry (`fitfileregistry.azurecr.io`).

Here is exactly what is happening and how to fix it.

### 1\. The Root Cause

Argo CD is trying to connect to your private registry to fetch the charts, but the credentials it is using are being rejected by Azure.

This usually happens for one of two reasons:

- Expired Service Principal: The Service Principal (Client ID) used to access the Azure Container Registry (ACR) has a "Client Secret" (password) that has expired. This is very common with Azure credentials which often have a 1 or 2-year lifespan.
- Rotated Keys: Someone may have regenerated the access keys for the registry, invalidating the old ones stored in Argo CD.

### 2\. How to Fix It

You need to update the credentials in Argo CD for the repository `fitfileregistry.azurecr.io`.

#### Step 1: Generate a New Secret in Azure

1. Log in to the Azure Portal.
2. Navigate to Microsoft Entra ID (formerly Azure AD) -> App registrations.
3. Find the Service Principal (Client ID) associated with your Argo CD or ACR access.
4. Go to Certificates & secrets -> Client secrets.
5. Create a New client secret.
6. Copy the "Value" immediately (you won't be able to see it again).

#### Step 2: Update Argo CD

You likely configured this repository imperatively (via CLI/UI) or declaratively (via a Kubernetes Secret).

Option A: Updating via Kubernetes Secret (Most common for GitOps) Find the secret that holds your repository credentials:

Look for a secret that corresponds to your Azure registry (e.g., `repo-fitfileregistry` or similar). Edit it:

You will need to base64 encode your new Client Secret before pasting it into the `data` section.

Replace the value for the `password` (or `clientSecret`) field in the secret manifest.

Option B: Updating via Argo CD CLI If you have the CLI installed and logged in:

_(Note: Ensure you include `--enable-oci` if you are using OCI-based Helm charts, which is standard for ACR)._

### 3\. Verify the Fix

Once the credentials are updated, Argo CD will not automatically retry instantly. You should force a refresh:

Watch the application status:

Once the child app successfully connects and generates its manifest, its status will change from `Unknown` to `Synced`, and the parent app `ff-hie-prod-34` will return to `Healthy`.

---

kubectl get secrets -n argocd -l argocd.argoproj.io/secret-type=repository

NAME TYPE DATA AGE

argocd-acr-pull-secret Opaque 8 113d

argocd-repo-fitfile-deployment-repo Opaque 6 242d

---

Based on the list, the secret you need to edit is `argocd-acr-pull-secret`.

The other secret (`argocd-repo-fitfile-deployment-repo`) corresponds to your GitLab deployment repository, which we know is working because the parent app is syncing successfully. The issue is specific to the Azure Container Registry (ACR) where the Helm charts live.

Here is the step-by-step procedure to fix the `401 Unauthorized` error.

### 1\. Confirm the Target

Before making changes, verify that `argocd-acr-pull-secret` actually points to `fitfileregistry.azurecr.io`.

Run this command to decode and view the secret's URL:

- If it outputs:`https://fitfileregistry.azurecr.io` (or similar), you have the right secret.
- If it outputs: a different URL, stop and let me know.

### 2\. Prepare the New Credentials

I assume you have generated a new Client Secret (password) for your Service Principal in the Azure Portal as discussed.

You must Base64 encode this new password before adding it to Kubernetes.

_Copy the output string._

### 3\. Update the Secret

Edit the secret in your cluster:

1. Locate the `data:` section.
2. Find the field named `password` (it might occasionally be named `clientSecret`, but `password` is standard for Argo repo secrets).
3. Replace the old hash with the new Base64 string you just generated.
4. Save and exit (type `:wq` if using vim).

### 4\. Force a Refresh

Argo CD caches authentication failures to prevent hammering the API. To make it retry immediately, you usually need to restart the Repo Server or hard refresh the app.

Option A: Restart Repo Server (Fastest/Surest way) This clears all connection caches.

Option B: Hard Refresh the App

Once done, check the application status again. The `Unknown` state should flip to `Synced`, and the parent app will become `Healthy`.
