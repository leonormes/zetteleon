---
aliases: []
confidence: 
created: 2025-10-23T11:57:09Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:15Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: "Subject_ Heads Up_ We're Switching to Pod Identity"
type:
uid: 
updated: 
version:
---

I'll investigate how IRSA is currently implemented and used in this EKS cluster using kubectl and AWS CLI to show you the exact patterns being used.

**Command Executed:**

```bash
aws eks describe-cluster --name eoe-sde-codisc --query 'cluster.identity.oidc.issuer' --output text
```

**Output:**

```sh
https://oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB
```

**Command Executed:**

```bash
kubectl get sa -A -o json | jq -r '.items[] | select(.metadata.annotations["eks.amazonaws.com/role-arn"] != null) | {namespace: .metadata.namespace, name: .metadata.name, role: .metadata.annotations["eks.amazonaws.com/role-arn"]}'
```

**Output:**

```sh
{
  "namespace": "kube-system",
  "name": "aws-cluster-autoscaler-sa",
  "role": "arn:aws:iam::135808916559:role/eoe-sde-codisc-eks-cluster-autoscaler-role"
}
{
  "namespace": "kube-system",
  "name": "ebs-csi-controller-sa",
  "role": "arn:aws:iam::135808916559:role/eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole"
}
```

**Command Executed:**

```bash
kubectl describe sa aws-cluster-autoscaler-sa -n kube-system
```

**Output:**

```sh
Name:                aws-cluster-autoscaler-sa
Namespace:           kube-system
Labels:              app.kubernetes.io/instance=cluster-autoscaler
                     app.kubernetes.io/managed-by=Helm
                     app.kubernetes.io/name=aws-cluster-autoscaler
                     helm.sh/chart=cluster-autoscaler-9.50.1
Annotations:         eks.amazonaws.com/role-arn: arn:aws:iam::135808916559:role/eoe-sde-codisc-eks-cluster-autoscaler-role
                     meta.helm.sh/release-name: cluster-autoscaler
                     meta.helm.sh/release-namespace: kube-system
Image pull secrets:  <none>
Mountable secrets:   <none>
Tokens:              <none>
Events:              <none>
```

**Command Executed:**

```bash
aws iam get-role --role-name eoe-sde-codisc-eks-cluster-autoscaler-role --output json
```

**Output:**

```sh
{
    "Role": {
        "Path": "/",
        "RoleName": "eoe-sde-codisc-eks-cluster-autoscaler-role",
        "RoleId": "AROAR7HWXTRH4M5A3WJPR",
        "Arn": "arn:aws:iam::135808916559:role/eoe-sde-codisc-eks-cluster-autoscaler-role",
        "CreateDate": "2025-02-14T17:49:20+00:00",
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Federated": "arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB"
                    },
                    "Action": "sts:AssumeRoleWithWebIdentity",
                    "Condition": {
                        "StringEquals": {
                            "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB:sub": "system:serviceaccount:kube-system:aws-cluster-autoscaler-sa"
                        }
                    }
                }
            ]
        },
        "MaxSessionDuration": 3600,
        "Tags": [
            {
                "Key": "GitlabRepo",
                "Value": "gitlab.com/fitfile/customers/eoe/hie-sde-v2"
            },
            {
                "Key": "eks_cluster",
                "Value": "eoe-sde-codisc"
            },
            {
                "Key": "ProvisionByOrgName",
                "Value": "FITFILE"
            },
            {
                "Key": "branch",
                "Value": "master"
            }
        ],
        "RoleLastUsed": {
            "LastUsedDate": "2025-10-23T12:01:23+00:00",
            "Region": "eu-west-2"
        }
    }
}
```

**Command Executed:**

```bash
aws iam list-attached-role-policies --role-name eoe-sde-codisc-eks-cluster-autoscaler-role --output json
```

**Output:**

```sh
{
    "AttachedPolicies": [
        {
            "PolicyName": "eoe-sde-codisc-EKSClusterAutoscalerPolicy",
            "PolicyArn": "arn:aws:iam::135808916559:policy/service-role/eoe-sde-codisc-EKSClusterAutoscalerPolicy"
        }
    ]
}
```

**Command Executed:**

```bash
aws iam list-role-policies --role-name eoe-sde-codisc-eks-cluster-autoscaler-role --output json
```

**Output:**

```sh
{
    "PolicyNames": []
}
```

**Command Executed:**

```bash
kubectl get deployment cluster-autoscaler -n kube-system -o yaml | grep -A 30 "serviceAccountName\|env:" | head -40
```

**Output:**

```sh
Error from server (NotFound): deployments.apps "cluster-autoscaler" not found
```

**Command Executed:**

```bash
kubectl get pods -n kube-system -l app.kubernetes.io/name=aws-cluster-autoscaler -o name | head -1 | xargs -I {} kubectl describe {} -n kube-system | grep -A 20 "Environment:\|Mounts:"
```

**Output:**

