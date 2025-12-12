---
aliases: []
confidence: 
created: 2025-10-15T09:43:26Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:15Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [playbook]
title: Investigating and Resolving Argo CD `OutOfSync` Applications
type:
uid: 
updated: 
version:
---

---

## **1. Purpose**

This playbook provides a step-by-step guide to diagnose and resolve an Argo CD application that is reported as `OutOfSync` on the Grafana monitoring dashboard.

The process begins with triage in Grafana, moves to log analysis to find the root cause, and finishes with resolution steps performed from a `kubectl`/`argocd` CLI environment. This guide assumes no initial knowledge of the failing application.

## **2. Triage and Identification**

### **2.1. Initial Observation**

The process starts when the **Argo CD Applications** dashboard in Grafana shows one or more applications with an `OutOfSync` status.

### **2.2. Identify the Failing Application**

To find the exact name of the out-of-sync application, we use a Prometheus query.

1. Navigate to the **Explore** view in Grafana.
2. Select your **Prometheus** datasource.
3. Execute the following query:

```sh
argocd_app_info{sync_status="OutOfSync"}
```

4. Examine the labels of the resulting time series. The **`name`** label identifies the application.
   - **Example:** In this case, we identified the application name as `ff-hie-prod-34`.

## **3. Log Analysis and Root Cause Diagnosis**

### **3.1. Find the Relevant Logs**

Now, use the application name to find relevant logs from the Argo CD Application Controller using your **Loki** datasource.

1. In the **Explore** view, switch to the **Loki** datasource.
2. Use a LogQL query to filter logs for the specific application.
   - **Generic Query:**

```sh
{namespace="argocd", pod=~"argocd-application-controller-.*"} |= "<app-name>"
```

- **Example:**

```sh
{namespace="argocd", pod=~"argocd-application-controller-.*"} |= "ff-hie-prod-34"
```

### **3.2. Analyse the Logs**

You are looking for the original error that caused the sync to fail. You may need to expand your time window to find it.

- **Symptom:** You will likely find many recent warnings indicating that auto-sync is being skipped due to a previous failure.

  > `Skipping auto-sync: failed previous sync attempt to <commit-hash>`

- **Root Cause:** Look further back in the logs for the actual error that occurred during a sync operation. Common errors are related to connectivity or manifest issues.
  - **Example 1: Internal Connectivity Failure (Redis)**

        > `"message": "...failed to list refs: dial tcp 172.20.26.106:6379: connect: connection refused"`

  - **Example 2: External Connectivity Failure (Git)**

        > `"message": "...failed to list refs: Get \\\"https://gitlab.com/...\\\": context deadline exceeded"`

**Diagnosis:** Based on the logs, we determined the root cause was a failure of the Argo CD components to connect to Redis and GitLab, which prevented the controller from fetching manifests. This caused the initial sync to fail and lock the application in an error state.

## **4. Resolution**

Resolution requires CLI access to the Kubernetes cluster and the Argo CD service.

### **4.1. Pre-requisite: Fix the Underlying Cause**

Before proceeding, ensure the root cause identified in the logs has been addressed by the responsible platform team (e.g., Redis pod has been fixed, network policies have been corrected).

### **4.2. Log in to the Argo CD CLI**

1. Find the Argo CD Server Hostname:

   Use kubectl to find the Ingress resource that exposes the Argo CD server.

   ```sh
   kubectl get ingress -n argocd
   ```

   The hostname will be in the `HOSTS` column.

2. Get the Admin Password:
   You will need to go to the customers HCP Vault and find `unhashed_admin_password`
3. Log In:

   Use the hostname and password to log in.

   - **Generic Command:**

```sh
argocd login <argocd-server-hostname>
```

- **Note:** You may need the `--insecure` flag if the server uses a self-signed or untrusted TLS certificate.

### **4.3. Clear the Error State and Sync the Application**

Because the application is stuck in a `SyncError` state, you must trigger a manual sync to clear it.

1. **Initiate the Manual Sync:**
   - **Generic Command:**

````sh
argocd app sync <app-name>
        ```

- **Example:**


```sh
argocd app sync ff-hie-prod-34
````

2. Verify the Result:

   Check the status of the application. The sync may take a few moments.

   - **Generic Command:**

     ```sh
     argocd app get <app-name>
     ```

   - **Example:**

     ```sh
     argocd app get ff-hie-prod-34
     ```

Expected Outcome:

The output should show Sync Status: Synced and Health Status: Healthy. The OutOfSync alert on the Grafana dashboard will now be resolved.
