---
created: 2026-01-13T07:41:10+00:00
modified: 2026-01-13T09:04:00+00:00
title: "SSoT: Secure Cross-Cloud Communication (AWS EKS & Azure AKS)"
---

%% Processed by Obsidian Agent

Cluster ID: 169

Source Files:

- [[30_Library/200_projects/10_Infrastructure/Networking/Securely Exposing AWS EKS Service to Azure AKS.md]]
- [[99_Archive/Processed_By_Agent/Private EKS Cluster Endpoints.md]]
- [[99_Archive/Processed_By_Agent/Exposing a Private EKS Service (relay) to Other Clusters.md]]
- [[30_Library/200_projects/10_Infrastructure/Networking/Private EKS Cluster Endpoints.md]]
- [[99_Archive/Processed_By_Agent/Remote request config.md]]
- [[_Inbox/Proposed_Merges/SSoT_Secure_Cross-Cloud_Communication_AWS_EKS__Azure_AKS.md]]
- [[99_Archive/Processed_By_Agent/Cross Cloud Networking.md]]
- [[99_Archive/Processed_By_Agent/Securely Exposing AWS EKS Service to Azure AKS.md]]
- [[30_Library/200_projects/10_Infrastructure/Networking/Secure Cross-Cloud Communication Between AWS EKS and Azure AKS for Task Distribution.md]]
- [[99_Archive/Processed_By_Agent/Secure Cross-Cloud Communication Between AWS EKS and Azure AKS for Task Distribution.md]]
- [[99_Archive/Processed_By_Agent/Cross-Cloud Kubernetes Networking Documentation Index.md]]
- [[30_Library/MoC/Cross-Cloud Kubernetes Networking Documentation Index.md]]
- [[30_Library/200_projects/10_Infrastructure/Networking/Remote request config.md]]
- [[30_Library/200_projects/10_Infrastructure/Networking/AWS Gateway API Controller.md]]
- [[30_Library/200_projects/10_Infrastructure/Cloud/Cross Cloud Networking.md]]
- [[30_Library/200_projects/10_Infrastructure/Networking/Exposing a Private EKS Service (relay) to Other Clusters.md]]
%%

# SSoT: Secure Cross-Cloud Communication (AWS EKS & Azure AKS)

## Core Concept

This Single Source of Truth consolidates architectural strategies and implementation details for establishing a secure, private communication channel between a job queue service (`relay`) hosted in a private **AWS EKS** cluster and a worker node service (`bunny`) hosted in an **Azure AKS** cluster. The primary objective is to enable `bunny` to poll `relay` for tasks and return results without exposing traffic to the public internet, satisfying strict security requirements for **mutual authentication (mTLS)**, **fine-grained authorization**, and **minimal attack surface** (e.g., handling sensitive NHS data).

## Details

### 1. Architecture Overview

The cluster of notes proposes three distinct but often complementary approaches to bridge the network gap between AWS and Azure.

| Approach | Connectivity Type | Key Mechanism | Pros | Cons |
|:--- |:--- |:--- |:--- |:--- |
| **A. AWS PrivateLink (Service-Level)** | Unidirectional (Consumer -> Provider) | VPC Endpoint Service + NLB | Traffic stays on AWS backbone (mostly); Isolates specific services; No need to peer entire VPCs. | Requires reachability from Azure (often needs VPN/Direct Connect bridge to reach the interface endpoint). |
| **B. Site-to-Site VPN (Network-Level)** | Bidirectional Tunnel | IPsec Tunnel (VGW <-> VPN Gateway) | Standard industry approach; Encrypted over public internet. | Higher management overhead (routing, BGP); Traffic traverses public internet (though encrypted). |
| **C. Gateway API & VPC Lattice (Modern)** | Application Networking | Kubernetes Gateway API + AWS VPC Lattice | Kubernetes-native config; Advanced routing (HTTPRoute); Abstracted infra. | Newer standard; Requires AWS Gateway API Controller setup; Still requires underlying reachability (VPN). |

### 2. Implementation: AWS Side (`relay`)

#### Network Load Balancer (NLB) & PrivateLink

