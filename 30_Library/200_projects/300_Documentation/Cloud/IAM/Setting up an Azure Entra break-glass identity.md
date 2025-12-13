---
aliases: []
confidence: 
created: 2025-03-21T10:00:11Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:50Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [access-control, entra, IAM]
title: Setting up an Azure Entra break-glass identity
type: plan
uid: 
updated: 
version: 
---

Setting up an Azure Entra break-glass identity is crucial for maintaining access to your tenant in emergency situations. Here's a breakdown of best practices and essential properties for a robust break-glass account:

**Core Principles:**

- **Minimize Usage:** Break-glass accounts should be used *only* when absolutely necessary, such as when all other administrative accounts are inaccessible
- **Strict Control:** Implement rigorous controls around the account's credentials and usage.
- **Auditing and Monitoring:** Thoroughly audit and monitor all activity performed by the break-glass account
- **Separation of Duties:** The break-glass account should be distinct from regular administrative accounts.

**Best Practices:**

1. **Dedicated Account:**

    - Create a dedicated cloud-only account solely for break-glass purposes. Avoid using personal accounts or accounts synchronized from on-premises Active Directory.
    - Name the account clearly, such as "BreakGlassAdmin" or "EmergencyAdmin," to indicate its purpose
2. **Strong and Unique Credentials:**

    - Generate a long, complex, and unique password. Store it securely in a dedicated password vault or hardware security module (HSM).
    - Consider using a passphrase instead of a traditional password for added complexity.
    - **No MFA:** Do not enable multi-factor authentication (MFA) for the break-glass account. The purpose is to allow access when normal MFA methods are unavailable. This is a risk, so all other security precautions must be increased to compensate.
3. **Minimal Permissions (Just Enough):**

    - While Global Administrator is often the default, carefully evaluate whether it's truly necessary. Consider using a custom role with the absolute minimum permissions required to recover access.
    - If you must use Global Admin, be sure that you have clear procedures for how to remove that role after the emergency is resolved.
    - Consider using Privileged Identity Management (PIM) to elevate the break glass account to global admin just in time
4. **Secure Storage of Credentials:**

    - Store the credentials in a physically secure location, such as a locked safe or a dedicated hardware security module (HSM)
    - Implement strict access controls to the storage location.
    - Consider distributing parts of the credentials to multiple trusted individuals, requiring a quorum to access them.
    - Create a physical document that details the steps to take to access the break glass account, and store it with the credentials.
5. **Regular Testing:**

    - Periodically test the break-glass account to ensure it functions correctly and that the credentials are valid
    - Simulate emergency scenarios to validate the recovery process.
    - Document the results of the tests.
6. **Comprehensive Auditing:**

    - Enable audit logging for the break-glass account and monitor it closely
    - Set up alerts to notify administrators of any activity performed by the account.
    - Review audit logs after each use.
7. **Documentation:**

    - Create detailed documentation outlining the purpose of the break-glass account, its credentials, and the recovery process.
    - Include instructions on how to use the account and how to revert any changes made.
8. **Privileged Identity Management (PIM):**

    - Integrate the break-glass account with Azure AD Privileged Identity Management (PIM) to require justification and approval for its use.
    - Set up time-bound activation for the account's permissions.
    - Require MFA for the PIM activation process (but not for the breakglass account itself). This means that to elevate the breakglass account, an admin with MFA must approve the elevation.

**Essential Properties:**

- **Account Name:** Clear and descriptive (e.g., "BreakGlassAdmin").
- **Password:** Long, complex, and unique.
- **Role:** Ideally a custom role with minimal permissions, or Global Administrator (with PIM).
- **Storage Location:** Physically secure and access-controlled.
- **Audit Logging:** Enabled and monitored.
- **Documentation:** Comprehensive and up-to-date.
- **Recovery Steps:** Detailed instructions for using the account.
- **No MFA:** MFA must be disabled for the account itself
- **Cloud Only:** The account must be cloud only.

**Example Scenario:**

