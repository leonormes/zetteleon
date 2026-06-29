---
title: 2026 Infrastructure Map
created: 2026-05-11 16:00:00+00:00
modified: 2026-05-11 16:00:00+00:00
tags:
- wiki
- infrastructure
- fitfile
- dns
- azure
- aks
- backup
sources:
- configs/dns/fitfile-dns-zone-2026-05-08.md
- wiki/projects/Azure AKS Backup — FTFL
- wiki/projects/Terraform IaC Modules
permalink: llmeon/wiki/2026-infrastructure-map
---

## Summary

Consolidated infrastructure map for FitFile systems as of May 2026. Covers DNS zone management (Cloudflare), Azure AKS clusters, backup infrastructure, and deployment environments across production, staging, testing, and sandbox configurations.

## DNS Zone: fitfile.net

**Provider:** Cloudflare  
**Zone ID:** 7c978fe256ced38d73c4ba3f5b11a46f  
**Export Date:** 2026-05-08  
**Total Records:** ~196 (A, CNAME, MX, NS, TXT)

### Key Infrastructure Endpoints

| Subdomain | Type | Content | Proxied | Environment | Purpose |
|-----------|------|---------|---------|-------------|---------|
| `fitfile.net` | A | 35.214.23.206 | No | Production | Root domain |
| `www.fitfile.net` | A | 35.214.23.206 | No | Production | Web redirect |
| `app.fitfile.net` | A | 172.167.50.137 | Yes | Production | Main application |
| `staging.fitfile.net` | A | 172.166.204.72 | Yes | Staging | Staging environment |
| `testing.fitfile.net` | A | 172.167.216.23 | Yes | Testing | Testing cluster |
| `dev-ac.fitfile.net` | A | 51.145.24.103 | Yes | Development | Dev environment |

### ArgoCD Endpoints (Multi-Cluster)

| Subdomain | IP | Environment | Notes |
|-----------|-----|-------------|-------|
| `argocd.fitfile.net` | 172.167.50.137 | Production | Main ArgoCD |
| `argocd-kch-mn2.fitfile.net` | 20.58.55.134 | KCH MN2 | Azure cluster |
| `argocd-kch-mn4.fitfile.net` | 20.117.102.187 | KCH MN4 | Azure cluster |
| `argocd-sh.fitfile.net` | 51.11.43.42 | SH | External cluster |
| `nhs-provider-1-argocd.fitfile.net` | 172.167.30.85 | NHS Provider 1 | EoE data provider |
| `nhs-provider-2-argocd.fitfile.net` | 172.167.42.203 | NHS Provider 2 | EoE data provider |
| `pentest-argocd.fitfile.net` | 20.162.255.100 | Pentest | Security testing |

### Argo Workflows Endpoints

| Subdomain | IP | Environment |
|-----------|-----|-------------|
| `argo-workflows.fitfile.net` | 172.167.50.137 | Production |
| `staging-argo-workflows.fitfile.net` | 172.167.91.135 | Staging |
| `testing-argo-workflows.fitfile.net` | 172.167.216.23 | Testing |
| `nhs-provider-1-argo-workflows.fitfile.net` | 172.167.30.85 | NHS Provider 1 |
| `nhs-provider-2-argo-workflows.fitfile.net` | 172.167.42.203 | NHS Provider 2 |

### Old/Deprecated Infrastructure (Deletion Candidates)

| Subdomain | IP | Notes |
|-----------|-----|-------|
| `old-ac.fitfile.net` | 51.11.2.213 | Old production cluster |
| `old-app.fitfile.net` | 51.11.2.213 | Old production cluster |
| `old-app2.fitfile.net` | 51.11.2.213 | Old production cluster |
| `old-app3.fitfile.net` | 51.11.2.213 | Old production cluster |
| `old-barts.fitfile.net` | 51.11.2.213 | Old production cluster |

### External/Third-Party Integrations

| Subdomain | Type | Target | Purpose |
|-----------|------|--------|---------|
| `email.fitfile.net` | CNAME | email.secureserver.net | GoDaddy email |
| `30519247.fitfile.net` | CNAME | sendgrid.net | SendGrid transactional email |
| `em6282.fitfile.net` | CNAME | u30519247.wl248.sendgrid.net | SendGrid dedicated IP |
| `s1._domainkey.fitfile.net` | CNAME | s1.domainkey.u30519247.wl248.sendgrid.net | DKIM signing |
| `s2._domainkey.fitfile.net` | CNAME | s2.domainkey.u30519247.wl248.sendgrid.net | DKIM signing |
| `fitfile-api-docs.fitfile.net` | CNAME | ssl.redocly.com | API documentation (Redoc) |
| `apples.fitfile.net` | CNAME | ff-eoe-sde-relay-680202258.eu-west-2.elb.amazonaws.com | AWS ELB relay |

