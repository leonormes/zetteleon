---
aliases: ["AKS Troubleshooting", "Azure Kubernetes Service Operations", "Karpenter for AKS"]
created: 2026-01-08T12:00:00Z
last_reviewed: "2026-03-28"
modified: 2026-03-28T17:50:00+00:00
status: evergreen
tags: ["aks", "azure", "kubernetes", "ops", "troubleshooting", "autoscaling"]
title: SoT - Azure Kubernetes Service (AKS) Operations
type: "SoT"
---

## 1. Operational Constraints & Common Errors

Deploying to AKS involves navigating specific Azure resource constraints and configuration requirements.

### 1.1 Initial Access and Permissions
- **Problem**: `az login` hangs or fails, often due to session conflicts or VPN/DNS issues.
- **Solution**:
    - Pre-Flight Checks: Verify VNet/Subnet CIDR blocks and peering upfront.
    - Egress Definition: Confirm if traffic (`0.0.0.0/0`) is forced through a specific firewall/appliance IP.
    - Jumpbox Verification: Use `run_me_first.sh` to validate HTTPS connectivity to ARM and MCR.

### 1.2 Resource Quota Limits (vCore)
- **Error**: "Reached or exceeded the maximum number of zones in subscription…"
- **Solution**: Increase subscription vCore allowance or reduce VM size/count.

### 1.3 Encryption Configuration
- **Error**: Deployment fails if `EncryptionAtHost` is not enabled.
- **Solution**: Enable `EncryptionAtHost` via Azure CLI at the subscription level.

---

## 2. Advanced Autoscaling (Karpenter for AKS)

To manage high-churn workloads (e.g., Workflows) efficiently, we utilize **Karpenter** for just-in-time node provisioning.

### 2.1 Core Resources
- **NodePools**: Define the constraints (instance types, zones) for the nodes Karpenter can launch.
- **NodeClaims**: Represent the request for a specific node to satisfy a pod's requirements.
- **NodeClasses**: Infrastructure-specific configuration (Subnets, Security Groups, AMIs).

### 2.2 Real-Time Visibility
Use the **Headlamp Karpenter Plugin** to monitor scaling events:
- **Scaling Decisions**: Understand *why* Karpenter chose a specific instance type or why a pod is still pending.
- **Pending Pods Dashboard**: View pods with unmet scheduling requirements (e.g., insufficient CPU, missing taints) in a unified view.
- **Live Edits**: Modify NodePool configurations with built-in validation to tune cluster behavior on the fly.

---

## 3. Firewall & Connectivity Requirements

Strict firewall rules are a primary blocker for AKS nodes coming online. Nodes require access to:

### 3.1 Critical Azure Global Endpoints
- `mcr.microsoft.com` (Container Registry)
- `*.cdn.mscr.io`
- `*.blob.core.windows.net`
- `login.microsoftonline.com` (Authentication)
- `management.azure.com`

### 3.2 AKS-Specific Endpoints
- `*.hcp.<region>.azmk8s.io`
- `*.tun.<region>.azmk8s.io` (Ports 9000, 443)
- `*.dp.<region>.azmk8s.io` (Port 443)

---

## 4. Maintenance & Reliability
- **Transient Faults**: Azure is a distributed system; intermittent failures during scaling or patching are expected. Implement **Retry Logic** in all applications.
- **Diagnostic Settings**: Ensure `microsoft.insights` provider is registered to export logs to Log Analytics for post-mortem analysis.

## Related Documentation
- [[SoT - AKS IP Allocation & Subnet Sizing]]
- [[aks-cluster-bootstrap-debug-runbook]]
- [[Introducing Headlamp Plugin for Karpenter - Scaling and Visibility-2]]