1. Create a cloud-only account named "BreakGlassAdmin."
2. Generate a strong, unique passphrase.
3. Store the passphrase in a locked safe, with a copy distributed to two trusted individuals.
4. Assign the account the Global Administrator role (ideally, a custom role with minimal permissions).
5. Enable audit logging for the account.
6. Document the recovery process, including instructions on how to access the credentials and use the account.
7. Test the account periodically.
8. Implement PIM for the account, requiring justification and approval for its use.
9. After use of the break glass account, reset the password immediately, and review all audit logs.
10. Ensure that any elevated privledges are removed as soon as possible.

By following these best practices, you can create a secure and effective break-glass identity for your Azure Entra environment.

Yes, you absolutely should minimize the number of Global Administrator accounts in your Azure Entra (Azure AD) environment. Ideally, you should aim for **zero** standing Global Administrator accounts for regular day-to-day operations.

**Why Minimize Global Admins?**

- **Increased Security Risk:** Global Administrator accounts have unrestricted access to your entire Azure Entra tenant If compromised, an attacker can cause significant damage
- **Reduced Auditability:** With multiple Global Administrators, it becomes harder to track who made what changes.
- **Compliance Requirements:** Many compliance frameworks require organizations to implement least privilege

**Running a Least Privilege System in Azure Entra:**

Here's how to implement a least privilege system:

1. **Identify and Document Roles:**

    - Create a comprehensive list of all administrative tasks performed in your Azure Entra environment.
    - Map these tasks to the corresponding Azure Entra roles.
2. **Use Built-in Roles:**

    - Leverage Azure Entra's built-in roles whenever possible. These roles provide granular permissions for specific tasks
    - Examples:
        - User Administrator: Manages user accounts.
        - Conditional Access Administrator: Manages Conditional Access policies
        - Exchange Administrator: Manages Exchange Online
        - SharePoint Administrator: Manages SharePoint Online
        - Intune Administrator: Manages Intune
    - Find the role that fits the job, and use that role.
3. **Create Custom Roles (If Necessary):**

    - If a built-in role doesn't meet your needs, create custom roles with the precise permissions required
    - Start with the least privilege possible and add permissions as needed.
4. **Implement Privileged Identity Management (PIM):**

    - Use PIM to grant just-in-time access to privileged roles
    - Require justification and approval for role activation.
    - Set time-bound activation periods.
    - Enforce MFA on PIM elevation.
    - PIM allows for auditing all role elevation actions
5. **Regular Access Reviews:**

    - Conduct regular access reviews to ensure that users and groups have the appropriate permissions.
    - Remove unnecessary permissions.
6. **Conditional Access:**

    - Use Conditional Access policies to enforce granular access controls based on factors like:
        - User location.
        - Device compliance.
        - Application.
        - Risk level.
    - This is a strong way to add layers of protection to your environment.
7. **Break-Glass Account (As Discussed):**

    - The break-glass account should be the *only* standing Global Administrator account (or an account that can be elevated to Global Admin via PIM).
    - Follow the best practices outlined in the previous response.
8. **Automation:**

    - Automate user and group provisioning and deprovisioning to reduce the risk of human error and ensure consistency
    - Automate access reviews.
9. **Monitoring and Auditing:**

    - Continuously monitor Azure Entra audit logs for suspicious activity.
    - Set up alerts to notify administrators of potential security threats
    - Integrate Azure Entra logs with your SIEM (Security Information and Event Management) system

**Key Principles for Least Privilege:**

- **Need to Know:** Grant access only to the resources that users and groups need to perform their job duties.
- **Need to Do:** Grant permissions only for the specific actions that users and groups need to perform.
- **Just-in-Time Access:** Grant temporary access to privileged roles when needed.

By implementing these best practices, you can significantly reduce the risk of security breaches and ensure that your Azure Entra environment is secure and compliant.

This is an excellent approach to managing privileged access using GitOps and Terraform Cloud. Here's a breakdown of how to secure the Terraform Cloud identity while granting it the necessary permissions for Entra user management, along with considerations for your proposed workflow:

**Securing the Terraform Cloud Identity:**

1. **Service Principal:**

    - Create a dedicated Azure Entra service principal specifically for Terraform Cloud. This service principal will act as the identity that Terraform uses to authenticate with Azure.
    - Avoid using personal accounts or managed identities for Terraform Cloud.
