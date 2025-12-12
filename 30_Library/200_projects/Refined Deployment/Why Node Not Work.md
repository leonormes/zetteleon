---
aliases: []
confidence: 
created: 2025-07-29T09:08:43Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/technology/kubernetes, troubleshooting]
title: Why Node Not Work
type:
uid: 
updated: 
version:
---

Based on your description, a scheduled **node image upgrade** initiated by Azure is the most probable cause for the behaviour you observed. This is a common maintenance operation in AKS where the underlying virtual machine's operating system is updated with the latest security patches.

The process can fail or get stuck, leading to the state you described, for several reasons.

---

## How AKS Node Upgrades Work

When Azure performs a node image upgrade, it follows a **"cordon and drain"** process on a node-by-node basis to minimise disruption:

1. **Cordon:** The target node is marked as unschedulable. This is what applies the `NoSchedule` taint you observed (what you referred to as the "doNotSchedule" label). This prevents any new pods from being scheduled on that node while it's being prepared for removal.
2. **Drain:** Kubernetes attempts to gracefully evict all existing pods from the cordoned node. The pods are then meant to be recreated by their respective controllers (like Deployments or StatefulSets) on other available nodes in the cluster.
3. **Replace:** Once the node is empty, it's deleted, and a new node with the updated OS image is created and joined to the cluster.

This process repeats for each node until the entire cluster is updated.

---

## Why the Upgrade Process Fails or Gets Stuck

The "drain" step is the most common point of failure. If Kubernetes cannot successfully evict all the pods from a node within a certain timeout, the entire upgrade process for that node halts. This can leave your cluster in a broken state with a cordoned node and pods failing to reschedule.

Common reasons for a drain failure include:

- **Restrictive Pod Disruption Budgets (PDBs):** This is a very frequent cause. A PDB specifies the minimum number of available replicas an application must have. If evicting a pod would violate its PDB (e.g., trying to evict the last remaining replica of a service where `minAvailable` is 1), the drain operation will be blocked.
- **Pods Not Managed by a Controller:** Pods created directly ("naked pods") without a Deployment, StatefulSet, or ReplicaSet won't be recreated elsewhere. The drain process can hang waiting for them to be terminated, as there's no controller to manage their lifecycle.
- **Insufficient Cluster Resources:** When pods are evicted from one node, they need to be rescheduled onto the other nodes. If the remaining nodes (like your one "working fine" node) lack sufficient CPU, memory, or other resources, the evicted pods will get stuck in a `Pending` state. This resource pressure could be why pods on another node started failing.
- **Long-Running Hooks or Finalizers:** A pod can have a `preStop` hook that needs to complete before it terminates. If this hook hangs or takes too long, it will prevent the pod from being evicted. Similarly, custom controllers sometimes add `finalizers` to pods, and if the controller fails to remove the finalizer, the pod will never be deleted.
- **Local Storage:** Pods using host-based storage (like `hostPath` volumes) can sometimes interfere with drain operations, although this is less common than with PDBs.

In your scenario, it's likely the upgrade process started on one node, cordoned it, but failed to drain it because of one of the issues above. This left the node in a `NoSchedule` state. The evicted pods (and potentially others) were then crammed onto the remaining nodes, overloading one of them (causing its pods to fail) while the last node managed to handle its share of the load.

---

## How to Diagnose and Prevent This

To confirm the cause and prevent it from happening again:

1. **Check the Azure Activity Log:** In the Azure portal, navigate to your AKS resource and check the **Activity Log**. Filter for the time around midnight. You should see an operation like **"Upgrade Node Image"** which will confirm an automated upgrade was the trigger.
2. **Inspect Pod and Node Events:**

- Check events on the stuck pods with `kubectl describe pod <pod-name> -n <namespace>`. Look for messages about `FailedScheduling` due to resource constraints or PDB violations.
- Check events on the cordoned node with `kubectl describe node <node-name>`. You may see events related to drain failures.

