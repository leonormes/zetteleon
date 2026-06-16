---
created: 2026-05-02T19:37:55+00:00
modified: 2026-06-08T11:49:21+00:00
project_category: refined_deployment
project_name: Refined Deployment
project_status: active
title: Kubernetes Storage Fundamentals
type:
---

## Kubernetes Storage Fundamentals

To understand the solution, we first need to grasp the core components of Kubernetes storage:

- PersistentVolumes (PVs): A PV is a piece of storage in the cluster that has been provisioned by an administrator or dynamically provisioned using StorageClasses. It's a resource in the cluster, just like a node is a cluster resource. PVs are volume1 plugins like EBS or Azure Disk, but have a lifecycle independent of any individual pod that uses the PV.2 This API object captures the details of the implementation of the storage, be that NFS, iSCSI, or a cloud-provider-specific3 storage system.4
- PersistentVolumeClaims (PVCs): A PVC is a request for storage by a user.5 It's similar to a Pod. Pods consume node resources; PVCs consume PV resources.6 Pods can request specific levels of resources (CPU and Memory).7 Claims can request8 specific size and access modes (e.g., ReadWriteOnce, ReadOnlyMany,9 or ReadWriteMany).10
- StorageClasses: A StorageClass provides a way for administrators to describe the "classes" of storage they offer.11 Different classes might map to quality-of-service levels,12 backup policies, or arbitrary policies determined by the cluster administrators. Kubernetes13 itself is unopinionated about what classes represent. This concept is sometimes called "profiles" in other storage systems.
  - Each StorageClass contains the fields' provisioner, parameters, and reclaimPolicy, which are used when a14 PersistentVolume belonging to the class needs to be dynamically provisioned.1516
  - The reclaimPolicy in the StorageClass is applied to PVs dynamically provisioned _by_ that StorageClass.
- Dynamic Provisioning: When none of the static PVs the administrator created match a user's PersistentVolumeClaim, the cluster may try to dynamically provision a17 volume specially for that PVC. This provisioning is based on StorageClasses: the PVC must request a StorageClass, and the administrator must have created and configured that class for dynamic provisioning to occur.18 The claim will remain unbound indefinitely if a StorageClass is specified and no PV matches, and no dynamic provisioner can service it.
- Lifecycle of PVs and PVCs:
  1. Provisioning: Storage is provisioned, either statically by an admin or dynamically via a StorageClass.19
  2. Binding: A PVC requests storage with specific requirements (size, access modes). The control plane searches for a matching PV (or provisions one dynamically) and binds the PVC to that PV.20
  3. Using: Pods can use the PVC as a volume. Once bound, the PV belongs to that specific PVC as long as the PVC exists.
  4. Reclaiming: When a user is finished with their volume, they can delete the PVC object from the API.21 The reclaimPolicy of the PV dictates what happens to the PV and the underlying storage after the PVC is deleted.22

## ---

Deep Dive into reclaimPolicy

The persistentVolumeReclaimPolicy field of a PersistentVolume tells the cluster what to do with the volume after its PersistentVolumeClaim has been deleted.

- Delete:
  - When the PVC is deleted, the PersistentVolume object is deleted from Kubernetes, and the associated storage asset in the external infrastructure (like an AWS EBS volume, Azure Disk, or GCE PD) is also deleted.23
  - This was the behaviour in your scenario: ArgoCD deleted the application, which deleted the associated PVCs. Because their PVs had a reclaimPolicy of Delete (often the default for dynamically provisioned volumes from StorageClasses unless specified otherwise), the cloud provider's Kubernetes integration (the cloud controller manager or CSI driver) proceeded to delete the underlying EBS volumes. This resulted in permanent data loss.
- Retain:
  - When the PVC is deleted, the PersistentVolume object is _not_ deleted. Instead, it is moved to the 'Released' phase. The underlying storage asset (e.g., EBS volume, Azure Disk) is _not_ deleted by Kubernetes.
  - This policy allows for manual recovery of the data. The data on the volume is presumed to still be intact.
  - A 'Released' PV is not immediately available for another claim because its claimRef field still holds a reference to the previous (now deleted) PVC.24 To reuse this PV:
    1. An administrator must manually clear the spec.claimRef from the PV object. This can be done using kubectl patch pv \<pv-name\> \--type json \-p='\[{"op": "remove", "path": "/spec/claimRef"}\]'.
    2. Once the claimRef is removed, the PV's status changes from 'Released' to 'Available'.
    3. A new PVC can then bind to this 'Available' PV, either by matching its requirements or by explicitly specifying the PV's name in its spec.volumeName field.25
