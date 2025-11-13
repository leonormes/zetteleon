---
aliases: []
confidence: 
created: 2025-11-11T12:55:24Z
epistemic: 
last_reviewed: 
modified: 2025-11-12T14:24:53Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [7276, 8595]
title: Kubernetes Multi-Cloud Backup Best Practices
type: 
uid: 
updated: 
---

## **Architect's Guide to Multi-Cloud Kubernetes Backup and Disaster Recovery: AWS EKS and Azure AKS**

### **A Comparative Analysis of Strategies, Tooling, and Practical Implementation**

#### **Part 1: The Kubernetes Backup Inventory: What to Protect and Why**

A successful Kubernetes backup strategy begins with a precise understanding of *what* must be protected. Unlike traditional virtual machine backups, which produce a single monolithic artifact, a Kubernetes backup is a composite of distinct, decoupled data tiers.1 An effective multi-cloud strategy must address each tier appropriately, as each has different backup methods, restoration procedures, and portability characteristics.

##### **1.1 The Misconception of "Full Backup"**

In a traditional IT context, a "full backup" implies a complete, point-in-time image of a server. In Kubernetes, this concept is misleading. A cluster is a dynamic, declarative system. A "backup" is less about a single image and more about capturing the *desired state* of applications (the resource objects) and the *actual state* of their data (the persistent volumes).1

While it is possible to manually inventory resources by using kubectl get commands to export YAML definitions for Deployments, Services, ConfigMaps, and Secrets 2, this method is insufficient. It provides a static, partial inventory but lacks the critical coordination with persistent data snapshots and fails to capture the ongoing state of a live system.

##### **1.2 Tier 1: Control Plane State (etcd)**

The etcd key-value store is the definitive database for all Kubernetes cluster data; it is the control plane's "brain".4 Every Deployment, Secret, ConfigMap, and Pod definition is stored in etcd.6

- **Backup Method:** For self-managed clusters, a direct snapshot of the etcd database is performed using the etcdctl snapshot save command.6 This creates a single snapshot.db file.  
- **Restoration:** This is a last-resort, "total cluster failure" scenario. The official procedure is highly disruptive: **all** kube-apiserver instances *must* be stopped before initiating the restore.6 The cluster is effectively offline during this operation.  
- **Limitations and Multi-Cloud Context:**  
  - **Managed Services (EKS/AKS):** For the environments specified in this report (AWS EKS and Azure AKS), etcd backup is largely a non-viable strategy for application-level recovery. Cloud providers manage the control plane, and direct access to etcd is restricted.9  
  - **Incomplete Data:** An etcd backup captures *only* the Kubernetes resource definitions. It does *not* include the data inside Persistent Volumes.9  
  - **Brittleness:** Restores are highly sensitive to versioning. An etcd snapshot must be restored to a cluster of the same Kubernetes major and minor version.10

Given these limitations, etcd backup should be viewed as a **cluster-level** DR tool (for total control plane failure), which is the responsibility of the cloud provider in EKS/AKS. It is *not* an **application-level** backup or multi-cloud migration tool.

##### **1.3 Tier 2: Kubernetes Resource Objects (The Application's "Shape")**

This tier represents the *desired state* of applications as defined by engineers and stored via the Kubernetes API. This is the primary target for modern, Kubernetes-native backup tools.

- **What it is:** The collection of YAML/JSON manifests that define all application components 3:  
  - **Workloads:** Deployments, StatefulSets, DaemonSets, Jobs.  
  - **Configuration:** ConfigMaps, Secrets.  
  - **Network:** Services, Ingresses, NetworkPolicies.  
  - **Storage Metadata:** PersistentVolumeClaims (PVCs), PersistentVolumes (PVs), StorageClasses.  
  - **Access Control:** Namespaces, ServiceAccounts, Roles, RoleBindings.  
- **Backup Method:** Modern tools like Velero and Kasten K10 back up this tier by querying the Kubernetes API server directly (not by accessing etcd). They retrieve these resource definitions and serialize them (as JSON or YAML) into a compressed file, which is then stored in an off-cluster object storage location (like AWS S3 or Azure Blob).1  
- **Portability:** This data is inherently portable. As text-based definitions, these resources can be restored to any compatible Kubernetes cluster.

##### **1.4 Tier 3: Application Data (Persistent Volumes)**

This tier is the *actual stateful data* used by applications, such as database files or user-uploaded content. This data resides on physical (or virtual) storage provisioned by the cluster.4

- **What it is:** The data blocks inside a PersistentVolume (PV), which is requested by a PersistentVolumeClaim (PVC).13  
- **The Critical Distinction:** Backing up the Tier 2 PersistentVolumeClaim object *only* backs up the YAML *request* for storage (e.g., "I need 50 GiB of fast storage"). It **does not** back up the 50 GiB of data *inside* that storage.1 A separate, dedicated mechanism is required for Tier 3, which is the most complex aspect of multi-cloud backup.

A complete and robust backup solution must treat the application as the unit of atomicity, capturing a consistent, point-in-time copy of both Tier 2 resources and their associated Tier 3 data.14 The following table summarizes this three-tier framework.

| Tier | Component | What It Is | Backup Method | Portability | Managed by (Tool) |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Tier 1:** Control Plane State | etcd Database | All cluster object definitions and state.6 | etcdctl snapshot 7 or cloud provider snapshot. | Low. Tied to K8s version and infrastructure.11 | Managed Kubernetes Service (EKS/AKS). |
| **Tier 2:** Resource Objects | YAML/JSON Manifests | Deployments, Services, Secrets, PVCs, etc..3 | API-server query and serialization to object storage.1 | High. Text-based definitions. | Velero, Kasten K10.7 |
| **Tier 3:** Application Data | PersistentVolumes | The actual data blocks on disk (e.g., AWS EBS, Azure Disk).12 | CSI Snapshots 15 or File-Level Backup (Restic/Kopia).16 | Varies (Low for CSI, High for File-Level).17 | Velero, Kasten K10.7 |
|  |  |  |  |  |  |

#### **Part 2: Core Strategies for Persistent Volume (Tier 3) Backup**

Backing up stateful application data (Tier 3) presents the central architectural challenge for multi-cloud DR. The choice of strategy involves a direct trade-off between **In-Cloud Resilience (Speed)** and **Cross-Cloud Portability (Flexibility)**.

##### **2.1 The Role of the Container Storage Interface (CSI)**

The Container Storage Interface (CSI) is the standard for exposing storage systems to Kubernetes.18 It provides a common API for operations like provisioning volumes and, most importantly, creating snapshots.15 Both AWS and Azure provide robust CSI drivers for their native block storage solutions:

- **AWS:** The ebs.csi.aws.com driver integrates Amazon Elastic Block Store (EBS).19  
- **Azure:** The disk.csi.azure.com driver integrates Azure Managed Disks.19

Backup tools use the generic Kubernetes VolumeSnapshot API object to request a snapshot, and the CSI driver handles the cloud-specific implementation.15

##### **2.2 Strategy 1: Native CSI Volume Snapshots (In-Cloud Resilience)**

This is the default and fastest method for backing up persistent data.

- **Mechanism:** A backup tool (like Velero or Kasten K10) instructs the CSI driver to create a VolumeSnapshot. The driver, in turn, calls the native cloud provider API (e.g., the AWS API to create an EBS snapshot or the Azure API to create a Managed Disk snapshot).1  
- **Pros:**  
  - **Speed:** Extremely fast, as it leverages the underlying storage platform's highly optimized, block-level snapshot capabilities.25  
  - **Efficiency:** Snapshots are typically incremental at the block level, saving on storage costs.24  
  - **Consistency:** Provides a "crash-consistent," point-in-time copy of the entire disk.25  