```sh
    Environment:
      POD_NAMESPACE:                kube-system (v1:metadata.namespace)
      SERVICE_ACCOUNT:               (v1:spec.serviceAccountName)
      AWS_REGION:                   eu-west-2
      AWS_STS_REGIONAL_ENDPOINTS:   regional
      AWS_ROLE_ARN:                 arn:aws:iam::135808916559:role/eoe-sde-codisc-eks-cluster-autoscaler-role
      AWS_WEB_IDENTITY_TOKEN_FILE:  /var/run/secrets/eks.amazonaws.com/serviceaccount/token
    Mounts:
      /var/run/secrets/eks.amazonaws.com/serviceaccount from aws-iam-token (ro)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-tg9wg (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True
  Initialized                 True
  Ready                       True
  ContainersReady             True
  PodScheduled                True
Volumes:
  aws-iam-token:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  86400
  kube-api-access-tg9wg:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    Optional:                false
    DownwardAPI:             true
QoS Class:                   BestEffort
```

Perfect! Now let me check the EBS CSI driver example as well, and then look at how pods actually use these credentials:

**Command Executed:**

```bash
kubectl describe sa ebs-csi-controller-sa -n kube-system
```

**Output:**

```sh
Name:                ebs-csi-controller-sa
Namespace:           kube-system
Labels:              app.kubernetes.io/component=csi-driver
                     app.kubernetes.io/managed-by=EKS
                     app.kubernetes.io/name=aws-ebs-csi-driver
                     app.kubernetes.io/version=1.48.0
Annotations:         eks.amazonaws.com/role-arn: arn:aws:iam::135808916559:role/eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole
Image pull secrets:  <none>
Mountable secrets:   <none>
Tokens:              <none>
Events:              <none>
```

**Command Executed:**

```bash
aws iam get-role --role-name eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole --query 'Role.AssumeRolePolicyDocument' --output json
```

**Output:**

```sh
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB:sub": "system:serviceaccount:kube-system:ebs-csi-controller-sa",
                    "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB:aud": "sts.amazonaws.com"
                }
            }
        }
    ]
}
```

**Command Executed:**

```bash
kubectl run test-irsa --image=amazon/aws-cli:2.15.34 --serviceaccount=aws-cluster-autoscaler-sa -n kube-system --rm -it --restart=Never -- sts get-caller-identity
```

**Output:**

```sh
error: unknown flag: --serviceaccount
See 'kubectl run --help' for usage.
```

**Command Executed:**

```bash
kubectl run test-irsa --image=amazon/aws-cli:2.15.34 --overrides='{"spec":{"serviceAccountName":"aws-cluster-autoscaler-sa"}}' -n kube-system --rm -it --restart=Never -- sts get-caller-identity 2>&1
```

**Output:**

```sh
All commands and output from this session will be recorded in container logs, including credentials and sensitive information passed through the command prompt.
If you don't see a command prompt, try pressing enter.
{
    "UserId": "AROAR7HWXTRH4M5A3WJPR:botocore-session-1761221208",
    "Account": "135808916559",
    "Arn": "arn:aws:sts::135808916559:assumed-role/eoe-sde-codisc-eks-cluster-autoscaler-role/botocore-session-1761221208"
}
pod "test-irsa" deleted from kube-system namespace
```

Excellent! Now let me check the OIDC provider details and create a comprehensive report:

**Command Executed:**

```bash
aws iam get-open-id-connect-provider --open-id-connect-provider-arn "arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB" --output json | jq '{Url, ClientIDList, ThumbprintList, Tags}'
```

**Output:**

```sh
{
  "Url": "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB",
  "ClientIDList": [
    "sts.amazonaws.com"
  ],
  "ThumbprintList": [
    "06b25927c42a721631c1efd9431e648fa62e1e39",
    "d9fe0a65fa00cabf61f5120d373a8135e1461f15",
    "9113c492911635f730e51f259f28873df5b7f01a"
  ],
  "Tags": [
    {
      "Key": "ProvisionByOrgName",
      "Value": "FITFILE"
    },
    {
      "Key": "branch",
      "Value": "master"
    },
    {
      "Key": "GitlabRepo",
      "Value": "gitlab.com/fitfile/customers/eoe/hie-sde-v2"
    },
    {
      "Key": "eks_cluster_name",
      "Value": "eoe-sde-codisc"
    }
  ]
}
```

**Command Executed:**

```bash
kubectl get mutatingwebhookconfigurations -o json | jq -r '.items[] | select(.metadata.name | contains("pod-identity")) | .metadata.name'
```

**Output:**

```sh
pod-identity-webhook
```

**Command Executed:**

```bash
kubectl describe mutatingwebhookconfiguration pod-identity-webhook | head -40
```

**Output:**

