---
aliases: ["FitFile Deployment Architecture"]
confidence: "5/5"
created: 2025-12-21T00:00:00Z
epistemic: "process"
last_reviewed: "2025-12-21"
modified: 2025-12-27T20:40:54+00:00
purpose: "To provide a detailed guide of the architecture and concepts for the FitFile deployment process."
review_interval: "3 months"
see_also: ["[[MOC - FitFile Deployment]]", "[[SoT - FITFILE Platform Deployment]]"]
source_of_truth: []
status: "stable"
tags: ["architecture", "concepts", "ff_deploy"]
title: SoT - FitFile Deployment - Architecture and Concepts
type: "SoT"
uid: 
updated: 
---

## Architecture & Concepts

- **"App of Apps" Pattern:** We do not deploy services manually. We deploy *one* Root Application, which points to the `ffnode` Chart. This chart acts as a manifest, spawning all other services (MongoDB, API, etc.).
    - *Reference:* [[FItfile deployment ArgoCD Style]]
- **Secret Flow:** Secrets are never in Git.
    - Path: `Vault (HCP)` -> `External Secret Operator` -> `K8s Secret` -> `Pod Mount`.
    - *Reference:* [[Vault to Kubernetes Secrets Management Guide]]
- **Private Access:** Direct access to the cluster API is blocked. All `kubectl` commands must tunnel through the Jumpbox or SSM.
- **Customer Management:** Customer management describes the multi-tenant architecture using ArgoCD ApplicationSets.
- **Platform Components:** [[FITFILE Platform Components]] provides an overview of the platform architecture.
- **Database:** [[Mongo Helm Config]]
