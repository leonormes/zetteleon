---
tags:
  - Ticket
---
\[FTFL-596\] Configure the Azure backups module for NNUH & MKUH

- Status: Selected for Development (To Do)

- Assignee: Leon Ormes

- Priority: Medium

- Sprint: FITFILE Sprint 15 (Active)

- Reporter: Ollie Rushton

  Description
The goal is to configure the backups module for the EoE Data Providers (NNUH & MKUH) that do not currently have it enabled.

  Pre-requisite Questions:

1. Frequency: What is the backup frequency? (Must be outside operational hours).

2. Retention: What is the backup retention period?

3. Minimum Count: What is the minimum number of backups to retain?

4. Cost: Has the cost of backups been factored into Node costs (including OMOP data)?

5. PVC Requirements: Do different PVCs have different requirements? (If yes, the Azure backups module may need modification).

6. Permissions: Does the Terraform service account have access? (If no, customer change requests are needed for SP roles).

  Known Backup Requirements:

- Application PVCs: MongoDB, SpiceDB (PostgreSQL), and standalone PostgreSQL.

- Hyve OMOP Database.

  Sub-tasks

- FTFL-597: Deploy Azure Backups Module to NNUH

- FTFL-598: Deploy Azure Backups Module to MKUH

- FTFL-605: Access the permissions and roles needed by backups and make relevant change requests to customers

  Comments

- Ollie Rushton: "Must check the our contracts + governance + compliance rules... start with @Helena Ahlfors"