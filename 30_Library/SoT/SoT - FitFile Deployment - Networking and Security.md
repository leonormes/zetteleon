---
aliases: ["K8s DNS Troubleshooting", "AKS DNS Operations", "Hybrid Cloud DNS"]
confidence: "5/5"
created: 2025-10-16T08:22:15Z
epistemic: "experience"
last_reviewed: "2025-12-26"
modified: 2025-12-26T18:08:04+00:00
purpose: "To provide the definitive guide for DNS architecture, operations, and troubleshooting within the FitFile hybrid cloud environment (AKS/EKS + On-Prem)."
review_interval: "6 months"
see_also: ["[[SoT - Cloud Networking Core Components]]", "[[SoT - Kubernetes Networking & DNS]]", "[[SoT - FitFile Deployment - Phase 2 - Core Infrastructure]]"]
source_of_truth: []
status: "stable"
tags: ["dns", "kubernetes", "networking", "troubleshooting", "aks", "eks"]
title: SoT - FitFile Deployment - Networking and Security
type: "SoT"
uid: 
updated: 
---

## 1. Principles of Hybrid DNS

To maintain stability across Azure, AWS, and On-Premise networks, we adhere to these core invariants:

1. **Split-Horizon Enforcement:**
    - **Public:** Use Cloudflare for global resolution. No split-horizon for public names to ensure ACME stability.
    - **Private:** Use `*.fitfile.internal` for M2M communication. Never expose these records publicly.
2. **Conditional Forwarding:**
    - Route *only* specific domains (e.g., `*.nhs.local`) to on-prem resolvers.
    - Default all other traffic to Cloud Recursive Resolvers (`168.63.129.16` for Azure, AmazonProvidedDNS for AWS).
3. **IaC Management:**
    - All DNS Zones, Resolver Rules, and Endpoints are managed via Terraform.

---

## 2. Kubernetes DNS Architecture (CoreDNS)

### 2.1 Configuration Best Practices

- **Minimal ConfigMap:** Use the `forward` plugin with explicit domain lists.
- **NodeLocal DNSCache:** Deployed to reduce latency and mitigate conntrack race conditions.
- **ndots Hygiene:** Set `ndots:2` for latency-sensitive workloads to reduce query amplification.

### 2.2 CoreDNS Config Snippet (Hybrid)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
          pods insecure
          fallthrough in-addr.arpa ip6.arpa
          ttl 30
        }
        # Forward On-Prem Zones
        forward nhs.local customer.corp 10.252.154.40 {
          force_tcp
        }
        # Forward Azure Private Link Zones (Required for AKS API)
        forward privatelink.uksouth.azmk8s.io 168.63.129.16 {
          force_tcp
        }
        # Default Upstream
        forward . 1.1.1.1 8.8.8.8
        cache 30
        loop
        reload
        loadbalance
    }
```

---

## 3. Cloud-Specific Implementations

### 3.1 Azure (AKS & Private Resolver)

- **Private DNS Zones:** Linked to VNet.
- **Resolver Architecture:**
    - **Inbound Endpoint:** Allows on-prem to query Azure Private Zones.
    - **Outbound Endpoint:** Used for conditional forwarding.
    - **Ruleset:**
        - `nhs.local` -> `10.252.154.40` (On-Prem)
        - `privatelink.*` -> `168.63.129.16` (Azure Recursive)

### 3.2 AWS (EKS & Route 53)

- **Private Hosted Zones:** Associated with the VPC.
- **Resolver Rules:**
    - **Outbound Endpoint:** Security Group allows UDP/TCP 53.
    - **Forward Rule:** `nhs.local` -> `10.252.154.40`.

---

## 4. Troubleshooting Guide

### 4.1 Common Failure Modes

1. **SERVFAIL:** Usually upstream timeout or firewall blocking UDP 53.
2. **NXDOMAIN on Private Link:** Kubernetes Pods cannot resolve Azure Private Endpoints because they are forwarding to On-Prem servers that don't know about Azure Private Zones.
    - **Fix:** Ensure conditional forwarding for `privatelink.*` points back to Azure DNS (`168.63.129.16`).
3. **ACME Validation Failures:** Split-horizon configuration shielding the challenge record.
    - **Fix:** Use DNS-01 validation via API.

### 4.2 Diagnostic Tools

- **Netshoot:** `kubectl run tmp-shell --rm -i --tty --image nicolaka/netshoot -- /bin/bash`
- **Dig:** `dig +short @10.252.154.40 nhs.local`
- **Logs:** `kubectl logs -n kube-system -l k8s-app=kube-dns`