```sh
Name:         pod-identity-webhook
Namespace:
Labels:       <none>
Annotations:  <none>
API Version:  admissionregistration.k8s.io/v1
Kind:         MutatingWebhookConfiguration
Metadata:
  Creation Timestamp:  2025-02-14T17:46:21Z
  Generation:          1
  Resource Version:    276
  UID:                 49e5c51e-dc17-40df-a21a-b4d7413655b5
Webhooks:
  Admission Review Versions:
    v1beta1
  Client Config:
    Ca Bundle:     LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURCVENDQWUyZ0F3SUJBZ0lJYlYrR0drWUNyazB3RFFZSktvWklodmNOQVFFTEJRQXdGVEVUTUJFR0ExVUUKQXhNS2EzVmlaWEp1WlhSbGN6QWVGdzB5TlRBeU1UUXhOelF3TVRkYUZ3MHpOVEF5TVRJeE56UTFNVGRhTUJVeApFekFSQmdOVkJBTVRDbXQxWW1WeWJtVjBaWE13Z2dFaU1BMEdDU3FHU0liM0RRRUJBUVVBQTRJQkR3QXdnZ0VLCkFvSUJBUUM0aC9nRXRpV2hIdE4rYmFFNE9MYllSUUh2aDF2OC9DU2paUEVheGtHTzc2Qmtrd3pNOUF2SE5yMjgKdGFXMXBtUGR4Vm53NU1WbXdNRFROY1dZZkhEbmFXV3BodmZUTDhJNlkwa2JyRkdZc3k3NzhqemptYzAvazdjQgpjUVU3Y3JrYWcrOUIzNnRmaWZaelIyUHBBVzJyOW53azkrVmNNUzFkaDc2N21SYmowRTJ3aDlLbzJRTjJMVUxQCkdnd0pPWTNoVWZ5bTA3UmF0cHFzaXA5MkRaMGw4TXI1QlppQXVueHk1VkRhSlBrM1BkUGhTOHJpTmw0WTdNYi8KKy9QMmVzb0hram9obW1tR0d1VUZGejBJdlA2c0JZc1dyTmMzQ1V4MlU3d0FXRzlFYkcvQ0Vyb0EvS1ZWbWNFVApMVkx3b3pHaTFvUmp1dXhGK2hEV2I3SU1GUEJmQWdNQkFBR2pXVEJYTUE0R0ExVWREd0VCL3dRRUF3SUNwREFQCkJnTlZIUk1CQWY4RUJUQURBUUgvTUIwR0ExVWREZ1FXQkJUY3ZEeGtDS1B6QnZWK2NWZ0NianhwYVpWSktUQVYKQmdOVkhSRUVEakFNZ2dwcmRXSmxjbTVsZEdWek1BMEdDU3FHU0liM0RRRUJDd1VBQTRJQkFRQ29OVVR0WS9rVgp3K2daUmo4NW5HUzFyNDFXNk0vM1lvVktaZklPY0hXRGl0WTJYQjd1WHVMRWtsQUVYVHJQRjU4WTZZaFE3UXZpCnVHUVh5aERpdm1JcEhxamJnaitHdldHQ3VlT3Bvb2pnMzBhdWU3Rk9wUDhYby9NTmlSYlA5L1lVY3Qrd1lnaE0KeGlBdGpzMVJiV2hrTFV0OCtaWlVsd1dsdTZuSWJXZFhLbGJweWVSQkF6VlBHakNnMlZTWXNHSFYvTTh0LzhxawpoN1d2N2xRczdCUzlwUFpCQjFEelMrZTAvVHFoMXdiayt0MEtieDRkUVUwbm1SSDA1T3VER0t1M2hQYnJqWFdVCkw0VnBDMGVXR1NvRDBkWjY2eUtDWWxlL0pHYVhnRzBIVjBhbTB6TDZZTS8xWS9nclNBcTFmQUlnRXAxVmlhTVkKeCsrT2M1NWVtWkFzCi0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K
    URL:           https://127.0.0.1:23443/mutate
  Failure Policy:  Ignore
  Match Policy:    Equivalent
  Name:            iam-for-pods.amazonaws.com
  Namespace Selector:
  Object Selector:
    Match Expressions:
      Key:              eks.amazonaws.com/skip-pod-identity-webhook
      Operator:         DoesNotExist
  Reinvocation Policy:  IfNeeded
  Rules:
    API Groups:

    API Versions:
      v1
    Operations:
      CREATE
    Resources:
      pods
    Scope:          *
  Side Effects:     None
  Timeout Seconds:  10
Events:             <none>
```

Perfect! Now let me create a comprehensive report. Let me generate the final document:

---

## **IRSA (IAM Roles for Service Accounts) Implementation Report**

### EKS Cluster: `eoe-sde-codisc`

---

### **Executive Summary**

IRSA is **fully operational** in this EKS cluster. The system uses a mutating webhook to automatically inject AWS credentials into pods based on ServiceAccount annotations. This report documents exactly how it works and provides patterns for implementing IRSA for theHyve.

---

### **🔧 How IRSA Works in This Cluster**

#### **1. The Core Components**

##### **A) OIDC Identity Provider (IAM)**

```sh
Provider ARN: arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB
Issuer URL:   https://oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB
Client ID:    sts.amazonaws.com
Status:       ✅ Active (Created: 2025-02-14)
```

**Tags on OIDC Provider:**

- `ProvisionByOrgName: FITFILE`
- `branch: master`
- `GitlabRepo: gitlab.com/fitfile/customers/eoe/hie-sde-v2`
- `eks_cluster_name: eoe-sde-codisc`

##### **B) Pod Identity Webhook (Kubernetes)**

```sh
Name:                pod-identity-webhook
Type:                MutatingWebhookConfiguration
Webhook:             iam-for-pods.amazonaws.com
Endpoint:            https://*********:23443/mutate
Created:             2025-02-14T17:46:21Z
```

