---
aliases: []
confidence: 
created: 2025-10-14T11:49:19Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:11Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: FITFILE Secret Inventory
type:
uid: 
updated: 
version:
---

This table outlines all the secrets deployed in the `HIE-PROD-34` environment, categorised by their respective deployment layers or namespaces.

| Namespace/Layer  | Secret Name                  | Description                                                                                            |
| :--------------- | :--------------------------- | :----------------------------------------------------------------------------------------------------- |
| **ffnode**       | `mongodb`                    | Contains the MongoDB root password and replica set key.                                                |
|                  | `postgresql`                 | Stores the PostgreSQL administrator password.                                                          |
|                  | `minio`                      | Holds the root user and password for the MinIO S3 service.                                             |
|                  | `argo-postgres-config`       | Contains the database credentials for Argo Workflows.                                                  |
|                  | `spicedb`                    | Stores the database and preshared key for SpiceDB.                                                     |
|                  | `workflows-secrets`          | Aggregates credentials for workflows, including MongoDB, Auth0, S3, and SpiceDB.                       |
|                  | `ude-secret`                 | Contains the Universal Data Encryption key.                                                            |
|                  | `fitfile-rsa-private-key`    | Stores the RSA private key (PKCS#8 format) and certificate.                                            |
|                  | `fitconnect`                 | Holds service credentials for the FITConnect application.                                              |
|                  | `ffcloud`                    | Contains credentials for the FFCloud coordinator service.                                              |
|                  | `frontend`                   | Stores credentials for the frontend application, including Auth0 and MongoDB details.                  |
|                  | `monitoring`                 | Contains credentials for Grafana Cloud services (Prometheus, Loki, Tempo).                             |
| **hutch**        | `bunny`                      | Holds credentials for the Bunny ETL database and Task API.                                             |
|                  | `relay`                      | Contains credentials for the Relay service, including database, RabbitMQ, and upstream API details.    |
|                  | `hutch-postgresql`           | Stores the administrator password for the Hutch PostgreSQL instance.                                   |
|                  | `hutch-rabbitmq`             | Holds the RabbitMQ password and the Erlang cookie.                                                     |
| **thehyve**      | `thehyve`                    | Contains Airflow credentials for the OMOP DB, Airflow DB, and admin user.                              |
|                  | `thehyve-postgresql-init-db` | Contains the PostgreSQL initialisation script for creating the airflow/ohdsi databases.                |
|                  | `thehyve-postgresql`         | Stores the administrator password for TheHyve's PostgreSQL instance.                                   |
| **Cluster-Wide** | `fitfile-eoe-tls`            | A TLS certificate for application ingresses, providing HTTPS for various endpoints.                    |
|                  | `fitfile-image-pull-secret`  | Short-lived credentials used by all namespaces to pull container images from Azure Container Registry. |

## FITFILE Deployment Secrets Architecture - Comprehensive Analysis

**Environment:** HIE-PROD-34 (East of England SDE CODISC)
**Date:** October 14, 2025

---

### Executive Summary

The FITFILE deployment uses **HashiCorp Vault Secrets Operator (VSO)** for centralized secrets management. The HIE-PROD-34 deployment contains **19 VaultStaticSecret resources** managing credentials for databases, authentication, monitoring, and application services.

#### Key Findings

- ✅ **Strong Foundation**: VSO provides dynamic secret rotation and drift detection
- ⚠️ **Security Concerns**: Hardcoded credentials exist in legacy `shared-secrets` chart
- 🔄 **Optimization Opportunities**: Secret consolidation and refresh interval tuning needed
- 📊 **Complexity**: 19 secrets across 3 deployment layers (ffnode, hutch, thehyve)

---

### 1. Complete Secrets Inventory

#### 1.1 Core Application Secrets (FFNode Chart - 12 secrets)

| Secret Name               | Vault Path       | Purpose                                             | Refresh | Rollout Restart      |
| ------------------------- | ---------------- | --------------------------------------------------- | ------- | -------------------- |
| `mongodb`                 | `application`    | MongoDB root password + replica set key             | ❌ null | ❌ None              |
| `postgresql`              | `application`    | PostgreSQL admin password                           | ❌ null | ❌ None              |
| `minio`                   | `application`    | MinIO S3 credentials (root user/password)           | ❌ null | ❌ None              |
| `argo-postgres-config`    | `argo-workflows` | Argo Workflows DB credentials                       | ❌ null | ❌ None              |
| `spicedb`                 | `spicedb`        | SpiceDB DB + preshared key                          | ❌ null | ❌ None              |
| `workflows-secrets`       | `application`    | Workflow credentials (MongoDB, Auth0, S3, SpiceDB)  | ❌ null | ❌ None              |
| `ude-secret`              | `application`    | Universal Data Encryption key                       | ❌ null | ❌ None              |
| `fitfile-rsa-private-key` | `application`    | RSA keypair (PKCS#8 + cert)                         | ❌ null | ❌ None              |
| `fitconnect`              | `application`    | FITConnect service credentials                      | ✅ 5m   | ✅ fitconnect-ftc    |
| `ffcloud`                 | `application`    | FFCloud coordinator credentials                     | ✅ 5m   | ✅ ffcloud-service   |
| `frontend`                | `application`    | Frontend app credentials (Auth0, MongoDB)           | ✅ 5m   | ✅ frontend-frontend |
| `monitoring`              | `monitoring`     | Grafana Cloud credentials (Prometheus, Loki, Tempo) | ❌ null | ❌ None              |

#### 1.2 Hutch Integration Secrets (4 secrets)

| Secret Name        | Vault Path | Purpose                                    | Refresh | Rollout Restart     |
| ------------------ | ---------- | ------------------------------------------ | ------- | ------------------- |
| `bunny`            | `hutch`    | Bunny ETL DB + Task API credentials        | ✅ 10m  | ✅ Bunny deployment |
| `relay`            | `hutch`    | Relay service (DB, RabbitMQ, upstream API) | ✅ 10m  | ✅ Relay deployment |
| `hutch-postgresql` | `hutch`    | Hutch PostgreSQL admin password            | ✅ 10m  | ✅ hutch-postgresql |
| `hutch-rabbitmq`   | `hutch`    | RabbitMQ password + Erlang cookie          | ✅ 10m  | ✅ hutch-rabbitmq   |

#### 1.3 TheHyve ETL Secrets (3 secrets)

| Secret Name                  | Vault Path | Purpose                                            | Refresh | Rollout Restart       |
| ---------------------------- | ---------- | -------------------------------------------------- | ------- | --------------------- |
| `thehyve`                    | `thehyve`  | Airflow credentials (OMOP DB, Airflow DB, admin)   | ✅ 10m  | ✅ TheHyve deployment |
| `thehyve-postgresql-init-db` | `thehyve`  | PostgreSQL init script (creates airflow/ohdsi DBs) | ✅ 10m  | ✅ thehyve-postgresql |
| `thehyve-postgresql`         | `thehyve`  | TheHyve PostgreSQL admin password                  | ✅ 10m  | ✅ thehyve-postgresql |

#### 1.4 TLS Certificates (cert-manager)

| Certificate       | Issuer       | Vault Path                              | DNS Names                                    |
| ----------------- | ------------ | --------------------------------------- | -------------------------------------------- |
| `fitfile-eoe-tls` | vault-issuer | `pki_int_hie-prod-34/sign/cert-manager` | `app.eoe-sde-codisc.privatelink.fitfile.net` |

**Used By:** FITConnect, FFCloud, Frontend ingresses

#### 1.5 Image Pull Secrets (VaultDynamicSecret)

| Secret                      | Type               | Vault Path                           | Distribution                |
| --------------------------- | ------------------ | ------------------------------------ | --------------------------- |
| `fitfile-image-pull-secret` | VaultDynamicSecret | `admin/central/azure/creds/acr-pull` | Reflected to all namespaces |

**Purpose:** Azure Container Registry authentication (short-lived Azure SP credentials)

---

### 2. Vault Secrets Operator (VSO) Architecture

#### 2.1 What VSO Does

The Vault Secrets Operator synchronizes secrets from HCP Vault into Kubernetes:

1. **Automatic Synchronization**: Pulls secrets from Vault → creates K8s secrets
2. **Drift Detection**: `hmacSecretData: true` detects manual modifications
3. **Automatic Rotation**: Secrets refresh at configured intervals (`refreshAfter`)
4. **Rollout Restart**: Pods restart automatically when secrets change
5. **Transformation**: Template secrets before creating K8s secrets (e.g., connection strings)

#### 2.2 Authentication Flow

```sh
1. Terraform creates AppRole (Role ID + Secret ID) in Vault
2. Terraform stores credentials in K8s secret (e.g., hie-prod-34-approle-secret)
3. Terraform creates VaultAuth resource pointing to AppRole secret
4. VSO authenticates to Vault using AppRole
5. VSO receives Vault token with namespace-scoped permissions
6. VSO creates/updates K8s secrets from VaultStaticSecret resources
```

#### 2.3 Secret Transformation Example

**Vault stores individual credentials:**

```sh
relay_postgresql_username = "relay_user"
relay_postgresql_password = "secure_pass"
```

**VSO transforms into connection string:**

```yaml
transformation:
templates:
db_connection_string:
text: 'Host=hutch-postgresql;Port=5432;Database=postgres;User Id={{get .Secrets "relay_postgresql_username"}};Password={{get .Secrets "relay_postgresql_password"}}'
```

**Result:** K8s secret contains ready-to-use connection string

---

### 3. Security Analysis

#### 3.1 ✅ Strengths

1. **Centralized Management**: All secrets in HCP Vault (external to cluster)
2. **AppRole Authentication**: Namespace-scoped, least-privilege access
3. **Drift Detection**: Prevents manual secret tampering
4. **Automatic Rotation**: Secrets refresh automatically (where configured)
5. **TLS Automation**: cert-manager + Vault PKI (no manual cert management)
6. **Dynamic ACR Credentials**: Short-lived Azure SP tokens

#### 3.2 ⚠️ Critical Security Issues

##### **Issue 1: Hardcoded Credentials in Git**

- **File:** `/charts/shared-secrets/values.yaml`
- **Problem:** Plaintext passwords in repository:

```yaml
mongodbUri:
password: fitconn5766
imageCredentials:
password: EyPX=KrgsnDgNZ7oTaNXX4L+3IH8xTOZ
```

- **Risk:** HIGH - Credentials exposed in Git history
- **Fix:** Migrate to VSO immediately, rotate credentials

##### **Issue 2: No Auto-Refresh on Critical Secrets**

- **Affected:** `mongodb`, `postgresql`, `minio`, `argo-postgres-config`, `spicedb`, `workflows-secrets`, `monitoring`
- **Problem:** `refreshAfter: null` = secrets never sync from Vault
- **Risk:** MEDIUM - Stale credentials if rotated in Vault
- **Fix:** Set `refreshAfter: 1h` minimum

##### **Issue 3: No Rollout Restart on Databases**

- **Affected:** `mongodb`, `postgresql`, `minio`
- **Problem:** Pods won't restart if secrets change
- **Risk:** MEDIUM - Manual intervention required for rotation
- **Fix:** Add `rolloutRestartTargets` for StatefulSets

##### **Issue 4: No Encryption at Rest**

- **Problem:** K8s secrets are base64-encoded, not encrypted
- **Risk:** MEDIUM - Readable if etcd compromised
- **Fix:** Enable K8s EncryptionConfiguration with KMS provider

---

### 4. Optimization Opportunities

#### 4.1 Standardize Refresh Intervals

**Current State:**

- 5m: Application secrets (fitconnect, ffcloud, frontend)
- 10m: Hutch/TheHyve secrets
- null: Databases, monitoring, workflows

**Recommended:**

| Secret Type          | Recommended Interval | Rationale                                |
| -------------------- | -------------------- | ---------------------------------------- |
| Database credentials | 1h                   | Infrequent rotation, high restart cost   |
| Application secrets  | 15m                  | Balance freshness vs. API load           |
| Hutch/TheHyve        | 15m                  | Align with application secrets           |
| Monitoring           | 1h                   | External service, low rotation frequency |
| Workflows            | 30m                  | Used by ephemeral pods                   |

**Benefits:**

- Reduced Vault API calls
- Fewer unnecessary pod restarts
- Better alignment with rotation policies

#### 4.2 Secret Consolidation

**Opportunity:** Merge related secrets to reduce VSO resource count

**Example:** Consolidate `mongodb`, `postgresql`, `minio` into single `databases` secret:

- Single refresh cycle
- Coordinated rollout restarts
- Simplified management

**Trade-off:** All databases restart together (brief downtime)

#### 4.3 Migrate to VaultDynamicSecret for Databases

**Current:** Static passwords in Vault KV

**Opportunity:** Use Vault database secrets engine for dynamic credentials

**Benefits:**

- Automatic password rotation
- Short-lived credentials (e.g., 1h TTL)
- Audit trail of credential usage
- No manual password management

**Implementation:**

```yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultDynamicSecret
metadata:
name: postgresql-dynamic
spec:
mount: database
path: creds/postgresql-admin
refreshAfter: 1h
```

---

### 5. Actionable Recommendations

#### 5.1 Immediate Actions (High Priority)

1. **Remove Hardcoded Credentials**

- Migrate `shared-secrets` chart to VSO
- Delete plaintext passwords from Git
- Rotate all compromised credentials

2. **Enable Secret Refresh**

```yaml

# Add to all database secrets:

refreshAfter: 1h

# Add to workflow secrets:

refreshAfter: 30m

# Add to monitoring secrets:

refreshAfter: 1h

```

3. **Add Rollout Restart Targets**

```yaml
# Example for mongodb secret:

rolloutRestartTargets:
  - kind: StatefulSet

name: hie-prod-34-mongodb
```

4. **Document Rotation Policy**

- Define rotation schedule (e.g., 90 days)
- Create runbook for manual rotation
- Set up alerts for expiring credentials

#### 5.2 Short-Term Improvements (Medium Priority)

5. **Standardize Refresh Intervals** (see section 4.1)
6. **Enable K8s Encryption at Rest**

- Configure EncryptionConfiguration on API server
- Use Azure Key Vault KMS provider
- Rotate encryption keys annually

7. **Add Monitoring**

- Alert on VSO sync failures
- Dashboard for secret age
- Audit log analysis for secret access

#### 5.3 Long-Term Enhancements (Low Priority)

8. **Migrate to VaultDynamicSecret** (see section 4.3)
9. **Implement Secret Scanning**

- Add pre-commit hooks (git-secrets, trufflehog)
- CI/CD pipeline secret scanning
- Regular repository audits

10. **Secret Versioning**

- Enable Vault KV v2 versioning
- Configure retention policy (keep last 10 versions)
- Test rollback procedure

---

### 6. Summary

The FITFILE deployment has a **solid foundation** with VSO providing centralized secret management. However, **critical gaps exist**:

- ❌ Hardcoded credentials in Git (HIGH RISK)
- ❌ No auto-refresh on 9/19 secrets (MEDIUM RISK)
- ❌ No encryption at rest (MEDIUM RISK)

**Priority Actions:**

1. Migrate `shared-secrets` to VSO immediately
2. Enable `refreshAfter` on all secrets
3. Add `rolloutRestartTargets` for databases
4. Enable K8s encryption at rest

**Long-term Vision:**

- Migrate to VaultDynamicSecret for databases
- Standardize refresh intervals
- Implement comprehensive monitoring

---

**Report Generated:** October 14, 2025
**Environment:** hie-prod-34 (EOE SDE CODISC)
