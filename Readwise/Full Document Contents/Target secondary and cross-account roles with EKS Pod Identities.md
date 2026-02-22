# Target secondary and cross-account roles with EKS Pod Identities

![rw-book-cover](https://docs.aws.amazon.com/assets/images/favicon.ico)

## Metadata
- Author: [[Amazon EKS Document History]]
- Full Title: Target secondary and cross-account roles with EKS Pod Identities
- Category: #articles
- Summary: Amazon EKS adds target IAM roles to EKS Pod Identities for automated role chaining. You can use this to automatically assume a role in another account and EKS Pod Identity rotates the temporary credentials. Each Pod Identity association must have an IAM role in the same account to assume first, then it uses that role to assume the target role.
- URL: https://docs.aws.amazon.com/eks/latest/userguide/pod-id-assign-target-role.html

## Full Document
**Help improve this page**

To contribute to this user guide, choose the **Edit this page on GitHub** link that is located in the right pane of every page.

### Access AWS Resources using EKS Pod Identity Target IAM Roles

When running applications on Amazon Elastic Kubernetes Service (Amazon EKS), you might need to access AWS resources that exist in the same or different AWS accounts. This guide shows you how to set up access between these accounts using EKS Pod Identity, which enables your Kubernetes pods to access other AWS resources.

#### Prerequisites

Before you begin, ensure you have completed the following steps:

#### How It Works

Pod Identity enables applications in your EKS cluster to access AWS resources across accounts through a process called role chaining. When creating a Pod Identity association, you can provide two IAM roles—an [EKS Pod Identity role](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-role.html) in the same account as your EKS cluster and a Target IAM Role from the account containing your AWS resources (like S3 buckets or DynamoDB tables). The [EKS Pod Identity role](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-role.html) must be in your EKS cluster’s account due to [IAM PassRole](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_iam-passrole-service.html) requirements, while the Target IAM Role can be in any AWS account. PassRole enables an AWS entity to delegate role assumption to another service. EKS Pod Identity uses PassRole to connect a role to a Kubernetes service account, requiring both the role and the identity passing it to be in the same AWS account as the EKS cluster. When your application pod needs to access AWS resources, it requests credentials from Pod Identity. Pod Identity then automatically performs two role assumptions in sequence: first assuming the [EKS Pod Identity role](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-role.html), then using those credentials to assume the Target IAM Role. This process provides your pod with temporary credentials that have the permissions defined in the target role, allowing secure access to resources in other AWS accounts.

#### Caching considerations

Due to caching mechanisms, updates to an IAM role in an existing Pod Identity association may not take effect immediately in the pods running on your EKS cluster. The Pod Identity Agent caches IAM credentials based on the association’s configuration at the time the credentials are fetched. If the association includes only an [EKS Pod Identity role](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-role.html) ARN and no Target IAM Role, the cached credentials last for 6 hours. If the association includes both the [EKS Pod Identity role](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-role.html) ARN and a Target IAM Role, the cached credentials last for 59 minutes. Modifying an existing association, such as updating the [EKS Pod Identity role](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-role.html) ARN or adding a Target IAM Role, does not reset the existing cache. As a result, the agent will not recognize updates until the cached credentials refresh. To apply changes sooner, you can recreate the existing pods; otherwise, you will need to wait for the cache to expire.

#### Step 1: Create and associate a Target IAM Role

In this step, you will establish a secure trust chain by creating and configuring a Target IAM Role. For demonstration, we will create a new Target IAM Role to establish a trust chain between two AWS accounts: the [EKS Pod Identity role](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-role.html) (e.g., `eks-pod-identity-primary-role`) in the EKS cluster’s AWS account gains permission to assume the Target IAM Role (e.g. `eks-pod-identity-aws-resources`) in your target account, enabling access to AWS resources like Amazon S3 buckets.

##### Create the Target IAM Role

1. Open the [Amazon IAM console](https://console.aws.amazon.com/iam/home#/clusters).
2. In the top navigation bar, verify that you are signed into the account containing the AWS resources (like S3 buckets or DynamoDB tables) for your Target IAM Role.
3. In the left navigation pane, choose **Roles**.
4. Choose the **Create role** button, then **AWS account** under "Trusted entity type."
5. Choose **Another AWS account**, enter your AWS account number (the account where your [EKS Pod Identity role](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-role.html) exists), then choose **Next**.
6. Add the permission policies you would like to associate to the role (e.g., AmazonS3FullAccess), then choose **Next**.
7. Enter a role name, such as `MyCustomIAMTargetRole`, then choose **Create role**.

##### Update the Target IAM Role trust policy

1. After creating the role, you’ll be returned to the **Roles** list. Find and select the new role you created in the previous step (e.g., `MyCustomIAMTargetRole`).
2. Select the **Trust relationships** tab.
3. Click **Edit trust policy** on the right side.
4. In the policy editor, replace the default JSON with your trust policy. Replace the placeholder values for role name and `111122223333` in the IAM role ARN with the AWS account ID hosting your EKS cluster. For example:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::111122223333:role/eks-pod-identity-primary-role"
            },
            "Action": "sts:AssumeRole",
        },
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::111122223333:role/eks-pod-identity-primary-role"
            },
            "Action": "sts:TagSession"
        }
    ]
}
```

##### Update the permission policy for EKS Pod Identity role

In this step, you will update the permission policy of the [EKS Pod Identity role](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-role.html) associated with your Amazon EKS cluster by adding the Target IAM Role ARN as a resource.

1. Open the [Amazon EKS console](https://console.aws.amazon.com/eks/home#/clusters).
2. In the left navigation pane, select **Clusters**, and then select the name of your EKS cluster.
3. Choose the **Access** tab.
4. Under **Pod Identity associations**, select your [EKS Pod Identity role](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-role.html).
5. Choose **Permissions**, **Add permissions**, then **Create inline policy**.
6. Choose **JSON** on the right side.
7. In the policy editor, replace the default JSON with your permission policy. Replace the placeholder value for role name and `222233334444` in the IAM role ARN with your Target IAM Role. For example:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sts:AssumeRole",
                "sts:TagSession"
            ],
            "Resource": "arn:aws:iam::222233334444:role/eks-pod-identity-aws-resources"
        }
    ]
}
```

