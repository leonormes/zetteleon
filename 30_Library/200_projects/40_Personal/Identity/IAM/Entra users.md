---
aliases: []
confidence: 
created: 2025-07-02T04:03:05Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:25Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Entra users
type:
uid: 
updated: 
version:
---

At its core, managing permissions in Microsoft Entra ID revolves around three key components: **Users**, **Groups**, and **Roles/Permissions**, all interacting within the context of **Applications** and **Scopes**.

Let's demystify the process and the terms you're encountering.

## Understanding the Core Components

Before diving into the "how-to," let's clarify the fundamental building blocks:

## **Users**

In Microsoft Entra ID, a "user object" represents an individual account in your directory. These can be member users (native to your tenant) or guest users (from other directories). Users are typically the "who" that needs access.

- **Properties**: User objects have various properties like display name, job title, email, and mobile phone number.
- **Management**: You can add, delete, update properties, reset passwords, and assign licenses to users.

## **Groups**

Groups are collections of users, devices, or service principals. They are a highly efficient way to manage access, as you can grant permissions to a group once, and all its members automatically inherit those permissions.

- **Types**:
- **Security Groups**: Primarily used to manage access to shared resources like applications or SharePoint sites.
- **Microsoft 365 Groups**: Offer collaboration opportunities (e.g., in Teams, SharePoint, Outlook) and can also be used for access management.
- **Membership Types**:
- **Assigned (Static)**: Members are manually added or removed by an administrator or group owner.
- **Dynamic**: Members are automatically added or removed based on rules (e.g., users from a specific department). This requires a Microsoft Entra ID P1 license.
- **Owners**: Groups can have owners (users or service principals) who can manage the group's properties and membership.
- **Role-assignable groups**: A special type of security or Microsoft 365 group that can be assigned Microsoft Entra roles (administrative roles). This requires setting the `isAssignableToRole` property to `true` during creation and needs a Microsoft Entra ID P1 or P2 license. These groups have restrictions, for example, a maximum of 500 per tenant.

## **Permissions And Roles**

- **Permissions**: These are specific actions that can be performed on Microsoft Entra resources, such as "create users," "read groups," or "update application properties". They define what an identity *can do*.
- **Roles (Role Definitions)**: A role is a collection of permissions. Instead of granting individual permissions, you assign a role that bundles multiple related permissions.
- **Built-in Roles**: Pre-defined roles by Microsoft with a fixed set of permissions (e.g., Global Administrator, User Administrator, Groups Administrator, Cloud Application Administrator).
- **Custom Roles**: Roles created by your organization with a specific set of permissions tailored to your needs.
- **Role Assignment**: This is the act of giving a role to a security principal (user, group, or service principal) at a specified scope. A role assignment consists of three elements: the **security principal**, the **role definition**, and the **scope**.

1. **Applications (Enterprise Applications & App Registrations)**:

- **App Registration**: This is the global definition of your application within Microsoft Entra ID, typically for applications you are developing or managing directly.
- **Enterprise Application**: This is an instance of an application object within your tenant, representing an application that your organization uses (e.g., GitLab, Salesforce, F5 BIG-IP). When you integrate a third-party SaaS app, you're usually working with an Enterprise Application, which has an associated service principal.
- **Service Principal**: An instance of an application object in a specific tenant. It defines how the application interacts with resources within that tenant and is what roles and permissions are assigned to for the application to function in your environment.

## How to Assign Permissions in the Entra Portal

The "portal process" can indeed seem like a maze because permissions can be assigned at different levels and through various paths. Here’s a breakdown:

### 1. Assigning Users/Groups to an Enterprise Application (for Application Access)

This is how you control *who can use* a specific application (like GitLab) integrated with Entra ID for SSO.

- **Path**: Identity > Applications > Enterprise applications > All applications.
- **Steps**:

1. Sign in to the Microsoft Entra admin center as at least a Cloud Application Administrator.
2. Browse to **Identity** > **Applications** > **Enterprise applications** > **All applications**.
3. Search for and select the specific application (e.g., GitLab).
4. In the left pane, select **Users and groups**.
5. Select **Add user/group**.
6. On the "Add Assignment" pane, select "None Selected" under **Users and groups**.
7. Search for and select the user(s) or group(s) you want to assign to the application.
8. Select **Select**.
9. Under "Select a role", choose the specific role you want to assign to the user or group for *this application*. If no roles are defined, the default is "Default Access". This relates to `app_roles` defined within the application's service principal.
10. On the "Add Assignment" pane, select **Assign**.

- **Key Concept**:
- **"Assignment required?"** property for the Enterprise Application: If set to "Yes," only assigned users/groups can sign in. If "No," all users can sign in, but only assigned ones see the app in their My Apps portal. It's recommended to set this to "Yes" for security.
- **Group-based assignment** is recommended for efficient access management, especially if you have a Microsoft Entra ID P1 or P2 license.

### 2. Assigning Users/Groups to an Administrative Role (Directory Roles)

This is how you grant administrative privileges *within Microsoft Entra ID itself* (e.g., permission to create users, manage groups, or configure applications).

- **Path for Users (Method 2: Directory Roles)**: Identity > Roles and Administrators > Roles and Administrators.
- **Steps**:

1. Sign in to the Microsoft Entra admin center as at least a Privileged Role Administrator (this is the least privileged role required to assign other roles at tenant scope).
2. Browse to **Identity** > **Roles & admins** > **Roles & admins**.
3. Select the desired role (e.g., "User Administrator" to create/manage users and groups).
4. Select **Add assignments**.
5. Select the users or **role-assignable groups** you want to assign to this role. Only role-assignable groups will appear here.
6. Select **Add** to assign the role.

- **Scope Options**:
- **Tenant Scope**: By default, roles are assigned at "tenant scope," meaning the permissions apply to all corresponding resources in the entire organization.
- **App Registration Scope**: Custom roles and some built-in roles can be assigned to the scope of a single app registration, allowing the assignee to manage only that specific application.
- **Administrative Unit Scope**: For more granular control, you can limit a role's permissions to specific organizational units (e.g., only manage users in the "Marketing" department). The user/group receiving the role assignment will only have permissions over members of that administrative unit, not the container itself unless the members are also explicitly added to the AU. This requires a Microsoft Entra ID P1 or P2 license.

### 3. Adding Members to a Group (for Group Membership)

This is how you populate a group with users, so they inherit the group's permissions or application access.

- **Path**: Identity > Groups > All groups.
- **Steps**:

1. Sign in to the Microsoft Entra admin center as at least a Groups Administrator.
2. Browse to **Identity** > **Groups** > **All groups**.
3. Select the group you want to add members to.
4. In the left pane, select **Members**.
5. Select **Add members** (or "Import members" for bulk operations).
6. Search for and select the user(s) or service principal(s) you want to add as members.
7. Select **Select**.

- **Alternative (Managed Identity)**: Managed identities for Azure resources can also be assigned roles, directly or via groups.

## How to See What Permissions a User Has

This involves checking multiple locations, as permissions can be inherited or directly assigned.

### 1. Check a User's Assigned Roles (Directory Roles)

This shows direct administrative roles and roles inherited through role-assignable groups.

- **Path**: Identity > Users > (Select User) > Assigned roles.
- **Details**: This view will show roles assigned directly to the user or indirectly via group membership if the group is a role-assignable group. If your tenant has Microsoft Entra ID P2 (which includes PIM), you'll see more details like "eligible," "active," and "expired" role assignments.

### 2. Check a User's Group Memberships

This shows all groups a user is a member of, which is crucial because groups are often used to grant access to applications and resources.

- **Path**: Identity > Users > (Select User) > Groups.
- **Details**: This list shows all groups the user is a direct or indirect member of (excluding nested group limitations for application assignments). Once you know the groups, you can then check what permissions *those groups* have.

### 3. Check an Application's User/Group Assignments

This shows which specific users and groups have been granted access to a particular enterprise application.