2. **Least Privilege Role Assignment:**

    - Grant the service principal the absolute minimum permissions required to manage users and roles in Azure Entra.
    - **Custom Roles are Key:** Create a custom Azure Entra role that includes only the necessary permissions. Avoid assigning the Global Administrator role.
    - Permissions to consider:
        - `Microsoft.Directory/users/ReadWrite` (or more granular permissions for specific user attributes)
        - `Microsoft.Directory/roleAssignments/ReadWrite`
        - `Microsoft.Directory/directoryRoles/Read`
        - If using PIM, you will need permissions related to the PIM API.
        - You may need permissions relating to groups depending on your implementation.
    - Scope the role assignment to the specific Azure Entra resources that Terraform Cloud needs to manage.
3. **Azure AD Application Registration:**

    - Register an application in Azure Entra to represent the Terraform Cloud service principal.
    - Generate a client secret for the application.
    - Store the client secret securely in Terraform Cloud's variable settings. **Do not store it in your Git repository.**
    - Use the Application ID and Client Secret in your Terraform Azure Provider configuration.
4. **Terraform Cloud Workspace Variables:**

    - Securely store the Azure Entra application ID, client secret, and tenant ID as environment variables in your Terraform Cloud workspace.
    - Mark these variables as sensitive to prevent them from being displayed in plain text.
5. **Managed Identities (Optional, but complex):**

    - While you can use Azure Managed Identities with Terraform Cloud, it adds significant complexity. Terraform Cloud needs to be able to run in Azure to use them. Service principals are the more common and recommended method.

**Implementing Your GitOps Workflow:**

1. **User Repository (UserRepo):**

    - Create a dedicated Git repository (UserRepo) to store the Terraform configuration for user and role management.
    - Structure the repository to represent the desired state of your Azure Entra users and roles.
    - Use a clear and consistent naming convention for Terraform resources.
2. **Pull Request (PR) Workflow:**

    - When a user needs elevated privileges, they create a PR in the UserRepo.
    - The PR description should clearly state the reason for the privilege request, the required role, and the requested TTL.
    - The PR should include the necessary Terraform code to grant the user the requested role with the specified TTL using PIM.
3. **Approval Process:**

    - Require two trusted individuals to review and approve the PR.
    - Use Git branch protection rules to enforce the approval process.
4. **Terraform Cloud Integration:**

    - Connect your UserRepo to a Terraform Cloud workspace.
    - Configure Terraform Cloud to automatically run the Terraform configuration when a PR is merged into the main branch.
5. **PIM Integration:**

    - Use the Azure AD provider for Terraform to interact with the PIM API.
    - Create Terraform resources to assign eligible roles with time-bound activation.
    - Ensure that the TTL is correctly set in the Terraform configuration.
6. **Automatic Reversion:**

    - PIM will automatically revert the role assignment after the TTL expires.
    - Consider adding Terraform code to remove the role assignment from the UserRepo after the TTL expires, to maintain the correct state.
7. **Audit Logging:**

    - Enable Azure Entra audit logging to track all role assignments and activations.
    - Monitor Terraform Cloud logs for any errors or suspicious activity.
    - Git history will also provide a clear audit trail of all changes.

**Terraform Code Example (Conceptual):**

Terraform

```sh
resource "azuread_user_eligible_role_assignment" "example" {
  user_object_id = "user_object_id"
  role_definition_id = "role_definition_id"
  justification = "Requested by user for project X"
  schedule {
    start_date_time = "2024-11-20T00:00:00Z"
    expiration {
      type = "afterDuration"
      duration = "PT1H" # 1 Hour
    }
  }
}
```

**Key Considerations:**

- **Error Handling:** Implement robust error handling in your Terraform code to handle potential issues during role assignment.
- **Testing:** Thoroughly test your Terraform configuration in a non-production environment before deploying it to production.
- **Documentation:** Document your GitOps workflow and Terraform configuration.
- **Security Reviews:** Conduct regular security reviews of your Terraform Cloud configuration and Azure Entra permissions.

By combining GitOps, Terraform Cloud, and Azure Entra PIM, you can create a secure and auditable system for managing privileged access in your Azure environment.