- Recycle:
  - If supported by the underlying volume plugin, Recycle performs a basic scrub (rm \-rf /thevolume/\*) on the volume and makes it available again for a new claim.
  - Note: The Recycle reclaim policy is deprecated. Instead, the recommended approach is to use dynamic provisioning. Most modern cloud provider CSI drivers do not support Recycle. You should avoid using it.

In your scenario, if the reclaimPolicy had been Retain, deleting the ArgoCD application (and its PVCs) would have left the PV objects in a 'Released' state and, crucially, the underlying AWS EBS volumes intact with their data.

## ---

Recommended Solution & Best Practices

Yes, changing the reclaimPolicy to Retain for PVs storing your critical application data is the correct approach to meet your goal of preventing data loss when an ArgoCD application is temporarily deleted and then recreated.

### Implementing reclaimPolicy: Retain

There are two main ways to ensure PVs have the Retain policy:

1. At the StorageClass Level (Recommended for New PVs):
   - Modify your existing StorageClass definitions or create new ones to include reclaimPolicy: Retain.
     YAML
     apiVersion: storage.k8s.io/v1
     kind: StorageClass
     metadata:
       name: my-retainable-storage
     provisioner: kubernetes.io/aws-ebs \# or ebs.csi.aws.com for AWS EBS CSI driver
                                       \# or kubernetes.io/azure-disk / disk.csi.azure.com for Azure
     parameters:
       type: gp3 \# Example for AWS EBS
       \# Other parameters like fsType, iops, throughput for AWS
       \# or skuName, cachingMode for Azure
     reclaimPolicy: Retain
     allowVolumeExpansion: true
     mountOptions:
       \- debug

   - Pros:
     - Enforces the desired policy automatically for all new PVs created using this StorageClass.
     - Centralised management and good for standardisation across applications.
     - Reduces manual intervention for new deployments.
   - Cons:
     - Less flexible if certain applications _should_ have their storage deleted with them (though this is usually managed by other means like backup/restore rather than relying on Delete for temporary cleanups).
     - Requires all new PVCs intended for persistent data to use this specific StorageClass.
2. On Individual (Existing) PVs:
   - For PVs that have already been provisioned, you can patch their reclaimPolicy.
   - Steps:
     1. Identify the PV: kubectl get pv
     2. Patch the PV:
        Bash
        kubectl patch pv \<your-pv-name\> \-p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'

   - Pros:
     - Allows granular control over existing volumes.
     - Can be done without downtime for the application (as long as the PVC is not deleted).
   - Cons:
     - Manual process, prone to error if not scripted or managed carefully for many PVs.
     - Doesn't affect new PVs unless the StorageClass is also updated.
   - Considerations and Risks:
     - The primary risk is timing. If a PVC is deleted _before_ its PV's reclaimPolicy is changed to Retain (and the old policy was Delete), the data will still be lost.
     - Ensure you have correctly identified the PVs associated with your application data.
     - For operational overhead, this can be scripted for bulk updates. Test the script in a non-production environment first.

### Changing reclaimPolicy for New PVs

1. Define or update your StorageClass to include reclaimPolicy: Retain.
2. Ensure your application's PVCs specify this StorageClass (or it's the default StorageClass).
3. When a PVC is created using this StorageClass, the dynamically provisioned PV will automatically inherit reclaimPolicy: Retain.

### Considerations for Existing PVs/PVCs

Changing the reclaimPolicy on an existing, bound PV from Delete to Retain is generally safe and straightforward using kubectl patch.26 The application using the PV can continue running. The change becomes effective when the PVC is eventually deleted.

The steps are:

1. Identify all relevant PVs.
2. For each PV, run: kubectl patch pv \<pv-name\> \-p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
3. Verify the change: kubectl get pv \<pv-name\> \-o yaml and check spec.persistentVolumeReclaimPolicy.

There's minimal operational overhead if scripted, but careful identification and execution are key. The main risk is human error in targeting the wrong PVs or mismanaging the patching process.

