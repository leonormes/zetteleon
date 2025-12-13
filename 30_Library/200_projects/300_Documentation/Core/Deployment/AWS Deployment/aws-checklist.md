---
aliases: []
confidence: 
created: 2025-02-07T12:57:56Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:51Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, ff_deploy]
title: aws-checklist
type: documentation
uid: 
updated: 
version:
---

## AWS Customer Checklist

### Prerequisites

1. AWS Account to deploy to
2. A terraform service account user assigned to our terraform-policy role definition
3. API key credentials for the terraform service account user
4. The region to deploy to
5. The FITFILE DevOps engineers responsible for deployment need to have access to the AWS Account

### Terraform Policy Definition

The following IAM policy defines the permissions required for the terraform service account:

```json
{
  "Version": "2012-10-17",
  "Statement":
    {
      "Effect": "Allow",
      "Action":
        "kms:CreateAlias",
        "kms:CreateGrant",
        "kms:CreateKey",
        "kms:DeleteAlias",
        "kms:DescribeKey",
        "kms:DisableKey",
        "kms:EnableKey",
        "kms:EnableKeyRotation",
        "kms:GetKeyPolicy",
        "kms:GetKeyRotationStatus",
        "kms:GetParametersForImport",
        "kms:ImportKeyMaterial",
        "kms:ListAliases",
        "kms:ListGrants",
        "kms:ListResourceTags",
        "kms:PutKeyPolicy",
        "kms:ReplicateKey",
        "kms:RevokeGrant",
        "kms:ScheduleKeyDeletion",
        "kms:TagResource",
        "kms:UntagResource",
        "kms:UpdateAlias",
        "kms:UpdateKeyDescription",
        "network-firewall:",
        "iam:ListEntitiesForPolicy",
        "iam:CreateRole",
        "iam:CreateInstanceProfile",
        "iam:DeleteRole",
        "iam:DeleteInstanceProfile",
        "iam:AttachRolePolicy",
        "iam:DeleteRolePolicy",
        "iam:DetachRolePolicy"
      ],
      "Resource": ""
    },
    {
      "Effect": "Allow",
      "Action":
        "ec2:AllocateAddress",
        "ec2:AssignPrivateNatGatewayAddress",
        "ec2:AssociateAddress",
        "ec2:AssociateDhcpOptions",
        "ec2:AssociateNatGatewayAddress",
        "ec2:AssociateRouteTable",
        "ec2:AssociateSubnetCidrBlock",
        "ec2:AssociateVpcCidrBlock",
        "ec2:AttachInternetGateway",
        "ec2:AttachVpnGateway",
        "ec2:AuthorizeSecurityGroupEgress",
        "ec2:AuthorizeSecurityGroupIngress",
        "ec2:CreateCustomerGateway",
        "ec2:CreateDefaultVpc",
        "ec2:CreateDhcpOptions",
        "ec2:CreateEgressOnlyInternetGateway",
        "ec2:CreateFlowLogs",
        "ec2:CreateInternetGateway",
        "ec2:CreateLaunchTemplate",
        "ec2:CreateNatGateway",
        "ec2:CreateNetworkAcl",
        "ec2:CreateNetworkAclEntry",
        "ec2:CreateRoute",
        "ec2:CreateRouteTable",
        "ec2:CreateSecurityGroup",
        "ec2:CreateSubnet",
        "ec2:CreateTags",
        "ec2:CreateVPC",
        "ec2:CreateVpcEndpoint",
        "ec2:CreateVpnGateway",
        "ec2:DeleteCustomerGateway",
        "ec2:DeleteDhcpOptions",
        "ec2:DeleteEgressOnlyInternetGateway",
        "ec2:DeleteFlowLogs",
        "ec2:DeleteInternetGateway",
        "ec2:DeleteKeyPair",
        "ec2:DeleteNatGateway",
        "ec2:DeleteNetworkAcl",
        "ec2:DeleteNetworkAclEntry",
        "ec2:DeleteVpcEndpoints",
        "ec2:DeleteRoute",
        "ec2:DeleteRouteTable",
        "ec2:DeleteSecurityGroup",
        "ec2:DeleteSubnet",
        "ec2:DeleteTags",
        "ec2:DeleteVPC",
        "ec2:DeleteVpnGateway",
        "ec2:DescribeAccountAttributes",
        "ec2:DescribeAddresses",
        "ec2:DescribeAddressesAttribute",
        "ec2:DescribeAvailabilityZones",
        "ec2:DescribeCustomerGateways",
        "ec2:DescribeDhcpOptions",
        "ec2:DescribeEgressOnlyInternetGateways",
        "ec2:DescribeFlowLogs",
        "ec2:DescribeImages",
        "ec2:DescribeInstanceAttribute",
        "ec2:DescribeInstanceCreditSpecifications",
        "ec2:DescribeInstanceTypes",
        "ec2:DescribeInstances",
        "ec2:DescribeInternetGateways",
        "ec2:DescribeKeyPairs",
        "ec2:DescribeLaunchTemplateVersions",
        "ec2:DescribeLaunchTemplates",
        "ec2:DescribeNatGateways",
        "ec2:DescribeNetworkAcls",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DescribePrefixLists",
        "ec2:DescribeRouteTables",
        "ec2:DescribeSecurityGroupRules",
        "ec2:DescribeSecurityGroups",
        "ec2:DescribeSubnets",
        "ec2:DescribeTags",
        "ec2:DescribeVolumes",
        "ec2:DescribeVpcAttribute",
        "ec2:DescribeVpcEndpointServices",
        "ec2:DescribeVpcEndpoints",
        "ec2:DescribeVpcs",
        "ec2:DescribeVpnGateways",
        "ec2:DetachInternetGateway",
        "ec2:DetachVpnGateway",
        "ec2:DisableVgwRoutePropagation",
        "ec2:DisassociateAddress",
        "ec2:DisassociateNatGatewayAddress",
        "ec2:DisassociateRouteTable",
        "ec2:DisassociateSubnetCidrBlock",
        "ec2:DisassociateVpcCidrBlock",
        "ec2:EnableVgwRoutePropagation",
        "ec2:ImportKeyPair",
        "ec2:ModifyInstanceAttribute",
        "ec2:ModifySubnetAttribute",
        "ec2:ModifyVpcAttribute",
        "ec2:ModifyVpcTenancy",
        "ec2:ReleaseAddress",
        "ec2:ReplaceNetworkAclEntry",
        "ec2:ReplaceNetworkAclAssociation",
        "ec2:ReplaceRoute",
        "ec2:ReplaceRouteTableAssociation",
        "ec2:RevokeSecurityGroupEgress",
        "ec2:RevokeSecurityGroupIngress",
        "ec2:RunInstances",
        "ec2:StartInstances",
        "ec2:StopInstances",
        "ec2:TerminateInstances",
        "ec2:UnassignPrivateNatGatewayAddress",
        "ec2:CreateNetworkInterface",
        "ec2:DeleteNetworkInterface",
        "ec2:AttachNetworkInterface",
        "ec2:DetachNetworkInterface",
        "ec2:ModifyNetworkInterfaceAttribute",
        "ec2:ResetNetworkInterfaceAttribute",
        "elasticloadbalancing:DescribeTags",
        "route53:",
        "elasticloadbalancing:DescribeLoadBalancerAttributes",
        "elasticloadbalancing:DescribeInstanceHealth",
        "elasticloadbalancing:DescribeLoadBalancerPolicies",
        "elasticloadbalancing:DescribeLoadBalancerPolicyTypes"
      ],
      "Resource": ""
    },
    {
      "Effect": "Allow",
      "Action":
        "eks:AssociateAccessPolicy",
        "eks:AssociateIdentityProviderConfig",
        "eks:CreateAccessEntry",
        "eks:CreateAddon",
        "eks:CreateCluster",
        "eks:CreatePodIdentityAssociation",
        "eks:CreateNodegroup",
        "eks:DeleteAccessEntry",
        "eks:DeleteAddon",
        "ec2:DeleteLaunchTemplate",
        "eks:DeleteNodegroup",
        "eks:DeleteCluster",
        "eks:DeletePodIdentityAssociation",
        "eks:DescribeAccessEntry",
        "eks:DescribeAddon",
        "eks:DescribeAddonVersions",
        "eks:DescribeCluster",
        "eks:DescribeNodegroup",
        "eks:DescribeIdentityProviderConfig",
        "eks:DescribeUpdate",
        "eks:DisassociateIdentityProviderConfig",
        "eks:DisassociateAccessPolicy",
        "eks:ListAddons",
        "eks:ListAssociatedAccessPolicies",
        "eks:ListTagsForResource",
        "eks:TagResource",
        "eks:UpdateNodegroupConfig",
        "eks:UntagResource",
        "eks:UpdateAccessEntry",
        "eks:UpdateAddon",
        "eks:UpdateClusterConfig"
      ],
      "Resource": ""
    },
    {
      "Effect": "Allow",
      "Action":
        "iam:AddRoleToInstanceProfile",
        "iam:AttachRolePolicy",
        "iam:CreateInstanceProfile",
        "iam:CreateOpenIDConnectProvider",
        "iam:CreatePolicy",
        "iam:CreateRole",
        "iam:CreateServiceLinkedRole",
        "iam:DeleteInstanceProfile",
        "iam:DeleteOpenIDConnectProvider",
        "iam:DeletePolicy",
        "iam:DeleteRole",
        "iam:DeleteRolePermissionsBoundary",
        "iam:DeleteRolePolicy",
        "iam:DetachRolePolicy",
        "iam:GetInstanceProfile",
        "iam:GetOpenIDConnectProvider",
        "iam:GetPolicy",
        "iam:GetPolicyVersion",
        "iam:GetRole",
        "iam:GetRolePolicy",
        "iam:ListAttachedRolePolicies",
        "iam:ListInstanceProfilesForRole",
        "iam:ListPolicyVersions",
        "iam:ListRolePolicies",
        "iam:PassRole",
        "iam:PutRolePermissionsBoundary",
        "iam:PutRolePolicy",
        "iam:RemoveRoleFromInstanceProfile",
        "iam:TagInstanceProfile",
        "iam:TagOpenIDConnectProvider",
        "iam:TagPolicy",
        "iam:TagRole",
        "iam:UntagInstanceProfile",
        "iam:UntagOpenIDConnectProvider",
        "iam:UntagPolicy",
        "iam:UntagRole",
        "iam:UpdateOpenIDConnectProviderThumbprint",
        "iam:UpdateRoleDescription",
        "network-firewall:",
        "logs:ListLogDeliveries"
      ],
      "Resource": ""
    }
  ]
}
```
