---
aliases: []
confidence: 
created: 2025-11-11T14:50:06Z
epistemic: 
last_reviewed: 
modified: 2025-11-11T15:44:06Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Kubernetes Backup and Disaster Recovery for AWS and Azure
type: 
uid: 
updated: 
---

## Kubernetes Backup and Disaster Recovery for AWS and Azure

**Multi-cloud backup and disaster recovery strategies demand Kubernetes-native approaches that work seamlessly across AWS and Azure.** This comprehensive guide provides production-ready backup architectures, tool-specific implementations, and operational best practices for DevOps engineers managing stateful applications across cloud providers. Modern organizations require portable backup formats, automated recovery workflows, and cost-optimized retention strategies that prevent vendor lock-in while maintaining enterprise-grade data protection.

### What to back up in Kubernetes Clusters

Comprehensive Kubernetes backup requires protecting three distinct layers: the control plane state stored in etcd, persistent application data in volumes, and the declarative configurations defining cluster resources. **Each component demands different backup strategies** because they serve different purposes in cluster recovery.

**Control plane: etcd cluster state**. The etcd distributed key-value store serves as Kubernetes' single source of truth, storing all API objects, cluster configurations, node information, RBAC policies, Custom Resource Definitions, Secrets, ConfigMaps, and service discovery details. Located at `/var/lib/etcd` by default, etcd runs as a leader-based distributed system using the Raft consensus protocol. For highly available clusters with multiple control plane nodes, only one etcd backup is needed since data replicates across all members. Production environments should run etcd 3.4.22+ or 3.5.6+, which provide improved snapshot capabilities and stability.

**Persistent data layer: volumes and claims**. PersistentVolumes represent cluster-level storage resources while PersistentVolumeClaims represent user requests for that storage. Critical components include the PV/PVC bindings, StorageClass definitions, and the actual data stored on backing storage systems like AWS EBS volumes or Azure Managed Disks. Access modes matter for backup strategy: ReadWriteOnce volumes mount to single nodes, ReadWriteMany support multi-node access, and ReadOnlyMany provide shared read access. Each access mode affects how volume snapshots can be taken and restored.

**Application configurations and workload definitions**. This layer encompasses all Kubernetes-native resources: Deployments with replica specifications, StatefulSets maintaining sticky identities, DaemonSets ensuring pod copies on each node, Services exposing applications, Ingress rules routing external traffic, NetworkPolicies controlling pod-to-pod communication, and Helm releases with their metadata stored as Secrets. RBAC configurations including Roles, ClusterRoles, RoleBindings, and ServiceAccounts must be backed up to maintain security postures. Custom Resource Definitions and their instances require special handling since they represent application-specific extensions to Kubernetes.

### Backup Strategies for Each Component

**etcd snapshot-based backup (recommended primary method)**. Use the etcdctl tool with API version 3 to create consistent point-in-time snapshots. The critical command structure:

```bash
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save /opt/backup/etcd-snapshot-$(date +%Y%m%d-%H%M%S).db
```

This approach requires three certificates for TLS authentication located in `/etc/kubernetes/pki/etcd/` for kubeadm clusters. **Production frequency recommendations**: minimum daily backups, preferably every 12 hours for active clusters. High-transaction environments should snapshot every 15 minutes. Always verify snapshot integrity immediately after creation using etcdutl.

Restoration requires special handling to prevent cache invalidation in Kubernetes controllers. The `--bump-revision` and `--mark-compacted` flags are essential for production restores:

```bash
etcdutl snapshot restore snapshot.db \
  --bump-revision 1000000000 \
  --mark-compacted \
  --data-dir /var/lib/etcd-from-backup
```

The revision bump adds one billion to the current revision number (covering approximately one week at under 1,500 writes per second), while mark-compacted terminates all existing watches, forcing Kubernetes informer caches to rebuild. Without these flags, restored clusters experience cache inconsistencies that cause unpredictable behavior.

**Persistent volume backup via CSI snapshots**. Kubernetes 1.20+ provides GA support for the VolumeSnapshot API (snapshot.storage.k8s.io/v1), offering cloud-agnostic volume snapshots through Container Storage Interface drivers. This Kubernetes-native approach works across AWS EBS (`ebs.csi.aws.com`), Azure Disk (`disk.csi.azure.com`), and Google Persistent Disk.

First, create a VolumeSnapshotClass:

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: aws-ebs-snapclass
driver: ebs.csi.aws.com
deletionPolicy: Retain
```

Then snapshot a PVC:

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: mysql-data-snapshot
spec:
  volumeSnapshotClassName: aws-ebs-snapclass
  source:
    persistentVolumeClaimName: mysql-data-pvc
```

Restore from snapshot by specifying it as a dataSource in a new PVC. CSI snapshots provide crash-consistent backups suitable for most applications, but **databases require application-aware backups** for transactional consistency.

**Application-consistent backups for stateful workloads**. Databases and stateful applications need coordinated backups that ensure data integrity. Use pre-backup hooks to quiesce applications:

```bash
# PostgreSQL: Use native backup tools
kubectl exec statefulset/postgres-0 -- \
  pg_basebackup -D /backup -Ft -z -P -U postgres

# MySQL: Dump with proper locking
kubectl exec statefulset/mysql-0 -- \
  mysqldump --all-databases --single-transaction \
  --master-data=2 > backup.sql

# MongoDB: Create consistent backup
kubectl exec statefulset/mongo-0 -- \
  mongodump --archive=/backup/mongo.archive --gzip
```

For StatefulSets, backup each pod's PVC independently since each maintains unique state. Snapshot all PVCs simultaneously or use application-native replication for consistency across replicas.

