---
aliases: []
confidence: 
created: 2025-07-02T17:05:47Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:25Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: application entra
type:
uid: 
updated: 
version:
---

It sounds like you've successfully used Terraform to create your Entra application, which is a great step towards infrastructure as code! The challenge you're facing now, where the `email.send` API permission requires administrator approval, is a common one and stems from Microsoft Entra ID's robust consent framework designed to protect organizational data. Let's break down why this approval is needed and how you can automate it.

## Why Administrator Approval is Required for `email.send`

1. Consent Mechanism: In Microsoft Entra ID (formerly Azure Active Directory), applications need explicit permission (consent) to access protected resources like user data or organizational data [1, 2]. This consent can be granted by an individual user (user consent) or by an administrator (admin consent) [3].
   - User Consent: Users can generally authorize an application to access their own data or act on their behalf with "delegated permissions" [3].
   - Admin Consent: Many permissions, especially those that grant access to significant portions of an organization's data or allow highly privileged operations, require an administrator's approval [2-7]. This ensures that sensitive data isn't inadvertently exposed by individual users consenting to broad access. The `email.send` permission, which allows an application to send emails from your Microsoft 365 domain, falls into this category because it impacts organizational communication and could be used for spam or phishing if not properly controlled.

2. Types of Permissions:
   - Delegated Permissions: If your "Autho" application sends emails on behalf of a specific user, it would typically use delegated permissions.
   - Application Permissions (App Roles): If "Autho" sends emails without a user context (e.g., a background service sending notifications), it would need application permissions.
   - For Microsoft Graph API permissions (like `email.send`), even `Application Administrator` or `Cloud Application Administrator` roles cannot consent to all application permissions [8-10]. Permissions for Microsoft Graph often require a higher-privileged role like `Privileged Role Administrator` to grant consent [10, 11].

3. Application Configuration and Consent:
   - When an application is configured to "require user assignment," individual users are not allowed to consent to permissions for themselves, even if the permission would otherwise allow user consent. In such cases, an administrator must grant tenant-wide consent [12-14]. This might be contributing to why an admin is prompted for approval.
   - Microsoft Entra ID also has "risk-based step-up consent" which is enabled by default. If a consent request is deemed risky (e.g., for newly registered multi-tenant apps that are not publisher verified and require non-basic permissions), it automatically triggers a "step-up" to require admin consent [15, 16]. This could also be a reason for the approval prompt.

Your Terraform configuration successfully created the application object in Entra ID. However, creating the application object is distinct from granting that application the permissions it needs to access other resources, especially sensitive ones. The Service Principal or user account that Terraform uses to authenticate needs sufficient permissions itself to perform the consent operation on behalf of the organization.

## How to Automate Administrator Approval with Terraform

To automate the approval of the `email.send` API permission using Terraform, you need to ensure that the identity Terraform uses for authentication (a Service Principal or Managed Identity) has the necessary permissions to grant consent to such a sensitive permission.

Here's how you can set it up:

1. Choose the Right Authentication Method for Terraform Automation:
   - For non-interactive scenarios like CI/CD pipelines, Microsoft recommends using either a Service Principal or a Managed Identity for Terraform authentication [17-25]. These "workload identities" are designed for automation and are not affected by Multi-Factor Authentication (MFA) requirements that apply to user identities [25-27].
   - You can configure Terraform to use a Service Principal via environment variables (e.g., `ARM_CLIENT_ID`, `ARM_CLIENT_SECRET`, `ARM_TENANT_ID`) [28] or directly in the provider block (though environment variables are recommended for security) [29].
   - For Managed Identity, you'd set `ARM_USE_MSI` to `true` and specify the tenant ID [22, 30, 31].

