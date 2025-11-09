---
aliases: []
confidence: 
created: 2025-10-23T14:20:40Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:14Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: thehyve-mkuh-investigation-report
type:
uid: 
updated: 
version:
---

## Thehyve-mkuh Deployment Investigation Report

**Generated:** 2025-10-23  
**Cluster:** fitfile-cloud-prod-1-aks-cluster  
**Namespace:** thehyve-mkuh  
**Investigation Date:** 2025-10-23 14:08 UTC

---

### Executive Summary

The **thehyve-mkuh** deployment is an Apache Airflow-based ETL system running on the **fitfile-cloud-prod-1-aks-cluster** (AKS). The deployment has been operational for 141 days and consists of:

- **Main Application**: Apache Airflow (webserver + scheduler) running in a single pod with 2 containers
- **Database**: PostgreSQL 16.3.0 in a StatefulSet with persistent storage
- **Management**: Deployed and maintained via ArgoCD GitOps
- **Overall Health**: ✅ **Healthy** - All pods running, ArgoCD synced

#### Key Metrics

- **Namespace Age**: 141 days
- **Pod Uptime**: 20 days (recent restart)
- **Current Status**: All pods running (2/2 containers ready)
- **CPU Usage**: 43m (Airflow), 16m (PostgreSQL)
- **Memory Usage**: 1.4Gi (Airflow), 7Gi (PostgreSQL)
- **Storage**: 21Gi total (20Gi DB, 1Gi reports)

#### ⚠️ Active Warnings

- Image pull secret warnings detected (non-blocking, pods still running)

---

### Deployment Architecture

#### Overview

```sh
┌─────────────────────────────────────────────────┐
│              ArgoCD GitOps                      │
│  https://gitlab.com/fitfile/deployment.git      │
│  Branch: latest-release                         │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│           thehyve-mkuh Namespace                │
│                                                 │
│  ┌──────────────────────────────────────┐      │
│  │  Deployment: thehyve-mkuh            │      │
│  │  ┌────────────────────────────┐      │      │
│  │  │ Pod (thehyve-mkuh-...)     │      │      │
│  │  │  - Init: database setup    │      │      │
│  │  │  - Webserver (8080)        │      │      │
│  │  │  - Scheduler               │      │      │
│  │  └────────────┬───────────────┘      │      │
│  └───────────────┼──────────────────────┘      │
│                  │                              │
│                  │ SQL Connection               │
│                  ▼                              │
│  ┌──────────────────────────────────────┐      │
│  │  StatefulSet: postgresql             │      │
│  │  ┌────────────────────────────┐      │      │
│  │  │ Pod: postgresql-0          │      │      │
│  │  │  - PostgreSQL 16.3.0       │      │      │
│  │  │  - Port 5432                │      │      │
│  │  └────────┬───────────────────┘      │      │
│  │           │                          │      │
│  │           ▼                          │      │
│  │  PVC: data (20Gi)                    │      │
│  └──────────────────────────────────────┘      │
│                                                 │
│  Additional PVC: thehyve-mkuh-reports (1Gi)    │
└─────────────────────────────────────────────────┘
```

#### Component Topology

- **Application Type**: Apache Airflow ETL (NHS MKUH site)
- **Executor**: LocalExecutor (single-pod architecture)
- **Container Pattern**: Multi-container pod (init + webserver + scheduler)
- **Database**: Dedicated PostgreSQL StatefulSet
- **Storage**: Persistent volumes with `default-retain` storage class

---

### Resource Details

#### Deployment: Thehyve-mkuh

| Property        | Value                                                               |
| --------------- | ------------------------------------------------------------------- |
| **Name**        | thehyve-mkuh                                                        |
| **Replicas**    | 1 (desired/current/available)                                       |
| **Strategy**    | Recreate                                                            |
| **Age**         | 141 days                                                            |
| **Image**       | fitfileregistry.azurecr.io/thehyve/fitfile_etl_container_mkuh:0.4.2 |
| **Helm Chart**  | thehyve-0.0.2                                                       |
| **App Version** | 0.0.3                                                               |

#### Container Specifications

##### Init Container

| Name | Image                                                               |
| ---- | ------------------------------------------------------------------- |
| init | fitfileregistry.azurecr.io/thehyve/fitfile_etl_container_mkuh:0.4.2 |

**Purpose**: Database initialization and migrations

##### Application Containers

| Container     | Image                            | CPU Request | CPU Limit | Memory Request | Memory Limit |
| ------------- | -------------------------------- | ----------- | --------- | -------------- | ------------ |
| **webserver** | fitfile_etl_container_mkuh:0.4.2 | 250m        | -         | 512Mi          | -            |
| **scheduler** | fitfile_etl_container_mkuh:0.4.2 | 125m        | 2         | 128Mi          | 24Gi         |

#### Health Probes

##### Webserver

- **Liveness**: HTTP GET :8080/ (delay=10s, timeout=1s, period=10s)
- **Readiness**: HTTP GET :8080/ (delay=5s, timeout=1s, period=10s)

#### Environment Configuration

**Environment Variables** (sourced from Secret `thehyve-mkuh`):

- `AIRFLOW_ADMIN_EMAIL`
- `AIRFLOW_ADMIN_FIRSTNAME`
- `AIRFLOW_ADMIN_LASTNAME`
- `AIRFLOW_ADMIN_PASSWORD`
- `AIRFLOW_ADMIN_USERNAME`
- `AIRFLOW__CORE__SQL_ALCHEMY_CONN`
- `OMOP_TARGET_DB`

**Explicit Environment Variables**:

- `AIRFLOW__CORE__EXECUTOR=LocalExecutor`
- `AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS=False`
- `AIRFLOW__CORE__LOAD_EXAMPLES=False`
- `AIRFLOW__CORE__STORE_DAG_CODE=True`
- `AIRFLOW__CORE__STORE_SERIALIZED_DAGS=True`
- `AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True`
- `AIRFLOW__WEBSERVER__RBAC=False`
- `NHS_SITE=mkuh`

#### Volumes

| Name       | Type                  | Details                    |
| ---------- | --------------------- | -------------------------- |
| reports    | PersistentVolumeClaim | thehyve-mkuh-reports (1Gi) |
| log-volume | EmptyDir              | 500Mi size limit           |

---

### PostgreSQL StatefulSet

| Property            | Value                                                              |
| ------------------- | ------------------------------------------------------------------ |
| **Name**            | thehyve-mkuh-postgresql                                            |
| **Replicas**        | 1                                                                  |
| **Image**           | fitfileregistry.azurecr.io/bitnami/postgresql:16.3.0-debian-12-r19 |
| **Chart**           | postgresql-15.5.15                                                 |
| **Age**             | 141 days                                                           |
| **Update Strategy** | RollingUpdate                                                      |

#### PostgreSQL Container Resources

| Resource           | Value |
| ------------------ | ----- |
| **CPU Request**    | 250m  |
| **Memory Request** | 256Mi |
| **CPU Limit**      | -     |
| **Memory Limit**   | -     |

#### PostgreSQL Configuration

**Environment**:

- `BITNAMI_DEBUG=false`
- `POSTGRESQL_PORT_NUMBER=5432`
- `POSTGRESQL_VOLUME_DIR=/bitnami/postgresql`
- `PGDATA=/bitnami/postgresql/data`
- `POSTGRES_PASSWORD` (from secret)
- `POSTGRESQL_SHARED_PRELOAD_LIBRARIES=pgaudit`

**Volumes**:

- **data**: VolumeClaimTemplate (20Gi, ReadWriteOnce)
- **custom-init-scripts**: ConfigMap (thehyve-mkuh-postgresql-init-scripts)
- **dshm**: EmptyDir (Memory)
- **empty-dir**: EmptyDir (temporary storage)

#### Health Checks

- **Liveness**: `pg_isready` (delay=30s, timeout=5s, period=10s)
- **Readiness**: `pg_isready` + initialization check (delay=5s, timeout=5s, period=10s)

---

### Storage Configuration

#### Persistent Volume Claims

| PVC Name                       | Status | Volume                                   | Capacity | Access Mode | Storage Class  | Age  |
| ------------------------------ | ------ | ---------------------------------------- | -------- | ----------- | -------------- | ---- |
| data-thehyve-mkuh-postgresql-0 | Bound  | pvc-1ecead9f-0d26-46e9-a8ce-6f9fcf5fb01e | 20Gi     | RWO         | default-retain | 141d |
| thehyve-mkuh-reports           | Bound  | pvc-ee9da2a4-ac09-4a8a-9923-0dff24e6beff | 1Gi      | RWO         | default-retain | 141d |

#### Persistent Volumes

| PV Name                                  | Capacity | Status | Claim                                       | Storage Class  | Age  |
| ---------------------------------------- | -------- | ------ | ------------------------------------------- | -------------- | ---- |
| pvc-1ecead9f-0d26-46e9-a8ce-6f9fcf5fb01e | 20Gi     | Bound  | thehyve-mkuh/data-thehyve-mkuh-postgresql-0 | default-retain | 141d |
| pvc-ee9da2a4-ac09-4a8a-9923-0dff24e6beff | 1Gi      | Bound  | thehyve-mkuh/thehyve-mkuh-reports           | default-retain | 141d |

**Total Storage Provisioned**: 21Gi  
**Storage Class Features**: `default-retain` - volumes persist after PVC deletion

---

### Networking

#### Services

| Service Name               | Type                 | Cluster IP | Port(s)  | Selector                            | Age  |
| -------------------------- | -------------------- | ---------- | -------- | ----------------------------------- | ---- |
| thehyve-mkuh               | ClusterIP            | (internal) | 8080/TCP | app.kubernetes.io/name=thehyve-mkuh | 141d |
| thehyve-mkuh-postgresql    | ClusterIP            | (internal) | 5432/TCP | app.kubernetes.io/name=postgresql   | 141d |
| thehyve-mkuh-postgresql-hl | ClusterIP (Headless) | None       | 5432/TCP | app.kubernetes.io/name=postgresql   | 141d |

**Note**: No external LoadBalancer or NodePort services. Access is cluster-internal only.

#### Ingress Resources

**Status**: No Ingress resources found in the namespace.

**Implication**: The Airflow web interface is not directly exposed outside the cluster. Access would require:

- Port-forwarding via kubectl
- Internal cluster routing
- External ingress controller in a different namespace

#### Network Policies