**Configuration backup via GitOps and manifest export**. Store all Kubernetes manifests in Git repositories following infrastructure-as-code practices. This provides version control, audit trails, and declarative state management. Export cluster resources periodically:

```bash
# Export all workload configurations
kubectl get deployments,statefulsets,daemonsets,services,ingress \
  --all-namespaces -o yaml > workloads-$(date +%Y%m%d).yaml

# Export RBAC policies
kubectl get roles,rolebindings,clusterroles,clusterrolebindings \
  --all-namespaces -o yaml > rbac-$(date +%Y%m%d).yaml

# Export CRDs and custom resources
kubectl get crds -o yaml > crds-$(date +%Y%m%d).yaml
```

For Helm deployments, preserve release metadata:

```bash
helm list --all-namespaces -o yaml > helm-releases.yaml
helm get values <release> -n <namespace> > values.yaml
helm get manifest <release> -n <namespace> > manifest.yaml
```

**File-level backup with Restic**. For volumes that don't support native snapshots or require cloud-agnostic portability, use Restic for file-level backups. Restic provides incremental backups with content-defined chunking, AES-256 encryption, and deduplication. Velero and other tools integrate Restic for backing up any volume type to object storage (S3, Azure Blob, GCS, MinIO).

### Velero for Multi-cloud Backup

Velero (formerly Heptio Ark) is the leading open-source, Kubernetes-native backup solution with extensive AWS and Azure support. As a CNCF project with VMware backing, Velero provides cluster resource backups, persistent volume snapshots, and cross-cloud migration capabilities.

**Architecture and operation**. Velero runs as a server deployment in its own namespace within your cluster, using custom resource definitions (BackupStorageLocation, VolumeSnapshotLocation, Backup, Restore) to define backup policies. The Velero CLI interacts with these CRDs to trigger operations. Velero creates tarballs of Kubernetes objects stored in object storage and coordinates volume snapshots through cloud provider APIs or CSI.

**AWS EKS installation and configuration**. Install Velero on AWS with EBS volume snapshots and S3 backup storage:

```bash
# Set environment variables
BUCKET=velero-backups-prod
REGION=us-west-2
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)

# Create S3 bucket
aws s3 mb s3://$BUCKET --region $REGION

# Create IAM policy for Velero
cat > velero-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeVolumes", "ec2:DescribeSnapshots",
        "ec2:CreateTags", "ec2:CreateVolume",
        "ec2:CreateSnapshot", "ec2:DeleteSnapshot"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:DeleteObject", "s3:PutObject",
                 "s3:AbortMultipartUpload", "s3:ListMultipartUploadParts"],
      "Resource": ["arn:aws:s3:::${BUCKET}/*"]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": ["arn:aws:s3:::${BUCKET}"]
    }
  ]
}
EOF

aws iam create-policy \
  --policy-name VeleroAccessPolicy \
  --policy-document file://velero-policy.json

# Create IAM service account for EKS (using IRSA)
eksctl create iamserviceaccount \
  --cluster=my-eks-cluster \
  --name=velero-server \
  --namespace=velero \
  --role-name=eks-velero-backup \
  --role-only \
  --attach-policy-arn=arn:aws:iam::$ACCOUNT:policy/VeleroAccessPolicy \
  --approve

# Install Velero via Helm
helm repo add vmware-tanzu https://vmware-tanzu.github.io/helm-charts

cat > values-aws.yaml <<EOF
configuration:
  backupStorageLocation:
    - bucket: $BUCKET
      provider: aws
      default: true
      config:
        region: $REGION
  volumeSnapshotLocation:
    - config:
        region: $REGION
      provider: aws
initContainers:
  - name: velero-plugin-for-aws
    image: velero/velero-plugin-for-aws:v1.9.0
    volumeMounts:
      - mountPath: /target
        name: plugins
credentials:
  useSecret: false
serviceAccount:
  server:
    annotations:
      eks.amazonaws.com/role-arn: "arn:aws:iam::$ACCOUNT:role/eks-velero-backup"
EOF

helm install velero vmware-tanzu/velero \
  --create-namespace \
  --namespace velero \
  -f values-aws.yaml
```

**Azure AKS installation and configuration**. Configure Velero for Azure with Managed Disk snapshots and Blob Storage:

