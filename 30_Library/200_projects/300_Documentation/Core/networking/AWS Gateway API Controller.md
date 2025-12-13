---
aliases: []
confidence: 
created: 2025-04-02T08:41:26Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [FFAPP-3588]
title: AWS Gateway API Controller
type: 
uid: 160cd9bb-e0af-4b92-a096-c2314aa1bd36
updated: 
version: 
---

I can certainly be helpful to you in this endeavour. Drawing upon the provided sources, my understanding is that to get the AWS Gateway API Controller functioning correctly, especially in a private EKS cluster, several components need to be configured precisely. The knowledge base I have access to details the prerequisites for deploying the controller, the core concepts behind it, the installation procedures, and how it interacts with AWS services like VPC Lattice. It also covers cross-cluster service exposure and security considerations. The GitHub repository likely contains example configurations and manifests which can be invaluable.

Let's break down the components you'll need to set up to get the AWS Gateway API Controller working in your private EKS cluster and successfully expose your specific service privately:

**1. Prerequisites and Cluster Setup:**

Before you can even install the AWS Gateway API Controller, certain prerequisites must be in place on your workstation and within your AWS environment.

- **Command-Line Interface (CLI) Tools:** You'll need several CLI tools installed on your workstation to interact with AWS and your Kubernetes cluster. These include:
    - **AWS CLI:** This is the official command-line interface for interacting with AWS services. It's crucial for creating and managing IAM policies and roles, which is likely where your credential issues stem from.
    - **kubectl:** This is the Kubernetes command-line tool that allows you to run commands against your Kubernetes cluster. You'll use it to apply manifests, create namespaces, and manage Kubernetes resources related to the Gateway API Controller.
    - **helm:** This is a package manager for Kubernetes. It's the recommended method for installing the AWS Gateway API Controller as it simplifies deployment and management.
    - **eksctl:** This is a CLI tool specifically for Amazon EKS (Elastic Kubernetes Service). While the AWS Gateway API Controller can be used on any Kubernetes cluster on AWS, EKS is a straightforward and recommended way to prepare a cluster. `eksctl` can be used to create clusters and set up AWS policies.
    - **jq:** This is a lightweight and flexible command-line JSON processor. It's useful for manipulating JSON files, particularly when working with AWS CLI outputs.
- **AWS EKS Cluster (Private VPC):** You need to have an AWS EKS cluster already running. Given your requirement for a private network, it's crucial that your EKS cluster is configured within a private Virtual Private Cloud (VPC). You might have the cluster API server endpoint configured for private access to ensure all communication stays within your VPC. You'll also need to set your AWS Region and Cluster Name as environment variables.

**2. Kubernetes Gateway API Custom Resource Definitions (CRDs):**

The Kubernetes Gateway API relies on Custom Resource Definitions (CRDs) to define resources like `GatewayClass`, `Gateway`, `HTTPRoute`, and others.

- **Installation Requirement:** These CRDs are no longer bundled with the AWS Gateway API Controller itself as of version 1.1.0, so you must install them manually. The latest Gateway API CRDs are available, and you need to follow the provided installation process, typically using `kubectl apply` with YAML files obtained from the official Kubernetes Gateway API repository. This step is fundamental as the controller needs these definitions to understand and manage the Gateway API resources you will create.

**3. IAM Permissions for the AWS Gateway API Controller:**

This is the most likely area where your credential issues are arising. The AWS Gateway API Controller needs specific IAM permissions to interact with AWS APIs, particularly Amazon VPC Lattice. You need to set up these permissions to allow the controller to operate correctly. This process involves several steps:

- **Create an IAM Policy:** It's recommended to create an IAM policy with the necessary permissions to invoke the Gateway API and interact with VPC Lattice resources. You can download a recommended inline policy from the AWS Application Networking Kubernetes GitHub repository or create one manually. This policy should grant the controller permissions to perform actions related to VPC Lattice service networks, services, target groups, and potentially security policies. The documentation and the `recommended-inline-policy.json` file in the GitHub repository () are your primary resources for defining this policy.
- **Create an IAM Role:** An IAM role needs to be created that the controller's pods will assume. This role will be associated with the IAM policy you created in the previous step.
- **Attach the IAM Policy to the Role:** The IAM policy must be attached to the IAM role, granting the role the defined permissions. You will need the Amazon Resource Name (ARN) of the created policy for this step.
- **Configure Controller Permissions (Pod Identities or IRSA):** The controller needs a way to assume the IAM role. There are two main methods for this:
    - **Pod Identities (Recommended):** To use Pod Identities, you need to set up the Agent and configure the controller's Kubernetes Service Account to assume the necessary permissions using EKS Pod Identity. This involves:
        - Creating the Pod Identity addon for your EKS cluster.
        - Ensuring your custom node role (if applicable) has permissions for the Pod Identity Agent to perform the `AssumeRoleForPodIdentity` action.
        - Creating a Kubernetes Service Account specifically for the AWS Gateway API Controller within the `aws-application-networking-system` namespace.
        - Creating a Pod Identity association linking the IAM role, the `aws-application-networking-system` namespace, and the controller's Service Account.
    - **IAM Roles for Service Accounts (IRSA):** If you choose to use IRSA, you need to:
        - Create an IAM OIDC (OpenID Connect) provider for your EKS cluster if you haven't already. This allows IAM to trust your EKS cluster's identity provider. You can use `eksctl utils associate-iam-oidc-provider` for this.
        - Create an `iamserviceaccount` Kubernetes resource, attaching the ARN of the IAM policy you created to this service account. This service account should also reside in the `aws-application-networking-system` namespace.

    It's critical to ensure that the IAM role has the correct trust relationship configured to allow either the Pod Identity agent or the OIDC provider and the Kubernetes service account to assume the role. The GitHub repository likely provides examples of trust policies. Choosing the right method and configuring it correctly is essential for the controller pods to obtain the necessary AWS credentials.

**4. Create the `aws-application-networking-system` Namespace:**

You need to create a dedicated namespace in your Kubernetes cluster named `aws-application-networking-system`. This is the namespace where you will deploy the AWS Gateway API Controller. You can create this namespace by applying a simple YAML manifest file using `kubectl apply`.

**5. Create the `amazon-vpc-lattice` GatewayClass:**

Finally, you need to create a `GatewayClass` resource named `amazon-vpc-lattice` in your Kubernetes cluster. This Kubernetes resource informs the Gateway API implementation which controller should handle `Gateway` resources that specify this `GatewayClass`. When you define a `Gateway` with the `amazon-vpc-lattice` `GatewayClass`, the controller will watch for it and the associated resources (like `HTTPRoute`), creating the corresponding resources in Amazon VPC Lattice. You can apply the provided YAML file for this using `kubectl apply`. The GitHub repository will contain this YAML file (`gatewayclass.yaml` in the `files/controller-installation` directory).

**6. Install the AWS Gateway API Controller:**

Once the prerequisites are met, you can proceed with installing the controller itself. You can do this using either `kubectl` or `helm`. Helm is generally the recommended approach.

- **Using Helm:** You would typically add the AWS ECR public repository and install the controller using a `helm install` command. When using Helm, you'll likely need to set the `serviceAccount.create` value to `false` if you have manually created the Service Account in the IAM setup steps. You'll also specify the namespace as `aws-application-networking-system`. You can find the Helm chart details in the GitHub repository (`aws-gateway-controller-chart`).
- **Using kubectl:** Alternatively, you can apply a YAML manifest file directly using `kubectl apply`. This manifest file is also available in the GitHub repository (`deploy-v1.1.0.yaml` for version 1.1.0).

**7. Private Network Considerations and Exposing Your Service:**

Since your EKS cluster is private, the AWS Gateway API Controller, in conjunction with Amazon VPC Lattice, will facilitate exposing your service privately.