**What it does:**

- Intercepts pod creation requests
- Checks if the ServiceAccount has `eks.amazonaws.com/role-arn` annotation
- Automatically injects environment variables and volumes into the pod

---

#### **2. The Injection Mechanism**

When a pod is created with an IRSA-enabled ServiceAccount, the webhook automatically adds:

##### **Environment Variables:**

```bash
AWS_ROLE_ARN=arn:aws:iam::135808916559:role/eoe-sde-codisc-eks-cluster-autoscaler-role
AWS_WEB_IDENTITY_TOKEN_FILE=/var/run/secrets/eks.amazonaws.com/serviceaccount/token
AWS_STS_REGIONAL_ENDPOINTS=regional
AWS_REGION=eu-west-2
```

##### **Volume Mounts:**

```yaml
volumeMounts:
  - name: aws-iam-token
    mountPath: /var/run/secrets/eks.amazonaws.com/serviceaccount
    readOnly: true

volumes:
  - name: aws-iam-token
    projected:
      sources:
        - serviceAccountToken:
            audience: sts.amazonaws.com
            expirationSeconds: 86400
            path: token
```

**Key Point:** The token is a **Kubernetes ServiceAccount token** that is trusted by AWS via the OIDC provider. It expires after 24 hours (86400 seconds) and is automatically rotated.

---

#### **3. The Authentication Flow**

```sh
┌─────────────────────────────────────────────────────────────────┐
│ 1. Pod starts with ServiceAccount that has IRSA annotation     │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. Webhook injects AWS_ROLE_ARN, AWS_WEB_IDENTITY_TOKEN_FILE   │
│    and mounts projected SA token at the specified path         │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. AWS SDK reads environment variables and token file          │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. SDK calls sts:AssumeRoleWithWebIdentity with the token      │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. AWS STS validates token against OIDC provider               │
│    - Checks issuer matches OIDC provider URL                   │
│    - Checks audience is "sts.amazonaws.com"                    │
│    - Checks subject matches condition in IAM role trust policy │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. STS returns temporary AWS credentials (15 min - 12 hours)   │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. SDK uses temporary credentials for AWS API calls            │
│    (automatically refreshes before expiration)                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### **📊 Current IRSA Implementations**

#### **Example 1: Cluster Autoscaler**

##### **ServiceAccount:**

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: aws-cluster-autoscaler-sa
  namespace: kube-system
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::135808916559:role/eoe-sde-codisc-eks-cluster-autoscaler-role
  labels:
    app.kubernetes.io/managed-by: Helm
```

##### **IAM Role Trust Policy:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB:sub": "system:serviceaccount:kube-system:aws-cluster-autoscaler-sa"
        }
      }
    }
  ]
}
```

**Note:** Only checks `:sub` (subject), not `:aud` (audience).

##### **IAM Role Permissions:**

- Attached managed policy: `eoe-sde-codisc-EKSClusterAutoscalerPolicy`
- No inline policies

##### **Tags:**

```sh
GitlabRepo: gitlab.com/fitfile/customers/eoe/hie-sde-v2
eks_cluster: eoe-sde-codisc
ProvisionByOrgName: FITFILE
branch: master
```

##### **Verification Test:**

```bash
$ kubectl run test-irsa --image=amazon/aws-cli:2.15.34 \
  --overrides='{"spec":{"serviceAccountName":"aws-cluster-autoscaler-sa"}}' \
  -n kube-system --rm -it --restart=Never -- sts get-caller-identity

{
    "UserId": "*********************:botocore-session-1761221208",
    "Account": "135808916559",
    "Arn": "arn:aws:sts::135808916559:assumed-role/eoe-sde-codisc-eks-cluster-autoscaler-role/botocore-session-1761221208"
}
```

✅ **IRSA is working perfectly** - pod successfully assumed the IAM role.

---

#### **Example 2: EBS CSI Driver**

##### **ServiceAccount:**

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ebs-csi-controller-sa
  namespace: kube-system
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::135808916559:role/eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole
  labels:
    app.kubernetes.io/managed-by: EKS
```

##### **IAM Role Trust Policy:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB:sub": "system:serviceaccount:kube-system:ebs-csi-controller-sa",
          "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB:aud": "sts.amazonaws.com"
        }
      }
    }
  ]
}
```

**Note:** This one checks **both** `:sub` and `:aud`. This is the **recommended best practice** by AWS.

---

### **🎯 Pattern for theHyve Implementation**

Based on the working examples, here's what needs to be created for theHyve:

#### **1. IAM Role Structure**

```sh
Role Name: eoe-sde-codisc-thehyve-irsa-role
Account:   135808916559
Region:    eu-west-2
```

#### **2. Trust Policy (Recommended)**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB:sub": "system:serviceaccount:thehyve:thehyve",
          "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB:aud": "sts.amazonaws.com"
        }
      }
    }
  ]
}
```

