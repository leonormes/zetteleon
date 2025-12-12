---
aliases: []
confidence: 
created: 2025-10-23T11:01:03Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:15Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [hie-prod-34]
title: IAM AssumeROle
type:
uid: 
updated: 
version:
---

## IAM Role Analysis Report - EKS Node AssumeRole Permissions

**Date:** 2025-10-23  
**Instance ID:** i-0ade93e1cfcfbe9f7  
**Target Role to Assume:** arn:aws:iam::339713007003:role/dlz-tst-writer-codisc

---

### Executive Summary

The EKS node instance **cannot** assume the target role `dlz-tst-writer-codisc` because it lacks the required `sts:AssumeRole` permission. An additional IAM policy must be attached to enable cross-account role assumption.

---

### Instance Configuration

#### EC2 Instance Details

- **Instance ID:** i-0ade93e1cfcfbe9f7
- **IAM Instance Profile:** eks-b0cca93b-5c5a-d547-77b0-4b87ebec8cbd
- **IAM Role Name:** eoe-sde-codisc-node-group

#### Current IAM Role Configuration

**Role:** `eoe-sde-codisc-node-group`

**Attached Managed Policies (3):**

1. AmazonEKS_CNI_Policy (arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy)
2. AmazonEC2ContainerRegistryReadOnly (arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly)
3. AmazonEKSWorkerNodePolicy (arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy)

**Inline Policies:** None

---

### Policy Analysis

#### 1. AmazonEKS_CNI_Policy

**Purpose:** Allows the AWS VPC CNI plugin to manage network interfaces

**Key Permissions:**

- Network interface management (create, delete, attach, detach)
- `ec2:CreateTags` - **LIMITED** to network interfaces only (`arn:aws:ec2:*:*:network-interface/*`)
- `ec2:DescribeTags`

**AssumeRole Permission:** ❌ **NOT PRESENT**

---

#### 2. AmazonEC2ContainerRegistryReadOnly

**Purpose:** Allows pulling container images from ECR

**Key Permissions:**

- ECR read operations (GetAuthorizationToken, BatchGetImage, etc.)

**AssumeRole Permission:** ❌ **NOT PRESENT**

---

#### 3. AmazonEKSWorkerNodePolicy

**Purpose:** Allows EKS worker nodes to interact with AWS services

**Key Permissions:**

- EC2 describe operations (instances, volumes, VPCs, etc.)
- `eks:DescribeCluster`
- `eks-auth:AssumeRoleForPodIdentity` (for EKS Pod Identity, **NOT** STS AssumeRole)

**AssumeRole Permission:** ❌ **NOT PRESENT**

---

### Findings

#### ❌ Missing Permission

The role `eoe-sde-codisc-node-group` does **NOT** have `sts:AssumeRole` permission.

#### What We're Looking For

A policy statement containing:

```json
{
  "Effect": "Allow",
  "Action": "sts:AssumeRole",
  "Resource": "arn:aws:iam::339713007003:role/dlz-tst-writer-codisc"
}
```

#### What We Found

- ✅ `eks-auth:AssumeRoleForPodIdentity` exists (different from `sts:AssumeRole`)
- ❌ `sts:AssumeRole` does **NOT** exist in any attached policy

---

### Required Action

#### Recommended Solution: Add Inline Policy

Create an inline policy on the `eoe-sde-codisc-node-group` role:

**Policy Document:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAssumeQCRWriterRole",
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::339713007003:role/dlz-tst-writer-codisc"
    }
  ]
}
```

**AWS CLI Command:**

```bash
aws iam put-role-policy \
  --role-name eoe-sde-codisc-node-group \
  --policy-name AllowAssumeQCRWriterRole \
  --policy-document file://assume-role-policy.json
```

---

### Additional Verification Required

#### Trust Relationship on Target Role

Ensure the target role `dlz-tst-writer-codisc` in account 339713007003 allows the source role to assume it.

**Expected Trust Policy:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<SOURCE_ACCOUNT_ID>:role/eoe-sde-codisc-node-group"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

**Verification Command:**

```bash
aws iam get-role --role-name dlz-tst-writer-codisc \
  --query 'Role.AssumeRolePolicyDocument' --output json
```

---

### Testing After Implementation

```bash
aws sts assume-role \
  --role-arn arn:aws:iam::339713007003:role/dlz-tst-writer-codisc \
  --role-session-name test-session
