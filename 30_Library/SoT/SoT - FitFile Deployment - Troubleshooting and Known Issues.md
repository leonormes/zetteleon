---
aliases: [FitFile Deployment Troubleshooting]
confidence: 5/5
created: 2025-12-21T12:00:00Z
epistemic: process
last_reviewed: 2025-12-21
modified: 2025-12-21T14:57:22Z
purpose: To provide a detailed guide of troubleshooting and known issues for the FitFile deployment process.
review_interval: 3 months
see_also: ["[[MOC - FitFile Deployment]]", "[[SoT - FITFILE Platform Deployment]]"]
source_of_truth: true
status: stable
tags: [ff_deploy, known_issues, troubleshooting]
title: SoT - FitFile Deployment - Troubleshooting and Known Issues
type: SoT
uid: 
updated: 
version: 1.0
---

## Troubleshooting & Known Issues

- **"ArgoCD Sync Failed":** Check `VaultAuth` status. Often caused by missing Vault secrets in Phase 1.
- **"Image Pull Error":** Check ACR/ECR credentials in the `imagePullSecrets`.
- **"Terraform State Lock":** Check TFC console for hanging runs.
- **Azure Errors:** [[Errors Encountered During Azure Deployment]]
- **Azure Backup Errors:** [[SoT - Azure Backup and Restore]]
- **General Fixes:** [[Fitfile deployment fixes]]
- **Connectivity:** [[from the linux jumpbox inside the vpc how do I deb]]
- **Node.js:** [[Why Node Not Work]]
