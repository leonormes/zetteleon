---
aliases: []
confidence: 
created: 2025-10-16T08:22:15Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:04Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/technology/networking/dns]
title: Azure AKS DNS operations and CoreDNS troubleshooting
type:
uid: 
updated: 
version:
---

Here’s a focused review of your recent work history as it relates to DNS in Kubernetes across AWS and Azure, followed by a consolidated set of best practices for private/public DNS in K8s and the two clouds.

Work history highlights (what you’ve already been doing)

- Azure AKS DNS operations and CoreDNS troubleshooting
  - You’ve actively debugged and managed CoreDNS in AKS, including restarts and config inspection from a jumpbox ([[2025-08-12]]), plus in-cluster DNS tests with netshoot.
- Split-horizon/public vs private DNS and certificate management
  - You documented the recurring issues with cert-manager when private zones shadow public records, and began consolidating naming into a dual-layer model (public vs M2M private) with private internal TLDs (e.g., fitfile.internal). See your report and notes captured in Consolidating DNS Configuration and Centralizing Naming (most recently updated [[2025-10-14]]).
- Hybrid DNS to on-prem for CUH
  - You coordinated DNS forwarding from AKS/VNet to on-prem (10.252.154.40), while keeping Azure private zone resolution for AKS API (privatelink.uksouth.azmk8s.io). You proposed two approaches and timeboxed testing: (1) on-prem conditional forwarding back to Azure; (2) Azure Private DNS Resolver with split-rule forwarding ([[2025-10-16]]).
  - You worked with CUH/Telefónica to allow Cloudflare (1.1.1.1) and on-prem DNS via Azure Firewall; initial tests with dig failed ([[2025-10-14]]), then succeeded after network changes (2025-10-15/16).
- Public DNS and naming consolidation
  - You moved towards centralizing public DNS in Cloudflare and using CNAMEs for customer vanity domains to FITFILE canonical names, to avoid cross-tenant updates and split-horizon pitfalls ([[2025-10-14]]).