```

---

### Summary

| Item                      | Status                                |
| ------------------------- | ------------------------------------- |
| Instance Profile Found    | ✅ Yes                                |
| IAM Role Identified       | ✅ eoe-sde-codisc-node-group          |
| sts:AssumeRole Permission | ❌ **MISSING**                        |
| Required Action           | Add inline policy with sts:AssumeRole |
| Security Impact           | Low (specific resource ARN)           |

**Conclusion:** The node cannot assume the target role until the `sts:AssumeRole` permission is added to the `eoe-sde-codisc-node-group` role.

This is an excellent and thorough analysis. Based on your report, here is a summary of what needs to happen and why, so the `hyve` pod can assume its role and write to the S3 bucket.

---

### **Executive Summary**

The `hyve` pod cannot access the S3 bucket because the underlying EKS worker node it runs on (`eoe-sde-codisc-node-group`) lacks the fundamental AWS permission to assume the required role (`dlz-tst-writer-codisc`).

To fix this, two things must be in place:

1. **Permission to Ask**: The node's IAM role must be granted the `sts:AssumeRole` permission.
2. **Permission to Grant**: The target role must have a trust policy that accepts requests from the node's role.

Your report confirms the first part is missing.

---

### **The Problem: A Two-Part Handshake is Failing**

Think of assuming an IAM role as a two-part security handshake:

1. **The "Asker" (Your EKS Node)**: The entity initiating the request (the EKS node's role, `eoe-sde-codisc-node-group`) must have permission to ask to become another role. This is done via the `sts:AssumeRole` permission.
2. **The "Giver" (Your Target S3 Role)**: The role being assumed (`dlz-tst-writer-codisc`) must explicitly trust the "Asker" and be willing to grant it temporary credentials.

Your analysis confirms the handshake fails at the very first step. The EKS node's role has **no policy allowing it to perform `sts:AssumeRole`**, so it can't even begin the process.

---

### **The Solution: What Needs to Happen**

As your report correctly identifies, there are two required actions.

#### **Action 1: Grant the Node Permission to Assume the Role (Required)**

You must add an inline IAM policy to the `eoe-sde-codisc-node-group` role. This policy explicitly allows it to assume the `dlz-tst-writer-codisc` role.

**Policy to Add:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAssumeQCRWriterRole",
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::339713007003:role/dlz-tst-writer-codisc"
    }
  ]
}
```

- **Why?** This gives the EKS node the ability to make the `sts:AssumeRole` call, which is the foundational step for the `hyve` application to get temporary credentials for S3 access. Without this, the process is a non-starter.

#### **Action 2: Verify the Target Role's Trust Policy (Verification)**

Your report correctly points out that you must also verify the trust relationship on the target role (`dlz-tst-writer-codisc`). Its trust policy must allow the `eoe-sde-codisc-node-group` role to assume it.

**Expected Trust Policy on `dlz-tst-writer-codisc`:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<SOURCE_ACCOUNT_ID>:role/eoe-sde-codisc-node-group"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

*Replace `<SOURCE_ACCOUNT_ID>` with the AWS account ID where the EKS cluster resides.*

- **Why?** This completes the handshake. The node asks for permission, and the target role confirms, "Yes, I trust you. Here are the temporary credentials."

Once Action 1 is completed and Action 2 is verified, the `hyve` application will be able to successfully assume the role and gain the necessary permissions to write to the S3 bucket.

This is an important screen, and it's good you're asking. Based on our goal, the best practice is to **not create an access key at all**.

Therefore, the correct option on this screen is to **press "Cancel"**.

### **Why You Should Not Create an Access Key**

The page you're on is for creating a long-term **IAM User** access key. This is considered a security risk for applications running on AWS and is exactly the problem that our `AssumeRole` strategy is designed to solve.

- **Static Keys are a Liability**: If you create an access key and secret, you have to store them somewhere (like Vault), and they become a permanent, powerful credential that can be leaked.
- **Role Assumption is More Secure**: The method we've been working towards uses temporary, automatically-rotated credentials. The application never sees a long-term secret. It simply asks the EKS node for permission, and the node uses its IAM role to get a short-lived token from AWS.

### **The Correct Path: Modify the IAM Role, Not the User**

The solution outlined in your report does not involve creating any new credentials or access keys. It involves modifying an existing **IAM Role**.

Here is the correct workflow in the AWS Console:

1. Navigate to the **IAM** service.
2. On the left-hand menu, click on **Roles**.
3. In the search bar, find the EKS node's role: `eoe-sde-codisc-node-group`.
4. Click on the role name to open its summary page.
5. Under the "Permissions" tab, click the **"Add permissions"** dropdown and select **"Create inline policy"**.
6. In the policy editor, switch to the **JSON** tab.
7. Paste the policy document from your report:

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "AllowAssumeQCRWriterRole",
          "Effect": "Allow",
          "Action": "sts:AssumeRole",
          "Resource": "arn:aws:iam::339713007003:role/dlz-tst-writer-codisc"
        }
      ]
    }
    ```

8. Click **"Next"**, give the policy a name (e.g., `AllowAssumeQCRWriterRole`), and save it.

By following these steps, you are granting the necessary permission to the existing role, which is the secure and correct way to enable the `hyve` pod to assume its target role.
