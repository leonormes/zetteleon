---
created: 2026-02-05T11:05:21+00:00
modified: 2026-02-05T12:38:04+00:00
title: application-sercrets
---

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

  "fitfile_tenant_pkcs8.key": "" // The private tenant pkcs8 signing key. See below
  "fitfile_tenant_public.crt": "" // The public tenant signing key. See below
}
```