| Policy Name             | Target Pods             | Type            | Age  |
| ----------------------- | ----------------------- | --------------- | ---- |
| thehyve-mkuh-postgresql | postgresql primary pods | Ingress, Egress | 141d |

##### PostgreSQL Network Policy Details

**Pod Selector**:

- `app.kubernetes.io/component=primary`
- `app.kubernetes.io/instance=thehyve-mkuh`
- `app.kubernetes.io/name=postgresql`

**Ingress Rules**:

- **Port**: 5432/TCP
- **From**: Any source (not restricted)

**Egress Rules**:

- **To**: Any destination (not restricted)
- **Ports**: All ports allowed

**Analysis**: The network policy allows PostgreSQL to accept connections from any pod in the cluster on port 5432 and make outbound connections freely. This is permissive and suitable for a cluster-internal database.

---

### Configuration Management

#### ConfigMaps

| ConfigMap                            | Purpose                           | Age  |
| ------------------------------------ | --------------------------------- | ---- |
| kube-root-ca.crt                     | CA certificate bundle             | 141d |
| thehyve-mkuh-postgresql-init-scripts | PostgreSQL initialization scripts | 141d |

**PostgreSQL Init Scripts**: Used to set up the OMOP database schema and initial data.

#### Secrets

| Secret Name             | Type   | Data Keys | Age  |
| ----------------------- | ------ | --------- | ---- |
| thehyve-mkuh            | Opaque | 7         | 141d |
| thehyve-mkuh-postgresql | Opaque | 1         | 141d |

**Secret Usage**:

- `thehyve-mkuh`: Airflow admin credentials and database connection strings
- `thehyve-mkuh-postgresql`: PostgreSQL password

**⚠️ Security Note**: All secrets are Opaque type (base64 encoded). Consider using Sealed Secrets, External Secrets Operator, or Azure Key Vault integration for enhanced secret management.

---

### GitOps & Deployment Management

#### ArgoCD Application

| Property                  | Value                                       |
| ------------------------- | ------------------------------------------- |
| **Name**                  | thehyve-mkuh                                |
| **Namespace**             | argocd                                      |
| **Sync Status**           | ✅ Synced                                   |
| **Health Status**         | ✅ Healthy                                  |
| **Repository**            | <https://gitlab.com/fitfile/deployment.git> |
| **Target Revision**       | latest-release                              |
| **Path**                  | charts/integrations/thehyve                 |
| **Current Revision**      | e837ef35f628ca6e8280e7f28eeb7620919ec201    |
| **Destination Server**    | <https://kubernetes.default.svc>            |
| **Destination Namespace** | thehyve-mkuh                                |

#### Helm Configuration

| Property         | Value                                     |
| ---------------- | ----------------------------------------- |
| **Release Name** | thehyve-mkuh                              |
| **Values File**  | /ffnodes/fitfile/ff-c/thehyve_values.yaml |

#### Sync Policy

- **Automated**: ✅ Yes
- **Prune**: ✅ Enabled (removes resources not in Git)
- **Self-Heal**: ✅ Enabled (automatically corrects drift)

**Analysis**: The deployment follows GitOps best practices with automated sync and self-healing enabled. Any manual changes to the cluster will be automatically reverted to match the Git repository state.

---

### Current Status & Health

#### Pod Status

| Pod Name                      | Ready | Status  | Restarts | Age | Node                           | IP         |
| ----------------------------- | ----- | ------- | -------- | --- | ------------------------------ | ---------- |
| thehyve-mkuh-59784df844-bglpm | 2/2   | Running | 0        | 20d | aks-system-54209202-vmss000000 | (internal) |
| thehyve-mkuh-postgresql-0     | 1/1   | Running | 0        | 20d | aks-system-54209202-vmss000000 | (internal) |

**Observations**:

- All pods healthy with 0 restarts in the last 20 days
- Both pods co-located on the same node (may affect HA)
- Clean uptime indicates stability

#### Resource Utilization

| Pod                           | CPU Usage | Memory Usage   |
| ----------------------------- | --------- | -------------- |
| thehyve-mkuh-59784df844-bglpm | 43m       | 1445Mi (1.4Gi) |
| thehyve-mkuh-postgresql-0     | 16m       | 6956Mi (6.8Gi) |

**Resource Analysis**:

- **Airflow Pod**: Using 17% of requested CPU (250m), memory usage at 282% of request (512Mi) but well below limit (24Gi)
- **PostgreSQL**: Using 6% of requested CPU (250m), memory usage at 27x request (256Mi) - **consider increasing memory request**
- Total cluster CPU impact: 59m
- Total cluster memory impact: 8.3Gi

#### Recent Events

**Last 50 Events** (sorted by timestamp):

```sh
LAST SEEN   TYPE      REASON                            OBJECT                              MESSAGE
2m51s       Warning   FailedToRetrieveImagePullSecret   pod/thehyve-mkuh-postgresql-0       Unable to retrieve image pull secret (fitfile-image-pull-secret)
2m49s       Warning   FailedToRetrieveImagePullSecret   pod/thehyve-mkuh-59784df844-bglpm   Unable to retrieve image pull secret (fitfile-image-pull-secret)
```

**Analysis**: Image pull secret warnings are present but non-blocking (pods are running successfully). This suggests:

1. Images are already cached on the node
2. The secret may be missing or misconfigured but not currently needed
3. Should be investigated to ensure future deployments succeed

#### Log Analysis Highlights

**Recent Application Activity** (last 50 lines):

**Database Initialization**:

- ✅ Database migrations completed successfully
- ✅ Initialization done

**Scheduler Activity**:

- Healthy scheduler heartbeat every ~5 minutes
- Regular orphaned task checks (normal Airflow behavior)
- Message: `INFO - Adopting or resetting orphaned tasks for active dag runs`

**Webserver Activity**:

- HTTP 302 redirects from `/home` to `/login/?next=.../home`
- HTTP 200 responses on login endpoint
- Probes: `kube-probe/1.33` checking health successfully

**⚠️ Warnings & Deprecations**:

1. **SQL Alchemy Connection**: Using deprecated `postgres://` scheme (should be `postgresql://`)
2. **Config Location**: `sql_alchemy_conn` moved from `[core]` to `[database]` section
3. **CLI Commands**: `db upgrade` and `db init` deprecated (use `db migrate` instead)
4. **Rate Limiting**: Using in-memory storage (not recommended for production)

**Impact**: These are warnings, not errors. The application functions correctly but should be updated in the next release.

---

### RBAC Configuration

#### Service Accounts

| Service Account         | Age  |
| ----------------------- | ---- |
| default                 | 141d |
| thehyve-mkuh            | 141d |
| thehyve-mkuh-postgresql | 141d |

#### Roles & Role Bindings

**Status**: No custom Roles or RoleBindings detected in the namespace.

**Analysis**:

- Service accounts exist but have default permissions only
- Deployment uses ServiceAccount: `thehyve-mkuh`
- PostgreSQL uses ServiceAccount: `thehyve-mkuh-postgresql`
- **Recommendation**: Review if additional RBAC permissions are needed for Airflow operations

---

### Autoscaling

**Status**: No HorizontalPodAutoscaler (HPA) or VerticalPodAutoscaler (VPA) resources found.

**Current Configuration**:

- Fixed replica count: 1
- No automatic scaling based on CPU/memory metrics

**Considerations**:

- The LocalExecutor architecture may limit horizontal scaling benefits
- Consider VPA for right-sizing memory requests (PostgreSQL significantly over memory request)

---

### Issues & Recommendations

#### 🔴 Critical Issues

None identified. System is healthy and operational.

#### 🟡 Warnings & Concerns

##### 1. Image Pull Secret Issues

**Issue**: Recurring warnings about missing `fitfile-image-pull-secret`

**Impact**: Low (current pods running from cached images)

**Recommendation**:

```bash
# Verify secret exists and is correctly configured
kubectl get secret fitfile-image-pull-secret -n thehyve-mkuh
# If missing, recreate:
kubectl create secret docker-registry fitfile-image-pull-secret \
  --docker-server=fitfileregistry.azurecr.io \
  --docker-username=<username> \
  --docker-password=<password> \
  -n thehyve-mkuh
```

##### 2. PostgreSQL Memory Configuration

**Issue**: PostgreSQL using 6956Mi but only requesting 256Mi (27x over request)

**Impact**: Medium (affects cluster scheduling decisions)

**Recommendation**:

```yaml
# Update PostgreSQL StatefulSet resource requests in values file:
resources:
  requests:
    memory: "8Gi" # Increase from 256Mi
    cpu: "250m" # Keep current
```

##### 3. Deprecated Airflow Configuration

**Issue**: Multiple deprecation warnings in logs

**Impact**: Low (warnings only, functionality not affected)

**Recommendation**: Update Airflow configuration:

```python
# In Airflow config or environment:
# 1. Change connection string
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql://...  # Change from postgres://

# 2. Update CLI usage in init containers to use:
airflow db migrate  # Instead of airflow db upgrade/init

# 3. Consider external rate limiting backend for production
```

##### 4. Single Point of Failure

**Issue**: Both pods running on same node (`aks-system-54209202-vmss000000`)

**Impact**: Medium (node failure affects entire deployment)

**Recommendation**:

```yaml
# Add pod anti-affinity rules to spread pods:
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchLabels:
              app.kubernetes.io/instance: thehyve-mkuh
          topologyKey: kubernetes.io/hostname
```

##### 5. No Ingress Configuration

**Issue**: Airflow UI not exposed outside cluster

**Impact**: Low (may be intentional for security)

**Recommendation**: If external access needed:

```yaml
# Add ingress configuration:
ingress:
  enabled: true
  annotations:
    nginx.ingress.kubernetes.io/auth-type: basic
  hosts:
    - host: thehyve-mkuh.fitfile.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: thehyve-mkuh-tls
      hosts:
        - thehyve-mkuh.fitfile.example.com
```

#### ✅ Positive Observations

1. **Stable Deployment**: 20 days uptime with zero restarts
2. **GitOps Compliance**: ArgoCD sync healthy with self-healing enabled
3. **Persistent Storage**: Using retain policy to prevent data loss
4. **Network Isolation**: PostgreSQL protected by network policy
5. **Resource Limits**: Scheduler has appropriate memory limit (24Gi)
6. **Health Monitoring**: Proper liveness and readiness probes configured

---

### Summary & Next Steps

#### System Health: ✅ HEALTHY

