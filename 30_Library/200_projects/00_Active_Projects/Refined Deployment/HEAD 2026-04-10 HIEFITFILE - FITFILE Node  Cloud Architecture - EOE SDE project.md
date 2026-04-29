---
captured: "2026-04-28T13:28:20+01:00 2026-04-28T13:28:20+01:00"
created: 2026-04-28T12:28:22+00:00
modified: 2026-04-28T12:48:01+00:00
source: "https://fitfile.atlassian.net/wiki/spaces/EOE/pages/2753789953/2026-04-10+HIE+FITFILE+-+FITFILE+Node+Cloud+Architecture"
status: "processing"
tags: ["input"]
title: HEAD 2026-04-10 HIEFITFILE - FITFILE Node  Cloud Architecture - EOE SDE project
type: "head"
---

## Raw Output / Content

## Participants

- FITFILE:,
- HIE EoE: Mark Dines-Allen, Keiran Raines

## Agenda

- Discuss deployment architecture for the FITFILE Node at NUH

## Meeting Recording

Link to recording of the meeting: [NUH FITFILE Node Cloud Prep](https://fathom.video/share/ByQ2mq95p1TfY2Lh1Z17cgAaXxipc7b6)

## Meeting Summary

### Key Takeaways

- Proposed Strategy: Deploy FITFILE's managed Kubernetes stack in AWS, either in a new, transferable NUH account or a sub-account under HIE's ISO-friendly organisation.
- Data Access is the Blocker: The key decision is how NUH's research database will be accessed. The simplest path is for NUH to push data to AWS (e.g., via DMS), avoiding complex on-prem networking.
- Governance: The proposal must be framed to address NUH's governance concerns. FITFILE is ready to complete a DPIA if required by the trust's IG team.
- Simplified Pitch: The proposal will focus on the managed Cloud service, omitting complex on-prem networking options to avoid confusion and accelerate a decision.

### NUH's Cloud Readiness

- Phil Quinlan is open to Cloud but the NUH team lacks the internal technical expertise to support it.
- The team will pitch a managed Kubernetes service where FITFILE handles all deployment (via Terraform), monitoring, and operations.
- This approach simplifies NUH's role to providing only the necessary database connection.

### Deployment Options

- Two AWS account structures were discussed:
	- Option 1 (New Account): A dedicated NUH account.
		- The account must be transferable, allowing NUH to take full ownership later if they develop internal cloud expertise.
		- Option 2 (Sub-Account): A sub-account under HIE's existing ISO-friendly organisation.
		- Provides NUH with immediate comfort by placing the service in a familiar, compliant environment.
				- Billing: HIE would incur costs, which could be offset against the contract value.

### Data Access Strategy

- The primary technical challenge is connecting to NUH's on-prem research database.
- Two main options were identified:
	- On-Premise Connection: The Cloud node connects directly to the database via a VPN or other secure link.
		- Complexity: Requires NUH to implement and manage the network connection.
				- Risk: Potential performance issues with live database access.
		- Data Pipeline to Cloud: NUH pushes data to a Cloud-native store (e.g., AWS RDS, S3) using a service like AWS DMS.
		- Benefit: Simplest, most frictionless path, avoiding all on-prem networking complexity.
				- Unknowns: Requires knowing the data volume and current storage format.

### Governance & Communication

- The proposal must be framed to address NUH's governance rules.
- FITFILE is prepared to complete a DPIA if the Cloud model requires it, even though the original on-prem plan did not.
- Key NUH stakeholders are already involved in the contract, including:
	- Edward Stimpson (Research and Innovation Legal Services Manager)
		- Tom Smith
