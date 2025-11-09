---
aliases: []
confidence: 
created: 2025-09-26T08:31:45Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:09Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: AWS SDE Audit
type:
uid: 
updated: 
version:
---

## EKS Networking Audit Report for `eoe-sde-codisc` (Updated)

**Date:** [[2025-09-26]]
[[AWS SDE Audit recommendations]]

### 1. Executive Summary

This report details the network configuration for the EKS cluster **`eoe-sde-codisc`**, based on the provided audit log. The cluster operates with a **private API endpoint** within VPC **`vpc-0aabc42188b2162bf`** in the `eu-west-2` (London) region.

Key findings from the detailed log include:

- The cluster utilises a mix of **public and private subnets**.
- Pod-to-pod networking is managed by **Calico CNI** using a **VXLAN overlay**.
- Traffic ingress is handled primarily by an **NGINX Ingress Controller**, which is exposed via an AWS Network Load Balancer (NLB). An additional Application Load Balancer (ALB) is also present in the VPC.
- Security is managed through both AWS **Security Groups** and Kubernetes **Network Policies**, although the policies in place are currently permissive.

---

### 2. AWS VPC and Infrastructure Layer

The underlying AWS infrastructure defines the primary security and routing boundaries for the cluster.

#### 2.1. VPC and Subnets

The cluster is provisioned in **`vpc-0aabc42188b2162bf`** across two primary subnets. An analysis of their associated route tables reveals a mixed public/private configuration:

- **`subnet-02b4bec3447cbbf9e` (Private):** This subnet's route table (`rtb-010658b9d1ef194c6`) directs default `0.0.0.0/0` traffic to a NAT Gateway (`nat-02c1a6d832f6683e5`). This is a standard private subnet configuration, allowing workloads to initiate outbound connections to the internet without being directly reachable from it.
- **`subnet-0c3d71c782e12d044` (Public):** This subnet's route table (`rtb-0c3588944a5ce5db3`) has a default `0.0.0.0/0` route pointing to an Internet Gateway (`igw-0b63cf7dd6df08d4e`). This makes resources in this subnet, such as load balancers, directly accessible from the internet.

#### 2.2. Security Groups (SGs)

Security Groups act as the main instance-level firewalls.

- **Cluster Security Group (`sg-02dcb1a5bbe8844b8`):** This SG is applied to the EKS control plane. Its ingress rules are configured to allow communication from the worker nodes and other cluster components. Notably, it also contains ingress rules from `0.0.0.0/0` for the NodePorts `31139` and `32623`, which are used by the Ingress Controller's Load Balancer. While this is functional, allowing direct access from the internet to nodes is a permissive configuration; typically, only the load balancer's source IPs would be allowed.
- **Node Security Group (`sg-0a3345e3be2761343`):** This SG is associated with the worker nodes and controls traffic directly to and from them. It facilitates node-to-node communication for the CNI, accepts traffic from the Load Balancer, and allows the nodes to communicate with the control plane.

#### 2.3. Network ACLs

All cluster subnets are associated with a single custom Network ACL (`acl-0b059cc861528dc9f`). This NACL has default rules allowing all inbound and all outbound traffic, making it non-restrictive. Security is therefore primarily being enforced by the Security Groups.

#### 2.4. Load Balancers

Two load balancers were identified in the VPC:

1. **NGINX Ingress NLB:** An AWS Network Load Balancer (`a09b6c067...`) listens on TCP ports **80** and **443**. It is tagged by Kubernetes (`kubernetes.io/service-name: ingress-nginx/ingress-nginx-controller`) and serves as the main entry point for the NGINX Ingress Controller.
2. **Relay ALB:** An AWS Application Load Balancer named `eoe-sde-codisc-relay-alb` listens on HTTPS port **443**. This ALB is not tagged by Kubernetes, suggesting it may have been provisioned and managed outside the standard Kubernetes service lifecycle, possibly for a specific application like the `hutch-relay` service.

---

### 3. Kubernetes Networking Layer

Internal cluster networking defines how services communicate and how they are exposed.

#### 3.1. CNI Plugin: Calico

The audit log confirms that **Calico** is the active CNI plugin.

- **Pod Networking:** Pods are assigned IP addresses from the `192.168.0.0/16` range.
- **Network Model:** Node annotations (`projectcalico.org/IPv4VXLANTunnelAddr`) confirm that Calico is using a **VXLAN overlay network**. This encapsulates pod-to-pod traffic when it traverses different nodes, allowing the pod network to function independently of the underlying VPC IP space.

#### 3.2. Traffic Ingress and Services

Traffic is routed to applications primarily through Kubernetes Ingress resources managed by NGINX.

- **Primary Ingress Host:** All main applications use the hostname `app.eoe-sde-codisc.privatelink.fitfile.net`. Path-based routing on this host directs traffic as follows:
  - `/ffcloud` ➡️ `hie-prod-34-ffcloud-service`
  - `/fitconnect` ➡️ `hie-prod-34-fitconnect-ftc`
  - `/fitfile` and `/` ➡️ `hie-prod-34-frontend-frontend`
- **ArgoCD Ingress:** A separate Ingress is defined for `argocd.eoe-sde-codisc.privatelink.fitfile.net`, routing directly to the `argocd-server` service.
- **NodePort Service:** The `hutch-relay` service is exposed on `NodePort` `32080`, allowing direct access via any node's IP address. This is likely the backend for the manually configured `eoe-sde-codisc-relay-alb`.

#### 3.3. Network Policies

Kubernetes Network Policies are in use in several namespaces to control pod-to-pod traffic flow.

- **Databases:** In the `hie-prod-34`, `hutch`, and `spicedb` namespaces, Network Policies are applied to `mongodb` and `postgresql` pods. These policies allow ingress traffic on their respective database ports (e.g., `5432/TCP` for PostgreSQL).
- **Minio:** A policy in `hie-prod-34` allows ingress to Minio on ports `9000` and `9001`.
- **Observation:** The current policies are not restrictive about the source of traffic, allowing connections from **any pod** within the cluster. For a more secure posture, these policies could be tightened to only allow ingress from specific application pods that require database access.
