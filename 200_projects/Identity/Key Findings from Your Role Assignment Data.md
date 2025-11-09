---
aliases: []
confidence: 
created: 2025-07-02T12:19:37Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:25Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Key Findings from Your Role Assignment Data
type:
uid: 
updated: 
version:
---

1. High Number of Privileged Roles: The analysis shows many highly privileged roles have been assigned. The most common roles are `User Access Administrator` (9 assignments), `Owner` (8 assignments), and `Contributor` (3 assignments). These roles grant significant control over the resources.
2. Most Permissions are Assigned to Individuals: Of the 23 total role assignments, 17 are assigned directly to `Users`, while only 1 is assigned to a `Group`. The remaining 5 are for `Service Principals` (applications or automated services).
3. Permissions are inherited from Above: Crucially, only one of the 23 role assignments is directly on your `rg-ff-uks-gp-net` resource group. The vast majority are applied at much broader scopes, such as the entire Subscription or even higher-level Management Groups.

## What This Means: The Principle of Inheritance

In Azure, permissions flow downwards. If someone has a role on a Management Group, they have that same role on all subscriptions and resource groups beneath it. If they have a role on a Subscription, they have that same role on all resource groups within it.

This is why you are seeing so many people with access to `rg-ff-uks-gp-net`. Even though their permissions weren't assigned directly to your resource group, they have roles like 'Owner' or 'Contributor' at the subscription level, and those permissions are inherited.

## Answering Your Key Question

> "Can all these people access the application running in the sub we were given?"

Yes, effectively, they can. Anyone with an `Owner` or `Contributor` role at a scope above your resource group (like the subscription `709f3d57-b6d7-48c6-8252-6b1c1174a541`) can modify, delete, and manage the resources within your application's resource group. A `User Access Administrator` can change who has access to what, including giving themselves or others `Owner` rights.

## High-Privilege Assignments of Concern

I have filtered the list to show only the assignments for the most powerful roles: `Owner`, `Contributor`, and `User Access Administrator`. This is the list you should review carefully with your client.

| DisplayName                         | RoleDefinitionName        | Scope                                                                                 | ObjectType       |
| :---------------------------------- | :------------------------ | :------------------------------------------------------------------------------------ | :--------------- |
| 47d1717c7ae848cdbc423ca2            | Contributor               | /providers/Microsoft.Management/managementGroups/mg-landingzones                      | ServicePrincipal |
| Andrew Bell                         | User Access Administrator | /                                                                                     | User             |
| Cloud Admin                         | User Access Administrator | /                                                                                     | User             |
| FITFILE DevOps Users                | Contributor               | /subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541                                   | Group            |
| FITFILE Terraform Cloud Provisioner | Contributor               | /subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541                                   | ServicePrincipal |
| FITFILE Terraform Cloud Provisioner | User Access Administrator | /subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541                                   | ServicePrincipal |
| Sean Donnelly                       | User Access Administrator | /                                                                                     | User             |
| Sean Donnelly                       | Owner                     | /subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541                                   | User             |
| Rachel Goodall                      | User Access Administrator | /                                                                                     | User             |
| Rachel Goodall                      | Owner                     | /providers/Microsoft.Management/managementGroups/mg-cuh                               | User             |
| McKenna, Alexis                     | User Access Administrator | /                                                                                     | User             |
| McKenna, Alexis                     | Owner                     | /subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541                                   | User             |
| McKenna, Alexis                     | Owner                     | /providers/Microsoft.Management/managementGroups/mg-cuh                               | User             |
| McKenna, Alexis                     | User Access Administrator | /providers/Microsoft.Management/managementGroups/3d7d135a-ac7f-46ad-aa55-54639dd31d14 | User             |
| Michael Scullion                    | User Access Administrator | /                                                                                     | User             |
| Michael Scullion                    | Owner                     | /                                                                                     | User             |
| Michael Scullion                    | Owner                     | /providers/Microsoft.Management/managementGroups/mg-genprod                           | User             |
| Michael Scullion                    | Owner                     | /providers/Microsoft.Management/managementGroups/mg-landingzones                      | User             |
| Michael Scullion                    | Owner                     | /providers/Microsoft.Management/managementGroups/mg-cuh                               | User             |
| David Sullivan                      | User Access Administrator | /                                                                                     | User             |

