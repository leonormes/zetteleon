---
created: 2026-01-30T15:39:41+00:00
modified: 2026-02-01T15:09:20+00:00
title: fitfile-mersey-care-infrastructure
uuid: 20db6ad4-32b0-4933-9c50-facf7b2cc071
---

## FITFILE Infrastructure - Mersey Care Deployment

### Overview

This document describes the FITFILE platform deployment within the Mersey Care Organisation Perimeter on Azure. The architecture follows a hub-spoke model with the FITFILE subscription spoke connecting to Mersey Care's existing customer subscription hub.

---

### Architecture Boundaries

#### Mersey Care Organisation Perimeter

The entire deployment resides within Mersey Care's organisational boundary, ensuring data sovereignty and compliance with healthcare data regulations.

#### Azure Tenant

All resources are deployed within a single Azure Tenant owned/managed by Mersey Care.

- what are the ingress
- what are the egress points

---

### Network Architecture

#### FITFILE Subscription Spoke

The FITFILE platform operates within its own Azure subscription spoke containing:

##### Virtual Network (VNET)

- Jumpbox Subnet: Contains the Jumpbox VM for secure administrative access
- Workflows Subnet: Hosts the FITFILE Data Pipeline (AKS-based)
- System Subnet: Hosts the FITFILE Platform (AKS-based)

##### Subnets & Components

| Subnet | Component | Purpose |
|--------|-----------|---------|
| Jumpbox Subnet | Jumpbox VM | Secure administrative access point |
| Workflows Subnet | FITFILE Data Pipeline | Data processing workflows (runs on AKS) |
| System Subnet | FITFILE Platform | Core platform services (runs on AKS) |

#### Existing Customer Subscription - Hub

Mersey Care's existing Azure subscription acts as the hub, containing:

- VNET: Customer's existing virtual network
- Firewall: Central firewall with configurations
- Load Balancer: Handles inbound traffic distribution
- VPN Access: Enables secure remote access for Mersey Care users

#### VNET Peering

The FITFILE Subscription Spoke connects to the Existing Customer Subscription Hub via VNET Peering, enabling secure communication between the two networks while maintaining network isolation.

