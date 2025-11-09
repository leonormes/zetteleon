---
aliases: []
confidence: 
created: 2025-10-15T11:04:32Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: aws-sde logs
type:
uid: 
updated: 
version:
---

Right, I've reviewed the log file you provided. There are several important findings across different components of the `eoe-sde-codisc` cluster. I've categorised them by severity and provided analysis and recommendations for each.

---

## **🔥 Critical Finding**

### Vault Secrets Operator Permission Error

- **What I Found**: The `vault-secrets-operator` is being denied permission when trying to issue a TLS certificate.

```sh
{"level":"error",..."msg":"Vault request failed",..."path":"pki_int_hie-prod-34/issue/hie-prod-34-server",..."error":"...Code: 403. Errors:\\n\\n* 1 error occurred:\\n\\t* permission denied\\n\\n"}
```

- **Architectural Context**: This relates to the **EKS Access Control** and security model. The Vault Secrets Operator uses a Kubernetes service account that is supposed to have IAM credentials (likely via IRSA) to authenticate with Vault and perform actions based on its assigned policies.
- **Why It Matters**: This is a critical failure. It means that any service in your cluster relying on the operator to automatically generate or renew TLS certificates from your PKI backend **will not work**. This could lead to service outages when certificates expire.
- **Recommendation**: You need to check the Vault ACL policies associated with the role the operator is using. The role needs `update` permissions on the path `pki_int_hie-prod-34/issue/hie-prod-34-server`.
  1. **Find the Operator's Service Account**:

```bash
kubectl get pods -n vault-secrets-operator-system -l app.kubernetes.io/name=vault-secrets-operator -o jsonpath='{.items[0].spec.serviceAccountName}'
```

  2. **Check the Role in Vault**: Investigate the Vault role that this service account authenticates as. Check its attached policies and ensure one of them grants the required permissions. The policy in Vault should look something like this:

```hcl
# Policy for vault-secrets-operator
path "pki_int_hie-prod-34/issue/hie-prod-34-server" {
capabilities = ["update"]
}
```

---

## **⚠️ High Priority Findings**

### 1\. [[Cluster Autoscaler Cannot Scale Down Nodes]]

- **What I Found**: The cluster autoscaler is repeatedly trying to scale down but finds that two nodes are "unremovable" because their CPU request utilisation is too high (66% and 77%).

```sh
I1015 09:59:35.847271       1 eligibility.go:163] Node ip-10-65-6-220.eu-west-2.compute.internal unremovable: cpu requested (77.4745% of allocatable) is above the scale-down utilization threshold
I1015 09:59:35.847467       1 eligibility.go:163] Node ip-10-65-4-247.eu-west-2.compute.internal unremovable: cpu requested (66.5051% of allocatable) is above the scale-down utilization threshold
```

- **Architectural Context**: This relates to the **EKS Cluster (`module.eks`)** configuration, specifically the `Cluster Autoscaler` addon and the `WorkflowsNodeGroup` and `SystemNodeGroup`. These nodes are part of your worker node fleet.
- **Why It Matters**: This prevents the cluster from shrinking, which can lead to unnecessary AWS costs for running idle or underutilised EC2 instances. The default utilisation threshold is typically 50%, and your nodes are exceeding it.
- **Recommendation**:
  1. **Investigate Pods on the Nodes**: Find out which pods are running on these specific nodes and consuming the most CPU resources. This will tell you if the load is legitimate or if you have misconfigured resource requests.

```bash
# Describe the nodes to see all running pods and their resource requests
kubectl describe node ip-10-65-6-220.eu-west-2.compute.internal
kubectl describe node ip-10-65-4-247.eu-west-2.compute.internal
```

  2. **Adjust Threshold (If Necessary)**: If this high utilisation is expected, you can adjust the cluster autoscaler's startup arguments to increase the `--scale-down-utilization-threshold`. This is a trade-off between cost and performance.

### 2\. MongoDB Metrics Exporter is Faulty

- **What I Found**: The `metrics` sidecar in your MongoDB pod is spamming a very long list of errors, all stating that a metric was "collected before with the same name and label values".

