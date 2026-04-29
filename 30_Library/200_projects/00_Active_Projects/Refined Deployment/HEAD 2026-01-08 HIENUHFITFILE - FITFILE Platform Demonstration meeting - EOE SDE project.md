---
captured: "2026-04-28T13:27:58+01:00 2026-04-28T13:27:58+01:00"
created: 2026-04-28T12:28:00+00:00
modified: 2026-04-28T12:48:01+00:00
source: "https://fitfile.atlassian.net/wiki/spaces/EOE/pages/2570158081/2026-01-08+HIE+NUH+FITFILE+-+FITFILE+Platform+Demonstration+meeting"
status: "processing"
tags: ["input"]
title: HEAD 2026-01-08 HIENUHFITFILE - FITFILE Platform Demonstration meeting - EOE SDE project
type: "head"
---

## Raw Output / Content

## Participants

- FITFILE:,,,
- HIE EoE: Mark Dines-Allen
- HIE East Midlands: Nada Mostafa, Olu Ogunjana, Anna Rutkowska
- NUH: Phil Quinlan, Andy Rae, Tom Smith, Irene Juurlink, Alex Waldren-Glenn, Allison Lloyd
- Apologies: Tim Robinson (HIE East Midlands)

## Agenda

- Demo session of the FITFILE platform

## Meeting Recording

Link to recording of the meeting: [Impromptu Microsoft Teams Meeting](https://fathom.video/share/sHEdJZBxy-UaQLYypYk2iDneyF4y4esk)

## Meeting Summary

Demo FITFILE's federated data platform and discuss its integration with NUH's data environment.

### Key Takeaways

- To accelerate deployment, the initial FITFILE node will use NUH's existing pseudonymised research data (SAT, COSD). This bypasses the Trust's overstretched Digital team, who are focused on a major EPR rollout.
- The long-term plan is to integrate FITFILE earlier in the pipeline, using raw identifiable data. This enables the SDE's crucial cross-Trust patient deduplication, which is not possible with NUH's current pseudonymisation.
- A mandatory third-party vendor assessment is to be completed by FITFILE. DPIA requirements are to be confirmed–may not be necessary for this project.

### FITFILE Platform Overview

- Core Capabilities: Data access, privacy treatment, and linkage.
- Architecture: Decentralised, federated "mesh" of nodes. Each node is deployed within a data provider's (e.g., NUH) environment.
- Privacy Features:
	- Processing pushed to the source to minimise data movement.
		- Supports reversible pseudonymisation and irreversible anonymisation (via k-anonymity, zero-knowledge proof).
		- Compatible with external tokenisation systems (e.g., IQVIA) for cross-SDE federation.
- Deployment Model:
	- A Kubernetes cluster is deployed in an isolated cloud segment within NUH's environment.
		- FITFILE has no direct access to NUH data post-deployment.
		- Updates are pulled via GitOps, limiting FITFILE's access.

### NUH's Data Environment & Governance

Infrastructure:

- Primary data warehouse is fully on-prem (SQL Server).
- Strategic direction is cloud-first for new systems.
- IT estate is managed in-house with formal change management (ITIL, CABs).
- Current Data Flow:
	- Identifiable Data: Resides in the on-prem data warehouse (managed by Irene/Alex).
		- Processing: National Data Opt-Out applied → pseudonymisation → creation of a research data asset.
		- Research Data: The pseudonymised data is then accessible to the R&I team (managed by Tom).
- Governance Challenge: FITFILE's proposed model, which processes identifiable data, creates a new boundary that requires approvals from the overstretched Digital team.

### Implementation Strategy

NUH proposed option:

- Deploy the FITFILE node to connect to NUH's existing pseudonymised research data.
- This aligns with an already-approved internal IG process, making deployment faster and simpler by avoiding the Digital team's current workload.
- This approach prevents the SDE from performing cross-trust patient deduplication, as it relies on NUH's internal pseudonymisation key, not a shared one.

Alternative option:

- Integrate FITFILE earlier in the pipeline to access raw, identifiable data.
- This enables the SDE's crucial cross-trust patient deduplication, which is a key capability for federated analytics.
- This phase will require significant governance work and approvals from NUH's Digital team.

Required Approvals & Processes

- Third-Party Vendor Assessment: A lengthy, mandatory NUH process for all new suppliers.
- DPIA requirements to be confirmed by NUH.
- Data Centre Agreement: A template was provided by Mark Dines-Allen for NUH review.
