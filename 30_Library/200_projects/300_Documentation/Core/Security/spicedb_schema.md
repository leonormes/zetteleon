---
aliases: []
confidence: 
created: 2025-02-07T12:57:56Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: spicedb_schema
type:
uid: 
updated: 
version:
---

## spicedb_schema

depends_on::

```mermaid
graph TD;
    fitfile_user["fitfile/user"]
    fitfile_tenant["fitfile/tenant"]
    fitfile_project["fitfile/project"]

    fitfile_tenant -->|data_source_manager| fitfile_user
    fitfile_tenant -->|data_set_manager| fitfile_user
    fitfile_tenant -->|organisation_admin| fitfile_user
    fitfile_tenant -->|organisation_user| fitfile_user

    fitfile_project -->|project_admin| fitfile_user
    fitfile_project -->|identifiable_user| fitfile_user
    fitfile_project -->|re_id_user| fitfile_user
    fitfile_project -->|pseudonymised_user| fitfile_user
    fitfile_project -->|anonymised_user| fitfile_user

    fitfile_project -->|project_host| fitfile_tenant
    fitfile_project -->|project_data_partner| fitfile_tenant
```
