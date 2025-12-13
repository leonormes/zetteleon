---
aliases: []
confidence: 
created: 2025-03-11T10:03:10Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [azure, IAM]
title: Creating an Azure Account A Detailed Guide for the Team Wiki
type: documentation
uid: 
updated: 
version:
---

## Creating an Azure Account: A Detailed Guide for the Team Wiki

This document outlines the process of creating an Azure account, detailing the steps involved, the identities required, and the resulting components. This information is crucial for team members who need to understand the foundational elements of our Azure environment.

### What a Human Does to Create an Azure Account

Creating an Azure account is typically initiated by a human user through the Azure portal or the Azure website. Here's a step-by-step breakdown of the process:

1.  **Navigate to the Azure Sign-Up Page:** The user starts by visiting the official Azure website, usually by searching for "Azure sign up" or going directly to a URL like `azure.microsoft.com`.
2.  **Initiate the Free Account or Paid Subscription Process:** Azure offers different types of subscriptions, including a free account with limited credits and paid subscriptions like "Pay-As-You-Go." The user selects the desired subscription type to begin.
3.  **Provide Identity Information:** This is a critical step. The user needs to provide an identity to associate with the Azure account. This identity can be:
    -   **Microsoft Account (MSA):** A personal email address (like Outlook.com, Hotmail.com, or even Gmail, Yahoo, etc. linked to a Microsoft Account). If the user doesn't have one, they will be prompted to create one.
    -   **Work or School Account (Organizational Account):** An email address provided by an organization that uses Microsoft 365 or Azure Active Directory (now Microsoft Entra ID). This is generally preferred for business use as it aligns with organizational identity management.

4.  **Provide Personal/Organizational Details:** Depending on the subscription type and account type, the user will be asked to provide details such as:
    -   **Name and Contact Information:** Personal details like name, email, phone number, and address.
    -   **Organization Information (if applicable):** Organization name, address, and potentially tax information.

5.  **Phone Verification:** Azure usually requires phone verification to confirm the user's identity. A verification code is sent via SMS to the provided phone number, which the user must enter on the website.
6.  **Payment Information (for Paid Subscriptions):** For paid subscriptions, the user needs to provide credit card or other payment details. Free accounts might also require this for identity verification, although they are not initially charged.
7.  **Accept Agreement:** The user must review and accept the Microsoft Azure agreement, which outlines the terms of service and legal conditions.
8.  **Azure Account Creation Completes:** After completing these steps, the Azure account creation process is finalized. The user is typically redirected to the Azure portal.

### Identity Requirements for Initial Azure Account Creation

To create a new Azure account and tenant, the human user needs to possess one of the following identities:

-   **A Microsoft Account (MSA):** This is the most straightforward way to create an Azure account, especially for individual use or testing. Any valid MSA can be used.
-   **A Work or School Account associated with an existing Azure AD/Entra ID:** If the user is part of an organization already using Microsoft cloud services, they can use their organizational account. However, creating a *new* Azure tenant typically requires using an MSA or creating a *new* Entra ID instance in conjunction with the Azure signup process.

**Important Note:** You cannot create an Azure tenant without associating it with one of these identity types initially. There's always a root identity tied to the creation.

### What Comes with Creating an Azure Account

When a user signs up for an Azure account, several key components are provisioned:

-   **Azure Subscription:** This is the fundamental billing and management unit in Azure. Think of it as a container for all your Azure resources. When you sign up, you are creating at least one Azure subscription. You can have multiple subscriptions under a single Azure account for various purposes (e.g., development, production, different departments). The subscription is linked to the identity used during signup for initial management.
-   **Azure Tenant (Microsoft Entra Tenant):** This is automatically created alongside your first Azure subscription. The Azure tenant is your organization's dedicated instance of Microsoft Entra ID (formerly Azure Active Directory). It's the identity service for Azure and Microsoft 365. It manages users, groups, and permissions for all your Azure resources and potentially other Microsoft cloud services.
-   **Entra ID Instance:** Yes, when you create an Azure account, you automatically get an Entra ID instance. This instance is the core identity and access management service for your Azure environment. It's where user accounts, groups, application registrations, and role-based access control (RBAC) are managed. It's the same technology as Microsoft 365's directory but dedicated to your Azure resources.
-   **Initial Azure Portal Access:** The user who created the account gains access to the Azure portal (`portal.azure.com`). This web-based console is the primary interface for managing Azure resources, subscriptions, and the Entra ID tenant.