- **Cons (The Critical Limiter):**  
  - **Non-Portable:** This is the most critical fact for multi-cloud architectures. An AWS EBS snapshot is an AWS-proprietary object and an Azure Disk snapshot is an Azure-proprietary object. It is **not possible** to restore an EBS snapshot to an Azure Disk, or vice-versa.17  
- **Use Case:** This strategy is ideal for high-frequency, operational recoveries: recovering from accidental data deletion, rolling back a failed application upgrade, or performing DR *within the same cloud region*.

It is important to correct a common misconception: while the CSI API itself is a "portable" standard 27, the snapshot *artifacts* it produces are **not**. An architecture built *only* on CSI snapshots has a robust in-cloud resilience strategy but **no cross-cloud portability**.

##### **2.3 Strategy 2: Logical File-Level Backups (Cross-Cloud Portability)**

This strategy bypasses provider-specific snapshots in favor of a logical, file-based approach.

- **Mechanism:** This method uses a file-level backup tool like **Restic** 29 or **Kopia** 16, which are often integrated directly with Velero. A privileged DaemonSet mounts the live application volume and performs a file-by-file copy, uploading the (deduplicated and compressed) data to a cloud-agnostic object storage bucket (S3/Blob).17  
- **Pros:**  
  - **Fully Portable:** The backup is simply a collection of data blocks in an object storage bucket. It is 100% cloud-agnostic and provides the true "vendor lock-in avoidance" required for a multi-cloud DR strategy.17  
- **Cons:**  
  - **Speed:** Significantly slower than a block-level snapshot, as it must traverse the entire filesystem.25  
  - **Performance Impact:** Performs heavy I/O on the *live* application volume, which can degrade application performance during the backup.  
  - **Consistency:** Because the backup can take a long time, there is a risk of data modification *during* the backup process, leading to potential inconsistencies.25

##### **2.4 Strategy 3: Snapshot Data Movement (The Hybrid "Best-of-Both")**

This advanced technique, now the preferred method for portable backups, combines the strengths of the previous two strategies.

- **Mechanism:**  
  1. Velero first requests a fast, consistent **CSI snapshot** (Strategy 1).  
  2. A Velero node-agent pod then mounts this *snapshot* (not the live volume).  
  3. Velero uses **Kopia** 16 to perform the portable, file-level backup *from the static snapshot*.  
  4. Once the upload to object storage is complete, the temporary CSI snapshot is deleted.  
- **Configuration:** In Velero, this is often enabled via the snapshotMoveData: true flag in the backup configuration.16  
- **Pros:**  
  - **Consistent:** Achieves the perfect, point-in-time consistency of a CSI snapshot.25  
  - **Low Impact:** The high-I/O file-scanning work is performed against the *snapshot*, not the live production volume.25  
  - **Portable:** The final backup artifact is a fully portable, logical copy in object storage, identical to Strategy 2.16  
- **Cons:**  
  - Requires additional temporary storage headroom on the cluster's storage platform to hold the snapshot during the backup process.25  
- **Use Case:** This is the **architect-recommended** strategy for cross-cloud DR.

The optimal architecture is not to choose one strategy, but to use a hybrid, policy-driven approach. For example, an organization should:

- Run **Daily Backups** using **Strategy 1 (Native CSI Snapshots)** for fast, operational, in-cloud recovery. Retain these for 7 days.  
- Run **Weekly DR Backups** using **Strategy 3 (Snapshot Data Movement)** to create a full, portable copy. Replicate this backup artifact to the DR cloud (e.g., from S3 to Azure Blob) and retain it for 30 days.

This multi-policy model provides both operational speed and true DR portability.

| Strategy | Mechanism | Key Velero Flag | Pros | Cons | Use Case |
| :---- | :---- | :---- | :---- | :---- | :---- |
| 1. Native CSI Snapshot | Cloud Provider's block snapshot (EBS, Azure Disk) via CSI.15 | --snapshot-volumes=true | Extremely fast, low-impact, crash-consistent.25 | **Not portable across clouds**.17 | Operational recovery, in-cloud DR. |
| 2. Logical File-Level Backup | File-by-file copy from *live* volume (Restic/Kopia).16 | --use-restic or --use-kopia | **Fully portable**, storage-agnostic.17 | Slow, high I/O impact, potential for inconsistency.25 | Cross-cloud migration, archival. |
| 3. Snapshot Data Movement | 1. CSI snapshot (for consistency). 2. Kopia uploads *snapshot* data to S3/Blob.16 | snapshotMoveData: true 16 | **Best of both:** Fast, consistent snapshot + **portability**.25 | Newer feature, requires snapshot storage headroom.25 | **Recommended Cross-Cloud DR**. |
|  |  |  |  |  |  |

#### **Part 3: Ensuring Application Consistency (Application-Aware Backups)**

For stateful applications like databases, a "crash-consistent" snapshot (Strategy 1) is not enough. Data may be in memory buffers and not yet flushed to disk, leading to a corrupt or incomplete restore.31 "Application-consistent" backups are required, which ensure the application is in a clean, quiesced state *before* the snapshot is taken.31

##### **3.1 Implementation: Preand Post-Backup Execution Hooks**

Kubernetes-native backup tools achieve application consistency by using execution hooks to run commands *inside* the application's container at specific points in the backup lifecycle.31

- **Velero Hooks:** Velero implements hooks using simple Kubernetes annotations on the Pod object.34  
  - pre.hook.backup.velero.io/command: Runs *before* the backup (e.g., to quiesce the database).  
  - post.hook.backup.velero.io/command: Runs *after* the snapshot (e.g., to un-quiesce the database).  
- **Kasten K10 (Kanister):** Kasten uses a more structured, open-source framework called Kanister.36 Instead of simple annotations, a Blueprint (a Custom Resource) defines the multi-step backup and restore "phases" for a specific application (e.g., "quiesce," "dump," "restore").26

This "application-aware" model shifts responsibility. The infrastructure team provides the backup *platform* (Velero/Kasten), but the application team *must* define the consistency *logic* (the hooks or Blueprints). This is a critical organizational best practice: backup logic should be embedded within the application's own deployment manifests (e.g., its Helm chart or Kustomize base).

##### **3.2 Practical Example: Backing up PostgreSQL with Velero**

To create an application-consistent backup of a PostgreSQL database, a pre-hook annotation is used to run pg_dump. This dumps the database's logical content into a SQL file *on a persistent volume*.37 Velero then backs up that volume, capturing both the physical database files *and* the clean, logical SQL dump.

The pod definition would include annotations similar to the following:

YAML

apiVersion: v1  
kind: Pod  
metadata:  
  name: postgres-pod  
  annotations:  

## 1. Define the Pre-backup Hook Command
    pre.hook.backup.velero.io/command: '["/bin/sh", "-c", "pg_dump -U myuser -d mydb -f /var/lib/postgresql/data/dump.sql"]'  
## 2. Specify the Container to Run the Command in
    pre.hook.backup.velero.io/container: "postgres"  
## 3. Set a Timeout
    pre.hook.backup.velero.io/timeout: "5m"  

