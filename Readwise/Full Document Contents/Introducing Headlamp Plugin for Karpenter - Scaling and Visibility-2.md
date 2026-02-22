# Introducing Headlamp Plugin for Karpenter - Scaling and Visibility

![rw-book-cover](https://kubernetes.io/icons/icon-128x128.png)

## Metadata
- Author: [[Kubernetes – Production-Grade Container Orchestration]]
- Full Title: Introducing Headlamp Plugin for Karpenter - Scaling and Visibility
- Category: #articles
- Summary: The Headlamp Karpenter Plugin lets users see and manage autoscaling in Kubernetes clusters in real time. It shows scaling events, metrics, and resource relationships to help debug and tune cluster behavior. The plugin supports live edits and works with several cloud providers, improving cluster visibility and control.
- URL: https://kubernetes.io/blog/2025/10/06/introducing-headlamp-plugin-for-karpenter/

## Full Document
Headlamp is an open‑source, extensible Kubernetes SIG UI project designed to let you explore, manage, and debug cluster resources.

Karpenter is a Kubernetes Autoscaling SIG node provisioning project that helps clusters scale quickly and efficiently. It launches new nodes in seconds, selects appropriate instance types for workloads, and manages the full node lifecycle, including scale-down.

The new Headlamp Karpenter Plugin adds real-time visibility into Karpenter’s activity directly from the Headlamp UI. It shows how Karpenter resources relate to Kubernetes objects, displays live metrics, and surfaces scaling events as they happen. You can inspect pending pods during provisioning, review scaling decisions, and edit Karpenter-managed resources with built-in validation. The Karpenter plugin was made as part of a LFX mentor project.

The Karpenter plugin for Headlamp aims to make it easier for Kubernetes users and operators to understand, debug, and fine-tune autoscaling behavior in their clusters. Now we will give a brief tour of the Headlamp plugin.

#### Map view of Karpenter Resources and how they relate to Kubernetes resources

Easily see how Karpenter Resources like NodeClasses, NodePool and NodeClaims connect with core Kubernetes resources like Pods, Nodes etc.

![Map view showing relationships between resources](https://kubernetes.io/blog/2025/10/06/introducing-headlamp-plugin-for-karpenter/mini-map-view.png)Map view showing relationships between resources
#### Visualization of Karpenter Metrics

Get instant insights of Resource Usage v/s Limits, Allowed disruptions, Pending Pods, Provisioning Latency and many more .

![NodePool default metrics shown with controls to see different frequencies](https://kubernetes.io/blog/2025/10/06/introducing-headlamp-plugin-for-karpenter/chart-1.png)NodePool default metrics shown with controls to see different frequencies
![NodeClaim default metrics shown with controls to see different frequencies](https://kubernetes.io/blog/2025/10/06/introducing-headlamp-plugin-for-karpenter/chart-2.png)NodeClaim default metrics shown with controls to see different frequencies
#### Scaling decisions

Shows which instances are being provisioned for your workloads and understand the reason behind why Karpenter made those choices. Helpful while debugging.

![Pod Placement Decisions data including reason, from, pod, message, and age](https://kubernetes.io/blog/2025/10/06/introducing-headlamp-plugin-for-karpenter/pod-decisions.png)Pod Placement Decisions data including reason, from, pod, message, and age
![Node decision data including Type, Reason, Node, From, Message](https://kubernetes.io/blog/2025/10/06/introducing-headlamp-plugin-for-karpenter/node-decisions.png)Node decision data including Type, Reason, Node, From, Message
#### Config editor with validation support

Make live edits to Karpenter configurations. The editor includes diff previews and resource validation for safer adjustments.

![Config editor with validation support](https://kubernetes.io/blog/2025/10/06/introducing-headlamp-plugin-for-karpenter/config-editor.png)Config editor with validation support
View and track Karpenter specific resources in real time such as “NodeClaims” as your cluster scales up and down.

![Node claims data including Name, Status, Instance Type, CPU, Zone, Age, and Actions](https://kubernetes.io/blog/2025/10/06/introducing-headlamp-plugin-for-karpenter/node-claims.png)Node claims data including Name, Status, Instance Type, CPU, Zone, Age, and Actions
![Node Pools data including Name, NodeClass, CPU, Memory, Nodes, Status, Age, Actions](https://kubernetes.io/blog/2025/10/06/introducing-headlamp-plugin-for-karpenter/nodepools.png)Node Pools data including Name, NodeClass, CPU, Memory, Nodes, Status, Age, Actions
![EC2 Node Classes data including Name, Cluster, Instance Profile, Status, IAM Role, Age, and Actions](https://kubernetes.io/blog/2025/10/06/introducing-headlamp-plugin-for-karpenter/nodeclass.png)EC2 Node Classes data including Name, Cluster, Instance Profile, Status, IAM Role, Age, and Actions
#### Dashboard for Pending Pods

View all pending pods with unmet scheduling requirements/Failed Scheduling highlighting why they couldn't be scheduled.

![Pending Pods data including Name, Namespace, Type, Reason, From, and Message](https://kubernetes.io/blog/2025/10/06/introducing-headlamp-plugin-for-karpenter/pending-pods.png)Pending Pods data including Name, Namespace, Type, Reason, From, and Message
##### **Karpenter Providers**

This plugin should work with most Karpenter providers, but has only so far been tested on the ones listed in the table. Additionally, each provider gives some extra information, and the ones in the table below are displayed by the plugin.

| Provider Name | Tested | Extra provider specific info supported |
| --- | --- | --- |
| [AWS](https://github.com/aws/karpenter-provider-aws) | ✅ | ✅ |
| [Azure](https://github.com/Azure/karpenter-provider-azure) | ✅ | ✅ |
| [AlibabaCloud](https://github.com/cloudpilot-ai/karpenter-provider-alibabacloud) | ❌ | ❌ |
| [Bizfly Cloud](https://github.com/bizflycloud/karpenter-provider-bizflycloud) | ❌ | ❌ |
| [Cluster API](https://github.com/kubernetes-sigs/karpenter-provider-cluster-api) | ❌ | ❌ |
| [GCP](https://github.com/cloudpilot-ai/karpenter-provider-gcp) | ❌ | ❌ |
| [Proxmox](https://github.com/sergelogvinov/karpenter-provider-proxmox) | ❌ | ❌ |
| [Oracle Cloud Infrastructure (OCI)](https://github.com/zoom/karpenter-oci) | ❌ | ❌ |

Please [submit an issue](https://github.com/headlamp-k8s/plugins/issues) if you test one of the untested providers or if you want support for this provider (PRs also gladly accepted).

Please see the [plugins/karpenter/README.md](https://github.com/headlamp-k8s/plugins/tree/main/karpenter) for instructions on how to use.

Please [submit an issue](https://github.com/headlamp-k8s/plugins/issues) if you use Karpenter and have any other ideas or feedback. Or come to the [Kubernetes slack headlamp channel](https://kubernetes.slack.com/?redir=%2Fmessages%2Fheadlamp) for a chat.
