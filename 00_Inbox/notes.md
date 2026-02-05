---
created: 2026-02-05T10:29:53+00:00
modified: 2026-02-05T11:03:48+00:00
title: notes
---

## Notes

This just creates empty secrets on vault.

Inside the Central Services repository, cd to hcp/vault - Central Services

Within locals.tf add a new block to the deployments variable.

The secret objects to create may differ with each deployment, but generally for new deployments it will look like this:

```json
"<replace_with_deployment_key>" = {
  secrets = tomap({
    "application" = {},
    "spicedb" = {},
    "cloudflare" = {}, # only needed if using cloudflare
    "monitoring" = {}, # for grafana creds
    "argo-workflows" = {}, # for argo workflows sso configuration
  })
}
```

FOLLOW THE COMMENTS BESIDE EACH SECRET FOR HOW TO POPULATE THEM

VAULT DOES NOT EXCEPT JSON WITH COMMENTS AND SO WILL NOT SAVE UNTIL THEY ARE REMOVED

```json
{
// Leave blank - do not need to fill
  "cli_auth0_client_id": "", 
  "cli_auth0_client_secret": "", 
// Leave blank - do not need to fill
  "mesh_client_cert": "", 
  "mesh_client_key": "", 
  "mesh_hash_secret": "", 
  "mesh_mailbox_password": "", 
// generate secure password (e.g. from LastPass) (min length 10, alphanumeric only)
  "mongodb_password": "", 
  "mongodb_username": "root",
  // generate secure password (length: 64, alphanumeric only)
  "mongodb_replica_set_key": "", 
// generate secure password (e.g. from LastPass) (min length 10, alphanumeric only)
  "postgresql_password": "", 
  "postgresql_username": "postgres",
 // generate secure password (min length 10, alphanumeric only)
  "s3_access_key_id": "ffadmin",
  "s3_secret_access_key": "",

  "ude_key": "", // generate from ude_cli using `key-gen` command. Needs to be same in all connected tenants

  "spicedb_pre_shared_key": "" // This may be different based on whether you use centralised spicedb or not. If centralised, get it from vault from admin/fitfile/production/spicedb_secrets. Otherwise, get from spicedb_secrets you will create

  "fitfile_tenant_pkcs8.key": "" // The private tenant pkcs8 signing key. See below
  "fitfile_tenant_public.crt": "" // The public tenant signing key. See below
}
```

To generate the fitfile_tenant signing keys, do the following:

```sh
mkdir <deployment-key>
cd <deployment-key>
openssl genrsa -out keypair.pem 4096
openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in keypair.pem -out pkcs8.key
openssl rsa -in keypair.pem -pubout -out publickey.crt 
```
