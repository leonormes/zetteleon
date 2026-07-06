---
created: 2026-04-28T08:24:50+00:00
modified: 2026-07-04T10:51:35+00:00
permalink: llmeon/30-library/200-projects/ftfl-596-configure-azure-backups
project_category: refined_deployment
project_name: Refined Deployment
project_status: active
title: FTFL-596 Configure Azure Backups
type: null
---

## FTFL-596: Configure the Azure Backups Module for NNUH & MKUH

Status: In Progress

Priority: Medium

Assignee: Leon Ormes

Reporter: Ollie Rushton

Created: 2026-04-20

Link: <https://fitfile.atlassian.net/browse/FTFL-596>

### Description

We need to configure the backups module for the EoE Data Providers which don't currently have it enabled.

We should have answers to the following before we start this ticket:

1. What is the backup frequency (must be outside of operational hours)
2. What is the backup retention period
3. What is the minimum number of backups to retain?
4. Has cost of backups been factored in to Node costs (including the OMOP data)?
5. Do different PVCs have different backup requirements?
  1. If yes, then we need a ticket to modify the azure backups module
6. Will the Terraform service account have access to create/update/delete these resources?
  1. If no, need to create a ticket to request each data provider to update the SP's roles.

Backup requirements we already know:

- Any application PVC should be backed up - I.e. our MongoDB, SpiceDB (postgresql), PostgreSQL
- The Hyve OMOP database should be backed up

### Sub-tasks

#### [FTFL-605](https://fitfile.atlassian.net/browse/FTFL-605): Access the Permissions and Roles Needed by Backups and Make Relevant Change Requests to Customers

- Status: Backlog
- Assignee: Leon Ormes
- Description:
    - Assess what permissions or RBAC role in Azure is needed to apply the azure-backups module
    - Raise any change requests with customers where a change to the Terraform SA is needed (NNUH/MKUH)
    - If Contributor over subscription or resource group
    - Check whether we need a Resource Provider in the azure subscription activated - check we can turn this on or off.

#### [FTFL-597](https://fitfile.atlassian.net/browse/FTFL-597): Deploy Azure Backups Module to NNUH

- Status: Backlog
- Assignee: Unassigned
- Description: Deploy the module to NNUH.

#### [FTFL-598](https://fitfile.atlassian.net/browse/FTFL-598): Deploy Azure Backups Module to MKUH

- Status: Backlog
- Assignee: Unassigned
- Description: Deploy the module to MKUH.