The **thehyve-mkuh** deployment is operating normally with all pods running and ArgoCD reporting healthy sync status. The system has demonstrated stability over the past 20 days with zero restarts.

#### Priority Actions

1. **High Priority**:
   - Fix image pull secret warnings (prevents future deployment issues)
   - Update PostgreSQL memory request to reflect actual usage

2. **Medium Priority**:
   - Address Airflow deprecation warnings in next release
   - Implement pod anti-affinity for better HA
   - Consider VPA for automatic resource right-sizing

3. **Low Priority**:
   - Evaluate need for external access via Ingress
   - Review RBAC permissions for least-privilege principle

#### Monitoring Recommendations

Add alerts for:

- Pod restart count > 3
- Memory usage > 90% of limit
- PVC storage usage > 80%
- ArgoCD sync failures
- Image pull failures

---

### Appendix: Quick Reference Commands

```bash
# Connect to Airflow webserver
kubectl port-forward -n thehyve-mkuh deployment/thehyve-mkuh 8080:8080

# Access PostgreSQL
kubectl exec -it -n thehyve-mkuh thehyve-mkuh-postgresql-0 -- psql -U postgres

# View live logs
kubectl logs -n thehyve-mkuh deployment/thehyve-mkuh -f --all-containers

# Check ArgoCD sync status
kubectl get application thehyve-mkuh -n argocd -o jsonpath='{.status.sync.status}'

# Force ArgoCD sync
kubectl patch application thehyve-mkuh -n argocd --type merge -p '{"operation":{"initiatedBy":{"username":"admin"},"sync":{"revision":"latest-release"}}}'

# Scale deployment (if needed)
# Note: ArgoCD will revert this unless changed in Git
kubectl scale deployment thehyve-mkuh -n thehyve-mkuh --replicas=1
```

---

Let me investigate the relationship between ff-c and thehyve by looking at the configuration and connections.

**Command Executed:**

```bash
kubectl get configmap thehyve-mkuh-postgresql-init-scripts -n thehyve-mkuh -o yaml
```

**Output:**

```sh
apiVersion: v1
data:
  00_init_dbs.sql: |
    CREATE DATABASE ohdsi;
    CREATE DATABASE airflow;
kind: ConfigMap
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","data":{"00_init_dbs.sql":"CREATE DATABASE ohdsi;\nCREATE DATABASE airflow;\n"},"kind":"ConfigMap","metadata":{"annotations":{},"labels":{"app.kubernetes.io/instance":"thehyve-mkuh","app.kubernetes.io/managed-by":"Helm","app.kubernetes.io/name":"postgresql","app.kubernetes.io/version":"16.3.0","argocd.argoproj.io/instance":"thehyve-mkuh","helm.sh/chart":"postgresql-15.5.15"},"name":"thehyve-mkuh-postgresql-init-scripts","namespace":"thehyve-mkuh"}}
  creationTimestamp: "2025-06-04T11:29:29Z"
  labels:
    app.kubernetes.io/instance: thehyve-mkuh
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: postgresql
    app.kubernetes.io/version: 16.3.0
    argocd.argoproj.io/instance: thehyve-mkuh
    helm.sh/chart: postgresql-15.5.15
  name: thehyve-mkuh-postgresql-init-scripts
  namespace: thehyve-mkuh
  resourceVersion: "156520414"
  uid: d301bd3c-4a61-4eb5-a70e-0701b7cc7b5d
```

**Command Executed:**

```bash
kubectl describe secret thehyve-mkuh -n thehyve-mkuh | grep -A 20 "Data"
```

**Output:**

```sh
Data
====
airflow_admin_email:           15 bytes
airflow_admin_firstname:       3 bytes
airflow_admin_lastname:        4 bytes
airflow_admin_password:        10 bytes
airflow_admin_username:        7 bytes
airflow_db_connection_string:  96 bytes
omop_db_connection_string:     83 bytes
```

Interesting! I can see there's an `omop_db_connection_string`. Let me check if I can find what ff-c is by looking at the services and databases in the cluster:

**Command Executed:**

```bash
kubectl get namespaces | grep -E "ff-c|fitfile"
```

**Output:**

```sh
ff-c                            Active   420d
```

Great! Let me explore the ff-c namespace:

**Command Executed:**

```bash
kubectl get svc -n ff-c | grep -i postgres
```

**Output:**

```sh

```

**Command Executed:**

```bash
kubectl get all -n ff-c
```

**Output:**

```sh
NAME                                       READY   STATUS    RESTARTS   AGE
pod/ff-c-ffcloud-service-55bdc94f6-8ntbz   3/3     Running   0          8d
pod/ff-c-fitconnect-ftc-565b86d9f8-np9rp   1/1     Running   0          8d
pod/workflows-api-69945c957d-24fsl         1/1     Running   0          8d

NAME                           TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
service/ff-c-ffcloud-service   ClusterIP   10.0.43.226   <none>        80/TCP    92d
service/ff-c-fitconnect-ftc    ClusterIP   10.0.74.58    <none>        80/TCP    420d
service/workflows-api          ClusterIP   10.0.75.101   <none>        80/TCP    420d

NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/ff-c-ffcloud-service   1/1     1            1           92d
deployment.apps/ff-c-fitconnect-ftc    1/1     1            1           420d
deployment.apps/workflows-api          1/1     1            1           420d

NAME                                              DESIRED   CURRENT   READY   AGE
replicaset.apps/ff-c-ffcloud-service-55bdc94f6    1         1         1       8d
replicaset.apps/ff-c-ffcloud-service-6578c586cc   0         0         0       30d
replicaset.apps/ff-c-fitconnect-ftc-565b86d9f8    1         1         1       8d
replicaset.apps/ff-c-fitconnect-ftc-6777fc4866    0         0         0       30d
replicaset.apps/workflows-api-69945c957d          1         1         1       8d
replicaset.apps/workflows-api-8468459865          0         0         0       30d
```

Now let me check the ArgoCD values file path mentioned in the deployment to understand the connection:

**Command Executed:**

```bash
kubectl get pods -n thehyve-mkuh -o jsonpath='{.items[0].spec.containers[*].env[*]}' | jq -r '. | select(.name | contains("OMOP")) | .name' 2>/dev/null || kubectl get deployment thehyve-mkuh -n thehyve-mkuh -o jsonpath='{.spec.template.spec.containers[*].env[*]}' | grep -i omop
```

**Output:**

```sh
OMOP_TARGET_DB
OMOP_TARGET_DB
```

Let me check what databases exist in the ff-c namespace that might have OMOP data:

**Command Executed:**

```bash
kubectl get statefulsets,deployments -n ff-c -o wide
```

**Output:**

```sh
NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE    CONTAINERS                                                IMAGES                                                                                                                                                  SELECTOR
deployment.apps/ff-c-ffcloud-service   1/1     1            1           92d    ff-c-ffcloud-service,ff-c-ffcloud-service-cli,scheduler   fitfileregistry.azurecr.io/ffcloud-service:1.0.699,fitfileregistry.azurecr.io/ffcloud-cli:1.0.49,fitfileregistry.azurecr.io/scheduler-service:1.0.282   app=ff-c-ffcloud-service
deployment.apps/ff-c-fitconnect-ftc    1/1     1            1           420d   ff-c-fitconnect-ftc                                       fitfileregistry.azurecr.io/fitconnect-service:1.0.633                                                                                                   app=ff-c-fitconnect-ftc
deployment.apps/workflows-api          1/1     1            1           420d   workflows-api                                             fitfileregistry.azurecr.io/dps/workflows-api:0.0.42                                                                                                     app=workflows-api
```

Let me check if there's a separate namespace or external database for OMOP. Let me look at the logs to see what database connection is being used:

**Command Executed:**

```bash
kubectl logs -n thehyve-mkuh deployment/thehyve-mkuh --tail=100 --all-containers=true | grep -i "omop\|connection\|database" | head -20
```

**Output:**

```sh
/home/airflow/.local/lib/python3.10/site-packages/airflow/configuration.py:819 DeprecationWarning: The sql_alchemy_conn option in [core] has been moved to the sql_alchemy_conn option in [database] - the old setting has been used, but please update your config.
/home/airflow/.local/lib/python3.10/site-packages/airflow/configuration.py:742 DeprecationWarning: The sql_alchemy_conn option in [core] has been moved to the sql_alchemy_conn option in [database] - the old setting has been used, but please update your config.
Performing upgrade to the metadata database postgresql://postgres:***@thehyve-mkuh-postgresql.thehyve-mkuh.svc.cluster.local:5432/airflow
Database migrating done!
/home/airflow/.local/lib/python3.10/site-packages/airflow/configuration.py:819 DeprecationWarning: The sql_alchemy_conn option in [core] has been moved to the sql_alchemy_conn option in [database] - the old setting has been used, but please update your config.
/home/airflow/.local/lib/python3.10/site-packages/airflow/configuration.py:742 DeprecationWarning: The sql_alchemy_conn option in [core] has been moved to the sql_alchemy_conn option in [database] - the old setting has been used, but please update your config.
/home/airflow/.local/lib/python3.10/site-packages/airflow/utils/providers_configuration_loader.py:55 DeprecationWarning: `db init` is deprecated.  Use `db migrate` instead to migrate the db and/or airflow connections create-default-connections to create the default connections
/home/airflow/.local/lib/python3.10/site-packages/airflow/utils/db.py:800 DeprecationWarning: The load_default_connections option in [core] has been moved to the load_default_connections option in [database] - the old setting has been used, but please update your config.
/home/airflow/.local/lib/python3.10/site-packages/airflow/configuration.py:819 DeprecationWarning: The sql_alchemy_conn option in [core] has been moved to the sql_alchemy_conn option in [database] - the old setting has been used, but please update your config.
/home/airflow/.local/lib/python3.10/site-packages/airflow/configuration.py:742 DeprecationWarning: The sql_alchemy_conn option in [core] has been moved to the sql_alchemy_conn option in [database] - the old setting has been used, but please update your config.
```

Let me check if there's a PostgreSQL or database in a different namespace that hosts OMOP data:

**Command Executed:**

```bash
kubectl get svc -A | grep -E "postgres|database|omop" | grep -v thehyve-mkuh
```

**Output:**

