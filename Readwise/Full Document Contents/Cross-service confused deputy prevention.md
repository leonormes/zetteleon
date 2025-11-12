# Cross-service confused deputy prevention

![rw-book-cover](https://docs.aws.amazon.com/assets/images/favicon.ico)

## Metadata
- Author: [[Amazon EKS Document History]]
- Full Title: Cross-service confused deputy prevention
- Category: #articles
- Summary: Added a topic with an example trust policy that you can apply for Cross-service confused deputy prevention.
Amazon EKS accepts the aws:SourceArn and aws:SourceAccount conditions in the trust policy of an EKS cluster role.
- URL: https://docs.aws.amazon.com/eks/latest/userguide/cross-service-confused-deputy-prevention.html

## Full Document
**Help improve this page**

To contribute to this user guide, choose the **Edit this page on GitHub** link that is located in the right pane of every page.

### Cross-service confused deputy prevention in Amazon EKS

The confused deputy problem is a security issue where an entity that doesn’t have permission to perform an action can coerce a more-privileged entity to perform the action. In AWS, cross-service impersonation can result in the confused deputy problem. Cross-service impersonation can occur when one service (the <emphasis>calling service</emphasis>) calls another service (the <emphasis>called service</emphasis>). The calling service can be manipulated to use its permissions to act on another customer’s resources in a way it should not otherwise have permission to access. To prevent this, AWS provides tools that help you protect your data for all services with service principals that have been given access to resources in your account.

We recommend using the [`aws:SourceArn`](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-sourcearn), [`aws:SourceAccount`](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-sourceaccount) global condition context keys in resource policies to limit the permissions that Amazon Elastic Kubernetes Service (Amazon EKS) gives another service to the resource.

`aws:SourceArn`

Use `aws:SourceArn` to associate only one resource with cross-service access.

`aws:SourceAccount`

Use `aws:SourceAccount` to let any resource in that account be associated with the cross-service use.

The most effective way to protect against the confused deputy problem is to use the `aws:SourceArn` global condition context key with the full ARN of the resource. If you don’t know the full ARN of the resource or if you are specifying multiple resources, use the `aws:SourceArn` global context condition key with wildcard characters () for the unknown portions of the ARN. For example, `arn:aws:
 `servicename`:`.

If the `aws:SourceArn` value does not contain the account ID, such as an Amazon S3 bucket ARN, you must use both `aws:SourceAccount` and `aws:SourceArn` to limit permissions.

#### Amazon EKS cluster role cross-service confused deputy prevention

An Amazon EKS cluster IAM role is required for each cluster. Kubernetes clusters managed by Amazon EKS use this role to manage nodes and the [legacy Cloud Provider](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.7/guide/service/annotations/#legacy-cloud-provider) uses this role to create load balancers with Elastic Load Balancing for services.
These cluster actions can only affect the same account, so we recommend that you limit each cluster role to that cluster and account.
This is a specific application of the AWS recommendation to follow the *principle of least privilege* in your account.

**Source ARN format**

The value of `aws:SourceArn` must be the ARN of an EKS cluster in the format `arn:aws::eks:`region`:`account`:cluster/`cluster-name``. For example, `arn:aws::eks:us-east-1:123456789012:cluster/my-cluster` .

**Trust policy format for EKS cluster roles**

The following example shows how you can use the `aws:SourceArn` and `aws:SourceAccount` global condition context keys in Amazon EKS to prevent the confused deputy problem.

```
{
  "Version": "2012-10-17",
  "Statement": :[.replaceable]`123456789012`:cluster/[.replaceable]`my-cluster`"
          },
        "StringEquals": {
            "aws:SourceAccount": "123456789012"
        }
      }
    }
  ]
}
```
