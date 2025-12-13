---
aliases: []
confidence: 
created: 2025-02-07T12:57:53Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:52Z
purpose: 
review_interval: 
see_also: []
source: https://dev.to/aws-builders/managing-aws-eks-access-entries-with-terraform-and-opentofu-414
source_of_truth: []
status: 
tags: [aws, ff_deploy, IAM]
title: aws_eks_access_management_with_terraform
type: config
uid: 
updated: 
version:
---

## AWS EKS Access Management with Terraform

> Setting up EKS authentication and authorization using Infrastructure as Code

### 📚 Introduction

Managing who can access your AWS EKS clusters can be tricky, especially in big companies. Usually, the person who creates the EKS cluster has full control. But this can be a problem for security and management. AWS EKS has new controls called access entries to help manage who can access your Kubernetes clusters more easily.

In this blog, we will show you how to use Terraform and OpenTofu to set up access entries for your AWS EKS clusters. We will explain what access entries are, the different options you can use, and how this new method makes it easier to manage who can access your clusters.

### The Need for EKS Access Entries

Traditionally, we used a special `aws-auth`

With the introduction of Access Entries, AWS has provided a more streamlined and efficient way to manage access to EKS clusters. Now, we can manage access directly through the

This new approach integrates seamlessly with

By moving access control to a dedicated infrastructure as code, we can manage access more easily and with less risk. In the old system, there was a chance you would lose cluster access if you deleted the cluster owner. Now, other users can add IAM principals to access the cluster through APIs, making it easier to manage access with

Access Entries also provide predefined access policies that can be assigned to IAM principals outside the cluster through EKS APIs. This allows users to access cluster resources without needing to define RBAC resources inside the Kubernetes cluster, simplifying the management process and enhancing security.

### ⚛️ Legacy Access Management: IAM and Aws-auth ConfigMaps

> 🔴 CAUTION: The aws-auth ConfigMap is deprecated

In the early days of AWS EKS, managing access to Kubernetes clusters was primarily done through AWS IAM roles and the `aws-auth` ConfigMap. This method involved mapping IAM users and roles to Kubernetes RBAC (Role-Based Access Control) roles and groups.

The `aws-auth` ConfigMap was a critical component in this setup, serving as the bridge between AWS IAM and Kubernetes RBAC.

#### Detailed Explanation of the Aws-auth ConfigMap

The `aws-auth` ConfigMap is a Kubernetes configuration map that resides in the `kube-system` namespace of an EKS cluster. It contains mappings that associate AWS IAM roles and users with Kubernetes RBAC roles and groups.

Here is an example of what the `aws-auth` ConfigMap might look like:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
data:
  mapRoles: |
    - rolearn: arn:aws:iam::123456789012:role/EKS-NodeInstanceRole
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes
  mapUsers: |
    - userarn: arn:aws:iam::123456789012:user/admin
      username: admin
      groups:
        - system:masters
  mapAccounts: |
    - "123456789012"
```

Components of the aws-auth ConfigMap

1. mapRoles: This section maps IAM roles to Kubernetes usernames and groups. For example, the `EKS-NodeInstanceRole` is mapped to the `system:nodes` group, which grants the necessary permissions for node operations.
2. mapUsers: This section maps IAM users to Kubernetes usernames and groups. For instance, the `admin` user is mapped to the `system:masters` group, granting cluster admin privileges.
3. mapAccounts: This optional section allows specifying AWS account IDs that are trusted to authenticate to the cluster.

#### Issues and Challenges with Using IAM and ConfigMap for Access Management

While the `aws-auth` ConfigMap provided a way to manage access, it came with several challenges:

1. Manual updates: Any changes to access control required manual updates to the `aws-auth` ConfigMap. This process was error-prone and could lead to misconfigurations.
2. Scalability: Managing access for a large number of users and roles became cumbersome. Each change required editing the ConfigMap, which was not scalable in large environments.
3. Risk of misconfiguration: A single mistake in the ConfigMap could break access control, potentially locking out users or granting unintended permissions.
4. Lack of visibility: The `aws-auth` ConfigMap did not provide a clear way to audit or track changes, making it difficult to maintain security and compliance.
5. Cluster owner issues: The default cluster creator had full admin rights, and there was no straightforward way to change the cluster owner. Deleting the cluster owner could result in losing access to the cluster.

#### A Real World Scenario

Consider a scenario where you need to add a new IAM user to the `system:masters` group for admin access. You would need to manually edit the `aws-auth` ConfigMap as follows:

1. Retrieve the current `aws-auth` ConfigMap:

```sh
    kubectl get configmap aws-auth -n kube-system -o yaml > aws-auth.yaml