```sh
time=2025-10-15T09:59:17.411Z level=ERROR ... msg="error gathering metrics:100 error(s) occurred:\n* [from Gatherer #2] collected metric \"mongodb_ss_metrics_query_multiPlanner_histograms_classicMicros_lowerBound\" ... was collected before with the same name and label values\n
```

- **Why It Matters**: This indicates a bug in your MongoDB metrics exporter. It's generating duplicate Prometheus metrics within a single scrape cycle, which is invalid. This creates a lot of log noise and, more importantly, likely means your Prometheus/Grafana monitoring for MongoDB is unreliable or incomplete.
- **Recommendation**: This is a known issue with some versions of the MongoDB exporter. You should check the version of the exporter being used and look for an updated version or a configuration flag to resolve the issue. The problem often lies in how histograms or certain server status metrics are aggregated.

---

## **🟡 Medium Priority Findings**

### 1\. Unschedulable Trivy Pod

- **What I Found**: The cluster autoscaler logs show that a pod named `trivy-system/node-collector-596888ff97-bjzxf` is `unschedulable`. The reason is that it doesn't tolerate the taint `{workflows: true}` which is applied to nodes in the `WorkflowsNodeGroup`.

```sh
I1015 09:59:35.846840       1 orchestrator.go:610] Pod trivy-system/node-collector-596888ff97-bjzxf can't be scheduled on eks-WorkflowsNodeGroup... predicate "TaintToleration" didn't pass
```

- **Architectural Context**: This is related to the `WorkflowsNodeGroup` which is specifically tainted to only run certain pods. Your security scanning tool (Trivy) needs to be configured to run on these nodes.
- **Why It Matters**: Your Trivy node collector cannot run on the workflow nodes, meaning you have a blind spot in your security and vulnerability scanning for any images running on that node group.
- **Recommendation**: Add the required `toleration` to the Trivy `node-collector` DaemonSet or Deployment manifest so that it can be scheduled on the tainted workflow nodes.

```yaml
# Add this toleration to the pod spec for the trivy-node-collector
tolerations:
- key: "workflows"
  operator: "Equal"
  value: "true"
  effect: "NoSchedule"
```

### 2\. Volume Snapshot CRDs Are Missing

- **What I Found**: The `csi-snapshotter` container is continuously failing because the required Custom Resource Definitions (CRDs) for volume snapshots are not installed in the cluster.

```sh
E1015 09:59:25.911539       1 reflector.go:200] "Failed to watch" err="failed to list *v1.VolumeSnapshotClass: the server could not find the requested resource (get volumesnapshotclasses.snapshot.storage.k8s.io)"
```

- **Why It Matters**: If you intend to use EBS volume snapshots for backups or other operations, this functionality is currently broken. If you do not intend to use it, these errors are just harmless noise.
- **Recommendation**: If you need volume snapshot capabilities, you must install the VolumeSnapshot CRDs into the cluster. You can typically get these from the `kubernetes-csi/external-snapshotter` GitHub repository. If you don't need this feature, you could consider disabling the snapshotter component of the EBS CSI driver to reduce the noise.

---

## **ℹ️ Informational Findings**

- **Relay Service Authentication**: The `hutch-relay` pod logs many messages like `Basic was not authenticated. Failure message: Missing Authorization Header`. These appear to be from health checks and its job polling mechanism. This is likely normal behaviour for unauthenticated probes but creates significant log noise. You could consider configuring your health probes to use a valid (low-privilege) auth header or adjusting the application's logging level to reduce this chatter.
- **Tigera Operator Warnings**: The `tigera-operator` frequently logs that it cannot find StatefulSets for Prometheus and Alertmanager. This means the operator is trying to manage Calico's own monitoring stack, which doesn't appear to be deployed. This is not an issue if you are using a separate monitoring solution, but it adds to the log noise.
- **Deprecated API Usage**: The `calico-typha` pods are issuing a warning that the `v1 Endpoints` API is deprecated. This is a low-priority notice. Calico will need to be updated eventually to use the newer `EndpointSlice` API, but this is not an immediate problem.