### DNS-Only Records (Not Proxied)

| Subdomain | IP | Notes |
|-----------|-----|-------|
| `echo.fitfile.net` | 131.145.24.249 | Echo/test endpoint |
| `cuh-poc-1.fitfile.net` | 217.38.237.183 | CUH PoC |
| `cuh-poc-1.privatelink.fitfile.net` | 217.38.237.183 | Private link |
| `lca-prd-2.fitfile.net` | 4.158.64.255 | LCA production |
| `mkuh-prd-4.fitfile.net` | 51.11.146.209 | MKUH production |
| `nnuh-prod-1.fitfile.net` | 195.171.151.154 | NNUH production |
| `secrets.fitfile.net` | 51.132.47.130 | Secrets management |
| `sonar.fitfile.net` | 51.11.153.23 | SonarQube |
| `sonarqube.fitfile.net` | 51.11.153.23 | SonarQube (alias) |
| `vpn.fitfile.net` | 52.56.250.251 | VPN endpoint |
| `vpntesting.fitfile.net` | 18.134.26.213 | VPN testing |

### ACME Challenge Records

Multiple `_acme-challenge.*` TXT records present for Let's Encrypt certificate validation across:
- Production: `app`, `app2`, `app3`, `argocd`, `argo-workflows`, `barts`
- Testing: `ff-test-a`, `ff-test-b`, `ff-test-c`
- Staging: `staging-argocd`, `staging-argo-workflows`, `storybook`
- Pentest: `pentest`, `pentest-argocd`, `pentest-argo-workflows`

**Note:** Some ACME challenges may be stale if parent hostnames no longer have A/CNAME records.

### Email Security Records

| Record | Type | Value | Status |
|--------|------|-------|--------|
| `fitfile.net` | MX | 0 smtp.secureserver.net | ✅ Present |
| `fitfile.net` | MX | 10 mailstore1.secureserver.net | ✅ Present |
| `cf2024-1._domainkey.fitfile.net` | TXT | DKIM v=DKIM1; k=rsa; p=... | ✅ Present |
| `fitfile.net` | TXT | MS=ms72564386 | Microsoft verification |
| `_dmarc.fitfile.net` | TXT | *(not found)* | ⚠️ **MISSING** |
| `fitfile.net` | TXT | *(SPF not found)* | ⚠️ **MISSING** |

**Security Gap:** No SPF or DMARC TXT records detected. Recommend adding:
```
fitfile.net.  IN  TXT  "v=spf1 include:secureserver.net include:sendgrid.net -all"
_dmarc.fitfile.net.  IN  TXT  "v=DMARC1; p=quarantine; rua=mailto:dmarc@fitfile.net"
```

### Delegated Sub-Zones

| Subdomain | Nameservers | Purpose |
|-----------|-------------|---------|
| `eoe.relay.fitfile.net` | ns-598.awsdns-10.net, ns-1072.awsdns-06.org, ns-2013.awsdns-59.co.uk, ns-388.awsdns-48.com | EoE relay delegation (AWS Route53) |

## Azure AKS Infrastructure

### Production Cluster

| Property | Value |
|----------|-------|
| **Cluster Name** | `aks-ff-uks-gp-1` |
| **Location** | UK South |
| **Resource Group** | `fitfile-cloud-prod-1-rg` |
| **VNet** | `aks-vnet-25797305` (10.224.0.0/12) |
| **Backup Vault** | `aks-ff-uks-gp-1-backup` |
| **Storage Account** | `stffuksgp1backup` |
| **Backup Policy** | `dailyaksbackups` (daily 2:00 AM UTC, 14-day retention) |
| **Protected Namespaces** | `barts`, `ff-a`, `ff-b`, `ff-c`, `spicedb`, `thehyve`, `thehyve-cuh`, `thehyve-mkuh` |
| **Jira Tickets** | FTFL-596 (config), FTFL-599 (runbook), FTFL-615 (IaC) |

### Backup Infrastructure Components

1. **Storage Account:** `stffuksgp1backup` with container `aks-backups`
2. **Private Endpoint Subnet:** `snet-ff-uks-gp-pe` (10.0.0.96/27)
3. **Private Endpoint:** `pe-stffuksgp1backup-blob`
4. **Private DNS Zone:** `privatelink.blob.core.windows.net` with VNet link
5. **Backup Vault:** `aksbackupvault` in `pentest-1-backup-rg`
6. **Snapshot RG:** `pentest-1-backup-snapshots-rg`
7. **AKS Extension:** `azure-aks-backup` (Succeeded)
8. **Policy:** `dailyaksbackups`
9. **Trusted Access Binding:** `azbkup-trust` with `backup-operator` role

