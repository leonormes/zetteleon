---
aliases: []
confidence: 
created: 2025-09-13T12:33:18Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:09Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, infrastructure, load-balancer, topic/technology/networking]
title: AWS Network Load Balancer Analysis
type:
uid: 
updated: 
version:
---

## General Details

- **Type**: Network Load Balancer (NLB)
- **Status**: Active
- **Scheme**: Internal (only accessible from within its VPC)
- **VPC ID**: `vpc-0aabc42186b2162bf`
- **IP Address Type**: IPv4
- **DNS Name**: `info-a09b6c067806443d8ba14d79fbd6a2ac-3d6a600ba7023f54.elb.eu-west-2.amazonaws.com`
- **ARN**: `arn:aws:elasticloadbalancing:eu-west-2:155808916559:loadbalancer/net/a09b6c067806443d8ba14d79fbd6a2ac/3d6a600ba7023f54`
- **Availability Zones**: Deployed across three AZs in the `eu-west-2` (London) region:
  - `eu-west-2a` (subnet-024dbc3447cbbb95e)
  - `eu-west-2b` (subnet-0c3d7fc782e12d044)
  - `eu-west-2c` (subnet-04f8bc449d443e9e3)

---

## Listener Configuration

The load balancer has two listeners configured to accept TCP traffic on different ports.

1. **TCP Port 443** (typically for HTTPS traffic)
   - **Protocol**: TCP
   - **Port**: 443
   - **Forwarding Target**: A target group named `k8s-ingressn-ingressn-cae349d97f`. The name suggests it's routing traffic to a Kubernetes Ingress controller.

2. **TCP Port 80** (typically for HTTP traffic)
   - **Protocol**: TCP
   - **Port**: 80
   - **Forwarding Target**: A target group named `k8s-ingressn-ingressn-c88724d983`.

Since this is a Network Load Balancer operating at Layer 4, it does not terminate TLS. The "Security policy" and "SSL/TLS certificate" fields are marked as "Not applicable". Any TLS handling would be done by the services in the target groups.

## Analysis of Traffic Flow (Updated)

This document explains how traffic travels from its origin to its final destination based on the configuration of the AWS Network Load Balancer `a09b6c06780644...`. This version is updated with findings from the inspection script and DNS resolution.

### Current State: Degraded Operation

The inspection reveals a critical issue: **only one of three registered EC2 instances is healthy**. All traffic is currently being routed to instance `i-0e32193c309a0eb8b`. This means the service lacks high availability and is vulnerable to an outage if that single instance fails.

### The Journey of a Packet

The configuration uses a `NodePort` pattern to expose a Kubernetes Ingress controller.

#### Step 1: Entry Point (The Load Balancer)

- An internal client within the VPC resolves the load balancer's DNS name (`a09b6c06...amazonaws.com`). The DNS lookup returns a list of private IP addresses corresponding to the load balancer's network interfaces, such as **`10.65.4.210`** and **`10.65.7.184`**.
- The client selects one of these IPs (e.g., `10.65.4.210`) and sends a TCP packet to it, destined for either **port 80** or **port 443**.

#### Step 2: Listener and Routing (Layer 4)

- The Network Load Balancer (NLB) receives the TCP packet on one of its private IPs. It checks the destination port to select a listener.
  - If the port is **80**, it selects the `k8s-ingressn-ingressn-c88724a983` target group.
  - If the port is **443**, it selects the `k8s-ingressn-ingressn-cae3d9a7ff` target group.
- The NLB looks at the health of the registered targets in the chosen group. **Crucially, it only finds one healthy target (`i-0e32193c309a0eb8b`)**.
- It forwards the TCP packet directly to the specific `NodePort` on that single healthy EC2 instance (e.g., port `31139` for HTTP, `32623` for HTTPS).

#### Step 3: Target Node and Kube-Proxy

