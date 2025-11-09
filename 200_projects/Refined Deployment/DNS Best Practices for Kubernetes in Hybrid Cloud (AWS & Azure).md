---
aliases: []
confidence: 
created: 2025-10-16T09:53:19Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/technology/networking/dns]
title: DNS Best Practices for Kubernetes in Hybrid Cloud (AWS & Azure)
type:
uid: 
updated: 
version:
---

## DNS Best Practices for Kubernetes in Hybrid Cloud (AWS & Azure)

This guide consolidates the best practices for managing public and private DNS for Kubernetes workloads on AWS and Azure, particularly in a hybrid environment with on-premises connectivity.

---

### Core Principles

- **Separate Public and Private DNS**:
  - **Public**: Use a dedicated public provider like Cloudflare for user-facing endpoints (`fitfile.net`). This ensures ACME (e.g., Let's Encrypt) certificate challenges work reliably. Avoid using split-horizon for these names.
  - **Private**: Employ internal-only TLDs for service-to-service communication (`m2m.fitfile.internal`). These zones must never be exposed publicly.
- **Prefer Conditional Forwarding**: Route DNS queries for specific internal or on-premises domains (e.g., `*.nhs.local`) to their authoritative resolvers. All other traffic should use standard public resolvers. This is more resilient than forwarding all queries to a single internal point.
- **Avoid Name Collisions**: Do not use the same fully qualified domain name (FQDN) in both public and private zones. If a split-horizon configuration is unavoidable, strictly control which clients see which view and never use those names for ACME DNS-01 validation.
- **Manage DNS as Code (IaC)**: Define all DNS components—zones, records, resolver rules, and endpoints—in **Terraform**. This provides change control, auditability, and repeatability.

---

### Kubernetes DNS Best Practices

#### CoreDNS

- **Minimal Configuration**: Keep the `CoreDNS` ConfigMap lean. Use the `forward` plugin with explicit domain lists for on-premises or cloud-private zones.
- **Monitoring**: Enable metrics and scrape them with Prometheus. Set up alerts in Grafana for `SERVFAIL` spikes, high latency, and resolution timeouts to detect issues proactively.

#### NodeLocal DNSCache

- **Deploy It**: Always deploy **NodeLocal DNSCache**. It acts as a caching agent on each Kubernetes node, reducing latency and mitigating issues related to `ndots` search path magnification. It improves DNS performance and reliability under load.

#### `ndots` Hygiene

- The `ndots` setting in a pod's `dnsConfig` can cause query amplification. If you control the workload, setting `ndots:2` can reduce unnecessary search path queries for latency-sensitive applications. Otherwise, rely on NodeLocal DNSCache to mitigate the impact.

---

### Public DNS & Certificate Management

- **Centralise Public DNS**: Use a single provider (e.g., Cloudflare) as the authority for all public names.
- **ACME Certificate Issuance**:
  - **DNS-01**: Prefer the **DNS-01** challenge type. It uses API integration with your DNS provider to create a TXT record, avoiding the need for inbound HTTP traffic from ACME servers, which can be blocked in restricted networks.
  - **HTTP-01**: If you must use the **HTTP-01** challenge, ensure that firewall policies, proxies, and any SSL inspection are configured to allow inbound traffic to the validation endpoints.
- **Customer Vanity Domains**: Instruct customers to create a **CNAME** record pointing their domain (e.g., `app.customer.com`) to your canonical service name (e.g., `customer-alias.fitfile.com`). This allows you to manage the TLS certificate and backend configuration without needing access to the customer's DNS zone.

---

### Cloud-Specific Implementations

#### AWS (EKS, Route 53)

- **Private DNS**: Use **Route 53 Private Hosted Zones** for internal domains (e.g., `*.m2m.fitfile.internal`), associated with the VPC where the EKS cluster resides.
- **Hybrid Conditional Forwarding**:
  - Use **Route 53 Resolver Endpoints** and **Resolver Rules**.
  - Create **outbound** resolver rules for on-premises domains (`*.nhs.local`) that forward queries to on-premises DNS servers over the VPN or Direct Connect.
  - If on-premises systems need to resolve AWS private names, create an **inbound** endpoint and configure on-premises DNS to forward relevant queries to its IP address.
- **EKS Private Clusters**: If you override the default VPC DNS settings, you **must** ensure that AWS-internal names like `privatelink.<region>.eks.amazonaws.com` can still be resolved. This typically requires a conditional forwarding rule back to the default `AmazonProvidedDNS` resolver.

#### Azure (AKS, Private DNS Zones)

- **Private DNS**: Use **Azure Private DNS Zones** for internal domains. Link these zones to the virtual networks (VNets) where AKS nodes and other resources are deployed.
- **Hybrid Conditional Forwarding**:
  - The preferred solution is the **Azure DNS Private Resolver**.
  - Create an **outbound endpoint** and a **forwarding ruleset**.
  - Add rules to forward on-premises domains (`*.nhs.local`) to on-premises DNS servers (e.g., `10.252.154.40`).
  - Crucially, add a rule to forward Azure-specific private zones (`privatelink.uksouth.azmk8s.io`, etc.) to the Azure recursive resolver at `168.63.129.16`.
  - An **inbound endpoint** allows on-premises systems to resolve names within Azure's private zones.
- **Firewall Rules**: Remember to configure **Azure Firewall** or NSGs to permit DNS traffic and any necessary egress for certificate validation or API calls, especially when SSL inspection is active.

---

### Practical Implementation

#### Reusable Code Snippets

##### 1. CoreDNS Forwarding Rules (Hybrid)

This `Corefile` fragment shows how to conditionally forward specific domains while sending everything else to public resolvers.

YAML

```sh
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

##### 2. AWS Route 53 Resolver Rules (Terraform)

Terraform

```sh
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

# Associate rule to the EKS VPC
resource "aws_route53_resolver_rule_association" "eks_vpc" {
  resolver_rule_id = aws_route53_resolver_rule.onprem.id
  vpc_id           = aws_vpc.eks.id
}
```

##### 3. Azure DNS Private Resolver (Terraform)

Terraform

```sh
# Private DNS Resolver with inbound/outbound endpoints
resource "azurerm_private_dns_resolver" "main" {
  name                = "dnsr-main"
  resource_group_name = azurerm_resource_group.network.name
  location            = azurerm_resource_group.network.location
  virtual_network_id  = azurerm_virtual_network.hub.id
}

resource "azurerm_private_dns_resolver_outbound_endpoint" "outbound" {
  name                    = "outbound"
  private_dns_resolver_id = azurerm_private_dns_resolver.main.id
  subnet_id               = azurerm_subnet.outbound_dns.id
}

# Ruleset with conditional forwarders
resource "azurerm_private_dns_resolver_dns_forwarding_ruleset" "rules" {
  name                  = "hybrid-rules"
  resource_group_name   = azurerm_resource_group.network.name
  location              = azurerm_resource_group.network.location
  outbound_endpoint_ids = [azurerm_private_dns_resolver_outbound_endpoint.outbound.id]
}

# Rule to forward on-prem domains
resource "azurerm_private_dns_resolver_forwarding_rule" "onprem" {
  name                      = "forward-nhs-local"
  dns_forwarding_ruleset_id = azurerm_private_dns_resolver_dns_forwarding_ruleset.rules.id
  domain_name               = "nhs.local."
  target_dns_servers {
    ip_address = "10.252.154.40"
    port       = 53
  }
}

# Rule to forward AKS Private Link zones back to Azure
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

---

#### Actionable Checklist

- **Public Layer**:
  - [ ] Confirm all public FQDNs exist only in Cloudflare.
  - [ ] Use DNS-01 for ACME where possible.
  - [ ] Standardise customer vanity domains via CNAME records.
- **Private Layer**:
  - [ ] Standardise internal TLDs (e.g., `m2m.fitfile.internal`).
  - [ ] In Azure, provision as Private DNS Zones and link to VNets.
  - [ ] In AWS, provision as Route 53 Private Hosted Zones and associate with VPCs.
- **Hybrid Forwarding**:
  - [ ] **Azure**: Deploy Azure DNS Private Resolver with forwarding rules for on-premises and Azure-private zones.
  - [ ] **AWS**: Configure Route 53 Resolver Endpoints and Rules for on-premises forwarding.
- **Kubernetes Tuning**:
  - [ ] Deploy NodeLocal DNSCache to all clusters.
  - [ ] Review CoreDNS configuration to ensure forwarders are explicit and minimal.
  - [ ] Monitor CoreDNS metrics.
- **Security and Observability**:
  - [ ] Restrict UDP/TCP 53 egress to known resolvers via security groups and firewall rules.
  - [ ] Enable DNS query logging (CoreDNS metrics, VPC Flow Logs, Azure Firewall logs).
  - [ ] Set DNS TTLs to a reasonable value (e.g., 30–300 seconds) to balance caching with agility.

---

#### Documentation & Standardisation

- Consolidate Terraform modules for DNS resources in the TFC registry.
- Maintain a central `Configuration Index` in Confluence as the source of truth for DNS architecture.
- Ensure clear ownership of DNS responsibilities is defined as per the `Cloud Network Engineer` role.
  Your thinking was almost right, and your initial statement captured a very real and common failure mode. The mistake in your mental model isn't about how authoritative DNS servers work—you got that part right—but about where the "fallback" logic actually lives.

Let's break down your original thinking and then correct the model.

---

### Your (Mostly Correct) Mental Model

You thought: "If a DNS resolver asks my internal DNS server for a record in a zone that the server is authoritative for (e.g., `fitfile.com`), and that record doesn't exist, the server will reply with `NXDOMAIN` (Non-Existent Domain). The process stops there."

**This is 100% correct for the authoritative server itself.** 🏛️ An authoritative server's job is to give definitive answers for the zones it controls. If it owns `fitfile.com` and you ask for a non-existent record like `random-service.fitfile.com`, it will firmly say "that does not exist," and it will not ask anyone else.

### Where the Model Went Wrong: The Role of the Resolver

Your mistake was assuming the initial query from a client (like a Kubernetes pod) *always* goes directly to that authoritative internal server. In modern setups, it goes to a **smart resolver** first, like `CoreDNS` or a cloud provider's resolver (e.g., Azure DNS Private Resolver).

This resolver acts more like a traffic controller than a simple phone book. It follows a set of rules before deciding where to send the query.

Here is the corrected mental model:

1. **A pod needs to resolve `www.fitfile.com` (a public record).** It sends the query to its local resolver, which is typically `CoreDNS`.
2. **CoreDNS consults its rulebook (`Corefile`).** It checks its rules in order:
   - **Rule 1:** Does the query end in `cluster.local`? No.
   - **Rule 2:** Is it for `nhs.local`? No.
   - **(Missing Rule):** Crucially, in a simple setup, there is no specific rule for `fitfile.com`.
   - **Rule 3 (The Catch-All):** The query matches the final `forward . 1.1.1.1` rule. The `.` means "everything else".

3. **The query is forwarded publicly.** CoreDNS sends the query to `1.1.1.1`, which resolves the public IP address. The internal authoritative server for the *private* `fitfile.com` zone was never even consulted.

This is the "fallback" I was referring to. It's not the authoritative server falling back; it's the **resolver choosing the public forwarder by default** because the query didn't match a more specific, private rule.

---

### The Scenario Where You Were Right (and Why It's Dangerous)

Now, consider a true split-horizon setup where the cloud VNet's DNS setting is pointed at a resolver that *is* authoritative for the private `fitfile.com` zone.

1. A pod needs to resolve `public-cdn.fitfile.com` (a record that *only* exists in the public Cloudflare zone).
2. The query goes to the VNet's configured DNS resolver (e.g., Azure's internal DNS).
3. This resolver sees the `fitfile.com` suffix and says, "Aha! I am authoritative for this zone."
4. It checks its list of **private** records for `public-cdn.fitfile.com`, finds nothing, and returns `NXDOMAIN`.
5. **The process stops.** The pod cannot resolve the address, even though it exists publicly.

This is the exact failure scenario your original statement correctly described. The resolver found a specific authority and stopped, with no "fallback" possible.

### Summary: Clarifying the Mental Model

- **Your old thought:** An `NXDOMAIN` from a private zone authority is a dead end. (Correct, but incomplete).
- **The refined model:** A client's query first hits a **resolver**. This resolver uses conditional logic. A "fallback" to public DNS happens when a query **does not match any specific internal/private forwarding rules**, causing the resolver to use its default catch-all forwarder. The private authoritative server is never even bothered.

The risk you correctly identified occurs when you configure your network in a way that forces **all** queries for a domain to go to the private authoritative server, which has no knowledge of the public-only records. This is why explicit conditional forwarding is the best practice.