#### **3. IAM Policy (Inline)**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAssumeCrossAccountRole",
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::339713007003:role/dlz-tst-writer-codisc"
    }
  ]
}
```

#### **4. Tags (Following Pattern)**

```sh
GitlabRepo: gitlab.com/fitfile/customers/eoe/hie-sde-v2
eks_cluster: eoe-sde-codisc
ProvisionByOrgName: FITFILE
branch: master
namespace: thehyve
service_account: thehyve
```

#### **5. ServiceAccount Annotation**

Add this to the Helm values file at `/ffnodes/eoe/hie-prod-34/thehyve_values.yaml`:

```yaml
serviceAccount:
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::135808916559:role/eoe-sde-codisc-thehyve-irsa-role
```

---

### **🔐 Cross-Account Role Configuration**

In account `339713007003`, the role `dlz-tst-writer-codisc` must trust the new IRSA role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::135808916559:role/eoe-sde-codisc-thehyve-irsa-role"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

---

### **✅ Verification Steps**

#### **1. Check ServiceAccount annotation**

```bash
kubectl describe sa thehyve -n thehyve | grep eks.amazonaws.com/role-arn
```

#### **2. Test Base IRSA credentials**

```bash
kubectl run aws-test --image=amazon/aws-cli:2.15.34 \
  --overrides='{"spec":{"serviceAccountName":"thehyve"}}' \
  -n thehyve --rm -it --restart=Never -- sts get-caller-identity
```

Expected output:

```json
{
  "Arn": "arn:aws:sts::135808916559:assumed-role/eoe-sde-codisc-thehyve-irsa-role/..."
}
```

#### **3. Test Cross-account assume**

```bash
kubectl run aws-test --image=amazon/aws-cli:2.15.34 \
  --overrides='{"spec":{"serviceAccountName":"thehyve"}}' \
  -n thehyve --rm -it --restart=Never -- \
  sts assume-role \
    --role-arn arn:aws:iam::339713007003:role/dlz-tst-writer-codisc \
    --role-session-name test
```

#### **4. Test S3 access** (after Setting Cross-account credentials)

```bash
aws s3 ls s3://eoe-sde-prd-dqr-381492210920 --region eu-west-2
```

---

### **📝 Application Changes Required**

#### **Environment Variables to REMOVE:**

- `QCR_ACCES_KEY_ID` ❌
- `QCR_SECRET_ACCESS_KEY` ❌

#### **Environment Variables to KEEP:**

- `QCR_IAM_ROLE` (value: `arn:aws:iam::339713007003:role/dlz-tst-writer-codisc`)
- `QCR_BUCKET` (value: `eoe-sde-prd-dqr-381492210920`)
- `AWS_REGION` (optional, set to `eu-west-2`)

#### **Application Code:**

No changes required if using AWS SDK! The SDK automatically:

1. Detects `AWS_ROLE_ARN` and `AWS_WEB_IDENTITY_TOKEN_FILE`
2. Calls `AssumeRoleWithWebIdentity` to get base credentials
3. Uses those credentials to call `AssumeRole` on the cross-account role
4. Automatically refreshes credentials before expiration

---

### **🎓 Key Takeaways**

1. **IRSA is transparent** - AWS SDKs handle everything automatically via environment variables
2. **The webhook does the magic** - automatically injects credentials into pods
3. **Tokens are short-lived** - ServiceAccount tokens expire in 24h, AWS credentials in 15min-12h
4. **No static credentials needed** - everything is dynamically generated
5. **Best practice** - Always check both `:sub` and `:aud` in trust policy conditions
6. **Cross-account works** - IRSA role can assume roles in other accounts

---

This report shows that IRSA is production-ready in your cluster and provides the exact pattern to follow for implementing it for theHyve.

Excellent security question! You're absolutely right - the IRSA role for theHyve should only be able to assume the specific cross-account role it needs, not any arbitrary role. This is enforced through IAM permissions on the IRSA role itself.

Let me show you exactly how this works:

**Command Executed:**

```bash
aws iam get-role-policy --role-name eoe-sde-codisc-eks-cluster-autoscaler-role --policy-name test 2>&1 || echo "No inline policies found"
```

**Output:**

```sh

