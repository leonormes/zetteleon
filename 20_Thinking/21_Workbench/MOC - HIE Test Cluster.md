---
created: 2025-12-04T12:02:41Z
last_reviewed:
modified: 2026-02-09T11:11:35+00:00
status: processing
tags: [customer/hie, ff_deploy, state/thinking]
title: MOC - HIE Test Cluster
type: head
updated:
---

I need to create a new hie cluster for testing.

The existing vpc has a cidr range of `10.65.0.0/20`

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
- find the hie iac
- create the new central services.
Then check the permissions.
