---
aliases: []
confidence: 
created: 2025-08-14T01:54:25Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:09Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, hie-prod-34, infrastructure, topic/technology/networking, vpc]
title: AWS resources associated with the hie sde VPC
type:
uid: 
updated: 
version:
---

Based on the information you provided, here is a summary of the AWS resources associated with the VPC `vpc-0aabc42188b2162bf`:

## VPC Details

- **VPC ID**: `vpc-0aabc42188b2162bf`
- **CIDR Block**: `10.65.0.0/20`
- **Owner ID**: `135808916559`
- **Tags**:
  - **Name**: `eoe-sde-codisc`
  - **GitlabRepo**: `gitlab.com/fitfile/customers/eoe/hie-sde-v2`
  - **ProvisionByOrgName**: `FITFILE`
  - **Branch**: `master`

## NAT Gateway

- **NAT Gateway ID**: `nat-02c1a6d832f6683e5`
- **Subnet ID**: `subnet-0ce985eee4e639be1`
- **Public IP**: `13.42.119.194`

## Internet Gateway

- **Internet Gateway ID**: `igw-0b63cf7dd6df08d4e`

## Route Tables

- **Route Table IDs**:
  - `rtb-060666c152e1ad6ce`
  - `rtb-03009d054373572a6`
  - `rtb-0c3588944a5ce5db3`
  - `rtb-010658b9d1ef194c6`
  - `rtb-0ca24dc7f388d634e`
  - `rtb-0b92d17eadd2aae7d`
  - `rtb-0f255359a851689bc`
  - `rtb-0c1cdd9adc08a70cd`

## Subnets

- **Subnets**:
  - `subnet-089c457b2998ff843` - CIDR: `10.65.2.0/23` - Name: `Jumpbox`
  - `subnet-02b4bec3447cbbf9e` - CIDR: `10.65.4.0/23` - Name: `Eks_az_1`
  - `subnet-0ce985eee4e639be1` - CIDR: `10.65.12.0/23` - Name: `Nat`
  - `subnet-04b88a21fbe703f1a` - CIDR: `10.65.14.0/23` - Name: `Nat_az_2`
  - `subnet-05aaee38dce4b5001` - CIDR: `10.65.8.0/23` - Name: `Firewall`
  - `subnet-037cf38f30c2cd25d` - CIDR: `10.65.10.0/23` - Name: `Endpoints`
  - `subnet-0c3d71c782e12d044` - CIDR: `10.65.6.0/23` - Name: `Eks_az_2`

## Security Groups

- **Security Groups**:
  - `sg-0c25c161ce4a58b4b` - Name: `eoe-sde-codisc-jumpbox-sg`
  - `sg-0a3345e3be2761343` - Name: `eoe-sde-codisc-eks-additional-access`
  - `sg-0bc91b9f1501f81c0` - Name: `eoe-sde-codisc-vpc-endpoints-20250214173612314300000009`
  - `sg-06a3ef4dc97a131f1` - Name: `eoe-sde-codisc-relay-alb-sg`
  - `sg-07983cf22f5dd5915` - Name: `codisc-from-sde-dev`
  - `sg-02a02b439ed4569b6` - Name: `eoe-sde-codisc-eks-elb`
  - `sg-02dcb1a5bbe8844b8` - Name: `eks-cluster-sg-eoe-sde-codisc-1541232588`
  - `sg-0e4f97de870b4f6c0` - Name: `default`

This setup is part of the infrastructure for the `eoe-sde-codisc` project, which is managed under the `FITFILE` organization. If you need further details or assistance with any specific resource, feel free to ask!

## AWS Infrastructure Documentation - Eoe-sde-codisc

### Overview

This document outlines the AWS infrastructure for the eoe-sde-codisc environment, including VPC, EKS cluster, node groups, and VPC endpoints.

### Account Information

- **AWS Account ID**: 135808916559
- **Region**: eu-west-2 (London)
- **Authentication**: SSO via `DiscoveryEngineeringAccess` role
- **User**: <leon.ormes@fitfile.com>

### Network Configuration

#### VPC

- **Name**: eoe-sde-codisc
- **VPC ID**: vpc-0aabc42188b2162bf
- **CIDR Block**: 10.65.0.0/20

#### Subnets

| CIDR Block    | Purpose      |
| ------------- | ------------ |
| 10.65.0.0/26  | EKS Subnet 1 |
| 10.65.0.64/26 | EKS Subnet 2 |

### EKS Cluster

- **Cluster Name**: eoe-sde-codisc
- **Status**: ACTIVE

#### Node Groups

##### SystemNodeGroupV2

- **Status**: ACTIVE
- **Instance Type**: m5.xlarge
- **Desired Capacity**: 2
- **Min Size**: 1
- **Max Size**: 2
- **Disk Size**: 60GB

##### WorkflowsNodeGroupV2