### Re-binding to 'Released' PVs After Application Re-creation

When your ArgoCD application is deleted, its PVCs are deleted. The associated PVs (now with reclaimPolicy: Retain) will transition to the 'Released' state. When ArgoCD recreates the application 5 minutes later, it will create new PVCs. For these new PVCs to use the existing data on the 'Released' PVs:

1. PV State: The PV is 'Released'. The underlying storage (e.g., EBS volume) still exists with data.
2. Manual Intervention (Default Kubernetes Behaviour): The 'Released' PV's spec.claimRef (which references the old, deleted PVC) must be removed to make the PV 'Available' again.27
   Bash
   kubectl patch pv \<your-pv-name\> \--type json \-p='\[{"op": "remove", "path": "/spec/claimRef"}\]'

3. PVC Re-binding:
   - Once the PV is 'Available', the newly created PVC (if it has the same name, namespace, and requests compatible storage size and access modes as the original) might automatically bind to this PV.
   - A more deterministic way is for the new PVC to explicitly request the PV by setting spec.volumeName: \<your-pv-name\> in its manifest. ArgoCD would need to manage this PVC definition.

This manual step of clearing claimRef can be a bottleneck if you need rapid re-creation. You might consider:

- A small operational script to run between ArgoCD deletion and re-creation.
- A custom Kubernetes controller/operator that watches for 'Released' PVs (perhaps with specific annotations/labels indicating they are for ArgoCD-managed apps) and automatically clears their claimRef to make them 'Available'. This is a more advanced solution.

### GitOps (ArgoCD) Specific Considerations

- StorageClass in Git: Define your StorageClasses (with reclaimPolicy: Retain) in Git and manage them via ArgoCD or another GitOps process. This ensures consistency.
- PVC Manifests: Ensure your ArgoCD application manifests define PVCs that use these StorageClasses.
- Application Deletion and Recreation:
  - When ArgoCD deletes an application, it will delete the PVCs.
  - With reclaimPolicy: Retain, PVs become 'Released'.
  - When ArgoCD recreates the application, it will create new PVCs.
  - You need a process (manual, scripted, or automated via a custom controller) to handle the 'Released' PVs (clear claimRef) so the new PVCs can bind to them.
  - If PVCs are named consistently and volumeName is not used in the PVC spec, after clearing claimRef, the new PVC (with the same name, namespace, size, access modes) should bind to the now 'Available' PV.
- Avoid Cascading Deletion of PVs: The Retain policy is key. Also, ensure ArgoCD's synchronisation settings or pruning logic for the application doesn't inadvertently try to delete PVs if they are managed outside the Application manifest scope (PVs are cluster-scoped, not namespaced like PVCs). Typically, ArgoCD manages namespaced resources defined in its Application scope.

## ---

Cloud-Specific Implementation (AWS & Azure)

Setting reclaimPolicy: Retain is done within the StorageClass definition, which is cloud-agnostic at the Kubernetes API level. The provisioner and parameters fields in the StorageClass handle the cloud-specific parts.

- AWS (e.g., using EBS):
  - StorageClass Example (EBS CSI Driver):
    YAML
    apiVersion: storage.k8s.io/v1
    kind: StorageClass
    metadata:
      name: aws-ebs-retained
    provisioner: ebs.csi.aws.com \# AWS EBS CSI driver
    volumeBindingMode: WaitForFirstConsumer
    reclaimPolicy: Retain
    allowVolumeExpansion: true
    parameters:
      type: gp3 \# Or io1, io2, etc.
      fsType: ext4
      \# encrypted: "true" \# Optionally encrypt
    \# kmsKeyId: "arn:aws:kms:REGION:ACCOUNT\_ID:key/KMS\_KEY\_ID" \# If using a specific KMS key

  - Behaviour: When a PVC using this class is deleted, the PV becomes 'Released'. The underlying EBS volume in your AWS account will not be deleted. You will continue to be billed for it. You are responsible for managing these retained EBS volumes (e.g., deleting them when no longer needed or re-attaching them).