spec:  
  containers:  

  - name: postgres  
    image: postgres:15  
    volumeMounts:  
    - mountPath: /var/lib/postgresql/data  
      name: pg-data  
  volumes:  
  - name: pg-data  
    persistentVolumeClaim:  
      claimName: pg-data-pvc

A corresponding post.hook.restore.velero.io annotation can be used to run psql < /var/lib/postgresql/data/dump.sql on restore, allowing for a choice between a full physical volume restore or a faster logical data import.38

### **Part 4: Tooling Deep Dive: Velero vs. Kasten K10**

The two most prominent tools for Kubernetes-native backup are the open-source Velero and the enterprise-grade Kasten K10.3

#### **4.1 Velero (Open Source, Plugin-Driven)**

Velero is an open-source tool (originated by Heptio, now VMWare) that operates as a controller in the cluster, managed via a CLI and Custom Resources (CRDs).39 Its multi-cloud capability is enabled by a powerful plugin system.41

- **Multi-Cloud Primitives:**  
  - BackupStorageLocation (BSL): A CRD that defines *where* to store Tier 2 (YAML) and logical Tier 3 (Restic/Kopia) data. This points to an object storage bucket (e.g., AWS S3 or Azure Blob).42  
  - VolumeSnapshotLocation (VSL): A CRD that defines *where* to store native Tier 3 CSI snapshots (e.g., a specific AWS region for EBS or an Azure resource group for Disks).42

##### **4.1.1 Velero Implementation for AWS EKS**

- **Storage (BSL):** An AWS S3 bucket.44  
- **Snapshots (VSL):** Amazon EBS snapshots.41  
- **Identity:** The recommended approach is **IRSA (IAM Roles for Service Accounts)**, which grants the Velero pods fine-grained permissions to S3 and EC2 (for snapshots) without using static keys.47  
- **Example velero install Command (using IRSA):**  
## Assumes IRSA is Configured for the 'velero' Service account

  velero install

    --provider aws

    --plugins velero/velero-plugin-for-aws:v1.13.0

    --bucket <YOUR-S3-BUCKET-NAME>

    --backup-location-config region=<YOUR-REGION>

    --snapshot-location-config region=<YOUR-REGION>

    --use-kopia

    --wait

### **4.1.2 Velero Implementation for Azure AKS**

- **Storage (BSL):** An Azure Blob Storage container.29  
- **Snapshots (VSL):** Azure Managed Disk snapshots.29  
- **Identity:** The recommended approach is **Microsoft Entra Workload Identity**, which, like IRSA, provides secure, "secret-less" pod-level identity.48  
- **Example velero install Command (using Service Principal, legacy method):**  
  Bash  
## Create the Credentials-velero File with SP Details [29, 50]

  AZURE_BACKUP_RESOURCE_GROUP=Velero_Backups  
  AZURE_STORAGE_ACCOUNT_ID=...  
  BLOB_CONTAINER=velero

  velero install

    --provider azure

    --plugins velero/velero-plugin-for-microsoft-azure:v1.13.0

    --bucket $BLOB_CONTAINER

    --secret-file./credentials-velero

    --backup-location-config resourceGroup=$AZURE_BACKUP_RESOURCE_GROUP,storageAccount=$AZURE_STORAGE_ACOUNT_ID

    --snapshot-location-config resourceGroup=$AZURE_RESOURCE_GROUP

    --use-kopia

    --wait

  *(Note: The Workload Identity setup is more complex and involves pre-configuring the federated identity, but is the recommended practice over the --secret-file method.)*

### **4.2 Kasten K10 (Enterprise, Application-Centric)**

Kasten K10 (by Veeam) is a "purpose-built data management platform" designed for enterprise-scale operations.3 It runs in its own namespace (kasten-io) 55 and is primarily managed via a graphical dashboard.55

- **Key Differentiators:**  
  - **Application Discovery:** Automatically discovers applications (e.g., by Helm release, operator, or labels) rather than forcing users to back up entire namespaces.55  
  - **Policy-Driven:** Focuses on high-level, policy-driven automation. An operator defines a "Gold" policy (e.g., backup every 4 hours, export to S3, retain for 30 days) and applies it to applications.55  
  - **Application Mobility:** Cross-cluster and cross-cloud migration is a core, automated feature.3  
- **Kasten Implementation for AWS/Azure:** Kasten uses "Location Profiles" to define S3 or Azure Blob storage targets.58 It natively integrates with the AWS and Azure CSI drivers for snapshots 26 and supports IRSA and Workload Identity for authentication.58 An operator typically accesses the dashboard (via kubectl port-forward55), creates a policy, and adds an "Export" action to that policy to push backup data to an S3 or Blob location for DR.

The fundamental distinction is that Velero is a powerful **toolkit**, while Kasten K10 is a comprehensive **platform**. A heavily CLI-driven DevOps team may prefer Velero's flexibility and CRD-based nature. An enterprise IT organization that requires a "single pane of glass," RBAC-driven delegation, and automated application mobility will find Kasten K10's abstractions valuable.

| Feature | Velero (Open Source) | Kasten K10 (Enterprise) | Architect's Note |
| :---- | :---- | :---- | :---- |
| **Model** | Open-source toolkit, plugin-driven.40 | Commercial data management platform.3 | Toolkit vs. Platform. |
| **Primary Interface** | CLI 60, Kubernetes CRDs. | Web Dashboard 55, Policy CRDs. | Kasten is built for delegation and visibility. |
| **App-Awareness** | Pre/Post-execution hooks (Pod annotations).34 | Kanister Blueprints (CRDs).36 | Kanister is a more structured, reusable framework. |
| **Multi-Cloud** | BackupStorageLocation plugins.41 | "Location Profiles".58 | Both are purpose-built for multi-cloud. |
| **Cross-Cloud Migration** | Manual. Requires file-level backup (Restic/Kopia) and manual StorageClass mapping.17 | Automated. A core feature ("Application Mobility").3 | Kasten streamlines the cross-cloud restore process. |
| **Cost** | Free (open source). Commercial support available. | Licensed (per node/Veeam). | TCO (time/risk) vs. License Cost. |
|  |  |  |  |

## **Part 5: Multi-Cloud Identity and Security Best Practices**

Securing the backup system is as important as the backup itself. This involves two domains: protecting the *data* (encryption) and protecting the *access* (identity).

### **5.1 Securing Backup Data (Encryption)**

- **Encryption-in-Transit:** All communication between the backup tools and cloud storage endpoints (S3, Azure Blob) must be enforced over TLS.62  
- **Encryption-at-Rest:**  
  - **Object Storage:** Server-side encryption must be enabled on the AWS S3 bucket (SSE-S3 or SSE-KMS) and the Azure Blob container.62  
  - **Cluster Secrets:** Kubernetes Secrets (which are base64-encoded, not encrypted, by default) must be protected using "encryption at rest" for the etcd database.63  
- **Immutability:** For ransomware protection, backups should be stored in an immutable state. This is achieved using **AWS S3 Object Lock** or **Azure Blob Immutable Storage**.62 This prevents backups from being altered or deleted, even by a privileged account, for a defined retention period.

### **5.2 Securing Backup Access (Identity)**

The "best practice" for identity has evolved from static secrets to dynamic, short-lived tokens.