- **Status**: ACTIVE
- **Instance Type**: m5.xlarge
- **Desired Capacity**: 1
- **Min Size**: 1
- **Max Size**: 1
- **Disk Size**: 20GB

### VPC Endpoints

The following VPC endpoints are configured for private connectivity:

1. **AWS Services**:
   - s3
   - autoscaling
   - elasticloadbalancing
   - sts
   - logs
   - ec2
   - ssmmessages
   - ec2messages

2. **ECR Endpoints**:
   - ecr.api
   - ecr.dkr

3. **Systems Manager**:
   - ssm

### Security

- **VPC Endpoints Security Group**: Configured and active

### Access Control

- Authentication: AWS IAM with SSO
- Role: AWSReservedSSO_DiscoveryEngineeringAccess_b38ff0a73dfb5f6d

### Notes

- The infrastructure is running in the eu-west-2 (London) region
- The environment appears to be properly configured with all necessary VPC endpoints for EKS operations
- Node groups are configured with appropriate scaling parameters for both system and workloads

---

## AWS Infrastructure Overview

### AWS Configuration

- **Profile:** 135808916559_DiscoveryEngineeringAccess
- **Account ID:** 135808916559
- **User ARN:** arn:aws:sts::135808916559:assumed-role/AWSReservedSSO_DiscoveryEngineeringAccess_b38ff0a73dfb5f6d/leon.ormes@fitfile.com
- **User ID:** AROAR7HWXTRH3OS4DQURH:leon.ormes@fitfile.com
- **Region:** Not Set
- **Default Region:** eu-west-2
- **AWS CLI Version:** aws-cli/2.27.53 Python/3.13.4 Linux/6.14.0-1009-aws exe/x86_64.ubuntu

AWS credentials have been successfully validated.

### AWS Resource Validation

#### VPC Configuration

- **VPC ID:** vpc-0aabc42188b2162bf
- **CIDR:** 10.65.0.0/20
- **Name:** eoe-sde-codisc

#### Subnet Configuration

- **Subnet CIDR 1:** 10.65.0.0/26
- **Subnet CIDR 2:** 10.65.0.64/26

#### EKS Cluster

- **Cluster Name:** eoe-sde-codisc
- **Status:** ACTIVE

#### Node Groups

##### SystemNodeGroupV2

- **Status:** ACTIVE
- **Desired Size:** 2
- **Disk Size:** 60
- **Instance Types:** m5.xlarge
- **Max Size:** 2
- **Min Size:** 1

##### WorkflowsNodeGroupV2

- **Status:** ACTIVE
- **Desired Size:** 1
- **Disk Size:** 20
- **Instance Types:** m5.xlarge
- **Max Size:** 1
- **Min Size:** 1

#### VPC Endpoints

- **s3**
- **autoscaling**
- **ecr.api**
- **ssm**
- **ecr.dkr**
- **elasticloadbalancing**
- **sts**
- **logs**
- **ec2**
- **ssmmessages**
- **ec2messages**

#### Security Groups

- **VPC Endpoints Security Group:** Validated

### Validation Summary

- **VPC ID:** vpc-0aabc42188b2162bf
- **EKS Cluster:** eoe-sde-codisc
- **Node Groups:** SystemNodeGroupV2, WorkflowsNodeGroupV2
- **Total VPC Endpoints:** 12

## AWS Infrastructure Overview

### AWS Configuration

- **Profile:** 135808916559_DiscoveryEngineeringAccess
- **Account ID:** 135808916559
- **Region:** Not set

### VPC Information

- **VPC ID:** vpc-0aabc42188b2162bf
- **VPC Name:** eoe-sde-codisc
- **CIDR Block:** 10.65.0.0/20

### Subnet Information

| Subnet ID                | CIDR Block    | Availability Zone | Public | Name      |
| ------------------------ | ------------- | ----------------- | ------ | --------- |
| subnet-037cf38f30c2cd25d | 10.65.10.0/23 | eu-west-2a        | False  | Endpoints |
| subnet-0ce985eee4e639be1 | 10.65.12.0/23 | eu-west-2a        | False  | Nat       |
| subnet-04b88a21fbe703f1a | 10.65.14.0/23 | eu-west-2b        | False  | Nat_az_2  |
| subnet-089c457b2998ff843 | 10.65.2.0/23  | eu-west-2a        | False  | Jumpbox   |
| subnet-02b4bec3447cbbf9e | 10.65.4.0/23  | eu-west-2a        | False  | Eks_az_1  |
| subnet-0c3d71c782e12d044 | 10.65.6.0/23  | eu-west-2b        | False  | Eks_az_2  |
| subnet-05aaee38dce4b5001 | 10.65.8.0/23  | eu-west-2a        | False  | Firewall  |

### Route Tables