## Recommendations and Next Steps

1. Discuss with Your Client: You should immediately share these findings with your primary contact at the client. It is possible this level of access is intentional for their administrative staff, but it's crucial to confirm and to ensure they understand the security implications.
2. Advocate for the Principle of Least Privilege: The current setup is the opposite of the "principle of least privilege," which states that a user should only be given the bare minimum permissions required to perform their job. The high number of `Owner` and `Contributor` roles at broad scopes is a security risk.
3. Recommend Using Groups for Access: Best practice is to assign roles to Azure AD Groups, not individual users. For example, instead of giving five developers the `Contributor` role individually, you would create a `Dev-Team-Group`, give the group the `Contributor` role, and then add or remove users from that group. This is much easier to manage and audit.

This situation is not uncommon, but it is important to address it to ensure the security and integrity of your application.

If you have further questions or get an updated list of roles, I would be happy to analyse it for you.

### How PIM Solves the Current Problem

PIM changes the model from "permanent access" to "eligible access". Instead of a user having the `Owner` role 24/7, they are made *eligible* for the `Owner` role and must go through a process to activate it when they need it

This directly addresses your issues by:

- Minimising Risk: It drastically reduces the security risk because privileged credentials are not active all the time, making them less likely to be compromised and misused
- Enabling Just-in-Time (JIT) Access: Users get high-privilege access only for a limited time when they have a legitimate need and have provided a justification
- Providing a Clear Audit Trail: Every role activation is logged, showing who requested access, when, for how long, and for what reason
- Enforcing Approvals: You can configure the most sensitive roles to require approval from a manager or another administrator before they can be activated

### Your Strategic Plan for Implementing PIM

Here is a step-by-step strategy you can propose to your client to move their current setup to a more secure, PIM-based model.

Step 1: Identify and Prioritise Critical Roles

Start with the most privileged roles that you identified in the previous analysis. Your initial focus should be on moving all assignments for these roles into PIM:

- Owner
- Contributor
- User Access Administrator

Step 2: Transition from 'Active' to 'Eligible' Assignments

For each high-privilege assignment, you will need to perform two actions:

1. Create an "Eligible" Assignment in PIM: In the PIM console, you will make the user or group *eligible* for the role. They now have the right to *ask* for the role, but they don't have it yet.
2. Remove the Permanent "Active" Assignment: This is the most important part. Once you've made them eligible in PIM, you must go to the standard Access control (IAM) blade and remove their permanent role assignment. If you don't do this, nothing has changed, and they will still have standing access.

Step 3: Configure PIM Role Settings

Within PIM, you can define the rules for activating each role. You should configure these settings according to the client's security policy. Best practices include:

- Set a Maximum Activation Duration: Limit how long a user can have the role activated (e.g., 4 or 8 hours).
- Require Justification: Force users to enter a business reason for activating the role.
- Enforce Multi-Factor Authentication (MFA): Require users to verify their identity with MFA before an activation can be completed
- Require Approval: For the most critical roles like `Owner`, configure an approval workflow where a designated approver must grant the request before the role becomes active.

Step 4: Group-Based PIM Assignments

To make this manageable in the long term, you should strongly advocate for assigning PIM eligibility to groups rather than individual users.

- Example: Create a group called `Azure-Subscription-Owners`. Make this *group* eligible for the `Owner` role in PIM. Then, control who can be an owner simply by adding or removing them from this Azure AD group.

Step 5: Educate the Administrators

The client's administrators who need these roles will have a new process to follow. They need to be shown how to:

1. Go to the PIM section in the Azure portal.
2. Find their eligible roles.
3. Request activation, provide justification, and complete any required checks (like MFA).

Step 6: Use Access Reviews

Schedule regular "Access Reviews" within PIM. This feature prompts you or a designated reviewer (like a team manager) to periodically re-certify that users still require their eligible roles. If someone no longer needs access, it can be easily removed, preventing "privilege creep" over time.