- **Path**: Identity > Applications > Enterprise applications > (Select Application) > Users and groups.
- **Details**: This page lists all users and groups assigned to the application, along with any specific application roles (`app_roles`) assigned to them for that application.

### 4. Check API Permissions Granted to an Application (Service Principal)

This is about what permissions the *application itself* has to access other APIs (like Microsoft Graph) on behalf of a user or itself. This is distinct from *who can use* the application.

- **Path**: Identity > Applications > Enterprise applications > (Select Application) > Permissions.
- **Details**:
- **Admin consent tab**: Shows permissions consented to for the entire organization.
- **User consent tab**: Shows permissions granted by specific users to the application.
- You can select a permission to view its details. Permissions can be revoked from the "Admin consent" tab.

## Clarification of Confusing Terms and Concepts

- **User Object vs. Group**: A user is an individual identity. A group is a collection of identities. Both are considered "security principals" and can be assigned roles or access.
- **Permissions vs. Roles**:
- **Permissions** are the raw, granular actions (e.g., `microsoft.directory/users/create` to create a user).
- **Roles** are predefined or custom bundles of these raw permissions (e.g., the "User Administrator" role contains the `microsoft.directory/users/create` permission, among others). You generally assign roles, not individual permissions, directly to users or groups for administrative purposes.
- **`app_role_assignment_required`**: This attribute on a service principal determines if users or groups *must be explicitly assigned* to the enterprise application before Microsoft Entra ID will issue a token for them to access the application. If `true`, only assigned users/groups can sign in. If `false`, any user can sign in, but only assigned users will see the app in their My Apps portal.
- **`app_roles`**: These are roles *published by the application itself*. For instance, a CRM application might define "Sales Representative," "Sales Manager," or "Admin" roles. When you assign users or groups to the application, you can assign them to one of these specific app roles. These are different from Microsoft Entra administrative roles.
- **`oauth2_permission_scopes`**: Also known as "delegated permissions," these define permissions that an application can request to act *on behalf of a signed-in user* (e.g., "read user's profile"). The user, or an administrator on their behalf, consents to these permissions.
- **`Directory.Read.All` vs. `User.Read.All` vs. `Application.Read.All`**: These are specific permissions within Microsoft Graph API that grant an application or service principal the ability to read directory objects (users, groups, applications). They are typically assigned to the *application's service principal* (not directly to a user).

## Summary of the Portal Process Flow

1. **Users** are the individuals.
2. **Groups** are collections of users (or other principals) for easier management.

- **To put a user in a group**: Go to the **Group** object in the portal and add the user as a **Member**.

1. **Applications** are the services your users access.

- **To give a user access to an application (for SSO)**: Go to the **Enterprise Application** object in the portal, select **Users and groups**, and assign the user (or a group they are a member of) to the application, potentially selecting an `app_role` specific to that application. Ensure "Assignment required" is set to "Yes" on the application's properties for stricter control.

1. **Roles** grant administrative powers or access to specific data/features *within Entra ID*.

- **To give a user administrative permissions (e.g., to create users or manage groups)**: Go to **Identity** > **Roles & admins** > **Roles & admins**, select the desired **Role**, and then add the user (or a role-assignable group) as an **Assignment**.
- **To give an *application* (service principal) permissions to interact with Entra ID or other Microsoft services**: Go to the **App Registration** or **Enterprise Application** object, select **API permissions**, and add the required Microsoft Graph (or other API) permissions. This is usually followed by granting admin consent.

The "different pages and subsections" you mentioned are generally organized logically:

- **Users blade**: For managing individual user accounts and their direct properties/assignments.
- **Groups blade**: For managing group properties, memberships, and group-based assignments.
- **Enterprise applications blade**: For managing access to SaaS applications and other applications your organization uses, and for reviewing the permissions granted to these applications.
- **Roles & admins blade**: For managing Microsoft Entra administrative roles and their assignments, including custom roles and administrative units.
- **App registrations blade**: Primarily for developers to register and configure their applications, including API permissions exposed or required by the application.

It's common to move between these sections depending on whether you're trying to manage *who can access an app*, *who has admin privileges*, or *what an app can do*.
