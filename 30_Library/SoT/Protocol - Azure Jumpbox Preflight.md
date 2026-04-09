---
aliases: [Azure Jumpbox Preflight Check, Customer One-Pager, run_me_first.sh Guide]
created: 2025-12-09T11:21:13Z
modified: 2026-04-09T08:11:06+00:00
Reviewed: true
status: evergreen
tags: [azure, bastion, ff_deploy, protocol, ssh]
title: Protocol - Azure Jumpbox Preflight
type: Protocol
---

Goal:

Before FITFILE deploys into your Azure subscription, we want to confirm that:

- The jumpbox / bastion host can reach Azure over HTTPS
- The deployment user can log in with the Azure CLI
- The user has the right permissions on the target subscription
- Azure Resource Manager (ARM) is reachable from your network

---

## 1. Establishing Connectivity: Azure Bastion

If the environment lacks a VPN, Azure Bastion is the preferred method for secure administrative access to the jumpbox.

### 1.1 Creating the Bastion Standard

1. Public IP: Create a Standard SKU Static Public IP.
2. Subnet: Create a subnet named exactly `AzureBastionSubnet` (minimum `/26`).
3. Provision:

   ```bash
   az network bastion create \
     --name {vnet-name}-bastion \
     --resource-group {rg-name} \
     --vnet-name {vnet-name} \
     --public-ip-address {pip-name} \
     --sku Standard \
     --enable-tunneling
   ```

### 1.2 Accessing the Jumpbox

```bash
az network bastion ssh \
  --name {bastion-name} \
  --resource-group {rg-name} \
  --target-resource-id {vm-resource-id} \
  --auth-type password \
  --username azadmin
```

---

## 2. Portal-Side Checks (Entra / Azure Admin)

### 2.1 Conditional Access: Test Azure CLI

Use the Conditional Access "What If" tool to ensure the Microsoft Azure CLI (App ID: `04b07795-8ddb-461a-bbee-02f9e1bf7b46`) is not blocked for the deployment user originating from the VNet egress IP.

### 2.2 RBAC: Confirm Deployment User Role

Ensure the user has at least Contributor and User Access Administrator (or a custom role allowing role assignments for Workload Identity).

---

## 3. Jumpbox Troubleshooting

### 3.1 Outbound SSH Hangs

- Bitdefender DCI: macOS "Content Filter + Transparent Proxy" can silently kill SSH connections on ports 22 and 443. Temporarily disable or use Azure Cloud Shell.
- Dual NSG Evaluation: Azure evaluates both NIC and Subnet NSGs. If either blocks port 22/443, the connection will time out.

### 3.2 Public IP Issues

- Silent Detach: Public IPs can silently show as `associated: null` after updates. Verify with:

  ```bash
  az network public-ip show -g {rg} -n {pip} --query '{ip:ipAddress, associated:ipConfiguration.id}'
  ```

- IP Config Names: Standard NICs often use `ipconfig1`, but Terraform-provisioned NICs may use `Configuration`. Verify name before running `ip-config update`.

---

## 4. Preflight Verification (run_me_first.sh)

Run the FITFILE preflight script on the jumpbox to validate ARM API connectivity, subscription visibility, and role membership.

```bash
chmod +x run_me_first.sh
./run_me_first.sh
```

### What the Script Checks

- HTTPS Connectivity: `login.microsoftonline.com` and `management.azure.com`.
- Login Detection: Detects common CA errors (e.g., `53003`).
- Subscription Access: Confirms the specified subscription is visible.

---

## 5. What to Send to FITFILE

1. Full terminal output of `run_me_first.sh`.
2. Results of the `az network private-dns zone list` to confirm split-horizon capability.
3. Confirmation of the NAT Gateway public IP for firewall allow-listing.
