---
aliases: []
confidence: 
created: 2025-07-02T04:17:28Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:25Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: User Management
type:
uid: 
updated: 
version:
---

User management, within the broader context of identities such as users and groups, in Microsoft Entra ID is a comprehensive system designed to provide a single place for storing and managing digital identity information. It encompasses the entire lifecycle of identities, from creation and modification to access provisioning, security, and eventual removal. This system supports both human identities (users) and non-human identities (workload identities like applications, service principals, and managed identities).

1. User Identities and their Attributes
   A user identity in Microsoft Entra ID is defined by a wide array of attributes that describe various aspects of an individual's account and organisational role. These attributes include:
   Account Status: `account_enabled` indicates if the account is active.
   Demographic Information: `age_group` (Adult, NotAdult, Minor) and `consent_provided_for_minor` (Granted, Denied, NotRequired).
   Contact Information: `business_phones`, `city`, `country`, `fax_number`, `mobile_phone`, `office_location`, `postal_code`, `state`, `street_address`, `im_addresses`, `mail`, `other_mails`, `proxy_addresses`.
   Organisational Details: `company_name`, `cost_center`, `department`, `division`, `employee_hire_date`, `employee_id`, `employee_type` (Employee, Contractor, Consultant, Vendor), `job_title`, `manager_id`.
   Naming and Identification: `display_name`, `given_name` (first name), `mail_nickname`, `object_id`, `surname` (family name/last name), `user_principal_name` (UPN).
   Account Type and Origin: `creation_type` (null for regular, Invitation for external, LocalAccount for B2C, EmailVerified for self-service sign-up), `external_user_state` (PendingAcceptance or Accepted for external users), and `user_type` (Guest or Member).
   On-premises Synchronisation: Attributes like `onpremises_distinguished_name`, `onpremises_domain_name`, `onpremises_immutable_id`, `onpremises_sam_account_name`, `onpremises_security_identifier`, `onpremises_sync_enabled`, and `onpremises_user_principal_name` are used when Azure AD Connect synchronises users from an on-premises directory.
   Other: `preferred_language`, `show_in_address_list` (for Outlook global address list), and `usage_location`.

When managing multiple users, data sources like `azuread_users` can retrieve basic information based on employee IDs, mail nicknames, email addresses, object IDs, or user principal names. These sources can also return all users or ignore missing ones.

2. User Account Status and Lifecycle Management
   User management involves various operations to control the state and behaviour of user accounts:
   Enabling/Disabling Accounts: Users can be enabled or disabled, affecting their ability to sign in.
   Password Management: Administrators can set initial passwords for new users, force password changes on next sign-in, and manage properties like `disable_password_expiration` and `disable_strong_password`. Password reset functionalities are also available, including self-service password reset (SSPR).
   External Users (Guests): Microsoft Entra ID supports B2B collaboration, allowing external partners and guest users to access resources using their own identity management solutions. Guest users have restricted directory permissions by default but can be added to administrator roles. Tools exist to monitor and clean up stale guest accounts using access reviews. External users can also be converted into internal users while preserving their existing user objects and access history.
   Bulk Operations: Microsoft Entra ID supports bulk creation, deletion, and restoration of users through CSV templates.
   User Profile Enhancements: The user profile page in the admin centre provides an overview, monitoring (sign-ins over 30 days), and detailed properties categorised by identity, job information, contact information, parental controls, settings, and on-premises details.

3. Group Management for User Access and Entitlements
   Groups are fundamental for efficient user management, allowing administrators to manage access to resources, applications, and tasks for multiple users simultaneously. This aligns with the Zero Trust security principle of limiting access to only those users who need it.
   Purpose of Groups:
   Access Management: Granting access permissions to applications, resources (e.g., SaaS apps, SharePoint sites, Azure services), and even parts of the Microsoft Entra organisation.
   License Assignment: Assigning licences to groups instead of individual users simplifies provisioning and ensures consistent license assignments. If a user is a member of multiple groups with licence policies or has directly assigned licences, the system combines all assigned product and service licences, consuming a single licence if the same one is assigned from multiple sources. Audit logs are available to monitor all activity related to group-based licensing.
   Delegating Administration: Groups can be used to delegate Microsoft Entra management work to less-privileged roles.
   Types of Groups: The sources primarily mention Security groups (used to manage access to shared resources) and Microsoft 365 groups (which can be created and managed with various settings).
   Membership Types:
   Direct Assignment: Users are individually assigned to a resource.
   Group Assignment: A Microsoft Entra group is assigned to a resource, granting all group members access. Both group owners and resource owners can manage group membership.
   Rule-Based Assignment (Dynamic Membership): Groups can be automatically populated with users or devices based on defined rules using attributes (e.g., `userType`, `companyName`, `manager`, `proxyAddresses`). This requires a Microsoft Entra ID P1 licence for each dynamic membership group member.
   External Authority Assignment: Access is managed by an external source (e.g., on-premises directory or SaaS app).
   Group Lifecycle Management:
   Naming Policy: Enforcing consistent naming conventions for Microsoft 365 groups, including prefixes, suffixes, and blocking specific words.
   Expiration Policy: Preventing inactive groups by automatically deleting unused groups after a specified period unless renewed by an owner.
   Self-Service Group Management: Allowing users to search for and join groups, or create and manage their own Microsoft 365 groups, which empowers teams and reduces IT administrative burden.
   Owners: Assigning multiple owners (at least two) to a group ensures continuity and reduces dependencies. Supported owner types are users or service principals.
   Group Permissions and Roles:
   The `azuread_group` resource can be used to configure groups, including setting `administrative_unit_ids` to place a group within an administrative unit, enabling `onpremises_group_type` for writeback, and assigning `owners`.
   `Group management permissions` can be used in custom role definitions to grant fine-grained access, such as managing group properties, members, owners, and creating/deleting groups. This feature requires Microsoft Entra ID P1 licences.