An error occurred (NoSuchEntity) when calling the GetRolePolicy operation: The role policy with name test cannot be found.
No inline policies found
```

**Command Executed:**

```bash
aws iam get-policy --policy-arn arn:aws:iam::135808916559:policy/service-role/eoe-sde-codisc-EKSClusterAutoscalerPolicy --output json | jq '{PolicyName, Description, DefaultVersionId}'
```

**Output:**

```sh
{
  "PolicyName": null,
  "Description": null,
  "DefaultVersionId": null
}
```

**Command Executed:**

```bash
aws iam get-policy-version --policy-arn arn:aws:iam::135808916559:policy/service-role/eoe-sde-codisc-EKSClusterAutoscalerPolicy --version-id v1 --output json | jq '.PolicyVersion.Document'
```

**Output:**

```sh
{
  "Statement": [
    {
      "Action": [
        "autoscaling:DescribeAutoScalingGroups",
        "autoscaling:DescribeAutoScalingInstances",
        "autoscaling:DescribeLaunchConfigurations",
        "autoscaling:DescribeScalingActivities",
        "ec2:DescribeImages",
        "ec2:DescribeInstanceTypes",
        "ec2:DescribeLaunchTemplateVersions",
        "ec2:GetInstanceTypesFromInstanceRequirements",
        "eks:DescribeNodegroup"
      ],
      "Effect": "Allow",
      "Resource": [
        "*"
      ]
    },
    {
      "Action": [
        "autoscaling:SetDesiredCapacity",
        "autoscaling:TerminateInstanceInAutoScalingGroup"
      ],
      "Effect": "Allow",
      "Resource": [
        "*"
      ]
    }
  ],
  "Version": "2012-10-17"
}
```

Perfect! Now I can show you exactly how to restrict theHyve. The cluster autoscaler policy shows it only has EC2/autoscaling permissions - no `sts:AssumeRole` at all. Let me create a clear explanation:

---

## **🔐 Restricting theHyve to Assume Only a Specific Role**

### **The Two-Layer Security Model**

IRSA uses a **two-layer permission model**:

#### **Layer 1: IAM Trust Policy (WHO Can Assume the role)**

This controls which ServiceAccounts can assume the IRSA role.

#### **Layer 2: IAM Permissions Policy (WHAT the Role Can do)**

This controls what the IRSA role is allowed to do, including which other roles it can assume.

---

### **For theHyve: The Secure Configuration**

#### **1. IRSA Role Trust Policy** (Layer 1)

This restricts WHO can use the role - only the specific ServiceAccount:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB:sub": "system:serviceaccount:thehyve:thehyve",
          "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB:aud": "sts.amazonaws.com"
        }
      }
    }
  ]
}
```

✅ **Result:** Only pods using the `thehyve/thehyve` ServiceAccount can assume this role.

---

#### **2. IRSA Role Permissions Policy** (Layer 2 - THE CRITICAL PART)

This restricts WHAT the role can do - **only assume the specific cross-account role**:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAssumeSpecificRoleOnly",
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::339713007003:role/dlz-tst-writer-codisc"
    }
  ]
}
```

✅ **Result:** The IRSA role can **ONLY** assume `arn:aws:iam::339713007003:role/dlz-tst-writer-codisc` and nothing else.

---

### **Why This is Secure**

#### **❌ What theHyve CANNOT Do:**

1. **Cannot assume any other role:**

```bash
   # This will FAIL - Access Denied
   aws sts assume-role --role-arn arn:aws:iam::135808916559:role/some-other-role
   aws sts assume-role --role-arn arn:aws:iam::339713007003:role/some-other-role
```

2. **Cannot access AWS services directly:**

```bash
   # This will FAIL - Access Denied (no EC2/S3/etc permissions)
   aws s3 ls
   aws ec2 describe-instances
```

3. **Cannot modify IAM:**

```bash
   # This will FAIL - Access Denied
   aws iam create-role ...
   aws iam attach-role-policy ...
```

#### **✅ What theHyve CAN Do:**

1. **Assume the specific cross-account role:**

```bash
   # This will SUCCEED
   aws sts assume-role \
     --role-arn arn:aws:iam::339713007003:role/dlz-tst-writer-codisc \
     --role-session-name thehyve-session
```

2. **After assuming that role, do whatever that role permits:**
   - Access S3 bucket `eoe-sde-prd-dqr-381492210920`
   - Any other permissions granted to `dlz-tst-writer-codisc`

---

### **The Complete Terraform Implementation**

Here's how to implement this securely:

```hcl
# IRSA Role with restrictive trust policy
resource "aws_iam_role" "thehyve_irsa" {
  name = "eoe-sde-codisc-thehyve-irsa-role"

  # Layer 1: WHO can assume this role (only the specific ServiceAccount)
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = "arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB:sub" = "system:serviceaccount:thehyve:thehyve"
            "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB:aud" = "sts.amazonaws.com"
          }
        }
      }
    ]
  })

  tags = {
    GitlabRepo         = "gitlab.com/fitfile/customers/eoe/hie-sde-v2"
    eks_cluster        = "eoe-sde-codisc"
    ProvisionByOrgName = "FITFILE"
    branch             = "master"
    namespace          = "thehyve"
    service_account    = "thehyve"
  }
}

# Layer 2: WHAT the role can do (ONLY assume the specific cross-account role)
resource "aws_iam_role_policy" "thehyve_irsa_assume_cross_account" {
  name = "allow-assume-dlz-tst-writer-codisc-only"
  role = aws_iam_role.thehyve_irsa.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowAssumeSpecificRoleOnly"
        Effect = "Allow"
        Action = "sts:AssumeRole"
        # CRITICAL: Only this specific role ARN
        Resource = "arn:aws:iam::339713007003:role/dlz-tst-writer-codisc"
      }
    ]
  })
}

