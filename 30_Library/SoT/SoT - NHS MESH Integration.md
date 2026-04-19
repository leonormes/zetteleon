---
aliases: [MESH Integration, NHS Digital Networking, NHS Mailbox]
created: 2025-12-10T13:06:37Z
last_reviewed: "2026-03-28"
modified: 2026-04-19T18:30:32+00:00
status: growing
tags: [compliance, healthcare, mesh, nhs, sot]
title: SoT - NHS MESH Integration
type: SoT
---

## Minimum Viable Understanding (MVU)

The Messaging Exchange for Social Care and Health (MESH) is the primary mechanism for asynchronous data exchange across the NHS. FITFILE uses MESH for services like the National Data Opt-out (NDOO) cleanup. Integration requires an active MESH Mailbox, ODS code registration, and compliance with HSCN technical standards.

---

## Working Knowledge

### 1. FITFILE MESH Configuration

- Organisation: FITFILE Group Ltd
- ODS Code: `8KM90`
- Mailbox ID: `8KM90HC001`
- Status: Production mailbox is Active and accessible.

### 2. Networking & Whitelisting

- Source IP Whitelisting: MESH does not require source IP whitelisting for access from different clusters.
- Geo-blocking: Access is restricted to UK-based IP addresses only.
- Connectivity: Must originate from an HSCN-compliant network or via approved cloud-to-HSCN gateways.

### 3. NHS Ecosystem Compliance

Any networking or processing of patient data within the NHS ecosystem must adhere to three foundational pillars:

#### A. Secure Data Environments (SDE)

Following the Goldacre Review, the NHS is shifting from "Data Sharing" (bulk physical transfers) to "Data Access" (Secure Data Environments). SDEs are the mandatory route for secondary use of NHS data.

- Five Safes: Safe People, Safe Projects, Safe Settings, Safe Data, Safe Outputs.

#### B. HSCN Connection Agreement

Mandatory for any organisation connecting to the Health and Social Care Network.

- TSS 201: Network architecture & monitoring.
- TSS 203: Encryption at rest and in transit.

#### C. Data Security and Protection Toolkit (DSPT)

Annual self-assessment against the National Data Guardian's 10 standards. Achieving "Standards Met" is a prerequisite for MESH and SDE access.

---

## Current Understanding

### International Data Transfers (ICO 2026)

For research involving international collaboration across GDPR boundaries, the 2026 ICO guidance mandates a Three-Step Test and a Data Protection Test (formerly TRA) to ensure the destination jurisdiction's protection is not materially lower than the UK's.

### National Data Opt-out (NDOO)

Compliance became mandatory in July 2022. Identifiable patient data for research must be filtered against the NDOO registry via the MESH "Check for National Data Opt-outs" service.

## Related Documentation

- [[SoT - OHDSI and FHIR Convergence]]
- [[HSCN Connection Agreement]]
- [[NHS Patient Data Research Networking]]