| Route Table ID        | Associated Subnet ID     | Routes                                                                                                                    |
| --------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| rtb-060666c152e1ad6ce | main                     | 10.65.0.0/20, 169.254.171.0/24, 129.224.0.0/17                                                                            |
| rtb-03009d054373572a6 | subnet-04b88a21fbe703f1a | 10.65.0.0/20, 0.0.0.0/0, 169.254.171.0/24, 129.224.0.0/17                                                                 |
| rtb-0c3588944a5ce5db3 | subnet-0c3d71c782e12d044 | 10.64.11.0/25, 10.64.11.128/25, 10.64.14.0/25, 10.64.14.128/25, 10.65.0.0/20, 0.0.0.0/0, 169.254.171.0/24, 129.224.0.0/17 |
| rtb-010658b9d1ef194c6 | subnet-02b4bec3447cbbf9e | 10.65.0.0/20, 0.0.0.0/0, 169.254.171.0/24, 129.224.0.0/17                                                                 |
| rtb-0ca24dc7f388d634e | subnet-0ce985eee4e639be1 | 10.65.0.0/20, 0.0.0.0/0, 169.254.171.0/24, 129.224.0.0/17                                                                 |
| rtb-0b92d17eadd2aae7d | subnet-05aaee38dce4b5001 | 10.65.0.0/20, 0.0.0.0/0, 169.254.171.0/24, 129.224.0.0/17                                                                 |
| rtb-0f255359a851689bc | subnet-037cf38f30c2cd25d | 10.65.0.0/20, 169.254.171.0/24, 129.224.0.0/17                                                                            |
| rtb-0c1cdd9adc08a70cd | subnet-089c457b2998ff843 | 10.65.0.0/20, 0.0.0.0/0, 169.254.171.0/24, 129.224.0.0/17                                                                 |

### Security Groups

| Security Group ID    | Name                                                    | Description                                                                                                                     |
| -------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| sg-07983cf22f5dd5915 | codisc-from-sde-dev                                     | Allow https from SDE-dev                                                                                                        |
| sg-0e4f97de870b4f6c0 | default                                                 | default VPC security group                                                                                                      |
| sg-02dcb1a5bbe8844b8 | eks-cluster-sg-eoe-sde-codisc-1541232588                | EKS created security group applied to ENI that is attached to EKS Control Plane master nodes, as well as any managed workloads. |
| sg-0a3345e3be2761343 | eoe-sde-codisc-eks-additional-access                    | Additional Security group for allowing access to EKS API and Node group communication.                                          |
| sg-02a02b439ed4569b6 | eoe-sde-codisc-eks-elb                                  | Security group for allowing access to the EKS elastic load balancer used by NGINX Ingress Controller                            |
| sg-0c25c161ce4a58b4b | eoe-sde-codisc-jumpbox-sg                               | Security group for jumpbox instance                                                                                             |
| sg-06a3ef4dc97a131f1 | eoe-sde-codisc-relay-alb-sg                             | Allow HTTPS from Azure AKS only                                                                                                 |
| sg-0bc91b9f1501f81c0 | eoe-sde-codisc-vpc-endpoints-20250214173612314300000009 | VPC endpoint security group                                                                                                     |

### VPC Endpoints

| VPC Endpoint ID        | Service Name                                            | Type                | Status    |
| ---------------------- | ------------------------------------------------------- | ------------------- | --------- |
| vpce-0fb9202f9ba748333 | com.amazonaws.eu-west-2.autoscaling                     | Interface           | available |
| vpce-071f075074211ab5a | com.amazonaws.eu-west-2.ec2                             | Interface           | available |
| vpce-0adeaf00b434a520b | com.amazonaws.eu-west-2.ec2messages                     | Interface           | available |
| vpce-060e3b4640d56ab3f | com.amazonaws.eu-west-2.ecr.api                         | Interface           | available |
| vpce-0113ccf3577641155 | com.amazonaws.eu-west-2.ecr.dkr                         | Interface           | available |
| vpce-07a9bcf7dd366c440 | com.amazonaws.eu-west-2.elasticloadbalancing            | Interface           | available |
| vpce-068b531f2538fd05d | com.amazonaws.eu-west-2.logs                            | Interface           | available |
| vpce-0b384c673bc88e44f | com.amazonaws.eu-west-2.s3                              | Gateway             | available |
| vpce-0911936ed99dac899 | com.amazonaws.eu-west-2.ssm                             | Interface           | available |
| vpce-07e0b2edeeff3ad11 | com.amazonaws.eu-west-2.ssmmessages                     | Interface           | available |
| vpce-0eee9f7a0f91860e4 | com.amazonaws.eu-west-2.sts                             | Interface           | available |
| vpce-031bfaf1e2ee877ca | com.amazonaws.vpce.eu-west-2.vpce-svc-037926ac4de4bc82c | GatewayLoadBalancer | available |

### NAT Gateways

| NAT Gateway ID        | Subnet ID                | Status    |
| --------------------- | ------------------------ | --------- |
| nat-02c1a6d832f6683e5 | subnet-0ce985eee4e639be1 | available |