- Azure (e.g., using Azure Disk):
  - StorageClass Example (Azure Disk CSI Driver):
    YAML
    apiVersion: storage.k8s.io/v1
    kind: StorageClass
    metadata:
      name: azure-disk-retained
    provisioner: disk.csi.azure.com \# Azure Disk CSI driver
    volumeBindingMode: WaitForFirstConsumer
    reclaimPolicy: Retain
    allowVolumeExpansion: true
    parameters:
      skuName: Premium\_LRS \# Or Standard\_LRS, StandardSSD\_LRS, UltraSSD\_LRS etc.
      cachingMode: ReadOnly \# Or None, ReadWrite
      \# kind: Managed (default) or Shared

  - Behaviour: Similar to AWS, when a PVC using this class is deleted, the PV becomes 'Released'. The underlying Azure Managed Disk in your Azure subscription will not be deleted. You will continue to be billed for it and are responsible for its lifecycle management.

Key Cloud Provider Consideration: The Retain policy means Kubernetes steps back from deleting the actual storage medium.28 This is good for data safety but introduces a manual (or automated via external tooling) clean-up responsibility for these "orphaned" cloud resources to avoid unnecessary costs and clutter.

## ---

Ensuring Data Integrity and Recoverability (Beyond reclaimPolicy)

While reclaimPolicy: Retain protects against accidental deletion via PVC removal, consider these additional measures for comprehensive data integrity and recoverability:

- Volume Snapshots:
  - Use the Kubernetes VolumeSnapshot API (requires a CSI driver that supports snapshots, like ebs.csi.aws.com or disk.csi.azure.com).29
  - Snapshots create point-in-time copies of your PV data, stored independently (e.g., as EBS Snapshots in AWS, or Azure Disk Snapshots).30
  - Crucial for recovering from data corruption, user error within the volume, or disaster recovery.
- Backup Solutions:
  - Employ tools like Velero (formerly Heptio Ark).31 Velero can back up your Kubernetes cluster resources (including PVs, PVCs, and other configurations) and, importantly, can also trigger volume snapshots of your PV data and store them in a separate object storage location (like S3 or Azure Blob Storage).32
  - This is excellent for full cluster or application state backup and restore.
- Application-Level Replication:
  - For stateful applications like databases (e.g., PostgreSQL, MySQL, MongoDB) or distributed systems (e.g., Elasticsearch, Kafka), utilise their native data replication features. This provides high availability and can protect against certain types of failures.
- Monitoring and Alerting:
  - Monitor PV usage, PVC status, available storage capacity, and snapshot creation success/failure.
  - Set up alerts for PVs in 'Released' state for extended periods to prompt clean-up or investigation.
- Regularly Test Recovery Procedures:
  - Practice restoring data from snapshots or backups to ensure your recovery processes work as expected. Don't wait for a disaster to test them.
- Immutable Infrastructure Principles (where applicable):
  - While data volumes are inherently stateful, the application workloads themselves can often be designed to be immutable. This simplifies rollbacks and updates.
- Change Management and Deletion Safeguards:
  - Implement stricter change management processes for deleting applications that use persistent storage.
  - Use Kubernetes Role-Based Access Control (RBAC) to limit who can delete PVCs or PVs.
  - Consider admission controllers or policies (e.g., using OPA Gatekeeper or Kyverno) to prevent deletion of critical PVCs without specific annotations or approvals.

---

By changing your reclaimPolicy to Retain (preferably at the StorageClass level for future PVs and by patching existing PVs), you will achieve your immediate goal of preventing data loss when an ArgoCD application is deleted and quickly recreated. Remember to address the manual step of clearing claimRef on 'Released' PVs to make them available for new PVCs. Complement this with robust backup and snapshot strategies for overall data resilience.

Sources

