---
aliases: []
created: 2025-02-07 12:57:55+00:00
last_reviewed: ''
modified: 2026-06-08 11:49:24+00:00
project_category: development
project_name: Core
project_status: archived
see_also: []
status: ''
superseded_by: ''
supersedes: ''
tags: []
title: spicedb_grpc_preshared_key
type: secret
updated: null
permalink: llmeon/30-library/200-projects/spicedb-grpc-preshared-key
---

## SPICEDB_GRPC_PRESHARED_KEY

[spicedb_pre_shared_key](secrets/spicedb_pre_shared_key.md)

```json
{ 
 "postgresql_password": "", // generate secure password (min length 10, alphanumeric only)
 "postgresql_username": "postgres", 
 "spicedb_preshared_key": "" // generated and shared within application_secrets (min length 10, alphanumeric only) 
}
```

In the deployment repo

charts/ffnode/values.yaml

charts/spicedb/templates/_vault.tpl

charts/spicedb/templates/schema-write-job.yaml

charts/local-dev/seed/templates/seed-spicedb-configmap.yaml

charts/local-dev/seed/templates/seed-spicedb-job.yaml

charts/local-dev/seed/templates/seed-spicedb-secret.yaml