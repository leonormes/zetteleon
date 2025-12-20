---
aliases: []
confidence: 
created: 2025-03-12T18:26:03Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [IAM]
title: Securing the Root Identity
type: 
uid: 
updated: 
version: 
---

The root identity, typically the initial Global Administrator account, holds the highest level of privilege in your Azure tenant. Securing this identity is paramount to maintaining the overall security of your environment. Here are some key measures to consider:

- **Enable Multi-Factor Authentication (MFA):** MFA adds an extra layer of security by requiring multiple forms of verification to access your account.
- **Use Privileged Identity Management (PIM):** PIM allows you to grant just-in-time privileged access to Azure resources, reducing the exposure time of privileges and increasing visibility into their use.
- **Limit Standing Privileges:** Avoid assigning permanent Global Administrator roles. Instead, use PIM to grant temporary access when needed.
- **Monitor for Suspicious Activities:** Regularly monitor Azure AD sign-in logs and audit logs for any unusual activities.
- **Use Cloud-Only Accounts for Azure Roles:** Create dedicated cloud-only accounts for administrative roles in Azure, ensuring they are not synchronized with on-premises Active Directory.
- **Use Temporary Access Pass (TAP) for Passwordless Authentication:** Temporary Access Pass (TAP) allows users to register passwordless authentication methods, such as Windows Hello for Business or FIDO2 security keys, during their initial sign-in. This eliminates the need for a password during the registration process6.

It's important to recognize the shift in security perimeter from traditional network security to identity. Identity is now considered the primary security perimeter in cloud environments. This means that securing identities and controlling access is crucial for protecting your Azure tenant.