- Terraform standardization across clouds
  - You’re curating TFC modules for private/public infrastructure and network/firewall components in Azure and AWS (e.g., private-infrastructure module updated recently; registry shows modules for AKS, firewall, hub network). References: [Configuration Index - Confluence](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2267906095/Configuration+Index) and TFC run for AWS EKS workspaces ([[2025-09-15]]): [TFC run](https://app.terraform.io/app/FITFILE-Platforms/workspaces/hie-prod-35/runs/run-GUggf96xncgLFD6C).

Best practices: private/public DNS for Kubernetes, AWS, and Azure

Core principles

- Separate public user-facing DNS from private M2M DNS
  - Public: use a public zone (e.g., Cloudflare) with globally resolvable names for UIs/endpoints. Avoid split-horizon for these names to keep ACME challenges reliable.
  - Private: use internal-only zones for service-to-service and hybrid integration (e.g., m2m.fitfile.internal / nhs.fitfile.internal). Never expose these publicly.
- Prefer conditional forwarding over “defaulting all DNS to X”
  - Route only the domains that truly need on-prem or cloud-private authority to the appropriate resolver. Everything else uses standard recursive resolution.
- Avoid private/public name collisions
  - Don’t use the same FQDN in both public and private zones. If split-view is unavoidable, strictly control who sees which view, and don’t use those names for ACME DNS-01 validation.
- Manage DNS via IaC
  - Treat DNS zones/records, conditional forward rules, and resolver endpoints as code (Terraform), with change control, auditability, and repeatability.

Kubernetes (generic) DNS practices

- CoreDNS
  - Keep the CoreDNS ConfigMap minimal. Use the forward plugin with explicit domain lists for on-prem/cloud-private zones.
  - Monitor CoreDNS: enable metrics to Prometheus/Grafana; alert on SERVFAIL spikes, latency, and timeouts.
- NodeLocal DNSCache
  - Deploy NodeLocal DNSCache to reduce latency and “query magnification.” It helps with ndots behavior and scales better under load.
- ndots hygiene
  - Prefer ndots:2 for latency-sensitive workloads if you control pod dnsConfig; otherwise rely on NodeLocal DNSCache to mitigate amplification.
- Liveness/readiness for DNS-dependent apps
  - Prefer health checks that tolerate DNS hiccups (backoff/retry), and avoid hard dependencies on single resolver IPs.

Public DNS and certificates

- Use Cloudflare (or your chosen public provider) for public names only.
- For ACME:
  - Prefer DNS-01 via API integration with your public DNS provider to avoid inbound HTTP validation issues in restricted networks.
  - If you must use HTTP-01, confirm firewall/proxy policies, SSL inspection bypasses, and reachability to ACME validation endpoints.
- Vanity/customer domains
  - Ask customers to create CNAMEs to your stable canonical names. You then terminate TLS and manage certs on your side. This avoids managing records in customer zones and avoids split-view traps.

AWS-specific best practices (EKS, Route 53, hybrid)

- Private DNS inside AWS
  - Use Route 53 Private Hosted Zones for internal app domains (e.g., \*.m2m.fitfile.internal) associated with the VPC where workloads live.
- Hybrid conditional forwarding
  - Use Route 53 Resolver Inbound/Outbound Endpoints and Resolver Rules:
    - Create outbound resolver rules for customer/on-prem zones (e.g., *.nhs.local,*.customer.corp) pointing to on-prem DNS IPs over the VPN/Direct Connect.
    - If on-prem needs to resolve AWS-private names, expose Inbound Endpoints and teach on-prem DNS to forward those private domains to the AWS inbound address.
- EKS and private control plane
  - If you direct pod DNS to on-prem resolvers, ensure conditional forwarders exist so privatelink.\<region\>.eks.amazonaws.com and other AWS private zones still resolve via AWS resolver paths.
  - Keep VPC DHCP options at AmazonProvidedDNS unless you have a well-managed hybrid plan; otherwise, breakage is common.
- Security
  - Allow UDP/TCP 53 only to your resolver IPs. Consider logging DNS queries via VPC flow logs and CoreDNS metrics. Keep resolver endpoints in subnets with the right NACL/SG policies.

Azure-specific best practices (AKS, Private DNS Zones, hybrid)

- Private DNS inside Azure
  - Use Azure Private DNS Zones for internal domains; link zones to the VNets where AKS nodes/pods run.
- Hybrid conditional forwarding
  - Prefer Azure DNS Private Resolver with:
    - Inbound endpoint for on-prem to query Azure-private zones when needed.
    - Outbound endpoint plus ruleset for conditional forwarding:
      - Forward privatelink.\<region\>.azmk8s.io to 168.63.129.16 (Azure recursive) if you’re otherwise pointing at on-prem resolvers.
      - Forward customer/on-prem domains (\*.nhs.local, etc.) to the on-prem DNS IPs (e.g., 10.252.154.40).
- AKS private cluster specifics
  - If the VNet DNS servers are set to on-prem resolvers, you must configure conditional forwarding for Azure private zones (AKS API privatelink zones, Private Endpoints) back to Azure or they won’t resolve.
- Firewall/proxy
  - When ACME or vendor APIs are needed, coordinate Azure Firewall/Proxy rules, especially if SSL inspection or auth proxies are in-path. You saw this with Grafana and Cloudflare on 2025-10-14/15.

Concrete snippets you can reuse

CoreDNS forward rules for hybrid

Use explicit zones to avoid sending everything to on-prem.

```yaml
# CoreDNS ConfigMap fragment
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
        # Forward on-prem/customer zones to on-prem DNS
        forward nhs.local customer.corp 10.252.154.40 {
          force_tcp
        }
        # Ensure AKS private API and Private Endpoints still resolve via Azure
        forward privatelink.uksouth.azmk8s.io 168.63.129.16 {
          force_tcp
        }
        # Everything else via upstream public resolvers (or NodeLocal)
        forward . 1.1.1.1 8.8.8.8
        cache 30
        loop
        reload
        loadbalance
    }
```

AWS Route 53 Resolver rules (Terraform sketch)

```hcl
# Outbound endpoint in VPC subnets
resource "aws_route53_resolver_endpoint" "outbound" {
  name               = "outbound-to-onprem"
  direction          = "OUTBOUND"
  security_group_ids = [aws_security_group.dns.id]
  ip_address {
    subnet_id = aws_subnet.shared_1.id
  }
  ip_address {
    subnet_id = aws_subnet.shared_2.id
  }
}

# Forward on-prem domain to on-prem DNS
resource "aws_route53_resolver_rule" "onprem" {
  domain_name          = "nhs.local."
  rule_type            = "FORWARD"
  resolver_endpoint_id = aws_route53_resolver_endpoint.outbound.id
  target_ip {
    ip = "10.252.154.40"
  }
  name = "forward-nhs-local"
}

# Associate rule to VPC with EKS
resource "aws_route53_resolver_rule_association" "eks_vpc" {
  resolver_rule_id = aws_route53_resolver_rule.onprem.id
  vpc_id           = aws_vpc.eks.id
}
```

Azure DNS Private Resolver (Terraform sketch)

```hcl
# Private DNS Resolver with inbound/outbound
resource "azurerm_private_dns_resolver" "main" {
  name                = "dnsr-main"
  resource_group_name = azurerm_resource_group.network.name
  location            = azurerm_resource_group.network.location
  virtual_network_id  = azurerm_virtual_network.hub.id
}

resource "azurerm_private_dns_resolver_inbound_endpoint" "inbound" {
  name                    = "inbound"
  private_dns_resolver_id = azurerm_private_dns_resolver.main.id
  ip_configurations {
    subnet_id = azurerm_subnet.inbound_dns.id
  }
}

resource "azurerm_private_dns_resolver_outbound_endpoint" "outbound" {
  name                    = "outbound"
  private_dns_resolver_id = azurerm_private_dns_resolver.main.id
  subnet_id               = azurerm_subnet.outbound_dns.id
}

# Ruleset with conditional forwarders
resource "azurerm_private_dns_resolver_dns_forwarding_ruleset" "rules" {
  name                = "hybrid-rules"
  resource_group_name = azurerm_resource_group.network.name
  location            = azurerm_resource_group.network.location
  outbound_endpoint_ids = [
    azurerm_private_dns_resolver_outbound_endpoint.outbound.id
  ]
}

# Forward on-prem
resource "azurerm_private_dns_resolver_forwarding_rule" "onprem" {
  name                      = "forward-nhs-local"
  dns_forwarding_ruleset_id = azurerm_private_dns_resolver_dns_forwarding_ruleset.rules.id
  domain_name               = "nhs.local."
  target_dns_servers {
    ip_address = "10.252.154.40"
    port       = 53
  }
}

# Forward AKS private API/PE zones back to Azure recursive
resource "azurerm_private_dns_resolver_forwarding_rule" "aks_privatelink" {
  name                      = "forward-aks-privatelink"
  dns_forwarding_ruleset_id = azurerm_private_dns_resolver_dns_forwarding_ruleset.rules.id
  domain_name               = "privatelink.uksouth.azmk8s.io."
  target_dns_servers {
    ip_address = "168.63.129.16"
    port       = 53
  }
}
```

Actionable checklist you can apply to current deployments

- Public layer
  - Ensure all public FQDNs live only in Cloudflare (no private shadowing). Use DNS-01 via Cloudflare API for ACME where possible.
  - For customer vanity domains, require CNAME to your canonical public names.
- Private layer
  - Standardize on internal TLDs (e.g., m2m.fitfile.internal). Provision in:
    - Azure: Private DNS Zones linked to VNets with AKS.
    - AWS: Route 53 Private Hosted Zones associated to the EKS VPC.
- Hybrid forwarding
  - Azure: deploy Private DNS Resolver with rulesets; forward on-prem domains to on-prem DNS, and forward Azure private zones back to 168.63.129.16.
  - AWS: configure Route 53 Resolver Outbound rules to on-prem; if on-prem needs AWS private names, publish Inbound endpoints and instruct on-prem to forward.
- Kubernetes tuning
  - Deploy NodeLocal DNSCache.
  - Keep CoreDNS forward rules explicit and minimal; monitor CoreDNS metrics.
  - For pods sensitive to DNS latency, consider ndots:2 via dnsConfig; otherwise rely on NodeLocal.
- Security and observability
  - Restrict UDP/TCP 53 egress to known resolvers only.
  - Log DNS traffic (CoreDNS metrics; VPC/Azure NSG/Firewall logs).
  - Keep DNS TTLs modest (30–300s) for agility during incident response.