2. Grant Necessary Permissions to Your Terraform Service Principal/Managed Identity:
   - This is the most critical step. The Service Principal (SP) or Managed Identity that Terraform uses to create and manage Azure AD objects must have sufficient permissions to grant "admin consent" for the `email.send` permission.
   - While `Application.ReadWrite.All` is generally required for Terraform to create and modify application objects themselves [32], it might not be sufficient to consent to all types of permissions, particularly sensitive Microsoft Graph permissions.
   - To grant tenant-wide admin consent for highly privileged Microsoft Graph permissions, the authenticated principal (your Terraform SP/Managed Identity) needs one of the following directory roles:
     - `Privileged Role Administrator`: This role has the ability to grant consent for any permission, for any API [11, 33, 34]. This is the most comprehensive role for granting consent to sensitive Microsoft Graph permissions like `email.send`.
     - `Global Administrator`: This role has full administrative access and can also grant consent [33, 35-37]. It's a highly privileged role, so it should be used with caution and limited to emergency scenarios or when no other existing role suffices [36, 37].
   - You would assign this role to the Service Principal object that represents your Terraform automation. This is done in the Azure Portal by navigating to Azure Active Directory > Enterprise Applications > (Your Terraform Service Principal) > Roles and Administrators > Add assignment and selecting the appropriate role [38-40].

3. Terraform Configuration to Request and Consent Permissions:
   - Once your Terraform Service Principal has the required elevated roles (e.g., `Privileged Role Administrator`), Terraform can then instruct the AzureAD provider to manage the required permissions and perform the admin consent.
   - Within your `azuread_application` resource block, you would define the `required_resource_access` block to specify the Microsoft Graph API and the `email.send` permission. The AzureAD provider, when run by a sufficiently privileged Service Principal, will then attempt to "grant admin consent" for these permissions.
   - Programmatically, the "Grant Admin Consent" button in the Azure portal for an application actually performs an `oauth2PermissionGrant` operation via the Microsoft Graph API [41, 42]. When your Terraform Service Principal has the necessary directory role, the AzureAD provider will execute the equivalent API calls.

Example Terraform Snippet (Conceptual - adapt to your actual configuration):

```terraform
resource "azuread_application" "autho_app" {
  display_name = "AuthoEmailSender"

  # ... other application properties ...

  required_resource_access {
    resource_app_id = "00000003-0000-0000-c000-000000000000" # Microsoft Graph API ID
    resource_access {
      id   = "c5393d2b-477b-409b-839e-31518f773cd6" # Replace with actual email.send scope ID for Microsoft Graph
      type = "Scope" # For delegated permission, or "Role" for application permission
    }
    # If using application permission (App Role) instead of delegated permission:
    # resource_access {
    #   id   = "..." # Replace with actual application permission ID for email.send
    #   type = "Role"
    # }
  }

  # Add owner to the application (recommended for management) [43-46]
  owners = [
    data.azuread_client_config.current.object_id # Object ID of the principal running Terraform
  ]
}

# Data source to get the object ID of the principal running Terraform
data "azuread_client_config" "current" {}

# You might also need to explicitly grant a delegated permission grant if your setup
# requires it, although required_resource_access combined with admin consent
# often suffices for most scenarios.
# resource "azuread_service_principal_delegated_permission_grant" "autho_email_send_grant" {
#   service_principal_id = azuread_application.autho_app.service_principal_id
#   principal_object_id  = data.azuread_client_config.current.object_id # Or the SPN of the Autho app if it's acting on its own behalf
#   resource_service_principal_id = "00000003-0000-0000-c000-000000000000" # Microsoft Graph API ID
#   scope_id = "c5393d2b-477b-409b-839e-31518f773cd6" # email.send scope ID
#   consent_type = "AllPrincipals" # For tenant-wide admin consent
# }
```

Note: The exact `id` (scope ID) for `email.send` needs to be retrieved from the Microsoft Graph API documentation for the specific Microsoft Graph permission you intend to use (e.g., `Mail.Send` delegated or application permission). The IDs provided in the source material [47-49] are examples or for general OAuth2 permission scopes, not necessarily specific to `Mail.Send`.

Important Security Consideration:

Granting a Service Principal or Managed Identity `Privileged Role Administrator` or `Global Administrator` role is a very high privilege. This should be done with extreme caution and only if absolutely necessary for your automation scenario. It grants the automated process extensive control over your Microsoft Entra ID tenant. Ensure your CI/CD environment and Terraform state files are highly secured.

Would you like me to help you find the specific `email.send` permission ID for Microsoft Graph, or perhaps delve into the security implications of granting elevated roles to your Terraform Service Principal?

