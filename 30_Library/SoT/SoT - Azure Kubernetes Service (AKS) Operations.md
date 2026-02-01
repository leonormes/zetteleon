---
aliases: ["AKS Troubleshooting", "Azure Kubernetes Service Operations"]
created: 2026-01-08T12:00:00Z
last_reviewed: "2026-01-08"
modified: 2026-02-01T15:08:01+00:00
status: "stable"
tags: ["aks", "azure", "kubernetes", "ops", "troubleshooting"]
title: SoT - Azure Kubernetes Service (AKS) Operations
type: "SoT"
---

## 1. Operational Constraints & Common Errors

Deploying to AKS involves navigating specific Azure resource constraints and configuration requirements.

### 1.1 Initial Access and Permissions

- Problem: `az login` hangs or fails, often due to session conflicts or VPN/DNS issues (e.g., resolving `app.privatelink.fitfile.net`).
- Solution:
    - Pre-Flight Checks: Verify VNet/Subnet CIDR blocks (e.g., `10.250.16.0/24`) and peering upfront.
    - Egress Definition: Confirm if traffic (`0.0.0.0/0`) is forced through a specific firewall/appliance IP.
    - Endpoint Whitelisting: Compile a list of external endpoints (Grafana, Vault, MCR) before deployment.
    - Jumpbox Verification: Script checks for `mcr.microsoft.com` resolution and ACR connectivity.

### 1.2 Resource Quota Limits (vCore)

- Error: "Reached or exceeded the maximum number of zones in subscription…"
- Context: This indicates the subscription's vCore allowance is insufficient for the requested node count/size.
- Solution: Increase the subscription vCore allowance or reduce the requested VM size/count.

### 1.3 Encryption Configuration

- Error: Deployment fails if `EncryptionAtHost` is not enabled on the subscription level.
- Solution: Execute the Azure CLI command to enable `EncryptionAtHost` for the subscription features.

### 1.4 Container Registry (ACR) Access

- Context: Cross-tenant access between AKS and ACR is a frequent failure point in Terraform (`azurerm_kubernetes_cluster`).
- Solution: Ensure the Service Principal or Managed Identity used by AKS has explicit `AcrPull` permissions on the target registry, even across tenants.

### 1.5 Transient Faults

- Nature: Azure is a distributed system; "transient faults" (short, intermittent failures) are a feature, not a bug. They occur during scaling, patching, or hardware shifts.
- Mitigation: Applications must implement Retry Logic. Do not expect 100% uptime for individual components.

---

## 2. Firewall & Connectivity Requirements

Strict firewall rules are a primary blocker for AKS nodes coming online. Nodes require access to:

### 2.1 Critical Azure Global Endpoints

- `mcr.microsoft.com` (Container Registry)
- `*.cdn.mscr.io`
- `*.blob.core.windows.net`
- `login.microsoftonline.com` (Authentication)
- `management.azure.com`

### 2.2 AKS-Specific Endpoints

- `*.hcp.<region>.azmk8s.io`
- `*.tun.<region>.azmk8s.io` (Ports 9000, 443)
- `*.dp.<region>.azmk8s.io` (Port 443)

### 2.3 OS & Time

- NTP servers (for Ubuntu/Azure Linux nodes).

Constraint: Failure to whitelist these results in nodes staying in a `NotReady` state or failing to pull system images.
