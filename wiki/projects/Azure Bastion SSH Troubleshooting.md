---
title: Azure Bastion SSH Troubleshooting
wiki_type: dossier
entity_kind: project
created: 2026-05-29T11:05:35+00:00
modified: 2026-05-29T11:05:35+00:00
tags: [wiki, dossier, azure, ssh, bastion, troubleshooting]
sources: [[2026-05-29-pieces-azure-bastion-ssh-troubleshooting]]
---

## Summary

Troubleshooting Azure Bastion SSH connectivity issues: `MaxAuthTries` exhaustion from too many SSH keys, `IdentitiesOnly=yes` backfiring with AAD auth type, and missing `--ssh-args` flag in Azure CLI bastion command.

## Key Facts

> "Diagnosed Azure Bastion SSH authentication failures across multiple root causes." — [[2026-05-29-pieces-azure-bastion-ssh-troubleshooting]]

## Timeline

- **2026-05-29**: Initial diagnosis — SSH certificate generated but connection failed with "Too many authentication failures"
- **2026-05-29**: Identified root cause — too many keys from 1Password exhausting `MaxAuthTries`
- **2026-05-29**: Applied `IdentitiesOnly=yes` fix but it backfired — excluded AAD certificate auth when using `--auth-type "AAD"`
- **2026-05-29**: Fixed Azure CLI syntax — `--ssh-args` flag doesn't exist; use `--` to pass SSH arguments instead

## Connections

- [[Azure-AKS]] — AKS cluster where bastion provides access
- [[Azure Entra ID IAM → IaC + PIM Migration]] — Related Azure IAM work
- [[HIE AWS Cluster — RDP via Jumpbox]] — Parallel jumpbox access pattern

## Contradictions

- None identified

## Open Questions

- What is the recommended SSH configuration for 1Password users connecting via Azure Bastion with AAD auth?
