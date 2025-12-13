---
aliases: []
confidence: 
created: 2025-03-10T04:26:20Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [azure, IAM]
title: Bootstrapping an Azure Tenant and Entra Instance with GitOps and Least Privilege
type: plan
uid: 
updated: 
version: 1
---

This article provides a comprehensive guide to bootstrapping an Azure tenant and an Entra ID (formerly Azure AD) instance using GitOps principles and adhering to the principle of least privilege. We will cover the initial account setup, securing the root identity, creating necessary identities for your development team, and bootstrapping the environment with GitOps.

## The Principle of Least Privilege

Before diving into the specifics, it's crucial to understand the core concept of least privilege. This security principle dictates that every user and application should have only the minimum necessary permissions to perform their tasks. This minimizes the potential damage from compromised accounts and helps maintain a secure environment. In the context of Azure, least privilege can be achieved through various means, such as:

- **Azure RBAC:** Azure role-based access control (RBAC) allows you to assign granular permissions to users and groups based on their roles and responsibilities.
- **Just-in-Time Access:** Granting temporary access to resources only when needed, instead of providing permanent privileges.
- **Regular Permission Reviews:** Periodically reviewing and revoking unnecessary permissions to ensure that access remains aligned with current needs.

By adhering to the principle of least privilege throughout the bootstrapping process, you establish a strong security foundation for your Azure tenant.

## Setting up the Initial Account with Least Privilege

When setting up your initial Azure account, it's essential to start with a secure configuration. According to Azure documentation, you should follow these practices:

- **Limit Subscription Owners:** Minimize the number of subscription owners to a maximum of three. This reduces the risk associated with a compromised owner account.
- **Assign Roles to Groups:** Instead of assigning roles directly to users, create groups and assign roles to those groups. This simplifies management and reduces the number of individual role assignments.

Furthermore, to bootstrap an Azure tenant, a user with Global Administrator privileges needs to elevate their access to grant themselves the "User Access Administrator" permission at the tenant root scope. This can be achieved using Azure CLI or PowerShell. For example, using Azure CLI, you can execute the following command:

Code snippet

```sh
az role assignment create --assignee <user-principal-name> --role "User Access Administrator" --scope "/"
```

This command assigns the "User Access Administrator" role to the specified user at the tenant root scope ("/").

![[Securing the Root Identity]]

## Understanding Azure AD Roles

Azure AD offers a variety of built-in roles with specific permissions to manage different aspects of your tenant. Understanding these roles is essential for assigning the appropriate permissions to your development team. Here's a table summarizing some key Azure AD roles:

|   |   |
|---|---|
|**Role Name**|**Permissions**|
|Application Administrator|Manage all aspects of enterprise applications, application registrations, and application proxy settings.|
|Cloud Application Administrator|Consent to application permissions, manage application proxy, and create application registrations.|
|User Administrator|Create, update, and delete users, assign licenses, and manage user attributes.|
|Groups Administrator|Create and manage groups, manage group settings, and control group expiration.|
|Security Administrator|Manage security-related features, such as password protection and smart lockout.|
|Global Reader|Read all configurations and access directory data.|
|Hybrid Identity Administrator|Manage hybrid identity features, such as Azure AD Connect and pass-through authentication.|

This is not an exhaustive list, and you can find more details about Azure AD roles and their permissions in the Microsoft Entra documentation.

## Creating Identities for the Dev Team with Least Privilege

When creating identities for your development team, it's essential to grant them only the permissions they need to perform their tasks. Here's how you can achieve this:

- **Define Roles Based on Tasks:** Identify the specific tasks that your developers need to perform and assign roles with the corresponding permissions.
- **Use Managed Identities:** Managed identities provide an automatically managed identity in Azure AD for applications to use when connecting to resources that support Azure AD authentication. This eliminates the need to manage credentials9.
- **Assign Roles with the Least Privilege:** Grant the minimum necessary permissions required for each role10.
- **Regularly Review Permissions:** Periodically review the permissions assigned to your development team and revoke any unnecessary access10.
- **Understand Consent:** Most applications require access to protected data, and the owner of that data needs to consent to that access. Consent can be granted by a tenant administrator for all users or by individual users.

While both system-assigned and user-assigned managed identities are available, user-assigned managed identities offer greater flexibility. They can be associated with multiple Azure resources and have an independent lifecycle, making them more suitable for most scenarios10.

Many Azure services support managed identities, including:

- Azure Virtual Machines
- Azure App Service
- Azure Functions
- Azure Kubernetes Service
- Azure Key Vault
- Azure Storage
- Azure SQL Database 9

By using managed identities and adhering to the principle of least privilege, you can ensure that your developers have the appropriate access to resources while minimizing security risks.

## Best Practices for Secure Identity Governance

Identity governance plays a crucial role in maintaining a secure Azure environment. Here are some best practices to consider:

- **Least Privilege:** As discussed earlier, grant users and applications only the minimum necessary permissions to perform their tasks.
- **Prevent Lateral Movement:** Implement measures to restrict the ability of compromised accounts to move laterally within your environment and gain access to other resources.
- **Deny by Default:** Start with a deny-by-default approach, where access to resources is restricted by default unless explicitly granted.
- **Defense in Depth:** Employ multiple layers of security, such as MFA, PIM, and Conditional Access, to protect your identities and resources11.

