---
aliases: []
confidence: 
created: 2025-09-30T09:24:58Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [project/work/mkuh, topic/technology/networking/dns]
title: Core DNS Components and Environments
type:
uid: 
updated: 
version:
---

This document outlines the comprehensive DNS requirements for the FITFILE deployment, focusing on the interaction between the SDE (hub) and CUH (spoke) environments. It details the authoritative zones, forwarding mechanisms, resolution paths, and critical considerations for ensuring seamless connectivity, service discovery, and certificate management across hybrid cloud infrastructure. A core aspect of this configuration is the implementation of a split-view DNS architecture, leveraging direct, reciprocal DNS zone management and conditional forwarding between Azure-native DNS services and CUH's on-premise infrastructure. This approach has rendered the Azure DNS Private Resolver redundant and it is planned for removal.

## 1. Core DNS Components and Environments

Understanding the roles of each DNS component within the SDE and CUH environments is critical for successful implementation.

### 1.1. SDE Hub (FITFILE)

- **Environment:** AWS EKS cluster.
- **DNS Requirements:** Requires robust DNS configuration for internal cluster communication, external access, and hybrid connectivity.
- **Key Considerations:**
  - Relies on a static outbound IP address (`13.42.119.194`) for firewall whitelisting by the CUH Node.
  - Adherence to FITFILE Firewall Requirements, Proxy Configuration, and TLS/mTLS Requirements.

### 1.2. CUH Spoke (FITFILE - Azure/On-Premise)

- **Environment:** Hybrid infrastructure encompassing an Azure Virtual Network (VNet) and CUH on-premise data centers.
- **DNS Requirements:** Needs comprehensive DNS resolution capabilities for FITFILE hostnames and must align with the overall split-view DNS architecture.
- **Key Considerations:**
  - Integrates both Azure-native services (Azure CoreDNS, Azure Private DNS Zones) and on-premise DNS servers.
  - Requires specific firewall rules to permit inbound DNS queries from the SDE Hub's static IP (`13.42.119.194`).

### 1.3. Azure CoreDNS

- **Role:** DNS service within the Azure Kubernetes Service (AKS) cluster, acting as the internal DNS resolver for the FITFILE Azure VNet.
- **Functionality:**
  - Responsible for internal cluster name resolution (`*.svc.cluster.local`).
  - Authoritative for `*.cuh.local` within the Azure environment.
  - Configured with conditional forwarding to CUH's on-premise DNS servers for `*.fitfile.internal` and `*.cuh.local`.
  - Used by `cert-manager` for internal DNS resolution (IP `10.2.0.10`).

### 1.4. CUH On-Premise DNS Server

- **Role:** Primary DNS infrastructure within the CUH on-premises network.
- **Functionality:**
  - Authoritative for critical FITFILE private zones, including `*.fitfile.internal` and `*.cuh.local`.
  - Configured with conditional forwarders to integrate with Azure DNS services, directing queries for `*.cuh.local` to Azure CoreDNS.
  - This server directly resolves `*.fitfile.internal` and `*.cuh.local` hostnames for on-premise resources.
- **IP Addresses:** Specific IP addresses for the CUH On-Premise DNS Servers need to be identified from the CUH IT team. A known IP for an on-premise SQL server is `10.252.169.98`, which may also function as a DNS server.

### 1.5. Azure Internal DNS Resolver IP (`168.63.129.16`)

- **Role:** Azure's internal DNS resolver service IP.
- **Functionality:** Queried by CUH On-Premise DNS when forwarding queries for domains like `*.fitfile.internal`, facilitating resolution of Azure-hosted private DNS zones.

## 2. FITFILE Domains and Management

FITFILE utilizes a multi-tiered domain strategy managed across different providers, necessitating a clear understanding of domain management and resolution paths.

### 2.1. Public FITFILE Domains

These domains are used for external access and are managed by public DNS providers.

- **`*.eoe.fitfile.net`**
  - **Management:** FITFILE Public DNS Management (Cloudflare).
  - **Purpose:** Public-facing domain for SDE Hub endpoints, accessible externally. Crucial for `cert-manager` DNS-01 challenges for public domain certificates.
- **`fitfile.cloud`**
  - **Management:** Cloudflare.
  - **Purpose:** Public user access to FITFILE applications and administrative dashboards.

### 2.2. Private FITFILE Domains

These domains are used for internal communication and are managed within private DNS zones.