- **Legacy Model (Anti-Pattern):** This model uses static, long-lived credentials, such as an IAM User's aws_access_key_id/secret_access_key 46 or an Azure Service Principal's client secret.29 These are stored in a Kubernetes Secret. This is a significant security risk; if the secret is compromised, the attacker gains high-privilege access to the storage account.  
- Modern Model (Recommended): OIDC Federation:  
  This "secret-less" pattern uses OpenID Connect (OIDC) to establish trust between the Kubernetes cluster and the cloud provider's IAM system.  
  - **On AWS (EKS):** This is **IAM Roles for Service Accounts (IRSA)**.47 The EKS cluster's OIDC issuer is trusted by an IAM Role. The Velero pod's ServiceAccount is annotated with that role. The pod exchanges its internal Kubernetes token for temporary AWS credentials from the AWS STS service, eliminating the need for static keys.  
  - **On Azure (AKS):** This is **Microsoft Entra Workload Identity**.48 The concept is identical. A "federated credential" is created in Entra ID, which trusts the AKS cluster's OIDC issuer and a specific ServiceAccount. The pod exchanges its token for an Entra ID token, eliminating the need for a Service Principal secret.

### **5.3 The Advanced Pattern: Cross-Cloud OIDC Federation**

This is the expert-level solution for a fully integrated multi-cloud DR strategy. It allows a pod in one cloud (EKS) to *natively and securely* authenticate to another cloud (Azure) *without any secrets*.

- **Scenario:** An EKS cluster needs to write DR backups *directly* to an Azure Blob container.  
- **Mechanism:**  
  1. An Azure Managed Identity is created with permissions to the Azure Blob container.  
  2. A "federated credential" is added to this Managed Identity.  
  3. This federated credential is configured to trust the **EKS cluster's OIDC Issuer URL** and the specific ServiceAccount of the Velero pod running on EKS.68  
  4. The Velero pod on EKS can now use its AWS-issued Kubernetes token to request an *Azure AD* token.  
  5. Velero uses this token to authenticate directly to Azure Blob.  
- **Implication:** This pattern (which also works in reverse from AKS to S3 71) radically simplifies the DR data path. It eliminates the need for an intermediate azcopy step (detailed in Part 6). A backup schedule on EKS can be configured to write *directly* to the Azure DR location, making the DR data "warm" and dramatically reducing the Recovery Time Objective (RTO).

## **Part 6: The Multi-Cloud Disaster Recovery Playbook: EKS to AKS**

This section provides a practical, step-by-step playbook for the user's core scenario: restoring an EKS backup to a new AKS cluster.

### **6.1 Pre-Restore: Resource Mapping**

A cross-cloud restore is not a simple "click-to-restore" operation. It is a *migration* that requires mapping resources from the AWS ecosystem to the Azure ecosystem.

| AWS EKS Resource | Azure AKS Equivalent | Velero Action Required |
| :---- | :---- | :---- |
| StorageClass (e.g., gp3) 19 | StorageClass (e.g., managed-csi-premium) 19 | **Critical:** Create a Velero ConfigMap to map storage classes.30 |
| PersistentVolume (AWS EBS) | PersistentVolume (Azure Managed Disk) | Velero restores PV/PVC YAML. Data **must** be from Restic/Kopia.17 |
| AWS S3 (Backup Storage) | Azure Blob Storage (Backup Storage) 73 | Velero BSL on AKS must point to Blob. Data must be copied.30 |
| AWS IRSA (Pod Identity) 47 | Azure Workload Identity (Pod Identity) 48 | Velero on AKS must be configured with Workload Identity to read from Blob.51 |
|  |  |  |

### **6.2 Playbook A: Standard (Reactive) Migration/DR**

This playbook is ideal for a one-time, planned *migration* or a *cold* DR scenario where backup data is not pre-staged.30

- **Step 1: Backup from EKS**  
  - Install Velero on EKS (see Part 4.1.1).  
  - Create the backup. It is **essential** to use a file-level backup method (Restic or Kopia) to ensure the PV data is portable.17  
    Bash  
## Use --use-kopia (or --use-restic) for a Portable, File-level Backup
## --snapshot-volumes=false Is Used with restic/kopia-only Backups
## Alternatively, Use Strategy 3 (Snapshot Data Movement) if Configured
    velero backup create eks-to-aks-backup   
      --include-namespaces my-app   
      --use-kopia   
      --snapshot-volumes=false   
      --wait

- **Step 2: Data Transfer (S3 to Azure Blob)**  
  - The Velero backup (resources and Kopia data) now exists in the S3 bucket. This data must be replicated to the Azure Blob container.  
  - Use the azcopy tool for this out-of-band transfer.30  
    Bash  
## Authenticate Azcopy to both AWS (S3) and Azure (Blob)
    azcopy copy 'https://<s3-bucket>.s3.amazonaws.com/backups'   
      'https://<blob-acct>.blob.core.windows.net/<container>/backups'   
      --recursive

- **Step 3: Prepare AKS for Restore**  
  - Install Velero on the new AKS cluster, configured to use the Azure Blob container (see Part 4.1.2). Set the BackupStorageLocation to accessMode: ReadOnly.29  
  - **CRITICAL: Create StorageClass Mapping:** This is the most important technical step. Without it, the restore will fail. Create a ConfigMap in the velero namespace to map the EKS StorageClass name to the desired AKS StorageClass name.30  
  - **Example sc-map.yaml:**  
    YAML  

```sh
apiVersion: v1  
kind: ConfigMap  
metadata:  
  name: change-storage-class  
  namespace: velero  
  labels:  
    # Identifies this as a config for Velero's built-in plugin  
    velero.io/plugin-config: ""  
    velero.io/change-storage-class: RestoreItemAction  
data:  
  # Map the EKS StorageClass "gp3" to the AKS StorageClass "managed-csi-premium"  
  gp3: managed-csi-premium  
  # Map any other classes  
  gp2: managed-csi`
```

  - Apply this file: kubectl apply -f sc-map.yaml.  
- **Step 4: Restore to AKS**  
- Run the Velero restore, referencing the backup name and the new ConfigMap.  

```sh
# Verify Velero on AKS can see the backup: velero backup get  
velero restore create restore-from-eks   
  --from-backup eks-to-aks-backup   
  --storage-class-mappings-config-map change-storage-class   
  --wait