### Internet Gateways

| Internet Gateway ID   | Status    |
| --------------------- | --------- |
| igw-0b63cf7dd6df08d4e | available |

### EKS Cluster Information

```json
{
  "Name": "eoe-sde-codisc",
  "Status": "ACTIVE",
  "Version": "1.32",
  "Endpoint": "https://23BDD27C5ECF85950BCEA129801871CB.gr7.eu-west-2.eks.amazonaws.com",
  "RoleARN": "arn:aws:iam::135808916559:role/eoe-sde-codisc-cluster",
  "VPC": "vpc-0aabc42188b2162bf",
  "Subnets": ["subnet-0c3d71c782e12d044", "subnet-02b4bec3447cbbf9e"],
  "SecurityGroups": ["sg-0a3345e3be2761343"],
  "EndpointAccess": false,
  "EndpointPrivateAccess": true,
  "PublicAccessCIDRs": []
}
```

### Kubernetes Network Information

#### Nodes

- ip-10-65-4-141.eu-west-2.compute.internal Ready 10.65.4.141 \\<none\\>
- ip-10-65-4-97.eu-west-2.compute.internal Ready 10.65.4.97 \\<none\\>
- ip-10-65-6-207.eu-west-2.compute.internal Ready 10.65.6.207 \\<none\\>

#### Services

