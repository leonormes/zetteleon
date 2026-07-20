---
created: 2026-07-08T11:26:15+00:00
modified: 2026-07-20T16:33:30+00:00
permalink: llmeon/00-inbox/perm
title: perm
type: note
---

Because you both hold the `organisation_admin` and `data_set_manager` roles, you effectively have maximum tenant-level privileges. The additional `data_source_manager` and `organisation_user` roles are technically redundant as their permissions are already covered by the admin and set manager relations.

Here is the formatted SDE section to add to your customer response:

## Summary for SDE

| Data Provider | Named Individual | RBAC Role | Authorised Operations |
| --- | --- | --- | --- |
| SDE | Oliver Rushton | Data Set Manager, Data Source Manager, Organisation Admin, Organisation User | Manage organisation members and projects, manage data sources and data sets (including export), manage schemas and templates, authorise and enable data disclosure, configure tenant and data source connections, read data catalogue, and read operations. |
| SDE | Leon Ormes | Data Set Manager, Data Source Manager, Organisation Admin, Organisation User | Manage organisation members and projects, manage data sources and data sets (including export), manage schemas and templates, authorise and enable data disclosure, configure tenant and data source connections, read data catalogue, and read operations. |

---

## Detailed Breakdown

Data Provider: SDE

Named Individual: Oliver Rushton

RBAC Roles: Data Set Manager (`data_set_manager`), Data Source Manager (`data_source_manager`), Organisation Admin (`organisation_admin`), Organisation User (`organisation_user`)

Authorised Operations:

- Access & Visibility: Log into the organisation, read the data catalogue, read data sources, read organisation members, and read operations.
- Organisation & Members: Create, read, update, and delete organisation members.
- Project Management: Create and delete projects.
- Data Source & Set Management: Create, update, and delete data sources; read and export data sets.
- Schema & Templates: Create, read, update, and delete data schemas and transformation templates.
- Connectivity & Authorisation: Enable and authorise data disclosure, connect data partner and consumer tenants, and write datasource-to-project/tenant connections.

Data Provider: SDE

Named Individual: Leon Ormes

RBAC Roles: Data Set Manager (`data_set_manager`), Data Source Manager (`data_source_manager`), Organisation Admin (`organisation_admin`), Organisation User (`organisation_user`)

Authorised Operations:

- Access & Visibility: Log into the organisation, read the data catalogue, read data sources, read organisation members, and read operations.
- Organisation & Members: Create, read, update, and delete organisation members.
- Project Management: Create and delete projects.
- Data Source & Set Management: Create, update, and delete data sources; read and export data sets.
- Schema & Templates: Create, read, update, and delete data schemas and transformation templates.
- Connectivity & Authorisation: Enable and authorise data disclosure, connect data partner and consumer tenants, and write datasource-to-project/tenant connections.