```sh
barts                           barts-postgresql                                  ClusterIP      10.0.241.127   <none>           5432/TCP                                420d
barts                           barts-postgresql-hl                               ClusterIP      None           <none>           5432/TCP                                420d
ff-a                            ff-a-postgresql                                   ClusterIP      10.0.198.246   <none>           5432/TCP                                420d
ff-a                            ff-a-postgresql-hl                                ClusterIP      None           <none>           5432/TCP                                420d
primary-care                    primary-care-postgresql                           ClusterIP      10.0.101.92    <none>           5432/TCP                                420d
primary-care                    primary-care-postgresql-hl                        ClusterIP      None           <none>           5432/TCP                                420d
spicedb                         spicedb-postgresql                                ClusterIP      10.0.136.164   <none>           5432/TCP                                420d
spicedb                         spicedb-postgresql-hl                             ClusterIP      None           <none>           5432/TCP                                420d
thehyve-cuh                     thehyve-cuh-postgresql                            ClusterIP      10.0.187.215   <none>           5432/TCP                                141d
thehyve-cuh                     thehyve-cuh-postgresql-hl                         ClusterIP      None           <none>           5432/TCP                                141d
thehyve                         thehyve-postgresql                                ClusterIP      10.0.76.130    <none>           5432/TCP                                224d
thehyve                         thehyve-postgresql-hl                             ClusterIP      None           <none>           5432/TCP                                224d
```

Perfect! Now I can see there are multiple database instances. Let me look more closely at the ff-c deployment to understand what database it uses:

**Command Executed:**

```bash
kubectl describe deployment ff-c-ffcloud-service -n ff-c | grep -A 30 "Environment:" | head -40
```

**Output:**

```sh
    Environment:
      NODE_ENV:                   production
      FITFILE_ENV:                production
      TENANT_SIGNING_PUBLIC_KEY:  <set to the key 'public.crt' in secret 'fitfile-rsa-private-key'>  Optional: true
    Mounts:
      /config from config (ro)
      /secrets from ffcloud-secrets (ro)
  Containers:
   ff-c-ffcloud-service:
    Image:      fitfileregistry.azurecr.io/ffcloud-service:1.0.699
    Port:       4000/TCP (http)
    Host Port:  0/TCP (http)
    Requests:
      cpu:      100m
    Liveness:   http-get http://:4000/ffcloud delay=15s timeout=12s period=15s #success=1 #failure=3
    Readiness:  http-get http://:4000/ffcloud delay=15s timeout=12s period=15s #success=1 #failure=3
    Environment:
      NODE_ENV:     production
      FITFILE_ENV:  production
    Mounts:
      /config from config (ro)
      /secrets from ffcloud-secrets (ro)
   ff-c-ffcloud-service-cli:
    Image:      fitfileregistry.azurecr.io/ffcloud-cli:1.0.49
    Port:       <none>
    Host Port:  <none>
    Environment:
      NODE_ENV:     production
      FITFILE_ENV:  production
    Mounts:
      /config from cli-config (ro)
   scheduler:
    Image:      fitfileregistry.azurecr.io/scheduler-service:1.0.282
    Port:       4001/TCP
    Host Port:  0/TCP
    Environment:
      NODE_ENV:     production
      FITFILE_ENV:  production
    Mounts:
      /config from scheduler-config (ro)
```

Let me check what secrets and config maps are being mounted to understand the database connections:

**Command Executed:**

```bash
kubectl get configmap -n ff-c -o name | head -10
```

**Output:**

```sh
configmap/artifact-repositories
configmap/ff-c-ffcloud-service-cli-config-ec35c472fc0b3d71b957ddc06d04d42
configmap/ff-c-ffcloud-service-config-8126f0f8d27a30ed69c6b747636d3b84495
configmap/ff-c-ffcloud-service-scheduler-config-f39aec33c712cf410c4296cbb
configmap/ff-c-fitconnect-ftc-config-eabd13196efa771d44c90f6b8680862242d1
configmap/fitconnect-load-definition
configmap/kube-root-ca.crt
configmap/load-data-cli-load-definition
configmap/load-data-config
configmap/submit-mesh-request-load-definition
```

Let me check a different approach - look at what DAGs (Airflow workflows) exist in thehyve to understand what it does:

**Command Executed:**

```bash
kubectl exec -n thehyve-mkuh deployment/thehyve-mkuh -c webserver -- ls -la /opt/airflow/dags/ 2>/dev/null || echo "Cannot access DAGs directory"
```

**Output:**

```sh
total 40
drwxrwxr-x 1 airflow root 4096 May 20 13:59 .
drwxrwxr-x 1 airflow root 4096 Oct  3 02:45 ..
-rw-rw-r-- 1 airflow root  596 Mar  1  2025 load_restricted_codes.py
-rw-rw-r-- 1 airflow root  549 Feb 15  2025 load_source_data.py
-rw-rw-r-- 1 airflow root  564 Feb 15  2025 load_vocabularies.py
-rw-rw-r-- 1 airflow root  526 Mar  1  2025 run_achilles.py
-rw-rw-r-- 1 airflow root  556 May 20 13:59 run_cdmOnboarding.py
-rw-rw-r-- 1 airflow root  515 Mar  1  2025 run_dqd.py
-rw-rw-r-- 1 airflow root  498 Feb 11  2025 run_etl.py
-rw-rw-r-- 1 airflow root  583 Mar  1  2025 source_to_filtered.py
```

Excellent! Now let me look at one of these DAG files to understand the data flow:

**Command Executed:**

```bash
kubectl exec -n thehyve-mkuh deployment/thehyve-mkuh -c webserver -- cat /opt/airflow/dags/load_source_data.py
```

**Output:**

```sh
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# Define the DAG
dag = DAG(
    'load_source_data',
    description='Loads the source data into the database',
    schedule_interval=None,
    start_date=datetime(2023, 3, 22),
    catchup=False
)

# Define the BashOperator task
load_source_data_task = BashOperator(
    task_id='load_source_data_task',
    bash_command='cd /home/airflow/etl; ./load_source_data.sh ',
    dag=dag
)

# Define the task dependencies
load_source_data_task
```

**Command Executed:**

```bash
kubectl exec -n thehyve-mkuh deployment/thehyve-mkuh -c webserver -- cat /opt/airflow/dags/run_etl.py
```

**Output:**

```sh
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# Define the DAG
dag = DAG(
    'run_etl',
    description='Runs the NHS to OMOP ETL pipeline',
    schedule_interval=None,
    start_date=datetime(2023, 3, 22),
    catchup=False
)

# Define the BashOperator task
run_etl_task = BashOperator(
    task_id='run_etl_task',
    bash_command='cd /home/airflow/etl; ./etl_run.sh ',
    dag=dag
)

# Define the task dependencies
run_etl_task
```

Perfect! Now let me check the ETL scripts to see where data comes from:

**Command Executed:**

```bash
kubectl exec -n thehyve-mkuh deployment/thehyve-mkuh -c webserver -- cat /home/airflow/etl/load_source_data.sh | head -50
```

**Output:**

```sh
#!/usr/bin/env bash

#
# This script can be used to (re-)load the CUH synthetic data into the `source_data` schema.
#
# Loading the source data is a pragmatic approach for POC 1, so this
# script contains some pragmatic hacks to make the sql scripts work.
#

# get DB connection info
# shellcheck disable=SC1091
source "$(dirname "$0")/setupEtlConfiguration.sh" "load_source_data"

loadDatabaseConfiguration

SOURCEDATACSVPATH=$(getEnvironmentOption "/home/airflow/etl/resources/synthetic_data" "$SOURCEDATACSVPATH" "directory")

ETL_CONFIG_PATH=$(getEnvironmentOption "/home/airflow/etl/config" "$TEST_ETL_CONFIG_PATH" "directory")
ETL_CONFIG_TEMPLATE="config-${NHS_SITE}.yml"
ETL_CONFIG_OUT="config-etl.yml"

prepareEtlConfiguration "$ETL_CONFIG_PATH" "$ETL_CONFIG_TEMPLATE" "$ETL_CONFIG_OUT"

python3 load_source_data.py --overwrite --source-dir "$SOURCEDATACSVPATH" -c "$ETL_CONFIG_PATH/$ETL_CONFIG_OUT" 2>&1 | tee "${QC_LOGFILE:-/tmp/load_source_data.log}"
```

Let me check the ETL configuration setup to see database connections:

**Command Executed:**

```bash
kubectl exec -n thehyve-mkuh deployment/thehyve-mkuh -c webserver -- cat /home/airflow/etl/setupEtlConfiguration.sh | grep -A 10 -B 5 "OMOP\|ff-c\|source"
```

**Output:**

```sh
mkdir -p "$QC_LOGPATH"
NOW=$(date +%Y-%m-%d-%H.%M.%S)
export QC_LOGFILE="$QC_LOGPATH/${1:-unknown-job}-$NOW.log"

function loadDatabaseConfiguration() {
 # assumption: OMOP_TARGET_DB = "user:password@host:port/database" (:port is optional)
 if [ -z "$OMOP_TARGET_DB" ]; then
  echo "env. var. OMOP_TARGET_DB has no value. Stop."
  exit 1
 fi

 parsed_pg=$(echo "$OMOP_TARGET_DB" | gawk '
 match($0, /^([^:]+):([^@]+)@([^/]+)\/(.*)$/, a) {
  pguser = a[1]
  pgpwd = a[2]
  pghost_port = a[3]
  pgdatabase = a[4]
  if (match(pghost_port, /^([^:]+):(.*)$/, aa)) {
   pghost = aa[1]
   pgport = aa[2]
  } else {
   pghost = pghost_port
--
  -e "s/^\s*database_name:.*$/  database_name: $PGDB/" \
  -e "s/^\s*username:.*$/  username: $PGUSER/" \
  -e "s/^\s*password:.*$/  password: $PGPWD/" \
  < "$configPath/$configIn" > "$configPath/$configOut"

 cp "$configPath/source_config-sample.yml" "$configPath/source_config.yml"
}
```

Now let me check the config files to understand the source database:

**Command Executed:**

```bash
kubectl exec -n thehyve-mkuh deployment/thehyve-mkuh -c webserver -- ls -la /home/airflow/etl/config/ | grep -E "config|yml"
```

**Output:**

```sh
-rw-r--r-- 1 airflow root  412 May 23 09:00 config-mkuh.yml
-rw-rw-r-- 1 airflow 1000  462 May 23 08:07 config-sample.yml
-rw-rw-r-- 1 airflow 1000  392 May 23 08:07 logging-sample.yml
-rw-rw-r-- 1 airflow 1000  263 May 23 08:07 source_config-sample.yml
-rw-rw-r-- 1 airflow 1000  177 May 23 08:07 vocab_config-sample.yml
```

