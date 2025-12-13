---
aliases: []
confidence: 
created: 2025-02-07T12:57:56Z
depends_on:
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: populate_secrets
type:
uid: 
updated: 
version:
---

## Populate Secrets

locals.tf

```json
{
  "cli_auth0_client_id": "", // Leave blank - do not need to fill
  "cli_auth0_client_secret": "", // Leave blank - do not need to fill

  "mesh_client_cert": "", // Leave blank if optout not required
  "mesh_client_key": "", // Leave blank if optout not required
  "mesh_hash_secret": "", // Leave blank if optout not required
  "mesh_mailbox_password": "", // Leave blank if optout not required

  "mongodb_password": "", // generate secure password (e.g. from LastPass) (min length 10, alphanumeric only)
  "mongodb_username": "root",
  "mongodb_replica_set_key": "", // generate secure password (length: 64, alphanumeric only)

  "postgresql_password": "", // generate secure password (e.g. from LastPass) (min length 10, alphanumeric only)
  "postgresql_username": "postgres",

  "s3_access_key_id": "ffadmin",
  "s3_secret_access_key": "", // generate secure password (min length 10, alphanumeric only)

  "ude_key": "", // generate from ude_cli using `key-gen` command. Needs to be same in all connected tenants

  "spicedb_pre_shared_key": "" // This may be different based on whether you use centralised spicedb or not. If centralised, get it from vault from admin/fitfile/production/spicedb_secrets. Otherwise, get from spicedb_secrets you will create
}
```

[auth0_client_id](../../DevOps/CI_CD/auth0_client_id.md)

[auth0_client_secret](secrets/auth0_client_secret.md)

[auth0_audience](auth0_audience)

[auth0_frontend_client_id](auth0_frontend_client_id)

[auth0_frontend_client_secret](auth0_frontend_client_secret)

[webapp_application_client_credential](webapp_application_client_credential)
