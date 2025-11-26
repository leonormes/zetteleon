---
title: "Azure Kubernetes Services (AKS) Core Concepts - Azure Kubernetes Service"
source: "https://learn.microsoft.com/en-us/azure/aks/core-aks-concepts?source=docs"
created: 2025-11-24
tags:
---
## Core concepts for Azure Kubernetes Service (AKS)

This article describes core concepts of Azure Kubernetes Service (AKS), a managed Kubernetes service that you can use to deploy and operate containerized applications at scale on Azure.

Kubernetes is an open-source container orchestration platform for automating the deployment, scaling, and management of containerized applications. For more information, see the official [Kubernetes documentation](https://kubernetes.io/docs/home/).

AKS is a managed Kubernetes service that simplifies deploying, managing, and scaling containerized applications that use Kubernetes. For more information, see [What is Azure Kubernetes Service (AKS)?](https://learn.microsoft.com/en-us/azure/aks/what-is-aks).

## Cluster components

An AKS cluster is divided into two main components:

- **Control plane**: The control plane provides the core Kubernetes services and orchestration of application workloads.
- **Nodes**: Nodes are the underlying virtual machines (VMs) that run your applications.

![Screenshot that shows Kubernetes control plane and node components.](https://learn.microsoft.com/en-us/azure/aks/media/concepts-clusters-workloads/control-plane-and-nodes.png)

### Control plane

The Azure managed control plane is composed of several components that help manage the cluster:

| Component | Description |
| --- | --- |
| `kube-apiserver` | The API server ([kube-apiserver](https://kubernetes.io/docs/concepts/overview/components/#kube-apiserver)) exposes the Kubernetes API to enable requests to the cluster from inside and outside of the cluster. |
| `etcd` | The highly available key-value store [etcd](https://kubernetes.io/docs/concepts/overview/components/#etcd) helps to maintain the state of your Kubernetes cluster and configuration. |
| `kube-scheduler` | The scheduler ([kube-scheduler](https://kubernetes.io/docs/concepts/overview/components/#kube-scheduler)) helps to make scheduling decisions. It watches for new pods with no assigned node and selects a node for them to run on. |
| `kube-controller-manager` | The controller manager ([kube-controller-manager](https://kubernetes.io/docs/concepts/overview/components/#kube-controller-manager)) runs controller processes, such as noticing and responding when nodes go down. |
| `cloud-controller-manager` | The cloud controller manager ([cloud-controller-manager](https://kubernetes.io/docs/concepts/overview/components/#cloud-controller-manager)) embeds cloud-specific control logic to run controllers specific to the cloud provider. |

### Nodes

Each AKS cluster has at least one node, which is an Azure VM that runs Kubernetes node components. The following components run on each node:

| Component | Description |
| --- | --- |
| `kubelet` | The [kubelet](https://kubernetes.io/docs/concepts/overview/components/#kubelet) ensures that containers are running in a pod. |
| `kube-proxy` | The [kube-proxy](https://kubernetes.io/docs/concepts/overview/components/#kube-proxy) is a network proxy that maintains network rules on nodes. |
| `container runtime` | The [container runtime](https://kubernetes.io/docs/concepts/overview/components/#container-runtime) manages the execution and lifecycle of containers. |

![Screenshot that shows Azure virtual machine and supporting resources for a Kubernetes node.](https://learn.microsoft.com/en-us/azure/aks/media/concepts-clusters-workloads/aks-node-resource-interactions.png)

## Node configuration

Configure the following settings for nodes.

The *Azure VM size* for your nodes defines CPUs, memory, size, and the storage type available, such as a high-performance solid-state drive or a regular hard-disk drive. The VM size you choose depends on the workload requirements and the number of pods that you plan to run on each node. As of May 2025, the default VM SKU and size will be dynamically selected by AKS based on available capacity and quota if the parameter is left blank during deployment. For more information, see [Supported VM sizes in Azure Kubernetes Service (AKS)](https://learn.microsoft.com/en-us/azure/aks/quotas-skus-regions#supported-vm-sizes).

In AKS, the *VM image* for your cluster's nodes is based on Ubuntu Linux, [Azure Linux](https://learn.microsoft.com/en-us/azure/aks/use-azure-linux), or Windows Server 2022. When you create an AKS cluster or scale out the number of nodes, the Azure platform automatically creates and configures the requested number of VMs. Agent nodes are billed as standard VMs. Any VM size discounts, including [Azure reservations](https://learn.microsoft.com/en-us/azure/cost-management-billing/reservations/save-compute-costs-reservations), are automatically applied.

### OS disks

Default OS disk sizing is used on new clusters or node pools only when a default OS disk size isn't specified. This behavior applies to both managed and ephemeral OS disks. For more information, see [Default OS disk sizing](https://learn.microsoft.com/en-us/azure/aks/concepts-storage#default-os-disk-sizing).

### Resource reservations

AKS uses node resources to help the nodes function as part of the cluster. This usage can cause a discrepancy between the node's total resources and the allocatable resources in AKS. To maintain node performance and functionality, AKS reserves two types of resources, CPU and memory, on each node. For more information, see [Resource reservations in AKS](https://learn.microsoft.com/en-us/azure/aks/node-resource-reservations).

### OS

AKS supports two linux distros: Ubuntu and Azure Linux. Ubuntu is the default Linux distro on AKS. Windows node pools are also supported on AKS with the [Long Term Servicing Channel (LTSC)](https://learn.microsoft.com/en-us/windows-server/get-started/servicing-channels-comparison) as the default channel on AKS. For more information on default OS versions, see documentation on [node images](https://learn.microsoft.com/en-us/azure/aks/node-images).

### Container runtime

A container runtime is software that executes containers and manages container images on a node. The runtime helps abstract away system calls or OS-specific functionality to run containers on Linux or Windows. For Linux node pools, [containerd](https://containerd.io/) is used on Kubernetes version 1.19 and higher. For Windows Server 2019 and 2022 node pools, [containerd](https://containerd.io/) is generally available and is the only runtime option on Kubernetes version 1.23 and higher.

## Pods

A *pod* is a group of one or more containers that share the same network and storage resources and a specification for how to run the containers. Pods typically have a 1:1 mapping with a container, but you can run multiple containers in a pod.

## Node pools

In AKS, nodes of the same configuration are grouped together into *node pools*. These node pools contain the underlying virtual machine scale sets and virtual machines (VMs) that run your applications.

When you create an AKS cluster, you define the initial number of nodes and their size (version), which creates a [system node pool](https://learn.microsoft.com/en-us/azure/aks/use-system-pools). System node pools serve the primary purpose of hosting critical system pods, such as CoreDNS and `konnectivity`.

To support applications that have different compute or storage demands, you can create *user node pools*. User node pools serve the primary purpose of hosting your application pods.

For more information, see [Create node pools in AKS](https://learn.microsoft.com/en-us/azure/aks/create-node-pools) and [Manage node pools in AKS](https://learn.microsoft.com/en-us/azure/aks/manage-node-pools).

When you create an AKS cluster in an Azure resource group, the AKS resource provider automatically creates a second resource group called the *node resource group*. This resource group contains all the infrastructure resources associated with the cluster, including VMs, virtual machine scale sets, and storage.

For more information, see the following resources:

- [Why are two resource groups created with AKS?](https://learn.microsoft.com/en-us/azure/aks/faq)
- [Can I provide my own name for the AKS node resource group?](https://learn.microsoft.com/en-us/azure/aks/faq)
- [Can I modify tags and other properties of the resources in the AKS node resource group?](https://learn.microsoft.com/en-us/azure/aks/faq)

## Namespaces

Kubernetes resources, such as pods and deployments, are logically grouped into *namespaces* to divide an AKS cluster and create, view, or manage access to resources.

The following namespaces are created by default in an AKS cluster:

| Namespace | Description |
| --- | --- |
| `default` | The [default](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/#initial-namespaces) namespace allows you to start using cluster resources without creating a new namespace. |
| `kube-node-lease` | The [kube-node-lease](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/#initial-namespaces) namespace enables nodes to communicate their availability to the control plane. |
| `kube-public` | The [kube-public](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/#initial-namespaces) namespace isn't typically used, but you can use it so that resources are visible across the whole cluster by any user. |
| `kube-system` | The [kube-system](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/#initial-namespaces) namespace is used by Kubernetes to manage cluster resources, such as `coredns`, `konnectivity-agent`, and `metrics-server`. It is not recommended to deploy your own applications to this namespace. For rare cases where deploying your own applications to this namespace is necessary, see the [FAQ](https://learn.microsoft.com/en-us/azure/aks/faq#can-admission-controller-webhooks-affect-kube-system-and-internal-aks-namespaces-) to learn how. |

![Screenshot that shows Kubernetes namespaces to logically divide resources and applications.](https://learn.microsoft.com/en-us/azure/aks/media/concepts-clusters-workloads/namespaces.png)

## Cluster modes

In AKS, you can create a cluster with the Automatic or Standard mode. AKS Automatic provides a more fully managed experience. You can manage cluster configuration, including nodes, scaling, security, and other preconfigured settings. AKS Standard provides more control over the cluster configuration, including the ability to manage node pools, scaling, and other settings.

For more information, see [AKS Automatic and Standard feature comparison](https://learn.microsoft.com/en-us/azure/aks/intro-aks-automatic#aks-automatic-and-standard-feature-comparison).

## Pricing tiers

AKS offers three pricing tiers for cluster management: Free, Standard, and Premium. The pricing tier you choose determines the features that are available for managing your cluster.

For more information, see [Pricing tiers for AKS cluster management](https://learn.microsoft.com/en-us/azure/aks/free-standard-pricing-tiers).

For more information, see [Supported Kubernetes versions in AKS](https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions).

For information on more core concepts for AKS, see the following resources:

- [AKS access and identity](https://learn.microsoft.com/en-us/azure/aks/concepts-identity)
- [AKS security](https://learn.microsoft.com/en-us/azure/aks/concepts-security)
- [AKS networking](https://learn.microsoft.com/en-us/azure/aks/concepts-network)
- [AKS storage](https://learn.microsoft.com/en-us/azure/aks/concepts-storage)
- [AKS scaling](https://learn.microsoft.com/en-us/azure/aks/concepts-scale)
- [AKS monitoring](https://learn.microsoft.com/en-us/azure/aks/monitor-aks)
- [AKS backup and recovery](https://learn.microsoft.com/en-us/azure/backup/azure-kubernetes-service-backup-overview)

---

## Additional resources

Training

Learning path

[Introduction to Kubernetes on Azure - Training](https://learn.microsoft.com/en-us/training/paths/intro-to-kubernetes-on-azure/?source=recommendations)

Learn about the basics of Docker containers, container orchestration with Kubernetes, and managed clusters on Azure Kubernetes Service.

Certification

[Microsoft Certified: Azure Fundamentals - Certifications](https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/?source=recommendations)

Demonstrate foundational knowledge of cloud concepts, core Azure services, plus Azure management and governance features and tools.