- **`*.fitfile.internal`**
  - **Management:** Primarily managed by CUH On-Premise DNS Server, also utilized by Azure CoreDNS. Authoritative for internal FITFILE M2M communication.
  - **Purpose:** General machine-to-machine (M2M) and NHS trust-specific communication within the FITFILE ecosystem. This domain is used instead of `privatelink.*` domains to bypass Azure's strict hostname validation.
- **`*.cuh.local`**
  - **Management:** CUH On-Premise DNS Server (`10.252.169.98`) is authoritative for this zone. Azure CoreDNS is also configured to be authoritative for this zone within Azure.
  - **Purpose:** Internal resolution for CUH-specific services.
- **`*.privatelink.fitfile.net`**
  - **Management:** Azure Private DNS.
  - **Purpose:** Secure private endpoints for NHS trust integrations. This domain pattern is actively avoided in general configurations due to Azure's strict hostname validation issues, as detailed in Section 5.1.

## 3. SDE Hub (AWS EKS) DNS Infrastructure

The SDE Hub, deployed within an AWS Elastic Kubernetes Service (EKS) cluster, uses a combination of AWS services and Kubernetes-native DNS.

### 3.1. Internal DNS Resolution (within AWS EKS)

- **CoreDNS:** The default DNS server in Kubernetes, deployed within EKS.
  - **Responsibility:** Resolving service names within the cluster (e.g., `service-name.namespace.svc.cluster.local`).
  - **Authoritative Source:** Kubernetes internal service names (`*.svc.cluster.local`).
  - **Configuration:** Managed via a ConfigMap, can be customized for forwarding rules. The internal DNS service IP is typically `10.2.0.10`.
- **AWS Route 53 Private Hosted Zones:** Used for private resources within the AWS VPC to be resolved by EKS workloads.
  - **Functionality:** Provide internal DNS resolution for VPC resources.
  - **Authoritative Source:** Route 53 Private Hosted Zones for private domains hosted within AWS.
  - **Integration:** CoreDNS can forward queries for specific private domains to Route 53 Resolver.

### 3.2. External DNS Resolution (from AWS EKS)

- **AWS Route 53 Public Hosted Zones:** Used for public-facing FITFILE services hosted on the SDE Hub.
  - **Functionality:** Map public hostnames (e.g., `*.eoe.fitfile.net`) to public IP addresses of AWS Load Balancers.
  - **Authoritative Source:** Route 53 Public Hosted Zones for public FITFILE domains.
- **General Internet Resolution:** EKS nodes and CoreDNS forward queries for general internet hostnames to AWS's default DNS resolver or public DNS servers (e.g., `8.8.8.8`, `1.1.1.1`).

### 3.3. SDE Hub's Role in Hybrid DNS Resolution

- **Managing FITFILE Public Domains:** AWS Route 53 Public Hosted Zones manage public DNS records for FITFILE domains.
- **Facilitating External Access:** Publicly accessible FITFILE services are exposed via AWS Load Balancers with DNS records in Route 53.
- **Interfacing with CUH DNS:** EKS CoreDNS can be configured with conditional forwarders to resolve CUH on-premise hostnames by forwarding queries to the CUH On-Premise DNS Server IP (`10.252.169.98`).

## 4. DNS Architecture and Resolution Flows

The deployment employs a sophisticated architecture centered around a Split-View DNS approach with direct forwarding, ensuring domain names resolve to different IP addresses based on network origin.

### 4.1. Split-View DNS Architecture

- **Concept:** Resolves domain names to different IP addresses based on the query's network origin (internal vs. external).
- **Implementation:** Achieved through direct, reciprocal DNS zone management and conditional forwarding between CUH on-premise DNS and Azure CoreDNS. This approach bypasses the need for an Azure DNS Private Resolver for inter-environment resolution.
- **Dependents:** Azure CoreDNS, CUH On-Premise DNS Server, FITFILE Private DNS Management (Azure Private DNS Zones for `*.privatelink.fitfile.net`), FITFILE Public DNS Management (Cloudflare for public domains).

### 4.2. Conditional Forwarding

Conditional forwarding directs DNS queries for specific domains to designated upstream DNS servers, enabling hybrid resolution.

- **CUH On-Premise DNS:** Authoritative for `*.cuh.local` and `*.fitfile.internal`.
  - Forwards queries for `*.cuh.local` to Azure CoreDNS (`10.2.0.10`).
  - Forwards queries for `*.fitfile.internal` to Azure CoreDNS or Azure's internal DNS resolver (`168.63.129.16`).
  - Forwards queries for `*.eoe.fitfile.net` to Azure CoreDNS.