```

1. Edit the `aws-auth.yaml` file to add the new user:

```yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: aws-auth
      namespace: kube-system
    data:
      mapRoles: |
        - rolearn: arn:aws:iam::123456789012:role/EKS-NodeInstanceRole
          username: system:node:{{EC2PrivateDNSName}}
          groups:
            - system:bootstrappers
            - system:nodes
      mapUsers: |
        - userarn: arn:aws:iam::123456789012:user/admin
          username: admin
          groups:
            - system:masters
        - userarn: arn:aws:iam::123456789012:user/new-admin
          username: new-admin
          groups:
            - system:masters
      mapAccounts: |
        - "123456789012"
```

1. Apply the updated ConfigMap:

```sh
    kubectl apply -f aws-auth.yaml
```

This manual process is prone to errors and does not scale well, highlighting the need for a more efficient access management solution.

### EKS API: The New Way of Granting Access

AWS has introduced a new way to manage access to EKS clusters using the EKS API. This method allows you to manage access entries directly through the API, making use of AWS IAM for authentication. This new approach simplifies the process of managing who can access your Kubernetes clusters and integrates seamlessly with Kubernetes' RBAC (Role-Based Access Control).

#### Enabling Access Entries

To enable Access Entries on new or existing clusters, you need to use the latest version of the AWS CLI, which includes the `--access-config` option in the EKS create/update commands. Here’s how you can enable Access Entries:

##### Creating a New Cluster with Access Entries

```sh
aws eks create-cluster \
   --name <CLUSTER_NAME> \
   --role-arn <CLUSTER_ROLE_ARN> \
   --resources-vpc-config subnetIds=<value>,endpointPublicAccess=true \
   --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enabled":true}]}' \
   --access-config authenticationMode=API_AND_CONFIG_MAP
```

Updating an existing cluster to use Access entries

```sh
aws eks update-cluster-config \
   --name <CLUSTER_NAME> \
   --access-config authenticationMode=API
```

#### Comparison Between the New API and the Old ConfigMap Method

#### Advantages of Using the EKS API

1. Simplified access management: The EKS API allows you to manage access entries directly, reducing the complexity and risk associated with manual ConfigMap updates.
2. Integration with IAM and RBAC: Combines AWS IAM for authentication and Kubernetes RBAC for authorization, providing a robust and flexible access control system.
3. Predefined Access Policies: AWS provides predefined access policies similar to Kubernetes ClusterRoles:
- AmazonEKSClusterAdminPolicy – cluster-admin
- AmazonEKSAdminPolicy – admin
- AmazonEKSEditPolicy – edit
- AmazonEKSViewPolicy – view
4. Enhanced security: By managing access through the EKS API, you can ensure that only authorized users have access to your clusters, improving overall security.
5. Infrastructure as Code (IaC): Easily manage access entries using IaC tools like Terraform, OpenTofu, Pulumi, Ansible, and CloudFormation.

#### Example AWS CLI Commands

Listing Existing Access Entries

```sh
aws eks list-access-entries --cluster-name <CLUSTER_NAME>
```

Creating a Cluster Access Entry

```sh
aws eks create-access-entry --cluster-name <CLUSTER_NAME> \
  --principal-arn <IAM_PRINCIPAL_ARN>
```

Associating an Access Policy to an Access Entry

```sh
aws eks associate-access-policy --cluster-name <CLUSTER_NAME> \
  --principal-arn <IAM_PRINCIPAL_ARN> \
  --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy \
  --access-scope type=cluster
```

Changing the `authentication_mode` is a one-way operation. You can switch from `CONFIG_MAP` to `API_AND_CONFIG_MAP`, and then to `API`, but you cannot revert these changes.

#### Combining EKS API with Kubernetes RBAC

The EKS API does not replace Kubernetes RBAC but works alongside it. For example, you can create a cluster access entry and then use Kubernetes RBAC to assign permissions:

1Creating a Cluster Access Entry

```sh
aws eks create-access-entry --cluster-name <CLUSTER_NAME> \
  --principal-arn <IAM_PRINCIPAL_ARN> \
  --kubernetes-groups eks-admins
