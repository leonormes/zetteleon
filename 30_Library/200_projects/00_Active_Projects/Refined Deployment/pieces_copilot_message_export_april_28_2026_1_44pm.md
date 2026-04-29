---
created: 2026-04-28T12:44:55+00:00
modified: 2026-04-28T12:48:01+00:00
title: pieces_copilot_message_export_april_28_2026_1_44pm
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Tuesday Apr 28, 2026 - 1:44 PM_
---

Below is a concise Hasse-style dependency hierarchy (poset) for the NUH work you're driving. I split it into the two active tracks your notes cover: A) Azure Backups for NNUH/MKUH, and B) NUH Hybrid Node deployment. Arrows imply "must precede." Parallel items on the same level have no order between them.

A) Azure Backups (NNUH/MKUH)—FTFL-596 track

Maximal deliverables: "Backups running for NNUH (FTFL-597) and MKUH (FTFL-598) with private networking locked down"

Level 0—Pre-conditions / governance

- Confirm customer IAM for Terraform SP (Contributor + Data Protection roles) and provider registration → [FTFL-605](https://fitfile.atlassian.net/browse/FTFL-605)
  - Note: Microsoft.DataProtection was observed Registered at 9:41 AM; SP role checks hit Entra 401 and need customer confirmation at 11:21 AM
- Confirm backup scope inputs from The Hyve (exact OMOP namespaces) and cost approval for OMOP snapshot size (staging ~1.2 TB)

Level 1—Network foundations (private path prerequisites)

- Allocate CIDR and create Private Endpoints subnet in AKS VNet → [FTFL-615](https://fitfile.atlassian.net/browse/FTFL-615)
- Create Private DNS zone (privatelink.blob.core.windows.net) and VNet link (same VNet as PE)

Level 2—Storage hardening (depends on Level 1)

- Create Storage Account Private Endpoint (blob) bound to the new subnet
- Lock storage: publicNetworkAccess = Disabled; defaultAction = Deny; bypass = []

Level 3—Backup substrate (can be done in parallel with Level 1 once IAM is confirmed)

- Ensure Backup Vault exists and AKS backup extension is healthy (policy host) for target clusters
  - Prod/staging cadence confirmed as daily 9:00 PM UTC, P14D retention (audited between 10:54–11:22 AM)

Level 4—Policy and scope (depends on Level 0 + Level 3)

- Update backup scope to include OMOP namespaces (immediate prod fix was to append includedNamespaces)
  - Finding at 11:21 AM: thehyve, thehyve-cuh, thehyve-mkuh were missing; labelSelectors not in use

Level 5—Apply per customer (depends on Levels 1–4)

- Apply NNUH module with final schedule/scope/PE settings → [FTFL-597](https://fitfile.atlassian.net/browse/FTFL-597)
- Apply MKUH module with final schedule/scope/PE settings → [FTFL-598](https://fitfile.atlassian.net/browse/FTFL-598)

Critical chain (minimal path):

FTFL-605 (IAM confirm) → FTFL-615 (PE subnet + DNS) → Storage PE + lockdown → Vault/extension healthy → Policy scope fixed → FTFL-597/FTFL-598 applies

Parallelizable now:

- Draft/PR Terraform for PE subnet, PE, DNS (FTFL-615)
- Prepare tfvars for includedNamespaces and cadence/retention per site
- Capture cost note for OMOP snapshots for sign-off

References:

- Jira roll-up and delta plan were appended at 11:22 AM in [Jira-FTFL-596](obsidian://open?vault=LLMeon&file=Jira-FTFL-596) and confirmed in CLI audits between 10:54–11:25 AM
- Prod storage posture (public access Enabled) and no PEs confirmed circa 11:21 AM; staging VNet/subnets mapped at 12:12 PM

B) NUH Hybrid Node deployment—project foundations

Maximal deliverable: "Hybrid node live (EE-SDE AWS ↔ NUH via VPN) with agreed governance and ops"

Level 0—Commercial/IG gates

- Combined DCA/DSA Trust-board sign-off and DPIA position → [NUH - Project Summary (Internal)](https://fitfile.atlassian.net/wiki/spaces/EOE/pages/2727673857/NUH-+Project+Summary+Internal)
  - Status captured on 04/24; meeting prep captured 1:35 PM today

Level 1—Architecture decision and account placement

- Confirm "Hybrid" split (EE-SDE AWS managed stack; NUH on-prem DB as source) → 04/10 meeting notes
- Decide AWS account model (new transferable NUH account vs HIE sub-account)

Level 2—Network pre-reqs (depends on Level 1)

- NUH provides VPN prerequisites: static public IP, IPsec profile, CIDRs, change window
- SDE side prepares Site-to-Site VPN (tunnels, routing, health checks)

Level 3—Runtime substrate (depends on Level 1; can proceed in parallel with Level 2)

- Provision managed K8s (EKS) and VPC networking in EE-SDE; private DNS; egress allow-list
- Alternatively, if NUH provides K8s/VM: confirm versions, RBAC/namespace, ingress, storage classes, image policy, and sizing (8 vCPU, 32–64 GB RAM, 500 GB SSD baseline)

Level 4—Security and operations (depends on Levels 2–3)

- Secrets/TLS patterns agreed (Vault/Sealed Secrets; internal CA vs public)
- Observability targets (metrics/log routing to NUH SIEM), support model, maintenance windows
- CAB cadence and emergency route (risk owner: Andy Callow)

Level 5—Data access provisioning (depends on Level 2)

- Choose path: direct VPN query vs NUH-push to cloud (e.g., DMS to S3/RDS)
- Validate data interfaces for SAT/COSD; credentials path and data dictionaries

Level 6—Install and validate

- Deploy Node components; run smoke tests; confirm RPO/RTO with backup/restore path

Critical chain:

DCA/DSA/DPIA → Hybrid/account decision → VPN prerequisites (NUH) → SDE VPN + EKS (or NUH K8s/VM readiness) → Security/ops patterns → Data access path → Install/validate

Parallelizable now:

- Prep VPN parameters and port/CIDR lists for Friday (1:00–2:00 PM session on 05/01)
- Confirm K8s/VM environment sheet with NUH infra
- Draft observability and secrets/TLS one-pagers to accelerate CAB

Sources:

- 01/08 → 04/10 meeting series consolidated in NUH space: [NUH - Key Project Documents](https://fitfile.atlassian.net/wiki/spaces/EOE/pages/2734292993/NUH+-+Key+Project+Documents)
- Friday prep captured at 1:35 PM in your vault "Work Required for Deployment" and Miro "NUH (HIE) v0.2"

Want this rendered as an actual diagram? I can output Graphviz/DOT or Mermaid so you can paste into Miro/Confluence.
