---
aliases: []
confidence: 
created: 2025-07-02T03:55:27Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:25Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: High-Level Overview of Entra Application Identity
type:
uid: 
updated: 
version:
---

Microsoft Entra ID is an Identity and Access Management (IAM) system designed to provide a central repository for digital identities. Application management in Microsoft Entra ID involves creating, configuring, managing, and monitoring applications in the cloud.

At its core, an application within Microsoft Entra ID is defined by two key objects:

1. Application object: This represents the application itself in your Microsoft Entra tenant. It's essentially the global definition of your software.
2. Service principal object: This is an instance of the application object within a specific tenant. It dictates how the application can access resources within that tenant. There's typically one application object but potentially multiple service principal objects for your application.

These application identities are used for several crucial purposes:

Secure Access: Once an application is registered, assigned users can securely access it.

Single Sign-On (SSO): Microsoft Entra ID enables users to sign in once with one set of credentials to access multiple independent software systems. This eliminates the need for users to log into every application separately. Entra ID supports various SSO methods, including SAML, OpenID Connect (OIDC), password-based, and linked SSO. Federated SSO, especially via SAML 2.0 or OpenID Connect, is considered the richest mode.

Automated User Provisioning: Application identities allow for the automatic creation, maintenance, and removal of user identities and roles in connected applications as user status or roles change.

Access Management: You can manage who has access to an application by assigning users and groups. This can be done through individual assignments or group-based assignments (which require a Microsoft Entra ID P1 or P2 license).

Security: Application identities are integral to implementing security features like multi-factor authentication (MFA) and Conditional Access policies, ensuring secure access to data and applications.

Ownership and Governance: You can assign owners to applications to manage their configuration, including SSO and provisioning. This ensures proper oversight and governance of your applications.

Microsoft Entra ID supports various types of applications, including thousands of pre-integrated applications from the Microsoft Entra gallery that can be set up with minimal effort. You can also register your own custom business applications or connect to on-premises applications using tools like Microsoft Entra application proxy.

## Entra as a Central Identity Manager for GitLab, Terraform Cloud, and Auth0

Microsoft Entra ID can serve as your central identity manager by providing a single place to store and manage digital identities for various applications, including those used by your small developer team like GitLab, Terraform Cloud, and Auth0.

Here's how this centralization is achieved:

Single Sign-On (SSO) Integration: You can configure your third-party applications (like GitLab or Auth0) to use Microsoft Entra ID as their primary identity provider for authentication. This means your developers would sign into all these tools using their existing Microsoft Entra credentials, leveraging federated SSO protocols like SAML 2.0 or OpenID Connect. If Auth0 acts as an identity provider, you can also configure Microsoft Entra ID to federate with it via Home Realm Discovery.

Automated User Provisioning: For applications that support it, Microsoft Entra ID can automatically create, update, and remove user accounts and roles within those applications (e.g., GitLab). This streamlines user lifecycle management across all integrated services.

Centralized Access Control: Instead of managing user access in each application independently, you can manage user and group assignments within Microsoft Entra ID. This allows you to apply consistent access policies, leveraging Microsoft Entra groups to simplify assignments for large numbers of users.

Enhanced Security Policies: By centralizing identity in Entra ID, you can enforce organization-wide security policies such as multi-factor authentication and Conditional Access. This means that if a developer tries to access GitLab, for example, they might be prompted for MFA based on a Conditional Access policy configured in Entra ID, even if GitLab itself doesn't directly enforce MFA.

## Managing Entra Users via Terraform for a GitOps User Management Flow

Your goal to manage Entra users via Terraform to create a GitOps user management flow is well-supported. Terraform is a popular Infrastructure-as-Code (IaC) tool that can interact with Azure (including Microsoft Entra ID) to manage resources declaratively.

Here’s how you can achieve this:

Terraform Authentication to Azure: Terraform offers several methods to authenticate to Azure, which are crucial for your GitOps pipeline:

Azure CLI authentication.