**Command Executed:**

```bash
kubectl exec -n thehyve-mkuh deployment/thehyve-mkuh -c webserver -- cat /home/airflow/etl/config/config-mkuh.yml
```

**Output:**

```sh
database:
  drivername: 'postgresql'
  host: '127.0.0.1'  # (localhost)
  port: 5432
  database_name: 'ohdsi'
  username: 'postgres'
  password:
  query:

schema_translate_map:
  cdm_schema: 'cdm'
  vocabulary_schema: 'vocab'
  source_schema: 'source_data'

run_options:
  load_vocabulary: F
  load_custom_vocabulary: T
  load_source_to_concept_map: T
  write_reports: F

sql_parameters:
  #placeholder: 'value'
```

Now let me check if there's any reference to ff-c in the environment or documentation:

**Command Executed:**

```bash
kubectl exec -n thehyve-mkuh deployment/thehyve-mkuh -c webserver -- env | grep -i "ff-c\|source\|fitfile" | head -10
```

**Output:**

```sh
AIRFLOW_ADMIN_EMAIL=ops@fitfile.com
```

Based on my investigation, I can now provide you with a clear answer about the relationship between ff-c and thehyve-mkuh:

## Answer: The Hyve DOES NOT Read Data From Ff-c

Based on my investigation, here's what I found:

### Data Flow Architecture

**thehyve-mkuh** is an **ETL (Extract, Transform, Load)** pipeline that:

1. **Reads from**: Local synthetic/test data stored in `/home/airflow/etl/resources/synthetic_data`
2. **Transforms to**: OMOP CDM (Common Data Model) format
3. **Writes to**: Its own PostgreSQL database (`thehyve-mkuh-postgresql`) in the `ohdsi` database with schemas:
   - `source_data` - raw NHS data
   - `cdm` - OMOP CDM transformed data
   - `vocab` - OMOP vocabulary/terminology

### What Thehyve-mkuh Does

The Airflow DAGs show it performs:

- **load_source_data** - Loads NHS source data into the source_data schema
- **run_etl** - Transforms NHS data to OMOP format
- **load_vocabularies** - Loads OMOP standard vocabularies
- **run_achilles** - Runs data quality and characterization
- **run_dqd** - Data Quality Dashboard
- **run_cdmOnboarding** - OMOP CDM onboarding processes

### What Ff-c Is

**ff-c** appears to be a **FITFILE Cloud service namespace** containing:

- `ff-c-ffcloud-service` - Main FITFILE cloud application (3 containers: service, CLI, scheduler)
- `ff-c-fitconnect-ftc` - FitConnect service
- `workflows-api` - Workflow management API

These are application services, not data sources for thehyve.

### Key Insight

The `OMOP_TARGET_DB` environment variable in thehyve-mkuh points to its **own** PostgreSQL instance (`thehyve-mkuh-postgresql.thehyve-mkuh.svc.cluster.local`), not to ff-c or any external database.

**The data flow is self-contained**: Source data → thehyve ETL → OMOP database (same namespace)

There's **no direct connection** between ff-c and thehyve-mkuh based on the current cluster configuration.

Let me investigate where the thehyve-mkuh configuration is managed and how to properly add variables.

**Command Executed:**

```bash
kubectl get application thehyve-mkuh -n argocd -o jsonpath='{.spec.source.helm.valueFiles}'
```

**Output:**

```sh
["/ffnodes/fitfile/ff-c/thehyve_values.yaml"]%
```

**Command Executed:**

```bash
kubectl get application thehyve-mkuh -n argocd -o jsonpath='{.spec.source.repoURL}'
```

**Output:**

```sh
https://gitlab.com/fitfile/deployment.git%
```

Now let me check if there's a local checkout of the deployment repo:

**Command Executed:**

```bash
find /Volumes/DAL/Fitfile/gitlab -maxdepth 3 -type d -name "deployment" -o -name "*deploy*" 2>/dev/null | grep -v node_modules | head -5
```

**Output:**

```sh
/Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/deployment-v2
/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment
```

**Command Executed:**

```bash
ls -la /Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ | head -20
```

**Output:**

```sh
total 280
drwxr-xr-x@ 28 leon.ormes  staff   896B 16 Oct 10:10 .
drwxr-xr-x@  7 leon.ormes  staff   224B  6 Oct 09:55 ..
-rw-r--r--@  1 leon.ormes  staff   6.0K  4 Sep 12:04 .DS_Store
drwxr-xr-x@ 18 leon.ormes  staff   576B 23 Oct 09:57 .git
-rw-r--r--@  1 leon.ormes  staff   347B  6 Sep 09:19 .gitignore
-rw-r--r--@  1 leon.ormes  staff   3.7K  2 Jul 14:26 .gitlab-ci.yml
drwxr-xr-x@ 19 leon.ormes  staff   608B 11 Oct 11:50 charts
drwxr-xr-x@  9 leon.ormes  staff   288B  7 Jan  2025 ffnodes
-rw-r--r--@  1 leon.ormes  staff   3.5K  5 Mar  2025 LOCALDEV_README.md
-rw-r--r--@  1 leon.ormes  staff   2.8K 16 Oct 10:10 Makefile
-rw-------@  1 leon.ormes  staff    10K 29 Jul 16:09 nohup.out
-rwxr-xr-x@  1 leon.ormes  staff   1.8K 29 Jul 13:32 pf.sh
drwxr-xr-x@  3 leon.ormes  staff    96B  7 Jan  2025 pipeline
drwxr-xr-x@ 11 leon.ormes  staff   352B 16 Oct 10:10 policies
-rw-r--r--@  1 leon.ormes  staff   763B  6 Feb  2025 README.md
-rwxr-xr-x@  1 leon.ormes  staff    18K 20 Sep 11:59 release-improved.sh
-rw-r--r--@  1 leon.ormes  staff   5.9K 20 Sep 11:59 release.log
-rwxr-xr-x@  1 leon.ormes  staff   7.0K 13 Feb  2025 release.sh
-rw-r--r--@  1 leon.ormes  staff   128B  7 Jan  2025 renovate.json
```

Perfect! Let me check the values file:

**Command Executed:**

```bash
find /Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment -path "*/ffnodes/fitfile/ff-c/thehyve_values.yaml" -o -path "*/thehyve*.yaml" 2>/dev/null | head -5
```

**Output:**

```sh
/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/fitfile/ff-c/thehyve_values.yaml
/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/fitfile/ff-b/thehyve_values.yaml
/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/fitfile/ff-a/thehyve_values.yaml
/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/eoe/hie-prod-34/thehyve_values.yaml
/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/integrations/thehyve/Chart.yaml
```

**Files Read:**

**/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/fitfile/ff-c/thehyve_values.yaml**

```sh
global:
  imagePullSecrets:
    - name: fitfile-image-pull-secret

image:
  # NOTE: Import the hyve container into our ACR with tag "latest"
  # NOTE: This is so you can delete the pod in thehyve namespace, and it will pull the "latest" tag
  pullPolicy: Always
  repository: fitfileregistry.azurecr.io/thehyve/fitfile_etl_container_mkuh
  tag: 0.4.2

extraEnvVars:
  - name: NHS_SITE
    value: mkuh
  - name: QCR_BUCKET
    valueFrom:
      secretKeyRef:
        name: thehyve
        key: qcr_bucket
  - name: QCR_ACCES_KEY_ID
    valueFrom:
      secretKeyRef:
        name: thehyve
        key: qcr_access_key_id
  - name: QCR_SECRET_ACCESS_KEY
    valueFrom:
      secretKeyRef:
        name: thehyve
        key: qcr_secret_access_key
  - name: QCR_IAM_ROLE
    valueFrom:
      secretKeyRef:
        name: thehyve
        key: qcr_iam_role

omop:
  db:
    host: "thehyve-mkuh-postgresql.thehyve-mkuh.svc.cluster.local"
    auth:
      username: "postgres"
      password: "postgres"
    dbName: "ohdsi"

# The hyve container has airflow user with 50000 UID
securityContext:
  runAsUser: 50000
  runAsGroup: 50000

airflow:
  db:
    host: "thehyve-mkuh-postgresql.thehyve-mkuh.svc.cluster.local"
    auth:
      username: "postgres"
      password: "postgres"
    dbName: "airflow"
  initAdmin:
    enabled: true
    username: "ffadmin"
    password: "ffpassword"
    firstname: "fit"
    lastname: "file"
    email: "ops@fitfile.com"

scheduler:
  resources:
    requests:
      cpu: "125m"
      memory: 128Mi

webserver:
  resources:
    requests:
      cpu: "250m"
      memory: 512Mi

postgresql:
  enabled: true
  auth:
    username: "postgres"
    password: "postgres"
  primary:
    resources:
      requests:
        cpu: 250m
        memory: 256Mi
    initdb:
      user: postgres
      scripts:
        00_init_dbs.sql: |
          CREATE DATABASE ohdsi;
          CREATE DATABASE airflow;
    persistence:
      size: 20Gi

extraDeploy:
  - apiVersion: secrets.hashicorp.com/v1beta1
    kind: VaultStaticSecret
    metadata:
      name: thehyve
      namespace: "{{ .Release.Namespace }}"
    spec:
      # Vault namespace where the secrets backend is
      namespace: admin/deployments/ff-c
      # Vault mount path of the secrets backend
      mount: secrets
      # Vault path in secrets engine mount to the secret
      path: thehyve
      # Type of the Vault static secret
      type: kv-v2
      # Used for environment drift detection. Should always be on
      hmacSecretData: true
      # Where to store the secrets, VSO will create the secret
      destination:
        create: true
        name: thehyve
        # Transform thehyve secrets
        transformation:
          excludes:
            - .*
          templates:
            qcr_bucket:
              text: '{{`{{get .Secrets "qcr_bucket"}}`}}'
            qcr_access_key_id:
              text: '{{`{{get .Secrets "qcr_access_key_id"}}`}}'
            qcr_secret_access_key:
              text: '{{`{{get .Secrets "qcr_secret_access_key"}}`}}'
            qcr_iam_role:
              text: '{{`{{get .Secrets "qcr_iam_role"}}`}}'
      # Restart these pods when secrets rotated
      rolloutRestartTargets:
        - kind: Deployment
          name: '{{ include "thehyve.fullname" . }}'
      # Refresh interval
      refreshAfter: 10m
      # Name of the CRD to authenticate to Vault
      vaultAuthRef: default

```