By proposing this PIM implementation plan, you are guiding your client towards a much more secure and auditable Azure environment that aligns with modern security best practices.

## Andrew Bell

- Role: `User Access Administrator`
- Scope: `/` (Root)

Reason for access:

This user has the `User Access Administrator` role at the highest possible level (Root). This gives them the ability to manage user access to all resources in the entire Azure AD Tenant, which includes all subscriptions and, therefore, your resource group. This is inherited access.

---

## Cloud Admin

- Role: `User Access Administrator`
- Scope: `/` (Root)

Reason for access:

Same as Andrew Bell, this account has access because it holds the `User Access Administrator` role at the Root level, granting it permissions that are inherited by all resources below it. This is inherited access.

---

## Sean Donnelly

- Role: `User Access Administrator`
- Scope: `/` (Root)
- Role: `Owner`
- Scope: `/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541`

Reason for access:

This user has two powerful roles. The `Owner` role is assigned at the subscription level. Since your resource group `rg-ff-uks-gp-net` is inside this subscription, they inherit full Owner privileges on your resources. This is inherited access.

---

## Rachel Goodall

- Role: `User Access Administrator`
- Scope: `/` (Root)
- Role: `Owner`
- Scope: `/providers/Microsoft.Management/managementGroups/mg-cuh`

Reason for access:

This user has the `Owner` role at the 'mg-cuh' Management Group level. Assuming your subscription is under this management group, their permissions are inherited all the way down to your resources. This is inherited access.

---

## McKenna, Alexis

- Role: `User Access Administrator`
- Scope: `/` (Root)
- Role: `Owner`
- Scope: `/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541`
- Role: `Owner`
- Scope: `/providers/Microsoft.Management/managementGroups/mg-cuh`
- Role: `User Access Administrator`
- Scope: `/providers/Microsoft.Management/managementGroups/3d7d135a-ac7f-46ad-aa55-54639dd31d14`

Reason for access:

This user has multiple high-privilege roles at very high scopes, including `Owner` of your subscription and `Owner` of a management group above it. They have comprehensive access to your resources due to this inherited access.

---

## Michael Scullion

- Role: `User Access Administrator`
- Scope: `/` (Root)
- Role: `Owner`
- Scope: `/` (Root)
- Role: `Owner`
- Scope: `/providers/Microsoft.Management/managementGroups/mg-genprod`
- Role: `Owner`
- Scope: `/providers/Microsoft.Management/managementGroups/mg-landingzones`
- Role: `Owner`
- Scope: `/providers/Microsoft.Management/managementGroups/mg-cuh`

Reason for access:

This user has the most extensive permissions, including `Owner` at the Root level. This grants them full control over every resource in the entire directory. Their access to your resources is inherited from the highest possible level.

---

## David Sullivan

- Role: `User Access Administrator`
- Scope: `/` (Root)

Reason for access:

Similar to Andrew Bell and Cloud Admin, this user's access comes from the `User Access Administrator` role at the Root scope, which is inherited by all resources.

---

## Mark Talbot

- Role: `Security Admin`
- Scope: `/providers/Microsoft.Management/managementGroups/3d7d135a-ac7f-46ad-aa55-54639dd31d14`

Reason for access:

This user has the `Security Admin` role on a Management Group. This role allows them to manage security policies and read security configurations, which would include the resources in your subscription if it falls under this Management Group. This is inherited access.

The provided source material extensively discusses the principle of least privilege access, both as a general security best practice and in its specific application to the FITFILE resources within the CUH Azure environment. This concept is fundamental to securing distributed, cloud-native systems.

### What the Sources Say About Least Privilege Access to FITFILE Resources

The principle of least privilege dictates that a person or component should be granted only the bare minimum access required to perform their job. This minimises the potential impact of a compromise, reduces the attack surface, and enhances overall security. For FITFILE resources within the CUH Azure environment, several specific aspects highlight the commitment to and challenges of implementing least privilege:

