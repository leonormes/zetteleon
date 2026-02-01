---
aliases: ["CoreDNS Configuration", "Hybrid Cloud DNS", "K8s DNS Architecture"]
confidence: "5/5"
created: 2025-10-16T08:22:15Z
epistemic: "technical"
last_reviewed: "2025-12-30"
modified: 2026-01-08T10:49:43+00:00
purpose: "Technical specification for DNS architecture and hybrid networking within the FitFile environment."
review_interval: "6 months"
see_also: ["[[SoT - FitFile Deployment - Operations & Troubleshooting]]", "[[SoT - FitFile Deployment - Strategy & Architecture]]"]
source_of_truth: []
status: "stable"
tags: ["aks", "eks", "kubernetes", "SoftwareEngineering/Networking", "SoftwareEngineering/networking/dns"]
title: SoT - FitFile Deployment - Networking & DNS
type: "SoT"
uid: 
updated: 
---

## 1. Hybrid DNS Principles

We enforce a Split-Horizon DNS strategy to manage resolution across Public (Internet), Private (Cloud VNet), and Legacy (On-Prem) boundaries.

1. Public Resolution: Global endpoints handled via Cloudflare.
2. Private Internal: `*.fitfile.internal` for machine-to-machine traffic. Never exposed to public resolvers.
3. Conditional Forwarding:
    - `nhs.local` and `customer.corp` queries are routed to On-Premise resolvers via VPN/ExpressRoute.
    - `privatelink.*.azmk8s.io` queries are routed to the cloud recursive resolver (`168.63.129.16` for Azure).

---

## 2. CoreDNS Architecture

The cluster DNS is the primary traffic router. We use NodeLocal DNSCache to improve performance and mitigate conntrack issues.

### 2.1 The Hybrid Corefile

All clusters must use a variant of this configuration to support hybrid resolution.

```yaml
.:53 {
    errors
    health
    ready
    kubernetes cluster.local in-addr.arpa ip6.arpa {
      pods insecure
      fallthrough in-addr.arpa ip6.arpa
    }
    # Forwarding rules for On-Premise environments
    forward nhs.local 10.252.154.40 {
      force_tcp
    }
    # Forwarding for Cloud Native Endpoints (Azure Private Link)
    forward privatelink.uksouth.azmk8s.io 168.63.129.16 {
      force_tcp
    }
    forward . 1.1.1.1 8.8.8.8
    cache 30
}
```

---

## 3. Cloud-Specific Implementations

### 3.1 Azure Private Resolver

We use the Azure DNS Private Resolver service to bridge the VNet and On-Prem networks.

- Inbound Endpoint: Allows On-Prem servers to resolve records in Azure Private DNS Zones.
- Outbound Endpoint: Allows AKS to forward specific internal queries back to On-Prem.

### 3.2 AWS Route 53 Resolver

Similar to Azure, we use Route 53 Resolver Endpoints.

- Forwarding Rules: Applied to the VPC to route `nhs.local` traffic to the corporate data center.

---

## 4. Troubleshooting DNS

_Detailed troubleshooting steps are located in: [[SoT - FitFile Deployment - Operations & Troubleshooting]]_

- Use `netshoot` for debugging.
- Verify `ndots:2` configuration in application pods.
- Check firewall rules (UDP/TCP 53) between the cluster and resolvers.