These practices help establish a robust security posture for your Azure tenant.

## Bootstrapping with GitOps

GitOps is a modern approach to managing infrastructure and applications that uses Git as the single source of truth. It leverages Git's version control capabilities to automate deployments and ensure consistency across environments.

Here's how you can bootstrap your Azure tenant and Entra instance using GitOps:

- **Choose a GitOps Tool:** Select a GitOps tool such as Flux or Argo CD. Flux is a popular open-source toolset that integrates well with Azure12.
- **Define Your Infrastructure as Code:** Use Infrastructure as Code (IaC) tools like Terraform or Bicep to define your Azure resources and Entra configurations in a declarative manner13.
- **Store Your Code in a Git Repository:** Store your IaC code and configuration files in a Git repository. This serves as the single source of truth for your environment14.
- **Automate Deployments with CI/CD:** Set up a CI/CD pipeline to automate the deployment of your infrastructure and Entra configurations from your Git repository14.

For example, you can use Flux to manage the deployment of your Azure Kubernetes Service (AKS) cluster. Here's a basic example of a Flux configuration file:

YAML

```sh
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: GitRepository
metadata:
  name: my-cluster-config
spec:
  interval: 5m0s
  ref:
    branch: main
  url: <your-git-repository-url>

---
apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
kind: Kustomization
metadata:
  name: my-cluster
spec:
  interval: 5m0s
  path: ./cluster
  prune: true
  sourceRef:
    kind: GitRepository
    name: my-cluster-config
  targetNamespace: flux-system
```

This configuration defines a Git repository as the source for your cluster configuration and instructs Flux to apply the Kustomization located in the `./cluster` path of the repository.

The Azure landing zone portal accelerator can further simplify the bootstrapping process. It allows you to bootstrap an entire Azure tenant without any infrastructure dependencies4.

## Tools and Technologies

Several tools and technologies can help automate the process of bootstrapping and securing your Azure tenant:

- **Azure CLI:** The Azure CLI provides a command-line interface for managing Azure resources13.
- **Azure PowerShell:** Azure PowerShell offers a set of cmdlets for managing Azure resources using PowerShell.
- **Terraform:** Terraform is an open-source IaC tool that allows you to define and provision infrastructure across various cloud providers, including Azure13.
- **Azure Automation:** Azure Automation provides a cloud-based automation service for automating various tasks in Azure. It offers features like: 15
    - **Schedules:** Trigger automation operations at predefined times.
    - **Modules:** Manage Azure and other systems using pre-built or custom modules.
    - **Credentials:** Securely store sensitive information that runbooks can use at runtime.
    - **Connections:** Store connection information for various systems.

These tools and technologies can be used with GitOps to streamline the bootstrapping process and ensure the security of your Azure tenant.

## Summary

Bootstrapping an Azure tenant and Entra instance with GitOps and least privilege involves several key steps:

1. **Establish a Secure Foundation:** Set up your initial account with limited privileges and secure the root identity using MFA, PIM, and other security measures.
2. **Understand Azure AD Roles:** Familiarize yourself with the different Azure AD roles and their permissions to assign appropriate access to your development team.
3. **Create Identities for the Dev Team:** Utilize managed identities and adhere to the principle of least privilege when creating identities for your developers.
4. **Bootstrap with GitOps:** Choose a GitOps tool like Flux, define your infrastructure as code, and automate deployments with CI/CD.
5. **Leverage Tools and Technologies:** Utilize tools like Azure CLI, Azure PowerShell, Terraform, Bicep, and Azure Automation to streamline the process.

By following these steps and adhering to security best practices, you can create a secure and efficient Azure environment for your organization. For further reading, refer to the Microsoft Entra documentation and Azure security best practices.

Bootstrapping an Azure tenant and Microsoft Entra ID (formerly Azure Active Directory) instance using GitOps principles while adhering to the principle of least privilege involves several key steps:

1. **Establish the Initial Account**:

    - Create the initial Global Administrator account in your Azure tenant. This account has full access and is necessary for the initial setup.
2. **Secure the Root Identity**:

    - Enable Multi-Factor Authentication (MFA) for the Global Administrator account to enhance security.
    - Utilize Microsoft Entra Privileged Identity Management (PIM) to implement just-in-time access, reducing the risk of standing administrative privileges.
3. **Implement GitOps for Configuration Management**:

    - Adopt GitOps practices by storing your Azure configurations as code in a Git repository.
    - Use tools like Azure DevOps or GitHub Actions to automate the deployment and management of Azure resources, ensuring that all changes are version-controlled and auditable.
4. **Assign Least Privilege Roles to the Development Team**:

    - Define roles and permissions based on the specific tasks that team members need to perform.
    - Assign the least privileged roles necessary for each task to minimize security risks. For example, if a developer needs to manage applications, assign the "Application Administrator" role rather than the more permissive "Global Administrator" role.
5. **Regularly Review and Audit Permissions**:

    - Conduct periodic reviews of role assignments to ensure that permissions align with current job responsibilities.
    - Utilize access reviews in Microsoft Entra ID Governance to facilitate these audits.

By following these steps, you can effectively bootstrap your Azure tenant and Microsoft Entra ID instance using GitOps principles while maintaining a security posture that aligns with the principle of least privilege.
