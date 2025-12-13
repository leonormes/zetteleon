---
aliases: []
confidence: 
created: 2025-03-14T06:46:10Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [IAM]
title: Restricting IAM Permissions to a Single User in AWS Programmatically
type: 
uid: 
updated: 
version: 
---

You're aiming to implement resource-level permissions in AWS IAM to restrict a principal's ability to manage only a specific IAM user, rather than all users. This is a security best practice to limit the blast radius of any potential security breaches. Here's how you can achieve this programmatically:

## Understanding Resource-Level Permissions in IAM

IAM policies, written in JSON format, define permissions in AWS. They consist of statements that specify:

-   **Actions**: What actions are allowed or denied (e.g., `iam:CreateUser`, `iam:GetUser`).
-   **Resources**: Which AWS resources the actions apply to (e.g., a specific IAM user, an S3 bucket).
-   **Effect**: Whether the action is allowed (`Allow`) or denied (`Deny`).

Resource-level permissions allow you to control access at a granular level. Instead of granting permissions to all resources of a certain type (like all IAM users), you can restrict them to specific resources.

## Restricting Permissions to a Single IAM User

To restrict permissions to a single IAM user, you need to craft an IAM policy that specifies the **resource ARN (Amazon Resource Name)** of that specific user in the `Resource` element of the policy statement.

Here's a breakdown of how to construct such a policy and apply it programmatically:

### 1. Identify the IAM User ARN

First, you need the ARN of the specific IAM user you want to grant restricted permissions to. The ARN for an IAM user has the following format:

arn:aws:iam::\<aws-account-id\>:user/\<user-name\>

-   Replace `\<aws-account-id\>` with your AWS account ID.
-   Replace `\<user-name\>` with the name of the IAM user you want to target.

You can find the ARN of an existing IAM user in the AWS Management Console or programmatically using the AWS CLI or SDKs (e.g., `aws iam get-user --user-name \<user-name\>`).

### 2. Create an IAM Policy Document

You'll create an IAM policy document in JSON format that includes statements to allow the necessary actions (`GetUser`, `DeleteUser`, and actions related to role assignment) but restricts the `Resource` to the specific IAM user ARN you identified.

Here's an example policy document:

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
                "arn:aws:iam::YOUR_AWS_ACCOUNT_ID:user/USER_NAME_TO_RESTRICT_TO"
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

Explanation:

 - Version: Specifies the policy language version. 2012-10-17 is the latest version.
 - Statement: An array of statements that define permissions.
   - First Statement:
     - Effect: Allow: Grants permission.
     - Action: Lists the allowed IAM actions:
       - iam:GetUser: Allows getting details of the specific user.
       - iam:DeleteUser: Allows deleting the specific user.
       - iam:AttachRolePolicy: Allows attaching roles to the specific user.
       - iam:DetachRolePolicy: Allows detaching roles from the specific user.
       - iam:ListAttachedRolePolicies: Allows listing roles attached to the specific user.
     - Resource: Crucially, this is where you restrict the permissions. It specifies the ARN of the single IAM user that this statement applies to. Replace YOUR_AWS_ACCOUNT_ID and USER_NAME_TO_RESTRICT_TO with your actual AWS account ID and the target IAM username.
   - Second Statement:
     - Effect: Allow: Grants permission.
     - Action: iam:ListRoles: Allows listing all IAM roles in the account. This is often necessary for the principal to be able to select and attach roles to the user. If you want to further restrict roles, you can also apply resource-level permissions to roles, but for this scenario, allowing listing all roles is generally acceptable.
     - Resource: "*": Applies to all IAM roles. If you wanted to restrict roles as well, you would specify role ARNs here.
Important Considerations:
 - iam:CreateUser: The policy does not include iam:CreateUser. This is because you specifically mentioned you want to restrict the principal to managing a single user. If the principal needs to create the initial user, you would need a separate, more permissive policy for the creation phase, or create the user beforehand.
 - iam:UpdateUser: This policy does not include iam:UpdateUser. If you need to allow modifications to the user (like changing password policies or other user attributes), you would need to add iam:UpdateUser to the Action list.
 - Error Handling: If the principal attempts to perform any of these actions on a different IAM user, the IAM policy will deny the action, resulting in an "Access Denied" error.
3. Programmatically Create and Attach the IAM Policy
You can programmatically create and attach this IAM policy using AWS SDKs (like boto3 for Python), AWS CLI, or Infrastructure as Code (IaC) tools like AWS CloudFormation or Terraform.
Using AWS CLI (Example):
 - Save the policy document to a file named restricted-user-policy.json.
 - Create the IAM Policy:

```sh
aws iam create-policy --policy-name RestrictedUserPolicy --policy-document \file://restricted-user-policy.json --description "Policy to restrict management to a single IAM user"
```

This command will output the ARN of the newly created policy. Note down the PolicyArn.

- Attach the Policy to the IAM Principal:
   You can attach the policy to an IAM user, group, or role, depending on which principal you want to grant these restricted permissions to. Let's assume you want to attach it to an IAM role named ResourceCreatorRole:

```sh
aws iam attach-role-policy --role-name ResourceCreatorRole --policy-arn \<PolicyArn_from_create_policy_command\>
```

Replace \<PolicyArn_from_create_policy_command\> with the PolicyArn you noted down in the previous step.

## Replace with Your Actual account ID and User name

Using Infrastructure as Code (IaC) - Terraform (Example):

```hcl
resource "aws_iam_policy" "restricted_user_policy" {
  name        = "RestrictedUserPolicy"
  description = "Policy to restrict management to a single IAM user"
  policy      = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "iam:GetUser",
          "iam:DeleteUser",
          "iam:AttachRolePolicy",
          "iam:DetachRolePolicy",
          "iam:ListAttachedRolePolicies"
        ]
        Resource = [
         "arn:aws:iam::YOUR_AWS_ACCOUNT_ID:user/USER_NAME_TO_RESTRICT_TO" # Replace placeholders
        ]
      },
      {
        Effect   = "Allow"
        Action   = "iam:ListRoles"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "restricted_policy_attachment" {
  role       = "ResourceCreatorRole" # Replace with your role name
  policy_arn = aws_iam_policy.restricted_user_policy.arn
}
```

Remember to replace the placeholders (YOUR_AWS_ACCOUNT_ID, USER_NAME_TO_RESTRICT_TO, ResourceCreatorRole) with your actual values in all programmatic approaches.

4. Testing and Verification

After applying the policy, thoroughly test the permissions of the IAM principal to ensure it behaves as expected:

 - Positive Test: Verify that the principal can perform the allowed actions (e.g., GetUser, DeleteUser, attach/detach roles) on the specified IAM user.
 - Negative Test: Verify that the principal cannot perform these actions on other IAM users.
 - Negative Test: Verify that the principal cannot perform actions that are not explicitly allowed (e.g., CreateUser, UpdateUser if not included in the policy).
By implementing resource-level permissions in this way, you can significantly enhance the security posture of your AWS environment by limiting the scope of IAM principal permissions. Remember to always follow the principle of least privilege when granting IAM permissions.
