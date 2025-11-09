---
aliases: []
confidence: 
created: 2025-05-24T08:22:23Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:12Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Kubernetes Debugging Runbook
type:
uid: 
updated: 
version:
---

**Purpose:** This runbook provides a starting point for general debugging of applications deployed to a cloud provider managed Kubernetes cluster, particularly when using Helm and Argo CD.

**Audience:** Operations and development teams.

**Assumptions:**

- Applications are deployed using Helm charts.
- Argo CD is used as the GitOps operator to manage deployments from a Git repository.
- You have `kubectl` installed and configured to connect to the target cluster [5].
- You have `helm` installed locally.
- You have `argocd` CLI installed locally.

**Key Tools:**

- `kubectl`: The primary command-line tool for interacting with a Kubernetes cluster [5].
- `helm`: Used for inspecting Helm charts and releases [1, 6].
- `argocd`: Used for interacting with the Argo CD instance [7].
- Cloud Provider Console: For checking cluster status, node health, and related cloud resources [8].
- Kubernetes Dashboard (if available and secured): Provides a graphical overview of the cluster [8, 9].

---

## 1. Initial Triage and Overview

**Goal:** Get a high-level understanding of the cluster and application status.

**Steps:**

1. **Check Cluster Health:**
   - Use `kubectl cluster-info` to verify connectivity and see basic cluster information [10].
   - Check node status: `kubectl get nodes` [11]. Look for nodes that are NotReady or have issues.
   - Check control plane status (if applicable to your managed service): Use your cloud provider's console or specific `kubectl` commands if exposed [12]. Managed services typically handle control plane health [13, 14].

2. **Check Application Status via Argo CD:**
   - Access the Argo CD UI or use the `argocd` CLI.
   - List applications: `argocd app list`.
   - Check the sync status and health status of the affected application [15]. Argo CD monitors the Git repository for the desired state and compares it to the live cluster state [3].
   - If the application is OutOfSync or unhealthy, drill down into the specific application in Argo CD for details on why. Argo CD can show differences between the desired state in Git and the actual state in the cluster [16].

3. **Check Application Status via `kubectl`:**
   - List Pods in the relevant namespace: `kubectl get pods -n <namespace>` [17]. Look for Pods in `CrashLoopBackOff`, `Error`, `Pending`, or other non-`Running` states [17].
   - List Deployments: `kubectl get deployments -n <namespace>`. Check the desired vs. current vs. ready counts [18].
   - List ReplicaSets: `kubectl get rs -n <namespace>`. Check if the desired number of replicas are running [18, 19]. Deployments manage ReplicaSets [19].
   - Check Services and Endpoints: `kubectl get services -n <namespace>` and `kubectl get endpoints -n <namespace>` or `kubectl get endpointslice -n <namespace>`. Ensure Services have associated Endpoints pointing to healthy Pods [20, 21].
   - Check Ingress (if used): `kubectl get ingress -n <namespace>`. Verify rules and ensure they are pointing to the correct Services [20].

---

## 2. Deep Dive Debugging - Identifying the Root Cause

**Goal:** Pinpoint the specific resource or issue causing the problem.

**Steps:**

1. **Examine Pods:**
   - Get detailed information about problematic Pods: `kubectl describe pod <pod-name> -n <namespace>`. Look at the "Events" section at the bottom for clues about scheduling, pulling images, or starting containers [22].
   - View container logs: `kubectl logs <pod-name> -n <namespace>` [23]. Use `-c <container-name>` if there are multiple containers in the Pod [24]. Use `--tail=<number>` to see recent logs or `--follow` to stream logs [25, 26].
   - If a Pod is in `CrashLoopBackOff`, the logs are crucial. It means the container is starting, crashing, and restarting repeatedly [17].
   - If a Pod is `Pending`, check the `kubectl describe pod` output for scheduling issues, such as insufficient resources (CPU, memory), node affinity/anti-affinity rules, or taints/tolerations preventing scheduling [13, 27].
   - If a Pod is in an `Error` state, check the logs and events for details on the error.
   - If a container won't start due to an image issue (e.g., `ImagePullBackOff`), verify the image name and tag in the Deployment manifest and check if the image exists and is accessible in the container registry [28].
   - If you suspect networking issues within a Pod, you can use `kubectl exec -it <pod-name> -n <namespace> -- /bin/sh` (or `/bin/bash`) to get a shell inside the container (if a shell is available) and use tools like `ping`, `wget`, or `nslookup` to test connectivity [24, 29, 30].

