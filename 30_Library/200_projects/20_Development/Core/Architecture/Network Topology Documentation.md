---
aliases: []
confidence: 
created: 2025-02-07T12:57:56Z
dependencies:
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:45Z
name: network_topology
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: network_topology
type: architecture_diagram
uid: 
updated: 
version:
---

## Network Topology Documentation

### Cross-Cloud Network Architecture

#### High-Level Overview

```mermaid
graph TB
    subgraph Azure[Azure Cloud]
        AH[Hub VNet]
        AS1[AKS Spoke VNet 1]
        AS2[AKS Spoke VNet 2]
        ACR[Azure Container Registry]
        AKV[Key Vault]
        APE[Private Endpoints]
    end

    subgraph AWS[AWS Cloud]
        ATG[Transit Gateway]
        EKS1[EKS VPC 1]
        EKS2[EKS VPC 2]
        S3[S3 Gateway]
        ECR[ECR Private]
    end

    AH -- Peering --- AS1
    AH -- Peering --- AS2
    AS1 -- Private Endpoint --- ACR
    AS2 -- Private Endpoint --- ACR
    AS1 -- Private Endpoint --- AKV
    AS2 -- Private Endpoint --- AKV

    ATG -- VPC Attachment --- EKS1
    ATG -- VPC Attachment --- EKS2
    EKS1 -- VPC Endpoint --- S3
    EKS2 -- VPC Endpoint --- S3
    EKS1 -- VPC Endpoint --- ECR
    EKS2 -- VPC Endpoint --- ECR

    AH -- Express Route --- ATG
```

#### Private DNS Resolution Flow

```mermaid
sequenceDiagram
    participant Pod as EKS Pod
    participant CoreDNS as CoreDNS
    participant R53 as Route53 Resolver
    participant ER as Express Route
    participant AzDNS as Azure Private DNS
    participant ACR as ACR Private DNS

    Pod->>CoreDNS: Query acr.azurecr.io
    CoreDNS->>R53: Forward query
    R53->>ER: Forward to Azure
    ER->>AzDNS: Resolve in Azure
    AzDNS->>ACR: Query private endpoint
    ACR->>AzDNS: Return private IP
    AzDNS->>ER: Return result
    ER->>R53: Forward response
    R53->>CoreDNS: Return private IP
    CoreDNS->>Pod: Resolved IP
```

### Network Components

#### Azure Components

1. Hub VNet
   - Address space: 10.0.0.0/16
   - Express Route Gateway
   - Azure Firewall
   - DNS Resolvers

2. AKS Spoke VNets
   - Address space: 10.1.0.0/16, 10.2.0.0/16
   - AKS subnets
   - Private endpoint subnets
   - Internal load balancer subnets

3. Private Endpoints
   - ACR private endpoint
   - Key Vault private endpoint
   - Storage private endpoint

#### AWS Components

1. Transit Gateway
   - Cross-cloud routing
   - VPC attachments
   - Route tables

2. EKS VPCs
   - Address space: 172.16.0.0/16, 172.17.0.0/16
   - Private subnets
   - VPC endpoints
   - NAT gateways

3. VPC Endpoints
   - S3 gateway endpoint
   - ECR interface endpoint
   - EKS API endpoint

### Network Security

#### Azure Security Controls

```mermaid
graph LR
    subgraph Azure Security
        AF[Azure Firewall]
        NSG[Network Security Groups]
        PL[Private Link]
        UDR[User Defined Routes]
    end

    AF -- Filter --- Traffic
    NSG -- Control --- Access
    PL -- Secure --- Services
    UDR -- Route --- Traffic
```

#### AWS Security Controls

```mermaid
graph LR
    subgraph AWS Security
        SG[Security Groups]
        NACL[Network ACLs]
        IGW[Internet Gateway]
        NGW[NAT Gateway]
    end

    SG -- Filter --- Traffic
    NACL -- Control --- Access
    IGW -- Block --- Public
    NGW -- Allow --- Egress
```

### Network Paths

#### Container Image Pull Path

```mermaid
sequenceDiagram
    participant EKS as EKS Node
    participant TGW as Transit Gateway
    participant ER as Express Route
    participant PE as Private Endpoint
    participant ACR as Azure Container Registry

    EKS->>TGW: Request image
    TGW->>ER: Route to Azure
    ER->>PE: Forward to endpoint
    PE->>ACR: Pull request
    ACR->>PE: Return image
    PE->>ER: Forward response
    ER->>TGW: Route to AWS
    TGW->>EKS: Deliver image
```

### Network Configuration Guidelines

#### Express Route / Direct Connect Setup

1. Circuit Requirements
   - Bandwidth: 1Gbps minimum
   - BGP enabled
   - Route filters configured

2. BGP Configuration

   ```sh
   Azure AS: 12076
   Customer AS: <assigned>
   AWS AS: <assigned>
   ```

#### Private DNS Configuration

1. Azure Private DNS Zones

   ```sh
   privatelink.azurecr.io
   privatelink.vaultcore.azure.net
   privatelink.blob.core.windows.net
   ```

2. AWS Route53 Private Hosted Zones

   ```sh
   eks.amazonaws.com
   ecr.amazonaws.com
   ```

### Network Validation Checklist

1. Connectivity Validation
2. Security Validation
3. Performance Validation

### Related Documentation
