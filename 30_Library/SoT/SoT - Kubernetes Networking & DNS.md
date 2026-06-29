---
aliases:
- Cluster Networking
- K8s Networking
- Pod Networking
created: 2025-12-16 13:52:08+00:00
last_reviewed: '2025-12-23'
modified: 2026-05-26 11:44:19+00:00
status: stable
tags:
- cni
- kubernetes
- service_discovery
- SoftwareEngineering/Networking
- SoftwareEngineering/networking/dns
title: SoT - Kubernetes Networking & DNS
type: SoT
updated: null
permalink: llmeon/30-library/so-t/so-t-kubernetes-networking-dns
---

## 1. The Core Model: "Flat Network"

Kubernetes mandates a Flat Network model where:

- All Pods can communicate with all other Pods without NAT.
- The IP that a Pod sees itself as is the same IP that others see it as.

### The Implementation: CNI (Container Network Interface)

The wiring is pluggable. CNI Plugins (like Calico, Cilium, Flannel) implement this model:

- Overlay Networks: Encapsulate packets to span across Nodes (e.g., VXLAN).
- Direct Routing: Route packets natively without encapsulation (e.g., BGP).
- Observability: See [[SoT - Calico Observability]] for details on monitoring the CNI layer via Prometheus/Grafana.

---

## 2. The Complete Request Flow: Public User to Private Pod

Cloud-native ingress uses multiple layers of abstraction to route a single FQDN to a container.

1. Public DNS Resolution: Browser resolves `www.example.com` to the public IP of a cloud Application Load Balancer (ALB).
2. Edge Routing (ALB): ALB terminates TLS, inspects the Host Header, and forwards traffic to the cluster nodes on a NodePort.
3. Ingress Routing (Ingress Controller): An in-cluster proxy (e.g., NGINX) receives the traffic. It also inspects the Host header and consults an Ingress Resource to find the target Kubernetes Service.
4. Internal Service Discovery: The Ingress controller queries CoreDNS for the service FQDN (e.g., `webapp.prod.svc.cluster.local`).
5. Cluster DNS Resolution: CoreDNS returns the ClusterIP.
6. Service-to-Pod Routing: `kube-proxy` load-balances the request from the ClusterIP to the private IP of a healthy Backend Pod.

---

## 3. Service Discovery (DNS & Services)

### The Service Abstraction

A Service provides a stable ClusterIP and DNS name, acting as an internal Layer 4 Load Balancer.

- ClusterIP: Internal-only IP.
- NodePort: Exposes Service on a static port on each Node IP.
- LoadBalancer: Provisions an external cloud load balancer (e.g., AWS ELB).

### CoreDNS (The Cluster Phonebook)

CoreDNS resolves service names to ClusterIPs within the cluster and can be configured with Conditional Forwarding for cross-cloud name resolution (e.g., resolving AWS Route53 names from an Azure AKS pod).

---

## 4. Network Security (Policies)

By default, Kubernetes networking is Open.

- Network Policies: Act as a firewall for Pods, using Selector-Based rules.
- Zero Trust: A best practice is to "Default Deny" all traffic and explicitly allow only required flows.

---

## 5. Private Cluster Ingress Patterns (EKS Specifics)

In private clusters where worker nodes lack public IPs, ingress requires explicit architectural choices for external connectivity (e.g., VPN, Direct Connect, or PrivateLink).

### Pattern A: Internal LoadBalancer (NLB/ALB)

- Mechanism: A Service of type `LoadBalancer` with annotations for an _internal_ AWS LB (`service.beta.kubernetes.io/aws-load-balancer-internal: "true"`).
- Use Case: Best for private connectivity via VPC Peering or VPN.
- Protocol: NLB for Layer 4 (TCP/UDP), ALB for Layer 7 (HTTP/S).

### Pattern B: AWS Load Balancer Controller (Ingress)

- Mechanism: Uses an `Ingress` resource managed by the AWS LB Controller to provision an ALB.
- Key Feature: Can be configured as `scheme: internal` to keep traffic within the VPC.
- Optimization: Supports "IP Mode" targets (sending traffic directly to Pod IPs) or "Instance Mode" (via NodePorts).

### Pattern C: NodePort + Manual Gateway

- Mechanism: Service type `NodePort` combined with a manually provisioned gateway or proxy.
- Source IP: Use `externalTrafficPolicy: Local` to preserve client source IP, though this can lead to traffic imbalance across nodes.

---

## 6. Troubleshooting Heuristics

> [!abstract] See Full Protocol
> For the step-by-step diagnostic algorithm, see: [[Protocol - HIE--NNUH Network Debugging]]

1. Pod-to-Pod: Is the CNI healthy? (`ping` Pod IPs).
2. Service Discovery: Can you resolve the name? (`nslookup my-service`).
3. Connectivity: Is `kube-proxy` running? Are endpoints populated? (`kubectl get endpoints`).
4. Policy: Is a Network Policy silently dropping packets? Use `tcpdump` to verify "SYN sent, no ACK" (Blackhole).

---

## 7. Cloud Provider Constraints & Conflicts

### Case Study: AWS Existing DNS Endpoints

In brownfield AWS environments, existing DNS entries can block Terraform deployments.

- Scenario: Terraform fails to create DNS records because entries like `ecr.eu-west-2.api.aws`, `datasync…`, or `vpce…` already exist.
- Root Cause: These are often VPC Interface Endpoints managed by AWS or another account. They have specific `HostedZoneId` and `Owner` fields (e.g., `vpce.amazonaws.com`).
- Resolution:
    - Discovery: Use `ec2:DescribeVpcEndpoints` to identify the owners.
    - Planning: Define ownership of DNS zones before deployment. If a VPC Endpoint exists, your automation must accept it as an external dependency rather than trying to recreate it.