#### Step 2: Associate the Target IAM Role to a Kubernetes service account

In this step, you will create an association between the Target IAM role and the Kubernetes service account in your EKS cluster.

1. Open the [Amazon EKS console](https://console.aws.amazon.com/eks/home#/clusters).
2. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to add the association to.
3. Choose the **Access** tab.
4. In the **Pod Identity associations**, choose **Create**.
5. Choose the [EKS Pod Identity role](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-role.html) in **IAM role** for your workloads to assume.
6. Choose the Target IAM role in **Target IAM role** that will be assumed by the [EKS Pod Identity role](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-role.html).
7. In the **Kubernetes namespace** field, enter the name of the namespace where you want to create the association (e.g., `my-app-namespace`). This defines where the service account resides.
8. In the **Kubernetes service account** field, enter the name of the service account (e.g., `my-service-account`) that will use the IAM credentials. This links the IAM role to the service account.
9. Choose **Create** to create the association.

#### (Optional) Step 3: Add External Permissions to an IAM Target Role

At times, you might need to give a third party access to your AWS resources (delegate access). For example, you decide to hire a third-party company called Example Corp to monitor your AWS account and help optimize costs. In order to track your daily spending, Example Corp needs to access your AWS resources. In this case, we recommend adding an `ExternalId` to the trust policy of your IAM Target Role to avoid possible [Confused Deputy](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html) issues.

##### Edit the trust policy

1. After creating the role, you’ll be returned to the **Roles** list. Find and click the new role you created in the previous step (e.g., `MyCustomIAMTargetRole`).
2. Select the **Trust relationships** tab.
3. Click **Edit trust policy** on the right side.
4. In the policy editor, replace the default JSON with your trust policy. Replace the `ExternalId` placeholder value for `aws-region/other-account/cluster-name/namespace/service-account-name`, where "region" is the AWS region of your cluster, "111122223333" is the other AWS account ID, "cluster-name" is the EKS cluster name, "namespace" is the Kubernetes namespace, and "service-account-name" is the Kubernetes service account name. For example:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::111122223333:role/eks-pod-identity-primary-role"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "region/111122223333/cluster-name/namespace/service-account-name"
                }
        },
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::111122223333:role/eks-pod-identity-primary-role"
            },
            "Action": "sts:TagSession"
        }
    ]
}
```
