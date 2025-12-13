---
aliases: []
confidence: 
created: 2025-02-07T12:57:55Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: spicedb_grpc_preshared_key
type: secret
uid: 
updated: 
version:
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
