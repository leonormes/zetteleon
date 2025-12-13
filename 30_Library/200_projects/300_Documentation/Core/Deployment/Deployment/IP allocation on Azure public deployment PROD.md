---
aliases: []
confidence: 
created: 2025-02-17T11:32:55Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:51Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ff_deploy, networking]
title: IP allocation on Azure public deployment PROD
type:
uid: 
updated: 
version:
---

OK, let's break down the IP allocation in your AKS cluster based on the provided report.

**1. Node IP Addresses**

- **Source:** These IPs come from the Azure Virtual Network subnet that you assigned to the AKS cluster during creation.
- **Management:** Azure manages the allocation of these IPs to the nodes. When you scale the cluster up or down, Azure automatically assigns or releases IPs from the subnet.
- **Purpose:** Each node in the cluster gets a unique IP address in this subnet. This allows the nodes to communicate with each other and with the outside world.

**2. Pod IP Addresses**

- **Source:** Pod IPs are allocated from a different, **cluster-internal** IP range. This range is separate from your Azure Virtual Network subnet.
- **Management:** Kubernetes manages the Pod IP address space. When a pod is created, Kubernetes assigns it an available IP from this internal range.
- **Purpose:** Pods use these IPs for communication within the cluster. Note that these IPs are not reachable from outside the cluster.

**3. Service IP Addresses**

- **Source:** Service IPs also come from the cluster's internal IP range.
- **Management:** Kubernetes assigns Service IPs.
- **Purpose:** Services provide a stable, internal endpoint for accessing a group of pods. Even if the pods backing a service change, the service IP remains the same.
    - **ClusterIP:** The default service type. It gives you an IP accessible only from within the cluster.
    - **LoadBalancer:** This type assigns an external Azure Load Balancer IP in addition to the internal ClusterIP. This allows external access to your service.

**IP Management Summary**

- **Azure:** Manages the Virtual Network subnet and assigns IPs to nodes.
- **Kubernetes:** Manages the cluster's internal IP address space and allocates IPs to pods and services.

**Key Takeaways**

- Nodes have IPs in your Azure VNet subnet, making them directly accessible.
- Pods and services use internal cluster IPs, not directly visible from outside.
- Services of type `LoadBalancer` get an additional external IP for outside access.

**Obsidian Markdown Format**

## AKS Cluster IP Allocation

### 1. Node IPs
- **Source:** Azure Virtual Network subnet
- **Management:** Azure
- **Purpose:** Node communication

### 2. Pod IPs
- **Source:** Cluster-internal IP range
- **Management:** Kubernetes
- **Purpose:** Pod communication

### 3. Service IPs
- **Source:** Cluster-internal IP range
- **Management:** Kubernetes
- **Purpose:** Stable endpoint for pods
    - **ClusterIP:** Internal access
    - **LoadBalancer:** External access

### IP Management
- **Azure:** VNet and node IPs
- **Kubernetes:** Cluster-internal IPs

If you'd like, you can ask me to delve deeper into a specific aspect of the IP allocation or network configuration.