1. **Deploy `relay`**: Ensure the service runs in private subnets.
2. **Internal NLB**: Provision a Network Load Balancer in the EKS VPC targeting `relay` pods (preferably using IP mode for efficiency).
3. **VPC Endpoint Service**: Create a VPC Endpoint Service associated with the NLB.
4. **Permissions**: Whitelist the Azure account (or specific principals) to allow connection to the Endpoint Service.

#### Kubernetes Gateway API (Alternative/Advanced)

Instead of manually managing the NLB, use the **AWS Gateway API Controller**:

1. **Prerequisites**:
    - Install Gateway API CRDs (manually, as they are not bundled).
    - Create `aws-application-networking-system` namespace.
    - **IAM Setup**: Create an IAM Policy for VPC Lattice permissions and associate it via **IRSA** (IAM Roles for Service Accounts) or **EKS Pod Identity**. _Note: Credential crashes are common here if the Trust Policy doesn't correctly reference the ServiceAccount or OIDC provider._
2. **GatewayClass**: Create a `GatewayClass` of type `amazon-vpc-lattice`.
3. **Gateway**: Define a `Gateway` resource listening on HTTPS (443).
4. **HTTPRoute**: Define an `HTTPRoute` to direct traffic to the `relay` Service. This automatically provisions VPC Lattice Service Networks and Target Groups.

### 3. Implementation: Azure Side (`bunny`)

1. **Connectivity**: Establish the physical bridge to AWS (Site-to-Site VPN or ExpressRoute) if direct private IP reachability is required.
2. **Interface Endpoint**: Create a Private Endpoint in the Azure VNet targeting the AWS VPC Endpoint Service name (if using PrivateLink logic) or route traffic through the VPN Gateway (if using direct VPN routing).
3. **DNS**: Configure Private DNS in Azure to resolve the `relay` service's hostname to the private IP of the interface endpoint or the remote AWS IP.
4. **Outbound Rules**: Configure Network Security Groups (NSGs) to allow `bunny` pods outbound access only to the specific AWS destination CIDR/IP on port 443.

### 4. Security Layer

#### Mutual TLS (mTLS)

_Recommended for verifying identity beyond just network reachability._

- **Protocol**: Two-way verification where `relay` validates `bunny`'s client certificate and vice versa.
- **AWS (Server)**: Store Server Certificate in AWS Secrets Manager. Configure Ingress/Gateway to validate Client Certs using a CA bundle stored in Kubernetes Secrets.
- **Azure (Client)**: Store Client Certificate in Azure Key Vault. Mount certificates to `bunny` pods (e.g., via CSI driver).

#### Authorization (RBAC & Network Policies)

- **Kubernetes RBAC**: Limit the `relay` service's access to the K8s API using a dedicated ServiceAccount.
- **Network Policies (AWS)**: Restrict ingress to `relay` pods to _only_ come from the Ingress Controller/Gateway/NLB subnet.
- **Network Policies (Azure)**: Restrict egress from `bunny` pods to _only_ the specific external IP/DNS of the relay service.

## Conflicts/Nuances

- **Connectivity Paradox**: Some notes suggest connecting "Azure Private Endpoint" directly to "AWS PrivateLink". In reality, cross-cloud PrivateLink usually requires an intermediate layer (like a VPN or specific SaaS configuration) because Azure cannot natively "see" an AWS VPC Endpoint Service ID across the internet without a network bridge or a public abstraction. **Resolution**: Assume a Site-to-Site VPN is the prerequisite foundational layer, _upon which_ PrivateLink or VPC Lattice provides the service isolation.
- **Public vs. Private Definitions**: A "Private" EKS cluster has a private API server. However, if a worker node subnet has a route to an Internet Gateway (to host a public load balancer), that subnet is technically public. **Strict Advice**: Keep `relay` in strictly private subnets (NAT Gateway only) and expose _only_ via the internal NLB/PrivateLink.
- **Gateway API vs. Ingress**: While Nginx Ingress is a standard solution, the notes trend towards the **Gateway API** as the modern "SSoT" preference for this architecture due to its better integration with AWS VPC Lattice and role-oriented design.