1. Identity and Access Management (IAM) for Users and Service Principals: The "TT_CUH_FitFile_HLD" document explicitly states that Telefónica Tech will implement "strict access control policies" to prevent unauthorised access to the FitFile Environment. This includes the creation of a "secure Service Principal" for the deployment of the FITFILE Terraform script, which will be assigned "relevant permissions required to deploy the script". Similarly, "cloud only guest accounts" are recommended for third-party vendors, with access restricted through "Role Based Access Controls (RBAC)". CUH FITFILE team users will also have "Role based access controls (RBAC)" based on their individual access requirements. The document further defines specific roles for subscription access, such as "CUH Users Reader" and "Third Party vendors Contributor," implying varying levels of access that align with the principle of least privilege.

General guidance from other sources reinforces this: Kubernetes RBAC is designed to grant specific, minimal permissions to users and service accounts. It is recommended to use groups and roles rather than assigning permissions to individual users for easier management and auditing. Kubernetes RBAC mitigates privilege escalation by limiting an attacker's ability to edit roles or role bindings. Azure Role-Based Access Control (Azure RBAC) serves a similar function for Azure resources, enabling fine-grained access management and segregating duties. The goal is to avoid granting "unrestricted permissions" and instead assign roles that "only allow the identity to complete the task, and no more".

2. Application and Container Privilege Management: The principle of least privilege extends to the applications and containers running within the FITFILE environment. The sources strongly advocate for running containers with the "minimum possible privileges". This includes:

- Non-Root Users: Processes within containers should ideally run as an ordinary, non-root user. Kubernetes allows blocking containers from running as root and specifying a `runAsNonRoot: true` field.
- Disabling Privilege Escalation: The `allowPrivilegeEscalation` field should be set to `false` in a container's security policy to prevent binaries from gaining root privileges. This is also a recommended policy for Kubernetes clusters.
- Linux Capabilities: Linux capabilities offer granular control over privileges. The default set of capabilities for Docker containers is often too generous. Best practice is to "drop all capabilities for every container, and only add specific capabilities if they’re needed".
- Read-Only Filesystems: Many containers do not need to write to their own filesystem. Setting `readOnlyRootFilesystem: true` is good practice.
- Pod Security Contexts and Policies (PSPs): These mechanisms allow defining security settings at the Pod or cluster level, ensuring pods are created with the "minimum privileges needed for operation," thereby reducing the attack surface. PSPs enforce rules such as not running as root or privileged.
- Resource Limits and Quotas: Defining CPU and memory limits for pods prevents them from consuming excessive resources, safeguarding other applications and contributing to the stability of the host. Resource quotas can be applied at the namespace level to control resource consumption across teams or projects.

3. Network Access Controls: Network security is a critical facet of least privilege. For FITFILE, firewall rules are configured to allow outbound traffic on Port 443 (HTTPS) to a list of prescribed URLs, and inbound traffic from a list of prescribed IP addresses (Auth0), indicating explicit permission-based network access. This is consistent with best practices for network policies:

- Default Deny: It is strongly recommended to set up network policies that deny ingress and egress traffic by default and then add specific rules to permit only expected traffic.
- Microsegmentation: Containers facilitate granular firewalling and microsegmentation, allowing containers only a limited ability to communicate, thus limiting the "blast radius" of an attack.
- FQDN and L7 Policies: Advanced Container Networking Services (ACNS) in Azure Kubernetes Service (AKS) allow for Fully Qualified Domain Name (FQDN) filtering and Layer 7 (L7) policies, enabling granular control based on domain names and application-level attributes (like HTTP methods or gRPC paths), further enforcing least privilege at the network layer.
- VPC Endpoints and DNS Filtering: The issue with existing DNS endpoints in AWS preventing Terraform deployment [Notes from EoE] highlights the need for explicit control over network resolution, and Azure DNS security policies offer filtering and logging of DNS queries at the VNet level. Network Security Groups (NSGs) and User Defined Routes (UDRs) are used to filter and route traffic within the FITFILE vNet, restricting inbound and outbound flow.