Perfect! Now let me check the Helm chart to understand the secret structure:

**Command Executed:**

```bash
find /Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/integrations/thehyve -name "*.yaml" -o -name "*.tpl" 2>/dev/null | head -10
```

**Output:**

```sh
/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/integrations/thehyve/Chart.yaml
/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/integrations/thehyve/templates/deployment.yaml
/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/integrations/thehyve/templates/ingress.yaml
/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/integrations/thehyve/templates/extra-deploy.yaml
/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/integrations/thehyve/templates/service.yaml
/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/integrations/thehyve/templates/serviceaccount.yaml
/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/integrations/thehyve/templates/_helpers.tpl
/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/integrations/thehyve/templates/secret.yaml
/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/integrations/thehyve/templates/persistentvolumeclaim.yaml
/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/integrations/thehyve/values.yaml
```

**Files Read:**

**/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/integrations/thehyve/templates/secret.yaml**

```sh
{{- if and (and .Values.omop.db.auth.existingSecretName .Values.airflow.db.auth.existingSecretName) (and .Values.airflow.initAdmin.enabled .Values.airflow.initAdmin.existingSecretName) -}}
{{- else -}}
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "thehyve.name" . }}
data:
  {{- if .Values.omop.db.auth.existingSecretName -}}
  {{ else }}
  {{- with .Values.omop.db }}
  omop_db_connection_string: {{ list (required "omop.db.auth.username is required if not using existing secret" .auth.username) ":" (required "omop.db.auth.password is required if not using existing secret" .auth.password) "@" (required "omop.db.host is required if not using existing secret" .host) ":" .port "/" .dbName | join ""  | b64enc |  quote }}
  {{- end -}}
  {{- end -}}
  {{- if .Values.airflow.db.auth.existingSecretName }}
  {{ else }}
  {{- with .Values.airflow.db }}
  airflow_db_connection_string: {{ list "postgres://" (required "airflow.db.auth.username is required if not using existing secret" .auth.username) ":" (required "airflow.db.auth.password is required if not using existing secret" .auth.password) "@" (required "airflow.db.host is required if not using existing secret" .host) ":" .port "/" .dbName | join ""  | b64enc |  quote }}
  {{- end -}}
  {{- end }}

  {{- if .Values.airflow.initAdmin.existingSecretName }}
  {{ else if .Values.airflow.initAdmin.enabled }}
  {{- with .Values.airflow.initAdmin }}
  airflow_admin_username: {{ required "airflow.initAdmin.username is required if not using existing secret" .username | b64enc |  quote }}
  airflow_admin_password: {{ required "airflow.initAdmin.password is required if not using existing secret" .password | b64enc |  quote }}
  airflow_admin_firstname: {{ required "airflow.initAdmin.firstname is required if not using existing secret" .firstname | b64enc |  quote }}
  airflow_admin_lastname: {{ required "airflow.initAdmin.lastname is required if not using existing secret" .lastname | b64enc |  quote }}
  airflow_admin_email: {{ required "airflow.initAdmin.email is required if not using existing secret" .email | b64enc |  quote }}
  {{- end -}}
  {{- end }}
{{- end -}}



```

Now let me check how the extraEnvVars are used:

**Files Read:**

**/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/integrations/thehyve/templates/deployment.yaml**

```sh
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "thehyve.fullname" . }}
  labels:
    {{- include "thehyve.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "thehyve.selectorLabels" . | nindent 6 }}
  strategy:
    # Means we don't get a MultiAttachVolume error when deploying updates
    type: Recreate
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "thehyve.labels" . | nindent 8 }}
        {{- with .Values.podLabels }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
    spec:
      {{- include "thehyve.imagePullSecrets" . | nindent 6 }}
      serviceAccountName: {{ include "thehyve.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      initContainers:
        - name: thehyve-init
          image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
          imagePullPolicy: Always
          command: ['/bin/bash', '-c']
          securityContext:
            {{- toYaml .Values.initSecurityContext | nindent 12 }}
          args:
            - |
              chown -R 50000:50000 /tmp/reports;
              airflow db upgrade && \
              sleep 5 && \
              airflow db init && \
              {{- if .Values.airflow.initAdmin.enabled }}
              airflow users create \
                  --username $AIRFLOW_ADMIN_USERNAME \
                  --password $AIRFLOW_ADMIN_PASSWORD \
                  --firstname $AIRFLOW_ADMIN_FIRSTNAME \
                  --lastname $AIRFLOW_ADMIN_LASTNAME \
                  --role Admin \
                  --email $AIRFLOW_ADMIN_EMAIL
              {{- else -}}
              echo "Init admin is not enabled"
              {{- end }}
          env: {{ include "thehyve.env" . | nindent 10 }}
          volumeMounts: {{ include "thehyve.volumeMounts.scheduler" . | fromYamlArray | toYaml | nindent 12 }}
      containers:
        - name: webserver
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          resources: {{ toYaml .Values.webserver.resources | nindent 12 }}
          command: ["airflow", "webserver"]
          ports:
            - name: http
              containerPort: {{ .Values.service.port }}
              protocol: TCP
          livenessProbe:
            {{- toYaml .Values.livenessProbe | nindent 12 }}
          readinessProbe:
            {{- toYaml .Values.readinessProbe | nindent 12 }}
          volumeMounts: {{ include "thehyve.volumeMounts.webserver" . | fromYamlArray | toYaml | nindent 12 }}
          env: {{ include "thehyve.env" . | fromYamlArray | toYaml | nindent 12 }}
        - name: scheduler
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          resources: {{ toYaml .Values.scheduler.resources | nindent 12 }}
          command: ["airflow", "scheduler"]
          volumeMounts: {{ include "thehyve.volumeMounts.scheduler" . | fromYamlArray | toYaml | nindent 12 }}
          env: {{ include "thehyve.env" . | fromYamlArray | toYaml | nindent 12 }}
      volumes: {{ include "thehyve.volumes" . | fromYamlArray | toYaml | nindent 8 }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}

```

**Files Read:**

**/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/charts/integrations/thehyve/templates/\_helpers.tpl**