- **Azure CoreDNS:** Authoritative for `*.cuh.local` within Azure.
  - Forwards queries for `*.fitfile.internal` to CUH On-Premise DNS Server (`10.252.169.98` or identified IPs).
  - Forwards queries for `*.cuh.local` to CUH On-Premise DNS Server.
  - Forwards queries for public internet domains to Azure's internal DNS resolver (`168.63.129.16`) or configured upstream public DNS servers.
- **EKS CoreDNS:**
  - Can be configured with conditional forwarders for `*.cuh.local` to point to the CUH On-Premise DNS Server (`10.252.169.98`).
  - Can forward queries for FITFILE internal domains (`*.fitfile.internal`, `*.privatelink.fitfile.net`) to Azure CoreDNS (`10.2.0.10`).

### 4.3. Resolution Flow Examples

- **CUH Spoke to FITFILE Internal Resource (`*.fitfile.internal`):**
  1. CUH on-premise resource queries `relay.cuh-prod-1.fitfile.internal`.
  2. CUH On-Premise DNS forwards the query to Azure CoreDNS (`10.2.0.10`).
  3. Azure CoreDNS resolves the hostname and returns the private IP.
- **FITFILE Internal Resource to CUH Resource (`*.cuh.local`):**
  1. An Azure resource queries `sql.cuh.local`.
  2. Azure CoreDNS forwards the query to CUH On-Premise DNS (`10.252.169.98`).
  3. CUH On-Premise DNS resolves the hostname and returns the IP.
- **CUH Spoke to FITFILE Public Resource (`*.eoe.fitfile.net`):**
  1. CUH on-premise resource queries `app.eoe.fitfile.net`.
  2. CUH On-Premise DNS forwards to Azure CoreDNS.
  3. Azure CoreDNS resolves the public hostname (likely via Cloudflare through its own upstream configuration) and returns the public IP.
- **Internal CUH Resolution (`*.cuh.local`) within Azure VNet:**
  1. An Azure AKS pod queries `internalapp.cuh.local`.
  2. Azure CoreDNS (`10.2.0.10`) forwards the query to CUH On-Premise DNS.
  3. CUH On-Premise DNS resolves the hostname and returns the IP to Azure CoreDNS, then to the pod.

## 5. Network and Security Requirements Impacting DNS

Specific network configurations and security policies impose constraints on DNS operations.

### 5.1. Cert-Manager DNS-01 Challenge and Split-Horizon DNS

- **Problem:** `cert-manager` experiences DNS-01 self-check failures for domains associated with Azure Private DNS Zones (e.g., `*.privatelink.fitfile.net`) due to Azure's internal DNS resolver (`168.63.129.16`) prioritizing linked private zones over public DNS records (Cloudflare). This leads to validation failures because the TXT record for the challenge is not found in the private zone. Azure's hostname validation can also reject domains containing `privatelink.*`, causing errors like `HTTPProxyWrongUrlError`.
- **Resolution Strategy:**
  1. **Force Public Resolvers for `cert-manager`:** Configure `cert-manager` to bypass internal DNS and query public resolvers directly (e.g., `1.1.1.1:53`, `8.8.8.8:53`). This requires configuring `certManager.extraArgs` in its Helm chart with `dns01-recursive-nameservers` and `dns01-recursive-nameservers-only=true`.
  2. **Firewall/Proxy Configuration:** Ensure firewall rules and proxy configurations allow `cert-manager` pods egress access on UDP/TCP port 53 to the specified public DNS servers. This is the documented method for resolving split-horizon DNS issues.
  3. **Avoidance of `*.privatelink.fitfile.net`:** The strategy of using consolidated private domains like `*.fitfile.internal` and managing resolution via direct forwarding circumvents Azure's strict hostname validation issues and the conflict with `cert-manager`'s DNS-01 challenges for these specific domain patterns.

### 5.2. FITFILE Firewall Requirements for DNS Traffic

- **Allow DNS Traffic:** Permit UDP/TCP port 53 traffic between the SDE Hub (AWS EKS) and CUH Node (Azure/On-Premise) environments.
- **IP Whitelisting:** Inbound DNS queries from the SDE Hub's static source IP (`13.42.119.194`) must be allowed on CUH's on-premise firewall.
- **Outbound Traffic Inspection/Bypass:** All outbound traffic from Azure VNETs must be routed through CUH's on-premise proxy/firewall, with DNS traffic inspected or bypassed according to defined policies.

