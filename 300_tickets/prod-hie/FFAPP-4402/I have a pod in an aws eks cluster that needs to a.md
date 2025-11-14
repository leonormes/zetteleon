---
aliases: []
confidence: 
created: 2025-10-23T10:26:50Z
epistemic: 
last_reviewed: 
modified: 2025-11-14T11:53:16Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: I have a pod in an aws eks cluster that needs to a
type:
uid: 
updated: 
version:
---

I have a pod in an aws eks cluster that needs to assume a role that allows it to write to an s3 bucket. We thought we needed the aws_secret_access_key and aws_access_key_id for those users but my llm said no. Can you validate the advice it gave

Your LLM advice is correct: you do not need AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY for your pod to assume the IAM role that allows writing to the S3 bucket.

Here is the validation and explanation based on the provided IAM AssumeRole report:

- In an EKS cluster, the pod itself doesn't hold long-term user credentials. Instead, the EKS worker node's IAM role must have the permission `sts:AssumeRole` on the target IAM role that grants S3 write access.
- The pod leverages the node's IAM role to assume the target role via AWS Security Token Service (STS). This provides temporary, automatically rotated credentials transparently.
- The two-part permission handshake:

1. The EKS node's IAM role must be allowed to call `sts:AssumeRole` on the target role.
2. The target role must trust the EKS node's role in its trust policy to accept the assume role request.

- Creating long-term static access keys (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY) for this is discouraged because they become permanent credentials that risk leakage and require secure storage.
- The proper setup is to add an inline IAM policy to the EKS node's role granting it the `sts:AssumeRole` action on the target S3-writing role and ensure the target role's trust policy allows this assumption.
- Once set, the pod will get temporary credentials via the node role's assumed role permissions and can securely write to the S3 bucket without static access keys.

In summary, your pod does not need AWS access keys; it uses the IAM role assumption mechanism via STS for secure, temporary credentials. This is the recommended best practice to avoid managing static credentials.[^1_1]

<div align="center">⁂</div>

[^1_1]: IAM-AssumeROle.md

---

## But how Do We Assert that only the Hyve Pod is Allowed to Assume that Role? I Don't want other Pods Being Able to Assume the Role

The right way to ensure that only the **hyve pod** can assume the IAM role (and not every pod running on the same node) is to use **IAM Roles for Service Accounts (IRSA)** instead of relying solely on the node’s IAM role.

Here’s how to do it securely:

### Step 1: Enable OIDC Provider for Your EKS Cluster

EKS uses OpenID Connect (OIDC) to map Kubernetes service accounts to IAM roles.

Run:

```bash
aws eks describe-cluster --name <cluster_name> --query "cluster.identity.oidc.issuer" --output text
```

If it isn’t enabled, set it up in the AWS Console or via the CLI. This gives each pod an identity tied to its service account.

### Step 2: Create a Dedicated Service Account for the Hyve Pod

In your `hyve` namespace (or whichever namespace you use):

```bash
kubectl create serviceaccount hyve-sa --namespace hyve
```

### Step 3: Create an IAM Role Trusted by Only That Service Account

Define the IAM role trust policy that restricts **who can assume it** to a specific service account in your cluster:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/<OIDC_PROVIDER>"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "<OIDC_PROVIDER>:sub": "system:serviceaccount:hyve:hyve-sa"
        }
      }
    }
  ]
}
```

This ensures **only pods** running under the service account `hyve-sa` in the `hyve` namespace can assume this IAM role — not other workloads.

### Step 4: Attach the Role to the Service Account

Use `eksctl` or AWS CLI to associate the IAM role with the service account:

```bash
eksctl create iamserviceaccount \
  --cluster <cluster_name> \
  --namespace hyve \
  --name hyve-sa \
  --attach-role-arn arn:aws:iam::<ACCOUNT_ID>:role/HyveS3WriterRole \
  --approve
```

### Step 5: Use the Service Account in the Deployment

In your pod/deployment manifest:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hyve
  namespace: hyve
spec:
  template:
    spec:
      serviceAccountName: hyve-sa
      containers:
        - name: hyve
          image: <your-image>
```

Now, only pods using that specific service account (and in the correct namespace) can obtain temporary credentials to assume the IAM role and write to S3.

This IRSA model aligns with AWS best practices because it:

- Eliminates shared node-level permissions,
- Scopes IAM access down to the Kubernetes service account identity, and
- Prevents other pods from impersonating the hyve pod’s role.[^2_1]
