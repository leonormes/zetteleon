---
captured: "2026-04-28T13:28:15+01:00 2026-04-28T13:28:15+01:00"
created: 2026-04-28T12:28:17+00:00
modified: 2026-05-26T11:44:30+00:00
source: "https://fitfile.atlassian.net/wiki/spaces/EOE/pages/2669707265/2026-03-03+HIE+NUH+FITFILE+-+FITFILE+Architecture+On+Premise+discussion"
status: "processing"
tags: ["input"]
title: HEAD 2026-03-03 HIENUHFITFILE - FITFILE Architecture  On Premise discussion - EOE SDE project
type: "head"
---

## Raw Output / Content

## 2026-03-03: HIE/NUH/FITFILE - FITFILE Architecture / On Premise Discussion

## Participants

- FITFILE:,,,
- HIE EoE: Mark Dines-Allen
- NUH: John Baines

## Agenda

- Discuss deployment architecture for the FITFILE Node at NUH

## Meeting Recording

Link to recording of the meeting: [FITFILE/NUH re: FITFILE Node deployment in NUH](https://fathom.video/share/VHPkoByiSag4nnkkTqbwu_RKPoJPek-D)

## Meeting Summary

### Key Takeaways

- The team discussed the options for the FITFILE Node deployment at NUH.
- Whilst the preferred route for NUH is an on premise deployment, this would include the management of a complex on premise Kubernetes cluster, which is not currently in FITFILE's remit.
- The existing on premise environment at NUH where the FITFILE Node is anticipated to be deployed, already has agreed IG approvals and SLAs, meaning getting the project up and running will be quick.
- A Hybrid Cloud model was proposed as a potential middle ground. It keeps data on-prem while using NUH's Azure tenant for managed Kubernetes, which is FITFILE's standard.
- A full-Cloud deployment, which is the FITFILE standard for deployment, is least preferred by NUH's team as the Trust would require the project to go through further IG approvals which may take a long time and would involve more resources which are already stretched.
- JB will discuss timelines with Andy Rae (NUH).
- FITFILE will spec the on premise option via NUH's server specification request form and provide a hybrid diagram to inform the final decision.

### Option 1: Fully On-Prem

- NUH's process: NUH can quickly provision a hardened Ubuntu 24.04 VM using a standard server build form.
- Management: NUH handles OS, security hardening, monitoring, and AV. FITFILE manages the application stack.
- Resilience: A single-site deployment is sufficient, as the system is not classified as critical.
- Environment: JB suggested that a test server could be built first for a POC before a production server is deployed.
- FITFILE's requirements: The application is memory-intensive and requires significant resources for its Kubernetes orchestration and computational workflows.

### Option 2: Hybrid Cloud

- Proposed Solution: A hybrid model was presented as a potential compromise.
- Architecture: Application and compute run in NUH's Azure tenant, connected to on-prem data sources via a private network link (ExpressRoute or VPN).
- Benefit: This keeps data on-prem while providing FITFILE with its preferred managed Kubernetes environment.
- Precedent: A similar hybrid solution was successfully deployed at Cambridge University Hospitals (CUH).