```bash
# Set Azure environment variables
AZURE_SUBSCRIPTION_ID=$(az account list --query '[?isDefault].id' -o tsv)
AZURE_TENANT_ID=$(az account list --query '[?isDefault].tenantId' -o tsv)
AZURE_BACKUP_RESOURCE_GROUP="velero-backups-rg"
AZURE_STORAGE_ACCOUNT_ID="velero$(uuidgen | cut -d '-' -f5 | tr '[A-Z]' '[a-z]')"
BLOB_CONTAINER="velero"

# Create resource group and storage account
az group create -n $AZURE_BACKUP_RESOURCE_GROUP --location westus2

az storage account create \
  --name $AZURE_STORAGE_ACCOUNT_ID \
  --resource-group $AZURE_BACKUP_RESOURCE_GROUP \
  --sku Standard_GRS \
  --encryption-services blob \
  --https-only true \
  --kind BlobStorage \
  --access-tier Hot

# Create blob container
az storage container create \
  -n $BLOB_CONTAINER \
  --public-access off \
  --account-name $AZURE_STORAGE_ACCOUNT_ID

# Get AKS infrastructure resource group (contains VMs and disks)
AZURE_RESOURCE_GROUP=$(az aks show \
  -n my-aks-cluster \
  -g my-resource-group \
  --query "nodeResourceGroup" -o tsv)

# Create service principal with required permissions
AZURE_CLIENT_SECRET=$(az ad sp create-for-rbac \
  --name "velero" \
  --role "Contributor" \
  --query 'password' -o tsv)

AZURE_CLIENT_ID=$(az ad sp list \
  --display-name "velero" \
  --query '[0].appId' -o tsv)

# Create credentials file
cat > credentials-velero <<EOF
AZURE_SUBSCRIPTION_ID=${AZURE_SUBSCRIPTION_ID}
AZURE_TENANT_ID=${AZURE_TENANT_ID}
AZURE_CLIENT_ID=${AZURE_CLIENT_ID}
AZURE_CLIENT_SECRET=${AZURE_CLIENT_SECRET}
AZURE_RESOURCE_GROUP=${AZURE_RESOURCE_GROUP}
AZURE_CLOUD_NAME=AzurePublicCloud
EOF

# Install Velero
velero install \
  --provider azure \
  --plugins velero/velero-plugin-for-microsoft-azure:v1.9.0 \
  --bucket $BLOB_CONTAINER \
  --secret-file ./credentials-velero \
  --backup-location-config \
    resourceGroup=$AZURE_BACKUP_RESOURCE_GROUP,storageAccount=$AZURE_STORAGE_ACCOUNT_ID,subscriptionId=$AZURE_SUBSCRIPTION_ID \
  --snapshot-location-config \
    resourceGroup=$AZURE_BACKUP_RESOURCE_GROUP,subscriptionId=$AZURE_SUBSCRIPTION_ID \
  --use-node-agent \
  --uploader-type=restic
```

**Creating and managing backups**. Execute on-demand and scheduled backups:

```bash
# On-demand backup of specific namespace
velero backup create prod-backup \
  --include-namespaces production \
  --snapshot-volumes \
  --ttl 720h

# Scheduled daily backup at 2 AM
velero schedule create daily-backup \
  --schedule="0 2 * * *" \
  --include-namespaces production,staging \
  --ttl 168h

# Backup with resource filtering
velero backup create app-backup \
  --selector app=mysql \
  --include-resources deployments,services,pvc

# Backup excluding certain resources
velero backup create cluster-backup \
  --exclude-resources events,events.events.k8s.io

# Check backup status
velero backup describe prod-backup --details
velero backup logs prod-backup
```

**Restoring from backups**. Restore entire namespaces or specific resources:

```bash
# Restore entire backup
velero restore create --from-backup prod-backup

# Restore to different namespace (migration)
velero restore create prod-to-dr \
  --from-backup prod-backup \
  --namespace-mappings production:production-dr

# Restore only specific resources
velero restore create partial-restore \
  --from-backup prod-backup \
  --include-resources deployment,service \
  --selector app=web

# Check restore status
velero restore describe prod-to-dr --details
```

**Application-consistent backups with hooks**. Use pre and post-backup hooks for database consistency:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: postgres-0
  annotations:
    pre.hook.backup.velero.io/command: '["/bin/bash", "-c", "PGPASSWORD=$POSTGRES_PASSWORD pg_dump -U postgres -h localhost mydb > /scratch/backup.sql"]'
    pre.hook.backup.velero.io/timeout: 3m
    post.hook.backup.velero.io/command: '["/bin/bash", "-c", "rm -f /scratch/backup.sql"]'
```

**Cross-cloud migration with Velero**. Migrate applications from AWS to Azure:

1. Create backup in AWS EKS cluster
2. Configure Azure AKS cluster with same S3 bucket as additional BackupStorageLocation
3. Sync backup metadata: `velero backup-location create aws-source --provider aws --bucket velero-backups --config region=us-west-2 --access-mode=ReadOnly`
4. Restore in Azure AKS: `velero restore create aws-to-azure --from-backup prod-backup`

This works because Velero stores backups in portable formats (JSON/YAML for Kubernetes objects, cloud snapshots or Restic for volumes).

### Kasten K10 for Enterprise Multi-cloud

Kasten K10 (now Veeam Kasten) provides an enterprise-grade, application-centric backup platform with advanced features beyond open-source tools. **Key differentiators include policy-driven automation, application-aware backups, multi-cluster management, and a sophisticated UI** for operations teams.

**Architecture and capabilities**. K10 runs as a Kubernetes operator in the `kasten-io` namespace, deploying multiple microservices that handle backup orchestration, data movement, catalog management, and policy execution. Unlike Velero's CLI-first approach, K10 provides an intuitive web dashboard accessible via port-forward or Ingress. K10 treats applications—not just namespaces—as the operational unit, automatically discovering application topology including deployments, services, ConfigMaps, Secrets, and PVCs.

**AWS EKS integration**. Install K10 on EKS with native AWS integrations:

```bash
# Add Kasten Helm repository
helm repo add kasten https://charts.kasten.io/

# Create namespace
kubectl create namespace kasten-io

# Install with AWS integration
helm install k10 kasten/k10 \
  --namespace=kasten-io \
  --set global.persistence.storageClass=gp3 \
  --set auth.tokenAuth.enabled=true \
  --set eula.accept=true \
  --set eula.company="Your Company" \
  --set eula.email="admin@company.com"

# Configure AWS S3 location profile
cat <<EOF | kubectl apply -f -
apiVersion: config.kio.kasten.io/v1alpha1
kind: Profile
metadata:
  name: aws-s3-profile
  namespace: kasten-io
spec:
  type: Location
  locationSpec:
    credential:
      secretType: AwsAccessKey
      secret:
        apiVersion: v1
        kind: Secret
        name: k10-aws-creds
        namespace: kasten-io
    type: ObjectStore
    objectStore:
      name: velero-backups
      objectStoreType: S3
      region: us-west-2
