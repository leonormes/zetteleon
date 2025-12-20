---
aliases: []
confidence: 
created: 2025-02-12T18:03:15Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:43Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [IAM]
title: IAM challenges
type: curriculum
uid: 
updated: 
version: 
---

Beginner Challenges (Core Concepts & Basic Permissions)

1. Create Your First IAM User

Create a new IAM user with programmatic access.

Assign minimal permissions (no policies attached).

Attempt to perform an action and observe the "Access Denied" error.

2. Attach Managed Policies to a User

Attach the AmazonS3ReadOnlyAccess policy to the IAM user.

Verify that the user can read S3 objects but cannot upload or delete them.

3. Create and Use IAM Groups

Create a group called Developers.

Attach a policy that grants access to EC2:DescribeInstances.

Add a user to the group and verify access.

4. Implement MFA for an IAM User

Enable multi-factor authentication (MFA) for an IAM user.

Attempt to log in without MFA and observe the behavior.

---

Intermediate Challenges (Custom Policies & Roles)

5. Write a Custom IAM Policy for S3 Access

Create a policy that allows a user to list all S3 buckets but only read objects from a specific bucket.

Attach it to an IAM user and verify.

6. Use an IAM Role for EC2

Create an IAM role that allows an EC2 instance to access an S3 bucket.

Launch an EC2 instance and attach the role.

Use the AWS CLI on the instance to verify S3 access.

7. Set Up a Trust Relationship Between Accounts

Create an IAM role in Account A that allows users from Account B to assume it.

Use sts:AssumeRole from Account B to assume the role and verify access.

8. Implement Least Privilege Principle

Audit permissions of an IAM user with AdministratorAccess.

Restrict permissions to only what's needed using a custom policy.

9. Create a Resource-Based Policy for an S3 Bucket

Allow read access to an S3 bucket only from a specific AWS account using a bucket policy.

Test access from different accounts.

---

Advanced Challenges (Cross-Account & Service-Specific IAM)

10. IAM Policy Conditions & Permissions Boundaries

Create an IAM policy that allows actions only if they originate from a specific IP range.

Apply a permissions boundary that prevents users from deleting resources.

11. Use IAM Roles for Kubernetes Pods (EKS IRSA)

Configure IAM Roles for Service Accounts (IRSA) to allow an EKS pod to access an S3 bucket.

Deploy a pod and verify access.

12. Set Up AWS Organizations & Service Control Policies (SCPs)

Create an AWS Organization.

Apply an SCP that prevents member accounts from creating new IAM users.

13. Implement IAM Access Analyzer

Use AWS IAM Access Analyzer to detect unused permissions.

Refine and clean up excessive permissions.

---

Expert Challenges (Enterprise-Scale IAM Security & Compliance)

14. Automate IAM Policy Generation with IAM Access Advisor

Analyze which permissions are used by an IAM role.

Generate a least-privilege policy based on activity.

15. Federate AWS IAM with an External Identity Provider (IdP)

Set up IAM federation with Azure AD or Okta.

Verify that users can sign in using their corporate credentials.

16. Create a Custom AWS Lambda Function for IAM Policy Auditing

Write a Lambda function that checks IAM users with inactive credentials.

Generate an alert if unused access keys are found.

17. Implement Attribute-Based Access Control (ABAC) in AWS IAM

Define IAM policies that grant access based on user attributes.

Use IAM session tags to enforce attribute-based access.

18. Implement AWS IAM Identity Center (SSO) for Multiple Accounts

Set up IAM Identity Center (AWS SSO) to centralize user management across multiple AWS accounts.

---

Final Challenge: Design a Secure IAM Strategy for an Enterprise

Create an IAM architecture for a large organization with multiple AWS accounts.

Implement best practices, including least privilege, role-based access control (RBAC), multi-factor authentication (MFA), permissions boundaries, service control policies (SCPs), and logging/auditing with AWS CloudTrail.

Justify your design decisions.
