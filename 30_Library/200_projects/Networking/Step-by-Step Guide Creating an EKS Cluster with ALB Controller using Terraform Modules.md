---
aliases: []
author: ["[[Navya A]]"]
confidence: 
created: 2025-03-27T09:48:25Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source: https://navyadevops.hashnode.dev/step-by-step-guide-creating-an-eks-cluster-with-alb-controller-using-terraform-modules
source_of_truth: []
status: 
tags: [gateway, ingress, k8s, networking]
title: Step-by-Step Guide Creating an EKS Cluster with ALB Controller using Terraform Modules
type: download
uid: 
updated: 
version: 
---

## Introduction

Welcome to our in-depth blog tutorial, where we'll walk you through the process of building an Amazon Elastic Kubernetes Service (EKS) cluster using Terraform modules. If you're eager to harness the power of Kubernetes on AWS with a structured and scalable approach, you're in the right place.

In this step-by-step guide, we'll cover everything from creating a Virtual Private Cloud (VPC) to deploying an AWS Load Balancer Controller, ensuring you have a robust and well-architected EKS cluster. So, let's embark on this journey together and demystify the process of setting up, scaling, and optimizing your Kubernetes environment.

*==You can find the resource in my Github repo:==* [***==GitHub==***](https://github.com/NavyaDeveloper/EKS_Terraform_with_ALB)

![Creating AWS EKS Cluster using Terraform | by Sushant Kapare | Medium](https://miro.medium.com/v2/resize:fit:1400/0*n-aSCw9JHc6aTO3J)

## Key Steps Covered

### 1\. VPC Creation

We kick things off by establishing a secure foundation – creating a VPC from scratch using Terraform modules. This sets the stage for a resilient and isolated network environment tailored for your EKS cluster.

### 2\. EKS Cluster Provisioning

With the VPC in place, we delve into provisioning the EKS cluster itself. Harnessing the power of Terraform modules simplifies this process, offering a modular and efficient Infrastructure as Code (IaC) approach.

### 3\. Adding Users to EKS

Discover how to extend access to your EKS cluster by modifying the `aws-auth` ConfigMap. We guide you through creating an IAM role, granting full access to the Kubernetes API, and allowing users to assume this role for EKS access.

### 4\. Automatic Scaling with Cluster-Autoscaler

Ensure the scalability of your EKS cluster with a detailed walkthrough on deploying the cluster-autoscaler. Leveraging both plain YAML and the kubectl Terraform provider, this solution dynamically adjusts cluster nodes based on resource utilization.

### 5\. AWS Load Balancer Controller Deployment

Using the Helm provider, we explore the deployment of the AWS Load Balancer Controller – a critical component for managing and configuring load balancers in your EKS cluster. This step optimizes the distribution of incoming traffic across your applications.

### 6\. Ingress Resource Creation

Cap it off by creating a test Ingress resource. This allows you to validate the functionality of the AWS Load Balancer Controller by effectively routing external traffic to the designated services within the EKS cluster.

By the end of this tutorial, you'll have gained valuable insights into setting up and managing an EKS cluster using Terraform modules. Each step is meticulously explained and demonstrated, empowering you to replicate the process for your own projects. Let's dive in and build a resilient Kubernetes environment on AWS!

## Creating AWS VPC Using Terraform

In this segment, we'll dive into the process of setting up an Amazon Virtual Private Cloud (VPC) using Terraform. A VPC provides a logically isolated section of the AWS Cloud where you can launch AWS resources securely. We'll utilize the `terraform-aws-modules/vpc` module to streamline this setup.

## Configuring Terraform Provider and Versions

Firstly, we need to configure the AWS Terraform provider and specify the required versions. The code snippet below sets up the provider for AWS, along with constraints for kubectl and helm providers. Adjust the region as needed.

```hcl
# terraform/provider.tf

provider "aws" {
  region = "us-east-1"  # Change to your desired region
}

terraform {
  required_providers {
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.14.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.6.0"
    }
  }

  required_version = "~> 1.0"
}
```

## Defining VPC Parameters

The next step involves defining the parameters for our VPC. We'll use the `terraform-aws-modules/vpc/aws` module for this purpose. The example below creates a VPC named "main" with a specified CIDR range. It spans two availability zones (us-east-1a and us-east-1b).

```hcl
# terraform/vpc.tf

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.14.3"

  name = "main"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.0.0/19", "10.0.32.0/19"]
  public_subnets  = ["10.0.64.0/19", "10.0.96.0/19"]

  enable_nat_gateway     = true
  single_nat_gateway     = true
  one_nat_gateway_per_az = false

  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Environment = "Dev"
  }
}
```

Explanation of key parameters:

- `name`: The name of the VPC.
- `cidr`: The CIDR block for the VPC.
- `azs`: Availability zones to span.
- `private_subnets` and `public_subnets`: Define the subnets for private and public resources.
- `enable_nat_gateway`: Enable NAT gateway for private subnets.
- `enable_dns_hostnames` and `enable_dns_support`: Enable DNS hostnames and support.

## Creating Amazon EKS Cluster Using Terraform

Now that we have set up our VPC, let's proceed to create an Amazon Elastic Kubernetes Service (EKS) cluster using Terraform. We'll name our cluster "my-eks" and specify the latest supported version by AWS, which is 1.26 at the moment. Additionally, we'll enable both private and public endpoints for flexibility in accessing the cluster.

## Configuring EKS Cluster Parameters

In the code snippet below, we define the parameters for our EKS cluster. We pull the VPC ID and private subnets dynamically from the VPC module we previously created. IAM Roles for Service Accounts (IRSA) is enabled for more secure access control.

```hcl
# terraform/eks.tf

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "18.29.0"

  cluster_name    = "my-eks"
  cluster_version = "1.26"

  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = true

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  enable_irsa = true

  eks_managed_node_group_defaults = {
    disk_size = 50
  }

  eks_managed_node_groups = {
    nodes = {
      min_size     = 1
      max_size     = 1
      desired_size = 1

      instance_types = ["t3.medium"]
    }
  }

  tags = {
    Environment = "testing"
  }
}
```

Explanation of key parameters:

- `cluster_name`: The name of the EKS cluster.
- `cluster_version`: The desired Kubernetes version.
- `cluster_endpoint_private_access` and `cluster_endpoint_public_access`: Enabling private and public access to the cluster.
- `vpc_id` and `subnet_ids`: Dynamically pulling VPC information.
- `enable_irsa`: Enabling IAM Roles for Service Accounts.
- `eks_managed_node_group_defaults` and `eks_managed_node_groups`: Configuring managed node groups with specific instance types.

## Running Terraform

After defining the EKS cluster parameters, run the following commands in your terminal:

```hcl
terraform init
terraform apply
```

The creation process usually takes up to 10 minutes. Once completed, update the Kubernetes context to connect to the cluster:

```hcl
aws eks update-kubeconfig --name my-eks --region us-east-1
```

Verify successful access to the EKS cluster:

```hcl
kubectl get nodes
```

## Adding IAM User & Role to EKS

In this section, we'll explore how to grant access to Kubernetes workloads for IAM users and IAM roles by configuring the `aws-auth` config map in the `kube-system` namespace. Initially, only the user who created the cluster can access and modify this config map. To extend access to team members, we have two options, and in this example, we'll demonstrate the second, preferred approach.

## 1\. Allowing EKS Access IAM Policy

Firstly, let's create an IAM policy named "allow-eks-access" that grants permission for the `eks:DescribeCluster` action. This action is crucial for updating the Kubernetes context and gaining initial access to the cluster.

```hcl
# terraform/iam.tf

module "allow_eks_access_iam_policy" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-policy"
  version = "5.3.1"

  name          = "allow-eks-access"
  create_policy = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "eks:DescribeCluster",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}
```

## 2\. Creating IAM Role for EKS Access

Next, let's create an IAM role named "eks-admin" that will be associated with the `system:masters` RBAC group in Kubernetes, providing full access to the Kubernetes API.

```hcl
# terraform/iam.tf

module "eks_admins_iam_role" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-assumable-role"
  version = "5.3.1"

  role_name         = "eks-admin"
  create_role       = true
  role_requires_mfa = false

  custom_role_policy_arns = [module.allow_eks_access_iam_policy.arn]

  trusted_role_arns = [
    "arn:aws:iam::${module.vpc.vpc_owner_id}:root"
  ]
}
```

## 3\. Creating IAM User

Let's create a test IAM user named "user1" with disabled access key and login profile creation. Access keys and login profiles will be generated manually from the AWS Management Console.

```hcl
# terraform/iam.tf

module "user1_iam_user" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-user"
  version = "5.3.1"

  name                          = "user1"
  create_iam_access_key         = false
  create_iam_user_login_profile = false

  force_destroy = true
}
```

## 4\. IAM Policy to Allow Assuming EKS Admin Role

Create an IAM policy that allows the IAM user to assume the "eks-admin" IAM role.

```hcl
# terraform/iam.tf

module "allow_assume_eks_admins_iam_policy" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-policy"
  version = "5.3.1"

  name          = "allow-assume-eks-admin-iam-role"
  create_policy = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "sts:AssumeRole",
        ]
        Effect   = "Allow"
        Resource = module.eks_admins_iam_role.iam_role_arn
      },
    ]
  })
}
```

## 5\. Creating IAM Group and Adding User

Create an IAM group named "eks-admin" and associate the IAM user "user1" with it. Attach the policy that allows assuming the "eks-admin" IAM role.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1705680396499/6786354d-f7e2-4268-9ae5-9c9023c7b1c6.png?auto=compress,format&format=webp)

```hcl
# terraform/iam.tf

module "eks_admins_iam_group" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-group-with-policies"
  version = "5.3.1"

  name                              = "eks-admin"
  attach_iam_self_management_policy = false
  create_group                      = true
  group_users                       = [module.user1_iam_user.iam_user_name]
  custom_group_policy_arns          = [module.allow_assume_eks_admins_iam_policy.arn]
}
```

After defining these IAM entities, run `terraform init` and `terraform apply` to create them. Now, let's generate new credentials for "user1" and create a local AWS profile.

```bash
aws configure --profile user1
```

Verify access to AWS services with the "user1" profile.

```bash
aws sts get-caller-identity --profile user1
```

To allow "user1" to assume the "eks-admin" IAM role, create another AWS profile with the role name.

```ini
# ~/.aws/config

[profile eks-admin]
role_arn        = arn:aws:iam::YOUR_ACCOUNT_ID:role/eks-admin
source_profile  = user1
```

Test if you can assume the "eks-admin" IAM role.

```bash
aws sts get-caller-identity --profile eks-admin
```

Now, update the Kubernetes config to use the "eks-admin" IAM role.

```bash
aws eks update-kubeconfig --name my-eks --region us-east-1 --profile eks-admin
```

Run `terraform apply` again to authorize Terraform to access the Kubernetes API and modify the `aws-auth` config map.

```hcl
# terraform/eks.tf

provider "kubernetes" {
  host                   = data.aws_eks_cluster.default.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.default.certificate_authority[0].data)

  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    args        = ["eks", "get-token", "--cluster-name", data.aws_eks_cluster.default.id]
    command     = "aws"
  }
}
```

Now, you can run `terraform apply` again to update the config map and grant access to the "eks-admin" IAM role. Verify successful access to the cluster.

```bash
kubectl auth can-i "*" "*"
```

You've now added an IAM user and role to your EKS cluster, extending access beyond the initial creator.

## Deploying Cluster Autoscaler and AWS Load Balancer Controller

In this section, we'll proceed to deploy the Cluster Autoscaler and the AWS Load Balancer Controller to enhance the capabilities of our Kubernetes cluster.

## Deploying Cluster Autoscaler

### 1\. IAM Role for Cluster Autoscaler

Let's start by creating an IAM role for the Cluster Autoscaler using Terraform. The IAM role needs permissions to access and modify AWS Auto Scaling Groups.

```hcl
# terraform/autoscaler-iam.tf

module "cluster_autoscaler_irsa_role" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "5.3.1"

  role_name                        = "cluster-autoscaler"
  attach_cluster_autoscaler_policy = true
  cluster_autoscaler_cluster_ids   = [module.eks.cluster_id]

  oidc_providers = {
    ex = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["kube-system:cluster-autoscaler"]
    }
  }
}
```

### 2\. Deploying Cluster Autoscaler to Kubernetes

Now, let's deploy the Cluster Autoscaler to Kubernetes using plain YAML configurations. We'll use the Kubernetes provider to apply these configurations.

```hcl
# terraform/autoscaler-manifest.tf

provider "kubectl" {
  host                   = data.aws_eks_cluster.default.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.default.certificate_authority[0].data)
  load_config_file       = false

  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    args        = ["eks", "get-token", "--cluster-name", data.aws_eks_cluster.default.id]
    command     = "aws"
  }
}

resource "kubectl_manifest" "service_account" {
  yaml_body = <<-EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    k8s-addon: cluster-autoscaler.addons.k8s.io
    k8s-app: cluster-autoscaler
  name: cluster-autoscaler
  namespace: kube-system
  annotations:
    eks.amazonaws.com/role-arn: ${module.cluster_autoscaler_irsa_role.iam_role_arn}
EOF
}

resource "kubectl_manifest" "role" {
  yaml_body = <<-EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: cluster-autoscaler
  namespace: kube-system
  labels:
    k8s-addon: cluster-autoscaler.addons.k8s.io
    k8s-app: cluster-autoscaler
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["create","list","watch"]
  - apiGroups: [""]
    resources: ["configmaps"]
    resourceNames: ["cluster-autoscaler-status", "cluster-autoscaler-priority-expander"]
    verbs: ["delete", "get", "update", "watch"]
EOF
}

resource "kubectl_manifest" "role_binding" {
  yaml_body = <<-EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: cluster-autoscaler
  namespace: kube-system
  labels:
    k8s-addon: cluster-autoscaler.addons.k8s.io
    k8s-app: cluster-autoscaler
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: cluster-autoscaler
subjects:
  - kind: ServiceAccount
    name: cluster-autoscaler
    namespace: kube-system
EOF
}

resource "kubectl_manifest" "cluster_role" {
  yaml_body = <<-EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-autoscaler
  labels:
    k8s-addon: cluster-autoscaler.addons.k8s.io
    k8s-app: cluster-autoscaler
rules:
  - apiGroups: [""]
    resources: ["events", "endpoints"]
    verbs: ["create", "patch"]
  - apiGroups: [""]
    resources: ["pods/eviction"]
    verbs: ["create"]
  - apiGroups: [""]
    resources: ["pods/status"]
    verbs: ["update"]
  - apiGroups: [""]
    resources: ["endpoints"]
    resourceNames: ["cluster-autoscaler"]
    verbs: ["get", "update"]
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["watch", "list", "get", "update"]
  - apiGroups: [""]
    resources:
      - "namespaces"
      - "pods"
      - "services"
      - "replicationcontrollers"
      - "persistentvolumeclaims"
      - "persistentvolumes"
    verbs: ["watch", "list", "get"]
  - apiGroups: ["extensions"]
    resources: ["replicasets", "daemonsets"]
    verbs: ["watch", "list", "get"]
  - apiGroups: ["policy"]
    resources: ["poddisruptionbudgets"]
    verbs: ["watch", "list"]
  - apiGroups: ["apps"]
    resources: ["statefulsets", "replicasets", "daemonsets"]
    verbs: ["watch", "list", "get"]
  - apiGroups: ["storage.k8s.io"]
    resources: ["storageclasses", "csinodes", "csidrivers", "csistoragecapacities"]
    verbs: ["watch", "list", "get"]
  - apiGroups: ["batch", "extensions"]
    resources: ["jobs"]
    verbs: ["get", "list", "watch", "patch"]
  - apiGroups: ["coordination.k8s.io"]
    resources: ["leases"]
    verbs: ["create"]
  - apiGroups: ["coordination.k8s.io"]
    resourceNames: ["cluster-autoscaler"]
    resources: ["leases"]
    verbs: ["get", "update"]
EOF
}

resource "kubectl_manifest" "cluster_role_binding" {
  yaml_body = <<-EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-autoscaler
  labels:
    k8s-addon: cluster-autoscaler.addons.k8s.io
    k8s-app: cluster-autoscaler
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-autoscaler
subjects:
  - kind: ServiceAccount
    name: cluster-autoscaler
    namespace: kube-system
EOF
}

resource "kubectl_manifest" "deployment" {
  yaml_body = <<-EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
  labels:
    app: cluster-autoscaler
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cluster-autoscaler
  template:
    metadata:
      labels:
        app: cluster-autoscaler
    spec:
      priorityClassName: system-cluster-critical
      securityContext:
        runAsNonRoot: true
        runAsUser: 65534
        fsGroup: 65534
      serviceAccountName: cluster-autoscaler
      containers:
        - image: registry.k8s.io/autoscaling/cluster-autoscaler:v1.26.2
          name: cluster-autoscaler
          resources:
            limits:
              cpu: 100m
              memory: 600Mi
            requests:
              cpu: 100m
              memory: 600Mi
          command:
            - ./cluster-autoscaler
            - --v=4
            - --stderrthreshold=info
            - --cloud-provider=aws
            - --skip-nodes-with-local-storage=false
            - --expander=least-waste
            - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/${module.eks.cluster_id}
          volumeMounts:
            - name: ssl-certs
              mountPath: /etc/ssl/certs/ca-certificates.crt
              readOnly: true
      volumes:
        - name: ssl-certs
          hostPath:
            path: "/etc/ssl/certs/ca-bundle.crt"
EOF
}
```

Apply these changes:

```bash
terraform init
terraform apply
```

Verify that the autoscaler is running:

```bash
kubectl get pods -n kube-system
```

### 3\. Testing Autoscaler with Nginx Deployment

To test the autoscaler, let's create an Nginx deployment:

```yaml
# k8s/nginx.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 4
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        resources:
          requests:
            cpu: "1"
```

Apply the deployment:

```bash
kubectl apply -f k8s/nginx.yaml
```

Watch the nodes to see if more are added:

```bash
watch -n 1 -t kubectl get nodes
```

## Deploying AWS Load Balancer Controller

### 1\. Helm Provider Configuration

Configure the Helm provider in Terraform:

```hcl
# terraform/helm-provider.tf

provider "helm" {
  kubernetes {
    host                   = data.aws_eks_cluster.default.endpoint
    cluster_ca_certificate = base64decode(data.aws_eks_cluster.default.certificate_authority[0].data)
    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      args        = ["eks", "get-token", "--cluster-name", data.aws_eks_cluster.default.id]
      command     = "aws"
    }
  }
}
```

### 2\. IAM Role for Load Balancer Controller

Create an IAM role for the AWS Load Balancer Controller with the necessary permissions:

```hcl
# terraform/helm-load-balancer-controller.tf

module "aws_load_balancer_controller_irsa_role" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "5.3.1"

  role_name = "aws-load-balancer-controller"

  attach_load_balancer_controller_policy = true

  oidc_providers = {
    ex = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["kube-system:aws-load-balancer-controller"]
    }
  }
}
```

### 3\. Deploying AWS Load Balancer Controller with Helm

Now, deploy the AWS Load Balancer Controller using Helm:

```hcl
# terraform/helm-load-balancer-controller.tf

resource "helm_release" "aws_load_balancer_controller" {
  name = "aws-load-balancer-controller"

  repository = "https://aws.github.io/eks-charts"
  chart      = "aws-load-balancer-controller"
  namespace  = "kube-system"
  version    = "1.4.4"

  set {
    name  = "replicaCount"
    value = 1
  }

  set {
    name  = "clusterName"
    value = module.eks.cluster_id
  }

  set {
    name  = "serviceAccount.name"
    value = "aws-load-balancer-controller"
  }

  set {
    name  = "serviceAccount.annotations.eks\\.amazonaws\\.com/role-arn"
    value = module.aws_load_balancer_controller_irsa_role.iam_role_arn
  }
}
```

The load balancer controller uses tags to discover subnets in which it can create load balancers. We also need to update terraform vpc module to include them. It uses an `elb` tag to deploy public load balancers to expose services to the internet and `internal-elb` for the private load balancers to expose services only within your VPC.

```hcl
#terraform/vpc.tf
  public_subnet_tags = {
    "kubernetes.io/role/elb" = "1"
  }
  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = "1"
  }
```

The last change that we need to make in our EKS cluster is to allow access from the EKS control plane to the `webhook` port of the AWS load balancer controller.

```hcl
terraform/vpc.tf  

node_security_group_additional_rules = {
    ingress_allow_access_from_control_plane = {
      type                          = "ingress"
      protocol                      = "tcp"
      from_port                     = 9443
      to_port                       = 9443
      source_cluster_security_group = true
      description                   = "Allow access from control plane to webhook port of AWS load balancer controller"
    }
  }
```

Apply these changes:

```bash
terraform init
terraform apply
```

Verify that the controller is running:

```bash
kubectl get pods -n kube-system
```

You can watch logs for more details:

```bash
kubectl logs -f -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller
```

### 4\. Testing with Echo Server Deployment and Ingress

Create an Echo server deployment with Ingress:

```yaml
# k8s/echoserver.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: echoserver
  namespace: default
spec:
  selector:
    matchLabels:
      app: echoserver
  replicas: 1
  template:
    metadata:
      labels:
        app: echoserver
    spec:
      containers:
      - image: k8s.gcr.io/e2e-test-images/echoserver:2.5
        name: echoserver
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: echoserver
  namespace: default
spec:
  ports:
  - port: 8080
    protocol: TCP
  type: NodePort
  selector:
    app: echoserver
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: echoserver
  namespace: default
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
spec:
  ingressClassName: alb
  rules:
    - http:
        paths:
          - path: /
            pathType: Exact
            backend:
              service:
                name: echoserver
                port:
                  number: 8080
```

Apply the deployment:

```bash
kubectl apply -f k8s/echoserver.yaml
```

Retrieve the application load balancer DNS name:

```bash
kubectl get ingress
```

Now you can access application using DNS of ALB created....

Congratulations! You've successfully deployed the Cluster Autoscaler and the AWS Load Balancer Controller to your EKS cluster, enabling automatic scaling and load balancing for your workloads.

## Summary

In this comprehensive tutorial, we navigated through the intricacies of setting up an Amazon EKS cluster on AWS using Terraform modules. Covering key steps from VPC creation to deploying essential components like the AWS Load Balancer Controller and Cluster Autoscaler, we ensured a robust and well-architected Kubernetes environment. The detailed explanations and code snippets empower users to understand each phase thoroughly. Beyond the core setup, we extended EKS access to IAM users and roles, demonstrating secure and scalable cluster management. By testing with Nginx deployments and Echo servers, we validated the effectiveness of the autoscaling and load balancing capabilities, enhancing the overall resilience of the Kubernetes environment.
