# AWS FF Install

# AWS FF Install

First, the user needs access to the resources created.
The terraform cloud service principle uses dynamic creds.
Steps for the Terraform;

- <code>terraform init --upgrade</code>

- <code>terraform apply -target="module.vpc" -auto-approve</code>

- <code>terraform apply -target="module.vpc_endpoints" -auto-approve</code>

- <code>terraform apply -target="module.eks" -auto-approve</code>

- <code>terraform apply -auto-approve</code>

- This ensure the right things are up and running before the EKS.

It would be good to separate the data for the config from the code. What are the data?

There is the code that deploys our stuff, then there is the data that is unique to each deployment.

- The deployment key.

- IP Ranges

- Cloud Provider

IP Ranges
Names

- Network names

- Deployment names

- Cluster names

- Secrets names

Secrets
Env Vars
There is the data for the config for each k8s resource we use.
Source = "[app.terraform.io/FITFILE-Platforms/eks/aws](http://app.terraform.io/FITFILE-Platforms/eks/aws)"

```sh
# Get all namespaces
kubectl get namespaces

# List all resources within a namespace (replace <namespace> with the actual namespace name)
kubectl get all -n <namespace>

# Get Deployments
kubectl get deployments -A -o yaml  # "-A" for all namespaces

# Get Services
kubectl get services -A -o yaml

# Get Ingresses
kubectl get ingresses -A -o yaml

# Get ConfigMaps
kubectl get configmaps -A -o yaml

# Get Secrets
kubectl get secrets -A -o yaml

# Get Persistent Volume Claims (PVCs)
kubectl get pvc -A -o yaml

# Get Persistent Volumes (PV)
kubectl get pv -A -o yaml

# Get StatefulSets, DaemonSets, Jobs (if applicable)
kubectl get statefulsets -A -o yaml
kubectl get daemonsets -A -o yaml
kubectl get jobs -A -o yaml
```

So far, I haven't had to update the aws/eks cluster.

## Problems

When I tried replacing the VPC terraform tried to destroy the VPC and re-deploy. It seemed to take far too long (14m). I looked and tried manually deleting the VPC but the VPC_endpoints were using it. I need to teardown the VPC_endpoints!
Terraform struggled all the way! I had to manually delete the endpoints, then the VPCs.

Came across a problem with the permissions on the KMS. The Terraform SP didn't have permissions define on the resource KMS. Even though I had given the permission in the role it need them on the resources as well.

[Aws Permissions](Aws%20Permissions)

## Terraform State

data.aws_availability_zones.available
data.aws_caller_identity.current
data.aws_iam_policy_document.assume_role
data.aws_iam_policy_document.bastion_trust_policy
data.aws_subnets.public

aws_default_route_table.r
aws_default_security_group.s

aws_iam_instance_profile.bastion
aws_iam_role.bastion
aws_iam_role.fitfile
aws_iam_role_policy_attachment.AmazonSSMManagedInstanceCore
aws_iam_role_policy_attachment.fitfile-AmazonEKSClusterPolicy
aws_iam_role_policy_attachment.fitfile-AmazonEKSVPCResourceController

aws_key_pair.my_key

aws_security_group.bastion

aws_subnet.subnet1

module.eks.data.aws_caller_identity.current
module.eks.data.aws_eks_addon_version.this\["coredns"\]
module.eks.data.aws_eks_addon_version.this\["kube-proxy"\]
module.eks.data.aws_eks_addon_version.this\["vpc-cni"\]
module.eks.data.aws_iam_policy_document.assume_role_policy
module.eks.data.aws_iam_session_context.current
module.eks.data.aws_partition.current

module.eks.aws_ec2_tag.cluster_primary_security_group\["createdBy"\]
module.eks.aws_ec2_tag.cluster_primary_security_group\["git_file"\]
module.eks.aws_ec2_tag.cluster_primary_security_group\["git_modifiers"\]
module.eks.aws_ec2_tag.cluster_primary_security_group\["git_org"\]
module.eks.aws_ec2_tag.cluster_primary_security_group\["git_repo"\]
module.eks.aws_ec2_tag.cluster_primary_security_group\["yor_name"\]

module.eks.aws_eks_access_entry.this\["cluster_creator"\]

module.eks.aws_eks_access_policy_association.this\["cluster_creator_admin"\]

module.eks.aws_eks_cluster.this

module.eks.aws_iam_policy.cluster_encryption
module.eks.aws_iam_role.this
module.eks.aws_iam_role_policy_attachment.cluster_encryption
module.eks.aws_iam_role_policy_attachment.this\["AmazonEKSClusterPolicy"\]
module.eks.aws_iam_role_policy_attachment.this\["AmazonEKSVPCResourceController"\]

