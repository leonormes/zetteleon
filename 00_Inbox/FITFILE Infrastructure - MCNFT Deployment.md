---
created: 2026-01-30T15:39:41+00:00
modified: 2026-02-06T14:29:45+00:00
title: FITFILE Infrastructure - MCNFT Deployment
uuid: 20db6ad4-32b0-4933-9c50-facf7b2cc071
---

## 1. Overview

Shortname: MCNFT

This document describes the FITFILE platform deployment within the MCNFT Organisation Perimeter on Azure. The architecture follows a hub-spoke model:

- Hub: MCNFT's existing customer subscription.
- Spoke: FITFILE subscription connected via VNET Peering.

The solution integrates local HR records with pseudonymised NHS long-term conditions data to support the well-being programme. All resources reside within a single Azure Tenant managed by MCNFT to ensure data sovereignty.

---

## 2. Data Scope & Handling

### Data Sources

1. Primary Data: HR data from MCNFT NHS Foundation Trust.
    - Scale: ~11,000 staff records.
    - Source: In-house or commercial database.
    - Update Frequency: One-off extract for the wellbeing programme (no ongoing updates planned).
2. External Data: DSCRO Patient Demographic Survey Data via NWSDE.

### Processing & Linkage

| Feature | Specification |
|:--- |:--- |
| Ingestion | Manual CSV file upload (MCNFT responsible for quality checks). |
| Linkage Fields | Name, Date of Birth (DOB), Postcode (NHS Number is _not_ used). |
| Matching | Deterministic linkage. |
| Privacy | Data is anonymised (used only for linking) via the irreversible FITFILE privacy protocol. |
| Output | CSV files stored in the Azure environment. |
| Retention | Data deleted upon project completion (TBC). |

---

## 3. Network Architecture

### FITFILE Subscription (Spoke)

Operates within its own Azure subscription and VNET, containing three key subnets:

| Subnet | Component | Traffic | Purpose |
|:--- |:--- |:--- |:--- |
| Jumpbox | Jumpbox VM | N/A | Secure administrative access (via Azure Bastion). |
| Workflows | Data Pipeline (AKS) | Inbound | Data ingestion, transformation, and processing workflows. |
| System | Platform (AKS) | Inbound | Core application platform services. |

### Customer Subscription (Hub)

MCNFT's existing environment acts as the hub, hosting:

- Firewall: Controls east-west/north-south traffic.
- Load Balancer: Distributes inbound traffic.
- VPN Access: Secure remote access for MCNFT users.

### Connectivity

- Internal: VNET Peering connects Hub and Spoke while maintaining isolation.
- External (NWSDE): The North West Secure Data Environment sits outside the perimeter. It contains the LCA FITFILE Node and DSCRO data source.
- DNS: Private DNS Zone (`mcnft-prod-1.fitfile.net`) uses split-horizon DNS.

---

## 4. Compute & Storage Resources

### Compute

- AKS Clusters: Two node pools (Data Pipeline & Platform).
- Jumpbox: Dedicated VM for Platform Team administration.

### Storage

- Azure Disks: Encrypted storage for AKS stateful workloads.
- Azure Backup: Disaster recovery for platform data and configurations.

---

## 5. Security & Compliance

### Access Control

- Platform Team: Access via Azure Bastion → Jumpbox.
- Infrastructure: Terraform Service Account (programmatic access).
- App Users: Auth0 handles authentication for Data Analysts/Managers.
- Secrets: Managed via HashiCorp Vault.

### Compliance & Privacy

- Residency: All data remains within MCNFT's Azure Tenant.
- Encryption: Data encrypted at rest (Azure Disks).
- Network: Protected by NSGs (subnet level) and the Hub Firewall.
- Opt-Outs:
    - National Data Opt-Out (NDOO): Mandatory compliance.
    - Staff Opt-Out: Staff with NDOO registered will not have data shared.

---

## 6. Central Services

Managed centrally by FITFILE:

| Service | Provider | Purpose |
|:--- |:--- |:--- |
| Identity | Auth0 | Authentication & Access Management. |
| Secrets | HashiCorp Vault | Secure storage. |
| Observability | Grafana | Monitoring, logging, alerting. |
| DNS/Certs | Cloudflare / ACME | Domain & certificate management. |
| Images | ACR | Node Update Service. |

---

## 7. Open Questions & Action Items

| Item | Context | Status |
|:--- |:--- |:--- |
| DNS Management | How is the split-horizon DNS (`prod-1.fitfile.net`) managed? | ⚠️ OPEN |
| App Access | How will Data Analysts/Managers access the Web Application? | ⚠️ OPEN |
| NWSDE Connectivity | How will the NWSDE Node communicate with the FITFILE platform? | ⚠️ OPEN |
| Data Owner | Confirm if Adam (TBC by Wesam) is primary for data provision. | ⚠️ OPEN |
| Records | Confirm exact record count (linked to 11k staff). | ⚠️ OPEN |
| VNET Peering | [] what do I need to know about the peering ^2026-01-30T19-57-26 | [View in Todoist](todoist://task?id=6fv3wCJ6wgHGRHmM) |