```

- **Step 5: Post-Restore Validation**  
  - Verify PersistentVolumeClaims are Bound (not Pending).  
  - Verify application pods are running.  
  - Manually update any cloud-specific resources, such as Service objects of type: LoadBalancer (which will have a new IP), Ingress hostnames, or container image references still pointing to Amazon ECR.30

### **6.3 Playbook B: Advanced (Proactive) DR**

This playbook uses the OIDC federation pattern (Part 5.3) for a *hot* DR scenario, eliminating the manual azcopy step and its associated RTO delay.

- **Step 1: Setup Cross-Cloud Federation (One-time)**  
  - On Azure, create a Managed Identity and add a federated credential that trusts the **EKS cluster's OIDC issuer**.69  
- **Step 2: Configure EKS Velero with Two BSLs**  
  - On the EKS cluster, configure velero backup-location create twice:  
    1. s3-local: The default BSL, points to S3, uses IRSA.  
    2. azure-dr: A second BSL, points to Azure Blob, uses the OIDC federation credentials.  
- **Step 3: Proactive Backup Scheduling**  
  - Create two schedules on the EKS cluster:  
    Bash  
## 1. Daily, Fast, In-cloud Snapshots for Operational Recovery
    velero schedule create daily-local-ops   
      --schedule="@daily"   
      --snapshot-volumes=true   
      --storage-location s3-local   
      --ttl 168h # 7 days

## 2. Weekly, Portable, DR-ready Backup Sent *directly* to Azure
    velero schedule create weekly-dr-to-azure   
      --schedule="@weekly"   
      --use-kopia   
      --snapshot-volumes=false   
      --storage-location azure-dr   
      --ttl 720h # 30 days

- **Step 4: Restore to AKS (On-Demand)**  
  - When disaster strikes, the data is **already** in Azure Blob.  
  - Install Velero on AKS (as in Playbook A).  
  - Create the StorageClass mapping ConfigMap.74  
  - Run the velero restore create command immediately. No azcopy is needed. This reduces RTO from "hours/days" to "minutes."

### **Part 7: Recovery, Retention, and Cost Optimization**

A complete strategy extends beyond the backup itself to include the full lifecycle management of recovery, retention, and cost.

#### **7.1 Recovery Order Best Practices**

Complex, microservice-based applications cannot be restored all at once. Dependencies must be respected. A DR playbook 2 must restore components in the correct sequence. The logical order is 77:

1. **Foundational Services:** Namespaces, RBAC, Secrets, ConfigMaps.  
2. **Data Stores:** StatefulSets and their PersistentVolumes (e.g., databases).  
3. **Application Services:** Deployments and Services (which depend on the data stores).

This is best implemented by using labels and selectors. At *backup* time, create separate, labeled backups (e.g., velero backup create... --selector "app-tier=database" and ... --selector "app-tier=frontend"). At *restore* time, the DR playbook can restore the "database" backup first, wait for it to be healthy, and only then restore the "frontend" backup.

#### **7.2 Backup Retention Policies (GFS)**

To balance recovery granularity with storage cost, a **Grandfather-Father-Son (GFS)** policy is a proven standard.78

- **Son (Daily):** Daily backups for operational recovery, retained for 7-14 days.  
- **Father (Weekly):** A full backup from one "Son" (e.g., Sunday's), retained for 4-6 weeks.  
- **Grandfather (Monthly):** The last "Father" of the month, retained for 12-24+ months for archival and compliance.

Kasten K10 has GFS policies as a built-in feature.57 In Velero, this is implemented by creating multiple velero schedule create commands, each with a different schedule (@daily, @weekly, @monthly) and a different --ttl (time-to-live) value.

#### **7.3 Cost Optimization Strategies**

Storing petabytes of backup data, especially portable file-level data, can become expensive.

- **Storage Tiering:** This is the primary cost control. Use cloud-native lifecycle policies to automatically transition backup data from "hot" (and expensive) storage (S3 Standard / Azure Hot) to "cold" (and cheap) archival storage (S3 Glacier / Azure Archive) after a set period, such as 30 days.81  
- **Deduplication:** Using logical backup tools like Kopia and Restic inherently provides block-level deduplication, which significantly reduces the total storage footprint compared to storing many full snapshots.

A critical architectural conflict exists between immutability 62 and cost-tiering.83 An S3 Object Lock (immutability) *prevents* a lifecycle policy from moving an object to Glacier until the lock expires. An architect must resolve this by:

1. Accepting higher cost for the immutability period (e.g., 30 days in S3 Standard).  
2. Using a hybrid model: Use S3 Object Lock for 30 days. Use S3 Cross-Region or Cross-Account Replication to copy the backup to a separate "archive account." This second, air-gapped account has different security keys and a different, aggressive lifecycle policy (e.g., move to Glacier Deep Archive after 1 day). This provides the "best-of-both" solution: short-term immutability and long-term cost savings.

### **Part 8: Conclusion and Architectural Recommendations**

A robust multi-cloud backup and DR strategy for Kubernetes is not about a single tool but about a holistic architecture that correctly balances in-cloud resilience with cross-cloud portability.

#### **8.1 Summary of Findings**

- The central challenge is the **Resilience vs. Portability** trade-off. Native CSI snapshots (EBS, Azure Disk) are fast and ideal for *resilience* (in-cloud operational recovery) but are **not portable**.17  
- Logical, file-level backups (Restic/Kopia) are required for *portability* (cross-cloud DR) but are slower and have consistency challenges if used naively.25  
- The **Snapshot Data Movement** hybrid (Strategy 3) is the superior technical solution, offering both point-in-time consistency (from a CSI snapshot) and full data portability (from a Kopia upload).16  
- A cross-cloud restore is a complex *migration* that hinges on correctly mapping StorageClasses via a Velero ConfigMap.74

#### **8.2 Final Architectural Recommendations**

1. **Adopt a Hybrid Backup Policy.** Do not choose one backup method. Implement a tiered policy:  
   - **For Operational Recovery:** Schedule **Daily CSI Snapshots** (Strategy 1). They are fast, cheap, and cover 99% of recovery needs.  
   - **For Disaster Recovery:** Schedule **Weekly Snapshot Data Movement Backups** (Strategy 3). This creates a consistent, portable, cross-cloud-ready artifact.  
2. **Mandate Secret-less Identity.** Forbid the use of static IAM keys and Service Principal secrets. Mandate the use of **IRSA (on EKS)** and **Workload Identity (on AKS)** as the baseline security posture for all backup tooling.48  
3. **Federate for "Hot" DR.** Implement the **Cross-Cloud OIDC Federation** pattern (Part 5.3). This allows the production EKS cluster to write DR backups *directly* to the Azure Blob DR target, making DR data "warm" and dramatically reducing RTO by eliminating the manual azcopy step.69  
4. **Embed Backup Logic in Applications.** Mandate that all stateful application teams *provide* their own pre.hook.backup.velero.io annotations in their application's Helm chart or Kustomize manifests.37 The backup system should *execute* policy, not *define* application-specific consistency logic.  
5. **Secure with Immutability and Air-Gaps.** Protect against ransomware by using **S3 Object Lock** or Azure Immutable Storage.62 Resolve the cost conflict by using **Cross-Account Replication** to a separate, air-gapped "archive" account with its own, separate cost-tiering lifecycle policies.  
6. **Select Tooling Based on Operational Model.**  
   - Start with **Velero** as the powerful, open-source, and flexible "toolkit."  
   - Evaluate **Kasten K10** as a commercial upgrade if the organization's needs evolve to require a multi-cluster "platform" with a UI, automated application mobility, and delegated RBAC for restores.

#### **Works cited**

1. Kubernetes backup and restore done right - Spectro Cloud, accessed on November 11, 2025, [https://www.spectrocloud.com/blog/kubernetes-backup-and-restore-done-right](https://www.spectrocloud.com/blog/kubernetes-backup-and-restore-done-right)  
2. Kubernetes Backup: In-Depth Tutorial & Best Practices - Trilio, accessed on November 11, 2025, [https://trilio.io/kubernetes-disaster-recovery/kubernetes-backup/](https://trilio.io/kubernetes-disaster-recovery/kubernetes-backup/)  
3. Chapter 6: Backups - Kubernetes Guides - Apptio, accessed on November 11, 2025, [https://www.apptio.com/topics/kubernetes/best-practices/backups/](https://www.apptio.com/topics/kubernetes/best-practices/backups/)  
4. Kubernetes Data Protection: A Guide to Backup and Protection, accessed on November 11, 2025, [https://www.backblaze.com/blog/kubernetes-data-protection-how-to-safeguard-your-containerized-applications/](https://www.backblaze.com/blog/kubernetes-data-protection-how-to-safeguard-your-containerized-applications/)  
5. Kubernetes Components, accessed on November 11, 2025, [https://kubernetes.io/docs/concepts/overview/components/](https://kubernetes.io/docs/concepts/overview/components/)  
6. Operating etcd clusters for Kubernetes | Kubernetes, accessed on November 11, 2025, [https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/)  
7. Best Practices for Backing Up Kubernetes Clusters and Persistent Storage - swissns GmbH, accessed on November 11, 2025, [https://www.swissns.ch/site/2024/08/best-practices-for-backing-up-kubernetes-clusters-and-persistent-storage/](https://www.swissns.ch/site/2024/08/best-practices-for-backing-up-kubernetes-clusters-and-persistent-storage/)  
8. Disaster recovery - etcd, accessed on November 11, 2025, [https://etcd.io/docs/v3.5/op-guide/recovery/](https://etcd.io/docs/v3.5/op-guide/recovery/)  
9. What is the Best Way to Protect your Kubernetes Cluster Against Disaster? - Veeam, accessed on November 11, 2025, [https://www.veeam.com/blog/protect-kubernetes-cluster-against-disaster.html](https://www.veeam.com/blog/protect-kubernetes-cluster-against-disaster.html)  
10. Chapter 5. Control plane backup and restore | Backup and restore | OpenShift Container Platform | 4.16 | Red Hat Documentation, accessed on November 11, 2025, [https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/backup_and_restore/control-plane-backup-and-restore](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/backup_and_restore/control-plane-backup-and-restore)  
11. Learn About Kubernetes Clusters Restore Based on etcd Snapshots - Oracle Help Center, accessed on November 11, 2025, [https://docs.oracle.com/en/solutions/kubernetes-restore-etcd-snapshot/index.html](https://docs.oracle.com/en/solutions/kubernetes-restore-etcd-snapshot/index.html)  
12. Volumes | Kubernetes, accessed on November 11, 2025, [https://kubernetes.io/docs/concepts/storage/volumes/](https://kubernetes.io/docs/concepts/storage/volumes/)  
13. Persistent Volumes - Kubernetes, accessed on November 11, 2025, [https://kubernetes.io/docs/concepts/storage/persistent-volumes/](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)  
14. Kubernetes Backup | 6 Best Practices You Need To Know - Veeam, accessed on November 11, 2025, [https://www.veeam.com/blog/kubernetes-backup-6-best-practices.html](https://www.veeam.com/blog/kubernetes-backup-6-best-practices.html)  
15. Volume Snapshots - Kubernetes, accessed on November 11, 2025, [https://kubernetes.io/docs/concepts/storage/volume-snapshots/](https://kubernetes.io/docs/concepts/storage/volume-snapshots/)  
16. How do you guys back up block storage PVs? : r/kubernetes - Reddit, accessed on November 11, 2025, [https://www.reddit.com/r/kubernetes/comments/1ffwmds/how_do_you_guys_back_up_block_storage_pvs/](https://www.reddit.com/r/kubernetes/comments/1ffwmds/how_do_you_guys_back_up_block_storage_pvs/)  
17. Migrate Kubernetes Persistent Volume Claims to AKS with Velero - Medium, accessed on November 11, 2025, [https://medium.com/microsoftazure/migrate-kubernetes-persistent-volume-claims-to-aks-with-velero-b831bdc9b171](https://medium.com/microsoftazure/migrate-kubernetes-persistent-volume-claims-to-aks-with-velero-b831bdc9b171)  
18. Container Storage Interface (CSI) for Kubernetes GA, accessed on November 11, 2025, [https://kubernetes.io/blog/2019/01/15/container-storage-interface-ga/](https://kubernetes.io/blog/2019/01/15/container-storage-interface-ga/)  
19. Storage Options for a Kubernetes Cluster - Azure Architecture Center | Microsoft Learn, accessed on November 11, 2025, [https://learn.microsoft.com/en-us/azure/architecture/aws-professional/eks-to-aks/storage](https://learn.microsoft.com/en-us/azure/architecture/aws-professional/eks-to-aks/storage)  
20. Container Storage Interface Snapshot Support in Velero, accessed on November 11, 2025, [https://velero.io/docs/v1.9/csi/](https://velero.io/docs/v1.9/csi/)  
21. Best practices for storage and backups in Azure Kubernetes Service (AKS) - Microsoft Learn, accessed on November 11, 2025, [https://learn.microsoft.com/en-us/azure/aks/operator-best-practices-storage](https://learn.microsoft.com/en-us/azure/aks/operator-best-practices-storage)  
22. Kubernetes CSI (Container Storage Interface): Complete Guide - Portworx, accessed on November 11, 2025, [https://portworx.com/knowledge-hub/a-complete-guide-to-kubernetes-csi/](https://portworx.com/knowledge-hub/a-complete-guide-to-kubernetes-csi/)  
23. Container Storage Interface (CSI) drivers on Azure Kubernetes Service (AKS), accessed on November 11, 2025, [https://learn.microsoft.com/en-us/azure/aks/csi-storage-drivers](https://learn.microsoft.com/en-us/azure/aks/csi-storage-drivers)  
24. velero incremental backup for snapshot of pv's not working - Azure · Issue #7276 - GitHub, accessed on November 11, 2025, [https://github.com/vmware-tanzu/velero/issues/7276](https://github.com/vmware-tanzu/velero/issues/7276)  
25. Kubernetes Backup using Velero - AFI.ai, accessed on November 11, 2025, [https://afi.ai/blog/kubernetes-velero-backup](https://afi.ai/blog/kubernetes-velero-backup)  
26. Use snapshot to backup Azure file with Kasten, accessed on November 11, 2025, [https://veeamkasten.dev/use-snapshot-to-backup-azure-file](https://veeamkasten.dev/use-snapshot-to-backup-azure-file)  
27. Using Kubernetes Container Storage Interface drivers - AWS Documentation, accessed on November 11, 2025, [https://docs.aws.amazon.com/filegateway/latest/files3/using-csi-drivers.html](https://docs.aws.amazon.com/filegateway/latest/files3/using-csi-drivers.html)  
28. Kubernetes and Container Portability: Navigating Multi-Cloud Flexibility | by Eyal Estrin ☁️, accessed on November 11, 2025, [https://aws.plainenglish.io/kubernetes-and-container-portability-navigating-multi-cloud-flexibility-aafcd3d7ad6e](https://aws.plainenglish.io/kubernetes-and-container-portability-navigating-multi-cloud-flexibility-aafcd3d7ad6e)  
29. Back up, restore workload clusters using Velero - AKS enabled by Azure Arc, accessed on November 11, 2025, [https://learn.microsoft.com/en-us/azure/aks/aksarc/backup-workload-cluster](https://learn.microsoft.com/en-us/azure/aks/aksarc/backup-workload-cluster)  
30. Migrate from Amazon Elastic Kubernetes Service to Azure ..., accessed on November 11, 2025, [https://learn.microsoft.com/en-us/azure/architecture/aws-professional/eks-to-aks/migrate](https://learn.microsoft.com/en-us/azure/architecture/aws-professional/eks-to-aks/migrate)  
31. Configure application consistent backups for Kubernetes - Veritas, accessed on November 11, 2025, [https://www.veritas.com/support/en_US/article.100054625](https://www.veritas.com/support/en_US/article.100054625)  
32. Dell PowerProtect Data Manager: Protecting Kubernetes Workloads, accessed on November 11, 2025, [https://www.delltechnologies.com/asset/en-hk/products/storage/industry-market/h18563-dell-powerprotect-data-manager-protecting-kubernetes-workloads-wp.pdf](https://www.delltechnologies.com/asset/en-hk/products/storage/industry-market/h18563-dell-powerprotect-data-manager-protecting-kubernetes-workloads-wp.pdf)  
33. How to backup and restore MySQL on Kubernetes - Portworx, accessed on November 11, 2025, [https://portworx.com/blog/how-to-backup-and-restore-mysql-on-kubernetes/](https://portworx.com/blog/how-to-backup-and-restore-mysql-on-kubernetes/)  
34. Configure Backup and Restore Hooks for Snapshots - Replicated Docs, accessed on November 11, 2025, [https://docs.replicated.com/vendor/snapshots-hooks](https://docs.replicated.com/vendor/snapshots-hooks)  
35. Backup Hooks - Velero Docs, accessed on November 11, 2025, [https://velero.io/docs/v1.9/backup-hooks/](https://velero.io/docs/v1.9/backup-hooks/)  
36. Kasten K10 or Velero? : r/kubernetes - Reddit, accessed on November 11, 2025, [https://www.reddit.com/r/kubernetes/comments/1deoxe8/kasten_k10_or_velero/](https://www.reddit.com/r/kubernetes/comments/1deoxe8/kasten_k10_or_velero/)  
37. Protecting Tanzu: The Right Way to Back Up Databases & PVCs, accessed on November 11, 2025, [https://cloudcasa.io/blog/protecting-tanzu-back-up-databases-and-pvcs/](https://cloudcasa.io/blog/protecting-tanzu-back-up-databases-and-pvcs/)  
38. Restore Hooks - Velero Docs, accessed on November 11, 2025, [https://velero.io/docs/main/restore-hooks/](https://velero.io/docs/main/restore-hooks/)  
39. Top 10 Kubernetes Backup and Recovery Tools for Containers, accessed on November 11, 2025, [https://container.watch/article/Top_10_Kubernetes_Backup_and_Recovery_Tools_for_Containers.html](https://container.watch/article/Top_10_Kubernetes_Backup_and_Recovery_Tools_for_Containers.html)  
40. TrilioVault vs. Veeam Kasten for Kubernetes vs. Velero Comparison - SourceForge, accessed on November 11, 2025, [https://sourceforge.net/software/compare/TrilioVault-vs-Veeam-Kasten-vs-Velero/](https://sourceforge.net/software/compare/TrilioVault-vs-Veeam-Kasten-vs-Velero/)  
41. Providers - Velero Docs, accessed on November 11, 2025, [https://velero.io/docs/v1.6/supported-providers/](https://velero.io/docs/v1.6/supported-providers/)  
42. Backup Storage Locations and Volume Snapshot Locations - Velero Docs, accessed on November 11, 2025, [https://velero.io/docs/v1.3.1/locations/](https://velero.io/docs/v1.3.1/locations/)  
43. Backup Storage Locations and Volume Snapshot Locations - Velero Docs, accessed on November 11, 2025, [https://velero.io/docs/main/locations/](https://velero.io/docs/main/locations/)  
44. Nutanix Kubernetes Platform 2.12 - Usage of Velero with AWS S3 Buckets, accessed on November 11, 2025, [https://portal.nutanix.com/page/documents/details?targetId=Nutanix-Kubernetes-Platform-v2_12:top-usage-of-velero-with-aws-c.html](https://portal.nutanix.com/page/documents/details?targetId=Nutanix-Kubernetes-Platform-v2_12:top-usage-of-velero-with-aws-c.html)  
45. Run Velero on AWS, accessed on November 11, 2025, [https://velero.io/docs/v0.11.0/aws-config/](https://velero.io/docs/v0.11.0/aws-config/)  
46. Run Velero on AWS, accessed on November 11, 2025, [https://velero.io/docs/v1.0.0/aws-config/](https://velero.io/docs/v1.0.0/aws-config/)  
47. IAM roles for service accounts - Amazon EKS - AWS Documentation, accessed on November 11, 2025, [https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html)  
48. Kubernetes Workload Identity and Access - Azure Architecture Center | Microsoft Learn, accessed on November 11, 2025, [https://learn.microsoft.com/en-us/azure/architecture/aws-professional/eks-to-aks/workload-identity](https://learn.microsoft.com/en-us/azure/architecture/aws-professional/eks-to-aks/workload-identity)  
49. Nutanix Kubernetes Platform 2.12 - Usage of Velero with Azure Blob Containers, accessed on November 11, 2025, [https://portal.nutanix.com/page/documents/details?targetId=Nutanix-Kubernetes-Platform-v2_12:top-usage-of-velero-with-azure-c.html](https://portal.nutanix.com/page/documents/details?targetId=Nutanix-Kubernetes-Platform-v2_12:top-usage-of-velero-with-azure-c.html)  
50. Run Velero on Azure - Velero Docs, accessed on November 11, 2025, [https://velero.io/docs/v1.0.0/azure-config/](https://velero.io/docs/v1.0.0/azure-config/)  
51. Setting Up Velero for AKS Backups with Azure Workload Identity | by Taylor Levits | Medium, accessed on November 11, 2025, [https://medium.com/@taylorlevits/setting-up-velero-for-aks-backups-with-azure-workload-identity-378dcc9d036e](https://medium.com/@taylorlevits/setting-up-velero-for-aks-backups-with-azure-workload-identity-378dcc9d036e)  
52. Using Velero for AKS Cross Region Disaster Recovery - Andy Roberts, accessed on November 11, 2025, [https://www.andyroberts.nz/posts/velero-aks-regional-dr/](https://www.andyroberts.nz/posts/velero-aks-regional-dr/)  
53. How can I use azure workload identity with different resource groups for snapshotter and storage · vmware-tanzu velero · Discussion #8595 - GitHub, accessed on November 11, 2025, [https://github.com/vmware-tanzu/velero/discussions/8595](https://github.com/vmware-tanzu/velero/discussions/8595)  
54. Doing fast export and restore on Azure - Veeam Kasten DevHub, accessed on November 11, 2025, [https://veeamkasten.dev/fast-export-restore-on-azure](https://veeamkasten.dev/fast-export-restore-on-azure)  
55. Kasten K10 for AKS on Azure Stack: Protection Guide - Veeam, accessed on November 11, 2025, [https://www.veeam.com/blog/kasten-k10-aks-azure-stack-protection-guide.html](https://www.veeam.com/blog/kasten-k10-aks-azure-stack-protection-guide.html)  
56. AKS Backup and Recovery - Azure Architecture Center | Microsoft Learn, accessed on November 11, 2025, [https://learn.microsoft.com/en-us/azure/architecture/operator-guides/aks/aks-backup-and-recovery](https://learn.microsoft.com/en-us/azure/architecture/operator-guides/aks/aks-backup-and-recovery)  
57. Minimum Backup Retention - Kyverno, accessed on November 11, 2025, [https://release-1-9-0.kyverno.io/policies/kasten/k10-minimum-retention/k10-override-minimum-retentions/](https://release-1-9-0.kyverno.io/policies/kasten/k10-minimum-retention/k10-override-minimum-retentions/)  
58. Kasten K10 for Backup & Restoring Kubernetes Cluster | by Nilesh Gadgi | CloudDrove, accessed on November 11, 2025, [https://blog.clouddrove.com/kasten-k10-for-backup-restoring-kubernetes-cluster-57af01deb4bd](https://blog.clouddrove.com/kasten-k10-for-backup-restoring-kubernetes-cluster-57af01deb4bd)  
59. How to backup / snapshot and restore full EKS cluster(s)? : r/kubernetes - Reddit, accessed on November 11, 2025, [https://www.reddit.com/r/kubernetes/comments/11ooiua/how_to_backup_snapshot_and_restore_full_eks/](https://www.reddit.com/r/kubernetes/comments/11ooiua/how_to_backup_snapshot_and_restore_full_eks/)  
60. Velero : Multi-Cloud K8 Cluster Backup and Restore | by Nikhil ..., accessed on November 11, 2025, [https://medium.com/@nikhil.pandit/velero-multi-cloud-k8-cluster-backup-and-restore-9b30ed1886d9](https://medium.com/@nikhil.pandit/velero-multi-cloud-k8-cluster-backup-and-restore-9b30ed1886d9)  
61. Restoring Applications — K10 4.5.1 documentation, accessed on November 11, 2025, [https://docs.kasten.io/4.5.1/usage/restore.html](https://docs.kasten.io/4.5.1/usage/restore.html)  
62. Part1: Kubernetes Backup Strategies: Balancing Cost, Security, and Availability, accessed on November 11, 2025, [https://dev.to/hstiwana/kubernetes-backup-strategies-balancing-cost-security-and-availability-3jpd](https://dev.to/hstiwana/kubernetes-backup-strategies-balancing-cost-security-and-availability-3jpd)  
63. Kubernetes Data Protection Best Practices - Trilio, accessed on November 11, 2025, [https://trilio.io/kubernetes-disaster-recovery/kubernetes-data-protection/](https://trilio.io/kubernetes-disaster-recovery/kubernetes-data-protection/)  
64. Good practices for Kubernetes Secrets, accessed on November 11, 2025, [https://kubernetes.io/docs/concepts/security/secrets-good-practices/](https://kubernetes.io/docs/concepts/security/secrets-good-practices/)  
65. Encrypting Confidential Data at Rest - Kubernetes, accessed on November 11, 2025, [https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/)  
66. Backup Reference - Velero Docs, accessed on November 11, 2025, [https://velero.io/docs/v1.11/backup-reference/](https://velero.io/docs/v1.11/backup-reference/)  
67. Run Velero on Azure, accessed on November 11, 2025, [https://velero.io/docs/v1.1.0/azure-config/](https://velero.io/docs/v1.1.0/azure-config/)  
68. An introduction to cross-cloud access in managed Kubernetes clusters | Nearform, accessed on November 11, 2025, [https://nearform.com/digital-community/an-introduction-to-cross-cloud-access-in-managed-kubernetes-clusters/](https://nearform.com/digital-community/an-introduction-to-cross-cloud-access-in-managed-kubernetes-clusters/)  
69. How to Authenticate to Azure from AWS EKS Using OIDC Federation - Medium, accessed on November 11, 2025, [https://medium.com/@rbjoergensen/how-to-authenticate-to-azure-from-aws-eks-using-oidc-federation-cb2bbf4ea163](https://medium.com/@rbjoergensen/how-to-authenticate-to-azure-from-aws-eks-using-oidc-federation-cb2bbf4ea163)  
70. Modern authentication with Azure workload identity federation | TO THE NEW Blog, accessed on November 11, 2025, [https://www.tothenew.com/blog/modern-authentication-with-azure-workload-identity-federation/](https://www.tothenew.com/blog/modern-authentication-with-azure-workload-identity-federation/)  
71. Using Azure Active Directory to authenticate to Amazon EKS | Containers, accessed on November 11, 2025, [https://aws.amazon.com/blogs/containers/using-azure-active-directory-to-authenticate-to-amazon-eks/](https://aws.amazon.com/blogs/containers/using-azure-active-directory-to-authenticate-to-amazon-eks/)  
72. How to federate into AWS from Azure DevOps using OpenID Connect, accessed on November 11, 2025, [https://aws.amazon.com/blogs/modernizing-with-aws/how-to-federate-into-aws-from-azure-devops-using-openid-connect/](https://aws.amazon.com/blogs/modernizing-with-aws/how-to-federate-into-aws-from-azure-devops-using-openid-connect/)  
73. Compare Storage Services on Azure and AWS - Azure Architecture Center | Microsoft Learn, accessed on November 11, 2025, [https://learn.microsoft.com/en-us/azure/architecture/aws-professional/storage](https://learn.microsoft.com/en-us/azure/architecture/aws-professional/storage)  
74. Restore Reference - Velero Docs, accessed on November 11, 2025, [https://velero.io/docs/main/restore-reference/](https://velero.io/docs/main/restore-reference/)  
75. Velero for Kubernetes Backup and Restore | by Suraj Solanki - Medium, accessed on November 11, 2025, [https://surajblog.medium.com/velero-for-kubernetes-backup-and-restore-10fba3a5efa4](https://surajblog.medium.com/velero-for-kubernetes-backup-and-restore-10fba3a5efa4)  
76. Migrate your Azure Kubernetes Service Cluster or Amazon EKS Cluster to Container Engine for Kubernetes using Velero - Oracle Help Center, accessed on November 11, 2025, [https://docs.oracle.com/en/learn/aks-eks-to-oke-migration-velero/index.html](https://docs.oracle.com/en/learn/aks-eks-to-oke-migration-velero/index.html)  
77. Kubernetes Disaster Recovery: 6 Best Practices - Veeam, accessed on November 11, 2025, [https://www.veeam.com/blog/kubernetes-disaster-recovery-6-best-practices.html](https://www.veeam.com/blog/kubernetes-disaster-recovery-6-best-practices.html)  
78. Grandfather-Father-Son Backup Explained - Trilio, accessed on November 11, 2025, [https://trilio.io/resources/grandfather-father-son-backup/](https://trilio.io/resources/grandfather-father-son-backup/)  
79. What is GFS Backup Retention Policy?, accessed on November 11, 2025, [https://www.vinchin.com/disaster-recovery/gfs-backup-retention-policy.html](https://www.vinchin.com/disaster-recovery/gfs-backup-retention-policy.html)  
80. Kubernetes - Veeam Backup & Replication User Guide, accessed on November 11, 2025, [https://helpcenter.veeam.com/docs/vbr/userguide/kubernetes.html](https://helpcenter.veeam.com/docs/vbr/userguide/kubernetes.html)  
81. AWS: Ways of keeping cost down while backing up S3 files to Glacier? - Stack Overflow, accessed on November 11, 2025, [https://stackoverflow.com/questions/15231733/aws-ways-of-keeping-cost-down-while-backing-up-s3-files-to-glacier](https://stackoverflow.com/questions/15231733/aws-ways-of-keeping-cost-down-while-backing-up-s3-files-to-glacier)  
82. AWS Glacier vs Azure Archive: Which Cold Storage Wins? - Wildnet Edge, accessed on November 11, 2025, [https://www.wildnetedge.com/blogs/aws-glacier-vs-azure-archive](https://www.wildnetedge.com/blogs/aws-glacier-vs-azure-archive)  
83. Cloud Backup Cost Optimization Strategies | Veeam, accessed on November 11, 2025, [https://www.veeam.com/blog/controlling-cloud-backup-costs.html](https://www.veeam.com/blog/controlling-cloud-backup-costs.html)