EOF
```

**Azure AKS integration**. Deploy K10 with Azure Blob Storage and Managed Disk support:

```bash
# Get Azure credentials
AZURE_TENANT_ID=$(az account show --query tenantId -o tsv)
AZURE_CLIENT_ID=<service-principal-app-id>
AZURE_CLIENT_SECRET=<service-principal-secret>

# Install K10
helm install k10 kasten/k10 \
  --namespace=kasten-io \
  --create-namespace \
  --set secrets.azureTenantId=$AZURE_TENANT_ID \
  --set secrets.azureClientId=$AZURE_CLIENT_ID \
  --set secrets.azureClientSecret=$AZURE_CLIENT_SECRET \
  --set global.persistence.storageClass=managed-csi

# Access dashboard
kubectl --namespace kasten-io port-forward service/gateway 8080:8000
# Navigate to http://127.0.0.1:8080/k10/#/
```

**Creating backup policies**. K10 uses policies to automate backup operations:

```yaml
apiVersion: config.kio.kasten.io/v1alpha1
kind: Policy
metadata:
  name: mysql-backup-policy
  namespace: kasten-io
spec:
  frequency: "@hourly"
  retention:
    hourly: 24
    daily: 7
    weekly: 4
    monthly: 12
  selector:
    matchExpressions:
      - key: app
        operator: In
        values:
          - mysql
  actions:
    - action: backup
      backupParameters:
        profile:
          name: aws-s3-profile
          namespace: kasten-io
    - action: export
      exportParameters:
        frequency: "@daily"
        profile:
          name: aws-s3-profile
          namespace: kasten-io
