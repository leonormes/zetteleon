---
created: 2026-03-09T11:28:46+00:00
modified: 2026-03-14T11:10:50+00:00
title: wiki-ssh-access-vmmkuhjmp01
---

## SSH Access to Vmmkuhjmp01 (MKUH Jumpbox)

### Overview

`vmmkuhjmp01` is a private jumpbox VM in the MKUH Azure environment, used to access the private AKS API server (`aks-mkuh-uks-prd-01`). The VM sits on a private VNet with no Azure Bastion (due to VNet CIDR constraints) and no public IP by default.

This page documents the process of enabling SSH access via a public IP with NSG lockdown, and the various blockers encountered along the way.

### Environment

| Resource | Value |
|---|---|
| VM Name | `vmmkuhjmp01` |
| Resource Group | `rg-mkuh-uks-prd-net` |
| VNet | `vnet-mkuh-plat-uks-01` |
| Subnet | `snet-mkuh-uks-prd-jumpbox` |
| Private IP | `10.104.189.164` |
| Public IP | `20.0.221.242` (`pip-mkuh-jmp01`, Standard SKU, Static) |
| OS | Ubuntu 22.04 LTS (Jammy) |
| VM Size | `Standard_D2s_v5` |
| Admin User | `azadmin` |
| Location | UK South |

### Access Options Considered

#### 1. Azure Bastion (blocked)

Bastion requires a dedicated `/26` subnet named `AzureBastionSubnet`. The MKUH VNet CIDR does not have sufficient address space to accommodate this without expansion. Not viable without VNet redesign.

#### 2. Public IP + NSG Lockdown (chosen)

Attach a Standard SKU public IP directly to the NIC and restrict inbound SSH via NSG rules scoped to specific source IPs. Fastest path to access.

#### 3. Azure VPN Point-to-Site

A VPN Gateway provides the most secure posture (no public IP on the VM) but adds cost (VPN Gateway SKU) and complexity (certificate management). Better long-term option if compliance requires it.

#### 4. `az ssh vm` With AAD/Entra

The `az ssh vm --local-user` flag does not tunnel through ARM—it still connects via direct SSH to the public IP. This is a common misconception. It is not a workaround for blocked SSH ports.

### Setup Steps

#### Step 1: Create the NIC-level NSG

```bash
az network nsg create \
  --resource-group rg-mkuh-uks-prd-net \
  --name nsg-mkuh-jmp01 \
  --location uksouth \
  --tags Application=MKUH CreatedWith=AzCLI Environment=live
```

#### Step 2: Add the SSH Rule (your IP only)

```bash
az network nsg rule create \
  --resource-group rg-mkuh-uks-prd-net \
  --nsg-name nsg-mkuh-jmp01 \
  --name AllowSSHFromAdmin \
  --priority 100 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --destination-port-ranges 22 443 \
  --source-address-prefixes <YOUR_IP>/32 \
  --destination-address-prefixes '*'
```

#### Step 3: Attach the NSG to the NIC

```bash
az network nic update \
  --resource-group rg-mkuh-uks-prd-net \
  --name vmmkuhjmp01Nic \
  --network-security-group nsg-mkuh-jmp01
```

#### Step 4: Create the Public IP

```bash
az network public-ip create \
  --resource-group rg-mkuh-uks-prd-net \
  --name pip-mkuh-jmp01 \
  --location uksouth \
  --sku Standard \
  --allocation-method Static \
  --tags Application=MKUH CreatedWith=AzCLI Environment=live
```

#### Step 5: Attach the Public IP to the NIC

> Important: The IP config name on this NIC is `Configuration`, not the default `ipconfig1`. Always verify first.

```bash
# Check the IP config name
az network nic ip-config list \
  --resource-group rg-mkuh-uks-prd-net \
  --nic-name vmmkuhjmp01Nic \
  --query "[0].name" -o tsv

# Attach
az network nic ip-config update \
  --resource-group rg-mkuh-uks-prd-net \
  --nic-name vmmkuhjmp01Nic \
  --name Configuration \
  --public-ip-address pip-mkuh-jmp01
```

#### Step 6: Add SSH Rule to the Subnet-level NSG

The subnet `snet-mkuh-uks-prd-jumpbox` has its own NSG (`nsg-mkuh-uks-prd-jumpbox`). Azure evaluates both NIC and subnet NSGs—both must allow the traffic.

```bash
az network nsg rule create \
  --resource-group rg-mkuh-uks-prd-net \
  --nsg-name nsg-mkuh-uks-prd-jumpbox \
  --name AllowSSHFromAdmin \
  --priority 111 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --destination-port-ranges 22 443 \
  --source-address-prefixes <YOUR_IP>/32 \
  --destination-address-prefixes '*'
```

#### Step 7: Connect

```bash
ssh azadmin@20.0.221.242
```

### Azure Cloud Shell as an SSH Client

If your local network blocks outbound SSH (see gotchas below), Azure Cloud Shell provides an in-browser terminal that operates from within Azure's own network.

1. Open `portal.azure.com` → click the Cloud Shell icon (`>_`) in the top nav bar
2. Choose Bash
3. SSH from there: `ssh azadmin@20.0.221.242`

Cloud Shell egress IPs are not stable—they change between sessions. Do not whitelist individual IPs. Use the `AzureCloud` service tag instead:

```bash
az network nsg rule create \
  --resource-group rg-mkuh-uks-prd-net \
  --nsg-name nsg-mkuh-jmp01 \
  --name AllowSSHFromCloudShell \
  --priority 110 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --destination-port-ranges 22 \
  --source-address-prefixes AzureCloud \
  --destination-address-prefixes '*'
```

