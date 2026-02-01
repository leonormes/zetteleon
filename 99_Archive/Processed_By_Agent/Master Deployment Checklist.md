---
created: 2026-01-29T21:51:22+00:00
modified: 2026-02-01T13:48:54+00:00
title: Master Deployment Checklist
type: head
Reviewed: true
status: archived
deprecated: 2026-02-01
superseded_by: "[[SoT - FitFile Deployment - Implementation Manual]]"
---

# DEPRECATED

> [!warning] Deprecated
> This checklist has been merged into **[[SoT - FitFile Deployment - Implementation Manual]]**. Please use that SoT for the canonical deployment steps.

Your deployment follows a six-phase pipeline with hard dependencies between networking, Central Services, platform deployment, and client-side configuration. The primary friction points identified are:

1. Vault-VSO credential propagation (recently migrated to JWT/OIDC)
2. VNET Peering establishment before platform deployment
3. DNS A-record propagation before Ingress can route traffic
4. Client-side inbound route configuration (external dependency, often blocks)

... (Rest of content preserved for history)