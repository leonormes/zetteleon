---
title: Azure Bastion SSH Troubleshooting
wiki_type: dossier
entity_kind: project
created: 2026-05-29 11:05:35+00:00
modified: 2026-05-29 19:54:32+00:00
tags:
- wiki
- dossier
- azure
- ssh
- bastion
- troubleshooting
sources:
- - 2026-05-29-pieces-azure-bastion-ssh-troubleshooting
- - 2026-05-29-pieces-azure-bastion-1password-ssh
permalink: llmeon/wiki/projects/azure-bastion-ssh-troubleshooting
---

## Summary

Troubleshooting Azure Bastion SSH connectivity issues: `MaxAuthTries` exhaustion from too many SSH keys, `IdentitiesOnly=yes` backfiring with AAD auth type, and missing `--ssh-args` flag in Azure CLI bastion command.

## Key Facts
- **2026-05-29 (09:20)**: For AAD-authenticated Bastion connections with 1Password SSH agent, `ssh-add -D` is ineffective because 1Password manages keys independently of macOS `ssh-agent`. Fix: either bypass the agent with `-o IdentityAgent=none` appended to the `az network bastion ssh` command, or scope which keys 1Password offers via `~/.config/1Password/ssh/agent.toml` — [[raw/2026-05-29-pieces-azure-bastion-1password-ssh]] (Pieces: 9dcbcf77-e097-4506-885a-de3c4bae68b0)


> "Diagnosed Azure Bastion SSH authentication failures across multiple root causes." — [[2026-05-29-pieces-azure-bastion-ssh-troubleshooting]]

## Timeline

- **2026-05-29**: Initial diagnosis — SSH certificate generated but connection failed with "Too many authentication failures"
- **2026-05-29**: Identified root cause — too many keys from 1Password exhausting `MaxAuthTries`
- **2026-05-29**: Applied `IdentitiesOnly=yes` fix but it backfired — excluded AAD certificate auth when using `--auth-type "AAD"`
- **2026-05-29**: Fixed Azure CLI syntax — `--ssh-args` flag doesn't exist; use `--` to pass SSH arguments instead
- **2026-05-29 09:20**: Identified 1Password SSH agent as root cause — `IdentityAgent=none` bypass or `agent.toml` scoping recommended

## Connections

- [[Azure-AKS]] — AKS cluster where bastion provides access
- [[Azure Entra ID IAM → IaC + PIM Migration]] — Related Azure IAM work
- [[HIE AWS Cluster — RDP via Jumpbox]] — Parallel jumpbox access pattern

## Contradictions

- None identified

## Open Questions

- What is the recommended SSH configuration for 1Password users connecting via Azure Bastion with AAD auth?