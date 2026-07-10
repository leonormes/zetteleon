---
created: 2026-07-09T00:00:00+00:00
modified: 2026-07-09T00:00:00+00:00
permalink: llmeon/raw/2026-07-09-cuh-dp-jumpbox-bastion-ssh-setup
source: transcript
tags: [raw]
title: 2026-07-09-cuh-dp-jumpbox-bastion-ssh-setup
---

## CUH-DP Jumpbox — Azure Bastion SSH Access Session

Claude Code session (working directory: `/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/CUH-DP`) walking through connecting to the CUH-DP jumpbox VM via Azure Bastion and copying files off it.

### VM details (from `az vm show` / Terraform)

- VM name: `FITFILEJumpbox`
- Resource group: `rg-ff-uks-gp-net`
- Subscription: `7bbc8ae5-1710-48ab-ab83-59b52bd0de1a` ("Testing")
- Full resource ID: `/subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Compute/virtualMachines/FITFILEJumpbox`
- OS: Ubuntu 22.04 LTS Gen2, `Standard_D2ads_v7`, no public IP
- Admin username: `azadmin`
- `osProfile.linuxConfiguration.ssh.publicKeys` is empty and `disablePasswordAuthentication: false` — this VM is configured for password auth, not key auth
- Description tag: "The VM to access the private AKS API server"
- Deployed via Terraform module `app.terraform.io/FITFILE-Platforms/private-infrastructure/azure` v1.3.47, `deployment_key = "cuh-prod-1"`, in `CUH-DP/main.tf`
- `CUH-DP/outputs.tf` exposes a sensitive output `jumpbox_admin_password` sourced from `var.admin_password` (a Terraform Cloud sensitive variable) — retrieved locally via `terraform output -raw jumpbox_admin_password`

### Bastion details (from `az network bastion list -g rg-ff-uks-gp-net`)

- Name: `bas-ff-uks-gp`
- Resource group: `rg-ff-uks-gp-net`
- `EnableTunneling: True`, `EnableIpConnect: True` — Standard SKU with native client support, so `az network bastion ssh` / `az network bastion tunnel` work directly from a local terminal without the portal.

### Connection method 1 — direct SSH via Bastion (password auth)

```bash
az network bastion ssh \
  --name bas-ff-uks-gp \
  --resource-group rg-ff-uks-gp-net \
  --target-resource-id "/subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Compute/virtualMachines/FITFILEJumpbox" \
  --auth-type password \
  --username azadmin \
  -- -o PubkeyAuthentication=no -o PreferredAuthentications=password
```

`-o PubkeyAuthentication=no -o PreferredAuthentications=password` prevents "Too many authentication failures" caused by the local SSH agent (e.g. 1Password) offering keys before the password prompt is reached — same root cause documented in the existing `Azure Bastion SSH Troubleshooting` dossier.

### Connection method 2 — tunnel + local SSH/SCP

```bash
az network bastion tunnel \
  --name bas-ff-uks-gp \
  --resource-group rg-ff-uks-gp-net \
  --target-resource-id "/subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Compute/virtualMachines/FITFILEJumpbox" \
  --resource-port 22 \
  --port 2222 &

ssh -o PubkeyAuthentication=no -o PreferredAuthentications=password azadmin@localhost -p 2222
```

Observed in session: running the `ssh` command immediately after backgrounding the tunnel failed with "Connection refused" — the tunnel needs a few seconds to print "Tunnel is ready, connect on port 2222" before it will accept connections. Retrying after that message appeared succeeded.

Also observed: on retry, `ssh` reported "WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED" for `[localhost]:2222`. This is expected/benign for Bastion tunnels, not a real MITM — the local port `2222` is a generic loopback endpoint that represents whatever VM the tunnel currently targets, so its host key differs from any previously-seen entry in `known_hosts` for that same port (e.g. from a prior tunnel session to a different jumpbox). Fix: `ssh-keygen -R "[localhost]:2222"` to drop the stale entry, or add `-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null` to skip the check entirely (this is what the sibling `NNUH-DP/jumpbox.sh` script in the FITFILE repo does by default).

File copy off the jumpbox, using the same open tunnel (copied `/home/azadmin/terraform` to local):

```bash
scp -r -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
    -o PubkeyAuthentication=no -o PreferredAuthentications=password \
    -P 2222 azadmin@localhost:/home/azadmin/terraform ./terraform
```

### Repo context

No Bastion/jumpbox Terraform exists inside `CUH-DP/` itself — the VM and Bastion are provisioned by the shared `private-infrastructure` TFC module into the shared `rg-ff-uks-gp-net` resource group. Sibling cluster `NNUH-DP` (same repo, `Clusters/eoe/Production/NNUH-DP/`) documents an equivalent setup in `Docs/JUMPBOX_SSH_EXAMPLE.md` and a `jumpbox.sh` helper script, but that cluster was migrated to SSH-key auth (`ssh_public_key` TFC variable, module v1.3.13) rather than the password auth CUH-DP still uses (module v1.3.47, `admin_password` variable, no `ssh_public_key` set).