```sh
{{/*
Expand the name of the chart.
*/}}
{{- define "thehyve.name" -}}
{{- default .Release.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified buny app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "thehyve.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := include "thehyve.name" . }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "thehyve.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "thehyve.labels" -}}
helm.sh/chart: {{ include "thehyve.chart" . }}
{{ include "thehyve.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "thehyve.selectorLabels" -}}
app.kubernetes.io/name: {{ include "thehyve.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "thehyve.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "thehyve.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

- name: OMOP_TARGET_DB
  value: {{ include "db.omop" . }}
- name: AIRFLOW__CORE__SQL_ALCHEMY_CONN
  value: {{ include "db.airflow" . }}
- name: AIRFLOW__CORE__STORE_DAG_CODE
  value: "True"
- name: AIRFLOW__CORE__STORE_SERIALIZED_DAGS
  value: "True"
- name: AIRFLOW__WEBSERVER__EXPOSE_CONFIG
  value: "True"
- name: AIRFLOW__WEBSERVER__RBAC
  value: "False"
- name: AIRFLOW__CORE__EXECUTOR
  value: "LocalExecutor"
- name: AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS
  value: "False"
- name: AIRFLOW__CORE__LOAD_EXAMPLES
  value: "False"

{{/*
Default environment variables for the containers
*/}}
{{- define "thehyve.env.defaults" -}}
{{- $envVars := list }}

{{- if .Values.omop.db.auth.existingSecretKey }}
  {{- $envVars = append $envVars (dict "name" "OMOP_TARGET_DB" "valueFrom" (dict "secretKeyRef" (dict "name" .Values.omop.db.auth.existingSecretName "key" .Values.omop.db.auth.existingSecretConnectionStringKey))) }}
{{- else }}
  {{- $envVars = append $envVars (dict "name" "OMOP_TARGET_DB" "valueFrom" (dict "secretKeyRef" (dict "name" (include "thehyve.name" .) "key" "omop_db_connection_string"))) }}
{{- end }}

{{- if .Values.airflow.db.auth.existingSecretKey }}
  {{- $envVars = append $envVars (dict "name" "AIRFLOW__CORE__SQL_ALCHEMY_CONN" "valueFrom" (dict "secretKeyRef" (dict "name" .Values.airflow.db.auth.existingSecretName "key" .Values.airflow.db.auth.existingSecretConnectionStringKey))) }}
{{- else }}
  {{- $envVars = append $envVars (dict "name" "AIRFLOW__CORE__SQL_ALCHEMY_CONN" "valueFrom" (dict "secretKeyRef" (dict "name" (include "thehyve.name" .) "key" "airflow_db_connection_string"))) }}
{{- end }}

{{- $envVars = append $envVars (dict "name" "AIRFLOW__CORE__STORE_DAG_CODE" "value" "True") }}
{{- $envVars = append $envVars (dict "name" "AIRFLOW__CORE__STORE_SERIALIZED_DAGS" "value" "True") }}
{{- $envVars = append $envVars (dict "name" "AIRFLOW__WEBSERVER__EXPOSE_CONFIG" "value" "True") }}
{{- $envVars = append $envVars (dict "name" "AIRFLOW__WEBSERVER__RBAC" "value" "False") }}
{{- $envVars = append $envVars (dict "name" "AIRFLOW__CORE__EXECUTOR" "value" "LocalExecutor") }}
{{- $envVars = append $envVars (dict "name" "AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS" "value" "False") }}
{{- $envVars = append $envVars (dict "name" "AIRFLOW__CORE__LOAD_EXAMPLES" "value" "False") }}

{{- if .Values.airflow.initAdmin.existingSecretKey }}
  {{- $envVars = append $envVars (dict "name" "AIRFLOW_ADMIN_USERNAME" "valueFrom" (dict "secretKeyRef" (dict "name" .Values.airflow.initAdmin.existingSecretName "key" .Values.airflow.initAdmin.existingSecretUsernameKey))) }}
  {{- $envVars = append $envVars (dict "name" "AIRFLOW_ADMIN_PASSWORD" "valueFrom" (dict "secretKeyRef" (dict "name" .Values.airflow.initAdmin.existingSecretName "key" .Values.airflow.initAdmin.existingSecretPasswordKey))) }}
  {{- $envVars = append $envVars (dict "name" "AIRFLOW_ADMIN_FIRSTNAME" "valueFrom" (dict "secretKeyRef" (dict "name" .Values.airflow.initAdmin.existingSecretName "key" .Values.airflow.initAdmin.existingSecretFirstnameKey))) }}
  {{- $envVars = append $envVars (dict "name" "AIRFLOW_ADMIN_LASTNAME" "valueFrom" (dict "secretKeyRef" (dict "name" .Values.airflow.initAdmin.existingSecretName "key" .Values.airflow.initAdmin.existingSecretLastnameKey))) }}
  {{- $envVars = append $envVars (dict "name" "AIRFLOW_ADMIN_EMAIL" "valueFrom" (dict "secretKeyRef" (dict "name" .Values.airflow.initAdmin.existingSecretName "key" .Values.airflow.initAdmin.existingSecretEmailKey))) }}
{{- else }}
  {{- $envVars = append $envVars (dict "name" "AIRFLOW_ADMIN_USERNAME" "valueFrom" (dict "secretKeyRef" (dict "name" (include "thehyve.name" .) "key" "airflow_admin_username"))) }}
  {{- $envVars = append $envVars (dict "name" "AIRFLOW_ADMIN_PASSWORD" "valueFrom" (dict "secretKeyRef" (dict "name" (include "thehyve.name" .) "key" "airflow_admin_password"))) }}
  {{- $envVars = append $envVars (dict "name" "AIRFLOW_ADMIN_FIRSTNAME" "valueFrom" (dict "secretKeyRef" (dict "name" (include "thehyve.name" .) "key" "airflow_admin_firstname"))) }}
  {{- $envVars = append $envVars (dict "name" "AIRFLOW_ADMIN_LASTNAME" "valueFrom" (dict "secretKeyRef" (dict "name" (include "thehyve.name" .) "key" "airflow_admin_lastname"))) }}
  {{- $envVars = append $envVars (dict "name" "AIRFLOW_ADMIN_EMAIL" "valueFrom" (dict "secretKeyRef" (dict "name" (include "thehyve.name" .) "key" "airflow_admin_email"))) }}
{{- end }}


{{- toYaml $envVars }}
{{- end -}}

{{/*
Fully compiled environment variables to supply to the containers
*/}}
{{- define "thehyve.env" -}}
{{- $defaults := include "thehyve.env.defaults" . | fromYamlArray -}}
{{- $extra := .Values.extraEnvVars | default list -}}
{{- $listOfLists := list $defaults $extra -}}
{{- $merged := dict -}}
{{- /* Load defaults into merged dict */ -}}
{{- range $listOfLists }}
  {{- range . }}
    {{- $_ := set $merged .name . }}
  {{- end }}
{{- end }}
{{- /* Convert merged dict back into a list */ -}}
{{- $mergedList := list }}
{{- range $merged }}
  {{- $mergedList = append $mergedList . }}
{{- end }}
{{- toYaml $mergedList | nindent 0 }}
{{- end -}}

{{- define "thehyve.volumeMounts.webserver" -}}
  {{- $volumeMounts := list }}
  {{- $volumeMounts = append $volumeMounts (dict "mountPath" "/tmp/reports" "name" "reports") -}}

  {{- range (.Values.volumeMounts) -}}
    {{- $volumeMounts = append $volumeMounts . -}}
  {{- end -}}

{{- toYaml $volumeMounts | nindent 0 }}
{{- end -}}

{{- define "thehyve.volumeMounts.scheduler" -}}
  {{- $volumeMounts := list }}
  {{- $volumeMounts = append $volumeMounts (dict "mountPath" "/tmp/reports" "name" "reports") -}}

{{- toYaml $volumeMounts | nindent 0 }}
{{- end -}}

{{- define "thehyve.volumes" -}}
  {{- $volumes := list }}
  {{- $volumes = append $volumes (dict "name" "reports" "persistentVolumeClaim" (dict "claimName" (printf "%s-reports" (include "thehyve.fullname" .)))) -}}

  {{- range (.Values.volumes) -}}
    {{- $volumes = append $volumes . -}}
  {{- end -}}

{{- toYaml $volumes | nindent 0 }}
{{- end -}}


{{/*
Return the proper Docker Image Registry Secret Names
{{ include "hutch.bunny.imagePullSecrets" . }}
*/}}
{{- define "thehyve.imagePullSecrets" -}}
  {{- $pullSecrets := list }}
  {{- $localPullSecrets := .Values.imagePullSecrets -}}

  {{- range ((.Values.global).imagePullSecrets) -}}
    {{- if kindIs "map" . -}}
      {{- $pullSecrets = append $pullSecrets .name -}}
    {{- else -}}
      {{- $pullSecrets = append $pullSecrets . -}}
    {{- end }}
  {{- end -}}

  {{- range $localPullSecrets -}}
    {{- if kindIs "map" . -}}
      {{- $pullSecrets = append $pullSecrets .name -}}
    {{- else -}}
      {{- $pullSecrets = append $pullSecrets . -}}
    {{- end -}}
  {{- end -}}

  {{- if (not (empty $pullSecrets)) -}}
imagePullSecrets:
    {{- range $pullSecrets | uniq }}
  - name: {{ . }}
    {{- end }}
  {{- end }}
{{- end -}}

```

Perfect! Now I have all the information needed. Let me create a comprehensive guide for you:

**Diff:**

