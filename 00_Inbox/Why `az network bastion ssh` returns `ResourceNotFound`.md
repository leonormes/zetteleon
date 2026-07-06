---
title: pieces_copilot_message_export_july_6_2026_12_00pm
type: note
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-6-2026-12-00pm
---

*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Monday Jul 6, 2026 - 12:00 PM*
---
## Why `az network bastion ssh` returns `ResourceNotFound`

The bastion host `bas-ff-uks-gp` almost certainly does not exist inside the subscription your CLI session is currently scoped to. Here's the grounded evidence:

### The subscription mismatch

Your terminal output shows you logged in with `--tenant "cuhfoundationtrust.onmicrosoft.com"` and the CLI offered exactly **one** subscription/tenant pair:

```
[1] *  FitFile   709f3d57-b6d7-48c6-8252-6b1c1174a541   3d7d135a-ac7f-46ad-aa55-54639dd31d14
```

But your own past Azure Portal visits to that same bastion resource show it living under a **different subscription** entirely — one labelled "Testing" with subscription ID `7bbc8ae5-1710-48ab-ab83-59b52bd0de1a`, accessed via your `fitfile.com` account rather than `cuhfoundationtrust.onmicrosoft.com`:

> "Resource: bas-ff-uks-gp / Resource Group: rg-ff-uks-gp-net / Location: UK South / **Subscription: Testing** / Subscription ID: **7bbc8ae5-1710-48ab-ab83-59b52bd0de1a**" — captured multiple times, e.g. on [Azure Bastion Resource Overview: bas-ff-uks-gp](https://portal.azure.com/#@cuhfoundationtrust.onmicrosoft.com/resource/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Compute/virtualMachines/FITFILEJumpbox/overview) (29 Apr 2026, 21 May 2026).

That resource group name (`rg-ff-uks-gp-net`) is identical to the one you're targeting in the `FitFile` subscription — which is why the naming looked right in your script even though the resource lives elsewhere. `az network bastion ssh` scoped its lookup to whatever subscription `az account set --subscription 709f3d57-...` left active, and the bastion simply isn't there.

### Corroborating: the bastion is missing from the current subscription's resource list

A more recent capture (12 days ago) of the resource group **inside the `FitFile` subscription** (`709f3d57-...`) lists the contents of `rg-ff-uks-gp-net` — and `bas-ff-uks-gp` is conspicuously absent from the alphabetical listing (`aksbackupvault`, `bkv-ff-uks-gp-01`, `FITFILEJumpboxOsDisk`, …, `dnsrfr-ff-uks-gp-01`…) — see [Azure Resource Manager — FitFile Subscription Resources](https://portal.azure.com/#@cuhfoundationtrust.onmicrosoft.com/resource/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Compute/virtualMachines/FITFILEJumpbox/overview). Alphabetically a bastion named `bas-ff-uks-gp` should sit between those two entries — it doesn't appear, which is consistent with the bastion genuinely not existing under this subscription/tenant.

### A second possible contributing factor: infrastructure change

Your journal entry from 14 days ago (2026‑06‑22) notes a Jira ticket closing out:

> "Status: 2 items resolved since 08:16 run—FTFL-658 (MKUH Terraform SPIKE) and **FTFL-657 (Bastion Direct to AKS)** both moved to Done." (Obsidian: *LLMeon Daily Journal: 2026-06-22*)

"Bastion Direct to AKS" suggests recent work changing how the bastion/jumpbox path to AKS is wired — worth checking whether that ticket describes decommissioning or relocating the bastion resource as part of the change, since its timing lines up with the bastion disappearing from the `FitFile` subscription's resource list.

### What to try next

1. **Re-authenticate against the tenant that actually owns the bastion.** Your historical portal URLs show the bastion was viewed under the `fitfile.com` account, not `cuhfoundationtrust.onmicrosoft.com`. Try:
   ```bash
   az login --tenant <the AAD tenant backing fitfile.com>
   az account set --subscription 7bbc8ae5-1710-48ab-ab83-59b52bd0de1a
   ```
   (I don't have the exact tenant GUID for that fitfile.com login in memory — only the subscription ID above — so confirm it via `az account list` after logging in with the fitfile.com account, or check with whoever manages that tenant.)
2. **Verify the bastion still exists at all** — run `az network bastion list --resource-group rg-ff-uks-gp-net` against subscription `7bbc8ae5-1710-48ab-ab83-59b52bd0de1a` before retrying the SSH command, in case FTFL-657 removed/replaced it.
3. If FTFL-657 did retire the bastion in favor of "direct AKS" connectivity, the jumpbox SSH workflow itself may now be obsolete — worth pulling up that ticket's description in Jira to confirm the new intended access path.

I could not find a tool result that gives the exact tenant GUID for the `fitfile.com` login (only the `Testing` subscription ID `7bbc8ae5-1710-48ab-ab83-59b52bd0de1a`) — if you want, I can dig further into your Azure/Confluence history for that tenant ID specifically.