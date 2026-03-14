---
aliases: []
created: 2025-12-04T12:02:41Z
id: MOC - HIE Test Cluster
last_reviewed:
modified: 2026-02-27T09:19:56+00:00
status: processing
tags: [customer/hie, ff_deploy, state/thinking]
title: MOC - HIE Test Cluster
type: map
updated: 2026-02-09T12:00:00+00:00
---

I need to create a new hie cluster for testing.

The existing VPC has a CIDR range of `10.65.0.0/20`

```sh
./vpc_description.sh
--- Initialising AWS Resource Discovery ---
Region: eu-west-2
VPC ID: vpc-0aabc42188b2162bf
----------------------------------------
[+] Subnets in this VPC:
-------------------------------------------------------------
|                      DescribeSubnets                      |
+------------+-----------------+----------------------------+
|     AZ     |      CIDR       |            ID              |
+------------+-----------------+----------------------------+
|  eu-west-2a|  10.65.2.0/23   |  subnet-089c457b2998ff843  |
|  eu-west-2a|  10.65.4.0/23   |  subnet-02b4bec3447cbbf9e  |
|  eu-west-2a|  10.65.12.0/23  |  subnet-0ce985eee4e639be1  |
|  eu-west-2b|  10.65.14.0/23  |  subnet-04b88a21fbe703f1a  |
|  eu-west-2a|  10.65.8.0/23   |  subnet-05aaee38dce4b5001  |
|  eu-west-2a|  10.65.10.0/23  |  subnet-037cf38f30c2cd25d  |
|  eu-west-2b|  10.65.6.0/23   |  subnet-0c3d71c782e12d044  |
+------------+-----------------+----------------------------+
[+] Security Groups:
-------------------------------------------------------------------------------------
|                              DescribeSecurityGroups                               |
+-----------------------+-----------------------------------------------------------+
|          ID           |                           Name                            |
+-----------------------+-----------------------------------------------------------+
|  sg-0c25c161ce4a58b4b |  eoe-sde-codisc-jumpbox-sg                                |
|  sg-0bc91b9f1501f81c0 |  eoe-sde-codisc-vpc-endpoints-20250214173612314300000009  |
|  sg-0dc70f9990b53e4fd |  codisc-from-sde-multi                                    |
|  sg-02a02b439ed4569b6 |  eoe-sde-codisc-eks-elb                                   |
|  sg-06a3ef4dc97a131f1 |  eoe-sde-codisc-relay-alb-sg                              |
|  sg-0a3345e3be2761343 |  eoe-sde-codisc-eks-additional-access                     |
|  sg-02dcb1a5bbe8844b8 |  eks-cluster-sg-eoe-sde-codisc-1541232588                 |
|  sg-07983cf22f5dd5915 |  codisc-from-sde-dev                                      |
|  sg-0e4f97de870b4f6c0 |  default                                                  |
+-----------------------+-----------------------------------------------------------+
[+] EKS Clusters in this Region:
--- Cluster: eoe-sde-codisc ---
Status: ACTIVE
Endpoint: https://23BDD27C5ECF85950BCEA129801871CB.gr7.eu-west-2.eks.amazonaws.com
Version: 1.33
Managed Node Groups:
--------------------------
|     ListNodegroups     |
+------------------------+
||      nodegroups      ||
|+----------------------+|
||  SystemNodeGroup     ||
||  WorkflowsNodeGroup  ||
|+----------------------+|
----------------------------------------
Discovery Complete.
ip-10-65-2-8% kubectl get nodes
NAME                                        STATUS   ROLES    AGE     VERSION
ip-10-65-4-86.eu-west-2.compute.internal    Ready    <none>   3d20h   v1.33.5-eks-ecaa3a6
ip-10-65-5-32.eu-west-2.compute.internal    Ready    <none>   3d20h   v1.33.5-eks-ecaa3a6
ip-10-65-6-123.eu-west-2.compute.internal   Ready    <none>   3d20h   v1.33.5-eks-ecaa3a6
ip-10-65-6-238.eu-west-2.compute.internal   Ready    <none>   3d20h   v1.33.5-eks-ecaa3a6
ip-10-65-7-187.eu-west-2.compute.internal   Ready    <none>   3d18h   v1.33.5-eks-ecaa3a6
```

First step is to setup the central services.

- Login to vault
- login to terraform cloud
- find the HIE IaC
- create the new central services.
  Then check the permissions.

## Jira Task Breakdown (FTFL-223)

Summary: Node Installation EoE Test

Description: The Node installation includes the configuration of Central Services, Deployment of Infrastructure and Platform as well as the configuration of certificates and inbound routes.

### Subtasks

#### FTFL-226: Central Services EoE Test

_Status: Backlog_

This task configures Auth0, Grafana and Vault central services.

#### FTFL-225: Setup Infrastructure EoE Test

_Status: Backlog_

This task sets up the Network, Virtual Machines (Servers) and Kubernetes.

#### FTFL-224: Deploy Platform EoE Test

_Status: Backlog_

ArgoCD is deployed which then deploys the FITFILE platform.

[Confluence Link](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1839038518/Azure+-+Platform+private#Creating-Virtual-Network-Gateway)

Here is the summary formatted as a structured Wiki page. You can copy and paste this directly into your documentation system (Confluence, Notion, GitHub Wiki, etc.).

---

## Project: FITFILE Test Node Deployment

Date: 09/02/2026

Status: Approved / Pending Timeline

Primary Contact: Keiran Raine (HIE), Susannah Thomas (FITFILE)

### 1. Executive Summary

Health Innovation East (HIE) requires a dedicated FITFILE Test Node to validate SDE platform upgrades (specifically RES and LZA components) without risking stability in the production environment. This node will function independently within the HIE Test Environment.

### 2. Objectives

- To enable safe testing of SDE platform upgrades.
- To provide an environment for FITFILE to debug and test updates (harmonisation containers, queries) using synthetic data.
- To ensure no impact on the live production node during maintenance windows.

### 3. Scope of Work & Delivery Steps

The following steps have been agreed upon for the deployment:

1. Node Deployment: Deploy and configure the FITFILE test node.
2. Storage Integration: Integrate designated QC and Data Export S3 buckets (Test versions).
3. External Connectivity:
   - Connect to HDRUK Cohort Discovery (Pre-production collection).
   - Connect to RES Test environment.
4. Cohort Discovery: Deploy "Bunny" component to enable Cohort Discovery queries.

### 4. Technical Architecture & Assumptions

The following constraints and configurations have been confirmed by [[Keiran Raine]]:

| Category        | Requirement / Configuration                                                           |
| --------------- | ------------------------------------------------------------------------------------- |
| Hosting         | Same AWS Account as Production, but hosted in a Separate VPC.                         |
| Data Isolation  | No connection to Data Provider Nodes.                                                 |
| User Access     | Admin users only. No existing users will be transferred from the SDE Production Node. |
| Data Usage      | Local Synthetic Data only (for debugging/testing).                                    |
| Cost Management | Node must support Sleep Mode when not in use to reduce costs.                         |