2. **Examine Deployments and ReplicaSets:**
   - Get detailed information: `kubectl describe deployment <deployment-name> -n <namespace>`. This shows the associated ReplicaSets and their status [18].
   - Get detailed information for the associated ReplicaSet: `kubectl describe replicaset <replicaset-name> -n <namespace>`. This shows the Pod template and the status of the Pods it's managing [19].

3. **Examine Services:**
   - Get detailed information: `kubectl describe service <service-name> -n <namespace>`. Check the `Endpoints` section to see which Pods the Service is routing traffic to [20, 21]. If the list of Endpoints is empty or incorrect, it indicates a problem with the Pods or the Service's selector labels matching the Pods' labels [21].

4. **Examine Helm Release:**
   - Check the history of the Helm release: `helm history <release-name> -n <namespace>`. This shows past deployments and their status [31].
   - Get the deployed values: `helm get values <release-name> -n <namespace>`. This shows the configuration values used for the release [32].
   - Get the rendered manifests: `helm get manifest <release-name> -n <namespace>`. This shows the actual Kubernetes YAML that was applied to the cluster for this release [31]. Compare this to the expected YAML in your Git repository [16].

5. **Examine Argo CD Application:**
   - Use the Argo CD UI or `argocd app diff <application-name>` to see the difference between the desired state in Git and the live state in the cluster [3]. This can help identify if the deployed resources match what's in your Git repository.
   - Check the sync operation history in Argo CD for details on past deployments and any errors that occurred during the sync process.
   - If Argo CD is reporting an issue connecting to the cluster, use `argocd admin cluster kubeconfig <cluster-name>` (if configured) to troubleshoot connectivity [33, 34].

---

## 3. Common Issues and Potential Solutions

- **`CrashLoopBackOff`:**
  - **Cause:** Application within the container is crashing.
  - **Solution:** View container logs (`kubectl logs`) to identify application errors [17, 23]. Check application configuration passed via ConfigMaps or Secrets [35].
- **`ImagePullBackOff`:**
  - **Cause:** Kubernetes cannot pull the container image.
  - **Solution:** Verify the image name and tag in the Deployment manifest [28]. Check the container registry is accessible from the cluster and that credentials (if required) are correctly configured as ImagePullSecrets [35].
- **`Pending` Pods:**
  - **Cause:** Scheduler cannot find a suitable node.
  - **Solution:** Check `kubectl describe pod` for scheduling reasons (e.g., insufficient resources, taints, affinity rules) [13, 27]. Check node resource utilization (`kubectl top nodes` - requires Metrics Server) or in the cloud provider console [8].
- **Service has no Endpoints:**
  - **Cause:** The Service selector labels do not match the Pod labels, or no healthy Pods matching the selector exist.
  - **Solution:** Verify the `selector` in the Service manifest matches the `labels` in the Pod template of the Deployment [21]. Check the status of the Pods; if they are not `Running` and `Ready`, the Service will not route traffic to them.
- **Argo CD OutOfSync:**
  - **Cause:** The desired state in Git does not match the live state in the cluster. This could be due to manual changes in the cluster, errors during the Argo CD sync, or issues applying the manifests.
  - **Solution:** Use `argocd app diff` or the UI to see the differences [3]. Investigate errors in the sync history. Consider enabling auto-sync in Argo CD if manual changes are not intended.
- **Argo CD Health Status Unhealthy:**
  - **Cause:** Kubernetes reports that one or more resources managed by the Argo CD application are not in a healthy state (e.g., Deployment not having enough ready replicas, Pods crashing).
  - **Solution:** This is often a symptom of underlying Kubernetes resource issues. Follow the steps in Section 2 to debug the specific Kubernetes resources (Pods, Deployments, etc.).
- **Configuration Errors:**
  - **Cause:** Incorrect values or syntax in Helm charts or Kubernetes manifests.
  - **Solution:** Use `helm template` locally to render the manifests with the applied values and check for syntax errors or incorrect configurations [36, 37]. Use `kubectl apply --dry-run -o yaml` to see what Kubernetes would create or update without actually applying the changes [26, 38]. Use `kubectl diff` to preview changes before applying [23, 26]. Validate manifests with tools like `kubeval` [39].

---

## 4. Escalation

If the problem cannot be resolved using the steps above, escalate to the appropriate team (e.g., SRE, Platform Engineering) with details of the observed symptoms, the debugging steps taken, and any relevant logs or output.

---