```

**Application mobility and DR**. K10 excels at cross-cluster, cross-cloud application migration. Export applications from one cluster and import to another:

1. Create policy with export action to object storage
2. Run backup/export operation
3. In target cluster, import from same storage location
4. Transform configurations (namespace mappings, storage classes, etc.)
5. Restore with automated resource adjustments

**Advanced features**. K10 provides capabilities not available in open-source tools:
- **Continuous Data Protection**: Near-zero RPO with incremental snapshots
- **Compliance reporting**: Automated SLA tracking and audit reports
- **Multi-tenancy**: Namespace-scoped RBAC with self-service restore
- **Blueprint system**: Kanister blueprints for application-specific backup logic
- **Disaster recovery automation**: Automated failover testing and orchestration

**Pricing model**. K10 uses node-based licensing with a free tier (5 nodes), making it accessible for small deployments while scaling to enterprise needs. Enterprise editions include advanced features, support, and integration with Veeam Backup & Replication.

### Alternative Backup Tools Comparison

**Portworx PX-Backup**. Enterprise solution from Pure Storage offering container-granular, application-aware backups. PX-Backup provides namespace, pod, and tag-level backup granularity with multi-cloud storage support. Strengths include tight integration with Portworx storage platform, built-in disaster recovery orchestration, and migration capabilities. Best for organizations already using Portworx for persistent storage or requiring zero-RPO replication combined with backups.

**Trilio for Kubernetes (TrilioVault)**. Application-centric cloud-native data protection emphasizing continuous restore and self-service capabilities. Trilio offers point-in-time recovery, incremental backups, and strong multi-tenancy with RBAC. The Continuous Restore feature significantly reduces recovery time by maintaining warm standby applications. Ideal for multi-tenant environments requiring fine-grained access control and fast recovery windows.

**Cloud-native solutions**. AWS Backup for EKS and Azure Backup provide native integration but with limitations. AWS Backup supports EKS PersistentVolume backups via CSI snapshot integration but lacks application-aware features. Azure Backup similarly focuses on volume-level backups without full Kubernetes context. These work well for simple persistent volume protection but insufficient for complex application topologies.

**Tool comparison matrix**:

| Feature | Velero | Kasten K10 | Portworx PX-Backup | Trilio |
|---------|--------|------------|--------------------|---------|
| **License** | Open source (Apache 2.0) | Commercial (node-based) | Commercial | Commercial |
| **Multi-cloud** | Excellent (plugins) | Excellent (native) | Excellent | Excellent |
| **UI/Dashboard** | CLI-first, basic UI | Advanced web UI | Web UI | Web UI |
| **Application-aware** | Hooks required | Native | Native | Native |
| **Continuous DP** | No | Limited | Yes (with Portworx) | Yes |
| **Zero RPO** | No | No | Yes (replication) | Limited |
| **Multi-cluster mgmt** | Manual | Built-in | Built-in | Manual |

| **Cost** | Free | $$$ | $$$$ | $$$

 |

| **Best for** | Getting started, open source shops | Enterprise Kubernetes with budget | Portworx users, zero-RPO needs | Multi-tenant, fast recovery |

**Recommendation by use case**:
- **Small to medium environments**: Start with Velero for cost-effectiveness and simplicity
- **Enterprise production**: Kasten K10 for comprehensive features and support
- **Mission-critical, zero-RPO**: Portworx PX-Backup with storage replication
- **Multi-tenant SaaS platforms**: Trilio for granular RBAC and continuous restore
- **Hybrid strategy**: Velero as primary + Kasten K10 for critical applications

### Cross-cloud Challenges and Solutions

**Backup consistency across providers**. AWS and Azure use different snapshot APIs, storage types, and availability models. **Solution**: Use cloud-agnostic tools (Velero, Kasten K10) with Restic/Kopia for file-level backups that work identically across clouds. Store backups in S3-compatible object storage accessible from both environments. Configure separate VolumeSnapshotLocations for each cloud while using unified BackupStorageLocation for Kubernetes objects.

**Network and data transfer optimization**. Cross-cloud data transfer incurs egress charges ($0.09-0.12/GB) and latency. **Solutions**:
- Enable compression at source (50-70% size reduction)
- Use incremental backups reducing transfer to changed blocks only
- Implement deduplication at backup repository level
- Schedule large transfers during off-peak hours
- Consider Direct Connect (AWS) or ExpressRoute (Azure) for high-volume scenarios
- Cache frequently restored data in each cloud region

**Storage compatibility issues**. EBS volumes use block storage with specific IOPS characteristics, while Azure Managed Disks have different performance tiers. **Solutions**:
- Use CSI VolumeSnapshot API providing abstraction over cloud specifics
- Employ Velero with Restic for cloud-agnostic file-level volume backups
- Test restore performance in target cloud and adjust storage class specifications
- Map storage classes appropriately: AWS gp3 ↔ Azure StandardSSD_LRS, io2 ↔ Premium_LRS
- Document storage class transformations in runbooks

**Kubernetes version and API compatibility**. Different managed Kubernetes versions across clouds cause API object incompatibilities. **Solutions**:
- Maintain version parity between source and target clusters (ideally same minor version)
- Use `kubectl convert` for API version migrations during restore
- Test backups on matching Kubernetes versions before production migration
- Leverage Kasten K10's transformation capabilities for automatic API version conversion
- Validate Custom Resource Definitions exist in target cluster before restore

**Resource UID and naming conflicts**. Kubernetes assigns unique UIDs to resources that conflict during cross-cluster restore. **Solutions**:
- Velero automatically strips UIDs and regenerates them during restore
- Use namespace mapping to avoid conflicts: `--namespace-mappings source:target`
- Remove cloud-specific annotations and labels before restore
- Clean up LoadBalancer service specifications that reference cloud-specific resources
- Update Ingress configurations to match target cloud's ingress controller

**IAM and authentication differences**. AWS uses IAM roles with IRSA (IAM Roles for Service Accounts), while Azure uses Service Principals and Managed Identities. **Solutions**:
- Create separate credential sets for each cloud provider
- Use Velero's cloud credential plugin architecture for multi-cloud authentication
- Implement separate BackupStorageLocations with provider-specific credentials
- Document credential rotation procedures for each cloud
- Use least-privilege access policies specific to each cloud's security model

### Recovery order and Disaster Recovery

**Proper restoration sequence**. Follow this order to avoid dependency failures and ensure clean recovery:

1. **Restore etcd** (control plane recovery for self-managed clusters):
   - Stop all API servers before restore
   - Restore from snapshot on all control plane nodes simultaneously
   - Update etcd manifest with new data directory path
   - Restart kubelet and verify cluster health
   - Wait for all nodes to reach Ready state

2. **Restore namespace definitions**:
   - Recreate all namespaces first to establish boundaries
   - Apply ResourceQuotas and LimitRanges
   - Restore NetworkPolicies for security before workloads

3. **Restore RBAC and security policies**:
   - ServiceAccounts and their tokens
   - Roles, ClusterRoles, RoleBindings, ClusterRoleBindings
   - Pod Security Policies or Pod Security Standards
   - Admission webhooks

4. **Restore storage resources**:
   - StorageClasses must exist before PVCs
   - Restore or recreate PersistentVolumes
   - Restore PersistentVolumeClaims
   - Wait for PVCs to bind before deploying applications

5. **Restore ConfigMaps and Secrets**:
   - These must exist before pods that reference them
   - Verify encryption keys if using etcd encryption at rest

6. **Restore workloads in dependency order**:
   - Databases and stateful applications first
   - Backend services before frontends
   - Worker deployments before job schedulers
   - Verify each tier reaches Running state before proceeding

7. **Restore services and networking**:
   - Services reconnect pods to networking
   - Ingress rules expose applications externally
   - Validate external connectivity

8. **Validation and testing**:
   - Check application health endpoints
   - Verify data integrity
   - Test critical workflows
   - Monitor error logs

**RTO and RPO planning**. Define recovery objectives based on business criticality:

- **Mission-critical applications**: RPO <15 minutes, RTO <30 minutes
  - Implement continuous replication + hourly backups
  - Automated failover with health checks
  - Hot standby environment ready
- **Production applications**: RPO 1-4 hours, RTO 2-4 hours
  - Backup every 4 hours
  - Tested restore procedures
  - Warm standby or documented recovery process
- **Development/staging**: RPO 24 hours, RTO 4-8 hours
  - Daily backups sufficient
  - Manual recovery acceptable

**Disaster recovery testing**. Regularly validate recovery capabilities:

```bash
# Quarterly DR drill procedure
# 1. Create isolated test environment
kubectl create namespace dr-test

# 2. Restore production backup to test namespace
velero restore create dr-drill-$(date +%Y%m%d) \
  --from-backup prod-daily-backup \
  --namespace-mappings production:dr-test

# 3. Measure recovery time (start to application ready)
time kubectl wait --for=condition=ready pod \
  -l app=critical-service \
  -n dr-test \
  --timeout=600s

# 4. Validate data integrity
kubectl exec -n dr-test deployment/database -- \
  /scripts/validate-data-integrity.sh

# 5. Test application functionality
kubectl exec -n dr-test deployment/webapp -- \
  /scripts/health-check.sh