Use `AzureCloud.UKSouth` to narrow the scope if preferred.

### Gotchas and Lessons Learned

#### 1. Dual NSG Evaluation

Azure evaluates NSGs at both the NIC and subnet level. Traffic must be allowed by both. If your NIC NSG allows SSH but the subnet NSG has a `DenyAllInbound` rule at a lower priority, your connection will silently hang.

Diagnosis:

```bash
az network vnet subnet show \
  --resource-group <RG> \
  --vnet-name <VNET> \
  --name <SUBNET> \
  --query networkSecurityGroup.id -o tsv
```

#### 2. NSG Rule Priority Conflicts

Existing rules may already occupy the priority number you want. The error `SecurityRuleConflict` means a rule with that priority and direction already exists. Just increment the priority number.

#### 3. IP Config Names Are Not Always `ipconfig1`

The Terraform-provisioned NIC on this VM uses `Configuration` as the IP config name. Always verify before running `ip-config update`:

```bash
az network nic ip-config list \
  --resource-group <RG> \
  --nic-name <NIC> \
  --query "[0].name" -o tsv
```

#### 4. Public IP Can Silently Detach

After attaching a public IP via `az network nic ip-config update`, it may show as `associated: null` if the operation didn't stick or something else modified the NIC.

Always verify after attaching:

```bash
az network public-ip show \
  --resource-group <RG> \
  --name <PIP> \
  --query '{ip:ipAddress, associated:ipConfiguration.id}' -o json
```

If `associated` is `null`, the public IP is not wired up and no inbound traffic will reach the VM.

#### 5. Bitdefender DCI Blocks Outbound SSH

Bitdefender DCI (Content Filter + Transparent Proxy) silently kills SSH connections on any port, including 443. The symptom is an SSH connection that hangs at `Connecting to…` with no timeout error for a long period.

Diagnosis: Check macOS → System Settings → Network → VPN & Filters. If Bitdefender DCI is enabled, either temporarily disable it or use an alternative access method (Cloud Shell, mobile hotspot).

#### 6. `az ssh vm --local-user` Does NOT Tunnel through ARM

Despite appearances, `az ssh vm --local-user` establishes a direct SSH connection to the VM's public IP. It does not use the ARM control plane as a relay. If your network blocks SSH, this command will also fail.

#### 7. Cloud Shell Egress IPs Are Ephemeral

Cloud Shell runs on shared Azure infrastructure. The outbound IP can change between sessions and even within a session. Whitelisting individual IPs in NSG rules is fragile. Use the `AzureCloud` service tag.

#### 8. `az vm run-command` Works when SSH Doesn't

The `az vm run-command invoke` command always works because it operates through the ARM control plane over HTTPS. It is non-interactive but useful for diagnostics when SSH is blocked:

```bash
az vm run-command invoke \
  --resource-group rg-mkuh-uks-prd-net \
  --name vmmkuhjmp01 \
  --command-id RunShellScript \
  --scripts "<COMMAND>"
```

#### 9. Zsh Glob Expansion Breaks JMESPath Queries

In zsh, square brackets in `--query` arguments are interpreted as glob patterns. Always single-quote JMESPath queries:

```bash
# Broken in zsh
az vm get-instance-view --query instanceView.statuses[1].displayStatus

# Fixed
az vm get-instance-view --query 'instanceView.statuses[1].displayStatus'
```

#### 10. NAT Gateways Don't Block Inbound to Standard SKU PIPs

The jumpbox subnet has a NAT Gateway (`nat-mkuh-uks-prd-01`). NAT Gateways control outbound traffic only. A Standard SKU public IP on the NIC handles inbound independently. This is not a blocker.

### Useful Diagnostic Commands

```bash
# Check VM power state
az vm get-instance-view \
  --resource-group rg-mkuh-uks-prd-net \
  --name vmmkuhjmp01 \
  --query 'instanceView.statuses[1].displayStatus' -o tsv

# Check if sshd is running inside the VM
az vm run-command invoke \
  --resource-group rg-mkuh-uks-prd-net \
  --name vmmkuhjmp01 \
  --command-id RunShellScript \
  --scripts "ss -tlnp | grep 22"

# Check for subnet-level NSG
az network vnet subnet show \
  --resource-group rg-mkuh-uks-prd-net \
  --vnet-name vnet-mkuh-plat-uks-01 \
  --name snet-mkuh-uks-prd-jumpbox \
  --query networkSecurityGroup.id -o tsv

# Check for route table / UDRs
az network vnet subnet show \
  --resource-group rg-mkuh-uks-prd-net \
  --vnet-name vnet-mkuh-plat-uks-01 \
  --name snet-mkuh-uks-prd-jumpbox \
  --query routeTable.id -o tsv

# Test IP flow via Network Watcher
az network watcher test-ip-flow \
  --direction Inbound \
  --protocol TCP \
  --local 10.104.189.164:22 \
  --remote <SOURCE_IP>:50000 \
  --vm vmmkuhjmp01 \
  --resource-group rg-mkuh-uks-prd-net

# Verify public IP association
az network public-ip show \
  --resource-group rg-mkuh-uks-prd-net \
  --name pip-mkuh-jmp01 \
  --query '{ip:ipAddress, associated:ipConfiguration.id}' -o json
```

### TODO

- [ ] Import the CLI-created resources (NSG, PIP, NSG rules) into Terraform state
- [ ] Evaluate P2S VPN Gateway as a longer-term replacement for the public IP
- [ ] Standardise NSG naming to match existing Terraform conventions
- [ ] Add SSH public key to the VM and disable password authentication
- [ ] Consider auto-shutdown schedule for the jumpbox when not in use