| NAMESPACE                         | NAME                                            | TYPE         | CLUSTER-IP     | EXTERNAL-IP                                                                   | PORT(S)                               | AGE  |
| --------------------------------- | ----------------------------------------------- | ------------ | -------------- | ----------------------------------------------------------------------------- | ------------------------------------- | ---- |
| argo                              | argo-workflows-server                           | ClusterIP    | 172.20.141.37  | \\<none\\>                                                                    | 2746/TCP                              | 98d  |
| argo                              | argo-workflows-workflow-controller              | ClusterIP    | 172.20.145.149 | \\<none\\>                                                                    | 8080/TCP,8081/TCP                     | 98d  |
| argocd                            | argocd-application-controller-metrics           | ClusterIP    | 172.20.62.192  | \\<none\\>                                                                    | 8082/TCP                              | 180d |
| argocd                            | argocd-applicationset-controller                | ClusterIP    | 172.20.88.64   | \\<none\\>                                                                    | 7000/TCP                              | 180d |
| argocd                            | argocd-applicationset-controller-metrics        | ClusterIP    | 172.20.83.123  | \\<none\\>                                                                    | 8080/TCP                              | 180d |
| argocd                            | argocd-dex-server                               | ClusterIP    | 172.20.9.76    | \\<none\\>                                                                    | 5556/TCP,5557/TCP,5558/TCP            | 180d |
| argocd                            | argocd-notifications-controller-metrics         | ClusterIP    | 172.20.58.72   | \\<none\\>                                                                    | 9001/TCP                              | 180d |
| argocd                            | argocd-redis                                    | ClusterIP    | 172.20.26.106  | \\<none\\>                                                                    | 6379/TCP                              | 180d |
| argocd                            | argocd-repo-server                              | ClusterIP    | 172.20.124.0   | \\<none\\>                                                                    | 8081/TCP                              | 180d |
| argocd                            | argocd-repo-server-metrics                      | ClusterIP    | 172.20.224.108 | \\<none\\>                                                                    | 8084/TCP                              | 180d |
| argocd                            | argocd-server                                   | ClusterIP    | 172.20.107.137 | \\<none\\>                                                                    | 80/TCP,443/TCP                        | 180d |
| argocd                            | argocd-server-metrics                           | ClusterIP    | 172.20.78.63   | \\<none\\>                                                                    | 8083/TCP                              | 180d |
| aws-application-networking-system | gateway-api-controller-metrics-service          | ClusterIP    | 172.20.65.243  | \\<none\\>                                                                    | 8443/TCP                              | 108d |
| aws-application-networking-system | webhook-service                                 | ClusterIP    | 172.20.46.201  | \\<none\\>                                                                    | 443/TCP                               | 108d |
| calico-system                     | calico-kube-controllers-metrics                 | ClusterIP    | None           | \\<none\\>                                                                    | 9094/TCP                              | 143d |
| calico-system                     | calico-node-metrics                             | ClusterIP    | None           | \\<none\\>                                                                    | 9081/TCP,9900/TCP                     | 143d |
| calico-system                     | calico-typha                                    | ClusterIP    | 172.20.100.224 | \\<none\\>                                                                    | 5473/TCP                              | 143d |
| default                           | kubernetes                                      | ClusterIP    | 172.20.0.1     | \\<none\\>                                                                    | 443/TCP                               | 180d |
| hie-prod-34                       | hie-prod-34-ffcloud-service                     | ClusterIP    | 172.20.17.35   | \\<none\\>                                                                    | 80/TCP                                | 98d  |
| hie-prod-34                       | hie-prod-34-fitconnect-ftc                      | ClusterIP    | 172.20.116.61  | \\<none\\>                                                                    | 80/TCP                                | 98d  |
| hie-prod-34                       | hie-prod-34-frontend-frontend                   | ClusterIP    | 172.20.255.208 | \\<none\\>                                                                    | 80/TCP                                | 98d  |
| hie-prod-34                       | hie-prod-34-minio                               | ClusterIP    | 172.20.82.139  | \\<none\\>                                                                    | 9000/TCP,9001/TCP                     | 98d  |
| hie-prod-34                       | hie-prod-34-mongodb-b17ef-arbiter-headless      | ClusterIP    | None           | \\<none\\>                                                                    | 27017/TCP                             | 15d  |
| hie-prod-34                       | hie-prod-34-mongodb-b17ef-headless              | ClusterIP    | None           | \\<none\\>                                                                    | 27017/TCP                             | 15d  |
| hie-prod-34                       | hie-prod-34-mongodb-b17ef-metrics               | ClusterIP    | 172.20.202.248 | \\<none\\>                                                                    | 9216/TCP                              | 15d  |
| hie-prod-34                       | hie-prod-34-postgresql                          | ClusterIP    | 172.20.131.27  | \\<none\\>                                                                    | 5432/TCP                              | 98d  |
| hie-prod-34                       | hie-prod-34-postgresql-hl                       | ClusterIP    | None           | \\<none\\>                                                                    | 5432/TCP                              | 98d  |
| hie-prod-34                       | workflows-api                                   | ClusterIP    | 172.20.24.94   | \\<none\\>                                                                    | 80/TCP                                | 98d  |
| hutch                             | hutch-postgresql                                | ClusterIP    | 172.20.114.12  | \\<none\\>                                                                    | 5432/TCP                              | 98d  |
| hutch                             | hutch-postgresql-hl                             | ClusterIP    | None           | \\<none\\>                                                                    | 5432/TCP                              | 98d  |
| hutch                             | hutch-rabbitmq                                  | ClusterIP    | 172.20.205.137 | \\<none\\>                                                                    | 5672/TCP,4369/TCP,25672/TCP,15672/TCP | 98d  |
| hutch                             | hutch-rabbitmq-headless                         | ClusterIP    | None           | \\<none\\>                                                                    | 4369/TCP,5672/TCP,25672/TCP,15672/TCP | 98d  |
| hutch                             | hutch-relay                                     | NodePort     | 172.20.192.249 | \\<none\\>                                                                    | 8080:32080/TCP,8081:32081/TCP         | 98d  |
| hutch                             | hutch-relay-nlb                                 | LoadBalancer | 172.20.160.17  | a3fa3e531694f45b78c96ac280fbd0da-a9ba316831e0281c.elb.eu-west-2.amazonaws.com | 443:30537/TCP                         | 69d  |
| ingress-nginx                     | ingress-nginx-controller                        | LoadBalancer | 172.20.48.18   | a09b6c067806443db8a14d79fbd6a2ac-3d6a600ba7023f54.elb.eu-west-2.amazonaws.com | 80:31139/TCP,443:32623/TCP            | 106d |
| ingress-nginx                     | ingress-nginx-controller-admission              | ClusterIP    | 172.20.30.12   | \\<none\\>                                                                    | 443/TCP                               | 106d |
| kube-system                       | cluster-autoscaler-aws-cluster-autoscaler       | ClusterIP    | 172.20.8.154   | \\<none\\>                                                                    | 8085/TCP                              | 180d |
| kube-system                       | eks-extension-metrics-api                       | ClusterIP    | 172.20.162.174 | \\<none\\>                                                                    | 443/TCP                               | 180d |
| kube-system                       | kube-dns                                        | ClusterIP    | 172.20.0.10    | \\<none\\>                                                                    | 53/UDP,53/TCP,9153/TCP                | 180d |
| monitoring                        | grafana-k8s-monitoring-alloy                    | ClusterIP    | 172.20.145.117 | \\<none\\>                                                                    | 12345/TCP,4317/TCP,4318/TCP,9411/TCP  | 98d  |
| monitoring                        | grafana-k8s-monitoring-alloy-cluster            | ClusterIP    | None           | \\<none\\>                                                                    | 12345/TCP,4317/TCP,4318/TCP,9411/TCP  | 98d  |
| monitoring                        | grafana-k8s-monitoring-alloy-events             | ClusterIP    | 172.20.3.243   | \\<none\\>                                                                    | 12345/TCP                             | 98d  |
| monitoring                        | grafana-k8s-monitoring-alloy-logs               | ClusterIP    | 172.20.149.174 | \\<none\\>                                                                    | 12345/TCP                             | 98d  |
| monitoring                        | grafana-k8s-monitoring-grafana-agent            | ClusterIP    | 172.20.83.84   | \\<none\\>                                                                    | 12345/TCP,4317/TCP,4318/TCP,9411/TCP  | 98d  |
| monitoring                        | grafana-k8s-monitoring-kube-state-metrics       | ClusterIP    | 172.20.78.135  | \\<none\\>                                                                    | 8080/TCP                              | 98d  |
| monitoring                        | grafana-k8s-monitoring-prometheus-node-exporter | ClusterIP    | 172.20.173.164 | \\<none\\>                                                                    | 9100/TCP                              | 98d  |
| spicedb                           | spicedb                                         | ClusterIP    | 172.20.29.167  | \\<none\\>                                                                    | 50051/TCP,8443/TCP,50053/TCP,9090/TCP | 98d  |
| spicedb                           | spicedb-postgresql                              | ClusterIP    | 172.20.92.147  | \\<none\\>                                                                    | 5432/TCP                              | 98d  |
| spicedb                           | spicedb-postgresql-hl                           | ClusterIP    | None           | \\<none\\>                                                                    | 5432/TCP                              | 98d  |
| thehyve                           | thehyve                                         | ClusterIP    | 172.20.34.14   | \\<none\\>                                                                    | 8080/TCP                              | 98d  |
| thehyve                           | thehyve-postgresql                              | ClusterIP    | 172.20.59.87   | \\<none\\>                                                                    | 5432/TCP                              | 98d  |
| thehyve                           | thehyve-postgresql-hl                           | ClusterIP    | None           | \\<none\\>                                                                    | 5432/TCP                              | 98d  |
| tigera-elasticsearch              | tigera-linseed                                  | ExternalName | \\<none\\>     | tigera-guardian.tigera-guardian.svc.cluster.local                             | \\<none\\>                            | 143d |
| tigera-elasticsearch              | tigera-secure-es-gateway-http                   | ExternalName | \\<none\\>     | tigera-guardian.tigera-guardian.svc.cluster.local                             | \\<none\\>                            | 143d |
| tigera-fluentd                    | fluentd-metrics                                 | ClusterIP    | None           | \\<none\\>                                                                    | 9081/TCP                              | 143d |
| tigera-guardian                   | tigera-bast-to-guardian-proxy                   | ClusterIP    | 172.20.220.20  | \\<none\\>                                                                    | 9443/TCP                              | 143d |
| tigera-guardian                   | tigera-guardian                                 | ClusterIP    | 172.20.82.102  | \\<none\\>                                                                    | 443/TCP,9200/TCP,5601/TCP             | 143d |
| tigera-image-assurance            | tigera-image-assurance-api                      | ExternalName | \\<none\\>     | tigera-bast-to-guardian-proxy.tigera-guardian.svc.cluster.local               | \\<none\\>                            | 143d |
| tigera-prometheus                 | calico-node-alertmanager                        | ClusterIP    | 172.20.30.203  | \\<none\\>                                                                    | 9093/TCP                              | 143d |
| tigera-prometheus                 | prometheus-http-api                             | ClusterIP    | 172.20.45.237  | \\<none\\>                                                                    | 9090/TCP                              | 143d |
| tigera-system                     | tigera-api                                      | ClusterIP    | 172.20.155.58  | \\<none\\>                                                                    | 443/TCP,8080/TCP                      | 143d |
| trivy-system                      | trivy-operator                                  | ClusterIP    | None           | \\<none\\>                                                                    | 80/TCP                                | 167d |
| vault-secrets-operator-system     | vault-secrets-operator-metrics-service          | ClusterIP    | 172.20.16.65   | \\<none\\>                                                                    | 8443/TCP                              | 180d |