- [ ] what do I need to know about the peering ^2026-01-30T19-57-26
	- [📱 View in Todoist app](todoist://task?id=6fv3wCJ6wgHGRHmM) (Created: 📝 2026-01-30T19:57)

---

### Compute Resources

#### Azure Kubernetes Node Pools (AKS)

Two AKS node pools are deployed:

1. FITFILE Data Pipeline
   - Location: Workflows Subnet
   - Purpose: Handles data ingestion, transformation, and processing workflows
   - Traffic: Inbound

2. FITFILE Platform
   - Location: System Subnet
   - Purpose: Core application platform services
   - Traffic: Inbound

#### Jumpbox

- Purpose: Secure bastion-style access for platform team administration
- Access Method: Via Azure Bastion
- Subnet: Dedicated Jumpbox subnet

---

### Storage & Backup

#### Azure Backup Services

- Provides backup capabilities for platform data and configurations
- Ensures disaster recovery readiness

#### Azure Disks (Encrypted)

- Encrypted disk storage for persistent data
- Used by AKS workloads for stateful storage requirements

---

### Security Components

#### Azure Bastion

- Provides secure RDP/SSH access to the Jumpbox
- Eliminates need for public IP addresses on VMs
- Used by Platform Team for administrative access

#### Firewall

- Located in the Customer Hub subscription
- Manages traffic between spoke and external networks
- Firewall configurations control east-west and north-south traffic

#### Network Security Groups (NSG)

- Applied to VNET for traffic filtering
- Controls inbound/outbound traffic at subnet level

---

### DNS Configuration

#### Private DNS Zone

- Zone: `prod-1.fitfile.net`
- Type: Split-horizon DNS
- Purpose: Enables private name resolution within the Azure environment

#### Open Question

> How will DNS be managed?
>
> This is flagged as requiring clarification in the architecture.

---

### External Connectivity

#### NWSDE (North West Secure Data Environment)

Located outside the Mersey Care perimeter, NWSDE contains:

| Component | Purpose |
|-----------|---------|
| Firewall | Controls access to/from NWSDE |
| LCA FITFILE Node | Local Custodian Agent node for FITFILE |
| DSCRO Patient Demographic Survey Data | Patient demographic data source |
| Public Static IP | External access endpoint |

##### Open Questions for NWSDE Integration

> How will NWSDE Node access the Node?
>
> Connectivity between NWSDE and the FITFILE platform requires clarification.

#### OPT-OUT Notice

```
[OPT-OUT]
WE WILL NEED NDOO
```

Indicates a requirement for National Data Opt-Out (NDOO) compliance.

---

### User Access Patterns

#### Platform Team

- Access Method: Azure Bastion → Jumpbox
- Purpose: Administrative access to infrastructure and AKS clusters

#### Terraform Service Account

- Purpose: Infrastructure as Code deployments
- Access: Programmatic access to Azure resources

#### Data Manager

- Access Method: Application Requests to FITFILE Platform
- Open Question: How will FITFILE users access the Web Application?

#### Data Analyst

- Access Method:
  - Auth0 login for authentication
  - Application Requests to platform
- Data Source: Mersey Care Staff HR Data (via CSV file upload)
- Open Question: How will Mersey Care users access the Web Application?

---

### FITFILE Central Services

External services managed centrally by FITFILE:

| Service | Provider | Purpose |
|---------|----------|---------|
| DNS & TLS Certificate Management | Cloudflare | Domain and certificate management |
| Observability | Grafana | Monitoring, logging, and alerting |
| TLS Certificates | ACME Issuer | Automated certificate provisioning |
| Authentication | Auth0 | Identity and access management |
| Secrets Management | HashiCorp Vault | Secure secrets storage and management |
| Node Update Service | Azure Container Registry | Container image distribution |

---

### Data Flows

#### Inbound Data

1. Mersey Care Staff HR Data → CSV File Upload → Data Analyst workflow
2. DSCRO Patient Demographic Survey Data → NWSDE → FITFILE Platform

#### Outbound Traffic

- FITFILE Spoke → Outbound → Customer Hub → Firewall → External services

#### Internal Traffic

- Load Balancer distributes traffic to AKS workloads
- VNET Peering enables hub-spoke communication

---

### Authentication & Authorization

#### Auth0

- Primary identity provider
- Handles user authentication for Data Analysts
- Application login flow via Auth0

#### VPN Access

- Enables Mersey Care users to access internal resources
- Connected to the Customer Hub VNET

---

### Open Questions & Action Items

The architecture diagram highlights several items requiring resolution:

| Question | Area | Status |
|----------|------|--------|
| How will DNS be managed? | DNS Configuration | ⚠️ Open |
| How will FITFILE users access the Web Application? | User Access (Data Manager) | ⚠️ Open |
| How will Mersey Care users access the Web Application? | User Access (Data Analyst) | ⚠️ Open |
| How will NWSDE Node access the Node? | External Connectivity | ⚠️ Open |
| NDOO Implementation | Compliance | ⚠️ Required |

---

### Compliance Considerations

- Data Residency: All data remains within Mersey Care's Azure Tenant
- Encryption: Azure Disks are encrypted at rest
- Network Isolation: Hub-spoke model with firewall controls
- National Data Opt-Out (NDOO): Required for patient data handling
- Access Control: Bastion-based admin access, Auth0 for application users

---

### Diagram Legend

| Symbol | Meaning |
|--------|---------|
| Red boxes with questions | Items requiring clarification |
| Dashed lines | Network boundaries / logical groupings |
| Solid lines | Data flows / connections |
| VNET Peering label | Network peering connections |

---

_Document generated from architecture diagram dated 2026-01-30_