1. **Review Your Pod Disruption Budgets:**

- List all PDBs with `kubectl get pdb --all-namespaces`.
- Ensure that the `minAvailable` or `maxUnavailable` values make sense for your application's architecture. A common mistake is setting `minAvailable: 1` on a Deployment that only has one replica.

1. **Implement Planned Maintenance Windows:** To control when these automatic upgrades occur, configure a **[Planned Maintenance window](https://learn.microsoft.com/en-us/azure/aks/planned-maintenance)** for your AKS cluster. This allows you to schedule these operations for off-peak hours when your team is available to monitor them.

Here are the commands to investigate the failing node and the overall cluster state.

## 1. Check Cluster and Node Status

First, get a high-level view of your nodes and identify the exact name of the failing one.

- **List all nodes and their status:** This command shows if nodes are `Ready` or `NotReady`.

Bash

```sh
kubectl get nodes -o wide
```

- **Describe the failing node:** This provides detailed information, including **Conditions** and **Taints**, which are crucial. You've already seen the **Events** from this, but the conditions at the top are also important.

Bash

```sh
kubectl describe node <failing-node-name>
```

---

## 2. Investigate Pods

Check the state of pods on the failing node and any pods that are failing cluster-wide.

- **List all pods scheduled on the failing node:** These are likely in a `Terminating`, `Unknown`, or `Error` state.

```sh
kubectl get pods --all-namespaces -o wide --field-selector spec.nodeName=<failing-node-name>
```

- **Find all pods that are not running:** This can help you spot pods that failed to reschedule off the broken node.

```sh
kubectl get pods --all-namespaces | grep -iv "Running\|Completed"
```

- **Describe a failing pod:** For any pod that is stuck or has errors, this command will tell you why it's failing (e.g., `FailedScheduling` because of insufficient resources on other nodes).

Bash

```sh
kubectl describe pod <pod-name> -n <namespace>
```

---

## 3. Check the Underlying Azure VM

Since the events point to an Azure infrastructure issue (IMDS failure), you need to use the `az` CLI to check the underlying Virtual Machine Scale Set (VMSS) instance.

- **Get the AKS node resource group:** AKS nodes live in a separate, managed resource group, usually named `MC_resourcegroup_clustername_location`.

Bash

```sh
az aks show --resource-group <your-cluster-rg> --name <your-cluster-name> --query "nodeResourceGroup" -o tsv
```

- **List the VMSS for your node pool:** Use the resource group name from the previous command.

Bash

```sh
az vmss list --resource-group <mc-resource-group-name> -o table
```

- **List the individual VM instances in the VMSS:** This will show you the Azure-level provisioning state of the node and its **Instance ID**, which you'll need for the next commands. The name should match your Kubernetes node name.

Bash

```sh
az vmss list-instances --resource-group <mc-resource-group-name> --name <vmss-name> -o table
```

- **Get a detailed health view of the specific VM instance:** This is a key command to check for platform-level faults.

Bash

```sh
az vmss get-instance-view --resource-group <mc-resource-group-name> --name <vmss-name> --instance-id <instance-id-from-above>
```

---

## 4. How to Fix It 🛠️

Given the events, the node is likely unrecoverable and needs to be replaced. The best course of action is to reimage it.

- **Attempt to drain the node (optional, may fail):** This tells Kubernetes to gracefully move workloads off. It will likely time out but is good practice to try.

Bash

```sh
kubectl drain <failing-node-name> --ignore-daemonsets --delete-emptydir-data --force
```

- **Reimage the node:** This is the most direct way to fix it. Azure will reprovision the VM with a fresh OS image, which will resolve the corrupt runtime and networking issues. The node will then automatically rejoin the cluster.

Bash

```sh
az vmss reimage --resource-group <mc-resource-group-name> --name <vmss-name> --instance-id <instance-id>
```