#### Ingresses

| NAMESPACE   | NAME                                          | CLASS      | HOSTS                                                                                       | ADDRESS                                                                       | PORTS   | AGE  |
| ----------- | --------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------- | ---- |
| argocd      | argocd-server                                 | nginx      | argocd.eoe-sde-codisc.privatelink.fitfile.net,argocd.eoe-sde-codisc.privatelink.fitfile.net | a09b6c067806443db8a14d79fbd6a2ac-3d6a600ba7023f54.elb.eu-west-2.amazonaws.com | 80, 443 | 180d |
| hie-prod-34 | hie-prod-34-ffcloud-service-ingress           | \\<none\\> | app.eoe-sde-codisc.privatelink.fitfile.net                                                  | a09b6c067806443db8a14d79fbd6a2ac-3d6a600ba7023f54.elb.eu-west-2.amazonaws.com | 80, 443 | 98d  |
| hie-prod-34 | hie-prod-34-fitconnect-ftc-ingress            | \\<none\\> | app.eoe-sde-codisc.privatelink.fitfile.net                                                  | a09b6c067806443db8a14d79fbd6a2ac-3d6a600ba7023f54.elb.eu-west-2.amazonaws.com | 80, 443 | 98d  |
| hie-prod-34 | hie-prod-34-frontend-frontend-default-ingress | \\<none\\> | app.eoe-sde-codisc.privatelink.fitfile.net                                                  | a09b6c067806443db8a14d79fbd6a2ac-3d6a600ba7023f54.elb.eu-west-2.amazonaws.com | 80, 443 | 98d  |
| hie-prod-34 | hie-prod-34-frontend-frontend-ingress         | \\<none\\> | app.eoe-sde-codisc.privatelink.fitfile.net                                                  | a09b6c067806443db8a14d79fbd6a2ac-3d6a600ba7023f54.elb.eu-west-2.amazonaws.com | 80, 443 | 98d  |
| hutch       | api-gateway-ingress                           | \\<none\\> | relay.codisc-eoe-sde.uk                                                                     | 80                                                                            | 68d     |