````diff
--- /Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/trivy-report/thehyve-mkuh-add-variables-guide.md
+++ /Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/trivy-report/thehyve-mkuh-add-variables-guide.md
@@ -0,0 +1,453 @@
+# Adding Variables to thehyve-mkuh Deployment
+
+## Overview
+
+This guide explains how to add environment variables to the **thehyve-mkuh** deployment, including both configuration file changes and HashiCorp Vault secrets.
+
+---
+
+## 1. Adding Environment Variables to Kubernetes
+
+### Location: Values File
+
+**File Path:**
+```
+/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/fitfile/ff-c/thehyve_values.yaml
+```
+
+**Git Repository:**
+- Repo: `https://gitlab.com/fitfile/deployment.git`
+- Branch: `latest-release`
+- Path: `ffnodes/fitfile/ff-c/thehyve_values.yaml`
+
+### Method 1: Plain Environment Variables (Non-Sensitive)
+
+Add to the `extraEnvVars` section in `thehyve_values.yaml`:
+
+```yaml
+extraEnvVars:
+  - name: NHS_SITE
+    value: mkuh
+  # Add your new variable here:
+  - name: YOUR_VAR_NAME
+    value: "your-value"
+  - name: ANOTHER_VAR
+    value: "another-value"
+```
+
+**Use Case:** Configuration values, feature flags, non-sensitive settings
+
+---
+
+### Method 2: Secrets from Vault (Sensitive Data)
+
+#### Step A: Add Variable Reference in Values File
+
+Add to `extraEnvVars` section referencing the Vault secret:
+
+```yaml
+extraEnvVars:
+  - name: NHS_SITE
+    value: mkuh
+  # Existing Vault secrets
+  - name: QCR_BUCKET
+    valueFrom:
+      secretKeyRef:
+        name: thehyve
+        key: qcr_bucket
+  # Add your new secret reference:
+  - name: YOUR_SECRET_VAR
+    valueFrom:
+      secretKeyRef:
+        name: thehyve
+        key: your_secret_key
+```
+
+#### Step B: Add Secret to Vault Template
+
+In the same `thehyve_values.yaml` file, update the `extraDeploy` VaultStaticSecret section:
+
+**Location:** Lines 96-137 in `thehyve_values.yaml`
+
+Add your secret key to the `transformation.templates` section:
+
+```yaml
+extraDeploy:
+  - apiVersion: secrets.hashicorp.com/v1beta1
+    kind: VaultStaticSecret
+    metadata:
+      name: thehyve
+      namespace: "{{ .Release.Namespace }}"
+    spec:
+      namespace: admin/deployments/ff-c  # ← Vault namespace
+      mount: secrets
+      path: thehyve  # ← Secret path in Vault
+      type: kv-v2
+      hmacSecretData: true
+      destination:
+        create: true
+        name: thehyve
+        transformation:
+          excludes:
+            - .*
+          templates:
+            qcr_bucket:
+              text: '{{`{{get .Secrets "qcr_bucket"}}`}}'
+            qcr_access_key_id:
+              text: '{{`{{get .Secrets "qcr_access_key_id"}}`}}'
+            qcr_secret_access_key:
+              text: '{{`{{get .Secrets "qcr_secret_access_key"}}`}}'
+            qcr_iam_role:
+              text: '{{`{{get .Secrets "qcr_iam_role"}}`}}'
+            # Add your new secret template here:
+            your_secret_key:
+              text: '{{`{{get .Secrets "your_secret_key"}}`}}'
+```
+
+**Important Notes:**
+- The key name in `templates:` must match the key in `secretKeyRef.key`
+- Use the exact template format with escaped curly braces
+
+---
+
+## 2. Adding Secrets to HashiCorp Vault
+
+### Vault Namespace Structure
+
+**Full Vault Path:**
+```
+admin/deployments/ff-c/secrets/thehyve
+```
+
+**Breakdown:**
+- **Vault Namespace:** `admin/deployments/ff-c`
+- **Secrets Mount:** `secrets`
+- **Secret Path:** `thehyve`
+
+### Using Vault CLI
+
+#### Login to Vault
+
+```bash
+# Set Vault address
+export VAULT_ADDR="https://your-vault-address.com"
+
+# Login (use appropriate auth method)
+vault login -method=oidc
+# OR
+vault login -method=token
+```
+
+#### Set Namespace
+
+```bash
+# Set the correct namespace
+export VAULT_NAMESPACE="admin/deployments/ff-c"
+```
+
+#### Add/Update Secrets
+
+**Option 1: Add a Single Key-Value Pair**
+
+```bash
+vault kv put -mount=secrets thehyve \
+  your_secret_key="your-secret-value"
+```
+
+**Option 2: Update Existing Secret (Preserve Other Keys)**
+
+```bash
+# Read existing secret first
+vault kv get -mount=secrets thehyve
+
+# Update with patch (adds/updates only specified keys)
+vault kv patch -mount=secrets thehyve \
+  your_secret_key="your-secret-value" \
+  another_key="another-value"
+```
+
+**Option 3: Replace Entire Secret**
+
+```bash
+vault kv put -mount=secrets thehyve \
+  qcr_bucket="existing-bucket" \
+  qcr_access_key_id="existing-key-id" \
+  qcr_secret_access_key="existing-secret" \
+  qcr_iam_role="existing-role" \
+  your_secret_key="your-new-secret" \
+  another_key="another-secret"
+```
+
+#### Verify Secret
+
+```bash
+# List all keys in the secret
+vault kv get -mount=secrets thehyve
+
+# Get specific field
+vault kv get -mount=secrets -field=your_secret_key thehyve
+```
+
+### Using Vault UI
+
+1. **Navigate to Vault UI:** `https://your-vault-address.com/ui/`
+2. **Select Namespace:** Choose `admin/deployments/ff-c` from namespace dropdown
+3. **Navigate to Secrets Engine:**
+   - Click on `secrets/` mount
+   - Navigate to path `thehyve/`
+4. **Edit Secret:**
+   - Click on the secret
+   - Click "Create new version +"
+   - Add your new key-value pairs
+   - Click "Save"
+
+---
+
+## 3. Deployment Workflow
+
+### Step-by-Step Process
+
+1. **Add Secrets to Vault** (if needed)
+   ```bash
+   export VAULT_NAMESPACE="admin/deployments/ff-c"
+   vault kv patch -mount=secrets thehyve your_secret_key="value"
+   ```
+
+2. **Update Values File**
+   ```bash
+   cd /Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment
+
+   # Edit the file
+   vim ffnodes/fitfile/ff-c/thehyve_values.yaml
+   ```
+
+3. **Commit and Push Changes**
+   ```bash
+   git add ffnodes/fitfile/ff-c/thehyve_values.yaml
+   git commit -m "FFAPP-XXXX: feat(thehyve-mkuh): add YOUR_VAR_NAME environment variable"
+   git push origin latest-release
+   ```
+
+4. **Wait for ArgoCD Sync**
+   - ArgoCD will automatically detect the change
+   - Sync is triggered every 3 minutes (default)
+   - Or manually sync via ArgoCD UI
+
+5. **Verify Deployment**
+   ```bash
+   # Check ArgoCD sync status
+   kubectl get application thehyve-mkuh -n argocd -o jsonpath='{.status.sync.status}'
+
+   # Verify environment variables in pod
+   kubectl exec -n thehyve-mkuh deployment/thehyve-mkuh -c webserver -- env | grep YOUR_VAR_NAME
+
+   # Check if secret is loaded
+   kubectl describe secret thehyve -n thehyve-mkuh
+   ```
+
+---
+
+## 4. Current Configuration Reference
+
+### Existing Environment Variables
+
+**Plain Variables:**
+- `NHS_SITE=mkuh`
+
+**Vault-Sourced Secrets:**
+- `QCR_BUCKET` → from `thehyve.qcr_bucket`
+- `QCR_ACCES_KEY_ID` → from `thehyve.qcr_access_key_id`
+- `QCR_SECRET_ACCESS_KEY` → from `thehyve.qcr_secret_access_key`
+- `QCR_IAM_ROLE` → from `thehyve.qcr_iam_role`
+
+**Auto-Generated (from Chart):**
+- `OMOP_TARGET_DB` → from database config
+- `AIRFLOW__CORE__SQL_ALCHEMY_CONN` → from database config
+- `AIRFLOW_ADMIN_*` → from airflow.initAdmin config
+
+### Vault Secret Sync Behavior
+
+- **Refresh Interval:** 10 minutes
+- **Auto Rollout Restart:** Yes (deployment restarts on secret change)
+- **Drift Detection:** Enabled (HMAC validation)
+
+---
+
+## 5. Examples
+
+### Example 1: Add Database Connection String (Vault)
+
+**1. Add secret to Vault:**
+```bash
+export VAULT_NAMESPACE="admin/deployments/ff-c"
+vault kv patch -mount=secrets thehyve \
+  external_db_url="postgresql://user:pass@host:5432/dbname"
+```
+
+**2. Update `thehyve_values.yaml`:**
+```yaml
+extraEnvVars:
+  # ... existing vars ...
+  - name: EXTERNAL_DB_URL
+    valueFrom:
+      secretKeyRef:
+        name: thehyve
+        key: external_db_url
+
+extraDeploy:
+  - apiVersion: secrets.hashicorp.com/v1beta1
+    kind: VaultStaticSecret
+    # ... existing config ...
+    spec:
+      # ... existing spec ...
+      destination:
+        transformation:
+          templates:
+            # ... existing templates ...
+            external_db_url:
+              text: '{{`{{get .Secrets "external_db_url"}}`}}'
+```
+
+### Example 2: Add Feature Flag (Plain Value)
+
+**Update `thehyve_values.yaml`:**
+```yaml
+extraEnvVars:
+  # ... existing vars ...
+  - name: ENABLE_NEW_FEATURE
+    value: "true"
+  - name: LOG_LEVEL
+    value: "INFO"
+```
+
+### Example 3: Add API Key (Vault)
+
+**1. Add to Vault:**
+```bash
+export VAULT_NAMESPACE="admin/deployments/ff-c"
+vault kv patch -mount=secrets thehyve \
+  api_key="sk_live_1234567890abcdef"
+```
+
+**2. Update values file:**
+```yaml
+extraEnvVars:
+  - name: API_KEY
+    valueFrom:
+      secretKeyRef:
+        name: thehyve
+        key: api_key
+
+extraDeploy:
+  - apiVersion: secrets.hashicorp.com/v1beta1
+    kind: VaultStaticSecret
+    spec:
+      destination:
+        transformation:
+          templates:
+            api_key:
+              text: '{{`{{get .Secrets "api_key"}}`}}'
+```
+
+---
+
+## 6. Troubleshooting
+
+### Secret Not Appearing in Pod
+
+**Check VaultStaticSecret Status:**
+```bash
+kubectl get vaultstaticsecret thehyve -n thehyve-mkuh -o yaml
+kubectl describe vaultstaticsecret thehyve -n thehyve-mkuh
+```
+
+**Check Vault Secrets Operator Logs:**
+```bash
+kubectl logs -n vault-secrets-operator deployment/vault-secrets-operator-controller-manager
+```
+
+**Verify Secret Exists:**
+```bash
+kubectl get secret thehyve -n thehyve-mkuh -o yaml
+```
+
+### ArgoCD Not Syncing
+
+**Check Application Status:**
+```bash
+kubectl get application thehyve-mkuh -n argocd -o yaml
+```
+
+**Manual Sync:**
+```bash
+kubectl patch application thehyve-mkuh -n argocd --type merge -p '{"operation":{"initiatedBy":{"username":"admin"},"sync":{"revision":"latest-release"}}}'
+```
+
+**Check ArgoCD UI:**
+- URL: https://argocd.your-cluster.com
+- Navigate to `thehyve-mkuh` application
+
+### Environment Variable Not Set
+
+**Check Pod Environment:**
+```bash
+kubectl exec -n thehyve-mkuh deployment/thehyve-mkuh -c webserver -- env | sort
+```
+
+**Check Deployment Spec:**
+```bash
+kubectl get deployment thehyve-mkuh -n thehyve-mkuh -o jsonpath='{.spec.template.spec.containers[0].env}' | jq
+```
+
+### Vault Authentication Issues
+
+**Check VaultAuth:**
+```bash
+kubectl get vaultauth -n thehyve-mkuh
+kubectl describe vaultauth default -n thehyve-mkuh
+```
+
+---
+
+## 7. Best Practices
+
+### Security
+- ✅ **Always use Vault for sensitive data** (passwords, API keys, tokens)
+- ✅ Use `kv patch` to avoid overwriting existing secrets
+- ✅ Never commit secrets to Git
+- ❌ Don't use plain values for credentials
+
+### Naming Conventions
+- Use `UPPER_SNAKE_CASE` for environment variable names
+- Use `lower_snake_case` for Vault secret keys
+- Prefix related variables (e.g., `DB_HOST`, `DB_PORT`, `DB_NAME`)
+
+### Version Control
+- Follow commit message convention: `FFAPP-XXXX: type(scope): description`
+- Create feature branches for significant changes
+- Test in non-production first
+
+### Documentation
+- Document new variables in application README
+- Include purpose and expected values
+- Note any dependencies or prerequisites
+
+---
+
+## Quick Reference
+
+| Task | Namespace/Path |
+|------|----------------|
+| **Kubernetes Values File** | `ffnodes/fitfile/ff-c/thehyve_values.yaml` |
+| **Vault Namespace** | `admin/deployments/ff-c` |
+| **Vault Secrets Mount** | `secrets` |
+| **Vault Secret Path** | `thehyve` |
+| **Vault Full Path** | `admin/deployments/ff-c/secrets/thehyve` |
+| **Kubernetes Namespace** | `thehyve-mkuh` |
+| **Secret Name** | `thehyve` |
+| **ArgoCD Application** | `thehyve-mkuh` (in `argocd` namespace) |
+
+---
+
+**Last Updated:** 2025-10-23
+**Cluster:** fitfile-cloud-prod-1-aks-cluster

````

Perfect! I've created a comprehensive guide for you. Here's the answer to your question:

## Summary: Where to Add Variables

### 1. **For Kubernetes Environment Variables:**

**File Location:**

```sh
/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/fitfile/ff-c/thehyve_values.yaml
```

Add to the `extraEnvVars:` section (around line 12-34)

### 2. **For HashiCorp Vault Secrets:**

**Vault Namespace:**

```sh
admin/deployments/ff-c
```

**Full Vault Path:**

```sh
admin/deployments/ff-c/secrets/thehyve
```

**Command to add secrets:**

```bash
export VAULT_NAMESPACE="admin/deployments/ff-c"
vault kv patch -mount=secrets thehyve your_key="your_value"
```

### Key Points

1. **Plain environment variables** (non-sensitive): Add directly to `extraEnvVars` in the values file
2. **Secrets** (sensitive data):
   - Add to Vault at path `admin/deployments/ff-c/secrets/thehyve`
   - Reference in `extraEnvVars` using `secretKeyRef`
   - Add template in the `extraDeploy` VaultStaticSecret section

3. **The Vault namespace is `admin/deployments/ff-c`** - not just `ff-c`

I've created a detailed guide at `./thehyve-mkuh-add-variables-guide.md` with:

- Step-by-step instructions
- Code examples
- Troubleshooting tips
- Best practices
- Complete workflow from Vault → Values File → Deployment

The guide includes everything you need to add both plain variables and Vault-backed secrets to thehyve-mkuh! 🎯