### What Happens to the Identity that Created the Account

The identity (MSA or Work/School account) used to create the Azure account receives a very important initial role:

-   **Global Administrator in Entra ID:** The identity becomes the **first Global Administrator** within the newly created Entra ID tenant. This is a highly privileged role with complete administrative control over the entire Entra ID tenant and, by extension, all Azure resources associated with it. This user can manage all aspects of Entra ID, including users, groups, domains, and security settings, as well as all Azure services within the subscriptions linked to this tenant.
-   **Account Administrator for the Azure Subscription:** The identity also becomes the "Account Administrator" for the Azure subscription created during signup. This role has administrative control over the Azure subscription itself, including billing and subscription management.

**Crucially, this initial identity is extremely powerful and represents the root of trust for your Azure environment.**

### Does the Initial Identity Get an Entra ID? Does it Have a Special Identity in the Azure Account/Tenant

-   **Yes, the identity *becomes* an Entra ID identity:** When you use an MSA to create an Azure account, behind the scenes, that MSA is effectively *provisioned* or *represented* as a user identity within the new Entra ID tenant. If you use a Work/School account from an existing Entra ID, that account is simply granted Global Administrator rights in the *new* tenant.
-   **Special Identity - Global Administrator Role:** The special aspect is the **Global Administrator role** assigned to this initial identity in the Entra ID tenant. This role is not just "special" – it's the most privileged role in the entire Microsoft cloud ecosystem for your tenant. It bypasses most access controls within Entra ID and Azure services.
-   **No "Special" Azure Account Identity Beyond Roles:** Beyond the Global Administrator role, there isn't a fundamentally different type of identity within the Azure account or tenant. It's simply a user identity within Entra ID that has been granted this initial, highly privileged role. You can (and should) later create other identities, including service principals and regular user accounts, and assign them roles based on the principle of least privilege.

### Different Components Called: Account, Tenant, Entra ID Instance, Subscription

Let's clarify the terminology, as it can be confusing:

-   **Azure Account (Billing Account):** This is the top-level entity that represents your relationship with Microsoft for Azure services. It's primarily a billing and organizational construct. You sign up for an Azure *account*. It can contain one or more Azure subscriptions. Think of it as the umbrella over everything. However, the term "Azure Account" is sometimes used loosely to refer to the entire Azure environment, including the tenant and subscriptions.
-   **Azure Tenant (Microsoft Entra Tenant):** This is your organization's dedicated instance of Microsoft Entra ID. It's the identity management service. It's often referred to as your "directory." It's automatically created when you create your first Azure subscription. You manage users, groups, applications, and access control within your Azure tenant. **Yes, when you sign up for an Azure account, you are essentially creating an Azure tenant.**
-   **Entra ID Instance (Azure Active Directory Instance):** This is essentially synonymous with "Azure Tenant." "Entra ID" is the new name for "Azure Active Directory." So, an "Entra ID instance" and an "Azure Tenant" refer to the same thing – your organization's dedicated cloud-based directory service in Azure.
-   **Azure Subscription:** This is a logical container for Azure resources. It's the unit of resource deployment and billing. You can have multiple subscriptions within an Azure account, all associated with the same Azure tenant for identity management. Subscriptions help you organize and manage your Azure resources for different projects, teams, or environments.

**Analogy:**

Think of it like a building:

-   **Azure Account:** The company that owns and manages the entire building complex (your overall relationship with Azure).
-   **Azure Tenant (Entra ID Instance):** The security and directory service for the building complex. It manages who can access which offices and resources within the building (your organization's identity management).
-   **Azure Subscription:** Individual office spaces within the building. Each office space (subscription) can house different teams and projects, but they all use the building's central security and directory (Azure Tenant/Entra ID).

### Securing the Initial Identity - Critical First Step

Because the initial identity is granted the powerful Global Administrator role, it's **imperative** to secure it immediately after creating the Azure account. Best practices include:

-   **Enable Multi-Factor Authentication (MFA):** Immediately enable MFA for the initial Global Administrator identity.
-   **Document a Break-Glass Procedure:** Establish a documented and secure "break-glass" process for using this account only in emergencies.
-   **Consider a Dedicated Break-Glass Account:** For enhanced security, you might create a separate, dedicated "break-glass" Global Administrator account and restrict the use of the initial account.
-   **Principle of Least Privilege Going Forward:** For day-to-day administration, **never** use the Global Administrator account. Instead, create other administrator accounts or service principals and grant them only the specific roles they need to perform their tasks, following the principle of least privilege.

By understanding these details of Azure account creation, your team will be better equipped to manage and secure your Azure environment effectively from the outset. Remember to always prioritize security, especially for the initial root identity of your Azure tenant.

## Identifying the Initial Account Creator of Your Azure Tenant (Azure CLI & zsh)

This document outlines the process of identifying the initial Azure account creator using Azure CLI in a zsh environment. It details the steps involved, focusing on Azure CLI commands to find accounts that likely held initial administrative roles.

**Important Considerations:**

-   **No Single "Created By" Field:** Azure and Entra ID don't have a specific audit log or field that explicitly states "Tenant Created By: \[Identity]". We will focus on identifying accounts granted initial administrative roles.
-   **Focus on Initial Roles:** We'll identify accounts that were assigned the **Global Administrator** role (and potentially the **Account Administrator** role for the Azure subscription) around the tenant's creation time.
-   **Audit Logs are Key:** Entra ID and Azure Activity Logs are crucial for this investigation, and Azure CLI will be used to query them.
-   **Assumptions:** This guide assumes you have the Azure CLI installed and configured to connect to your Azure subscription. You'll need an account with sufficient permissions (at least **Privileged Role Administrator** or **Global Reader** in Entra ID, and **Subscription Owner** or **Billing Reader** on the Azure Subscription) to execute these commands.

### Process to Identify the Initial Account Using Azure CLI

1.  **Identify Global Administrators:** The initial tenant creator would have been assigned the Global Administrator role. List current Global Administrators and investigate their role assignment history.

-   **Using Azure CLI:**

```zsh
# List current Global Administrators
az role assignment list --role "Global Administrator" --query "[].principalName" --output table
```

-   This Azure CLI command lists the `principalName` (typically the user's email address) of all current users assigned the "Global Administrator" role.
-   **Review the list:** Examine the output for user accounts that seem like potential initial setup accounts. Consider:
-   Accounts with names like "admin," "administrator," "initialadmin," or similar.
-   Accounts that might belong to individuals responsible for the organization's initial IT setup.
-   Accounts that appear less likely to be regular day-to-day user accounts.

2.  **Examine Audit Logs for Role Assignment:** For the potential initial accounts identified, query the Entra ID audit logs to find out when they were assigned the Global Administrator role. The account with the earliest role assignment is likely the initial creator.

-   **Using Azure CLI:**

```zsh
# Set the User Principal Name of the user you want to investigate (replace with actual UPN)
user_principal_name="user@yourdomain.com"

# Query audit logs for "Add role to user" operations targeting the specified user for Global Administrator role
az audit-log show --query "value[?operationName == 'Add role to user' && targetResources[0].displayName == 'Global Administrator' && targetResources[1].displayName == '$user_principal_name'] | [].activityDateTime, initiatedBy.userPrincipalName, targetResources[1].displayName" --output table
```

-   **Important:** Replace `"user@yourdomain.com"` in the `user_principal_name` variable with the actual User Principal Name of one of the potential initial accounts you identified in step 1.
-   This command filters the Azure AD audit logs:
-   `operationName == 'Add role to user'`: Looks for role assignment events.
-   `targetResources[0].displayName == 'Global Administrator'`: Filters for events related to the "Global Administrator" role.
-   `targetResources[1].displayName == '$user_principal_name'`: Filters for events targeting the specific user account you are investigating.
-   `--query "..."`: Selects and formats the output to show:
-   `activityDateTime`: The timestamp of the audit event.
-   `initiatedBy.userPrincipalName`: The user who initiated the role assignment (often the same as the target user in initial setup scenarios, but good to check).
-   `targetResources[1].displayName`: The user account that was assigned the role.
-   `--output table`: Formats the output as a table for readability.
-   **Review the Output:** Run this command for each potential initial account from your Global Administrator list. Look at the `activityDateTime` column. The account with the **earliest timestamp** for the "Add role to user" event related to the "Global Administrator" role is the most probable initial tenant creator.

3.  **Check Azure Subscription Account Administrators (Less Direct, Potentially Helpful):** In some cases, the initial account creator might also be the initial "Account Administrator" for the Azure subscription.

    -   **Using Azure CLI:**

        ```zsh
        # Get the Subscription ID you are investigating (replace with your actual Subscription ID)
        subscription_id="YOUR_SUBSCRIPTION_ID"

        # List Account Administrators for the Azure Subscription
        az role assignment list --subscription $subscription_id --role "Account administrator" --output table
        ```

        -   **Important:** Replace `"YOUR_SUBSCRIPTION_ID"` with the actual ID of your Azure subscription. You can find your subscription ID in the Azure portal or by using `az account show --query id`.
        -   This command lists role assignments at the subscription scope for the "Account administrator" role.
        -   **Review the Output:** Check if any accounts listed here align with your potential initial account creators. Note that the "Account administrator" role is less commonly used now, so this might not always provide definitive results.

4.  **Consider Historical Documentation and Organizational Knowledge:**

    -   **Internal Documentation:** Search for any internal documentation from when your Azure tenant was first set up. This might include setup guides, onboarding documents, or IT records that could identify the person and account responsible for the initial Azure configuration.
    -   **Consult Long-Tenured IT Staff:** Speak with IT team members who were with the organization during the Azure tenant's initial setup. They might recall who performed the setup and which account was used.

### What Happens to the Identity that Created the Account? (Reiterated)

-   **Becomes Global Administrator:** The identity used to create the Azure tenant is automatically granted the **Global Administrator** role in the newly created Entra ID tenant.
-   **Becomes Azure Subscription Account Administrator (Potentially):** It might also become the initial **Account Administrator** for the Azure subscription.

**Best Practice - Secure the Initial Identity Immediately (Crucial):**

After identifying the likely initial account creator, prioritize securing this account:

-   **Enable Multi-Factor Authentication (MFA):** If not already enabled, immediately enforce MFA for this account.
-   **Implement Break-Glass Account Strategy:** Treat this account as a break-glass/emergency access account. Create a documented, secure process for its use, limit day-to-day usage, and consider renaming it to reflect its purpose.
-   **Principle of Least Privilege for Ongoing Admin:** For routine administrative tasks, delegate roles to other accounts with least privilege, avoiding the Global Administrator account.

### Components and Terminology Recap (as before)

-   **Azure Account (Billing Account):** Your overall billing relationship with Microsoft for Azure.
-   **Azure Tenant (Microsoft Entra Tenant / Entra ID Instance):** Your organization's dedicated identity service in Azure.
-   **Azure Subscription:** A container for Azure resources, used for billing and management within your Azure account and tenant.
-   **Global Administrator:** The highest privileged role in Entra ID, initially assigned to the tenant creator.

By using these Azure CLI commands and following the investigation steps, you can determine the identity that most likely created your Azure tenant. Remember to focus on securing this initial identity and implementing least privilege for ongoing Azure administration.

Let me know if you have any further questions or need more assistance!