4. Auditing and Monitoring for Compliance: Regular auditing and monitoring are crucial to ensuring least privilege is maintained. CUH is responsible for regularly auditing and monitoring access logs and compliance scores within the FitFile subscription. This aligns with general best practices recommending continuous auditing and monitoring for excessive access, abuse, or suspicious user behavior. Azure Monitor provides activity logging at the subscription level, and Microsoft Defender for Cloud offers recommendations and alerts related to resource security, including identity and access. Logging and threat detection are features that allow resource logs to provide enhanced service-specific metrics and logging, which can be sent to data sinks like Log Analytics workspace for security investigations.
5. Challenges and Considerations: Implementing least privilege is not without its challenges:

- Initial Broad Permissions: Documents like "FITFILE-Azure Deployment - Customer Checklist" mention granting "Contributor" access to the Subscription for a service principal and DevOps user. While necessary for initial setup, this is a highly privileged role, and the principle of least privilege implies these broad permissions should be refined to more specific roles post-initial deployment to reduce the "blast radius".
- Complexity: Detailed access control and granular permissions can introduce complexity. However, the sources argue that the security benefits outweigh this, especially for multi-tenant environments.
- Legacy Systems and Integration: The need for specific SQL credentials for the Bunny application and the FITFILE system to access OMOP data sources, with governance and security sign-off pending, shows that integrating with existing or on-premises systems can pose a challenge to implementing fine-grained access.
- Coordination and Planning: The "Navigating Complex Cloud Deployments" document highlights that a "lack of upfront information and coordination" regarding end-user and platform access (including DNS records) created "additional scope" and "firefighting". Proper upfront planning is essential for designing and implementing least privilege effectively.

In conclusion, the sources consistently advocate for the "principle of least privilege" as a cornerstone of security for FITFILE resources. This involves meticulous configuration of user and service principal roles via RBAC, granular control over container privileges (non-root, capabilities, privilege escalation), stringent network access policies, and robust auditing. While the implementation faces practical challenges related to initial setup permissions, integration, and planning, the core strategy aligns with empowering teams to manage security responsibly within their defined boundaries, thereby strengthening the overall security posture of the FITFILE environment.

Based on the provided materials, the core principle guiding access to FITFILE resources in Azure is the Principle of Least Privilege (PoLP). This principle dictates that users, service principals, and applications should only be granted the minimum permissions necessary to perform their required tasks, thereby limiting the potential impact of a security breach. Azure's Role-Based Access Control (RBAC) system is the primary mechanism for enforcing these permissions.

The report you've provided details inherited access, meaning that roles assigned at a higher scope (like the entire Azure AD Tenant, a Management Group, or the Subscription level) flow down to all resources beneath them, including your `rg-ff-uks-gp-net` resource group. The `rg-ff-uks-gp-net` resource group is specifically designated for virtual network resources (vNet, NSG, Route tables) within the FITFILE environment.

Let's break down the reported access for each individual and assess its alignment with the established security posture:

### Analysis of Inherited Access for Individuals

1. Andrew Bell

- Role: `User Access Administrator`
- Scope: `/` (Root)
- Reason for Access: This role at the root scope grants Andrew Bell the ability to manage user access to *all* resources in the entire Azure AD Tenant, which includes all subscriptions and, consequently, your `rg-ff-uks-gp-net` resource group. The `User Access Administrator` role "lets you manage user access to Azure resources".
- Alignment: While this role provides significant control over access assignments, its assignment at the root scope is a very broad privilege. The Principle of Least Privilege suggests that such powerful roles should be carefully controlled and ideally time-limited or scoped more narrowly if the day-to-day duties do not require tenant-wide access management. This level of access goes beyond merely managing resources within a specific subscription.

2. Cloud Admin

- Role: `User Access Administrator`
- Scope: `/` (Root)
- Reason for Access: Similar to Andrew Bell, this account has inherited access due to holding the `User Access Administrator` role at the Root level, granting it permissions over all resources below it.
- Alignment: The same concerns apply here as for Andrew Bell. A `User Access Administrator` role at the root scope provides extensive permissions, potentially exceeding the principle of least privilege for routine operations.

3. Sean Donnelly