- The packet arrives at the high-numbered port on the EC2 instance `i-0e32193c309a0eb8b`.
- The node's internal Kubernetes networking service (`kube-proxy`) intercepts the packet. It knows that this `NodePort` corresponds to the Ingress controller's service.
- `kube-proxy` forwards the packet to the actual Ingress controller pod running on that node.

#### Step 4: Final Destination (Kubernetes Ingress Pod)

- The packet finally arrives at the Ingress controller pod. **This is where Layer 7 (Application) logic begins.**
- The Ingress software (e.g., NGINX) inspects the HTTP headers (`Host`, path, etc.). If the traffic was on port 443, it also performs TLS termination here.
- Based on its routing rules (Kubernetes Ingress objects), it proxies the request to the correct internal Kubernetes Service and, ultimately, to the final application pod that will handle the request.

#### Summary

The traffic ends up at an application pod inside the Kubernetes cluster, but it gets there by being routed **exclusively through the single healthy node (`i-0e32193c309a0eb8b`)**. The NLB correctly identifies the unhealthy nodes and avoids sending them traffic, but this has created a single point of failure for the entire application. The root cause is that the health checks are failing on the other two nodes.

This document explains how traffic travels from its origin to its final destination based on the configuration of the AWS Network Load Balancer `a09b6c06780644...`. This version is updated with findings from the inspection script.

## Analysis of Traffic Flow (Updated)

This document explains how traffic travels from its origin to its final destination based on the configuration of the AWS Network Load Balancer `a09b6c06780644...`. This version is updated with findings from the inspection script and DNS resolution.

### Current State: Degraded Operation

The inspection reveals a critical issue: **only one of three registered EC2 instances is healthy**. All traffic is currently being routed to instance `i-0e32193c309a0eb8b`. This means the service lacks high availability and is vulnerable to an outage if that single instance fails.

### The Journey of a Packet

The configuration uses a `NodePort` pattern to expose a Kubernetes Ingress controller.

#### Step 1: Entry Point (The Load Balancer)

- An internal client within the VPC resolves the load balancer's DNS name (`a09b6c06...amazonaws.com`) to one of its private IPs.
- The client sends a TCP packet to this IP, destined for either **port 80** or **port 443**.

#### Step 2: Listener and Routing (Layer 4)

- The Network Load Balancer (NLB) receives the TCP packet. It checks the destination port to select a listener.
  - If the port is **80**, it selects the `k8s-ingressn-ingressn-c88724a983` target group.
  - If the port is **443**, it selects the `k8s-ingressn-ingressn-cae3d9a7ff` target group.
- The NLB looks at the health of the registered targets in the chosen group. **Crucially, it only finds one healthy target (`i-0e32193c309a0eb8b`)**.
- It forwards the TCP packet directly to the specific `NodePort` on that single healthy EC2 instance (e.g., port `31139` for HTTP, `32623` for HTTPS).

#### Step 3: Target Node and Kube-Proxy

- The packet arrives at the high-numbered port on the EC2 instance `i-0e32193c309a0eb8b`.
- The node's internal Kubernetes networking service (`kube-proxy`) intercepts the packet. It knows that this `NodePort` corresponds to the Ingress controller's service.
- `kube-proxy` forwards the packet to the actual Ingress controller pod running on that node.

#### Step 4: Final Destination (Kubernetes Ingress Pod)

- The packet finally arrives at the Ingress controller pod. **This is where Layer 7 (Application) logic begins.**
- The Ingress software (e.g., NGINX) inspects the HTTP headers (`Host`, path, etc.). If the traffic was on port 443, it also performs TLS termination here.
- Based on its routing rules (Kubernetes Ingress objects), it proxies the request to the correct internal Kubernetes Service and, ultimately, to the final application pod that will handle the request.

#### Summary

The traffic ends up at an application pod inside the Kubernetes cluster, but it gets there by being routed **exclusively through the single healthy node (`i-0e32193c309a0eb8b`)**. The NLB correctly identifies the unhealthy nodes and avoids sending them traffic, but this has created a single point of failure for the entire application. The root cause is that the health checks are failing on the other two nodes.
