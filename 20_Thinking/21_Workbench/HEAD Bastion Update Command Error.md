---
captured: "2026-02-16T09:37:50+00:00 2026-02-16T09:37:50+00:00"
created: 2026-02-16T09:37:57+00:00
modified: 2026-02-27T09:19:50+00:00
source: "https://chatgpt.com/c/698cc82e-6034-838f-96f0-bfa186c8865f"
status: "processing"
tags: ["input"]
title: HEAD Bastion Update Command Error
type: "head"
---

## Raw Output / Content

az network bastion update \\ --name vnet-lca-plat-uks-01-bastion \\ --resource-group rg-lca-uks-prd-net \\ --set sku.name="Standard" \\ --vnet-name vnet-lca-plat-uks-01 \\ --public-ip-address bastion-lca-plat-uks-01PublicIp unrecognized arguments: --vnet-name vnet-lca-plat-uks-01 --public-ip-address bastion-lca-plat-uks-01PublicIp Examples from AI knowledge base: <https://aka.ms/cli>\_ref Read more about the command in reference docs

---

You're hitting this because `az network bastion update` does not accept:

- `--vnet-name`
- `--public-ip-address`

Those parameters are valid for create, not update.

---

## 🔎 Why This Fails

`update` only modifies properties on an existing Bastion resource.

You can change the SKU, but you cannot attach it to a VNet or Public IP during update—those are immutable once created.

---

## ✅ Correct Command to Upgrade SKU to Standard

If your goal is just to upgrade from Basic → Standard:

That's it.

No VNet or Public IP parameters needed.

---

## ⚠️ Important Notes

1. Basic → Standard is supported
2. Downgrade Standard → Basic is NOT supported
3. The Bastion must already have:
	- A `AzureBastionSubnet`
	- A Standard Public IP (required for Standard SKU)

---

## 🔍 If You Get SKU Errors

Check what you currently have:

If the Public IP is Basic, you must:

1. Create a new Standard Public IP
2. Recreate the Bastion (you can't swap the IP on update)

---

## 🧠 Infrastructure-as-Code Note (Since You Use Terraform)

If this is production networking, I strongly recommend:

- Updating this via Terraform
- Importing the existing Bastion into state
- Letting Terraform handle the SKU upgrade

Manual CLI updates can cause drift.

---

If you paste the output of `az network bastion show`, I'll tell you exactly whether this is a simple SKU flip or a rebuild situation.

---

az network bastion update \\ --name vnet-lca-plat-uks-01-bastion \\ --resource-group rg-lca-uks-prd-net \\ --set sku.name=Standard (BastionHostMustHaveAtleastOneHostIpConfiguration) BastionHost /subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/rg-lca-uks-prd-net/providers/Microsoft.Network/bastionHosts/vnet-lca-plat-uks-01-bastion must contain at least 1 IP Configuration. Code: BastionHostMustHaveAtleastOneHostIpConfiguration Message: BastionHost /subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/rg-lca-uks-prd-net/providers/Microsoft.Network/bastionHosts/vnet-lca-plat-uks-01-bastion must contain at least 1 IP Configuration. …/cloudhop on  main!? on ⛵ fitfile-cloud-testing-aks-cluster (testing) on ☁️ FitFileLZ on 🅰 (eu-west-2) at 18:19:46 ❯ az network bastion show \\ --name vnet-lca-plat-uks-01-bastion \\ --resource-group rg-lca-uks-prd-net \\ --query "{sku:sku.name, publicIp:ipConfigurations\[0\].publicIpAddress.id}" { "publicIp": null, "sku": "Developer" }

---

That output tells us exactly what's going on:

- Your Bastion is SKU = Developer
- Developer SKU Bastion is shared infra and does not have `ipConfigurations` / a Public IP the way dedicated Bastion does
- When you try to flip `sku` to `Standard`, Azure validates the _dedicated_ shape and fails because there's no host IP configuration:

`BastionHostMustHaveAtleastOneHostIpConfiguration` ✅

Microsoft's own guidance for upgrading from Bastion Developer says you must first have:

- an `AzureBastionSubnet` (/26 or larger)
- a Standard, Static Public IP, then apply the SKU change.

CLI nuance: `az network bastion update` can set `sku`, but it doesn't let you add the missing `ipConfigurations`, which is why you're stuck in this half-step. The portal flow does the full "shape change" in one go.

Below are two workable paths.

---

## Option A (simplest): Upgrade in the Azure Portal

This matches the official "Upgrade from Bastion Developer" steps.

High level:

1. Create `AzureBastionSubnet` (/26+) in the VNet
2. Create a Standard/Static Public IP
3. Go to Bastion → Configuration → change Tier to Standard → select the Public IP → Apply

---

## Option B (CLI-only): Do it with an ARM/Bicep Deployment (recommended if You want "all CLI")

This works because an ARM/Bicep deployment performs a full PUT of the Bastion resource including `properties.ipConfigurations` (which is what you're missing). The resource schema explicitly includes `ipConfigurations` and `sku`.

### 1) Create the Required Subnet

(Choose an unused /26 in your VNet address space.)

### 2) Create a Standard + Static Public IP

### 3) Deploy an Update that Adds ipConfigurations + Sets SKU Standard

Create a file `bastion-upgrade.bicep`:

Deploy it:

Afterwards, verify:

---

## Why Your Earlier --public-ip-address Attempt Didn't Work

The CLI reference shows `--public-ip-address` is required for non-Developer SKUs (and not required for Developer).

But `az network bastion update` doesn't expose "attach PIP / add ipConfigurations", so you can't complete the upgrade with `update` alone—hence the ARM/Bicep (or portal) route.

---

If you want, paste:

…and I'll suggest a safe `/26` for `AzureBastionSubnet` that won't collide with your current subnets.
