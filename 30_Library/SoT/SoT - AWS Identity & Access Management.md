---
aliases: [AWS IAM]
conformant: false
created: 2026-04-05T10:30:00+00:00
last-synthesis: 2026-04-05
last_reviewed: null
modified: 2026-08-29T09:36:34+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-aws-identity-access-management
status: Active
synthesis-count: 1
tags: [aws, iam, security, sot]
title: SoT - AWS Identity & Access Management
type: sot
---

## Minimum Viable Understanding (MVU)

AWS Identity and Access Management (IAM) is a web service that helps you securely control access to AWS resources. You use IAM to control who is authenticated (signed in) and authorized (has permissions) to use resources.

---

## 1. Core Components

- IAM Users: Entities you create in AWS to represent the person or service that uses it to interact with AWS.
- IAM Groups: Collections of IAM users. You can use groups to specify permissions for multiple users.
- IAM Roles: Identities with permission policies that determine what the identity can and cannot do in AWS. Roles are intended to be assumable by anyone who needs them.
- Policies: JSON documents that define permissions. They can be identity-based or resource-based.

---

## 2. Advanced Permission Modeling

### A. Resource-Level Permissions

To limit the blast radius of a security breach, use resource-level permissions to restrict a principal's ability to manage only specific resources.

Example: Restricting Management to a Single IAM User

Instead of granting `iam:*` to all users, you can craft a policy that specifies the ARN (Amazon Resource Name) of the target user in the `Resource` element.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iam:GetUser",
                "iam:DeleteUser",
                "iam:AttachRolePolicy",
                "iam:DetachRolePolicy",
                "iam:ListAttachedRolePolicies"
            ],
            "Resource": [
                "arn:aws:iam::ACCOUNT_ID:user/TARGET_USER_NAME"
            ]
        },
        {
            "Effect": "Allow",
            "Action": "iam:ListRoles",
            "Resource": "*"
        }
    ]
}
```

### B. Implementation via Code (IaC)

Always use Infrastructure as Code (Terraform, CloudFormation) to manage IAM policies to ensure auditability and repeatability.

```hcl
resource "aws_iam_policy" "restricted_user_policy" {
  name        = "RestrictedUserPolicy"
  policy      = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["iam:GetUser", "iam:DeleteUser"]
        Resource = ["arn:aws:iam::ACCOUNT_ID:user/TARGET_USER_NAME"]
      }
    ]
  })
}
```

---

## 3. Best Practices

1. Follow Least Privilege: Grant only the permissions required to perform a task.
2. Use Roles for Applications: Instead of embedding AWS access keys in your application, use IAM Roles for EC2/EKS (IRSA).
3. MFA for Root/Admins: Enable Multi-Factor Authentication for the AWS root account and all administrative users.
4. Regularly Rotate Credentials: Automate the rotation of access keys and secrets.

---

## Related Knowledge

- [[SoT - Digital Identity]]
- [[SoT - Modern Authentication Standards]]
- [[SoT - Zero Trust Architecture]]