# 6. Document results and improve
# 7. Clean up test environment
kubectl delete namespace dr-test
```

**Minimal downtime strategies**:

- **Blue-green deployment for DR**: Maintain secondary environment, switch DNS/load balancer during disaster
- **Canary recovery**: Restore portion of traffic (10%) to recovered environment, gradually increase
- **Active-active multi-region**: Deploy across multiple regions/clouds with global load balancing, automatic failover
- **Pre-staged recovery**: Maintain recent empty cluster with configurations ready, restore only data during disaster

### Backup Retention and Cost Optimization

**GFS (Grandfather-Father-Son) retention strategy**. Implement tiered retention balancing compliance, recovery needs, and cost:

- **Hourly (Son)**: Keep 24 restore points, 1 day retention
  - For applications requiring frequent recovery points
  - Store in high-performance storage (S3 Standard, Azure Hot)
- **Daily (Father)**: Keep 7 restore points, 1 week retention
  - Operational recovery window
  - Move to Standard-IA or Cool storage after 1 day
- **Weekly**: Keep 4-5 restore points, 1 month retention
  - Monthly operational needs
  - Move to Glacier Flexible Retrieval or Cool
- **Monthly (Grandfather)**: Keep 12 restore points, 1 year retention
  - Compliance and audit requirements
  - Store in Glacier or Archive tier
- **Yearly**: Keep 7 restore points, 7+ years retention
  - Long-term compliance (SOX, HIPAA)
  - Deep Archive or Archive tier

**Automated retention enforcement**:

```yaml
# Velero schedule with TTL
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: production-backup
spec:
  schedule: "0 */4 * * *"  # Every 4 hours
  template:
    ttl: 168h  # 7 days
    includedNamespaces:
      - production
    snapshotVolumes: true
```

**AWS S3 lifecycle policy**:

```json
{
  "Rules": [
    {
      "Id": "TransitionToIA",
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 7,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 30,
          "StorageClass": "GLACIER"
        },
        {
          "Days": 365,
          "StorageClass": "DEEP_ARCHIVE"
        }
      ],
      "Expiration": {
        "Days": 2555
      }
    }
  ]
}
```

**Storage tier pricing comparison** (per GB/month):

**AWS**:
- S3 Standard: $0.023
- S3 Standard-IA: $0.0125 (retrieval: $0.01/GB)
- S3 Glacier Flexible: $0.004 (retrieval: $0.03/GB, 3-5 hours)
- S3 Glacier Deep Archive: $0.00099 (retrieval: $0.02/GB, 12-48 hours)

**Azure**:
- Blob Hot: $0.0184
- Blob Cool: $0.01 (retrieval: $0.01/GB)
- Blob Archive: $0.002 (retrieval: $0.02/GB, 15 hours)

**Cost optimization strategies**:

1. **Compression**: Enable at backup tool level (Velero gzip, Kasten LZ4)
   - Typical reduction: 50-70%
   - Minimal CPU overhead
   - Faster transfers

2. **Deduplication**: Block-level dedup with Restic/Kopia
   - Savings: 40-70% for similar workloads
   - More effective with incremental backups
   - Small performance penalty during backup

3. **Incremental backups**: Backup only changed data
   - First backup: Full (100%)
   - Subsequent backups: 5-10% typical
   - 90-95% storage savings after initial

4. **Example cost calculation** (10TB application data):
   - **Without optimization**: 10TB × $0.023 = $230/month (S3 Standard)
   - **With compression (60% reduction)**: 4TB × $0.023 = $92/month
   - **With compression + dedup (70% combined)**: 3TB × $0.023 = $69/month
   - **With compression + dedup + tiering**:
     - Week 1 (Standard): 3TB × $0.023 = $69
     - Week 2-4 (Standard-IA): 9TB × $0.0125 = $112.50
     - Month 2-12 (Glacier): 33TB × $0.004 = $132
     - Total average: ~$25/month
   - **Total savings**: 89% reduction

**Cross-region and cross-cloud cost considerations**:
- AWS inter-region data transfer: $0.02/GB
- AWS egress to internet: $0.09/GB
- Azure inter-region: $0.02/GB
- Azure egress: $0.087/GB
- **Strategy**: Keep primary backups in same region (free), replicate weekly/monthly to DR region, compress before transfer

### Security Best Practices

**Encryption at rest**. Protect backup data using multiple encryption layers:

**AWS S3 encryption**:

```bash
# Server-side encryption with AWS KMS
aws s3api put-bucket-encryption \
  --bucket velero-backups \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "aws:kms",
        "KMSMasterKeyID": "arn:aws:kms:us-west-2:ACCOUNT:key/KEY-ID"
      },
      "BucketKeyEnabled": true
    }]
  }'
```

**Azure Blob encryption**:

```bash
# Enable encryption with customer-managed keys
az storage account update \
  --name velerostorage \
  --resource-group backups \
  --encryption-key-source Microsoft.Keyvault \
  --encryption-key-vault https://myvault.vault.azure.net \
  --encryption-key-name backup-key
```

**Velero client-side encryption**:

```bash
# Enable Restic encryption
velero install \
  ... \
  --use-node-agent \
  --uploader-type=restic
# Restic automatically encrypts with AES-256
```

**etcd encryption at rest**:

```yaml
# /etc/kubernetes/encryption-config.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
      - configmaps
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: <base64-encoded-32-byte-key>
      - identity: {}
```

**Encryption in transit**. Ensure all backup traffic uses TLS 1.2+:
- HTTPS-only for S3/Blob Storage access
- TLS for etcd client connections
- VPN or VPC peering for cross-cloud replication
- Encrypt before transmission for sensitive data

**Access control and least privilege**:

**AWS IAM policy** (minimal permissions):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::velero-backups",
        "arn:aws:s3:::velero-backups/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeVolumes",
        "ec2:DescribeSnapshots",
        "ec2:CreateSnapshot",
        "ec2:DeleteSnapshot",
        "ec2:CreateTags"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "ec2:ResourceTag/kubernetes.io/cluster/my-cluster": "owned"
        }
      }
    }
  ]
}
```