Managed Identity authentication. This is particularly relevant for CI/CD environments as it eliminates the need to manage credentials directly in your code. Managed identities can also be used as Federated Identity Credentials (FIC) for Microsoft Entra ID applications, allowing workloads to obtain Microsoft Entra tokens without managing secrets. This fits perfectly with a GitOps approach, as your CI/CD pipeline (e.g., in GitLab CI/CD) could use a managed identity to authenticate to Entra ID and perform operations.

Service Principal with Client Secret or Certificate.

Service Principal with OpenID Connect.

Managing Entra Objects with Terraform: Terraform allows you to create and modify Azure Active Directory (now Entra ID) objects, such as applications, users, and groups.

Application Management (`azuread_application`): The `azuread_application` resource in Terraform is used to manage application registrations in Microsoft Entra ID. You can define attributes like `display_name`, `client_id`, `identifier_uris`, `app_roles`, `owners`, and `required_resource_access`. This allows you to codify your application registrations.

Federated Identity Credentials (`azuread_application_federated_identity_credential`): For enhanced security and to avoid secrets in your GitOps pipeline, you can use `azuread_application_federated_identity_credential`. This resource manages federated identity credentials for applications, allowing them to trust tokens from external identity providers (like your CI/CD system) to obtain Microsoft Entra access tokens without managing secrets. This means your GitLab CI/CD pipeline could be configured to obtain Entra ID tokens directly, enabling it to manage users and applications through Terraform.

User and Group Management: While the provided excerpts focus heavily on application management, the underlying concept of Terraform managing "Azure Active Directory objects such as users and groups" is explicitly stated. This means you can use Terraform to define desired states for your Entra users and groups, including their attributes and memberships, and then apply these configurations through your GitOps pipeline. This allows you to version control your user and group configurations, enabling auditability and automated deployments.

Role-Based Access Control (RBAC) and Custom Roles:

Terraform can be used to assign roles to users, groups, or service principals. For a GitOps flow, you would define these role assignments in your Terraform code.

You can create custom roles with specific, least-privileged permissions for your GitOps service principal (the identity Terraform uses). For example, a custom role could be designed to only allow the creation and management of users and groups, without broader administrative permissions. Users in a custom role can be assigned permissions over a specific application or at the directory scope.

Using role-assignable groups (requires Microsoft Entra ID P1 or P2 license) allows you to assign Entra roles to groups, simplifying management as you can add or remove users from the group to grant/revoke access to the role. This is a great fit for GitOps, where group membership changes can trigger automated updates.

By combining Entra ID's capabilities for centralized identity and application management with Terraform's IaC approach and the use of federated identity credentials, your small developer team can establish a robust and secure GitOps flow for managing all user access across your tools, including GitLab, Terraform Cloud, and Auth0.

Would you like me to elaborate on the different authentication methods Terraform can use with Entra ID, or perhaps explain how to structure your Terraform configuration for managing users and groups?

### How a Microsoft Entra Application Relates to the SSO Process for GitLab

At its core, for an application like GitLab to use Microsoft Entra ID for SSO, it needs to be represented and configured within your Microsoft Entra tenant. This representation is primarily handled through an **application object** and a **service principal object**.

Here's how these elements work together to facilitate SSO for GitLab:

1. **The Application and Service Principal Objects in Entra ID**
   - An **application object** in Microsoft Entra ID serves as the global definition of your software. It resides in the tenant where the application is registered.
   - A **service principal object** is an instance of the application object within a specific tenant. It dictates how the application can access resources within that tenant. You'll typically have one application object, but potentially multiple service principal objects if your application is used in different tenants.
   - For GitLab to leverage Microsoft Entra ID for SSO, you essentially "register" or "integrate" GitLab as an application within your Microsoft Entra tenant, which creates these objects.