1\. [https://www.pulumi.com/ai/answers/dc46b3d3-b965-4c5e-86c5-07b50fb843fe](https://www.pulumi.com/ai/answers/dc46b3d3-b965-4c5e-86c5-07b50fb843fe)

2\. [https://www.javaadvent.com/2021/12/different-approaches-to-building-stateful-microservices-in-the-cloud-native-world.html](https://www.javaadvent.com/2021/12/different-approaches-to-building-stateful-microservices-in-the-cloud-native-world.html)

3\. [https://aws.github.io/aws-eks-best-practices/windows/docs/storage/](https://aws.github.io/aws-eks-best-practices/windows/docs/storage/)

4\. [https://vox.veritas.com/t5/Protection/Veritas-NetBackup-Kubernetes-protection-Architecture/ba-p/891528](https://vox.veritas.com/t5/Protection/Veritas-NetBackup-Kubernetes-protection-Architecture/ba-p/891528)

5\. [https://blog.codefarm.me/2024/02/29/kubernetes-volumes/](https://blog.codefarm.me/2024/02/29/kubernetes-volumes/)

6\. [https://docs.openshift.com/dedicated/storage/index.html](https://docs.openshift.com/dedicated/storage/index.html)

7\. [https://ny55.blogspot.com/2020/07/kubernetes-interview-questions.html](https://ny55.blogspot.com/2020/07/kubernetes-interview-questions.html)

8\. [http://kuber.tech-notes.net/pages/Kubernetes\_overview/2020-01-27-kubernetes-volumes.html](http://kuber.tech-notes.net/pages/Kubernetes_overview/2020-01-27-kubernetes-volumes.html)

9\. [https://kubernetes.io/docs/concepts/\_print/](https://kubernetes.io/docs/concepts/_print/)

Here's a comprehensive, actionable guide to Kubernetes storage, focusing on PersistentVolumes (PVs), PersistentVolumeClaims (PVCs), StorageClasses, and especially the reclaimPolicy attribute, with best practices for preventing data loss in GitOps environments like ArgoCD. This includes cloud-specific notes for AWS and Azure.

### Kubernetes Storage Overview

Kubernetes abstracts storage using PersistentVolumes (PVs) and PersistentVolumeClaims (PVCs). A PV is a cluster resource representing a piece of storage in the cluster, provisioned either statically (by an admin) or dynamically (via a StorageClass). A PVC is a user's request for storage, specifying size, access mode, and optionally a StorageClass. Kubernetes binds a PVC to a suitable PV, and the pod uses the PVC as a volume mount. The lifecycle of a PV is independent of the pod, but the PVC's lifecycle is tied to the application's needs.

Dynamic provisioning is the most common approach: when a PVC requests storage with a StorageClass, Kubernetes automatically provisions a PV using the underlying cloud provider (e.g., AWS EBS, Azure Disk) and binds it to the PVC. The StorageClass defines parameters for the storage backend and sets the default reclaimPolicy, which is usually Delete for cloud volumes. See [Kubernetes docs](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) and [Kubermatic blog](https://www.kubermatic.com/blog/keeping-the-state-of-apps-4-persistentvolumes-and-persistentvolum/) for more.

### Deep Dive: reclaimPolicy (Delete, Retain, Recycle)

The reclaimPolicy on a PV determines what happens to the underlying storage when the PVC is deleted:

- Delete: The default for dynamically provisioned volumes. When the PVC is deleted, Kubernetes deletes the PV and the underlying storage resource (e.g., AWS EBS volume, Azure Disk). This is what caused your data loss: when the ArgoCD application (and thus its PVCs) was deleted, the cloud provider deleted the storage before the app could be redeployed.
- Retain: When the PVC is deleted, the PV is not deleted. Instead, it enters the Released phase. The underlying storage is preserved, but the PV is not available for new claims until it is manually cleaned up and reset by an admin. This prevents accidental data loss, as the data remains intact even if the application is deleted and recreated.
- Recycle: Deprecated. The PV is scrubbed (basic data wipe) and made available for new claims. Not recommended for production.

See [Kubernetes docs](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#reclaiming) and [SimplyBlock best practices](https://www.simplyblock.io/blog/kubernetes-persistent-volumes-how-to-best-practices/) for more.

#### What Happens with Retain?

When a PVC is deleted and the PV's reclaimPolicy is Retain, the PV moves to the Released phase. The data is preserved, but the PV is not automatically available for new claims. An admin must manually intervene to make the PV available again (e.g., by removing the claimRef and possibly cleaning up data if reusing the volume). This is ideal for critical data, as it prevents automatic deletion and gives you a chance to recover or rebind the volume.

### Recommended Solution & Best Practices

#### Is Retain the Best Approach?

Yes, for application data that must persist across accidental deletions or redeployments, setting reclaimPolicy: Retain is the best practice. This ensures that deleting a PVC (e.g., via ArgoCD app deletion) does not delete the underlying storage, preventing data loss.

#### Where to Set reclaimPolicy: StorageClass vs. Individual PVs

- StorageClass: Set reclaimPolicy: Retain in the StorageClass definition. All dynamically provisioned PVs using this StorageClass will inherit the policy. This is the recommended approach for consistency and automation.
- Individual PVs: You can manually set or change the reclaimPolicy on specific PVs, but this is operationally intensive and error-prone at scale.

Pros of StorageClass-level setting: Consistency, automation, less risk of human error, and easier management for new volumes.

Cons: All PVs using that StorageClass will have the same policy, which may not be desired for all workloads.

#### Changing reclaimPolicy for New PVs

Edit your StorageClass YAML to set reclaimPolicy: Retain:

 apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: my-retain-storageclass

provisioner: kubernetes.io/aws-ebs \# or disk.csi.azure.com for Azure

reclaimPolicy: Retain

parameters:

  type: gp3 \# AWS example

1. Update your PVCs to use this StorageClass.

#### Changing reclaimPolicy for Existing PVs

You can patch the reclaimPolicy of an existing PV:

 kubectl patch pv \<pv-name\> \-p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'

- Considerations: Changing the policy is immediate, but if the PVC is already deleted and the PV is in Released or Failed state, you may need to manually recover or rebind the PV. There is some operational overhead, especially if you have many PVs.
- Risks: If you forget to set Retain, data loss can occur. If you set Retain but do not have a process for cleaning up old PVs, you may accumulate unused volumes and incur cloud costs.

#### Best Practices for GitOps/ArgoCD Environments

- Always use Retain for application data that must survive app deletion.
- Document and automate the process for recovering and reusing Retain PVs (e.g., manual intervention to rebind PVs to new PVCs).
- Consider using finalizers or protection mechanisms to prevent accidental deletion of critical PVCs.
- Use volume snapshots (if supported by your cloud provider) for additional backup and recovery.

### Cloud-Specific Implementation

#### AWS (EBS)

Set reclaimPolicy: Retain in your StorageClass for EBS:

 apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: ebs-retain

provisioner: ebs.csi.aws.com

reclaimPolicy: Retain

parameters:

  type: gp3

- When a PVC is deleted, the EBS volume is not deleted. You can manually reattach it or rebind it to a new PVC.

#### Azure (Azure Disk)

Set reclaimPolicy: Retain in your StorageClass for Azure Disk:

 apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: azure-retain

provisioner: disk.csi.azure.com

reclaimPolicy: Retain

parameters:

  skuName: Standard\_LRS

- The Azure Disk is preserved after PVC deletion. Manual intervention is required to reuse or clean up the disk.

Cloud-specific notes: Both AWS and Azure support Retain, but you must manage orphaned disks to avoid unnecessary costs. Some cloud providers may have additional features (e.g., volume snapshots, backup integration) that you should leverage for critical data.

### Ensuring Data Integrity: Additional Practices

- Volume Snapshots: Use Kubernetes VolumeSnapshot resources (if supported by your CSI driver/cloud provider) to take regular backups of your data.
- Finalizers: Use PVC finalizers to prevent accidental deletion until certain conditions are met.
- Access Controls: Use RBAC to restrict who can delete PVCs or PVs.
- Monitoring: Set up monitoring/alerting for PV/PVC events and orphaned resources.
- Disaster Recovery: Document and test your recovery procedures, including how to rebind a Retain PV to a new PVC.

### Summary: Actionable Steps

1. Update StorageClasses: Set reclaimPolicy: Retain for StorageClasses used by critical application data.
2. Patch Existing PVs: For existing PVs, patch the reclaimPolicy to Retain as needed.
3. Update PVCs: Ensure PVCs for critical data use the correct StorageClass.
4. Document Recovery: Document the process for recovering and reusing Retain PVs.
5. Monitor and Clean Up: Regularly monitor for orphaned PVs and clean up as appropriate.
6. Leverage Snapshots: Use volume snapshots for additional data protection.
7. Restrict Deletion: Use RBAC and finalizers to prevent accidental deletion of critical PVCs.

References:

- [Kubernetes Persistent Volumes Official Docs](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Kubermatic: PersistentVolumes and PersistentVolumeClaims](https://www.kubermatic.com/blog/keeping-the-state-of-apps-4-persistentvolumes-and-persistentvolum/)
- [SimplyBlock: Kubernetes Persistent Volumes Best Practices](https://www.simplyblock.io/blog/kubernetes-persistent-volumes-how-to-best-practices/)