Your query about the best practices for automation, particularly the balance between Service Principal (SP) privileges and human approval, touches upon core security and operational efficiency considerations in Microsoft Entra ID. It's an excellent question, as finding the right balance is crucial for secure and smooth development workflows.

Let's break down the best practices for automation, focusing on Service Principals (SPs) and Managed Identities, and how human approval mechanisms like the admin consent workflow and Privileged Identity Management (PIM) fit into the picture.

### Best Practices for Automation Authentication (e.g., Terraform in CI/CD)

For non-interactive automation, such as running Terraform in a CI server, Microsoft strongly recommends using either a **Service Principal** or a **Managed Identity** [1, 2]. Authenticating with the Azure CLI when running Terraform locally is recommended for interactive use [1, 2].

It's critical to **migrate away from using Azure CLI with an Entra ID user and password for automated processes**, especially if Multi-Factor Authentication (MFA) is enabled [3-5]. MFA disrupts non-interactive scripts because it requires user interaction [6, 7]. Workload identities like Service Principals and Managed Identities are designed for non-interactive automation scenarios and do not require MFA for authentication [4, 7-9].

1. **Embrace the Principle of Least Privilege:**
   This is the most fundamental security best practice [10-13]. When granting any identity, including a Service Principal or Managed Identity, permissions to access services, you should **always grant only the minimum permissions needed** to perform the desired actions [10]. For example, if an identity is used to read data from a storage account, it should not have permissions to write data to it [10]. Granting excessive permissions (e.g., making a Managed Identity a Contributor on an Azure subscription when not needed) significantly increases the security "blast radius" if that identity is compromised, leading to greater potential damage [10].

2. **Choose Between Service Principals and Managed Identities:**
   - **Service Principals (SPs):** These are essentially identities for applications. When configuring a Service Principal for managing Azure Active Directory, you must grant it the necessary permissions to create and modify Azure Active Directory objects such as users and groups [1, 2]. When authenticating using a service principal, Microsoft recommends **assigning permissions using app roles** rather than directory roles, especially when working with Microsoft Graph [14].
   - **Managed Identities:** These are Azure-managed identities for applications that eliminate the need to manage secrets, credentials, certificates, and keys [15].
     - **User-Assigned Managed Identities are Recommended:** For Microsoft services, user-assigned identities are generally the recommended type [16]. They are provisioned independently from compute resources and can be assigned to multiple resources, offering more efficiency across a broader range of scenarios [16-18]. Their lifecycle is decoupled from the resources they are associated with, allowing you to pre-configure them and their role assignments before the resources requiring them are deployed [18]. This also helps avoid rate limits for Microsoft Entra object creations if you're rapidly deploying many resources [19, 20].
     - **Direct Permission Assignment for Managed Identities (Crucial for Automation Efficiency):** While Managed Identities can be added to Microsoft Entra groups that have permissions, there's a **limitation**: changes to a Managed Identity's group or role membership can take **several hours** to propagate because these changes are expressed as claims in access tokens, which are cached [21, 22]. If this delay is unacceptable for your automation requirements, it is **recommended to group Azure resources using a user-assigned managed identity with permissions applied *directly to the identity***, rather than adding or removing the managed identities from a Microsoft Entra group that has permissions [22]. This ensures changes take effect more quickly [22].

### The Role of Human Approval

The question of human approval to limit SP privileges is central to a robust security posture. While direct, least-privilege permissions are best for *runtime automation*, human approval plays a vital role in the *initial setup, configuration changes, and highly sensitive operations*.