output "thehyve_irsa_role_arn" {
  value       = aws_iam_role.thehyve_irsa.arn
  description = "IRSA role ARN for theHyve ServiceAccount annotation"
}
```

---

### **Additional Security Best Practices**

#### **1. Add External ID (Optional but Recommended)**

For cross-account assume role, add an external ID:

**In the IRSA role permissions policy:**

```json
{
  "Sid": "AllowAssumeSpecificRoleOnly",
  "Effect": "Allow",
  "Action": "sts:AssumeRole",
  "Resource": "arn:aws:iam::339713007003:role/dlz-tst-writer-codisc",
  "Condition": {
    "StringEquals": {
      "sts:ExternalId": "thehyve-eoe-sde-codisc-unique-id"
    }
  }
}
```

**In the cross-account role trust policy (account 339713007003):**

```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::135808916559:role/eoe-sde-codisc-thehyve-irsa-role"
  },
  "Action": "sts:AssumeRole",
  "Condition": {
    "StringEquals": {
      "sts:ExternalId": "thehyve-eoe-sde-codisc-unique-id"
    }
  }
}
```

#### **2. Restrict by Session Name (Optional)**

```json
{
  "Sid": "AllowAssumeSpecificRoleOnly",
  "Effect": "Allow",
  "Action": "sts:AssumeRole",
  "Resource": "arn:aws:iam::339713007003:role/dlz-tst-writer-codisc",
  "Condition": {
    "StringLike": {
      "sts:RoleSessionName": "thehyve-*"
    }
  }
}
```

#### **3. Restrict Duration (Optional)**

```json
{
  "Sid": "AllowAssumeSpecificRoleOnly",
  "Effect": "Allow",
  "Action": "sts:AssumeRole",
  "Resource": "arn:aws:iam::339713007003:role/dlz-tst-writer-codisc",
  "Condition": {
    "NumericLessThanEquals": {
      "sts:DurationSeconds": "3600"
    }
  }
}
```

---

### **Verification: Testing the Restrictions**

#### **Test 1: Verify ONLY the Allowed Role Can Be assumed**

```bash
# Start a test pod
kubectl run test-thehyve --image=amazon/aws-cli:2.15.34 \
  --overrides='{"spec":{"serviceAccountName":"thehyve"}}' \
  -n thehyve --rm -it --restart=Never -- bash

# Inside the pod:
# This should SUCCEED
aws sts assume-role \
  --role-arn arn:aws:iam::339713007003:role/dlz-tst-writer-codisc \
  --role-session-name test

# This should FAIL with AccessDenied
aws sts assume-role \
  --role-arn arn:aws:iam::339713007003:role/some-other-role \
  --role-session-name test

# This should FAIL with AccessDenied
aws sts assume-role \
  --role-arn arn:aws:iam::135808916559:role/some-other-role \
  --role-session-name test
```

#### **Test 2: Verify no Direct AWS access**

```bash
# These should all FAIL with AccessDenied
aws s3 ls
aws ec2 describe-instances
aws iam list-roles
```

---

### **Summary: The Security Model**

```sh
┌──────────────────────────────────────────────────────────────┐
│ ServiceAccount: thehyve/thehyve                              │
│ Annotation: eks.amazonaws.com/role-arn                       │
└──────────────────┬───────────────────────────────────────────┘
                   │ (Trust Policy - Layer 1)
                   │ ✓ Only this SA can assume role
                   ▼
┌──────────────────────────────────────────────────────────────┐
│ IRSA Role: eoe-sde-codisc-thehyve-irsa-role                  │
│ Account: 135808916559                                        │
│                                                              │
│ Permissions (Layer 2):                                       │
│   ✓ sts:AssumeRole on ONE specific role only                │
│   ✗ NO other AWS permissions                                │
└──────────────────┬───────────────────────────────────────────┘
                   │ (sts:AssumeRole)
                   │ Resource: arn:...../dlz-tst-writer-codisc
                   ▼