module.eks.aws_security_group.cluster
module.eks.aws_security_group.node
module.eks.aws_security_group_rule.cluster\["ingress_nodes_443"\]
module.eks.aws_security_group_rule.node\["egress_all"\]
module.eks.aws_security_group_rule.node\["ingress_cluster_443"\]
module.eks.aws_security_group_rule.node\["ingress_cluster_4443_webhook"\]
module.eks.aws_security_group_rule.node\["ingress_cluster_6443_webhook"\]
module.eks.aws_security_group_rule.node\["ingress_cluster_8443_webhook"\]
module.eks.aws_security_group_rule.node\["ingress_cluster_9443_webhook"\]
module.eks.aws_security_group_rule.node\["ingress_cluster_kubelet"\]
module.eks.aws_security_group_rule.node\["ingress_nodes_ephemeral"\]
module.eks.aws_security_group_rule.node\["ingress_self_coredns_tcp"\]
module.eks.aws_security_group_rule.node\["ingress_self_coredns_udp"\]

module.eks.time_sleep.this

module.vpc.aws_default_network_acl.this
module.vpc.aws_default_route_table.default
module.vpc.aws_default_security_group.this
module.vpc.aws_default_vpc.this
module.vpc.aws_route_table.private
module.vpc.aws_route_table.private
module.vpc.aws_route_table_association.private
module.vpc.aws_route_table_association.private

module.vpc.aws_subnet.private
module.vpc.aws_subnet.private

module.vpc.aws_vpc.this

module.vpc_endpoints.data.aws_vpc_endpoint_service.this\["autoscaling"\]
module.vpc_endpoints.data.aws_vpc_endpoint_service.this\["ec2"\]
module.vpc_endpoints.data.aws_vpc_endpoint_service.this\["ecr_api"\]
module.vpc_endpoints.data.aws_vpc_endpoint_service.this\["ecr_dkr"\]
module.vpc_endpoints.data.aws_vpc_endpoint_service.this\["elasticloadbalancing"\]
module.vpc_endpoints.data.aws_vpc_endpoint_service.this\["logs"\]
module.vpc_endpoints.data.aws_vpc_endpoint_service.this\["s3"\]
module.vpc_endpoints.data.aws_vpc_endpoint_service.this\["ssm"\]
module.vpc_endpoints.data.aws_vpc_endpoint_service.this\["sts"\]
module.vpc_endpoints.aws_security_group.this
module.vpc_endpoints.aws_security_group_rule.this\["ingress_https"\]
module.vpc_endpoints.aws_vpc_endpoint.this\["autoscaling"\]
module.vpc_endpoints.aws_vpc_endpoint.this\["ec2"\]
module.vpc_endpoints.aws_vpc_endpoint.this\["ecr_api"\]
module.vpc_endpoints.aws_vpc_endpoint.this\["ecr_dkr"\]
module.vpc_endpoints.aws_vpc_endpoint.this\["elasticloadbalancing"\]
module.vpc_endpoints.aws_vpc_endpoint.this\["logs"\]
module.vpc_endpoints.aws_vpc_endpoint.this\["s3"\]
module.vpc_endpoints.aws_vpc_endpoint.this\["ssm"\]
module.vpc_endpoints.aws_vpc_endpoint.this\["sts"\]

module.eks.module.eks_managed_node_group\["initial"\].data.aws_caller_identity.current
module.eks.module.eks_managed_node_group\["initial"\].data.aws_iam_policy_document.assume_role_policy
module.eks.module.eks_managed_node_group\["initial"\].data.aws_partition.current
module.eks.module.eks_managed_node_group\["initial"\].aws_iam_role.this
module.eks.module.eks_managed_node_group\["initial"\].aws_iam_role_policy_attachment.this\["AmazonEC2ContainerRegistryReadOnly"\]
module.eks.module.eks_managed_node_group\["initial"\].aws_iam_role_policy_attachment.this\["AmazonEKSWorkerNodePolicy"\]
module.eks.module.eks_managed_node_group\["initial"\].aws_iam_role_policy_attachment.this\["AmazonEKS_CNI_Policy"\]
module.eks.module.eks_managed_node_group\["initial"\].aws_launch_template.this

module.eks.module.kms.data.aws_caller_identity.current
module.eks.module.kms.data.aws_iam_policy_document.this
module.eks.module.kms.data.aws_partition.current
module.eks.module.kms.aws_kms_key.this

module.eks.module.eks_managed_node_group\["initial"\].module.user_data.null_resource.validate_cluster_service_cidr

[Open: Pasted image 20241001145603.png](b7ccbbd80202f8e4af96e071b6c768a5_MD5.jpeg)

![b7ccbbd80202f8e4af96e071b6c768a5_MD5.jpeg](b7ccbbd80202f8e4af96e071b6c768a5_MD5.jpeg)


[Open: Pasted image 20241001145640.png](3ec6333fbcacb128b984a356a84b0e9e_MD5.jpeg)

![3ec6333fbcacb128b984a356a84b0e9e_MD5.jpeg](3ec6333fbcacb128b984a356a84b0e9e_MD5.jpeg)

[Open: Pasted image 20241001145813.png](a1854069c3b65c70357356c16fd9e369_MD5.jpeg)

![a1854069c3b65c70357356c16fd9e369_MD5.jpeg](a1854069c3b65c70357356c16fd9e369_MD5.jpeg)

[Open: Pasted image 20241001145834.png](362e94bcb88b2ed2b92c629875a45290_MD5.jpeg)

![362e94bcb88b2ed2b92c629875a45290_MD5.jpeg](362e94bcb88b2ed2b92c629875a45290_MD5.jpeg)