---
captured: "2026-03-07T16:56:29+00:00 2026-03-07T16:56:29+00:00"
created: 2026-03-07T16:56:30+00:00
modified: 2026-03-14T11:10:44+00:00
source: "https://claude.ai/chat/627bbe3c-9959-4ffb-a9b2-e8d93ee4779f"
status: "processing"
tags: ["input"]
title: HEAD Azure jumpbox bastion SSH with password authentication
type: "head"
---

## Raw Output / Content

I have a jumpbox in azure private network. { "apiVersion": "2025-04-01", "id": "/subscriptions/454e1659-7f91-4963-b468-668ac7cef106/resourceGroups/rg-mkuh-uks-prd-net/providers/Microsoft.Compute/virtualMachines/vmmkuhjmp01", "name": "vmmkuhjmp01", "type": "microsoft.compute/virtualmachines", "location": "uksouth", "tags": { "Application": "MKUH", "AutoLockExclusion": "true", "CreatedWith": "Terraform", "Criticality": "Tier1", "Department": "SDE", "Description": "The VM to access the private AKS API server", "Environment": "live", "ManagedBy": "FITFILE", "Owner": "Milton Keynes University Hospital", "Status": "live" }, "properties": { "hardwareProfile": { "vmSize": "Standard\_D2s\_v5" }, "provisioningState": "Succeeded", "vmId": "5a2d4ee5-083d-4d9b-8eff-fd0c01eede13", "storageProfile": { "imageReference": { "publisher": "Canonical", "offer": "0001-com-ubuntu-server-jammy", "sku": "22\_04-lts-gen2", "version": "latest", "exactVersion": "22.04.202601310" }, "osDisk": { "osType": "Linux", "name": "vmmkuhjmp01OsDisk", "createOption": "FromImage", "caching": "ReadWrite", "writeAcceleratorEnabled": false, "managedDisk": { "storageAccountType": "Standard\_LRS", "id": "/subscriptions/454e1659-7f91-4963-b468-668ac7cef106/resourceGroups/rg-mkuh-uks-prd-net/providers/Microsoft.Compute/disks/vmmkuhjmp01OsDisk" }, "deleteOption": "Detach", "diskSizeGB": 30 }, "dataDisks": \[\], "diskControllerType": "SCSI" }, "osProfile": { "computerName": "vmmkuhjmp01", "adminUsername": "azadmin", "linuxConfiguration": { "disablePasswordAuthentication": false, "ssh": { "publicKeys": \[\] }, "provisionVMAgent": true, "patchSettings": { "patchMode": "ImageDefault", "assessmentMode": "ImageDefault" } }, "secrets": \[\], "allowExtensionOperations": true, "requireGuestProvisionSignal": true }, "networkProfile": { "networkInterfaces": \[{ "id": "/subscriptions/454e1659-7f91-4963-b468-668ac7cef106/resourceGroups/rg-mkuh-uks-prd-net/providers/Microsoft.Network/networkInterfaces/vmmkuhjmp01Nic", "properties": { "primary": true } } \] }, "diagnosticsProfile": { "bootDiagnostics": { "enabled": true } }, "priority": "Regular", "extensionsTimeBudget": "PT1H30M", "timeCreated": "2026-03-05T16:34:50.3863005Z" }, "resources": \[{ "name": "vmmkuhjmp01CustomScript", "id": "/subscriptions/454e1659-7f91-4963-b468-668ac7cef106/resourceGroups/rg-mkuh-uks-prd-net/providers/Microsoft.Compute/virtualMachines/vmmkuhjmp01/extensions/vmmkuhjmp01CustomScript", "type": "Microsoft.Compute/virtualMachines/extensions", "location": "uksouth", "tags": {}, "properties": { "autoUpgradeMinorVersion": false, "provisioningState": "Succeeded", "enableAutomaticUpgrade": false, "suppressFailures": false, "publisher": "Microsoft.Azure.Extensions", "type": "CustomScript", "typeHandlerVersion": "2.0" } } \], "etag": "\\"2\\"" } Update these commands to create and ssh with password to it 1. Create the Standard Bastion This uses the dedicated `create` command which is much more robust at mapping the networking requirements. This is LCRCA

Verification & SSH Once the creation completes (approx. 5-10 mins), you can immediately run your original command:

---

Here are the updated commands for MKUH. I've substituted everything I can derive from the VM JSON and flagged the VNet/Bastion names you'll need to confirm.

---

What I know for certain from the JSON: subscription, resource group, VM name, admin username.

What I'm inferring from your naming convention: VNet name, Bastion name, Public IP name. Adjust these if MKUH uses a different pattern.

### 1\. Login

_(Same tenant—confirm this is correct for the MKUH subscription.)_

### 2\. Create the Standard Bastion

⚠️ Before running: you need the actual VNet name that `vmmkuhjmp01Nic` is attached to. Quickest way to confirm:

That'll return the full subnet ID, which contains the VNet name. Also confirms the Bastion's `AzureBastionSubnet` needs to exist in that same VNet.

### 3\. SSH with Password

Immediate next action: run the `az network nic show` command above to get the VNet name, then substitute it into commands 2 and 3.

---