4. Identities in a Broader Context: Workload Identities and Role-Based Access Control (RBAC)
   Beyond human users, Microsoft Entra ID manages workload identities, which include applications, service principals, and managed identities. These are crucial for securing communication between services and automating access without managing credentials.

Managed Identities:

What they are: Automatically managed identities in Microsoft Entra ID, assigned to Azure compute resources (e.g., Virtual Machines, App Service, Azure Functions, Container Instances). They eliminate the need for developers to manage secrets, credentials, or certificates.

Types:

System-assigned: Tied to a single Azure resource, deleted with the resource, and cannot be shared. Permissions are granted using role-based access control (RBAC).

User-assigned: Standalone Azure resources that can be assigned to multiple Azure resources, with an independent lifecycle. They are recommended for most scenarios, especially for rapid creation of resources or when access is required before a resource is deployed.

How they work: Applications use managed identities to obtain Microsoft Entra tokens, which are automatically authenticated based on the environment where the code runs, requiring no secrets in the code.

Accessing Resources: Managed identities can authenticate to any service that supports Microsoft Entra authentication, including Azure services like Storage Accounts, SQL Databases, CosmosDB, Key Vault, Service Bus, and Event Hubs.

Workload Identity Federation (Managed Identity as FIC): A managed identity can be used as a federated identity credential (FIC) for Microsoft Entra ID applications, enabling credential-free authentication for workloads acting as Entra ID applications. A maximum of 20 FICs can be added to an application or user-assigned managed identity. Only user-assigned managed identities are supported for this feature.

Best Practices: Always adhere to the `principle of least privilege`, granting only the necessary permissions. Consider the impact of assigning managed identities to Azure resources, as any user with code execution access to that resource can access all associated identities. Lifecycle differences (system-assigned deleted with resource, user-assigned independent) are important.

Role-Based Access Control (RBAC):

Purpose: Microsoft Entra RBAC manages access to Microsoft Entra resources (users, groups, applications) using the Microsoft Graph API, enabling granular permissions and adherence to the `principle of least privilege`.

Role Categories:

Microsoft Entra ID-specific roles: Grant permissions to manage resources within Microsoft Entra ID only (e.g., User Administrator, Groups Administrator).

Service-specific roles: Defined in Microsoft Entra ID for service-specific privileges (e.g., Exchange Administrator, Intune Administrator).

Cross-service roles: Span multiple services (e.g., Global Administrator, Global Reader, Security Administrator).

Built-in Roles: Numerous built-in roles are available (e.g., Global Administrator, User Administrator, Groups Administrator, Helpdesk Administrator, License Administrator, Privileged Authentication Administrator).

Custom Roles: Administrators can create custom roles with specific, fine-grained permissions for user and group management scenarios. These require Microsoft Entra ID P1 licences.

Administrative Units (AUs): AUs are Microsoft Entra resources that act as containers for users, groups, or devices, allowing administrators to restrict the scope of permissions for a role to a specific portion of the organisation. For instance, a Helpdesk Administrator can be delegated to manage users only in their supported region. Adding a group to an administrative unit brings the group itself into management scope, but not its members unless they are separately added. `Restricted management administrative units` offer enhanced protection for specific objects, blocking direct modifications by tenant-level administrators unless they have explicit assignment to the AU scope. AUs require Microsoft Entra ID P1 licences for administrators and Free licences for members. If using dynamic membership rules for AUs, each member needs a P1 licence.

5. Access and Consent Management for Applications
   User management also extends to how users interact with applications, particularly concerning access and consent:
   Application Access: Users, groups, and owners can be assigned to applications, and access can be managed through single sign-on (SSO), resource assignment, consent mechanisms, and automated provisioning.
   User Consent: Users can grant permission for an application to access protected resources and organisational data. This can occur when a user signs in for the first time.
   Admin Consent: Some applications, depending on required permissions, may require an administrator to grant consent on behalf of the organisation. Administrators should carefully evaluate permissions before granting tenant-wide admin consent, distinguishing between "delegated permissions" (acting on behalf of a user) and "application permissions" (accessing data for the entire organisation without user interaction). Consent policies allow control over which applications users can consent to.
   Single Sign-On (SSO): SSO allows users to sign in once with one set of credentials to access multiple independent software systems. Microsoft Entra ID supports various SSO options, including SAML, OpenID Connect (OIDC), and password-based SSO.
   Conditional Access and MFA: Policies can be configured to enforce multifactor authentication (MFA) and other conditions to safeguard access to applications.
   Removing Access: Scenarios like compromised accounts or employee termination necessitate revoking access. This involves understanding how access tokens and refresh tokens work, as revocation can take time to propagate.