```

2Applying a Cluster Role Binding

Create a `crb.yaml` file with the following content:

```sh
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin-ae
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: eks-admins
```

Apply the Cluster Role Binding:

```sh
kubectl apply -f crb.yaml
```

#### Managing EKS Access Policies with Terraform and OpenTofu

##### Prerequisites

- AWS Account: Ensure you have an AWS account and the necessary permissions to create the required resources.
- Terraform: Install Terraform on your machine.
- OpenTofu: Ensure OpenTofu is installed on your machine.

##### IAC Configuration

Here is an example configuration to set up an EKS cluster with access entries:

```sh
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "my-cluster"
  cluster_version = "1.30"

  cluster_endpoint_public_access  = true

  cluster_addons = {
    coredns                = {}
    eks-pod-identity-agent = {}
    kube-proxy             = {}
    vpc-cni                = {}
  }

  vpc_id                   = "vpc-1234556abcdef"
  subnet_ids               =
  control_plane_subnet_ids =

  # EKS Managed Node Group(s)
  eks_managed_node_group_defaults = {
    instance_types =
  }

  eks_managed_node_groups = {
    example = {
      # Starting on 1.30, AL2023 is the default AMI type for EKS managed node groups
      ami_type       = "AL2023_x86_64_STANDARD"
      instance_types =

      min_size     = 2
      max_size     = 10
      desired_size = 2
    }
  }

  # Cluster access entry
  # To add the current caller identity as an administrator
  enable_cluster_creator_admin_permissions = true

  access_entries = {
    # One access entry with a policy associated
    example = {
      kubernetes_groups =
      principal_arn     = "arn:aws:iam::123456789012:role/something"

      policy_associations = {
        example = {
          policy_arn = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSViewPolicy"
          access_scope = {
            namespaces =
            type       = "namespace"
          }
        }
      }
    }
  }

  tags = {
    Environment = "dev"
    Terraform   = "true"
  }
}
```

#### Explanation of the Code

This Terraform configuration sets up an AWS EKS cluster with the following components:

1. EKS Cluster: Creates an EKS cluster named "my-cluster" with version 1.30.
2. Cluster Endpoint: Enables public access to the cluster endpoint.
3. Cluster Addons: Installs essential Kubernetes addons such as CoreDNS, EKS Pod Identity Agent, Kube-Proxy, and VPC CNI.
4. VPC Configuration: Specifies the VPC and subnets for the EKS cluster.
5. Managed Node Groups: Configures managed node groups with specified instance types and sizes.
6. Access Entries:
- Cluster Creator Admin Permissions: Enables the current caller identity as an administrator.
- Example Access Entry: Creates an access entry for an IAM role with the ARN `arn:aws:iam::123456789012:role/something`. This entry is associated with the `AmazonEKSViewPolicy`, granting view permissions within the "default" namespace.

#### Applying the Configuration

This configuration automates the setup of an AWS EKS cluster, including the creation of access entries and the association of IAM policies. Specifically, it creates the following:

- Access entries:
- Example Access Entry: Associates the IAM role `arn:aws:iam::123456789012:role/something` with the `AmazonEKSViewPolicy`, granting view permissions within the "default" namespace.
- IAM Policies:
- AmazonEKSClusterPolicy: Attached to the EKS cluster IAM role.
- AmazonEKSVPCResourceController: Attached to the EKS cluster IAM role.
- AmazonEKSViewPolicy: Associated with the example access entry.

#### Checking Access Entries and IAM Policies

After the creation is complete, you can verify the access entries and IAM policies using the AWS CLI:

##### List Access Entries

To list the access entries for your EKS cluster, use the following command:

```sh
aws eks list-access-entries --cluster-name my-cluster
```

This command will output the access entries associated with your cluster, including the IAM role and the policies attached.

##### Describe IAM Role

To check the IAM policies attached to the EKS cluster IAM role, use the following command:

```sh
aws iam list-attached-role-policies --role-name <IAM_ROLE_NAME>
```

Replace `<IAM_ROLE_NAME>` with the name of your IAM role. This command will list all the policies attached to the specified IAM role.

#### Closing Statement

Managing AWS EKS access policies using Terraform and OpenTofu simplifies the process of setting up and maintaining your Kubernetes clusters. By using both AWS IAM policies and Kubernetes RBAC, you can achieve a resilient and flexible access control system. This approach allows you to centrally manage permissions through AWS while also providing fine-grained control within the Kubernetes cluster.