### 5.3. FITFILE Proxy Configuration and DNS Bypass

- **Context:** Non-transparent proxies (e.g., CUH's McAfee Web Proxy at `10.252.142.180`) require authentication and cannot proxy DNS traffic (port 53).
- **DNS Bypass Mechanism:** DNS traffic on port 53 must bypass HTTP proxies.
  - **`NO_PROXY` Settings:** Configure `NO_PROXY` (or `no_proxy`) environment variables to exclude DNS servers and internal network ranges from proxy inspection.
  - **Firewall Rules:** Ensure firewall rules permit port 53 traffic to DNS servers and exempt it from proxy inspection.
- **Essential `NO_PROXY` Entries and Network Ranges:**
  - **SDE Hub (AWS EKS):**
    - Kubernetes Internal: `*.svc`, `*.svc.cluster.local`, `kubernetes.default.svc`
    - Loopback: `localhost`, `127.0.0.1`
    - Azure Metadata Service: `169.254.169.254`
    - Azure CoreDNS IP: `10.2.0.10`
    - Azure Internal DNS Resolver IP: `168.63.129.16`
    - CUH On-Premise DNS Server IPs: (To be identified)
    - CUH Internal Network CIDRs: (To be identified, but include `10.252.142.180` and `10.252.169.98`)
  - **CUH Node (Azure VNet & On-Premise):**
    - CUH On-Premise DNS Server IPs: (To be identified)
    - CUH Internal Network CIDRs: (To be identified, but include `10.252.142.180` and `10.252.169.98`)
    - Azure VNet CIDRs: `10.250.160.0/24`, `10.224.0.0/12`
    - Azure CoreDNS IP: `10.2.0.10`
    - Azure Internal DNS Resolver IP: `168.63.129.16`

### 5.4. FITFILE TLS/mTLS Requirements

- **Relevance to DNS:** Certificate management (e.g., via `cert-manager`) relies on DNS validation. Successful certificate issuance and renewal are directly tied to proper DNS resolution paths, especially involving Cloudflare for public certificates and the correct handling of private zones. The `cert-manager` DNS01 challenge failure underscores the critical need for correct DNS resolution bypass for port 53.

## 6. DNS Record Types

- **A Records:** Map hostnames to IPv4 addresses (e.g., for internal services, proxy IPs).
- **CNAME Records:** Alias hostnames (e.g., for public domains pointing to load balancers).
- **TXT Records:** Primarily used by `cert-manager` for DNS-01 challenges to validate domain ownership.
- **SOA Records:** Indicate authoritative name servers for a zone.

## 7. DNS High Availability and Failover

- **Redundant DNS Servers:** Implement redundant DNS servers on both CUH on-premise and Azure sides.
- **Health Checks:** Configure health checks for DNS forwarders for automatic failover.

## 8. Zone Management Practices

- **Authoritative Zones:**
  - `*.cuh.local`: CUH On-Premise DNS Server (`10.252.169.98`), Azure CoreDNS.
  - `*.fitfile.internal`: CUH On-Premise DNS Server, Azure CoreDNS (forwarding to CUH).
  - `*.privatelink.fitfile.net`: Azure Private DNS.
  - `*.eoe.fitfile.net`: Cloudflare (public resolution).
- **Least Privilege:** Configure DNS servers and zones with the principle of least privilege.
- **Documentation:** Maintain clear documentation of all DNS zones, conditional forwarders, and configurations.
- **Automation:** Utilize Infrastructure as Code (IaC) tools like Terraform for consistent and repeatable management of DNS zones and configurations.

## 9. Recommended Visual Diagrams

To enhance clarity, the following diagrams are recommended:

- **Overall FITFILE Hub-and-Spoke Network Architecture:** Depicting AWS SDE Hub (EKS), Azure VNET (CUH Node), CUH On-Premise network, connections, firewalls, and proxy.
- **Split-View DNS Resolution Flow:** Illustrating queries originating from Azure to CUH On-Premise, CUH On-Premise to Azure, and external access scenarios.
- **CUH On-Premise DNS Server Configuration:** Showing managed zones and conditional forwarders.
- **Azure CoreDNS Configuration:** Illustrating its role as authoritative for `*.cuh.local` and forwarding for `*.fitfile.internal`, and the use of Azure Private DNS Zones.