az network nic show \\ --ids /subscriptions/454e1659-7f91-4963-b468-668ac7cef106/resourceGroups/rg-mkuh-uks-prd-net/providers/Microsoft.Network/networkInterfaces/vmmkuhjmp01Nic \\ --query 'ipConfigurations\[0\].subnet.id' -o tsv /subscriptions/454e1659-7f91-4963-b468-668ac7cef106/resourceGroups/rg-mkuh-uks-prd-net/providers/Microsoft.Network/virtualNetworks/vnet-mkuh-plat-uks-01/subnets/snet-mkuh-uks-prd-jumpbox

---

The VNet name `vnet-mkuh-plat-uks-01` matches what I guessed—commands 2 and 3 are good to go as written, no changes needed.

Immediate next action: confirm the `AzureBastionSubnet` exists in that VNet:

If that returns a CIDR, you're clear to run the `bastion create`. If it 404s, you'll need to create the subnet first (minimum `/26`).

---

az network vnet subnet show \\ --resource-group rg-mkuh-uks-prd-net \\ --vnet-name vnet-mkuh-plat-uks-01 \\ --name AzureBastionSubnet \\ --query 'addressPrefix' -o tsv (NotFound) Resource /subscriptions/454e1659-7f91-4963-b468-668ac7cef106/resourceGroups/rg-mkuh-uks-prd-net/providers/Microsoft.Network/virtualNetworks/vnet-mkuh-plat-uks-01/subnets/AzureBastionSubnet not found. Code: NotFound Message: Resource /subscriptions/454e1659-7f91-4963-b468-668ac7cef106/resourceGroups/rg-mkuh-uks-prd-net/providers/Microsoft.Network/virtualNetworks/vnet-mkuh-plat-uks-01/subnets/AzureBastionSubnet not found.

---

As expected—need to create it. First, check what address space is in use so we pick a free `/26`:

That'll show you the VNet CIDR(s) and all existing subnet ranges. Once you paste the output, I'll pick a free `/26` for the Bastion subnet.

---

az network vnet show \\ --resource-group rg-mkuh-uks-prd-net \\ --name vnet-mkuh-plat-uks-01 \\ --query '{addressSpace: addressSpace.addressPrefixes, subnets: subnets\[\].{name:name, prefix:addressPrefix}}' -o json { "addressSpace": \["10.104.189.128/26" \], "subnets": \[{ "name": "snet-mkuh-uks-prd-jumpbox", "prefix": "10.104.189.160/29" }, { "name": "snet-mkuh-uks-prd-system", "prefix": "10.104.189.128/28" }, { "name": "snet-mkuh-uks-prd-workflows", "prefix": "10.104.189.144/28" } \] }

---

This is a problem. The entire VNet is a `/26` (64 addresses, `.128`–`.191`), and here's the layout:

| Subnet | Range | Size |
| --- | --- | --- |
| `snet-mkuh-uks-prd-system` | `.128`–`.143` | /28 (16) |
| `snet-mkuh-uks-prd-workflows` | `.144`–`.159` | /28 (16) |
| `snet-mkuh-uks-prd-jumpbox` | `.160`–`.167` | /29 (8) |
| Free | `.168`–`.191` | 24 addresses |

`AzureBastionSubnet` requires a minimum `/26` (64 addresses). You've only got 24 free—and the whole VNet is only 64 total. It won't fit.

### Options

1. Expand the VNet address space—add a second CIDR block (e.g. `10.104.189.192/26`) then create the Bastion subnet within it
2. Create the Bastion in a peered VNet—if there's a hub/connectivity VNet already, the Bastion can live there and still reach this jumpbox via peering

Option 1 is simplest if nothing else occupies `.192/26` in the wider network. To check feasibility, do you have visibility into the broader IP allocation for MKUH, or is there a hub VNet (like `RG-CONNECTIVITY-*`) that might already have a Bastion?

Immediate next action: check if a hub/connectivity VNet already exists for MKUH:

If that only returns the one VNet, also check the connectivity RG if one exists.

---

the jumpbox says it has Associated IPs include all instance-level public IPs, public frontend IPs of load balancers, and NAT gateway public IPs associated to this resource. Up to 100 public IP addresses are shown for each resource type. For other related IPs, such as public IPs that may be accessible from this resource using a user-defined route (UDR) to an NVA, or associated with an Azure Firewall resource, please view the associated resources directly. 51.145.90.43 nat-mkuh-uks-prd-01 (NAT gateway) IPv4 Can I ssh straight to this jmpbox?

---

No—that's a NAT gateway IP, which is outbound-only. It gives the jumpbox a consistent source IP for outgoing traffic, but doesn't accept any inbound connections.

To SSH directly (without Bastion), the NIC would need its own public IP assigned and an NSG rule allowing inbound TCP/22.

### Quick check—does the NIC Have a Direct Public IP?

If that returns empty, there's no direct public IP and your options are:

1. Attach a public IP + NSG rule—quickest path to SSH, but opens an inbound surface (lock the NSG to your IP only)
2. Expand the VNet and add Bastion—more secure, more effort
3. `az serial-console`—if you just need to run a few commands on the box right now

What's your goal right now? If it's just "get onto the jumpbox to run `kubectl` ", option 1 scoped to your IP is the fastest path. If this is production-permanent access, Bastion is the right call long-term.