┌──────────────────────────────────────────────────────────────┐
│ Cross-Account Role: dlz-tst-writer-codisc                    │
│ Account: 339713007003                                        │
│                                                              │
│ Trust Policy:                                                │
│   ✓ Trusts: eoe-sde-codisc-thehyve-irsa-role               │
│                                                              │
│ Permissions:                                                 │
│   ✓ S3 access to eoe-sde-prd-dqr-381492210920              │
│   ✓ Whatever else is granted                                │
└──────────────────────────────────────────────────────────────┘
```

**Result:** theHyve can ONLY assume the one specific role you want, and nothing else. This follows the principle of least privilege.

## Recommendation (TL;DR)

- **Phase 1 (Terraform Cloud, main infra):** Create the IAM IRSA role and its OIDC trust + policy to allow `sts:AssumeRole` to the cross-account role. Output the role ARN.
- **Phase 2 (Jumpbox, app deploy):** Annotate the `thehyve` ServiceAccount with the role ARN via Helm/Argo (preferred) or Kubernetes provider. Remove static AWS keys from app values/secrets.
- **Cross-account trust (339713007003):** Update the trust policy for `dlz-tst-writer-codisc` in that account’s repo/pipeline (separate, but can be done in parallel with Phase 1).

This follows your existing pattern (e.g., cluster-autoscaler IRSA lives in infra), avoids Terraform Cloud needing private EKS API access, and keeps app ownership with the app pipeline.

---

### Why This Split

- **IAM is infra:** The IRSA role, OIDC trust, and `sts:AssumeRole` permission are AWS account/infra concerns that should be created before any pod runs. Place in [Production/hie-sde-v2/](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/hie-sde-v2:0:0-0:0) (Phase 1).
- **Kubernetes access is private:** Terraform Cloud cannot (and shouldn’t) reach the private EKS API to annotate the ServiceAccount. The jumpbox can. Do the SA annotation in Phase 2.
- **Ownership boundaries:** Helm/Argo owns app resources. Annotating the SA in the chart avoids Terraform/Helm drift on K8s objects.

---

### What Goes where

#### Phase 1 (Terraform Cloud: [Deployment/Clusters/eoe/Production/hie-sde-v2/](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/hie-sde-v2:0:0-0:0))

- **Create IRSA role:** `eoe-sde-codisc-thehyve-irsa-role` with:
  - Trust: OIDC provider and `sub = system:serviceaccount:thehyve:thehyve` (+ `aud = sts.amazonaws.com`)
  - Policy: `sts:AssumeRole` for `arn:aws:iam::339713007003:role/dlz-tst-writer-codisc`
  - Tags: merge your `local.tags` plus `eks_cluster`, `service_account`, `namespace`
- **Output:** `thehyve_irsa_role_arn` (to be consumed by Phase 2).

This matches your existing locals and provider setup in [hie-sde-v2](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/hie-sde-v2:0:0-0:0) and doesn’t require Kubernetes connectivity.

#### Phase 2 (Jumpbox: App deploy)

- **Annotate SA via Helm/Argo (preferred):** In the app chart values (e.g., [thehyve_values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/eoe/hie-prod-34/thehyve_values.yaml:0:0-0:0) under `Deployment/helm_chart_deployment/ffnodes/eoe/hie-prod-34/`), add:

  ```yaml
  serviceAccount:
    create: true # or false if SA is pre-created elsewhere
    name: thehyve
    annotations:
      eks.amazonaws.com/role-arn: <thehyve_irsa_role_arn>
  ```

  Feed `<thehyve_irsa_role_arn>` from Phase 1 output (via CI var, artifact, or remote state).

- **Remove static creds from values/secrets:**
  - Remove `QCR_ACCES_KEY_ID` and `QCR_SECRET_ACCESS_KEY` envs (and related secrets).
  - Keep `QCR_BUCKET` and, if your app expects it, `QCR_IAM_ROLE` = `arn:aws:iam::339713007003:role/dlz-tst-writer-codisc`.
- If you deploy the app with Terraform from the jumpbox, you can instead use the Kubernetes provider there to annotate the existing SA (and avoid Helm drift by not having Helm manage the SA).

#### Cross-account Trust (Account 339713007003)

- Update the trust policy of `dlz-tst-writer-codisc` to trust:
  - `arn:aws:iam::135808916559:role/eoe-sde-codisc-thehyve-irsa-role`
- Do this in the target account’s IaC repo/pipeline. It’s independent of cluster access and can happen alongside Phase 1.

---

### Wiring Phase 1 → Phase 2

- **Via remote state (if Phase 2 uses Terraform):**

  ```hcl
  data "terraform_remote_state" "cluster" {
    backend = "remote"
    config = {
      organization = "FITFILE-Platforms"
      workspaces = { name = "<hie-sde-v2-workspace-name>" }
    }
  }

  locals {
    thehyve_irsa_role_arn = data.terraform_remote_state.cluster.outputs.thehyve_irsa_role_arn
  }
  ```

- **Via Helm values:** Export the ARN as a CI/CD variable and template it into [thehyve_values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/eoe/hie-prod-34/thehyve_values.yaml:0:0-0:0).

---

### Notes Specific to Your Repo

- Infra locals and tagging are already standardized (`local.name = eoe-sde-codisc`, `local.tags`, `local.region`). Keep the IRSA code in [Production/hie-sde-v2/](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/hie-sde-v2:0:0-0:0) (e.g., `irsa_thehyve.tf`) alongside your existing EKS stack.
- The current [thehyve_values.yaml](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/ffnodes/eoe/hie-prod-34/thehyve_values.yaml:0:0-0:0) shows:
  - Static creds (`QCR_ACCES_KEY_ID`, `QCR_SECRET_ACCESS_KEY`) coming from a secret. Plan to delete those keys and their secret entries when moving to IRSA.
  - Keep `QCR_BUCKET`. Keep `QCR_IAM_ROLE` only if your app code uses it explicitly; otherwise, rely on default provider chain and omit it.

---

### Validation Checklist

- **Phase 1:** `terraform apply` creates role and outputs ARN.
- **Cross-account:** Trust policy updated to allow assume by the IRSA role.
- **Phase 2:** SA annotated. `kubectl -n thehyve describe sa thehyve` shows the role ARN.
- **Runtime test:** From a debug pod using SA `thehyve`, `aws sts get-caller-identity` shows assumed `eoe-sde-codisc-thehyve-irsa-role`. Then verify `sts assume-role` into `dlz-tst-writer-codisc` and S3 access to `eoe-sde-prd-dqr-381492210920`.

---

### Summary

- **Use a combination:** IAM role in Phase 1 (Terraform Cloud, infra repo) + SA annotation and secret cleanup in Phase 2 (jumpbox, app deploy).
- **Cross-account trust** updated in the target account’s pipeline.
- This aligns with your current patterns, avoids private API access from Terraform Cloud, and cleanly separates infra IAM from app rollout.
