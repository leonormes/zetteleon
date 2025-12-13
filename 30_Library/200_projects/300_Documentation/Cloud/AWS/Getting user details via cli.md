---
aliases: []
confidence: 
created: 2025-02-07T12:57:53Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, cli]
title: Getting user details via cli
type: 
uid: 
updated: 
version: 
---

Here are some options to retrieve the user's configuration:

1. Using the AWS CLI `get-user` command:
This command will output the basic user information in JSON format.

```sh
aws iam get-user --user-name leon.ormes
```

1. To get more detailed information, including the user's policies, you can use a combination of commands:

   a. Get user details:

```sh
aws iam get-user --user-name leon.ormes
```

   b. List attached policies:

```sh
aws iam list-attached-user-policies --user-name leon.ormes
```

   c. List inline policies:

      ```

      aws iam list-user-policies --user-name leon.ormes

      ```

   d. For each inline policy, get the policy document:

```sh
aws iam get-user-policy --user-name leon.ormes --policy-name [policy-name]
```

3. If you prefer a single command that retrieves most of the user's information, you can use the `get-account-authorization-details` command with a filter:

```sh
aws iam get-account-authorization-details --filter User --query 'UserDetailList[?UserName==`leon.ormes`]'
```

This command will output a comprehensive JSON that includes the user's details, attached managed policies, and inline policies.

Each of these commands will output the results in JSON format, which you can then examine or further process as needed. You can redirect the output to a file for easier analysis:

```sh
aws iam get-account-authorization-details --filter User --query 'UserDetailList[?UserName==`leon.ormes`]' > leon_ormes_config.json
```

By using these CLI commands, you can easily extract and examine the user's configuration without needing to navigate through the console interface. This approach also allows for easier automation and integration with other tools or scripts if needed.

Sources

[1] [Use CreateLoginProfile with a CLI - AWS Identity and Access Management] (<https://docs.aws.amazon.com/IAM/latest/UserGuide/iam_example_iam_CreateLoginProfile_section.html>)

[3] [Use GetUser with an AWS SDK or CLI - AWS Identity and Access Management] (<https://docs.aws.amazon.com/IAM/latest/UserGuide/iam_example_iam_GetUser_section.html>)

[6] [Use ChangePassword with a CLI - AWS Identity and Access Management] (<https://docs.aws.amazon.com/IAM/latest/UserGuide/iam_example_iam_ChangePassword_section.html>)

The JSON document describes the permissions associated with the AWS IAM user `leon.ormes`. Here's a breakdown of the key properties and what they signify:

## JSON Properties and Their Meaning

1. Path: The hierarchy in which the user resides. The default path is `/`, meaning no custom hierarchy is used.
2. UserName: The name of the IAM user (`leon.ormes`).
3. UserId: A unique identifier for the IAM user.
4. Arn: The Amazon Resource Name that uniquely identifies the user within AWS.
5. CreateDate: The date and time when the user was created.
6. UserPolicyList: Inline policies directly attached to the user, specifying permissions.

    - PolicyName: Name of the inline policy (e.g., `routedns`, `view_eks`).
    - PolicyDocument: Contains detailed policy definitions, including:
        - Version: Policy language version (current is `2012-10-17`).
        - Statement: List of permissions:
            - Effect: Whether the permission is `Allow` or `Deny`.
            - Action: Actions allowed or denied (e.g., `route53:ListResourceRecordSets`).
            - Resource: Resources the actions apply to, specified using ARNs.
            - Sid (optional): Statement identifier for easy reference.
7. GroupList: Groups the user belongs to. It’s empty here, indicating no group memberships.
8. AttachedManagedPolicies: Managed policies attached to the user. These are predefined AWS policies that grant various permissions:

    - AmazonRoute53FullAccess: Full access to Route 53 services.
    - AdministratorAccess: Unrestricted access to all AWS services and resources.
    - AWSKeyManagementServicePowerUser: Permissions to manage keys and grants, but not delete keys or manage IAM policies.
    - IAMUserChangePassword: Allows the user to change their own password.
9. Tags: Metadata tags associated with the user, likely for resource organization or identification.

## What Can the User Do

- Route53 Operations: Full access via the `AmazonRoute53FullAccess` policy.
- Administrative Privileges: With `AdministratorAccess`, the user can perform virtually any action in AWS.
- KMS Operations: Ability to manage encryption keys with `AWSKeyManagementServicePowerUser`.
- Password Management: Allowed to change their own password.

## How to Review All Permissions

1. Evaluate Inline Policies:

    - Review the `UserPolicyList` for granular permissions directly assigned to the user.
2. Review Managed Policies:

    - Examine the `AttachedManagedPolicies`. Their ARNs can be looked up in the AWS Management Console or CLI to view the full permissions.
3. Effective Permissions:

    - Use the AWS IAM Console or AWS CLI to simulate policies using the `iam simulate-principal-policy` command. This shows effective permissions.

Would you like a summary of the steps to verify this in AWS?

Your AWS permissions are defined by a combination of inline user policies, attached managed policies, and potentially group memberships (although there are none listed here). Here's a breakdown of the document:

---

## User Details

- UserName: `leon.ormes`
- UserId: Unique identifier for the user.
- Arn: Amazon Resource Name for the user.
- CreateDate: Date and time the user was created.

---

## Inline Policies

These are custom policies directly attached to your user.

1. PolicyName: `routedns`

    - Effect: `Allow`
        - Action: `route53:ListResourceRecordSets`
            - Grants permission to list DNS records in Route 53.
        - Resource: `arn:aws:route53:::hostedzone/`
            - Applies to all Route 53 hosted zones.
2. PolicyName: `view_eks`

    - Effect: `Allow`
        - Actions:
            - Grants various permissions related to Amazon EKS (Elastic Kubernetes Service), such as listing clusters, describing node groups, and accessing the Kubernetes API.
            - Also includes `iam:ListRoles` to list IAM roles.
        - Resource: ``
            - Applies globally to all resources.
        - Additionally grants `ssm:GetParameter` to retrieve parameters in Systems Manager for resources specific to your account.

---

## Attached Managed Policies

These are predefined policies provided by AWS or your organization and attached to your user.

1. AmazonRoute53FullAccess:

    - Grants full access to manage Route 53 DNS services.
2. AdministratorAccess:

    - Grants full administrative access to all AWS resources and services.
3. AWSKeyManagementServicePowerUser:

    - Grants permissions to manage AWS Key Management Service (KMS) keys, but not full administrative privileges.
4. IAMUserChangePassword:

    - Allows you to change your own IAM password.

---

## Tags

Tags are metadata attached to the user, often for tracking or organizational purposes. These include keys like `leonlaptop`, `leonterm`, and others, with specific values assigned.

---

## Working Out All Permissions

To review the effective permissions:

1. Inline Policies: Analyze each statement in the policy document for actions and resources allowed/denied.
2. Attached Managed Policies:
    - Use the AWS Management Console or AWS CLI to view the details of these policies.
    - Example CLI command:

```bash
aws iam get-policy --policy-arn <PolicyArn>
```

        Then retrieve the policy version:

```bash
aws iam get-policy-version --policy-arn <PolicyArn> --version-id <VersionId>
```

1. Evaluate Overlap:
    - Policies with `Allow` effects override `Deny` only if there’s no explicit `Deny` elsewhere.
2. Simulate Permissions:
    - Use the AWS IAM Policy Simulator to evaluate which actions and resources you can access: [IAM Policy Simulator](https://policysim.aws.amazon.com/).

Would you like further guidance on simulating permissions or reviewing specific policies in more detail?