2. **Enabling Single Sign-On (SSO) for GitLab**
   - **What is SSO?** Single sign-on is an authentication method that allows users to sign in once with one set of credentials to access multiple independent software systems, eliminating the need to log into every application separately.
   - **SSO Options**: Microsoft Entra ID supports various SSO methods for cloud applications, including federation-based options like **SAML (Security Assertion Markup Language)** and **OpenID Connect (OIDC)**. These are the most common and "richest" modes for integrating third-party SaaS applications like GitLab. Password-based SSO and Linked SSO are also available for different scenarios.
   - **Integrating GitLab**: You would configure GitLab to use Microsoft Entra ID as its identity provider (IdP) for authentication. This means when a user tries to access GitLab, GitLab (as the service provider, SP) redirects the user's authentication request to Microsoft Entra ID.

3. **The SSO Process (SAML/OpenID Connect) in Detail**
   - **SAML-based SSO (Common for SaaS Apps like GitLab)**:
     - Many SaaS applications are preintegrated in the Microsoft Entra gallery and can be set up with minimal effort. You can also integrate non-gallery SAML applications.
     - When configuring SAML-based SSO, Microsoft Entra ID acts as the **Identity Provider (IdP)** and GitLab acts as the **Service Provider (SP)**.
     - The configuration involves setting key values:
       - **Identifier (Entity ID)**: This is a unique URL specific to the application (GitLab in this case) that identifies it to Microsoft Entra ID. Microsoft Entra ID uses the issuer (which is typically the Identifier) to find the application in your directory.
       - **Reply URL (Assertion Consumer Service URL)**: This is the URL of GitLab where Microsoft Entra ID sends the authenticated user and the SAML token after successful sign-in. It must be an HTTPS URL for secure transfer of SAML tokens.
       - **Sign-on URL**: This is the URL where users initiate the sign-on flow from GitLab (SP-initiated flow).
     - **Authentication Flow**: When a user attempts to sign in to GitLab (the SP), GitLab redirects them to Microsoft Entra ID (the IdP) for preauthentication. Microsoft Entra ID then processes any Conditional Access policies and authenticates the user using their Microsoft Entra account. Upon successful authentication, Microsoft Entra ID issues a **SAML token** (also called a SAML assertion). This token is signed with a unique certificate generated by Microsoft Entra ID. The user's browser redirects back to GitLab with this SAML token, and GitLab validates the token and signs the user in.
   - **OpenID Connect (OIDC)-based SSO**:
     - OIDC is an authentication protocol built on top of OAuth 2.0, an authorization protocol. When a user tries to log in, OIDC verifies their identity based on authentication performed by an authorization server (Microsoft Entra ID). Once authenticated, OAuth 2.0 grants the application (GitLab) access to user's resources without exposing credentials.
     - When adding an OIDC application, you might be redirected to the application's sign-in/sign-up page to complete the setup process. The application is then added to your tenant.
     - OIDC also relies on tokens (ID tokens and access tokens) issued by Microsoft Entra ID.

4. **Key Configuration Aspects for the Entra Application**
   - **User and Group Assignment**: To control who can access GitLab via Entra SSO, you assign users and/or groups to the enterprise application in Microsoft Entra ID. If the application is configured to require user assignment, only assigned users can sign in. Group-based assignment, which requires a Microsoft Entra ID P1 or P2 license, is an efficient way to manage access for teams.
   - **Certificates**: For SAML SSO, Microsoft Entra ID generates a self-signed certificate (valid for three years by default) to sign the SAML response. It's crucial to manage the lifetime of this certificate and have a process for renewal to prevent outages. You can also configure token encryption for added security.
   - **User Experience (My Apps Portal)**: Once configured, users can access GitLab from the Microsoft Entra My Apps portal, which provides a single place for them to view and launch all applications they have access to. Direct sign-on links can also be used.

In essence, the Microsoft Entra application object and its associated service principal object define GitLab within your Entra ID tenant. Through careful configuration of SSO (likely SAML or OIDC), certificate management, and user/group assignments, Microsoft Entra ID becomes the central authentication authority for GitLab, allowing your developers to use their existing Entra credentials seamlessly.