- Role: `User Access Administrator` (Scope: `/` Root)
- Role: `Owner` (Scope: `/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541`)
- Reason for Access: Sean Donnelly holds two very powerful roles. The `Owner` role is assigned at the subscription level, which means they have full control over all resources within that subscription, including the `rg-ff-uks-gp-net` resource group, because permissions are inherited. The `User Access Administrator` role at the root level further adds broad access management capabilities. It is mentioned that Sean Donnelly is involved in the CUH deployment status and security review of FITFILE infrastructure. He also assists Leon with network configurations, including peering and route tables.
- Alignment: Having `Owner` access at the subscription level and `User Access Administrator` at root provides comprehensive control. While "Subscription Administrator Owner" is a role reserved for CUH and Telefónica Tech administrative users, and Leon (who is responsible for AKS infrastructure deployment) was granted "Contributor" access on the FITFILE subscription, `Owner` is a higher privilege than `Contributor`. While such broad access might be necessary for high-level administration or initial setup (e.g., for a "Service Principal" or "FITFILE DevOps user" during deployment, Contributor access to the Subscription is required), for day-to-day operations, the Principle of Least Privilege would suggest more granular access where possible.

4. Rachel Goodall

- Role: `User Access Administrator` (Scope: `/` Root)
- Role: `Owner` (Scope: `/providers/Microsoft.Management/managementGroups/mg-cuh`)
- Reason for Access: Rachel Goodall has the `Owner` role assigned at the `mg-cuh` Management Group level. Assuming your subscription is under this management group (as stated that "An FITFILE subscription will be added to the General Production management group"), her permissions are inherited down to your resources.
- Alignment: Similar to Sean Donnelly, these roles provide broad, inherited access across the management group. This level of access extends across all subscriptions under `mg-cuh`, which might encompass more resources than strictly necessary for specific FITFILE operations, again potentially deviating from least privilege for daily tasks.

5. McKenna, Alexis

- Role: `User Access Administrator` (Scope: `/` Root)
- Role: `Owner` (Scope: `/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541`)
- Role: `Owner` (Scope: `/providers/Microsoft.Management/managementGroups/mg-cuh`)
- Role: `User Access Administrator` (Scope: `/providers/Microsoft.Management/managementGroups/3d7d135a-ac7f-46ad-aa55-54639dd31d14`)
- Reason for Access: Alexis McKenna possesses multiple high-privilege roles at various high scopes, including `Owner` of your specific subscription and `Owner` of a management group above it. She also has `User Access Administrator` roles at both the root and another management group level. This provides comprehensive, extensive inherited access to your resources. Alexis is also mentioned in the context of CUH signing off on changes.
- Alignment: The sheer number and breadth of high-privilege roles assigned to Alexis McKenna (`Owner` and `User Access Administrator` at multiple high levels) grants her significant control over the entire Azure environment including your FITFILE subscription. This is a very powerful set of permissions that, if not strictly managed through Just-in-Time (JIT) access or similar mechanisms, would directly contradict the Principle of Least Privilege for standard operational duties.

6. Michael Scullion

- Role: `User Access Administrator` (Scope: `/` Root)
- Role: `Owner` (Scope: `/` Root)
- Role: `Owner` (Scope: `/providers/Microsoft.Management/managementGroups/mg-genprod`)
- Role: `Owner` (Scope: `/providers/Microsoft.Management/managementGroups/mg-landingzones`)
- Role: `Owner` (Scope: `/providers/Microsoft.Management/managementGroups/mg-cuh`)
- Reason for Access: Michael Scullion has an even broader set of `Owner` roles, including at the root (`/`) level and across multiple management groups (`mg-genprod`, `mg-landingzones`, `mg-cuh`), in addition to `User Access Administrator` at root. These roles collectively provide maximum possible inherited access to all resources within these scopes.
- Alignment: This level of access is the most extensive in the report. Being an `Owner` at the root scope grants "full access to all resources including the right to delegate access to others". This is an administrative super-user equivalent. While potentially necessary for extremely high-level platform architects or auditors, having such wide-ranging permanent access for multiple individuals greatly increases the attack surface and is a significant deviation from the Principle of Least Privilege.

7. David Sullivan

