---
aliases: []
created: 2025-02-07T12:57:55Z
last_reviewed: ""
modified: 2026-04-09T07:46:45+00:00
prodos: {kind: atomic, lifecycle: seedling, trust: working, id: "", review: {interval: "", last_reviewed: ""}, chronos: {last_synthesis: "", synthesis_count: 0}, atomic: {form: concept}, protocol: {applies_to: [], binary_checklist: true}, moc: {hub_for: [], entry_points: []}, ops: {tool: "", target_service: "", hop_level: "", requires_tunnel: false, prerequisites: []}, prompt: {description: "", inject_as: "", model_hints: ""}, project: {area: "", status: "", owner: ""}}
see_also: []
status: ""
superseded_by: ""
supersedes: ""
tags: []
title: spicedb_grpc_preshared_key
type: "secret"
updated: 
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