**Azure RBAC** (custom role):

```json
{
  "Name": "Velero Backup Operator",
  "IsCustom": true,
  "Description": "Minimal permissions for Velero",
  "Actions": [
    "Microsoft.Compute/disks/read",
    "Microsoft.Compute/disks/beginGetAccess/action",
    "Microsoft.Compute/snapshots/*",
    "Microsoft.Storage/storageAccounts/blobServices/containers/read",
    "Microsoft.Storage/storageAccounts/blobServices/containers/write"
  ],
  "NotActions": [],
  "AssignableScopes": ["/subscriptions/{subscription-id}"]
}
```

**Kubernetes RBAC for backup operations**:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: backup-operator
  namespace: production
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: backup-operator
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "list"]
  - apiGroups: ["velero.io"]
    resources: ["backups"]
    verbs: ["create", "get", "list"]
  - apiGroups: ["velero.io"]
    resources: ["restores"]
    verbs: ["get", "list"]  # No create permission
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: backup-operator
  namespace: production
subjects:
  - kind: ServiceAccount
    name: backup-operator
roleRef:
  kind: Role
  name: backup-operator
  apiGroup: rbac.authorization.k8s.io
```

**Immutable backups (WORM protection)**:

**AWS S3 Object Lock**:

```bash
# Enable Object Lock (must be done at bucket creation)
aws s3api create-bucket \
  --bucket velero-backups-immutable \
  --region us-west-2 \
  --object-lock-enabled-for-bucket

# Set default retention
aws s3api put-object-lock-configuration \
  --bucket velero-backups-immutable \
  --object-lock-configuration '{
    "ObjectLockEnabled": "Enabled",
    "Rule": {
      "DefaultRetention": {
        "Mode": "GOVERNANCE",
        "Days": 30
      }
    }
  }'
```

**Azure Blob immutability**:

```bash
# Set time-based retention policy
az storage container immutability-policy create \
  --account-name velerostorage \
  --container-name backups \
  --period 30
```

**Benefits of immutability**:
- Ransomware cannot encrypt or delete backups
- Prevents accidental deletion by administrators
- Meets compliance requirements (SEC 17a-4, FINRA)
- Provides audit-proof backup retention

**Air-gapped backup strategies**:

1. **Logical air gap**: Network isolation with delayed deletion
   - Separate AWS account with no direct network access
   - Cross-account S3 bucket replication
   - MFA required for deletion operations
   - 72-hour delay before deletion takes effect

2. **Physical air gap**: Offline media
   - Export backups to removable drives
   - Store drives in secure facility
   - Highest protection but slowest recovery

3. **Time-delayed replication**:
   - Primary backup location with immediate access
   - Secondary location with 24-hour replication delay
   - If primary compromised, secondary preserves day-old data

**Security implementation checklist**:
- ✅ Encryption at rest (KMS/Key Vault) for all backup storage
- ✅ Encryption in transit (TLS 1.2+) for all data transfers
- ✅ IAM/RBAC least privilege for backup service accounts
- ✅ MFA required for backup administrator access
- ✅ Immutable backups enabled (S3 Object Lock/Azure Blob immutability)
- ✅ Logical or physical air gap for critical backups
- ✅ Audit logging enabled for all backup operations
- ✅ Regular CIS Kubernetes benchmark scanning
- ✅ Secrets encrypted in etcd and backups
- ✅ Network policies restricting backup pod access
- ✅ Regular security reviews and penetration testing
- ✅ Incident response plan for backup compromise

### Preventing Vendor Lock-in

**Multi-cloud portability strategy**. Avoid dependence on single cloud provider or proprietary backup formats:

1. **Use Velero as universal tool**: Single backup solution works across AWS EKS, Azure AKS, GKE, and on-premises
   - Install with provider-specific plugins
   - Configure multiple BackupStorageLocations
   - Test restore from AWS backup to Azure cluster quarterly

2. **Portable backup formats**:
   - Kubernetes manifests in JSON/YAML (cloud-agnostic)
   - Velero uses TAR archives with standard structure
   - Restic repositories are portable across storage backends
   - Avoid proprietary formats from cloud-native backup services

3. **Cloud-agnostic storage backend**: Use S3-compatible object storage
   - MinIO (self-hosted S3-compatible)
   - Wasabi (cloud S3-compatible)
   - Ceph RGW (on-premises S3-compatible)
   - All major backup tools support S3 API

**Tool-agnostic approaches**:

**GitOps for configurations**:

```bash
# All Kubernetes manifests in Git
git-repo/
├── apps/
│   ├── production/
│   │   ├── deployments/
│   │   ├── services/
│   │   └── configmaps/
│   └── staging/
├── infrastructure/
│   ├── namespaces/
│   ├── rbac/
│   └── storage-classes/
└── argocd/
    └── applications/

# Backup is implicit (Git commits)
# Restore is GitOps sync (ArgoCD, Flux)
```

**Standard Kubernetes APIs**:
- CSI VolumeSnapshots work across all CSI drivers
- Standard PV/PVC API abstracts cloud storage
- Kubernetes-native backup tools use these APIs

**Application-specific backup tools** (truly portable):

```bash
# PostgreSQL
pg_dump -h postgres-service -U postgres -Fc dbname > backup.dump
# Restore works on any PostgreSQL, any cloud

# MySQL
mysqldump --all-databases > backup.sql
# Cloud-agnostic, database-native