- Role: `User Access Administrator`
- Scope: `/` (Root)
- Reason for Access: Similar to Andrew Bell and Cloud Admin, David Sullivan's access is derived from the `User Access Administrator` role at the Root scope, which is inherited by all resources.
- Alignment: The same concerns apply here as for Andrew Bell and Cloud Admin regarding the broadness of the `User Access Administrator` role at the root scope.

8. Mark Talbot

- Role: `Security Admin`
- Scope: `/providers/Microsoft.Management/managementGroups/3d7d135a-ac7f-46ad-aa55-54639dd31d14`
- Reason for Access: Mark Talbot has the `Security Admin` role on a specific Management Group. This role grants permissions to manage security policies and read security configurations, which would include your `rg-ff-uks-gp-net` resource group if it falls under this Management Group.
- Alignment: The `Security Admin` role provides significant security-related permissions, albeit at a management group scope rather than subscription. While managing security is crucial, the PoLP would still advocate for the most restrictive set of permissions required for the specific tasks, and continuous auditing of such roles.

### Overall Alignment with Stated Principles

1. Principle of Least Privilege (PoLP): The report highlights a significant number of individuals with highly privileged roles (`Owner`, `User Access Administrator`) at very broad scopes (root, subscription, or management group levels). While these roles provide the technical capability to manage resources, including the FITFILE subscription and its resource groups, they do not fully align with the rigorous application of PoLP for day-to-day operations. The sources consistently recommend granting "only the minimum permissions necessary" and segregating duties to "limit the potential attack surface". Broad permissions assigned at higher levels mean that if any of these highly privileged accounts are compromised, the attacker would gain extensive control across a wide range of Azure resources, not just those directly related to FITFILE.
2. Explicit Role Assignments: The `FITFILE Azure Deployment - Customer Checklist` states that a "service principal" and a "FITFILE DevOps user" need "Contributor access to the Subscription" for deployment. Leon's access is confirmed as "Contributor" on the FITFILE subscription, aligning with this. However, the roles reported for most individuals (Owner, User Access Administrator) are *more* permissive than Contributor.
3. Authentication and Auditing: The sources state that "Multi-factor authentication is enabled on all synchronised and cloud-only accounts". CUH is also "responsible for regularly audit[ing] and monitor[ing] access logs" and "implement[ing] access controls, and regularly audit[ing] compliance score[s]". While the report on inherited access doesn't directly confirm MFA enforcement or audit frequency, the existence of these broad roles makes robust auditing and enforcement of MFA even more critical to mitigate the inherent risk.
4. Security Responsibility: CUH is responsible for "management and security monitoring of FitFile subscription". Telefónica Tech is responsible for "implement[ing] multi-factor authentication and strict access control policies". The report indicates that the "strict access control policies" might not be fully applied in practice if these broad roles are for ongoing, rather than temporary, high-level administrative tasks.

### Conclusion on Alignment

The report aligns in principle with the use of Azure RBAC for managing access and the understanding that permissions are inherited from higher scopes. However, the prevalence of broadly scoped, highly privileged roles (`Owner`, `User Access Administrator`, `Security Admin` at root, subscription, or management group levels) for multiple individuals suggests a potential deviation from the strict application of the Principle of Least Privilege for ongoing operational access. While some high-level roles are necessary for initial deployment and core administration, a large number of individuals holding such wide-ranging inherited permissions increases security risk by providing more access than might be strictly necessary for their daily tasks.

To truly align with the stated security posture, a deeper look might be warranted to confirm if these broad permissions are temporary (e.g., for deployment or specific, infrequent high-privilege operations) or if more granular, just-in-time access (JIT) strategies are being employed to reduce the standing privileges of these accounts.

Having high-level access spread across multiple teams introduces several significant security risks, primarily due to the principle of inherited access in Azure and the general challenges of managing privileges in complex, distributed systems like Kubernetes.

Here's a breakdown of the key risks:

1. Violation of the Principle of Least Privilege
   - Many individuals across different teams, such as Andrew Bell, Cloud Admin, Sean Donnelly, Rachel Goodall, Alexis McKenna, Michael Scullion, and David Sullivan, have roles like `User Access Administrator` and `Owner` assigned at broad scopes (e.g., `/` (Root), Management Group, or the entire Subscription). Michael Scullion, for instance, has `Owner` access at the Root level, granting full control over every resource in the entire directory. Sean Donnelly and Alexis McKenna also have `Owner` roles at the subscription level. These powerful roles' permissions are inherited by all resources underneath them, including your `rg-ff-uks-gp-net` resource group.
   - This broad access directly contravenes the principle of least privilege, which dictates that individuals and components should only have the bare minimum access required to perform their job functions. Giving users more privileges than necessary increases the exposure of an account to attackers.

2. Increased Attack Surface and Accidental Misconfigurations
   - The more complex a system, the more likely it is to have vulnerabilities. Broadly assigned high-level privileges increase the overall attack surface by providing more potential entry points for malicious actors.
   - As an organization grows, it becomes increasingly risky for everyone to have administrator rights, as it's too easy for someone to make a mistake and inadvertently change something they shouldn't. These security misconfigurations are a common attack vector.

3. Higher Risk of Privilege Escalation
   - If an attacker gains an initial foothold, broad permissions held by multiple users make it significantly easier to escalate privileges. Privilege escalation involves extending beyond intended permissions by exploiting system vulnerabilities or poor configuration.
   - For example, if processes inside containers are running as the `root` user by default (which is a common insecure configuration), an attacker who manages to escape the container will instantly gain `root` privileges on the host machine, bypassing further privilege escalation steps.
   - Even if a container runs as a non-root user, there's still potential for privilege escalation based on Linux permissions. The `cluster-admin` role in Kubernetes is a superuser equivalent to `root` on Unix systems and should be guarded carefully, never given to non-cluster operators or internet-exposed service accounts.

4. Compromised Credentials and Insider Threats
   - High-level access across many individuals increases the risk that one of these privileged accounts could be compromised. Attackers frequently target privileged accounts to gain complete control of an organization's data and systems.
   - Even accidental commitment of plain-text secrets to version control is a serious risk; any such secret should be considered compromised and rotated immediately. The "FITFILE" checklist mentions the need for CUH to provide SQL credentials, and the risk of pulling resources bypassing the CUH on-premise firewall, which could expose data if credentials or access points are compromised.

5. Challenges in Auditing and Accountability
   - When many users have high-level access, it becomes challenging to track and audit specific actions, making it harder to determine who was responsible if a malicious action occurs. A lack of an audit trail for secrets management, for example, is a significant drawback. Effective security requires continuous auditing and monitoring of access to resources to detect excessive access, abuse, or suspicious user behavior.

6. Weakened Segregation of Duties
   - The principle of segregation of duties advocates for different components or people having authority over only the smallest subset of the system needed for their tasks, which limits the damage a single privileged user might inflict. When high-level access is spread broadly without strict controls, this principle is violated, increasing the blast radius of any security incident.

7. Complex Secrets Management
   - High-level access can expose secrets such as passwords, API tokens, and TLS certificates. Secrets stored in plain text (like Base64 encoding in etcd) or retrieved/sent in plain text are vulnerable unless encryption is configured.
   - Organizations need a centralized secrets management strategy to avoid "secrets sprawl" (secrets spread across config files, YAMLs, Git repositories), with proper authorization, logging, monitoring, and automated rotation. Without it, many individuals with high access might inadvertently expose critical credentials.

8. Multi-Tenancy Risks
   - While containers offer a security boundary, their isolation is not as strong as virtual machines (VMs). All containers on a given host share the same kernel. If containers run as `root` by default, and access is not tightly controlled, compromising one container could lead to host takeover.
   - In a multi-tenant environment where multiple teams (or even external parties) share infrastructure, if one tenant is compromised due to broad access, it can impact the security of other services. Any privileged container on the same host can have full access to any other container, regardless of Kubernetes namespaces.

In summary, broad, high-level access across multiple teams creates a larger attack surface, increases the likelihood and impact of accidental misconfigurations or malicious activity, complicates auditing, and undermines fundamental security principles like least privilege and segregation of duties.