#### Network Policies

| NAMESPACE   | NAME                           | POD-SELECTOR                                                                                                            | AGE |
| ----------- | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------- | --- |
| hie-prod-34 | hie-prod-34-minio              | app.kubernetes.io/instance=hie-prod-34-minio,app.kubernetes.io/name=minio                                               | 98d |
| hie-prod-34 | hie-prod-34-minio-provisioning | app.kubernetes.io/component=minio-provisioning                                                                          | 98d |
| hie-prod-34 | hie-prod-34-mongodb-b17ef      | app.kubernetes.io/component=mongodb,app.kubernetes.io/instance=hie-prod-34-mongodb-b17ef,app.kubernetes.io/name=mongodb | 15d |
| hie-prod-34 | hie-prod-34-postgresql         | app.kubernetes.io/component=primary,app.kubernetes.io/instance=hie-prod-34-postgresql,app.kubernetes.io/name=postgresql | 98d |
| hutch       | hutch-postgresql               | app.kubernetes.io/component=primary,app.kubernetes.io/instance=hutch,app.kubernetes.io/name=postgresql                  | 98d |
| hutch       | hutch-rabbitmq                 | app.kubernetes.io/instance=hutch,app.kubernetes.io/name=rabbitmq                                                        | 98d |
| spicedb     | spicedb-postgresql             | app.kubernetes.io/component=primary,app.kubernetes.io/instance=spicedb,app.kubernetes.io/name=postgresql                | 98d |
| thehyve     | thehyve-postgresql             | app.kubernetes.io/component=primary,app.kubernetes.io/instance=thehyve,app.kubernetes.io/name=postgresql                | 98d |

### CNI Information

- Error from server (NotFound): daemonsets.apps "aws-node" not found

### CoreDNS Configuration

```yaml
apiVersion: v1
data:
  Corefile: |
    .:53 {
        errors
        health {
            lameduck 5s
          }
        ready
        rewrite name app.eoe-sde-codisc.privatelink.fitfile.net ingress-nginx-controller.ingress-nginx.svc.cluster.local
        kubernetes cluster.local in-addr.arpa ip6.arpa {
          pods insecure
          fallthrough in-addr.arpa ip6.arpa
        }
        prometheus :9153
        forward . /etc/resolv.conf
        cache 30
        loop
        reload
        loadbalance
    }
kind: ConfigMap
metadata:
  creationTimestamp: "2025-02-14T17:48:14Z"
  labels:
    eks.amazonaws.com/component: coredns
    k8s-app: kube-dns
  name: coredns
  namespace: kube-system
  resourceVersion: "6230336"
  uid: 35a55934-f357-480f-9d28-10edb8ee1a53
```

### Conclusion

- ✅ Network diagnostics completed

Based on the information provided in the long-term memories and project context, it appears that there is an egress setup for the `fitconnect` to call out to the internet. Here's a summary of the relevant components:

1. **NAT Gateway**:
   - The NAT Gateway with ID `nat-02c1a6d832f6683e5` is configured with a static Elastic IP `13.42.119.194`. This NAT Gateway is used to provide internet access for resources in private subnets within the VPC. It is located in the subnet `subnet-0ce985eee4e639be1` in the `eu-west-2a` availability zone. This setup allows instances in private subnets to initiate outbound traffic to the internet while preventing unsolicited inbound traffic.

2. **Route Tables**:
   - The route tables associated with the VPC `vpc-0aabc42188b2162bf` should have routes directing outbound traffic from private subnets to the NAT Gateway. This is a common configuration to enable egress traffic to the internet.

3. **Firewall and Security Groups**:
   - The configuration includes network firewall rules and security groups that manage traffic routing and security. These components ensure that only authorized traffic is allowed to and from the internet.

4. **Proxy Configuration**:
   - There is mention of a corporate web proxy (Skyhigh/McAfee Secure Web Gateway) that intercepts outbound traffic and requires authentication. This proxy setup is part of the security perimeter and ensures that all outbound traffic is monitored and controlled.

5. **On-Premise Integration**:
   - The FITFILE system integrates with the Cambridge University Hospitals (CUH) on-premise infrastructure, which includes FortiGate firewalls and an on-premise web proxy. This setup allows traffic from the FITFILE Azure subscription to flow through the secure ExpressRoute connection and the CUH firewalls before reaching the internet.

