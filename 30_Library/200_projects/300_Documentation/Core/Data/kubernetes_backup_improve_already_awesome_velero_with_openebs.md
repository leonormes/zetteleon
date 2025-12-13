---
aliases: []
confidence: 
created: 2025-02-07T12:57:56Z
epistemic: 
id: kubernetes_backup_improve_already_awesome_velero_with_openebs
last_reviewed: 
modified: 2025-12-13T11:39:45Z
purpose: 
review_interval: 
see_also: []
source: https://blog.mayadata.io/openebs/suggesting-ways-to-improve-already-awesome-velero
source_of_truth: []
status: 
tags: []
title: kubernetes_backup_improve_already_awesome_velero_with_openebs
type:
uid: 
updated: 
version:
---

## Kubernetes Backup Improve Already Awesome Velero with OpenEBS

I'm an engineer at MayaData, a company dedicated to enabling data agility through the use of Kubernetes as a data layer and the sponsor of the CNCF project [OpenEBS](https://openebs.io/) and other open source projects. Take it for a test drive via free and easy to use management software by registering [here](https://account.mayadata.io/signup).

Velero is an open source tool for a reliable back up, recovery, and migration of Kubernetes clusters and persistent volumes that have become popular in the OpenEBS community and more broadly in the Kubernetes community. Velero works both on premises and in a public cloud.

In this blog, I will describe what we have learned about Velero in the course of building a couple of solutions that work with Velero, including the future improvements in Velero I see as the most important.

A quick note about OpenEBS - the addition of a container attached storage (CAS) to your environment means the complete application stack, top to bottom, is running on Kubernetes itself and your workloads are still loosely coupled. No more wondering whether your underlying shared storage system meets your needs - and no more meetings debating whether you are going to use storage system A or cloud storage B. We see users picking OpenEBS to abstract away underlying differences between for example local disk, cloud volumes and existing storage systems - and also because the users want to remain in control and not to rely on some other storage admin or storage service. OpenEBS is now a CNCF project, so we are incredibly open to third-party contributors and are independently governed even though most contributors, including myself today work for MayaData.

Velero

Velero consists of a server process running as a deployment in your Kubernetes cluster and a command-line interface (CLI) with which DevOps teams and platform operators configure scheduled backups, trigger ad-hoc backups, perform restores, and more. Velero seamlessly integrates OpenEBS storage via a plug-in that puts the complete solution stack, top to bottom, under DevOps management.

### What Makes Velero Unique

Unlike other tools that directly access the Kubernetes etcd database to perform backups and restores, Velero uses the Kubernetes API to capture the state of cluster resources and to restore them when necessary. This API-driven approach has several key benefits:

- Backups can capture subsets of the cluster’s resources, filtering by namespace, resource type, and/or label selector, providing a high degree of flexibility around what’s backed up and restored.
- Users of managed Kubernetes offerings often do not have access to the underlying etcd database, so direct backups/restores of it are not possible.
- Resources exposed through aggregated API servers can easily be backed up and restored even if they’re stored in a separate etcd database.

Additionally, Velero enables you to backup and restore your applications’ persistent data alongside Kubernetes cluster configurations.

There are three ways in which you can backup data using Velero:

- File-based backup using a free, open-source backup tool called
- Snapshots of persistent volumes using one of the supported cloud providers’ block storage offerings (Amazon EBS Volumes, Azure Managed Disks, Google Persistent Disks).
- Plugin model that enables anyone to implement additional object and block storage backends, outside the central Velero repository. The OpenEBS cStor Plugin

### Separate API to Upload Snapshot Files

Backing up volumes using the snapshot providers consists of two main steps: Snapshot the data + Upload the data to wherever you would like to store the volume snapshot. IO operations to the volumes are stopped before starting this process and released after upload of the snapshot files. If the data in the volume is enormous, the upload process can take a considerable amount of time, and this means there will be downtime for the workload. We believe that this problem can be solved by providing a separate API to upload the snapshot files by Velero.

Here is the link of the proposal PR that would implement this improvement:

### Directory-based Restic Backups

Restic inherently is a file-based backup. Currently, Velero is using Restic to backup Kubernetes volumes by taking the backup of all the files which are present in /var/lib/kubelet/pods/\<podUID\>/volumes/ or /opt/rke/var/lib/kubelet/pods in case of RancherOS or /var/lib/kubelet/pods/\<podUID\>/volumes/mount in case of CSI volumes path.

In the OpenEBS community we often hear from users that they would like to backup only a particular directory only from the above path mentioned, and to have only that directory data restored or migrated with the associated Kubernetes volume. This support can help to execute a lot of backup use cases, one of which is app-consistent backups, which is triggered on a per workload basis:

App Consistent backups

There are two main categories of backup: Physical backups and Logical backups. Physical backup copies all the physical files that belong to the database (like data files, control files, log files, executables, etc.). By comparison, a logical backup only extracts the data from the data files into dump files.

Physical backup of the database can be done using Velero restic to take the backup of the whole db volume. That can be useful in some cases however it can take so long to make and restore your back-up that you violate what is called your recovery point objective (RPO)- the maximum window of time you can spend on getting the data back. Instead of the physical backup, we see a demand for logical backups to save much time, especially in the case of db small tables, leveraging mysqldump to provide a point-in-time application consistent backup.

In this case, we can only mysqldump file at the time of velero restic support.

Though, for this approach to work properly, post restore hooks needs to be supported by Velero. The Velero team is tracking this issue here:

Velero pod restarted after adding new credentials

MayaData’s

Data Migration as a Service(DMaaS) is a solution for data agility on the Kubernetes platform. This solution provides utilities and workflows to migrate Kubernetes stateful workloads along-with their persistent data from anywhere to anywhere, be it on-premise or across clouds. It is application-aware, so the application state is consistent before and after migration.

Currently, we provide support for GCS and AWS S3 buckets. We have faced some issues that have shown some of other not yet fully polished pieces of Velero. As an example, one issue occurred when a user started a scheduled backup with GCP credentials and at the same time - on the same cluster - another user started another scheduled backup for another application using a different cloud provider. When the credentials for the new user is added, the Velero pod is restarted, causing the backups to be stuck in InProgress state. This is a known issue documented here:

According to the above document:

“Velero (or a pod it was backing up) restarted during a backup, and the backup is stuck InProgress Velero cannot currently resume backups that were interrupted. Backups stuck in the InProgress phase can be deleted with kubectl delete backup \<name\> -n \<velero-namespace\>. Backups in the InProgress phase have not uploaded any files to object storage.”

This is the kind of issue that we anticipated when building DMaaS by the way, so we build some resilience into the system in terms of retries and otherwise use metadata about jobs and so forth. So far so good - the combination with the cStor engine and the OpenEBS architecture being comprised basically of a bunch of CRDs gives us a lot of hooks we can use to deliver on-demand and scheduled back-ups and restores.

### Conclusion

Hopefully, this blog shared some useful insights into the state of stateful backups using Velero and Restic (state of state :)). I’m confident that Velero will be improved with the collective efforts of the community. MayaData and the broader OpenEBS community is doing its part by creating a cStor plugin to extend backup options and also the managed back-up and migration service

### Resources

[https://blogs.vmware.com/cloudnative/2019/02/28/velero-v0-11-delivers-an-open-source-tool-to-back-up-and-migrate-kubernetes-clusters/](https://blogs.vmware.com/cloudnative/2019/02/28/velero-v0-11-delivers-an-open-source-tool-to-back-up-and-migrate-kubernetes-clusters/)