1. **Admin Consent Workflow:**
   This workflow allows users to provide a justification and request an administrator's review and approval for an application when they are unable to consent to the permissions themselves [23-28]. This is particularly relevant when:
   - An application requests permissions that regular users are not allowed to grant (e.g., tenant-wide access) [23, 29].
   - User consent is disabled in your tenant, preventing users from consenting to new applications on their own [25, 30, 31].
   - A "risky" user consent request is detected by Microsoft Entra ID Protection; such requests require a "step-up" to admin consent [32-35].
   - **Process:** When a user attempts to sign in to an application requiring admin consent, an "Approval required" message appears. The user can then submit a request to designated administrators/reviewers, who receive notifications [24, 28, 36-39]. Administrators can then review the requested permissions, application details, and justification before approving, denying, or blocking the request [40, 41].
   - **Granular Control:** Even after an administrator grants tenant-wide admin consent, user access to the application can still be limited by configuring the application to require user assignment [23, 42-46]. This means only assigned users (or groups) can sign in.
   - **Trust is Key:** Granting tenant-wide admin consent is a sensitive operation, as it can give the application publisher access to significant organizational data or highly privileged operations [47-49]. Administrators should carefully review the permissions and *trust the application and its publisher* before granting consent [47, 48, 50, 51].

2. **Privileged Identity Management (PIM):**
   While primarily for human administrators, PIM introduces the concept of "just-in-time" (JIT) access and approval workflows that are highly relevant to controlling privileges.
   - **Just-in-Time Access:** PIM allows you to grant time-limited access to roles, rather than permanent access, and requires activation when needed [52-55]. This significantly reduces the "standing access" of highly privileged accounts.
   - **Approval for Role Assignments:** PIM allows you to make a group eligible for a role assignment, and Microsoft recommends requiring an **approval process for eligible member assignments** [56]. This means that for sensitive roles, a human approval step can be mandated before a user (or a member of a group) can activate that privileged role.
   - **PIM for Groups:** You can use PIM for Groups to activate multiple roles at once. A user can be an eligible member or owner of a PIM group, and with one activation, they gain access to all linked resources, potentially subject to approval [57].

3. **Protected Actions:**
   This is a newer feature that allows you to assign Conditional Access policies to specific, high-impact permissions [58, 59]. When a user attempts to perform a *protected action*, they must satisfy the Conditional Access policies assigned to those permissions *at the time of the action* [58, 60].
   - **Dynamic Enforcement:** This means a user might have the permission assigned, but if the action is protected, they might be prompted for additional security (e.g., phishing-resistant MFA, access from a Privileged Access Workstation) [59, 60].
   - **Complementary to PIM:** Protected Actions enforce policies when an action is performed, while PIM enforces policies when a role is activated. They can be used together for stronger coverage [61, 62].

### Balancing Security and Convenience: The "Inconvenience"

The "inconvenience of human approval" is a trade-off for enhanced security.

- **For Initial Setup and Major Changes:** For the initial configuration of Service Principals or Managed Identities and any subsequent changes to their high-privilege permissions (e.g., granting `Application.ReadWrite.All`), **human approval (e.g., via the admin consent workflow)** is highly advisable. This allows security administrators to meticulously review the requested permissions and ensure they align with the principle of least privilege, preventing potential elevation of privilege [47-49, 51, 63, 64].
- **For Automated Runtime Operations:** Once Service Principals or Managed Identities are configured with carefully scoped, least-privilege permissions, the goal for day-to-day automation (like Terraform applying infrastructure changes) is to **minimize direct human intervention for every execution**. This is where assigning permissions directly to a **User-Assigned Managed Identity** (rather than relying heavily on group membership for the identity itself, due to token caching delays) becomes a best practice [22]. The "approval" is baked into the initial, reviewed permission grant to the identity, allowing the automation to run efficiently.
- **For Human Administrators:** For human administrators managing resources, **PIM** can introduce a controlled "inconvenience" (activating a role, potentially requiring approval) that significantly enhances security by limiting standing access [53]. Similarly, **Protected Actions** introduce "inconvenience" by requiring stronger authentication for sensitive operations, making it harder for compromised credentials to perform high-impact actions [58, 60].

In conclusion, while the idea of nesting groups for human users (like a "developer" group containing tool-specific groups) simplifies initial assignment, its limitations for application role assignments and provisioning mean it might not fully achieve single-point access for all tools via SSO. For automated processes like Terraform, utilizing **User-Assigned Managed Identities with directly assigned, least-privilege permissions** is the recommended best practice for efficiency and security, circumventing the need for repetitive human approval for every automated task execution. However, the **initial configuration and any escalations of these identity's permissions should absolutely go through a rigorous human approval process**, leveraging features like the admin consent workflow and PIM for privileged access where applicable.