- **VPC Lattice:** The AWS Gateway API Controller integrates with Amazon VPC Lattice, a fully managed application networking service that allows you to connect, secure, and monitor services across multiple VPCs and accounts. When you create Gateway API resources, the controller provisions corresponding resources in VPC Lattice, such as service networks and services.
- **Gateway Resource:** To expose your service, you will define a `Gateway` resource in your Kubernetes cluster, specifying the `amazon-vpc-lattice` `GatewayClass`. This `Gateway` will correspond to a VPC Lattice service network. You'll configure listeners on the `Gateway` to define the protocols (HTTP or HTTPS) and ports it will accept traffic on.
- **HTTPRoute Resource:** You will then create an `HTTPRoute` resource to define how traffic to the `Gateway` should be routed to your specific backend service within the EKS cluster. The `HTTPRoute` will specify matching rules based on hostnames, paths, and other criteria, directing traffic to the Kubernetes `Service` object that fronts your application.
- **Private Exposure:** Because you are using VPC Lattice within the same AWS account and region (as mentioned in the `getstarted.md`), the communication between your service and any clients accessing it through the VPC Lattice service network can remain entirely within your private AWS network. You can control access to your service network and services within VPC Lattice using security groups and potentially authentication policies.

**8. Troubleshooting Credential Issues:**

The fact that your controller pods are crashing due to missing/wrong credentials strongly suggests a problem with the IAM configuration you've set up for the controller. Double-check the following:

- **IAM Policy Content:** Ensure the IAM policy attached to the role has all the necessary permissions to interact with VPC Lattice. Refer to the `recommended-inline-policy.json` in the GitHub repository and the AWS Gateway API Controller documentation for the complete set of required permissions.
- **IAM Role Trust Relationship:** Verify that the trust relationship of the IAM role correctly allows the Kubernetes Service Account (if using IRSA) or the Pod Identity Agent (if using Pod Identities) to assume the role. The trust policy will reference either the OIDC provider of your EKS cluster (for IRSA) or the Pod Identity service principal.
- **Service Account Association:** Ensure that the AWS Gateway API Controller pods are indeed running under the Kubernetes Service Account you configured for IAM access (either through IRSA or Pod Identities). If using IRSA, the `eksctl create iamserviceaccount` command should have correctly annotated the Service Account. If using Pod Identities, the Pod Identity association must be correctly created.
- **Controller Deployment Configuration:** When deploying the controller (especially with Helm), make sure you are not inadvertently creating a new Service Account if you intend to use an existing one for IAM purposes.

By carefully reviewing and correcting your IAM setup based on the documentation and examples in the GitHub repository, you should be able to resolve the credential issues causing your controller pods to crash.

**Next Steps:**

I would strongly recommend the following as your next steps:

1. **Thoroughly review the IAM setup based on the AWS Gateway API Controller Deployment Prerequisites documentation and the `recommended-inline-policy.json` and trust policy examples in the GitHub repository.** Pay close attention to the specific ARNs and identifiers required in each step.
2. **Verify whether you intend to use Pod Identities or IRSA and ensure all the corresponding setup steps for your chosen method are completed accurately.**
3. **Double-check the namespace (`aws-application-networking-system`) and the creation of the `amazon-vpc-lattice` `GatewayClass`.**
4. **Review your controller installation method (Helm or kubectl) and ensure it's configured to use the Service Account you've associated with the IAM role.**
5. **Once the controller is running without crashing, proceed to define your `Gateway` and `HTTPRoute` resources to expose your specific service via VPC Lattice.**
6. **Consult the "Concepts" documentation () to deepen your understanding of how the AWS Gateway API Controller and VPC Lattice work together, especially in the context of private networking.**
7. **Refer to the example configurations in the GitHub repository ([https://github.com/aws/aws-application-networking-k8s]) for concrete implementations of `Gateway` and `HTTPRoute` resources.**

By systematically verifying each of these components, you should be able to get your Kubernetes Gateway API setup working correctly in your private EKS cluster. Let me know if you have more specific questions as you work through these steps.