### Staging/Testing Clusters

| Cluster | Resource Group | Status | Backup Status |
|---------|---------------|--------|---------------|
| `fitfile-cloud-staging-aks-cluster` | `fitfile-cloud-staging-rg` | Running | Extension Succeeded ✓ |
| `fitfile-cloud-testing-aks-cluster` | `fitfile-cloud-testing-rg` | Running | None (no backup extension) |

### EoE Data Provider Deployments

| Provider | ArgoCD URL | Argo Workflows URL | Status |
|----------|-----------|-------------------|--------|
| NHS Provider 1 | nhs-provider-1-argocd.fitfile.net (172.167.30.85) | nhs-provider-1-argo-workflows.fitfile.net | Deployed |
| NHS Provider 2 | nhs-provider-2-argocd.fitfile.net (172.167.42.203) | nhs-provider-2-argo-workflows.fitfile.net | Deployed |

## Terraform IaC Status

### Modules in Development

**Repository:** `terraform-azure-aks-backup` (GitLab)  
**Target Version:** v1.2.0

**Coverage:**
- ✅ Hardened storage account with private endpoint
- ✅ Private DNS zone with VNet link
- ✅ Backup vault configuration
- ✅ AKS backup extension
- ✅ Backup policy (daily, 14-day retention)
- ✅ Trusted access role binding (`backup-operator`)
- ⚠️ RBAC role assignments (Vault MSI, AKS MSI → snapshot RG) - needs refinement

**Known Gaps:**
1. Snapshot resource group is pre-existing (not created by module)
2. Extension config settings not visible in state
3. Immutability setting discrepancy (plan shows Disabled, portal shows Enabled)
4. Import scenario required for existing resources (backup instance GUID matches manual creation)

### Jira Tracking

| Ticket | Title | Status |
|--------|-------|--------|
| FTFL-596 | Backup Config | In Progress |
| FTFL-599 | Restore Runbook | In Progress |
| FTFL-615 | IaC / Terraform Modules | In Progress |
| FTFL-638 | Grafana/Alloy Monitoring | Recent fixes (log labeling) |

## Security Observations

### DNS Security Gaps

1. **Missing SPF Record:** No `v=spf1` TXT record for fitfile.net
2. **Missing DMARC Record:** No `_dmarc.fitfile.net` TXT record
3. **IP Exposure:** Several DNS-only records share IPs with proxied records (potential origin exposure)

### IP Sharing Analysis

| Shared IP | Proxied Records | DNS-Only Records | Risk |
|-----------|-----------------|------------------|------|
| 51.11.2.213 | old-ac, old-app, old-app2, old-app3, old-barts, prod-mongoweb, oncology-demo | *(none)* | Low (all deprecated) |
| 51.11.153.23 | *(none)* | sonar, sonarqube | Medium (direct IP exposure) |
| 217.38.237.183 | *(none)* | cuh-poc-1, cuh-poc-1.privatelink | Medium (direct IP exposure) |

## Connections

- [[wiki/projects/Azure AKS Backup — FTFL]] (parent initiative)
- [[wiki/projects/Terraform IaC Modules]] (IaC development)
- [[wiki/projects/NNU Azure Backup]] (deployment target)
- [[wiki/projects/MKUH Azure Backup]] (deployment target)
- [[wiki/projects/Azure Backup Restore Runbook]] (operational documentation)
- [[wiki/projects/Grafana Alloy Monitoring — FTFL-638]] (monitoring improvements)
- [[configs/dns/fitfile-dns-zone-2026-05-08.md]] (DNS zone source)

## Open Questions

1. Should deprecated `old-*` records be removed from DNS now or after migration confirmation?
2. What is the RTO/RPO target for the AKS backup policy?
3. Will Terraform modules support both private and public endpoint configurations?
4. How should the module handle snapshot resource group creation — as part of the module or external dependency?
5. Are there legitimate uses for the DNS-only records that share IPs with proxied records?

## Next Actions

1. **DNS Security:** Add SPF and DMARC TXT records
2. **DNS Cleanup:** Review and remove `old-*` records after stakeholder confirmation
3. **IaC:** Complete Terraform module for AKS backup (FTFL-615)
4. **Backup Extension:** Deploy backup extension to testing cluster (currently missing)
5. **Monitoring:** Continue Grafana/Alloy log labeling improvements (FTFL-638)