In conclusion, the egress gateway for `fitconnect` to call out to the internet is facilitated by the NAT Gateway and the corporate web proxy setup. This configuration ensures secure and controlled internet access for the `fitconnect` application. If you need to verify or modify this setup, you can check the route tables and security group configurations in your AWS environment.

Of course. Here is a wiki page detailing the network architecture and access controls for the `fitfile` application.

---

## **Networking Architecture: Eoe-sde-codisc Environment**

This document outlines the network configuration for the `eoe-sde-codisc` AWS environment, with a specific focus on the access capabilities of the `fitfile` application running within the `hie-prod-34` Kubernetes namespace.

### **I. High-Level Overview**

The entire environment is built within a single Virtual Private Cloud (VPC), `vpc-0aabc42188b2162bf`. This VPC is logically isolated from other virtual networks. The infrastructure within this VPC is designed around the principle of least privilege, using private subnets for workloads and controlling traffic flow through route tables, security groups, and network policies.

The `fitfile` application, along with its dependent services like PostgreSQL and Minio, runs in the `hie-prod-34` namespace on an Amazon EKS (Kubernetes) cluster. The cluster nodes themselves are located in private subnets, meaning they do not have public IP addresses and cannot be reached directly from the internet.

---

### **II. Outbound Access (Egress)**

How the `fitfile` application accesses the internet.

- **Path to Internet:** Applications within the `hie-prod-34` namespace can initiate outbound connections to the internet. This is facilitated by a **NAT (Network Address Translation) Gateway**.
  - **NAT Gateway ID:** `nat-02c1a6d832f6683e5`.
  - **Public IP:** All outbound traffic from the application appears to originate from the static public IP address `13.42.119.194`.
- **Routing:** The EKS nodes reside in private subnets (e.g., `Eks_az_1`, `Eks_az_2`). The route tables associated with these subnets (`rtb-010658b9d1ef194c6`, `rtb-0c3588944a5ce5db3`) have a default route (`0.0.0.0/0`) that directs all internet-bound traffic to the NAT Gateway.

**Conclusion:** The `fitfile` application **can** make calls out to the internet. This is necessary for it to connect to external APIs or services. All this traffic is routed through the NAT Gateway.

---

### **III. Inbound Access (Ingress)**

How external services access the `fitfile` application.

- **No Direct Public Access:** The application is **not** exposed directly to the public internet. The EKS cluster's API endpoint is private (`EndpointPrivateAccess: true`), and the application's ingress points use a `privatelink` hostname (`app.eoe-sde-codisc.privatelink.fitfile.net`).
- **Controlled Access via Load Balancer:** Inbound traffic is managed by an `ingress-nginx` controller, which runs behind an internal AWS Network Load Balancer.
- **Primary Entrypoint:** The primary access seems to be from a connected **Azure AKS environment**. This is suggested by the security group `sg-06a3ef4dc97a131f1` (`eoe-sde-codisc-relay-alb-sg`), whose purpose is to "Allow HTTPS from Azure AKS only".

**Conclusion:** The `fitfile` application can only be accessed from trusted, specific locations, primarily the connected Azure environment. It is not open to the general internet.

---

### **IV. Internal Network Access**

What the `fitfile` application can access within the AWS and Kubernetes environment.

#### **AWS Service Access**

The application can communicate with a wide range of AWS services privately and securely, without sending traffic over the public internet. This is achieved using **VPC Endpoints**. Key services accessible this way include:

- **Amazon S3:** For object storage.
- **Amazon ECR:** For pulling container images.
- **AWS STS (Security Token Service):** For IAM role authentication.
- **Amazon CloudWatch Logs:** For logging.
- **AWS Systems Manager (SSM):** For systems management.
- **EC2 and Elastic Load Balancing**.

#### **Kubernetes Cluster Access**

- **Internal DNS:** The CoreDNS service within the cluster is configured to resolve `app.eoe-sde-codisc.privatelink.fitfile.net` directly to the internal NGINX ingress controller service. This allows services within the cluster to communicate with each other using the external hostname, without the traffic ever leaving the cluster.
- **Pod-to-Pod Communication:** Communication between pods is restricted by **Kubernetes Network Policies**. Within the `hie-prod-34` namespace, there are specific policies defined for:
  - `hie-prod-34-minio`
  - `hie-prod-34-mongodb-b17ef`
  - `hie-prod-34-postgresql`
- This means that, by default, pods cannot freely communicate with each other unless a policy explicitly allows it, enforcing a zero-trust network model within the namespace.

**Conclusion:** The `fitfile` application has secure, private access to necessary AWS services and other applications within the cluster, such as its databases (`PostgreSQL`, `MongoDB`) and object store (`Minio`). This internal communication is tightly controlled by network policies.