# MongoDB
mongodump --archive=backup.archive --gzip
# Works across all MongoDB deployments

# Elasticsearch
curator_cli snapshot ...
# Native Elasticsearch snapshots
```

**Multi-tool backup strategy**:

**Primary**: Velero for Kubernetes resources + Restic for volumes
- Open-source, vendor-neutral
- Portable across all clouds
- No licensing costs

**Secondary**: Cloud-native for volume snapshots
- AWS EBS snapshots via Velero AWS plugin
- Azure Managed Disk snapshots via Velero Azure plugin
- Fast, efficient, but cloud-specific

**Tertiary**: Application-specific for critical databases
- Use native database backup tools
- Store backups in multiple clouds
- Truly portable across any infrastructure

**Testing cross-cloud portability**:

```bash
# Quarterly exercise: Restore AWS backup to Azure

# 1. Create backup in AWS EKS
velero backup create aws-to-azure-test --include-namespaces production

# 2. Wait for completion
velero backup describe aws-to-azure-test

# 3. Configure Azure cluster with AWS S3 access
velero backup-location create aws-source \
  --provider aws \
  --bucket velero-backups \
  --config region=us-west-2 \
  --access-mode=ReadOnly

# 4. Sync backup metadata
velero backup get

# 5. Restore to Azure with transformations
velero restore create aws-to-azure \
  --from-backup aws-to-azure-test \
  --namespace-mappings production:production-azure \
  --storage-class-mappings gp3:managed-csi

# 6. Validate application functionality
# 7. Document any issues for runbook updates
```

**Vendor lock-in prevention checklist**:
- ✅ Backup tool works on multiple clouds
- ✅ Backup format is open and documented
- ✅ Storage backend is S3-compatible or cloud-agnostic
- ✅ Restore tested to different cloud provider
- ✅ Application configurations in Git (GitOps)
- ✅ Database backups use native tools
- ✅ No dependency on cloud-specific APIs in application code
- ✅ CSI drivers used for all persistent storage
- ✅ Quarterly cross-cloud DR drills performed

### Production Implementation Roadmap

**Immediate action items** for establishing Kubernetes backup:

**Week 1: Deploy automated etcd backups**

```bash
# Cron job for etcd backup
kubectl apply -f - <<EOF
apiVersion: batch/v1
kind: CronJob
metadata:
  name: etcd-backup
  namespace: kube-system
spec:
  schedule: "0 */12 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: k8s.gcr.io/etcd:3.5.6
            command:
            - /bin/sh
            - -c
            - |
              ETCDCTL_API=3 etcdctl \
                --endpoints=https://127.0.0.1:2379 \
                --cacert=/etc/kubernetes/pki/etcd/ca.crt \
                --cert=/etc/kubernetes/pki/etcd/server.crt \
                --key=/etc/kubernetes/pki/etcd/server.key \
                snapshot save /backup/etcd-\$(date +%Y%m%d-%H%M%S).db
              # Upload to S3/Azure Blob
            volumeMounts:
            - name: etcd-certs
              mountPath: /etc/kubernetes/pki/etcd
            - name: backup
              mountPath: /backup
          volumes:
          - name: etcd-certs
            hostPath:
              path: /etc/kubernetes/pki/etcd
          - name: backup
            persistentVolumeClaim:
              claimName: etcd-backup-pvc
          restartPolicy: OnFailure
          hostNetwork: true
EOF
```

**Week 2: Deploy Velero with Restic**
- Follow AWS or Azure installation procedures provided earlier
- Create hourly backup schedule for critical namespaces
- Test restore to isolated namespace

**Week 3: Enable immutability and encryption**
- Configure S3 Object Lock or Azure Blob immutability
- Enable KMS encryption for backup storage
- Implement RBAC restricting backup access

**Month 1: Conduct full DR test**
- Perform complete cluster restore in isolated environment
- Measure and document RTO/RPO
- Update runbooks based on findings

**Cost optimization quick wins** (implement immediately):
- Enable compression: 50-70% reduction, no downside
- Configure lifecycle policies: Automatic tiering saves 60-80%
- Implement incremental backups: 90%+ storage reduction
- Combined savings: 70-90% total cost reduction

### Conclusion

Effective Kubernetes backup and disaster recovery across AWS and Azure requires a comprehensive multi-layered approach that protects control plane state, persistent data, and application configurations. **The most successful implementations combine open-source tools like Velero with enterprise solutions like Kasten K10**, leverage cloud-agnostic storage formats to prevent vendor lock-in, and implement automated retention policies with intelligent tiering for cost optimization.

Critical success factors include regular disaster recovery testing (quarterly minimum), proper recovery sequencing starting with etcd and progressing through namespaces to applications, robust security measures including encryption and immutable backups, and cross-cloud portability validation. Organizations should implement the GFS retention strategy, automate lifecycle policies to achieve 70-90% cost savings, and use application-aware backup hooks for databases requiring transactional consistency.

The recommended approach starts with Velero as a universal backup foundation providing portability across clouds, adds CSI VolumeSnapshots for Kubernetes-native volume protection, implements Restic for file-level backups of any volume type, and supplements with application-specific tools for critical databases. This multi-tool strategy balances cost, flexibility, and vendor independence while maintaining enterprise-grade data protection.

Immediate priorities for any Kubernetes deployment include deploying automated etcd backups within week one, installing Velero with Restic by week two, enabling immutability and encryption by week three, and conducting a full disaster recovery drill within the first month. These foundational steps ensure that when disaster strikes—whether from infrastructure failure, data corruption, ransomware, or operator error—recovery is measured in minutes rather than hours, with confidence that applications and data will be fully restored across any cloud environment.
