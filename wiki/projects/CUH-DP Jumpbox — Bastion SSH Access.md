---
title: CUH-DP Jumpbox — Bastion SSH Access
wiki_type: dossier
entity_kind: project
created: 2026-07-09 00:00:00+00:00
modified: 2026-07-09 00:00:00+00:00
tags:
- wiki
- dossier
- azure
- bastion
- ssh
- jumpbox
- cuh-dp
sources:
- raw/2026-07-09-cuh-dp-jumpbox-bastion-ssh-setup
permalink: llmeon/wiki/projects/cuh-dp-jumpbox-bastion-ssh-access
---

## Summary

How to reach the `FITFILEJumpbox` VM (CUH-DP production, the box used to access the private AKS API server) from a local machine via Azure Bastion, and how to copy files off it. The VM has no public IP and uses password auth; Bastion is Standard SKU with native-client tunneling enabled, so `az network bastion ssh` / `tunnel` work directly from a local terminal.

## Key Facts

- VM `FITFILEJumpbox` lives in resource group `rg-ff-uks-gp-net`, subscription `7bbc8ae5-1710-48ab-ab83-59b52bd0de1a`, deployed by the shared `private-infrastructure` TFC module (v1.3.47, `deployment_key = "cuh-prod-1"`) — no Bastion/jumpbox Terraform exists inside the `CUH-DP/` working directory itself.
  > "VM name: `FITFILEJumpbox` ... Deployed via Terraform module `app.terraform.io/FITFILE-Platforms/private-infrastructure/azure` v1.3.47" — [[raw/2026-07-09-cuh-dp-jumpbox-bastion-ssh-setup]]

- Bastion host is `bas-ff-uks-gp` in the same resource group, Standard SKU with `EnableTunneling: True`, so no portal step is required.
  > "Name: `bas-ff-uks-gp` ... `EnableTunneling: True`, `EnableIpConnect: True` — Standard SKU with native client support" — [[raw/2026-07-09-cuh-dp-jumpbox-bastion-ssh-setup]]

- Auth is password-based, not key-based: `osProfile.linuxConfiguration.ssh.publicKeys` is empty and `disablePasswordAuthentication: false`. The password is a Terraform Cloud sensitive variable (`var.admin_password`) exposed as the sensitive output `jumpbox_admin_password`, retrievable with `terraform output -raw jumpbox_admin_password`.
  > "this VM is configured for password auth, not key auth ... retrieved locally via `terraform output -raw jumpbox_admin_password`" — [[raw/2026-07-09-cuh-dp-jumpbox-bastion-ssh-setup]]

- Direct SSH: `az network bastion ssh --name bas-ff-uks-gp --resource-group rg-ff-uks-gp-net --target-resource-id <vm-id> --auth-type password --username azadmin -- -o PubkeyAuthentication=no -o PreferredAuthentications=password`. The `-o PubkeyAuthentication=no` flag is required to stop a local SSH agent (e.g. 1Password) exhausting `MaxAuthTries` before the password prompt is reached.
  > "`-o PubkeyAuthentication=no -o PreferredAuthentications=password` prevents 'Too many authentication failures'" — [[raw/2026-07-09-cuh-dp-jumpbox-bastion-ssh-setup]]

- Tunnel method: `az network bastion tunnel ... --resource-port 22 --port 2222 &` then `ssh azadmin@localhost -p 2222`. The tunnel takes a few seconds to become ready ("Tunnel is ready, connect on port 2222") — an `ssh` fired immediately after backgrounding the tunnel command gets "Connection refused".
  > "running the `ssh` command immediately after backgrounding the tunnel failed with 'Connection refused' — the tunnel needs a few seconds" — [[raw/2026-07-09-cuh-dp-jumpbox-bastion-ssh-setup]]

- A "REMOTE HOST IDENTIFICATION HAS CHANGED" warning on `[localhost]:2222` after retrying is expected/benign for Bastion tunnels (the local port is a generic endpoint whose host key differs per tunnel target), not a real MITM. Fix with `ssh-keygen -R "[localhost]:2222"`, or bypass with `-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null` (as the sibling `NNUH-DP/jumpbox.sh` script does by default).
  > "the local port `2222` is a generic loopback endpoint that represents whatever VM the tunnel currently targets, so its host key differs from any previously-seen entry" — [[raw/2026-07-09-cuh-dp-jumpbox-bastion-ssh-setup]]

- File copy off the jumpbox uses the same open tunnel with `scp -r ... -P 2222 azadmin@localhost:/home/azadmin/terraform ./terraform`.
  > "File copy off the jumpbox, using the same open tunnel" — [[raw/2026-07-09-cuh-dp-jumpbox-bastion-ssh-setup]]

- Sibling cluster `NNUH-DP` (same repo) documents an equivalent jumpbox setup but was migrated to SSH-key auth (`ssh_public_key` TFC variable, module v1.3.13) — CUH-DP has not made this change and remains on password auth with a newer module version (v1.3.47).
  > "that cluster was migrated to SSH-key auth ... rather than the password auth CUH-DP still uses" — [[raw/2026-07-09-cuh-dp-jumpbox-bastion-ssh-setup]]

## Connections

- [[Azure Bastion SSH Troubleshooting]] — general Bastion/SSH auth-failure root causes (1Password agent, `MaxAuthTries`, `--ssh-args` syntax); same `PubkeyAuthentication=no` fix applies here
- [[HIE AWS Cluster — RDP via Jumpbox]] — parallel jumpbox access pattern on a different cloud
- [[CUH-DP AKS Backup — Terraform]] — other CUH-DP production Terraform work in the same working directory
- [[Azure-AKS]] — the private AKS cluster this jumpbox exists to reach

## Contradictions

- None identified.

## Open Questions

- Should CUH-DP be migrated to SSH-key auth to match the `NNUH-DP` pattern (would remove password-retrieval friction and the `PubkeyAuthentication=no` workaround)?
- Where is `var.admin_password` actually set for the CUH-DP Terraform Cloud workspace (which TFC workspace name, and is it also stored in 1Password)?
